"""
Core components of Smart Home - The Next Generation.

Smart Home - TNG is a Home Automation framework for observing the state
of entities and react to changes. It is based on Home Assistant from
home-assistant.io and the Home Assistant Community.

Copyright (c) 2022-2023, Andreas Nixdorf

This program is free software: you can redistribute it and/or
modify it under the terms of the GNU General Public License as
published by the Free Software Foundation, either version 3 of
the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
General Public License for more details.

You should have received a copy of the GNU General Public
License along with this program.  If not, see
http://www.gnu.org/licenses/.
"""

import asyncio
import collections.abc
import logging
import types
import typing

from . import helpers
from .callback import callback
from .config_entries_flow_manager import ConfigEntriesFlowManager
from .config_entry import ConfigEntry
from .config_entry_change import ConfigEntryChange
from .config_entry_disabler import ConfigEntryDisabler
from .config_entry_source import ConfigEntrySource
from .config_entry_state import ConfigEntryState
from .config_type import ConfigType
from .const import Const
from .entity_registry_disabled_handler import EntityRegistryDisabledHandler
from .event import Event
from .operation_not_allowed import OperationNotAllowed
from .options_flow_manager import OptionsFlowManager
from .platform import Platform
from .smart_home_controller_error import SmartHomeControllerError
from .store import Store
from .unknown_entry import UnknownEntry
from .entity_registry_disabled_handler import _RELOAD_AFTER_UPDATE_DELAY

_STORAGE_KEY: typing.Final = "core.config_entries"
_STORAGE_VERSION: typing.Final = 1
_UNDEFINED: typing.Final = object()
_SAVE_DELAY: typing.Final = 1
# Deprecated since 0.73
_PATH_CONFIG: typing.Final = ".config_entries.json"


if not typing.TYPE_CHECKING:

    class SmartHomeController:
        ...


if typing.TYPE_CHECKING:
    from .smart_home_controller import SmartHomeController


