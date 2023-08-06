"""
Input Text Component for Smart Home - The Next Generation.

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

_cv: typing.TypeAlias = core.ConfigValidation


# pylint: disable=unused-variable
class Const:
    """ "Constants for the Input Text Component."""

    CONF_INITIAL: typing.Final = "initial"
    CONF_MIN: typing.Final = "min"
    CONF_MIN_VALUE: typing.Final = 0
    CONF_MAX: typing.Final = "max"
    CONF_MAX_VALUE: typing.Final = 100
    CONF_PATTERN: typing.Final = "pattern"
    CONF_VALUE: typing.Final = "value"

    MODE_TEXT: typing.Final = "text"
    MODE_PASSWORD: typing.Final = "password"

    ATTR_VALUE: typing.Final = CONF_VALUE
    ATTR_MIN: typing.Final = "min"
    ATTR_MAX: typing.Final = "max"
    ATTR_PATTERN: typing.Final = CONF_PATTERN

    SERVICE_SET_VALUE: typing.Final = "set_value"

    CREATE_FIELDS: typing.Final = {
        vol.Required(core.Const.CONF_NAME): vol.All(str, vol.Length(min=1)),
        vol.Optional(CONF_MIN, default=CONF_MIN_VALUE): vol.Coerce(int),
        vol.Optional(CONF_MAX, default=CONF_MAX_VALUE): vol.Coerce(int),
        vol.Optional(CONF_INITIAL, ""): _cv.string,
        vol.Optional(core.Const.CONF_ICON): _cv.icon,
        vol.Optional(core.Const.CONF_UNIT_OF_MEASUREMENT): _cv.string,
        vol.Optional(CONF_PATTERN): _cv.string,
        vol.Optional(core.Const.CONF_MODE, default=MODE_TEXT): vol.In(
            [MODE_TEXT, MODE_PASSWORD]
        ),
    }
    UPDATE_FIELDS: typing.Final = {
        vol.Optional(core.Const.CONF_NAME): _cv.string,
        vol.Optional(CONF_MIN): vol.Coerce(int),
        vol.Optional(CONF_MAX): vol.Coerce(int),
        vol.Optional(CONF_INITIAL): _cv.string,
        vol.Optional(core.Const.CONF_ICON): _cv.icon,
        vol.Optional(core.Const.CONF_UNIT_OF_MEASUREMENT): _cv.string,
        vol.Optional(CONF_PATTERN): _cv.string,
        vol.Optional(core.Const.CONF_MODE): vol.In([MODE_TEXT, MODE_PASSWORD]),
    }

    RELOAD_SERVICE_SCHEMA: typing.Final = vol.Schema({})
