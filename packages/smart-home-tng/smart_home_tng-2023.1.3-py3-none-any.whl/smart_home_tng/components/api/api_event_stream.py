"""
Rest API for Smart Home - The Next Generation.

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
import json
import logging
import typing

import async_timeout
from aiohttp import web

from ... import core
from .const import Const

_LOGGER: typing.Final = logging.getLogger(__name__)


# pylint: disable=unused-variable
class APIEventStream(core.SmartHomeControllerView):
    """View to handle EventStream requests."""

    def __init__(self):
        super().__init__(core.Const.URL_API_STREAM, "api:stream")

    async def get(self, request):
        """Provide a streaming interface for the event bus."""
        if not request[core.Const.KEY_SHC_USER].is_admin:
            raise core.Unauthorized()
        shc = request.app[core.Const.KEY_SHC]
        stop_obj = object()
        to_write = asyncio.Queue()

        if restrict := request.query.get("restrict"):
            restrict = restrict.split(",") + [core.Const.EVENT_SHC_STOP]

        async def forward_events(event):
            """Forward events to the open request."""
            if restrict and event.event_type not in restrict:
                return

            _LOGGER.debug(f"STREAM {id(stop_obj)} FORWARDING {event}")

            if event.event_type == core.Const.EVENT_SHC_STOP:
                data = stop_obj
            else:
                data = json.dumps(event, cls=core.JsonEncoder)

            await to_write.put(data)

        response = web.StreamResponse()
        response.content_type = "text/event-stream"
        await response.prepare(request)

        unsub_stream = shc.bus.async_listen(core.Const.MATCH_ALL, forward_events)

        try:
            _LOGGER.debug(f"STREAM {id(stop_obj)} ATTACHED", id(stop_obj))

            # Fire off one message so browsers fire open event right away
            await to_write.put(Const.STREAM_PING_PAYLOAD)

            while True:
                try:
                    async with async_timeout.timeout(Const.STREAM_PING_INTERVAL):
                        payload = await to_write.get()

                    if payload is stop_obj:
                        break

                    msg = f"data: {payload}\n\n"
                    _LOGGER.debug(f"STREAM {id(stop_obj)} WRITING {msg.strip()}")
                    await response.write(msg.encode("UTF-8"))
                except asyncio.TimeoutError:
                    await to_write.put(Const.STREAM_PING_PAYLOAD)

        except asyncio.CancelledError:
            _LOGGER.debug(f"STREAM {id(stop_obj)} ABORT")

        finally:
            _LOGGER.debug(f"STREAM {id(stop_obj)} RESPONSE CLOSED", id(stop_obj))
            unsub_stream()

        return response
