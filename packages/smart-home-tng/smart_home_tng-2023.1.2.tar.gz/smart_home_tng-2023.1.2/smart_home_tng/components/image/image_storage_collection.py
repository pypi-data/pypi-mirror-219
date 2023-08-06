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

import logging
import pathlib
import secrets
import shutil
import typing

import PIL as pil
from PIL import Image as pil_image
import voluptuous as vol
from aiohttp import web_request

from ... import core
from .const import Const

if not typing.TYPE_CHECKING:

    class ImageComponent:
        ...


if typing.TYPE_CHECKING:
    from .image_component import ImageComponent

_LOGGER: typing.Final = logging.getLogger(__name__)
_CREATE_SCHEMA: typing.Final = vol.Schema(Const.CREATE_FIELDS)
_UPDATE_SCHEMA: typing.Final = vol.Schema(Const.UPDATE_FIELDS)


# pylint: disable=unused-variable
class ImageStorageCollection(core.StorageCollection):
    """Image collection stored in storage."""

    def __init__(self, owner: ImageComponent, image_dir: pathlib.Path) -> None:
        """Initialize media storage collection."""
        super().__init__(
            core.Store(owner.controller, owner.storage_version, owner.storage_key),
            logging.getLogger(f"{__name__}.storage_collection"),
        )
        self.async_add_listener(self._change_listener)
        self._image_dir = image_dir

    async def _process_create_data(self, data: dict) -> dict:
        """Validate the config is valid."""
        data = _CREATE_SCHEMA(dict(data))
        uploaded_file: web_request.FileField = data["file"]

        if not uploaded_file.content_type.startswith("image/"):
            raise vol.Invalid("Only images are allowed")

        data[core.Const.CONF_ID] = secrets.token_hex(16)
        data["filesize"] = await self._shc.async_add_executor_job(self._move_data, data)

        data["content_type"] = uploaded_file.content_type
        data["name"] = uploaded_file.filename
        data["uploaded_at"] = core.helpers.utcnow().isoformat()

        return data

    def _move_data(self, data):
        """Move data."""
        uploaded_file: web_request.FileField = data.pop("file")

        # Verify we can read the image
        try:
            image = pil_image.open(uploaded_file.file)
        except pil.UnidentifiedImageError as err:
            raise vol.Invalid("Unable to identify image file") from err

        # Reset content
        uploaded_file.file.seek(0)

        media_folder = pathlib.Path(self._image_dir, data[core.Const.CONF_ID])
        media_folder.mkdir(parents=True)

        media_file = media_folder / "original"

        # Raises if path is no longer relative to the media dir
        media_file.relative_to(media_folder)

        _LOGGER.debug(f"Storing file {media_file}")

        with media_file.open("wb") as target:
            shutil.copyfileobj(uploaded_file.file, target)

        image.close()

        return media_file.stat().st_size

    @core.callback
    def _get_suggested_id(self, info: dict) -> str:
        """Suggest an ID based on the config."""
        return info[core.Const.CONF_ID]

    async def _update_data(self, data: dict, update_data: dict) -> dict:
        """Return a new updated data object."""
        return {**data, **_UPDATE_SCHEMA(update_data)}

    async def _change_listener(self, change_type, item_id, _data):
        """Handle change."""
        if change_type != core.Const.EVENT_COLLECTION_CHANGE_REMOVED:
            return

        await self._shc.async_add_executor_job(shutil.rmtree, self._image_dir / item_id)
