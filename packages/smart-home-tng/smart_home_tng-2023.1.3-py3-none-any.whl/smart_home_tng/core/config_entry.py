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
import collections
import collections.abc
import contextvars
import functools
import logging
import types
import typing
import weakref

from . import helpers
from .callback import callback
from .callback_type import CallbackType
from .config_entry_auth_failed import ConfigEntryAuthFailed
from .config_entry_change import ConfigEntryChange
from .config_entry_disabler import ConfigEntryDisabler
from .config_entry_not_ready import ConfigEntryNotReady
from .config_entry_source import ConfigEntrySource
from .config_entry_state import ConfigEntryState
from .config_flow import _CONFIG_HANDLERS
from .config_flow_platform import ConfigFlowPlatform
from .const import Const
from .core_state import CoreState
from .entity_registry_entry_disabler import EntityRegistryEntryDisabler
from .event import Event
from .integration import Integration
from .integration_not_found import IntegrationNotFound
from .platform import Platform
from .smart_home_controller_component import SmartHomeControllerComponent

_LOGGER: typing.Final = logging.getLogger(__name__)

_SOURCE_IGNORE: typing.Final = ConfigEntrySource.IGNORE.value

if not typing.TYPE_CHECKING:

    class SmartHomeController:
        pass


if typing.TYPE_CHECKING:
    from .smart_home_controller import SmartHomeController


UpdateListenerType: typing.TypeAlias = typing.Callable[
    [SmartHomeController, "ConfigEntry"],
    typing.Coroutine[typing.Any, typing.Any, None],
]


