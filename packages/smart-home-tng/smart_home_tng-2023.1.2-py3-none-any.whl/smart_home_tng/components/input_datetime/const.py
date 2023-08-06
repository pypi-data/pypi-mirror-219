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

import datetime
import typing
import voluptuous as vol

from ... import core

_cv: typing.TypeAlias = core.ConfigValidation


# pylint: disable=unused-variable
class Const:
    """Constants for the Input Datetime component."""

    CONF_HAS_DATE: typing.Final = "has_date"
    CONF_HAS_TIME: typing.Final = "has_time"
    CONF_INITIAL: typing.Final = "initial"

    DEFAULT_TIME: typing.Final = datetime.time(0, 0, 0)

    ATTR_DATETIME: typing.Final = "datetime"
    ATTR_TIMESTAMP: typing.Final = "timestamp"

    FMT_DATE: typing.Final = "%Y-%m-%d"
    FMT_TIME: typing.Final = "%H:%M:%S"
    FMT_DATETIME: typing.Final = f"{FMT_DATE} {FMT_TIME}"

    CREATE_FIELDS: typing.Final = {
        vol.Required(core.Const.CONF_NAME): vol.All(str, vol.Length(min=1)),
        vol.Optional(CONF_HAS_DATE, default=False): _cv.boolean,
        vol.Optional(CONF_HAS_TIME, default=False): _cv.boolean,
        vol.Optional(core.Const.CONF_ICON): _cv.icon,
        vol.Optional(CONF_INITIAL): _cv.string,
    }
    UPDATE_FIELDS: typing.Final = {
        vol.Optional(core.Const.CONF_NAME): _cv.string,
        vol.Optional(CONF_HAS_DATE): _cv.boolean,
        vol.Optional(CONF_HAS_TIME): _cv.boolean,
        vol.Optional(core.Const.CONF_ICON): _cv.icon,
        vol.Optional(CONF_INITIAL): _cv.string,
    }
    RELOAD_SERVICE_SCHEMA: typing.Final = vol.Schema({})
