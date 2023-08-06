"""
Amazon Alexa MediaPlayer Integration for Smart Home - The Next Generation.

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

This integration is based custom_component "alexa_media_player"
from the Home Assistant Community Store (HACS), which is distributed
under the Terms of the Apache License, Version 2.0

The original source code and license terms can be found under:
https://github.com/custom_components/alexa_media_player
"""

import datetime as dt
import typing

from ... import core

_platform: typing.TypeAlias = core.Platform


# pylint: disable=unused-variable
class Const:
    """Constants for the Alexa Media Player Integration"""

    PLAY_SCAN_INTERVAL: typing.Final = 20
    SCAN_INTERVAL: typing.Final = dt.timedelta(seconds=60)
    MIN_TIME_BETWEEN_SCANS: typing.Final = SCAN_INTERVAL
    MIN_TIME_BETWEEN_FORCED_SCANS: typing.Final = dt.timedelta(seconds=1)

    ALEXA_COMPONENTS: typing.Final = [
        _platform.MEDIA_PLAYER,
    ]
    DEPENDENT_ALEXA_COMPONENTS: typing.Final = [
        _platform.NOTIFY,
        _platform.SWITCH,
        # _platform.SENSOR,
        # _platform.ALARM_CONTROL_PANEL,
        # _platform.LIGHT,
        # _platform.BINARY_SENSOR
    ]

    HTTP_COOKIE_HEADER: typing.Final = "# HTTP Cookie File"
    CONF_ACCOUNTS: typing.Final = "accounts"
    CONF_DEBUG: typing.Final = "debug"
    CONF_CONTROLLER_URL: typing.Final = "controller_url"
    CONF_INCLUDE_DEVICES: typing.Final = "include_devices"
    CONF_EXCLUDE_DEVICES: typing.Final = "exclude_devices"
    CONF_QUEUE_DELAY: typing.Final = "queue_delay"
    CONF_EXTENDED_ENTITY_DISCOVERY: typing.Final = "extended_entity_discovery"
    CONF_SECURITYCODE: typing.Final = "securitycode"
    CONF_OTPSECRET: typing.Final = "otp_secret"
    CONF_PROXY: typing.Final = "proxy"
    CONF_PROXY_WARNING: typing.Final = "proxy_warning"
    CONF_TOTP_REGISTER: typing.Final = "registered"
    CONF_OAUTH: typing.Final = "oauth"
    DATA_LISTENER: typing.Final = "listener"

    EXCEPTION_TEMPLATE: typing.Final = (
        "An exception of type {0} occurred. Arguments:\n{1!r}"
    )

    DEFAULT_EXTENDED_ENTITY_DISCOVERY: typing.Final = False
    DEFAULT_QUEUE_DELAY: typing.Final = 1.5
    SERVICE_CLEAR_HISTORY: typing.Final = "clear_history"
    SERVICE_UPDATE_LAST_CALLED: typing.Final = "update_last_called"
    SERVICE_FORCE_LOGOUT: typing.Final = "force_logout"

    RECURRING_PATTERN: typing.Final = {
        None: "Never Repeat",
        "P1D": "Every day",
        "P1M": "Every month",
        "XXXX-WE": "Weekends",
        "XXXX-WD": "Weekdays",
        "XXXX-WXX-1": "Every Monday",
        "XXXX-WXX-2": "Every Tuesday",
        "XXXX-WXX-3": "Every Wednesday",
        "XXXX-WXX-4": "Every Thursday",
        "XXXX-WXX-5": "Every Friday",
        "XXXX-WXX-6": "Every Saturday",
        "XXXX-WXX-7": "Every Sunday",
    }

    RECURRING_DAY: typing.Final = {
        "MO": 1,
        "TU": 2,
        "WE": 3,
        "TH": 4,
        "FR": 5,
        "SA": 6,
        "SU": 7,
    }
    RECURRING_PATTERN_ISO_SET: typing.Final = {
        None: {},
        "P1D": {1, 2, 3, 4, 5, 6, 7},
        "XXXX-WE": {6, 7},
        "XXXX-WD": {1, 2, 3, 4, 5},
        "XXXX-WXX-1": {1},
        "XXXX-WXX-2": {2},
        "XXXX-WXX-3": {3},
        "XXXX-WXX-4": {4},
        "XXXX-WXX-5": {5},
        "XXXX-WXX-6": {6},
        "XXXX-WXX-7": {7},
    }

    ATTR_MESSAGE: typing.Final = "message"
    ATTR_EMAIL: typing.Final = "email"
    ATTR_NUM_ENTRIES: typing.Final = "entries"

    AUTH_CALLBACK_PATH: typing.Final = "/auth/alexamedia/callback"
    AUTH_CALLBACK_NAME: typing.Final = "auth:alexamedia:callback"
    AUTH_PROXY_PATH: typing.Final = "/auth/alexamedia/proxy"
    AUTH_PROXY_NAME: typing.Final = "auth:alexamedia:proxy"
