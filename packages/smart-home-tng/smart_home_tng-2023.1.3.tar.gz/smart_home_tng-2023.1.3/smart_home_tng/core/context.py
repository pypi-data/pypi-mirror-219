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

import typing

from .helpers.ulid import ulid


if not typing.TYPE_CHECKING:

    class Event:
        ...


if typing.TYPE_CHECKING:
    from .event import Event


# pylint: disable=unused-variable
class Context:
    """The context that triggered something."""

    __slots__ = ("user_id", "parent_id", "context_id", "origin_event")

    def __init__(
        self,
        user_id: str = None,
        parent_id: str = None,
        context_id: str = None,
    ) -> None:
        """Init the context."""
        self.context_id = context_id or ulid()
        self.user_id = user_id
        self.parent_id = parent_id
        self.origin_event: Event = None

    @property
    def id(self):
        return self.context_id

    def __eq__(self, other: typing.Any) -> bool:
        """Compare contexts."""
        return bool(
            self.__class__ == other.__class__ and self.context_id == other.context_id
        )

    def as_dict(self) -> dict[str, str]:
        """Return a dictionary representation of the context."""
        return {
            "id": self.context_id,
            "parent_id": self.parent_id,
            "user_id": self.user_id,
        }