# pylint: disable=unused-variable
class ConfigEntries:
    """Manage the configuration entries.

    An instance of this object is available via `shc.config_entries`.
    """

    RELOAD_AFTER_UPDATE_DELAY: typing.Final = _RELOAD_AFTER_UPDATE_DELAY

    def __init__(self, shc: SmartHomeController, config: ConfigType) -> None:
        """Initialize the entry manager."""
        self._shc = shc
        self._flow = ConfigEntriesFlowManager(shc, self, config)
        self._options = OptionsFlowManager(shc)
        self._config = config
        self._entries: dict[str, ConfigEntry] = {}
        self._domain_index: dict[str, list[str]] = {}
        self._store = Store[dict[str, list[dict[str, typing.Any]]]](
            shc, _STORAGE_VERSION, _STORAGE_KEY
        )
        EntityRegistryDisabledHandler(shc).async_setup()

    @property
    def flow(self) -> ConfigEntriesFlowManager:
        return self._flow

    @property
    def options(self) -> OptionsFlowManager:
        return self._options

    @callback
    def async_domains(
        self, include_ignore: bool = False, include_disabled: bool = False
    ) -> list[str]:
        """Return domains for which we have entries."""
        return list(
            {
                entry.domain: None
                for entry in self._entries.values()
                if (include_ignore or entry.source != ConfigEntrySource.IGNORE)
                and (include_disabled or not entry.disabled_by)
            }
        )

    @callback
    def async_get_entry(self, entry_id: str) -> ConfigEntry:
        """Return entry with matching entry_id."""
        return self._entries.get(entry_id)

    @callback
    def async_entries(self, domain: str = None) -> list[ConfigEntry]:
        """Return all entries or entries for a specific domain."""
        if domain is None:
            return list(self._entries.values())
        return [
            self._entries[entry_id] for entry_id in self._domain_index.get(domain, [])
        ]

    @callback
    def _dispatch_entry_changed(
        self, change: ConfigEntryChange, entry: ConfigEntry
    ) -> None:
        self._shc.dispatcher.async_send(
            ConfigEntry.SIGNAL_CONFIG_ENTRY_CHANGED, change, entry
        )

    async def async_add(self, entry: ConfigEntry) -> None:
        """Add and setup an entry."""
        if entry.entry_id in self._entries:
            raise SmartHomeControllerError(
                f"An entry with the id {entry.entry_id} already exists."
            )
        self._entries[entry.entry_id] = entry
        self._domain_index.setdefault(entry.domain, []).append(entry.entry_id)
        self._dispatch_entry_changed(ConfigEntryChange.ADDED, entry)
        await self.async_setup(entry.entry_id)
        self._async_schedule_save()

    async def async_remove(self, entry_id: str) -> dict[str, typing.Any]:
        """Remove an entry."""
        if (entry := self.async_get_entry(entry_id)) is None:
            raise UnknownEntry

        if not entry.state.recoverable:
            unload_success = entry.state is not ConfigEntryState.FAILED_UNLOAD
        else:
            unload_success = await self.async_unload(entry_id)

        await entry.async_remove(self._shc)

        del self._entries[entry.entry_id]
        self._domain_index[entry.domain].remove(entry.entry_id)
        if not self._domain_index[entry.domain]:
            del self._domain_index[entry.domain]
        self._async_schedule_save()

        dev_reg = self._shc.device_registry
        ent_reg = self._shc.entity_registry

        dev_reg.async_clear_config_entry(entry_id)
        ent_reg.async_clear_config_entry(entry_id)

        # If the configuration entry is removed during reauth, it should
        # abort any reauth flow that is active for the removed entry.
        for progress_flow in self._flow.async_progress_by_handler(entry.domain):
            context = progress_flow.get("context")
            if (
                context
                and context["source"] == ConfigEntrySource.REAUTH
                and "entry_id" in context
                and context["entry_id"] == entry_id
                and "flow_id" in progress_flow
            ):
                self._flow.async_abort(progress_flow["flow_id"])

        # After we have fully removed an "ignore" config entry we can try and
        # rediscover it so that a user is able to immediately start configuring
        # it. We do this by starting a new flow with the 'unignore' step. If the
        # integration doesn't implement async_step_unignore then this will be a
        # no-op.
        if entry.source == ConfigEntrySource.IGNORE:
            self._shc.async_create_task(
                self._flow.async_init(
                    entry.domain,
                    context={"source": ConfigEntrySource.UNIGNORE},
                    data={"unique_id": entry.unique_id},
                )
            )

        self._dispatch_entry_changed(ConfigEntryChange.REMOVED, entry)
        return {"require_restart": not unload_success}

    async def _async_shutdown(self, _event: Event) -> None:
        """Call when Home Assistant is stopping."""
        await asyncio.gather(
            *(entry.async_shutdown() for entry in self._entries.values())
        )
        await self.flow.async_shutdown()

    async def async_initialize(self) -> None:
        """Initialize config entry config."""
        # Migrating for config entries stored before 0.73
        config = await self._shc.async_migrator(
            self._shc.config.path(_PATH_CONFIG),
            self._store,
            old_conf_migrate_func=_old_conf_migrator,
        )

        self._shc.bus.async_listen_once(Const.EVENT_SHC_CLOSE, self._async_shutdown)

        if config is None:
            self._entries = {}
            self._domain_index = {}
            return

        entries = {}
        domain_index: dict[str, list[str]] = {}

        for entry in config["entries"]:
            pref_disable_new_entities = entry.get("pref_disable_new_entities")

            # Between 0.98 and 2021.6 we stored 'disable_new_entities'
            # in a system options dictionary
            if pref_disable_new_entities is None and "system_options" in entry:
                pref_disable_new_entities = entry.get("system_options", {}).get(
                    "disable_new_entities"
                )

            domain = entry["domain"]
            entry_id = entry["entry_id"]

            entries[entry_id] = ConfigEntry(
                version=entry["version"],
                domain=domain,
                entry_id=entry_id,
                data=entry["data"],
                source=entry["source"],
                title=entry["title"],
                # New in 0.89
                options=entry.get("options"),
                # New in 0.104
                unique_id=entry.get("unique_id"),
                # New in 2021.3
                disabled_by=ConfigEntryDisabler(entry["disabled_by"])
                if entry.get("disabled_by")
                else None,
                # New in 2021.6
                pref_disable_new_entities=pref_disable_new_entities,
                pref_disable_polling=entry.get("pref_disable_polling"),
            )
            domain_index.setdefault(domain, []).append(entry_id)

        self._domain_index = domain_index
        self._entries = entries

    async def async_setup(self, entry_id: str) -> bool:
        """Set up a config entry.

        Return True if entry has been successfully loaded.
        """
        if (entry := self.async_get_entry(entry_id)) is None:
            raise UnknownEntry

        if entry.state is not ConfigEntryState.NOT_LOADED:
            raise OperationNotAllowed

        # Setup Component if not set up yet
        if entry.domain in self._shc.config.components:
            await entry.async_setup(self._shc)
        else:
            # Setting up the component will set up all its config entries
            result = await self._shc.setup.async_setup_component(
                entry.domain, self._config
            )

            if not result:
                return result

        return entry.state is ConfigEntryState.LOADED

    async def async_unload(self, entry_id: str) -> bool:
        """Unload a config entry."""
        if (entry := self.async_get_entry(entry_id)) is None:
            raise UnknownEntry

        if not entry.state.recoverable:
            raise OperationNotAllowed

        return await entry.async_unload(self._shc)

    async def async_reload(self, entry_id: str) -> bool:
        """Reload an entry.

        If an entry was not loaded, will just load.
        """
        if (entry := self.async_get_entry(entry_id)) is None:
            raise UnknownEntry

        async with entry.reload_lock:
            unload_result = await self.async_unload(entry_id)

            if not unload_result or entry.disabled_by:
                return unload_result

            return await self.async_setup(entry_id)

    async def async_set_disabled_by(
        self, entry_id: str, disabled_by: ConfigEntryDisabler
    ) -> bool:
        """Disable an entry.

        If disabled_by is changed, the config entry will be reloaded.
        """
        if (entry := self.async_get_entry(entry_id)) is None:
            raise UnknownEntry

        if isinstance(disabled_by, str) and not isinstance(
            disabled_by, ConfigEntryDisabler
        ):
            self._shc.report(
                "uses str for config entry disabled_by. This is deprecated and will "
                + "stop working in Home Assistant 2022.3, it should be updated to use "
                + "ConfigEntryDisabler instead",
                error_if_core=False,
            )
            disabled_by = ConfigEntryDisabler(disabled_by)

        if entry.disabled_by is disabled_by:
            return True

        # pylint: disable=protected-access
        entry._disabled_by = disabled_by
        self._async_schedule_save()

        dev_reg = self._shc.device_registry
        ent_reg = self._shc.entity_registry

        if not entry.disabled_by:
            # The config entry will no longer be disabled, enable devices and entities
            dev_reg.async_config_entry_disabled_by_changed(entry)
            ent_reg.async_config_entry_disabled_by_changed(entry)

        # Load or unload the config entry
        reload_result = await self.async_reload(entry_id)

        if entry.disabled_by:
            # The config entry has been disabled, disable devices and entities
            dev_reg.async_config_entry_disabled_by_changed(entry)
            ent_reg.async_config_entry_disabled_by_changed(entry)

        return reload_result

    @callback
    def async_update_entry(
        self,
        entry: ConfigEntry,
        *,
        unique_id: str | object = _UNDEFINED,
        title: str | object = _UNDEFINED,
        data: collections.abc.Mapping[str, typing.Any] | object = _UNDEFINED,
        options: collections.abc.Mapping[str, typing.Any] | object = _UNDEFINED,
        pref_disable_new_entities: bool | object = _UNDEFINED,
        pref_disable_polling: bool | object = _UNDEFINED,
    ) -> bool:
        """Update a config entry.

        If the entry was changed, the update_listeners are
        fired and this function returns True

        If the entry was not changed, the update_listeners are
        not fired and this function returns False
        """
        changed = False

        for attr, value in (
            ("_unique_id", unique_id),
            ("_title", title),
            ("_pref_disable_new_entities", pref_disable_new_entities),
            ("_pref_disable_polling", pref_disable_polling),
        ):
            if value == _UNDEFINED or getattr(entry, attr) == value:
                continue

            setattr(entry, attr, value)
            changed = True

        if data is not _UNDEFINED and entry.data != data:
            changed = True
            # pylint: disable=protected-access
            entry._data = types.MappingProxyType(data)

        if options is not _UNDEFINED and entry.options != options:
            changed = True
            # pylint: disable=protected-access
            entry._options = types.MappingProxyType(options)

        if not changed:
            return False

        for listener_ref in entry.update_listeners:
            if (listener := listener_ref()) is not None:
                self._shc.async_create_task(listener(self._shc, entry))

        self._async_schedule_save()
        self._dispatch_entry_changed(ConfigEntryChange.UPDATED, entry)
        return True

    @callback
    def async_setup_platforms(
        self, entry: ConfigEntry, platforms: typing.Iterable[Platform | str]
    ) -> None:
        """Forward the setup of an entry to platforms."""
        helpers.report(
            "called async_setup_platforms instead of awaiting async_forward_entry_setups; "
            + "this will fail in version 2022.12",
            # Raise this to warning once all core integrations have been migrated
            level=logging.DEBUG,
            error_if_core=False,
        )
        for platform in platforms:
            self._shc.async_create_task(self.async_forward_entry_setup(entry, platform))

    async def async_forward_entry_setups(
        self, entry: ConfigEntry, platforms: typing.Iterable[Platform | str]
    ) -> None:
        """Forward the setup of an entry to platforms."""
        await asyncio.gather(
            *(self.async_forward_entry_setup(entry, platform) for platform in platforms)
        )

    async def async_forward_entry_setup(
        self, entry: ConfigEntry, domain: Platform | str
    ) -> bool:
        """Forward the setup of an entry to a different component.

        By default an entry is setup with the component it belongs to. If that
        component also has related platforms, the component will have to
        forward the entry to be setup by that component.

        You don't want to await this coroutine if it is called as part of the
        setup of a component, because it can cause a deadlock.
        """
        # Setup Component if not set up yet
        domain = str(domain)
        if domain not in self._shc.config.components:
            result = await self._shc.setup.async_setup_component(domain, self._config)

            if not result:
                return False

        integration = await self._shc.setup.async_get_integration(domain)

        await entry.async_setup(self._shc, integration=integration)
        return True

    async def async_unload_platforms(
        self, entry: ConfigEntry, platforms: collections.abc.Iterable[Platform | str]
    ) -> bool:
        """Forward the unloading of an entry to platforms."""
        return all(
            await asyncio.gather(
                *(
                    self.async_forward_entry_unload(entry, platform)
                    for platform in platforms
                )
            )
        )

    async def async_forward_entry_unload(
        self, entry: ConfigEntry, domain: Platform | str
    ) -> bool:
        """Forward the unloading of an entry to a different component."""
        # It was never loaded.
        if domain not in self._shc.config.components:
            return True

        integration = await self._shc.setup.async_get_integration(domain)

        return await entry.async_unload(self._shc, integration=integration)

    @callback
    def _async_schedule_save(self) -> None:
        """Save the entity registry to a file."""
        self._store.async_delay_save(self._data_to_save, _SAVE_DELAY)

    @callback
    def _data_to_save(self) -> dict[str, list[dict[str, typing.Any]]]:
        """Return data to save."""
        return {"entries": [entry.as_dict() for entry in self._entries.values()]}

    @staticmethod
    async def _old_conf_migrator(
        old_config: dict[str, typing.Any]
    ) -> dict[str, typing.Any]:
        """Migrate the pre-0.73 config format to the latest version."""
        return {"entries": old_config}


async def _old_conf_migrator(
    old_config: dict[str, typing.Any]
) -> dict[str, typing.Any]:
    """Migrate the pre-0.73 config format to the latest version."""
    return {"entries": old_config}
