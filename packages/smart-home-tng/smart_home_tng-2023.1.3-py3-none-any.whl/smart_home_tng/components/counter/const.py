"""
Counter Integration for Smart Home - The Next Generation.

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
    """Constants for the Counter Component."""

    ATTR_INITIAL: typing.Final = "initial"
    ATTR_STEP: typing.Final = "step"
    ATTR_MINIMUM: typing.Final = "minimum"
    ATTR_MAXIMUM: typing.Final = "maximum"
    VALUE: typing.Final = "value"

    CONF_INITIAL: typing.Final = "initial"
    CONF_RESTORE: typing.Final = "restore"
    CONF_STEP: typing.Final = "step"

    DEFAULT_INITIAL: typing.Final = 0
    DEFAULT_STEP: typing.Final = 1

    ENTITY_ID_FORMAT: typing.Final = "{}.{}"

    SERVICE_DECREMENT: typing.Final = "decrement"
    SERVICE_INCREMENT: typing.Final = "increment"
    SERVICE_RESET: typing.Final = "reset"
    SERVICE_CONFIGURE: typing.Final = "configure"

    CREATE_FIELDS: typing.Final = {
        vol.Optional(core.Const.CONF_ICON): _cv.icon,
        vol.Optional(CONF_INITIAL, default=DEFAULT_INITIAL): _cv.positive_int,
        vol.Required(core.Const.CONF_NAME): vol.All(_cv.string, vol.Length(min=1)),
        vol.Optional(core.Const.CONF_MAXIMUM, default=None): vol.Any(
            None, vol.Coerce(int)
        ),
        vol.Optional(core.Const.CONF_MINIMUM, default=None): vol.Any(
            None, vol.Coerce(int)
        ),
        vol.Optional(CONF_RESTORE, default=True): _cv.boolean,
        vol.Optional(CONF_STEP, default=DEFAULT_STEP): _cv.positive_int,
    }

    UPDATE_FIELDS: typing.Final = {
        vol.Optional(core.Const.CONF_ICON): _cv.icon,
        vol.Optional(CONF_INITIAL): _cv.positive_int,
        vol.Optional(core.Const.CONF_NAME): _cv.string,
        vol.Optional(core.Const.CONF_MAXIMUM): vol.Any(None, vol.Coerce(int)),
        vol.Optional(core.Const.CONF_MINIMUM): vol.Any(None, vol.Coerce(int)),
        vol.Optional(CONF_RESTORE): _cv.boolean,
        vol.Optional(CONF_STEP): _cv.positive_int,
    }
