"""
System Log Component for Smart Home - The Next Generation.

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
    """Constants for the System Log Component."""

    CONF_MAX_ENTRIES: typing.Final = "max_entries"
    CONF_FIRE_EVENT: typing.Final = "fire_event"
    CONF_MESSAGE: typing.Final = "message"
    CONF_LEVEL: typing.Final = "level"
    CONF_LOGGER: typing.Final = "logger"

    DEFAULT_MAX_ENTRIES: typing.Final = 50
    DEFAULT_FIRE_EVENT: typing.Final = False

    EVENT_SYSTEM_LOG: typing.Final = "system_log_event"

    SERVICE_CLEAR: typing.Final = "clear"
    SERVICE_WRITE: typing.Final = "write"

    SERVICE_CLEAR_SCHEMA: typing.Final = vol.Schema({})
    SERVICE_WRITE_SCHEMA: typing.Final = vol.Schema(
        {
            vol.Required(CONF_MESSAGE): _cv.string,
            vol.Optional(CONF_LEVEL, default="error"): vol.In(
                ["debug", "info", "warning", "error", "critical"]
            ),
            vol.Optional(CONF_LOGGER): _cv.string,
        }
    )
