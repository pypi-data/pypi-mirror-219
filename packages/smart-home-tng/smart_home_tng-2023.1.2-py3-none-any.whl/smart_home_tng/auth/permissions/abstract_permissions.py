"""
Permission Layer for Smart Home - The Next Generation.

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

import collections.abc


# pylint: disable=unused-variable
class AbstractPermissions:
    """Default permissions class."""

    _cached_entity_func: collections.abc.Callable[[str, str], bool] = None

    def _entity_func(self) -> collections.abc.Callable[[str, str], bool]:
        """Return a function that can test entity access."""
        raise NotImplementedError()

    def access_all_entities(self, key: str) -> bool:
        """Check if we have a certain access to all entities."""
        raise NotImplementedError()

    def check_entity(self, entity_id: str, key: str) -> bool:
        """Check if we can access entity."""
        if (entity_func := self._cached_entity_func) is None:
            entity_func = self._cached_entity_func = self._entity_func()

        return entity_func(entity_id, key)
