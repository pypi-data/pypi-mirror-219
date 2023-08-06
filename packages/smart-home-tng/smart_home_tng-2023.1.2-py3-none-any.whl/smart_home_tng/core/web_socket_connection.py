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
import typing

from .. import auth
from .context import Context
from .json_type import JsonType
from .unauthorized import Unauthorized

if not typing.TYPE_CHECKING:

    class WebSocket:
        class Component:
            pass


if typing.TYPE_CHECKING:
    from .web_socket import WebSocket


# pylint: disable=unused-variable
class WebSocketConnection(abc.ABC):
    """
    Base class for Web Socket Connection.

    Implementented in component websocket_api.
    """

    @property
    @abc.abstractmethod
    def owner(self) -> WebSocket.Component:
        """Return the administrating WebSocket component."""

    @property
    @abc.abstractmethod
    def refresh_token_id(self) -> str:
        """Return the refresh token id."""

    @property
    @abc.abstractmethod
    def user(self) -> auth.User:
        """Get the connected user."""

    @abc.abstractmethod
    def context(self, msg: dict[str, typing.Any]) -> Context:
        """Return a context."""

    def send_result(self, msg_id: int, result: typing.Any = None) -> None:
        """Send a result message."""
        self.send_message(self.owner.result_message(msg_id, result))

    @abc.abstractmethod
    async def send_big_result(self, msg_id: int, result: typing.Any) -> None:
        """Send a result message that would be expensive to JSON serialize."""

    def send_error(self, msg_id: int, code: str, message: str) -> None:
        """Send a error message."""
        self.send_message(self.owner.error_message(msg_id, code, message))

    def send_event_message(self, iden: JsonType | int, event: typing.Any):
        self.send_message(self.owner.event_message(iden, event))

    @property
    @abc.abstractmethod
    def supported_features(self) -> dict[str, int]:
        """Get supported features."""

    @supported_features.setter
    @abc.abstractmethod
    def supported_features(self, value: dict[str, int]) -> None:
        """Set supported features."""

    @property
    @abc.abstractmethod
    def send_message(
        self,
    ) -> typing.Callable[
        [str | dict[str, typing.Any] | typing.Callable[[], str]], None
    ]:
        """Return the sendmessage function."""

    def require_admin(self):
        """Check admin and call function."""
        user = self.user

        if user is None or not user.is_admin:
            raise Unauthorized()

    def result_message(
        self, iden: int, result: typing.Any = None
    ) -> dict[str, typing.Any]:
        """Return a success result message."""
        return self.owner.result_message(iden, result)

    def error_message(
        self, iden: int, code: str, message: str
    ) -> dict[str, typing.Any]:
        """Return an error result message."""
        return self.owner.error_message(iden, code, message)

    def check_user(
        self,
        iden: int,
        only_owner: bool = False,
        only_system_user: bool = False,
        allow_system_user: bool = True,
        only_active_user: bool = True,
        only_inactive_user: bool = False,
    ) -> bool:
        """Check current user."""

        user = self.user
        if only_owner and not user.is_owner:
            self.send_error(iden, "only_owner", "Only allowed as owner")
            return False

        if only_system_user and not user.system_generated:
            self.send_error(iden, "only_system_user", "Only allowed as system user")
            return False

        if not allow_system_user and user.system_generated:
            self.send_error(iden, "not_system_user", "Not allowed as system user")
            return False

        if only_active_user and not user.is_active:
            self.send_error(iden, "only_active_user", "Only allowed as active user")
            return False

        if only_inactive_user and user.is_active:
            self.send_error(iden, "only_inactive_user", "Not allowed as active user")
            return False

        return True
