"""
Stream Component for Smart Home - The Next Generation.

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

from aiohttp import web

from .const import Const
from .stream import Stream
from .stream_view import StreamView

if not typing.TYPE_CHECKING:

    class StreamComponent:
        pass


if typing.TYPE_CHECKING:
    from .stream_component import StreamComponent


# pylint: disable=unused-variable
class HlsInitView(StreamView):
    """Stream view to serve HLS init.mp4."""

    def __init__(self, owner: StreamComponent):
        url = r"/api/hls/{token:[a-f0-9]+}/init.mp4"
        name = "api:stream:hls:init"
        cors_allowed = True
        super().__init__(owner, url, name, cors_allowed=cors_allowed)

    async def handle(
        self, request: web.Request, stream: Stream, sequence: str, part_num: str
    ) -> web.Response:
        """Return init.mp4."""
        track = stream.add_provider(Const.HLS_PROVIDER)
        if not (segments := track.get_segments()) or not (body := segments[0].init):
            return web.HTTPNotFound()
        return web.Response(
            body=body,
            headers={"Content-Type": "video/mp4"},
        )
