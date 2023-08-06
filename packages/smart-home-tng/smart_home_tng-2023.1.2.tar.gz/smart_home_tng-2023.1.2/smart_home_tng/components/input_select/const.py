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

_cv: typing.TypeAlias = core.ConfigValidation


def _unique(options: typing.Any) -> typing.Any:
    try:
        return vol.Unique()(options)
    except vol.Invalid as exc:
        raise core.SmartHomeControllerError(
            "Duplicate options are not allowed"
        ) from exc


# pylint: disable=unused-variable
class Const:
    """Constants for the Input Select Component."""

    CONF_INITIAL: typing.Final = "initial"
    CONF_OPTIONS: typing.Final = "options"

    ATTR_CYCLE: typing.Final = "cycle"

    SERVICE_SELECT_OPTION: typing.Final = core.Select.SERVICE_SELECT_OPTION
    SERVICE_SELECT_NEXT: typing.Final = "select_next"
    SERVICE_SELECT_PREVIOUS: typing.Final = "select_previous"
    SERVICE_SELECT_FIRST: typing.Final = "select_first"
    SERVICE_SELECT_LAST: typing.Final = "select_last"
    SERVICE_SET_OPTIONS: typing.Final = "set_options"

    CREATE_FIELDS: typing.Final = {
        vol.Required(core.Const.CONF_NAME): vol.All(str, vol.Length(min=1)),
        vol.Required(CONF_OPTIONS): vol.All(
            _cv.ensure_list, vol.Length(min=1), _unique, [_cv.string]
        ),
        vol.Optional(CONF_INITIAL): _cv.string,
        vol.Optional(core.Const.CONF_ICON): _cv.icon,
    }
    UPDATE_FIELDS: typing.Final = {
        vol.Optional(core.Const.CONF_NAME): _cv.string,
        vol.Optional(CONF_OPTIONS): vol.All(
            _cv.ensure_list, vol.Length(min=1), _unique, [_cv.string]
        ),
        vol.Optional(CONF_INITIAL): _cv.string,
        vol.Optional(core.Const.CONF_ICON): _cv.icon,
    }

    RELOAD_SERVICE_SCHEMA: typing.Final = vol.Schema({})

    STORAGE_VERSION_MINOR: typing.Final = 2
