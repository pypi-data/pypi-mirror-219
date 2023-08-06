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
class Timer:
    """ "Constants for the Timer Component."""

    DEFAULT_DURATION: typing.Final = 0
    DEFAULT_RESTORE: typing.Final = False

    ATTR_DURATION: typing.Final = "duration"
    ATTR_REMAINING: typing.Final = "remaining"
    ATTR_FINISHES_AT: typing.Final = "finishes_at"
    ATTR_RESTORE: typing.Final = "restore"
    ATTR_FINISHED_AT: typing.Final = "finished_at"

    CONF_DURATION: typing.Final = "duration"
    CONF_RESTORE: typing.Final = "restore"

    STATUS_IDLE: typing.Final = "idle"
    STATUS_ACTIVE: typing.Final = "active"
    STATUS_PAUSED: typing.Final = "paused"

    EVENT_TIMER_FINISHED: typing.Final = "timer.finished"
    EVENT_TIMER_CANCELLED: typing.Final = "timer.cancelled"
    EVENT_TIMER_STARTED: typing.Final = "timer.started"
    EVENT_TIMER_RESTARTED: typing.Final = "timer.restarted"
    EVENT_TIMER_PAUSED: typing.Final = "timer.paused"

    SERVICE_START: typing.Final = "start"
    SERVICE_PAUSE: typing.Final = "pause"
    SERVICE_CANCEL: typing.Final = "cancel"
    SERVICE_FINISH: typing.Final = "finish"

    CREATE_FIELDS: typing.Final = {
        vol.Required(Const.CONF_NAME): _cv.string,
        vol.Optional(Const.CONF_ICON): _cv.icon,
        vol.Optional(CONF_DURATION, default=DEFAULT_DURATION): _cv.time_period,
        vol.Optional(CONF_RESTORE, default=DEFAULT_RESTORE): _cv.boolean,
    }
    UPDATE_FIELDS: typing.Final = {
        vol.Optional(Const.CONF_NAME): _cv.string,
        vol.Optional(Const.CONF_ICON): _cv.icon,
        vol.Optional(CONF_DURATION): _cv.time_period,
        vol.Optional(CONF_RESTORE): _cv.boolean,
    }

    RELOAD_SERVICE_SCHEMA: typing.Final = vol.Schema({})
