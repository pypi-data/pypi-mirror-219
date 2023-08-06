"""
Timer Component for Smart Home - The Next Generation.

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
from .timer import _format_timedelta

_timer: typing.TypeAlias = core.Timer

_CREATE_SCHEMA: typing.Final = vol.Schema(_timer.CREATE_FIELDS)
_UPDATE_SCHEMA: typing.Final = vol.Schema(_timer.UPDATE_FIELDS)


# pylint: disable=unused-variable
class TimerStorageCollection(core.StorageCollection):
    """Timer storage based collection."""

    async def _process_create_data(self, data: dict) -> dict:
        """Validate the config is valid."""
        data = _CREATE_SCHEMA(data)
        # make duration JSON serializeable
        data[_timer.CONF_DURATION] = _format_timedelta(data[_timer.CONF_DURATION])
        return data

    @core.callback
    def _get_suggested_id(self, info: dict) -> str:
        """Suggest an ID based on the config."""
        return info[core.Const.CONF_NAME]

    async def _update_data(self, data: dict, update_data: dict) -> dict:
        """Return a new updated data object."""
        data = {**data, **_UPDATE_SCHEMA(update_data)}
        # make duration JSON serializeable
        if _timer.CONF_DURATION in update_data:
            data[_timer.CONF_DURATION] = _format_timedelta(data[_timer.CONF_DURATION])
        return data
