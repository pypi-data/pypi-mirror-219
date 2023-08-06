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

import logging
import pathlib
import shutil
import typing

import voluptuous as vol
from aiohttp import web, web_request

from ... import core
from .const import Const
from .local_source import LocalSource
from .media_source_item import MediaSourceItem

if not typing.TYPE_CHECKING:

    class MediaSourceComponent:
        ...


if typing.TYPE_CHECKING:
    from .media_source_component import MediaSourceComponent


_MAX_UPLOAD_SIZE: typing.Final = 1024 * 1024 * 10
_LOGGER: typing.Final = logging.getLogger(__name__)
_SCHEMA: typing.Final = vol.Schema(
    {
        "media_content_id": str,
        "file": web_request.FileField,
    }
)


# pylint: disable=unused-variable
class UploadMediaView(core.SmartHomeControllerView):
    """View to upload images."""

    def __init__(self, owner: MediaSourceComponent, source: LocalSource) -> None:
        """Initialize the media view."""

        url = "/api/media_source/local_source/upload"
        name = "api:media_source:local_source:upload"
        super().__init__(url, name)

        self._owner = owner
        self._source = source

    async def post(self, request: web.Request) -> web.Response:
        """Handle upload."""
        if not request[core.Const.KEY_SHC_USER].is_admin:
            raise core.Unauthorized()

        # Increase max payload
        request._client_max_size = _MAX_UPLOAD_SIZE  # pylint: disable=protected-access

        try:
            data = _SCHEMA(dict(await request.post()))
        except vol.Invalid as err:
            _LOGGER.error(f"Received invalid upload data: {err}")
            raise web.HTTPBadRequest() from err

        try:
            item = MediaSourceItem.from_uri(self._owner, data["media_content_id"], None)
        except ValueError as err:
            _LOGGER.error(f"Received invalid upload data: {err}")
            raise web.HTTPBadRequest() from err

        try:
            source_dir_id, location = self._source.async_parse_identifier(item)
        except core.Unresolvable as err:
            _LOGGER.error("Invalid local source ID")
            raise web.HTTPBadRequest() from err

        uploaded_file: web_request.FileField = data["file"]

        if not uploaded_file.content_type.startswith(Const.VALID_CONTENT_TYPES):
            _LOGGER.error("Content type not allowed")
            raise vol.Invalid("Only images and video are allowed")

        try:
            core.helpers.raise_if_invalid_filename(uploaded_file.filename)
        except ValueError as err:
            _LOGGER.error("Invalid filename")
            raise web.HTTPBadRequest() from err

        try:
            await self._owner.controller.async_add_executor_job(
                self._move_file,
                self._source.async_full_path(source_dir_id, location),
                uploaded_file,
            )
        except ValueError as err:
            _LOGGER.error(f"Moving upload failed: {err}")
            raise web.HTTPBadRequest() from err

        return self.json(
            {"media_content_id": f"{data['media_content_id']}/{uploaded_file.filename}"}
        )

    def _move_file(
        self, target_dir: pathlib.Path, uploaded_file: web_request.FileField
    ) -> None:
        """Move file to target."""
        if not target_dir.is_dir():
            raise ValueError("Target is not an existing directory")

        target_path = target_dir / uploaded_file.filename

        target_path.relative_to(target_dir)
        core.helpers.raise_if_invalid_path(str(target_path))

        with target_path.open("wb") as target_fp:
            shutil.copyfileobj(uploaded_file.file, target_fp)
