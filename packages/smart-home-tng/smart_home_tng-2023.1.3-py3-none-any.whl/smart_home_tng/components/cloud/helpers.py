"""
Home Assistant Cloud Component for Smart Home - The Next Generation.

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
import functools
import http
import logging
import typing

import aiohttp

from ... import core

_CLOUD_ERRORS: typing.Final = {
    asyncio.TimeoutError: (
        http.HTTPStatus.BAD_GATEWAY,
        "Unable to reach the Home Assistant cloud.",
    ),
    aiohttp.ClientError: (
        http.HTTPStatus.INTERNAL_SERVER_ERROR,
        "Error making internal request",
    ),
}
_LOGGER: typing.Final = logging.getLogger(__name__)

# pylint: disable=unused-variable


def _handle_cloud_errors(handler):
    """Webview decorator to handle auth errors."""

    @functools.wraps(handler)
    async def error_handler(view, request, *args, **kwargs):
        """Handle exceptions that raise from the wrapped request handler."""
        try:
            result = await handler(view, request, *args, **kwargs)
            return result

        except Exception as err:  # pylint: disable=broad-except
            status, msg = _process_cloud_exception(err, request.path)
            return view.json_message(
                msg, status_code=status, message_code=err.__class__.__name__.lower()
            )

    return error_handler


def _process_cloud_exception(exc, where):
    """Process a cloud exception."""
    err_info = None

    for err, value_info in _CLOUD_ERRORS.items():
        if isinstance(exc, err):
            err_info = value_info
            break

    if err_info is None:
        _LOGGER.exception(f"Unexpected error processing request for {where}")
        err_info = (http.HTTPStatus.BAD_GATEWAY, f"Unexpected error: {exc}")

    return err_info


def _ws_handle_cloud_errors(handler):
    """Websocket decorator to handle auth errors."""

    @functools.wraps(handler)
    async def error_handler(connection: core.WebSocket.Connection, msg: dict):
        """Handle exceptions that raise from the wrapped handler."""
        try:
            return await handler(connection, msg)

        except Exception as err:  # pylint: disable=broad-except
            err_status, err_msg = _process_cloud_exception(err, msg["type"])
            connection.send_error(msg["id"], err_status, err_msg)

    return error_handler
