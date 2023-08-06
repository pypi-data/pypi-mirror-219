"""
Core components of Smart Home - The Next Generation.

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

from .config_validation import ConfigValidation as _cv
from .const import Const


# pylint: disable=unused-variable
class InputNumber:
    """InputNumber namespace."""

    CONF_INITIAL: typing.Final = "initial"
    CONF_MIN: typing.Final = "min"
    CONF_MAX: typing.Final = "max"
    CONF_STEP: typing.Final = "step"

    MODE_SLIDER: typing.Final = "slider"
    MODE_BOX: typing.Final = "box"

    ATTR_INITIAL: typing.Final = "initial"
    ATTR_VALUE: typing.Final = "value"
    ATTR_MIN: typing.Final = "min"
    ATTR_MAX: typing.Final = "max"
    ATTR_STEP: typing.Final = "step"

    SERVICE_SET_VALUE: typing.Final = "set_value"
    SERVICE_INCREMENT: typing.Final = "increment"
    SERVICE_DECREMENT: typing.Final = "decrement"

    CREATE_FIELDS: typing.Final = {
        vol.Required(Const.CONF_NAME): vol.All(str, vol.Length(min=1)),
        vol.Required(CONF_MIN): vol.Coerce(float),
        vol.Required(CONF_MAX): vol.Coerce(float),
        vol.Optional(CONF_INITIAL): vol.Coerce(float),
        vol.Optional(CONF_STEP, default=1): vol.All(
            vol.Coerce(float), vol.Range(min=1e-9)
        ),
        vol.Optional(Const.CONF_ICON): _cv.icon,
        vol.Optional(Const.CONF_UNIT_OF_MEASUREMENT): _cv.string,
        vol.Optional(Const.CONF_MODE, default=MODE_SLIDER): vol.In(
            [MODE_BOX, MODE_SLIDER]
        ),
    }

    UPDATE_FIELDS: typing.Final = {
        vol.Optional(Const.CONF_NAME): _cv.string,
        vol.Optional(CONF_MIN): vol.Coerce(float),
        vol.Optional(CONF_MAX): vol.Coerce(float),
        vol.Optional(CONF_INITIAL): vol.Coerce(float),
        vol.Optional(CONF_STEP): vol.All(vol.Coerce(float), vol.Range(min=1e-9)),
        vol.Optional(Const.CONF_ICON): _cv.icon,
        vol.Optional(Const.CONF_UNIT_OF_MEASUREMENT): _cv.string,
        vol.Optional(Const.CONF_MODE): vol.In([MODE_BOX, MODE_SLIDER]),
    }

    RELOAD_SERVICE_SCHEMA: typing.Final = vol.Schema({})