# pylint: disable=unused-variable
class ConfigEntry:
    """Hold a configuration entry."""

    EVENT_FLOW_DISCOVERED: typing.Final = "config_entry.discovered"
    DISCOVERY_NOTIFICATION_ID: typing.Final = "config_entry.discovery"
    SIGNAL_CONFIG_ENTRY_CHANGED: typing.Final = "config_entry.changed"
    RECONFIGURE_NOTIFICATION_ID: typing.Final = "config_entry.reconfigure"

    __slots__ = (
        "_entry_id",
        "_version",
        "_domain",
        "_title",
        "_data",
        "_options",
        "_unique_id",
        "_supports_unload",
        "_supports_remove_device",
        "_pref_disable_new_entities",
        "_pref_disable_polling",
        "_source",
        "_state",
        "_disabled_by",
        "_setup_lock",
        "_update_listeners",
        "_reason",
        "_async_cancel_retry_setup",
        "_on_unload",
        "_reload_lock",
    )

    def __init__(
        self,
        version: int,
        domain: str,
        title: str,
        data: collections.abc.Mapping[str, typing.Any],
        source: str,
        pref_disable_new_entities: bool = None,
        pref_disable_polling: bool = None,
        options: collections.abc.Mapping[str, typing.Any] = None,
        unique_id: str = None,
        entry_id: str = None,
        state: ConfigEntryState = ConfigEntryState.NOT_LOADED,
        disabled_by: ConfigEntryDisabler = None,
    ) -> None:
        """Initialize a config entry."""
        # Unique id of the config entry
        self._entry_id = entry_id or helpers.random_uuid_hex()

        # Version of the configuration.
        self._version = version

        # Domain the configuration belongs to
        self._domain = domain

        # Title of the configuration
        self._title = title

        # Config data
        self._data = types.MappingProxyType(data)

        # Entry options
        self._options = types.MappingProxyType(options or {})

        # Entry system options
        if pref_disable_new_entities is None:
            pref_disable_new_entities = False

        self._pref_disable_new_entities = pref_disable_new_entities

        if pref_disable_polling is None:
            pref_disable_polling = False

        self._pref_disable_polling = pref_disable_polling

        # Source of the configuration (user, discovery, cloud)
        self._source = source

        # State of the entry (LOADED, NOT_LOADED)
        self._state = state

        # Unique ID of this entry.
        self._unique_id = unique_id

        # Config entry is disabled
        if isinstance(disabled_by, str) and not isinstance(
            disabled_by, ConfigEntryDisabler
        ):
            helpers.report(
                "uses str for config entry disabled_by. This is deprecated and will "
                + "stop working in Home Assistant 2022.3, it should be updated to use "
                + "ConfigEntryDisabler instead",
                error_if_core=False,
            )
            disabled_by = ConfigEntryDisabler(disabled_by)
        self._disabled_by = disabled_by

        # Supports unload
        self._supports_unload = False

        # Supports remove device
        self._supports_remove_device = False

        # Listeners to call on update
        self._update_listeners: list[
            weakref.ReferenceType[UpdateListenerType] | weakref.WeakMethod
        ] = []

        # Reason why config entry is in a failed state
        self._reason: str = None

        # Function to cancel a scheduled retry
        self._async_cancel_retry_setup: typing.Callable[[], typing.Any] = None

        # Hold list for functions to call on unload.
        self._on_unload: list[CallbackType] = None

        # Reload lock to prevent conflicting reloads
        self._reload_lock = asyncio.Lock()

    @property
    def supports_unload(self) -> bool:
        return self._supports_unload

    @property
    def supports_remove_device(self) -> bool:
        return self._supports_remove_device

    @property
    def disabled_by(self) -> ConfigEntryDisabler:
        return self._disabled_by

    @property
    def reason(self) -> str:
        return self._reason

    @property
    def reload_lock(self) -> asyncio.Lock:
        return self._reload_lock

    @property
    def entry_id(self) -> str:
        return self._entry_id

    @property
    def version(self) -> int:
        return self._version

    @property
    def domain(self) -> str:
        return self._domain

    @property
    def unique_id(self) -> str:
        return self._unique_id

    @property
    def pref_disable_new_entities(self) -> bool:
        return self._pref_disable_new_entities

    @property
    def pref_disable_polling(self) -> bool:
        return self._pref_disable_polling

    @property
    def data(self) -> collections.abc.Mapping[str, typing.Any]:
        return self._data

    @property
    def options(self) -> collections.abc.Mapping[str, typing.Any]:
        return self._options

    @property
    def source(self) -> str:
        return self._source

    @property
    def title(self) -> str:
        return self._title

    @property
    def update_listeners(
        self,
    ) -> list[weakref.ReferenceType[UpdateListenerType] | weakref.WeakMethod]:
        return self._update_listeners

    @property
    def state(self) -> ConfigEntryState:
        return self._state

    @callback
    def set_state(
        self, controller: SmartHomeController, state: ConfigEntryState, reason: str
    ) -> None:
        """Set the state of the config entry."""
        self._state = state
        self._reason = reason
        controller.dispatcher.async_send(
            self.SIGNAL_CONFIG_ENTRY_CHANGED, ConfigEntryChange.UPDATED, self
        )

    async def async_setup(
        self,
        shc: SmartHomeController,
        *,
        integration: Integration = None,
        tries: int = 0,
    ) -> None:
        """Set up an entry."""
        _current_entry.set(self)
        if self._source == _SOURCE_IGNORE or self._disabled_by:
            return

        if integration is None:
            integration = await shc.setup.async_get_integration(self._domain)

        try:
            component = integration.get_component()
        except ImportError as err:
            _LOGGER.error(
                f"Error importing integration {integration.domain} to set up "
                + f"{self._domain} configuration entry: {err}"
            )
            if self._domain == integration.domain:
                self.set_state(shc, ConfigEntryState.SETUP_ERROR, "Import error")
            return

        shc_component = SmartHomeControllerComponent.get_component(integration.domain)
        if shc_component is not None:
            self._supports_remove_device = shc_component.supports_remove_from_device
            self._supports_unload = shc_component.supports_entry_unload
        else:
            self._supports_unload = await self.support_entry_unload(shc, self._domain)
            self._supports_remove_device = await self.support_remove_from_device(
                shc, self._domain
            )

        if self._domain == integration.domain:
            platform = None
            if shc_component is not None:
                platform = shc_component.get_platform(Platform.CONFIG_FLOW)
                if not isinstance(platform, ConfigFlowPlatform):
                    platform = None
            if platform is None:
                try:
                    integration.get_platform("config_flow")
                except ImportError as err:
                    _LOGGER.error(
                        "Error importing platform config_flow from integration "
                        + f"{integration.domain} to set up {self._domain} "
                        + f"configuration entry: {err}"
                    )
                    self.set_state(shc, ConfigEntryState.SETUP_ERROR, "Import error")
                    return

            # Perform migration
            if not await self.async_migrate(shc):
                self.set_state(shc, ConfigEntryState.MIGRATION_ERROR, None)
                return

        error_reason = None

        try:
            if shc_component is not None:
                result = await shc_component.async_setup_entry(self)
            else:
                result = await component.async_setup_entry(shc, self)

            if not isinstance(result, bool):
                _LOGGER.error(
                    f"{integration.domain}.async_setup_entry did not return boolean"
                )
                result = False
        except ConfigEntryAuthFailed as ex:
            message = str(ex)
            auth_base_message = "could not authenticate"
            error_reason = message or auth_base_message
            auth_message = (
                f"{auth_base_message}: {message}" if message else auth_base_message
            )
            _LOGGER.warning(
                f"Config entry '{self._title}' for {self._domain} integration {auth_message}"
            )
            self._async_process_on_unload()
            self.async_start_reauth(shc)
            result = False
        except ConfigEntryNotReady as ex:
            self.set_state(shc, ConfigEntryState.SETUP_RETRY, str(ex) or None)
            wait_time = 2 ** min(tries, 4) * 5
            tries += 1
            message = str(ex)
            ready_message = f"ready yet: {message}" if message else "ready yet"
            if tries == 1:
                _LOGGER.warning(
                    f"Config entry '{self._title}' for {self._domain} integration not "
                    + f"{ready_message}; Retrying in background"
                )
            else:
                _LOGGER.debug(
                    f"Config entry '{self._title}' for {self._domain} integration not "
                    + f"{ready_message}; Retrying in {wait_time} seconds"
                )

            async def setup_again(*_: typing.Any) -> None:
                """Run setup again."""
                self._async_cancel_retry_setup = None
                await self.async_setup(shc, integration=integration, tries=tries)

            if shc.state == CoreState.RUNNING:
                self._async_cancel_retry_setup = shc.tracker.async_call_later(
                    wait_time, setup_again
                )
            else:
                self._async_cancel_retry_setup = shc.bus.async_listen_once(
                    Const.EVENT_SHC_STARTED, setup_again
                )

            self._async_process_on_unload()
            return
        except Exception:  # pylint: disable=broad-except
            _LOGGER.exception(
                f"Error setting up entry {self._title} for {integration.domain}"
            )
            result = False

        # Only store setup result as state if it was not forwarded.
        if self._domain != integration.domain:
            return

        if result:
            self.set_state(shc, ConfigEntryState.LOADED, None)
        else:
            self.set_state(shc, ConfigEntryState.SETUP_ERROR, error_reason)

    async def async_shutdown(self) -> None:
        """Call when Home Assistant is stopping."""
        self.async_cancel_retry_setup()

    @callback
    def async_cancel_retry_setup(self) -> None:
        """Cancel retry setup."""
        if self._async_cancel_retry_setup is not None:
            self._async_cancel_retry_setup()
            self._async_cancel_retry_setup = None

    async def async_unload(
        self, shc: SmartHomeController, *, integration: Integration = None
    ) -> bool:
        """Unload an entry.

        Returns if unload is possible and was successful.
        """
        if self._source == _SOURCE_IGNORE:
            self.set_state(shc, ConfigEntryState.NOT_LOADED, None)
            return True

        if self.state == ConfigEntryState.NOT_LOADED:
            return True

        if integration is None:
            try:
                integration = await shc.setup.async_get_integration(self._domain)
            except IntegrationNotFound:
                # The integration was likely a custom_component
                # that was uninstalled, or an integration
                # that has been renamed without removing the config
                # entry.
                self.set_state(shc, ConfigEntryState.NOT_LOADED, None)
                return True

        component = integration.get_component()

        if integration.domain == self._domain:
            if not self.state.recoverable:
                return False

            if self.state is not ConfigEntryState.LOADED:
                self.async_cancel_retry_setup()

                self.set_state(shc, ConfigEntryState.NOT_LOADED, None)
                return True

        shc_component = SmartHomeControllerComponent.get_component(integration.domain)
        if shc_component is not None:
            supports_unload = shc_component.supports_entry_unload
        else:
            supports_unload = hasattr(component, "async_unload_entry")

        if not supports_unload:
            if integration.domain == self._domain:
                self.set_state(
                    shc, ConfigEntryState.FAILED_UNLOAD, "Unload not supported"
                )
            return False

        try:
            if shc_component is not None:
                result = await shc_component.async_unload_entry(self)
            else:
                result = await component.async_unload_entry(shc, self)

            assert isinstance(result, bool)

            # Only adjust state if we unloaded the component
            if result and integration.domain == self._domain:
                self.set_state(shc, ConfigEntryState.NOT_LOADED, None)

            self._async_process_on_unload()

            # https://github.com/python/mypy/issues/11839
            return result
        except Exception:  # pylint: disable=broad-except
            _LOGGER.exception(
                f"Error unloading entry {self._title} for {integration.domain}"
            )
            if integration.domain == self._domain:
                self.set_state(shc, ConfigEntryState.FAILED_UNLOAD, "Unknown error")
            return False

    async def async_remove(self, shc: SmartHomeController) -> None:
        """Invoke remove callback on component."""
        if self._source == _SOURCE_IGNORE:
            return

        try:
            integration = await shc.setup.async_get_integration(self._domain)
        except IntegrationNotFound:
            # The integration was likely a custom_component
            # that was uninstalled, or an integration
            # that has been renamed without removing the config
            # entry.
            return

        component = integration.get_component()
        shc_component = SmartHomeControllerComponent.get_component(self._domain)
        if shc_component is not None:
            supports_remove = shc_component.supports_entry_remove
        else:
            supports_remove = hasattr(component, "async_remove_entry")
        if not supports_remove:
            return
        try:
            if shc_component is not None:
                await shc_component.async_remove_entry(self)
            else:
                await component.async_remove_entry(shc, self)
        except Exception:  # pylint: disable=broad-except
            _LOGGER.exception(
                f"Error calling entry remove callback {self._title} for {integration.domain}"
            )

    async def _legacy_migrate(self, shc: SmartHomeController) -> bool:
        """Migrate an entry.

        Returns True if config entry is up-to-date or has been migrated.
        """
        # legacy module based implementation
        if (handler := _CONFIG_HANDLERS.get(self._domain)) is None:
            _LOGGER.error(
                f"Flow handler not found for entry {self._title} for {self._domain}"
            )
            return False

        # Handler may be a partial
        # Keep for backwards compatibility
        # https://github.com/home-assistant/core/pull/67087#discussion_r812559950
        while isinstance(handler, functools.partial):
            handler = handler.func

        if self._version == handler.version:
            return True

        integration = await shc.setup.async_get_integration(self._domain)
        component = integration.get_component()
        supports_migrate = hasattr(component, "async_migrate_entry")
        if not supports_migrate:
            _LOGGER.error(
                f"Migration handler not found for entry {self._title} for "
                + f"{self._domain}"
            )
            return False

        try:
            result = await component.async_migrate_entry(shc, self)
            if not isinstance(result, bool):
                _LOGGER.error(
                    f"{self._domain}.async_migrate_entry did not return boolean"
                )
                return False
            if result:
                # pylint: disable=protected-access
                shc.config_entries._async_schedule_save()
            return result
        except Exception:  # pylint: disable=broad-except
            _LOGGER.exception(f"Error migrating entry {self._title} for {self._domain}")
            return False

    async def async_migrate(self, shc: SmartHomeController) -> bool:
        """Migrate an entry.

        Returns True if config entry is up-to-date or has been migrated.
        """
        handler_version = 0  # ungültiger default
        handler = _CONFIG_HANDLERS.get(self._domain)
        if isinstance(handler, ConfigFlowPlatform):
            handler_version = handler.version
        else:
            comp = SmartHomeControllerComponent.get_component(self._domain)
            if comp is None:
                return await self._legacy_migrate(shc)

        # new class based implementation
        if handler is None:
            platform = comp.get_platform(Platform.CONFIG_FLOW)
            if not isinstance(platform, ConfigFlowPlatform):
                return await self._legacy_migrate(shc)

            handler_version = platform.describe_config_flow()

        if self._version == handler_version:
            return True

        supports_migrate = comp.supports_migrate_entry

        if not supports_migrate:
            _LOGGER.error(
                f"Migration handler not found for entry {self._title} for "
                + f"{self._domain}"
            )
            return False

        try:
            result = await comp.async_migrate_entry(self)
            if not isinstance(result, bool):
                _LOGGER.error(
                    f"{self._domain}.async_migrate_entry did not return boolean"
                )
                return False
            if result:
                # pylint: disable=protected-access
                shc.config_entries._async_schedule_save()
            return result
        except Exception:  # pylint: disable=broad-except
            _LOGGER.exception(f"Error migrating entry {self._title} for {self._domain}")
            return False

    def add_update_listener(self, listener: UpdateListenerType) -> CallbackType:
        """Listen for when entry is updated.

        Returns function to unlisten.
        """
        weak_listener: typing.Any
        # weakref.ref is not applicable to a bound method, e.g. method of a class instance,
        # as reference will die immediately
        if hasattr(listener, "__self__"):
            weak_listener = weakref.WeakMethod(typing.cast(types.MethodType, listener))
        else:
            weak_listener = weakref.ref(listener)
        self._update_listeners.append(weak_listener)

        return lambda: self._update_listeners.remove(weak_listener)

    def as_dict(self) -> dict[str, typing.Any]:
        """Return dictionary version of this entry."""
        return {
            "entry_id": self._entry_id,
            "version": self._version,
            "domain": self._domain,
            "title": self._title,
            "data": dict(self._data),
            "options": dict(self._options),
            "pref_disable_new_entities": self._pref_disable_new_entities,
            "pref_disable_polling": self._pref_disable_polling,
            "source": self._source,
            "unique_id": self._unique_id,
            "disabled_by": self._disabled_by,
        }

    @callback
    def async_on_unload(self, func: CallbackType) -> None:
        """Add a function to call when config entry is unloaded."""
        if self._on_unload is None:
            self._on_unload = []
        self._on_unload.append(func)

    @callback
    def _async_process_on_unload(self) -> None:
        """Process the on_unload callbacks."""
        if self._on_unload is not None:
            while self._on_unload:
                self._on_unload.pop()()

    @callback
    def async_start_reauth(self, shc: SmartHomeController) -> None:
        """Start a reauth flow."""
        flow_context = {
            "source": ConfigEntrySource.REAUTH,
            "entry_id": self._entry_id,
            "title_placeholders": {"name": self._title},
            "unique_id": self._unique_id,
        }

        for flow in shc.config_entries.flow.async_progress_by_handler(self._domain):
            if flow["context"] == flow_context:
                return

        shc.async_create_task(
            shc.config_entries.flow.async_init(
                self._domain,
                context=flow_context,
                data=self._data,
            )
        )

    @callback
    def _handle_entry_updated_filter(event: Event) -> bool:
        """Handle entity registry entry update filter.

        Only handle changes to "disabled_by".
        If "disabled_by" was CONFIG_ENTRY, reload is not needed.
        """
        if (
            event.data["action"] != "update"
            or "disabled_by" not in event.data["changes"]
            or event.data["changes"]["disabled_by"]
            is EntityRegistryEntryDisabler.CONFIG_ENTRY
        ):
            return False
        return True

    @staticmethod
    async def support_entry_unload(shc: SmartHomeController, domain: str) -> bool:
        """Test if a domain supports entry unloading."""
        integration = await shc.setup.async_get_integration(domain)
        component = integration.get_component()
        shc_component = SmartHomeControllerComponent.get_component(domain)
        if shc_component is not None:
            return shc_component.supports_entry_unload
        return hasattr(component, "async_unload_entry")

    @staticmethod
    async def support_remove_from_device(shc: SmartHomeController, domain: str) -> bool:
        """Test if a domain supports being removed from a device."""
        integration = await shc.async_get_integration(domain)
        component = integration.get_component()
        shc_component = SmartHomeControllerComponent.get_component(domain)
        if shc_component is not None:
            return shc_component.supports_remove_from_device

        return hasattr(component, "async_remove_config_entry_device")

    @staticmethod
    def current_entry() -> contextvars.ContextVar:
        return _current_entry


_current_entry: contextvars.ContextVar[ConfigEntry] = contextvars.ContextVar(
    "current_entry", default=None
)
