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

from .entity import Entity
from .extra_stored_data import ExtraStoredData
from .restore_state_data import RestoreStateData
from .state import State
from .stored_state import StoredState

_LOGGER: typing.Final = logging.getLogger(__name__)


# pylint: disable=unused-variable
class RestoreEntity(Entity):
    """Mixin class for restoring previous entity state."""

    async def async_internal_added_to_shc(self) -> None:
        """Register this entity as a restorable entity."""
        _, data = await asyncio.gather(
            super().async_internal_added_to_shc(),
            RestoreStateData.async_get_instance(self._shc),
        )
        data.async_restore_entity_added(self)

    async def async_internal_will_remove_from_shc(self) -> None:
        """Run when entity will be removed from hass."""
        _, data = await asyncio.gather(
            super().async_internal_will_remove_from_shc(),
            RestoreStateData.async_get_instance(self._shc),
        )
        data.async_restore_entity_removed(self.entity_id, self.extra_restore_state_data)

    async def _async_get_restored_data(self) -> StoredState:
        """Get data stored for an entity, if any."""
        if self._shc is None or self.entity_id is None:
            # Return None if this entity isn't added to hass yet
            _LOGGER.warning(
                "Cannot get last state. Entity not added to Smart Home - The Next Generation."
            )
            return None
        data = typing.cast(
            RestoreStateData, await RestoreStateData.async_get_instance(self._shc)
        )
        if self.entity_id not in data.last_states:
            return None
        return data.last_states[self.entity_id]

    async def async_get_last_state(self) -> State:
        """Get the entity state from the previous run."""
        if (stored_state := await self._async_get_restored_data()) is None:
            return None
        return stored_state.state

    async def async_get_last_extra_data(self) -> ExtraStoredData:
        """Get the entity specific state data from the previous run."""
        if (stored_state := await self._async_get_restored_data()) is None:
            return None
        return stored_state.extra_data

    @property
    def extra_restore_state_data(self) -> ExtraStoredData:
        """Return entity specific state data to be restored.

        Implemented by platform classes.
        """
        return None
