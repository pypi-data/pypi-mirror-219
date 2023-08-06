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

import asyncio
import collections.abc
import contextlib
import datetime
import logging
import typing

import async_timeout
from aiohttp import WSMsgType, web

from ... import core
from .auth_phase import AuthPhase
from .disconnect import Disconnect
from .helpers import _error_message
from .web_socket_adapter import WebSocketAdapter

_LOGGER: typing.Final = logging.getLogger(__name__)
_WS_LOGGER: typing.Final = logging.getLogger(f"{__name__}.connection")


# pylint: disable=unused-variable
class WebSocketHandler:
    """Handle an active websocket client connection."""

    def __init__(self, owner: core.WebSocket.Component, request: web.Request) -> None:
        """Initialize an active connection."""
        self._owner = owner
        self._request = request
        self._wsock = web.WebSocketResponse(heartbeat=55)
        self._to_write: asyncio.Queue = asyncio.Queue(
            maxsize=core.WebSocket.MAX_PENDING_MSG
        )
        self._handle_task: asyncio.Task = None
        self._writer_task: asyncio.Task = None
        self._logger = WebSocketAdapter(_WS_LOGGER, {"connid": id(self)})
        self._peak_checker_unsub: collections.abc.Callable[[], None] = None

    async def _writer(self) -> None:
        """Write outgoing messages."""
        # Exceptions if Socket disconnected or cancelled by connection handler
        with contextlib.suppress(
            RuntimeError, ConnectionResetError, *core.WebSocket.CANCELLATION_ERRORS
        ):
            while not self._wsock.closed:
                if (process := await self._to_write.get()) is None:
                    break

                if not isinstance(process, str):
                    message: str = process()
                else:
                    message = process
                self._logger.debug(f"Sending {message}")
                await self._wsock.send_str(message)

        # Clean up the peaker checker when we shut down the writer
        if self._peak_checker_unsub is not None:
            self._peak_checker_unsub()
            self._peak_checker_unsub = None

    @core.callback
    def _send_message(
        self, message: str | dict[str, typing.Any] | collections.abc.Callable[[], str]
    ) -> None:
        """Send a message to the client.

        Closes connection if the client is not reading the messages.

        Async friendly.
        """
        if isinstance(message, dict):
            message = _message_to_json(message)

        try:
            self._to_write.put_nowait(message)
        except asyncio.QueueFull:
            self._logger.error(
                f"Client exceeded max pending messages [2]: {core.WebSocket.MAX_PENDING_MSG}"
            )

            self._cancel()

        if self._to_write.qsize() < core.WebSocket.PENDING_MSG_PEAK:
            if self._peak_checker_unsub:
                self._peak_checker_unsub()
                self._peak_checker_unsub = None
            return

        if self._peak_checker_unsub is None:
            self._peak_checker_unsub = self._owner.controller.tracker.async_call_later(
                core.WebSocket.PENDING_MSG_PEAK_TIME, self._check_write_peak
            )

    @core.callback
    def _check_write_peak(self, _utc_time: datetime.datetime) -> None:
        """Check that we are no longer above the write peak."""
        self._peak_checker_unsub = None

        if self._to_write.qsize() < core.WebSocket.PENDING_MSG_PEAK:
            return

        self._logger.error(
            "Client unable to keep up with pending messages. Stayed over "
            + f"{core.WebSocket.PENDING_MSG_PEAK} for "
            + f"{core.WebSocket.PENDING_MSG_PEAK_TIME} seconds"
        )
        self._cancel()

    @core.callback
    def _cancel(self) -> None:
        """Cancel the connection."""
        if self._handle_task is not None:
            self._handle_task.cancel()
        if self._writer_task is not None:
            self._writer_task.cancel()

    async def async_handle(self) -> web.WebSocketResponse:
        """Handle a websocket response."""
        request = self._request
        wsock = self._wsock
        try:
            async with async_timeout.timeout(10):
                await wsock.prepare(request)
        except asyncio.TimeoutError:
            self._logger.warning(f"Timeout preparing request from {request.remote}")
            return wsock

        self._logger.debug(f"Connected from {request.remote}")
        self._handle_task = asyncio.current_task()

        @core.callback
        def handle_shc_stop(_event: core.Event) -> None:
            """Cancel this connection."""
            self._cancel()

        unsub_stop = self._owner.controller.bus.async_listen(
            core.Const.EVENT_SHC_STOP, handle_shc_stop
        )

        # As the webserver is now started before the start
        # event we do not want to block for websocket responses
        self._writer_task = asyncio.create_task(self._writer())

        auth = AuthPhase(
            self._owner, self._logger, self._send_message, self._cancel, request
        )
        connection = None
        disconnect_warn = None

        try:
            self._send_message(AuthPhase.auth_required_message())

            # Auth Phase
            try:
                async with async_timeout.timeout(10):
                    msg = await wsock.receive()
            except asyncio.TimeoutError as err:
                disconnect_warn = "Did not receive auth message within 10 seconds"
                raise Disconnect from err

            if msg.type in (WSMsgType.CLOSE, WSMsgType.CLOSING):
                raise Disconnect

            if msg.type != WSMsgType.TEXT:
                disconnect_warn = "Received non-Text message."
                raise Disconnect

            try:
                msg_data = msg.json()
            except ValueError as err:
                disconnect_warn = "Received invalid JSON."
                raise Disconnect from err

            self._logger.debug(f"Received {msg_data}")
            connection = await auth.async_handle(msg_data)
            self._owner.connection_opened()

            # Command phase
            while not wsock.closed:
                msg = await wsock.receive()

                if msg.type in (WSMsgType.CLOSE, WSMsgType.CLOSING):
                    break

                if msg.type != WSMsgType.TEXT:
                    disconnect_warn = "Received non-Text message."
                    break

                try:
                    msg_data = msg.json()
                except ValueError:
                    disconnect_warn = "Received invalid JSON."
                    break

                self._logger.debug(f"Received {msg_data}")
                connection.async_handle(msg_data)

        except asyncio.CancelledError:
            self._logger.info("Connection closed by client")

        except Disconnect:
            pass

        except Exception:  # pylint: disable=broad-except
            self._logger.exception("Unexpected error inside websocket API")

        finally:
            unsub_stop()

            if connection is not None:
                connection.async_handle_close()

            try:
                self._to_write.put_nowait(None)
                # Make sure all error messages are written before closing
                await self._writer_task
                await wsock.close()
            except asyncio.QueueFull:  # can be raised by put_nowait
                self._writer_task.cancel()

            finally:
                if disconnect_warn is None:
                    self._logger.debug("Disconnected")
                else:
                    self._logger.warning("Disconnected: %s", disconnect_warn)

                if connection is not None:
                    self._owner.connection_closed()

        return wsock


def _message_to_json(message: dict[str, typing.Any]) -> str:
    """Serialize a websocket message to json."""
    try:
        return core.Const.JSON_DUMP(message)
    except (ValueError, TypeError):
        # pylint: disable=unexpected-keyword-arg
        msg = core.helpers.format_unserializable_data(
            core.helpers.find_paths_unserializable_data(
                message, dump_func=core.Const.JSON_DUMP
            )
        )
        _LOGGER.error(f"Unable to serialize to JSON. Bad data found at {msg}")
        return core.Const.JSON_DUMP(
            _error_message(
                message["id"],
                core.WebSocket.ERR_UNKNOWN_ERROR,
                "Invalid JSON in response",
            )
        )
