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
import logging
import typing

from .callback import callback
from .const import Const
from .entity_registry_entry_disabler import EntityRegistryEntryDisabler
from .event import Event


if not typing.TYPE_CHECKING:

    class SmartHomeController:
        ...


if typing.TYPE_CHECKING:
    from .smart_home_controller import SmartHomeController


_RELOAD_AFTER_UPDATE_DELAY: typing.Final = 30
_LOGGER: typing.Final = logging.getLogger(__name__)


# pylint: disable=unused-variable
class EntityRegistryDisabledHandler:
    """Handler to handle when entities related to config entries updating disabled_by."""

    def __init__(self, shc: SmartHomeController) -> None:
        """Initialize the handler."""
        self._shc = shc
        self._changed: set[str] = set()
        self._remove_call_later: typing.Callable[[], None] = None

    @callback
    def async_setup(self) -> None:
        """Set up the disable handler."""
        self._shc.bus.async_listen(
            Const.EVENT_ENTITY_REGISTRY_UPDATED,
            self._handle_entry_updated,
            event_filter=self._handle_entry_updated_filter,
        )

    @callback
    async def _handle_entry_updated(self, event: Event) -> None:
        """Handle entity registry entry update."""
        registry = self._shc.entity_registry
        entity_entry = registry.async_get(event.data["entity_id"])

        if (
            # Stop if no entry found
            entity_entry is None
            # Stop if entry not connected to config entry
            or entity_entry.config_entry_id is None
            # Stop if the entry got disabled. In that case the entity handles it
            # themselves.
            or entity_entry.disabled_by
        ):
            return

        config_entry = self._shc.config_entries.async_get_entry(
            entity_entry.config_entry_id
        )
        assert config_entry is not None

        if config_entry.entry_id not in self._changed and config_entry.supports_unload:
            self._changed.add(config_entry.entry_id)

        if not self._changed:
            return

        # We are going to delay reloading on *every* entity registry change so that
        # if a user is happily clicking along, it will only reload at the end.

        if self._remove_call_later:
            self._remove_call_later()

        self._remove_call_later = self._shc.tracker.async_call_later(
            _RELOAD_AFTER_UPDATE_DELAY, self._handle_reload
        )

    async def _handle_reload(self, _now: typing.Any) -> None:
        """Handle a reload."""
        self._remove_call_later = None
        to_reload = self._changed
        self._changed = set()

        _LOGGER.info(
            "Reloading configuration entries because disabled_by changed in entity "
            + f"registry: {', '.join(self._changed)}"
        )

        await asyncio.gather(
            *(self._shc.config_entries.async_reload(entry_id) for entry_id in to_reload)
        )

    @staticmethod
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
