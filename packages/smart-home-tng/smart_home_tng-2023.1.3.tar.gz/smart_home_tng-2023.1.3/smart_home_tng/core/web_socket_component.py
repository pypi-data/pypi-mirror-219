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
import contextvars
import typing
import voluptuous as vol

from .event import Event
from .json_type import JsonType
from .smart_home_controller_component import SmartHomeControllerComponent
from .web_socket_connection import WebSocketConnection
from .web_socket_command_handler import WebSocketCommandHandler
from .state import State


# pylint: disable=unused-variable
class WebSocketComponent(SmartHomeControllerComponent):
    """Required base component for Web Socket API."""

    @property
    @abc.abstractmethod
    def current_connection(self) -> contextvars.ContextVar[WebSocketConnection]:
        """Return the context var for the current connection."""

    @property
    def active_connection(self) -> WebSocketConnection:
        return self.current_connection.get()

    @abc.abstractmethod
    def register_command(
        self,
        command_or_handler: str | WebSocketCommandHandler,
        schema: vol.Schema | dict[vol.Marker, typing.Any],
        handler: WebSocketCommandHandler = None,
    ) -> None:
        """Register a websocket command."""

    @abc.abstractmethod
    def result_message(
        self, iden: int, result: typing.Any = None
    ) -> dict[str, typing.Any]:
        """Return a success result message."""

    @abc.abstractmethod
    def error_message(
        self, iden: int, code: str, message: str
    ) -> dict[str, typing.Any]:
        """Return an error result message."""

    @abc.abstractmethod
    def cached_event_message(self, iden: int, event: Event) -> str:
        """Return an event message.

        Serialize to json once per message.

        Since we can have many clients connected that are
        all getting many of the same events (mostly state changed)
        we can avoid serializing the same data for each connection.
        """

    @abc.abstractmethod
    def cached_state_diff_message(self, iden: int, event: Event) -> str:
        """Return an event message.

        Serialize to json once per message.

        Since we can have many clients connected that are
        all getting many of the same events (mostly state changed)
        we can avoid serializing the same data for each connection.
        """

    def event_message(
        self, iden: JsonType | int, event: typing.Any
    ) -> dict[str, typing.Any]:
        """Return an event message."""

    @abc.abstractmethod
    def compressed_state_dict_add(self, state: State) -> dict[str, typing.Any]:
        """Build a compressed dict of a state for adds.

        Omits the lu (last_updated) if it matches (lc) last_changed.

        Sends c (context) as a string if it only contains an id.
        """

    @abc.abstractmethod
    def message_to_json(self, message: dict[str, typing.Any]) -> str:
        """Serialize a websocket message to json."""

    @abc.abstractmethod
    def require_admin(self, connection: WebSocketConnection) -> None:
        """Validate  user to be an admin."""

    @abc.abstractmethod
    def check_user(
        self,
        connection: WebSocketConnection,
        iden: int,
        only_owner: bool = False,
        only_system_user: bool = False,
        allow_system_user: bool = True,
        only_active_user: bool = True,
        only_inactive_user: bool = False,
    ) -> bool:
        """
        Validates that login user exist in current WS connection.

        Will write out error message if not authenticated.
        """

    @abc.abstractmethod
    def connection_opened(self) -> None:
        """Increment connection counter."""

    @abc.abstractmethod
    def connection_closed(self) -> None:
        """Decrement connection counter."""

    @property
    @abc.abstractmethod
    def open_connections(self) -> int:
        """Return connection counter."""

    @abc.abstractmethod
    def has_handler(self, msg_type: str) -> bool:
        """Check if a handler is defined for the message type."""

    @abc.abstractmethod
    def get_handler(self, msg_type: str) -> tuple[WebSocketCommandHandler, vol.Schema]:
        """Return the handler for the message."""
