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

import datetime as dt
import typing

from . import helpers
from .extra_stored_data import ExtraStoredData
from .restored_extra_data import RestoredExtraData
from .state import State

_StoredStateT = typing.TypeVar("_StoredStateT", bound="StoredState")


# pylint: disable=unused-variable
class StoredState:
    """Object to represent a stored state."""

    def __init__(
        self,
        state: State,
        extra_data: ExtraStoredData,
        last_seen: dt.datetime,
    ) -> None:
        """Initialize a new stored state."""
        self._extra_data = extra_data
        self._last_seen = last_seen
        self._state = state

    @property
    def state(self) -> State:
        return self._state

    @property
    def last_seen(self) -> dt.datetime:
        return self._last_seen

    @property
    def extra_data(self) -> ExtraStoredData:
        return self._extra_data

    def as_dict(self) -> dict[str, typing.Any]:
        """Return a dict representation of the stored state."""
        result = {
            "state": self._state.as_dict(),
            "extra_data": self._extra_data.as_dict() if self._extra_data else None,
            "last_seen": self._last_seen,
        }
        return result

    @classmethod
    def from_dict(cls: type[_StoredStateT], json_dict: dict) -> _StoredStateT:
        """Initialize a stored state from a dict."""
        extra_data_dict = json_dict.get("extra_data")
        extra_data = RestoredExtraData(extra_data_dict) if extra_data_dict else None
        last_seen = json_dict["last_seen"]

        if isinstance(last_seen, str):
            last_seen = helpers.parse_datetime(last_seen)

        return cls(
            typing.cast(State, State.from_dict(json_dict["state"])),
            extra_data,
            last_seen,
        )
