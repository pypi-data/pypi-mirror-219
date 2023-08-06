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

import abc

from .callback import callback
from .entity import Entity


# pylint: disable=unused-variable
class GroupEntity(Entity):
    """Representation of a Group of entities."""

    @property
    def should_poll(self) -> bool:
        """Disable polling for group."""
        return False

    async def async_added_to_shc(self) -> None:
        """Register listeners."""
        self.async_on_remove(self._shc.async_at_start(self._update_at_start))

    async def _update_at_start(self, _shc):
        self.async_update_group_state()
        self.async_write_state()

    @callback
    def async_defer_or_update_state(self) -> None:
        """Only update once at start."""
        if not self._shc.is_running:
            return

        self.async_update_group_state()
        self.async_write_state()

    @abc.abstractmethod
    def async_update_group_state(self) -> None:
        """Abstract method to update the entity."""
