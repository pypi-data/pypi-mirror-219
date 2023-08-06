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

import collections

from .entity_registry_entry import EntityRegistryEntry


# pylint: disable=unused-variable
class EntityRegistryItems(collections.UserDict[str, "EntityRegistryEntry"]):
    """Container for entity registry items, maps entity_id -> entry.

    Maintains two additional indexes:
    - id -> entry
    - (domain, platform, unique_id) -> entry
    """

    def __init__(self) -> None:
        """Initialize the container."""
        super().__init__()
        self._entry_ids: dict[str, EntityRegistryEntry] = {}
        self._index: dict[tuple[str, str, str], str] = {}

    def __setitem__(self, key: str, entry: EntityRegistryEntry) -> None:
        """Add an item."""
        if key in self:
            old_entry = self[key]
            del self._entry_ids[old_entry.id]
            del self._index[(old_entry.domain, old_entry.platform, old_entry.unique_id)]
        super().__setitem__(key, entry)
        self._entry_ids.__setitem__(entry.id, entry)
        self._index[(entry.domain, entry.platform, entry.unique_id)] = entry.entity_id

    def __delitem__(self, key: str) -> None:
        """Remove an item."""
        entry = self[key]
        self._entry_ids.__delitem__(entry.id)
        self._index.__delitem__((entry.domain, entry.platform, entry.unique_id))
        super().__delitem__(key)

    def get_entity_id(self, key: tuple[str, str, str]) -> str:
        """Get entity_id from (domain, platform, unique_id)."""
        return self._index.get(key)

    def get_entry(self, key: str) -> EntityRegistryEntry:
        """Get entry from id."""
        return self._entry_ids.get(key)
