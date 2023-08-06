"""
Media Source Component for Smart Home - The Next Generation.

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

import mimetypes

from aiohttp import web

from ... import core
from .const import Const
from .local_source import LocalSource


# pylint: disable=unused-variable
class LocalMediaView(core.SmartHomeControllerView):
    """
    Local Media Finder View.

    Returns media files in config/media.
    """

    def __init__(self, shc: core.SmartHomeController, source: LocalSource) -> None:
        """Initialize the media view."""
        url = "/media/{source_dir_id}/{location:.*}"
        name = "media"
        super().__init__(url, name)
        self._shc = shc
        self._source = source

    async def get(
        self, _request: web.Request, source_dir_id: str, location: str
    ) -> web.FileResponse:
        """Start a GET request."""
        try:
            core.helpers.raise_if_invalid_path(location)
        except ValueError as err:
            raise web.HTTPBadRequest() from err

        if source_dir_id not in self._shc.config.media_dirs:
            raise web.HTTPNotFound()

        media_path = self._source.async_full_path(source_dir_id, location)

        # Check that the file exists
        if not media_path.is_file():
            raise web.HTTPNotFound()

        # Check that it's a media file
        mime_type, _ = mimetypes.guess_type(str(media_path))
        if not mime_type or mime_type.split("/")[0] not in Const.MEDIA_MIME_TYPES:
            raise web.HTTPNotFound()

        return web.FileResponse(media_path)
