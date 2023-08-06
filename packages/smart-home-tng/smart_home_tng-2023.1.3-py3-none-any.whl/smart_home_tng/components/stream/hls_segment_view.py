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

import http
import typing

from aiohttp import web

from .const import Const
from .hls_stream_output import HlsStreamOutput
from .stream import Stream
from .stream_view import StreamView

if not typing.TYPE_CHECKING:

    class StreamComponent:
        pass


if typing.TYPE_CHECKING:
    from .stream_component import StreamComponent


# pylint: disable=unused-variable
class HlsSegmentView(StreamView):
    """Stream view to serve a HLS fmp4 segment."""

    def __init__(self, owner: StreamComponent):
        url = r"/api/hls/{token:[a-f0-9]+}/segment/{sequence:\d+}.m4s"
        name = "api:stream:hls:segment"
        cors_allowed = True
        super().__init__(owner, url, name, cors_allowed=cors_allowed)

    async def handle(
        self, request: web.Request, stream: Stream, sequence: str, part_num: str
    ) -> web.StreamResponse:
        """Handle segments."""
        # pylint: disable=protected-access
        track: HlsStreamOutput = stream._internal_add_provider(Const.HLS_PROVIDER)
        track.idle_timer.awake()
        # Ensure that we have a segment. If the request is from a hint for part 0
        # of a segment, there is a small chance it may have arrived before the
        # segment has been put. If this happens, wait for one part and retry.
        if not (
            (segment := track.get_segment(int(sequence)))
            or (
                await track.part_recv(timeout=track.stream_settings.hls_part_timeout)
                and (segment := track.get_segment(int(sequence)))
            )
        ):
            return web.Response(
                body=None,
                status=http.HTTPStatus.NOT_FOUND,
            )
        return web.Response(
            body=segment.get_data(),
            headers={
                "Content-Type": "video/iso.segment",
            },
        )
