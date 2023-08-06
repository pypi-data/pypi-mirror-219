"""
Camera Component for Smart Home - The Next Generation.

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

import logging
import typing

from aiohttp import web

from ... import core
from .camera_view import CameraView

_LOGGER: typing.Final = logging.getLogger(__name__)
_MIN_STREAM_INTERVAL: typing.Final = 0.5  # seconds


# pylint: disable=unused-variable
class CameraMjpegStream(CameraView):
    """Camera View to serve an MJPEG stream."""

    def __init__(self, component: core.EntityComponent):
        url = "/api/camera_proxy_stream/{entity_id}"
        name = "api:camera:stream"
        super().__init__(component, url, name)

    async def handle(
        self, request: web.Request, camera: core.Camera
    ) -> web.StreamResponse:
        """Serve camera stream, possibly with interval."""
        if (interval_str := request.query.get("interval")) is None:
            try:
                stream = await camera.handle_async_mjpeg_stream(request)
            except ConnectionResetError:
                stream = None
                _LOGGER.debug("Error while writing MJPEG stream to transport")
            if stream is None:
                raise web.HTTPBadGateway()
            return stream

        try:
            # Compose camera stream from stills
            interval = float(interval_str)
            if interval < _MIN_STREAM_INTERVAL:
                raise ValueError(f"Stream interval must be be > {_MIN_STREAM_INTERVAL}")
            return await camera.handle_async_still_stream(request, interval)
        except ValueError as err:
            raise web.HTTPBadRequest() from err
