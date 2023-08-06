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

# pylint: disable=unused-variable, unused-import

import typing

from .callback import callback
from .data_update_coordinator import DataUpdateCoordinator
from .entity import Entity

_DataUpdateCoordinatorT = typing.TypeVar(
    "_DataUpdateCoordinatorT", bound="DataUpdateCoordinator[typing.Any]"
)


class CoordinatorEntity(Entity, typing.Generic[_DataUpdateCoordinatorT]):
    """A class for entities using DataUpdateCoordinator."""

    def __init__(
        self, coordinator: _DataUpdateCoordinatorT, context: typing.Any = None
    ) -> None:
        """Create the entity with a DataUpdateCoordinator."""
        self._coordinator = coordinator
        self._coordinator_context = context

    @property
    def coordinator(self) -> _DataUpdateCoordinatorT:
        return self._coordinator

    @property
    def coordinator_context(self) -> typing.Any:
        return self._coordinator_context

    @property
    def should_poll(self) -> bool:
        """No need to poll. Coordinator notifies entity of updates."""
        return False

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return self.coordinator.last_update_success

    async def async_added_to_shc(self) -> None:
        """When entity is added to Smart Home Controller."""
        await super().async_added_to_shc()
        self.async_on_remove(
            self.coordinator.async_add_listener(
                self._handle_coordinator_update, self.coordinator_context
            )
        )

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self.async_write_state()

    async def async_update(self) -> None:
        """Update the entity.

        Only used by the generic entity update service.
        """
        # Ignore manual update requests if the entity is disabled
        if not self.enabled:
            return

        await self.coordinator.async_request_refresh()
