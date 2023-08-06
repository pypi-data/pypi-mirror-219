"""
Web Socket Api Component for Smart Home - The Next Generation.

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

# pylint: disable=unused-variable, unused-import

import asyncio
import collections.abc
import contextvars
import typing
import voluptuous as vol

from ... import core, auth
from .web_socket_adapter import WebSocketAdapter
from .helpers import _error_message


class _ActiveConnection(core.WebSocket.Connection):
    """Handle an active websocket client connection."""

    def __init__(
        self,
        owner: core.WebSocket.Component,
        logger: WebSocketAdapter,
        send_message: collections.abc.Callable[
            [str | dict[str, typing.Any] | collections.abc.Callable[[], str]], None
        ],
        user: auth.User,
        refresh_token: auth.RefreshToken,
    ) -> None:
        """Initialize an active connection."""
        self._logger = logger
        self._owner = owner
        self._send_message = send_message
        self._user = user
        self._refresh_token_id = refresh_token.id
        self._subscriptions: dict[
            collections.abc.Hashable, collections.abc.Callable[[], typing.Any]
        ] = {}
        self._last_id = 0
        self._supported_features: dict[str, int] = {}
        _current_connection.set(self)

    @property
    def owner(self) -> core.WebSocket.Component:
        return self._owner

    @property
    def supported_features(self) -> dict[str, int]:
        return self._supported_features

    @supported_features.setter
    def supported_features(self, value: dict[str, int]) -> None:
        self._supported_features = value
        if value is None:
            self._supported_features = {}

    @property
    def logger(self) -> WebSocketAdapter:
        return self._logger

    @property
    def send_message(
        self,
    ) -> typing.Callable[
        [str | dict[str, typing.Any] | typing.Callable[[], str]], None
    ]:
        return self._send_message

    @property
    def subscriptions(
        self,
    ) -> dict[collections.abc.Hashable, collections.abc.Callable[[], typing.Any]]:
        return self._subscriptions

    @property
    def user(self) -> auth.User:
        return self._user

    @property
    def refresh_token_id(self) -> str:
        return self._refresh_token_id

    def context(self, _msg: dict[str, typing.Any]) -> core.Context:
        """Return a context."""
        return core.Context(user_id=self._user.id)

    async def send_big_result(self, msg_id: int, result: typing.Any) -> None:
        """Send a result message that would be expensive to JSON serialize."""
        content = await self._owner.controller.async_add_executor_job(
            core.Const.JSON_DUMP, self._owner.result_message(msg_id, result)
        )
        self._send_message(content)

    @core.callback
    def async_handle(self, msg: dict[str, typing.Any]) -> None:
        """Handle a single incoming message."""
        try:
            msg = core.WebSocket.MINIMAL_MESSAGE_SCHEMA(msg)
            cur_id = msg["id"]
        except vol.Invalid:
            self.logger.error("Received invalid command", msg)
            self.send_message(
                _error_message(
                    msg.get("id"),
                    core.WebSocket.ERR_INVALID_FORMAT,
                    "Message incorrectly formatted.",
                )
            )
            return

        if cur_id <= self._last_id:
            self.send_message(
                _error_message(
                    cur_id,
                    core.WebSocket.ERR_ID_REUSE,
                    "Identifier values have to increase.",
                )
            )
            return

        if not self._owner.has_handler(msg["type"]):
            self.logger.info(f"Received unknown command: {msg['type']}")
            self.send_message(
                _error_message(
                    cur_id, core.WebSocket.ERR_UNKNOWN_COMMAND, "Unknown command."
                )
            )
            return

        handler, schema = self._owner.get_handler(msg["type"])

        try:
            if asyncio.iscoroutinefunction(handler):
                asyncio.create_task(_handle_async_response(handler, self, schema(msg)))
            else:
                handler(self, schema(msg))
        except Exception as err:  # pylint: disable=broad-except
            self.async_handle_exception(msg, err)

        self._last_id = cur_id

    @core.callback
    def async_handle_close(self) -> None:
        """Handle closing down connection."""
        for unsub in self._subscriptions.values():
            unsub()

    @core.callback
    def async_handle_exception(
        self, msg: dict[str, typing.Any], err: Exception
    ) -> None:
        """Handle an exception while processing a handler."""
        log_handler = self._logger.error

        code = core.WebSocket.ERR_UNKNOWN_ERROR
        err_message = None

        if isinstance(err, core.Unauthorized):
            code = core.WebSocket.ERR_UNAUTHORIZED
            err_message = "Unauthorized"
        elif isinstance(err, vol.Invalid):
            code = core.WebSocket.ERR_INVALID_FORMAT
            err_message = vol.humanize.humanize_error(msg, err)
        elif isinstance(err, asyncio.TimeoutError):
            code = core.WebSocket.ERR_TIMEOUT
            err_message = "Timeout"
        elif isinstance(err, core.SmartHomeControllerError):
            err_message = str(err)

        # This if-check matches all other errors but also matches errors which
        # result in an empty message. In that case we will also log the stack
        # trace so it can be fixed.
        if not err_message:
            err_message = "Unknown error"
            log_handler = self._logger.exception

        log_handler(f"Error handling message: {err_message} ({code})")

        self._send_message(_error_message(msg["id"], code, err_message))


_current_connection = contextvars.ContextVar[_ActiveConnection](
    "current_connection", default=None
)


async def _handle_async_response(
    func: core.WebSocket.AsyncCommandHandler,
    connection: core.WebSocket.Connection,
    msg: dict[str, typing.Any],
) -> None:
    """Create a response and handle exception."""
    try:
        await func(connection, msg)
    except Exception as err:  # pylint: disable=broad-except
        connection.async_handle_exception(msg, err)
