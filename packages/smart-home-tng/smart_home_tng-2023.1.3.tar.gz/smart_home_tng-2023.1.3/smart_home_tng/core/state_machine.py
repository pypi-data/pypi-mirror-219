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
import collections.abc
import typing

from . import helpers
from .callback import callback
from .const import Const
from .context import Context
from .event_bus import EventBus
from .event_origin import EventOrigin
from .smart_home_controller_error import SmartHomeControllerError
from .state import State


# pylint: disable=unused-variable
class StateMachine:
    """Helper class that tracks the state of different entities."""

    def __init__(self, bus: EventBus, loop: asyncio.events.AbstractEventLoop) -> None:
        """Initialize state machine."""
        self._states: dict[str, State] = {}
        self._reservations: set[str] = set()
        self._bus = bus
        self._loop = loop

    def entity_ids(self, domain_filter: str = None) -> list[str]:
        """List of entity ids that are being tracked."""
        future = helpers.run_callback_threadsafe(
            self._loop, self.async_entity_ids, domain_filter
        )
        return future.result()

    @callback
    def async_entity_ids(
        self, domain_filter: str | collections.abc.Iterable[str] = None
    ) -> list[str]:
        """List of entity ids that are being tracked.

        This method must be run in the event loop.
        """
        if domain_filter is None:
            return list(self._states)

        if isinstance(domain_filter, str):
            domain_filter = (domain_filter.lower(),)

        return [
            state.entity_id
            for state in self._states.values()
            if state.domain in domain_filter
        ]

    @callback
    def async_entity_ids_count(
        self, domain_filter: str | collections.abc.Iterable[str] = None
    ) -> int:
        """Count the entity ids that are being tracked.

        This method must be run in the event loop.
        """
        if domain_filter is None:
            return len(self._states)

        if isinstance(domain_filter, str):
            domain_filter = (domain_filter.lower(),)

        return len(
            [None for state in self._states.values() if state.domain in domain_filter]
        )

    def all(
        self, domain_filter: str | collections.abc.Iterable[str] = None
    ) -> list[State]:
        """Create a list of all states."""
        return helpers.run_callback_threadsafe(
            self._loop, self.async_all, domain_filter
        ).result()

    @callback
    def async_all(
        self, domain_filter: str | collections.abc.Iterable[str] = None
    ) -> list[State]:
        """Create a list of all states matching the filter.

        This method must be run in the event loop.
        """
        if domain_filter is None:
            return list(self._states.values())

        if isinstance(domain_filter, str):
            domain_filter = (domain_filter.lower(),)

        return [
            state for state in self._states.values() if state.domain in domain_filter
        ]

    def get(self, entity_id: str) -> State:
        """Retrieve state of entity_id or None if not found.

        Async friendly.
        """
        return self._states.get(entity_id.lower())

    def is_state(self, entity_id: str, state: str) -> bool:
        """Test if entity exists and is in specified state.

        Async friendly.
        """
        state_obj = self.get(entity_id)
        return state_obj is not None and state_obj.state == state

    def remove(self, entity_id: str) -> bool:
        """Remove the state of an entity.

        Returns boolean to indicate if an entity was removed.
        """
        return helpers.run_callback_threadsafe(
            self._loop, self.async_remove, entity_id
        ).result()

    @callback
    def async_remove(self, entity_id: str, context: Context = None) -> bool:
        """Remove the state of an entity.

        Returns boolean to indicate if an entity was removed.

        This method must be run in the event loop.
        """
        entity_id = entity_id.lower()
        old_state = self._states.pop(entity_id, None)

        if entity_id in self._reservations:
            self._reservations.remove(entity_id)

        if old_state is None:
            return False

        self._bus.async_fire(
            Const.EVENT_STATE_CHANGED,
            {"entity_id": entity_id, "old_state": old_state, "new_state": None},
            EventOrigin.LOCAL,
            context=context,
        )
        return True

    def set(
        self,
        entity_id: str,
        new_state: str,
        attributes: collections.abc.Mapping[str, typing.Any] = None,
        force_update: bool = False,
        context: Context = None,
    ) -> None:
        """Set the state of an entity, add entity if it does not exist.

        Attributes is an optional dict to specify attributes of this state.

        If you just update the attributes and not the state, last changed will
        not be affected.
        """
        helpers.run_callback_threadsafe(
            self._loop,
            self.async_set,
            entity_id,
            new_state,
            attributes,
            force_update,
            context,
        ).result()

    @callback
    def async_reserve(self, entity_id: str) -> None:
        """Reserve a state in the state machine for an entity being added.

        This must not fire an event when the state is reserved.

        This avoids a race condition where multiple entities with the same
        entity_id are added.
        """
        entity_id = entity_id.lower()
        if entity_id in self._states or entity_id in self._reservations:
            raise SmartHomeControllerError(
                "async_reserve must not be called once the state is in the state machine."
            )

        self._reservations.add(entity_id)

    @callback
    def async_available(self, entity_id: str) -> bool:
        """Check to see if an entity_id is available to be used."""
        entity_id = entity_id.lower()
        return entity_id not in self._states and entity_id not in self._reservations

    @callback
    def async_set(
        self,
        entity_id: str,
        new_state: str,
        attributes: collections.abc.Mapping[str, typing.Any] = None,
        force_update: bool = False,
        context: Context = None,
    ) -> None:
        """Set the state of an entity, add entity if it does not exist.

        Attributes is an optional dict to specify attributes of this state.

        If you just update the attributes and not the state, last changed will
        not be affected.

        This method must be run in the event loop.
        """
        entity_id = entity_id.lower()
        new_state = str(new_state)
        attributes = attributes or {}
        if (old_state := self._states.get(entity_id)) is None:
            same_state = False
            same_attr = False
            last_changed = None
        else:
            same_state = old_state.state == new_state and not force_update
            same_attr = old_state.attributes == attributes
            last_changed = old_state.last_changed if same_state else None

        if same_state and same_attr:
            return

        now = helpers.utcnow()

        if context is None:
            context = Context(context_id=helpers.ulid(helpers.utc_to_timestamp(now)))

        state = State(
            entity_id,
            new_state,
            attributes,
            last_changed,
            now,
            context,
            old_state is None,
        )
        self._states[entity_id] = state
        self._bus.async_fire(
            Const.EVENT_STATE_CHANGED,
            {"entity_id": entity_id, "old_state": old_state, "new_state": state},
            EventOrigin.LOCAL,
            context,
            time_fired=now,
        )
