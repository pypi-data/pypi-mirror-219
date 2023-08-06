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

import collections.abc
import typing

import voluptuous as vol
import voluptuous.humanize as vh
from aiohttp import web

from ... import auth, core
from .disconnect import Disconnect
from .web_socket_adapter import WebSocketAdapter
from .active_connection import _ActiveConnection

_TYPE_AUTH: typing.Final = "auth"
_TYPE_AUTH_INVALID: typing.Final = "auth_invalid"
_TYPE_AUTH_OK: typing.Final = "auth_ok"
_TYPE_AUTH_REQUIRED: typing.Final = "auth_required"

_AUTH_MESSAGE_SCHEMA: typing.Final = vol.Schema(
    {
        vol.Required("type"): _TYPE_AUTH,
        vol.Required("access_token", "auth"): str,
    }
)


def _auth_ok_message() -> dict[str, str]:
    """Return an auth_ok message."""
    return {"type": _TYPE_AUTH_OK, "ha_version": core.Const.__version__}


def _auth_required_message() -> dict[str, str]:
    """Return an auth_required message."""
    return {"type": _TYPE_AUTH_REQUIRED, "ha_version": core.Const.__version__}


def _auth_invalid_message(message: str) -> dict[str, str]:
    """Return an auth_invalid message."""
    return {"type": _TYPE_AUTH_INVALID, "message": message}


# pylint: disable=unused-variable
class AuthPhase:
    """Connection that requires client to authenticate first."""

    def __init__(
        self,
        owner: core.WebSocket.Component,
        logger: WebSocketAdapter,
        send_message: collections.abc.Callable[
            [str | dict[str, typing.Any] | collections.abc.Callable[[], str]], None
        ],
        cancel_ws: core.CallbackType,
        request: web.Request,
    ) -> None:
        """Initialize the authentiated connection."""
        self._owner = owner
        self._send_message = send_message
        self._cancel_ws = cancel_ws
        self._logger = logger
        self._request = request

    @staticmethod
    def auth_required_message() -> dict[str, str]:
        return _auth_required_message().copy()

    async def async_handle(self, msg: dict[str, str]) -> core.WebSocket.Connection:
        """Handle authentication."""
        try:
            msg = _AUTH_MESSAGE_SCHEMA(msg)
        except vol.Invalid as err:
            error_msg = (
                f"Auth message incorrectly formatted: {vh.humanize_error(msg, err)}"
            )
            self._logger.warning(error_msg)
            self._send_message(_auth_invalid_message(error_msg))
            raise Disconnect from err

        if "access_token" in msg:
            self._logger.debug("Received access_token")
            refresh_token = (
                await self._owner.controller.auth.async_validate_access_token(
                    msg["access_token"]
                )
            )
            if refresh_token is not None:
                conn = await self._async_finish_auth(refresh_token.user, refresh_token)
                conn.subscriptions[
                    "auth"
                ] = self._owner.controller.auth.async_register_revoke_token_callback(
                    refresh_token.id, self._cancel_ws
                )

                return conn

        self._send_message(_auth_invalid_message("Invalid access token or password"))
        await self._owner.controller.http.process_wrong_login(self._request)
        raise Disconnect

    async def _async_finish_auth(
        self, user: auth.User, refresh_token: auth.RefreshToken
    ) -> core.WebSocket.Connection:
        """Create an active connection."""
        self._logger.debug("Auth OK")
        await self._owner.controller.http.process_success_login(self._request)
        self._send_message(_auth_ok_message())
        return _ActiveConnection(
            self._owner, self._logger, self._send_message, user, refresh_token
        )
