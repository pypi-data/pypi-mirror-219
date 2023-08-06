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

import typing

from ... import core
from .const import Const
from .image_serve_view import ImageServeView
from .image_storage_collection import ImageStorageCollection
from .image_upload_view import ImageUploadView


# pylint: disable=unused-variable
class ImageComponent(core.SmartHomeControllerComponent):
    """The Picture integration."""

    def __init__(self, path: typing.Iterable[str]):
        super().__init__(path)
        self._images: ImageStorageCollection = None

    async def async_setup(self, config: core.ConfigType) -> bool:
        """Set up the Image integration."""
        if not await super().async_setup(config):
            return False

        shc = self._shc

        image_dir = self._shc.config.path(self.domain)
        self._images = ImageStorageCollection(self, image_dir)
        await self._images.async_load()
        core.StorageCollectionWebSocket(
            self._images,
            self.domain,
            self.domain,
            Const.CREATE_FIELDS,
            Const.UPDATE_FIELDS,
        ).async_setup(create_create=False)

        shc.register_view(ImageUploadView(self._images))
        shc.register_view(ImageServeView(image_dir, self._images))
        return True
