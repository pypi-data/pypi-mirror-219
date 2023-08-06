"""
Input Select Component for Smart Home - The Next Generation.

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
from .util import _cv_input_select

_CREATE_SCHEMA: typing.Final = vol.Schema(
    vol.All(Const.CREATE_FIELDS, _cv_input_select)
)
_UPDATE_SCHEMA: typing.Final = vol.Schema(Const.UPDATE_FIELDS)


# pylint: disable=unused-variable
class InputSelectStorageCollection(core.StorageCollection):
    """Input storage based collection."""

    async def _process_create_data(
        self, data: dict[str, typing.Any]
    ) -> dict[str, typing.Any]:
        """Validate the config is valid."""
        return typing.cast(dict[str, typing.Any], _CREATE_SCHEMA(data))

    @core.callback
    def _get_suggested_id(self, info: dict[str, typing.Any]) -> str:
        """Suggest an ID based on the config."""
        return typing.cast(str, info[core.Const.CONF_NAME])

    async def _update_data(
        self, data: dict[str, typing.Any], update_data: dict[str, typing.Any]
    ) -> dict[str, typing.Any]:
        """Return a new updated data object."""
        update_data = _UPDATE_SCHEMA(update_data)
        return _cv_input_select({**data, **update_data})
