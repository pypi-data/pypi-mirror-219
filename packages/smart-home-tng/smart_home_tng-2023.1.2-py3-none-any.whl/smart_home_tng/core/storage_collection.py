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
import logging
import typing

from .callback import callback
from .collection_change_set import CollectionChangeSet
from .const import Const
from .id_manager import IDManager
from .item_not_found import ItemNotFound
from .observable_collection import ObservableCollection
from .smart_home_controller import SmartHomeController
from .store import Store

_SAVE_DELAY: typing.Final = 10


# pylint: disable=unused-variable
class StorageCollection(ObservableCollection):
    """Offer a CRUD interface on top of JSON storage."""

    def __init__(
        self,
        store: Store,
        logger: logging.Logger,
        id_manager: IDManager = None,
    ) -> None:
        """Initialize the storage collection."""
        super().__init__(logger, id_manager)
        self._store = store

    @property
    def _shc(self) -> SmartHomeController:
        """Smart Home Controller object."""
        # pylint: disable=protected-access
        return self._store._shc

    @property
    def store(self) -> Store:
        return self._store

    async def _async_load_data(self) -> dict:
        """Load the data."""
        return typing.cast(dict, await self._store.async_load())

    async def async_load(self) -> None:
        """Load the storage Manager."""
        raw_storage = await self._async_load_data()

        if raw_storage is None:
            raw_storage = {"items": []}

        for item in raw_storage["items"]:
            self._data[item[Const.CONF_ID]] = item

        await self.notify_changes(
            [
                CollectionChangeSet(
                    Const.EVENT_COLLECTION_CHANGE_ADDED, item[Const.CONF_ID], item
                )
                for item in raw_storage["items"]
            ]
        )

    @abc.abstractmethod
    async def _process_create_data(self, data: dict) -> dict:
        """Validate the config is valid."""

    @abc.abstractmethod
    @callback
    def _get_suggested_id(self, info: dict) -> str:
        """Suggest an ID based on the config."""

    @abc.abstractmethod
    async def _update_data(self, data: dict, update_data: dict) -> dict:
        """Return a new updated data object."""

    async def async_create_item(self, data: dict) -> dict:
        """Create a new item."""
        item = await self._process_create_data(data)
        item[Const.CONF_ID] = self._id_manager.generate_id(self._get_suggested_id(item))
        self._data[item[Const.CONF_ID]] = item
        self._async_schedule_save()
        await self.notify_changes(
            [
                CollectionChangeSet(
                    Const.EVENT_COLLECTION_CHANGE_ADDED, item[Const.CONF_ID], item
                )
            ]
        )
        return item

    async def async_update_item(self, item_id: str, updates: dict) -> dict:
        """Update item."""
        if item_id not in self._data:
            raise ItemNotFound(item_id)

        if Const.CONF_ID in updates:
            raise ValueError("Cannot update ID")

        current = self._data[item_id]

        updated = await self._update_data(current, updates)

        self._data[item_id] = updated
        self._async_schedule_save()

        await self.notify_changes(
            [
                CollectionChangeSet(
                    Const.EVENT_COLLECTION_CHANGE_UPDATED, item_id, updated
                )
            ]
        )

        return self._data[item_id]

    async def async_delete_item(self, item_id: str) -> None:
        """Delete item."""
        if item_id not in self._data:
            raise ItemNotFound(item_id)

        item = self._data.pop(item_id)
        self._async_schedule_save()

        await self.notify_changes(
            [CollectionChangeSet(Const.EVENT_COLLECTION_CHANGE_REMOVED, item_id, item)]
        )

    @callback
    def _async_schedule_save(self) -> None:
        """Schedule saving the area registry."""
        self._store.async_delay_save(self._data_to_save, _SAVE_DELAY)

    @callback
    def _data_to_save(self) -> dict:
        """Return data of area registry to store in a file."""
        return {"items": list(self._data.values())}
