"""
AVM FRITZ!SmartHome Integration for Smart Home - The Next Generation.

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

import logging
import typing

from ... import core


# pylint: disable=unused-variable
class Const:
    """Constants for the AVM FRITZ!SmartHome integration."""

    ATTR_STATE_BATTERY_LOW: typing.Final = "battery_low"
    ATTR_STATE_HOLIDAY_MODE: typing.Final = "holiday_mode"
    ATTR_STATE_SUMMER_MODE: typing.Final = "summer_mode"
    ATTR_STATE_WINDOW_OPEN: typing.Final = "window_open"

    COLOR_MODE: typing.Final = "1"
    COLOR_TEMP_MODE: typing.Final = "4"

    CONF_CONNECTIONS: typing.Final = "connections"
    CONF_COORDINATOR: typing.Final = "coordinator"

    DEFAULT_HOST: typing.Final = "fritz.box"
    DEFAULT_USERNAME: typing.Final = "admin"

    LOGGER: typing.Final[logging.Logger] = logging.getLogger(__package__)

    PLATFORMS: typing.Final[list[core.Platform]] = [
        core.Platform.BINARY_SENSOR,
        core.Platform.CLIMATE,
        core.Platform.COVER,
        core.Platform.LIGHT,
        core.Platform.SENSOR,
        core.Platform.SWITCH,
    ]
