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

import datetime
import logging
import typing

from . import helpers
from .callback import callback
from .const import Const
from .extra_stored_data import ExtraStoredData
from .json_encoder import JsonEncoder
from .singleton import Singleton
from .smart_home_controller_error import SmartHomeControllerError
from .state import State
from .store import Store
from .stored_state import StoredState

_LOGGER: typing.Final = logging.getLogger(__name__)
_STORAGE_KEY: typing.Final = "core.restore_state"
_STORAGE_VERSION: typing.Final = 1
# How long between periodically saving the current states to disk
_STATE_DUMP_INTERVAL = datetime.timedelta(minutes=15)
# How long should a saved state be preserved if the entity no longer exists
_STATE_EXPIRATION: typing.Final = datetime.timedelta(days=7)


if not typing.TYPE_CHECKING:

    class RestoreEntity:
        ...

    class SmartHomeController:
        ...


if typing.TYPE_CHECKING:
    from .restore_entity import RestoreEntity
    from .smart_home_controller import SmartHomeController


_single_helper = Singleton()


# pylint: disable=unused-variable
class RestoreStateData:
    """Helper class for managing the helper saved data."""

    def __init__(self, shc: SmartHomeController) -> None:
        """Initialize the restore state data class."""
        self._shc: SmartHomeController = shc
        self.store: Store = Store[list[dict[str, typing.Any]]](
            shc, _STORAGE_VERSION, _STORAGE_KEY, encoder=JsonEncoder
        )
        self.last_states: dict[str, StoredState] = {}
        self.entities: dict[str, RestoreEntity] = {}

    def _set_last_states(self, last_states: dict[str, StoredState]) -> None:
        self.last_states = last_states

    @staticmethod
    @Singleton.shc_singleton(_single_helper)
    async def async_get_instance(shc: SmartHomeController):
        """Get the singleton instance of this data helper."""
        data = RestoreStateData(shc)

        try:
            stored_states = await data.store.async_load()
        except SmartHomeControllerError as exc:
            _LOGGER.error("Error loading last states", exc_info=exc)
            stored_states = None

        if stored_states is None:
            _LOGGER.debug("Not creating cache - no saved states found")
            # pylint: disable=protected-access
            data._set_last_states({})
        else:
            data._set_last_states(  # pylint: disable=protected-access
                {
                    item["state"]["entity_id"]: StoredState.from_dict(item)
                    for item in stored_states
                    if helpers.valid_entity_id(item["state"]["entity_id"])
                }
            )
            _LOGGER.debug(f"Created cache with {list(data.last_states)}")

        async def shc_start(_shc: SmartHomeController) -> None:
            """Start the restore state task."""
            data.async_setup_dump()

        shc.async_at_start(shc_start)

        return data

    @classmethod
    async def async_save_persistent_states(cls, shc: SmartHomeController) -> None:
        """Dump states now."""
        data = await cls.async_get_instance(shc)
        await data.async_dump_states()

    @callback
    def async_get_stored_states(self) -> list[StoredState]:
        """Get the set of states which should be stored.

        This includes the states of all registered entities, as well as the
        stored states from the previous run, which have not been created as
        entities on this run, and have not expired.
        """
        now = helpers.utcnow()
        all_states = self._shc.states.async_all()
        # Entities currently backed by an entity object
        current_entity_ids = {
            state.entity_id
            for state in all_states
            if not state.attributes.get(Const.ATTR_RESTORED)
        }

        # Start with the currently registered states
        stored_states = [
            StoredState(
                state, self.entities[state.entity_id].extra_restore_state_data, now
            )
            for state in all_states
            if state.entity_id in self.entities and
            # Ignore all states that are entity registry placeholders
            not state.attributes.get(Const.ATTR_RESTORED)
        ]
        expiration_time = now - _STATE_EXPIRATION

        for entity_id, stored_state in self.last_states.items():
            # Don't save old states that have entities in the current run
            # They are either registered and already part of stored_states,
            # or no longer care about restoring.
            if entity_id in current_entity_ids:
                continue

            # Don't save old states that have expired
            if stored_state.last_seen < expiration_time:
                continue

            stored_states.append(stored_state)

        return stored_states

    async def async_dump_states(self) -> None:
        """Save the current state machine to storage."""
        _LOGGER.debug("Dumping states")
        try:
            await self.store.async_save(
                [
                    stored_state.as_dict()
                    for stored_state in self.async_get_stored_states()
                ]
            )
        except SmartHomeControllerError as exc:
            _LOGGER.error("Error saving current states", exc_info=exc)

    @callback
    def async_setup_dump(self, *_args: typing.Any) -> None:
        """Set up the restore state listeners."""

        async def _async_dump_states(*_: typing.Any) -> None:
            await self.async_dump_states()

        # Dump the initial states now. This helps minimize the risk of having
        # old states loaded by overwriting the last states once Home Assistant
        # has started and the old states have been read.
        self._shc.async_create_task(_async_dump_states())

        # Dump states periodically
        cancel_interval = self._shc.tracker.async_track_time_interval(
            _async_dump_states, _STATE_DUMP_INTERVAL
        )

        async def _async_dump_states_at_stop(*_: typing.Any) -> None:
            cancel_interval()
            await self.async_dump_states()

        # Dump states when stopping hass
        self._shc.bus.async_listen_once(
            Const.EVENT_SHC_STOP, _async_dump_states_at_stop
        )

    @callback
    def async_restore_entity_added(self, entity: RestoreEntity) -> None:
        """Store this entity's state when hass is shutdown."""
        self.entities[entity.entity_id] = entity

    @callback
    def async_restore_entity_removed(
        self, entity_id: str, extra_data: ExtraStoredData
    ) -> None:
        """Unregister this entity from saving state."""
        # When an entity is being removed from hass, store its last state. This
        # allows us to support state restoration if the entity is removed, then
        # re-added while hass is still running.
        state = self._shc.states.get(entity_id)
        # To fully mimic all the attribute data types when loaded from storage,
        # we're going to serialize it to JSON and then re-load it.
        if state is not None:
            state = State.from_dict(_encode_complex(state.as_dict()))
        if state is not None:
            self.last_states[entity_id] = StoredState(
                state, extra_data, helpers.utcnow()
            )

        self.entities.pop(entity_id)


def _encode(value: typing.Any) -> typing.Any:
    """Little helper to JSON encode a value."""
    try:
        return JsonEncoder.default(
            None,
            value,
        )
    except TypeError:
        return value


def _encode_complex(value: typing.Any) -> typing.Any:
    """Recursively encode all values with the JSONEncoder."""
    if isinstance(value, dict):
        return {_encode(key): _encode_complex(value) for key, value in value.items()}
    if isinstance(value, list):
        return [_encode_complex(val) for val in value]

    new_value = _encode(value)

    if isinstance(new_value, type(value)):
        return new_value

    return _encode_complex(new_value)
