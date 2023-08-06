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

import asyncio
import contextlib

import async_timeout
from aiohttp import web

from ... import core
from .camera_view import CameraView
from .image_utils import _scale_jpeg_camera_image


# pylint: disable=unused-variable
class CameraImageView(CameraView):
    """Camera view to serve an image."""

    def __init__(self, component: core.EntityComponent):
        url = "/api/camera_proxy/{entity_id}"
        name = "api:camera:image"
        super().__init__(component, url, name)

    async def handle(self, request: web.Request, camera: core.Camera) -> web.Response:
        """Serve camera image."""
        width = request.query.get("width")
        height = request.query.get("height")
        try:
            image = await _async_get_image(
                camera,
                core.Const.CAMERA_IMAGE_TIMEOUT,
                int(width) if width else None,
                int(height) if height else None,
            )
        except (core.SmartHomeControllerError, ValueError) as ex:
            raise web.HTTPInternalServerError() from ex
        return web.Response(body=image.content, content_type=image.content_type)


async def _async_get_image(
    camera: core.Camera,
    timeout: int = 10,
    width: int = None,
    height: int = None,
) -> core.Image:
    """Fetch a snapshot image from a camera.

    If width and height are passed, an attempt to scale
    the image will be made on a best effort basis.
    Not all cameras can scale images or return jpegs
    that we can scale, however the majority of cases
    are handled.
    """
    with contextlib.suppress(asyncio.CancelledError, asyncio.TimeoutError):
        async with async_timeout.timeout(timeout):
            if image_bytes := await camera.async_camera_image(
                width=width, height=height
            ):
                content_type = camera.content_type
                image = core.Image(content_type, image_bytes)
                if (
                    width is not None
                    and height is not None
                    and ("jpeg" in content_type or "jpg" in content_type)
                ):
                    assert width is not None
                    assert height is not None
                    return core.Image(
                        content_type, _scale_jpeg_camera_image(image, width, height)
                    )

                return image

    raise core.SmartHomeControllerError("Unable to get image")
