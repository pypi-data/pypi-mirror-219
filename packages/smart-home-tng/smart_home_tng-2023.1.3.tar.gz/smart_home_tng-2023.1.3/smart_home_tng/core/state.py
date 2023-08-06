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

import collections.abc
import datetime
import typing

from . import helpers
from .const import Const
from .context import Context
from .invalid_entity_format_error import InvalidEntityFormatError
from .invalid_state_error import InvalidStateError
from .read_only_dict import ReadOnlyDict

_StateT = typing.TypeVar("_StateT", bound="State")


# pyint: disable=unused-variable
class State:
    """Object to represent a state within the state machine.

    entity_id: the entity that is represented.
    state: the state of the entity
    attributes: extra information on entity and state
    last_changed: last time the state was changed, not the attributes.
    last_updated: last time this object was updated.
    context: Context in which it was created
    domain: Domain of this state.
    object_id: Object id of this state.
    """

    __slots__ = [
        "_entity_id",
        "_state",
        "_attributes",
        "_last_changed",
        "_last_updated",
        "_context",
        "_domain",
        "_object_id",
        "_as_dict",
    ]

    def __init__(
        self,
        entity_id: str,
        state: str,
        attributes: collections.abc.Mapping[str, typing.Any] = None,
        last_changed: datetime.datetime = None,
        last_updated: datetime.datetime = None,
        context: Context = None,
        validate_entity_id: bool = True,
    ) -> None:
        """Initialize a new state."""
        state = str(state)

        if validate_entity_id and not helpers.valid_entity_id(entity_id):
            raise InvalidEntityFormatError(
                f"Invalid entity id encountered: {entity_id}. "
                "Format should be <domain>.<object_id>"
            )

        if not State._valid_state(state):
            raise InvalidStateError(
                f"Invalid state encountered for entity ID: {entity_id}. "
                "State max length is 255 characters."
            )

        self._entity_id = entity_id.lower()
        self._state = state
        self._attributes = ReadOnlyDict(attributes or {})
        self._last_updated = last_updated or helpers.utcnow()
        self._last_changed = last_changed or self._last_updated
        self._context = context or Context()
        self._domain, self._object_id = helpers.split_entity_id(self._entity_id)
        self._as_dict: ReadOnlyDict[str, collections.abc.Collection[typing.Any]] = None

    def _valid_state(state: str) -> bool:
        """Test if a state is valid."""
        return len(state) <= Const.MAX_LENGTH_STATE_STATE

    @property
    def domain(self) -> str:
        return self._domain

    @property
    def context(self) -> Context:
        return self._context

    @property
    def entity_id(self) -> str:
        return self._entity_id

    @property
    def name(self) -> str:
        """Name of this state."""
        return self._attributes.get(
            Const.ATTR_FRIENDLY_NAME
        ) or self._object_id.replace("_", " ")

    @property
    def state(self) -> str:
        return self._state

    @property
    def attributes(self) -> ReadOnlyDict[str, typing.Any]:
        return self._attributes

    @property
    def last_changed(self) -> datetime.datetime:
        return self._last_changed

    @property
    def last_updated(self) -> datetime.datetime:
        return self._last_updated

    def as_dict(self) -> ReadOnlyDict[str, collections.abc.Collection[typing.Any]]:
        """Return a dict representation of the State.

        Async friendly.

        To be used for JSON serialization.
        Ensures: state == State.from_dict(state.as_dict())
        """
        if not self._as_dict:
            last_changed_isoformat = self._last_changed.isoformat()
            if self._last_changed == self._last_updated:
                last_updated_isoformat = last_changed_isoformat
            else:
                last_updated_isoformat = self._last_updated.isoformat()
            self._as_dict = ReadOnlyDict(
                {
                    "entity_id": self._entity_id,
                    "state": self._state,
                    "attributes": self._attributes,
                    "last_changed": last_changed_isoformat,
                    "last_updated": last_updated_isoformat,
                    "context": ReadOnlyDict(self._context.as_dict()),
                }
            )
        return self._as_dict

    @classmethod
    def from_dict(cls: type[_StateT], json_dict: dict[str, typing.Any]) -> _StateT:
        """Initialize a state from a dict.

        Async friendly.

        Ensures: state == State.from_json_dict(state.to_json_dict())
        """
        if not (json_dict and "entity_id" in json_dict and "state" in json_dict):
            return None

        last_changed = json_dict.get("last_changed")

        if isinstance(last_changed, str):
            last_changed = helpers.parse_datetime(last_changed)

        last_updated = json_dict.get("last_updated")

        if isinstance(last_updated, str):
            last_updated = helpers.parse_datetime(last_updated)

        if context := json_dict.get("context"):
            context = Context(
                context_id=context.get("id"), user_id=context.get("user_id")
            )

        return cls(
            json_dict["entity_id"],
            json_dict["state"],
            json_dict.get("attributes"),
            last_changed,
            last_updated,
            context,
        )

    # pylint: disable=protected-access
    def __eq__(self, other: typing.Any) -> bool:
        """Return the comparison of the state."""
        return (
            self.__class__ == other.__class__
            and self._entity_id == other._entity_id
            and self._state == other._state
            and self._attributes == other._attributes
            and self._context == other._context
        )

    def __repr__(self) -> str:
        """Return the representation of the states."""
        attrs = f"; {helpers.repr_helper(self._attributes)}" if self._attributes else ""

        return (
            f"<state {self._entity_id}={self._state}{attrs}"
            f" @ {helpers.as_local(self._last_changed).isoformat()}>"
        )
