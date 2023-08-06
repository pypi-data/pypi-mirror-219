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

from .const import Const
from .collection_change_set import CollectionChangeSet
from .observable_collection import ObservableCollection


# pylint: disable=unused-variable
class YamlCollection(ObservableCollection):
    """Offer a collection based on static data."""

    async def async_load(self, data: list[dict]) -> None:
        """Load the YAML collection. Overrides existing data."""
        old_ids = set(self._data)

        change_sets = []

        for item in data:
            item_id = item[Const.CONF_ID]

            if item_id in old_ids:
                old_ids.remove(item_id)
                event = Const.EVENT_COLLECTION_CHANGE_UPDATED
            elif self._id_manager.has_id(item_id):
                self._logger.warning(f"Duplicate ID '{item_id}' detected, skipping")
                continue
            else:
                event = Const.EVENT_COLLECTION_CHANGE_ADDED

            self._data[item_id] = item
            change_sets.append(CollectionChangeSet(event, item_id, item))

        for item_id in old_ids:
            change_sets.append(
                CollectionChangeSet(
                    Const.EVENT_COLLECTION_CHANGE_REMOVED,
                    item_id,
                    self._data.pop(item_id),
                )
            )

        if change_sets:
            await self.notify_changes(change_sets)
