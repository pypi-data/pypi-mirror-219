"""
Tag Component for Smart Home - The Next Generation.

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
import uuid

import voluptuous as vol

from ... import core
from .const import Const

_CREATE_SCHEMA: typing.Final = vol.Schema(Const.CREATE_FIELDS)
_UPDATE_SCHEMA: typing.Final = vol.Schema(Const.UPDATE_FIELDS)


# pylint: disable=unused-variable
class TagStorageCollection(core.StorageCollection):
    """Tag collection stored in storage."""

    async def _process_create_data(self, data: dict) -> dict:
        """Validate the config is valid."""
        data = _CREATE_SCHEMA(data)
        if not data[Const.TAG_ID]:
            data[Const.TAG_ID] = str(uuid.uuid4())
        # make last_scanned JSON serializeable
        if Const.LAST_SCANNED in data:
            data[Const.LAST_SCANNED] = data[Const.LAST_SCANNED].isoformat()
        return data

    @core.callback
    def _get_suggested_id(self, info: dict[str, str]) -> str:
        """Suggest an ID based on the config."""
        return info[Const.TAG_ID]

    async def _update_data(self, data: dict, update_data: dict) -> dict:
        """Return a new updated data object."""
        data = {**data, **_UPDATE_SCHEMA(update_data)}
        # make last_scanned JSON serializeable
        if Const.LAST_SCANNED in update_data:
            data[Const.LAST_SCANNED] = data[Const.LAST_SCANNED].isoformat()
        return data
