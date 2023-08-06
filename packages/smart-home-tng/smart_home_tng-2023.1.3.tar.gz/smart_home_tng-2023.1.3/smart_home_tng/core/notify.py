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
class Notify:
    """Notify namespace."""

    ATTR_DATA: typing.Final = Const.ATTR_DATA

    # Text to notify user of
    ATTR_MESSAGE: typing.Final = Const.ATTR_MESSAGE

    # Target of the notification (user, device, etc)
    ATTR_TARGET: typing.Final = Const.ATTR_TARGET

    # Title of notification
    ATTR_TITLE: typing.Final = Const.ATTR_TITLE

    PLATFORM_SCHEMA: typing.Final = vol.Schema(
        {
            vol.Required(Const.CONF_PLATFORM): _cv.string,
            vol.Optional(Const.CONF_NAME): _cv.string,
        },
        extra=vol.ALLOW_EXTRA,
    )
