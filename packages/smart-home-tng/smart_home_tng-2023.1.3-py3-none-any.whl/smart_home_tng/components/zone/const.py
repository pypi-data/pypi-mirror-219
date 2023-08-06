"""
Zone Component for Smart Home - The Next Generation.

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
    """Constants for the zone component."""

    CONF_PASSIVE: typing.Final = "passive"
    HOME_ZONE: typing.Final = "home"
    ATTR_PASSIVE: typing.Final = "passive"
    ATTR_RADIUS: typing.Final = "radius"

    DEFAULT_PASSIVE: typing.Final = False
    DEFAULT_RADIUS: typing.Final = 100

    ENTITY_ID_HOME: typing.Final = f"zone.{HOME_ZONE}"

    ICON_HOME: typing.Final = "mdi:home"
    ICON_IMPORT: typing.Final = "mdi:import"

    CREATE_FIELDS: typing.Final = {
        vol.Required(core.Const.CONF_NAME): _cv.string,
        vol.Required(core.Const.CONF_LATITUDE): _cv.latitude,
        vol.Required(core.Const.CONF_LONGITUDE): _cv.longitude,
        vol.Optional(core.Const.CONF_RADIUS, default=DEFAULT_RADIUS): vol.Coerce(float),
        vol.Optional(CONF_PASSIVE, default=DEFAULT_PASSIVE): _cv.boolean,
        vol.Optional(core.Const.CONF_ICON): _cv.icon,
    }

    UPDATE_FIELDS: typing.Final = {
        vol.Optional(core.Const.CONF_NAME): _cv.string,
        vol.Optional(core.Const.CONF_LATITUDE): _cv.latitude,
        vol.Optional(core.Const.CONF_LONGITUDE): _cv.longitude,
        vol.Optional(core.Const.CONF_RADIUS): vol.Coerce(float),
        vol.Optional(CONF_PASSIVE): _cv.boolean,
        vol.Optional(core.Const.CONF_ICON): _cv.icon,
    }

    RELOAD_SERVICE_SCHEMA: typing.Final = vol.Schema({})
