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
import typing

from . import helpers
from .context import Context
from .event_origin import EventOrigin


class Event:  # pylint: disable=unused-variable
    """Representation of an event within the bus."""

    __slots__ = ["_event_type", "_data", "_origin", "_time_fired", "_context"]

    def __init__(
        self,
        event_type: str,
        data: dict[str, typing.Any] = None,
        origin: EventOrigin = EventOrigin.LOCAL,
        time_fired: datetime.datetime = None,
        context: Context = None,
    ) -> None:
        """Initialize a new event."""
        self._event_type = event_type
        self._data = data or {}
        self._origin = origin
        self._time_fired = time_fired or helpers.utcnow()
        self._context: Context = context or Context(
            context_id=helpers.ulid(helpers.utc_to_timestamp(self.time_fired))
        )

    @property
    def event_type(self) -> str:
        return self._event_type

    @property
    def data(self) -> dict[str, typing.Any]:
        return self._data

    @property
    def origin(self) -> EventOrigin:
        return self._origin

    @property
    def time_fired(self) -> datetime.datetime:
        return self._time_fired

    @property
    def context(self) -> Context:
        return self._context

    def __hash__(self) -> int:
        """Make hashable."""
        # The only event type that shares context are the TIME_CHANGED
        return hash((self.event_type, self.context.context_id, self.time_fired))

    def as_dict(self) -> dict[str, typing.Any]:
        """Create a dict representation of this Event.

        Async friendly.
        """
        return {
            "event_type": self.event_type,
            "data": dict(self.data),
            "origin": str(self.origin.value),
            "time_fired": self.time_fired.isoformat(),
            "context": self.context.as_dict(),
        }

    def __repr__(self) -> str:
        """Return the representation."""
        if self.data:
            return (
                f"<Event {self.event_type}[{str(self.origin)[0]}]: "
                + f"{helpers.repr_helper(self.data)}>"
            )

        return f"<Event {self.event_type}[{str(self.origin)[0]}]>"

    def __eq__(self, other: typing.Any) -> bool:
        """Return the comparison."""
        return (  # type: ignore[no-any-return]
            self.__class__ == other.__class__
            and self.event_type == other.event_type
            and self.data == other.data
            and self.origin == other.origin
            and self.time_fired == other.time_fired
            and self.context == other.context
        )
