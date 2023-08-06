"""
Image Component for Smart Home - The Next Generation.

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
import pathlib

import PIL as pil
from aiohttp import hdrs as web_hdrs
from aiohttp import web

from ... import core
from .const import Const
from .image_storage_collection import ImageStorageCollection


# pylint: disable=unused-variable
class ImageServeView(core.SmartHomeControllerView):
    """View to download images."""

    def __init__(
        self, image_folder: pathlib.Path, image_collection: ImageStorageCollection
    ) -> None:
        """Initialize image serve view."""
        url = "/api/image/serve/{image_id}/{filename}"
        name = "api:image:serve"
        super().__init__(url, name, requires_auth=False)

        self._transform_lock = asyncio.Lock()
        self._image_folder = image_folder
        self._images = image_collection

    async def get(self, request: web.Request, image_id: str, filename: str):
        """Serve image."""
        image_size = filename.split("-", 1)[0]
        try:
            parts = image_size.split("x", 1)
            width = int(parts[0])
            height = int(parts[1])
        except (ValueError, IndexError) as err:
            raise web.HTTPBadRequest from err

        if not width or width != height or width not in Const.VALID_SIZES:
            raise web.HTTPBadRequest

        image_info = self._images.get_item(image_id)

        if image_info is None:
            raise web.HTTPNotFound()

        shc = request.app[core.Const.KEY_SHC]
        target_file = pathlib.Path(self._image_folder, image_id, f"{width}x{height}")

        if not target_file.is_file():
            async with self._transform_lock:
                # Another check in case another request already finished it while waiting
                if not target_file.is_file():
                    await shc.async_add_executor_job(
                        _generate_thumbnail,
                        pathlib.Path(self._image_folder, image_id, "original"),
                        image_info["content_type"],
                        target_file,
                        (width, height),
                    )

        return web.FileResponse(
            target_file,
            headers={
                **core.Const.CACHE_HEADERS,
                web_hdrs.CONTENT_TYPE: image_info["content_type"],
            },
        )


def _generate_thumbnail(original_path, content_type, target_path, target_size):
    """Generate a size."""
    image = pil.ImageOps.exif_transpose(pil.Image.open(original_path))
    image.thumbnail(target_size)
    image.save(target_path, format=content_type.split("/", 1)[1])
