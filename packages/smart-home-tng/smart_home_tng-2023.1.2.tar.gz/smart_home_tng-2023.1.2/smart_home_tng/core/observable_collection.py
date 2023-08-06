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
import asyncio
import collections.abc
import itertools as it
import logging
import typing

from .callback import callback
from .change_listener import ChangeListener
from .change_set_listener import ChangeSetListener
from .collection_change_set import CollectionChangeSet
from .const import Const
from .entity import Entity
from .id_manager import IDManager


if not typing.TYPE_CHECKING:

    class EntityComponent:
        ...

    class SmartHomeController:
        ...


if typing.TYPE_CHECKING:
    from .entity_component import EntityComponent
    from .smart_home_controller import SmartHomeController


# pylint: disable=unused-variable
class ObservableCollection(abc.ABC):
    """Base collection type that can be observed."""

    def __init__(self, logger: logging.Logger, id_manager: IDManager = None) -> None:
        """Initialize the base collection."""
        self._logger = logger
        self._id_manager = id_manager or IDManager()
        self._data: dict[str, dict] = {}
        self._listeners: list[ChangeListener] = []
        self._change_set_listeners: list[ChangeSetListener] = []

        self._id_manager.add_collection(self._data)

    def get_item(self, item_id: str, default=None) -> dict:
        """Return data for item_id, or default if not found"""
        return self._data.get(item_id, default)

    @property
    def data(self) -> dict[str, dict]:
        return self._data

    @callback
    def sync_entity_lifecycle(
        self,
        shc: SmartHomeController,
        domain: str,
        platform: str,
        entity_component: EntityComponent,
        create_entity: collections.abc.Callable[[dict], Entity],
    ) -> None:
        """Map a collection to an entity component."""
        entities: dict[str, Entity] = {}
        ent_reg = shc.entity_registry

        async def _add_entity(change_set: CollectionChangeSet) -> Entity:
            def entity_removed() -> None:
                """Remove entity from entities if it's removed or not added."""
                if change_set.item_id in entities:
                    entities.pop(change_set.item_id)

            entities[change_set.item_id] = create_entity(change_set.item)
            entities[change_set.item_id].async_on_remove(entity_removed)
            return entities[change_set.item_id]

        async def _remove_entity(change_set: CollectionChangeSet) -> None:
            ent_to_remove = ent_reg.async_get_entity_id(
                domain, platform, change_set.item_id
            )
            if ent_to_remove is not None:
                ent_reg.async_remove(ent_to_remove)
            elif change_set.item_id in entities:
                await entities[change_set.item_id].async_remove(force_remove=True)
            # Unconditionally pop the entity from the entity list to avoid racing against
            # the entity registry event handled by Entity._async_registry_updated
            if change_set.item_id in entities:
                entities.pop(change_set.item_id)

        async def _update_entity(change_set: CollectionChangeSet) -> None:
            if change_set.item_id not in entities:
                return
            await entities[change_set.item_id].async_update_config(change_set.item)

        _func_map: dict[
            str,
            collections.abc.Callable[
                [CollectionChangeSet],
                collections.abc.Coroutine[typing.Any, typing.Any, Entity],
            ],
        ] = {
            Const.EVENT_COLLECTION_CHANGE_ADDED: _add_entity,
            Const.EVENT_COLLECTION_CHANGE_REMOVED: _remove_entity,
            Const.EVENT_COLLECTION_CHANGE_UPDATED: _update_entity,
        }

        async def _collection_changed(
            change_sets: collections.abc.Iterable[CollectionChangeSet],
        ) -> None:
            """Handle a collection change."""
            # Create a new bucket every time we have a different change type
            # to ensure operations happen in order. We only group
            # the same change type.
            for _, grouped in it.groupby(
                change_sets, lambda change_set: change_set.change_type
            ):
                new_entities = [
                    entity
                    for entity in await asyncio.gather(
                        *(
                            _func_map[change_set.change_type](change_set)
                            for change_set in grouped
                        )
                    )
                    if entity is not None
                ]
                if new_entities:
                    await entity_component.async_add_entities(new_entities)

        self.async_add_change_set_listener(_collection_changed)

    @callback
    def async_items(self) -> list[dict]:
        """Return list of items in collection."""
        return list(self._data.values())

    @callback
    def async_add_listener(self, listener: ChangeListener) -> None:
        """Add a listener.

        Will be called with (change_type, item_id, updated_config).
        """
        self._listeners.append(listener)

    @callback
    def async_add_change_set_listener(self, listener: ChangeSetListener) -> None:
        """Add a listener for a full change set.

        Will be called with [(change_type, item_id, updated_config), ...]
        """
        self._change_set_listeners.append(listener)

    async def notify_changes(
        self, change_sets: collections.abc.Iterable[CollectionChangeSet]
    ) -> None:
        """Notify listeners of a change."""
        await asyncio.gather(
            *(
                listener(change_set.change_type, change_set.item_id, change_set.item)
                for listener in self._listeners
                for change_set in change_sets
            ),
            *(
                change_set_listener(change_sets)
                for change_set_listener in self._change_set_listeners
            ),
        )
