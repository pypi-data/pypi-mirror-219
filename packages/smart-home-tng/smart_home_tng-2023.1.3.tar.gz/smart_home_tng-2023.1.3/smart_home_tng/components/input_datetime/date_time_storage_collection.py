"""
Input Datetime Component for Smart Home - The Next Generation.

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

import voluptuous as vol

from ... import core
from .const import Const
from .utils import has_date_or_time

_CREATE_SCHEMA: typing.Final = vol.Schema(Const.CREATE_FIELDS)
_UPDATE_SCHEMA: typing.Final = vol.Schema(Const.UPDATE_FIELDS)


# pylint: disable=unused-variable
class DateTimeStorageCollection(core.StorageCollection):
    """Input storage based collection."""

    async def _process_create_data(self, data: dict) -> dict:
        """Validate the config is valid."""
        create_data = _CREATE_SCHEMA(data)
        return has_date_or_time(create_data)

    @core.callback
    def _get_suggested_id(self, info: dict) -> str:
        """Suggest an ID based on the config."""
        return info[core.Const.CONF_NAME]

    async def _update_data(self, data: dict, update_data: dict) -> dict:
        """Return a new updated data object."""
        update_data = _UPDATE_SCHEMA(update_data)
        return has_date_or_time({**data, **update_data})
