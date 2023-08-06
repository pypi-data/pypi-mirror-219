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

from .collection_change_set import CollectionChangeSet
from .const import Const
from .observable_collection import ObservableCollection


# pylint: disable=unused-variable
class IDLessCollection(ObservableCollection):
    """A collection without IDs."""

    _counter = 0

    async def async_load(self, data: list[dict]) -> None:
        """Load the collection. Overrides existing data."""
        await self.notify_changes(
            [
                CollectionChangeSet(
                    Const.EVENT_COLLECTION_CHANGE_REMOVED, item_id, item
                )
                for item_id, item in list(self._data.items())
            ]
        )

        self._data.clear()

        for item in data:
            self._counter += 1
            item_id = f"fakeid-{self._counter}"

            self._data[item_id] = item

        await self.notify_changes(
            [
                CollectionChangeSet(Const.EVENT_COLLECTION_CHANGE_ADDED, item_id, item)
                for item_id, item in self._data.items()
            ]
        )
