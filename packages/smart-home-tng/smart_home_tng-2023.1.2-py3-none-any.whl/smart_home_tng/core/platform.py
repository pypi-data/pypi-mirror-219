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

import enum

from ..backports import strenum


# pylint: disable=unused-variable
class Platform(strenum.LowercaseStrEnum):
    """Available entity platforms."""

    APPLICATION_CREDENTIALS = enum.auto()
    """Get ApplicationCredentials instance."""
    CONFIG_FLOW = enum.auto()
    """Get ConfigFlow instance."""
    TRIGGER = enum.auto()
    """Get TriggerProtocol instance"""
    ACTION = enum.auto()
    """Get ActionProtocol instance."""
    CONDITION = enum.auto()
    """Get ActionConditionProtocol instance."""

    ALERT = enum.auto()
    AUTOMATION = enum.auto()
    BACKUP = enum.auto()
    COUNTER = enum.auto()
    DIAGNOSTICS = enum.auto()
    DISCOVERY = enum.auto()
    ENERGY = enum.auto()
    GROUP = enum.auto()
    SMART_HOME_CONTROLLER = "homeassistant"
    INTENT = enum.auto()
    INPUT_BOOLEAN = enum.auto()
    INPUT_BUTTON = enum.auto()
    INPUT_DATETIME = enum.auto()
    INPUT_SELECT = enum.auto()
    INPUT_TEXT = enum.auto()
    INPUT_NUMBER = enum.auto()
    LOGBOOK = enum.auto()
    MEDIA_SOURCE = enum.auto()
    PERSON = enum.auto()
    RECORDER = enum.auto()
    REPRODUCE_STATE = enum.auto()
    SCRIPT = enum.auto()
    SIGNIFICANT_CHANGE = enum.auto()
    SYSTEM_HEALTH = enum.auto()
    TIMER = enum.auto()
    WEBHOOK = enum.auto()
    ZONE = enum.auto()

    AIR_QUALITY = enum.auto()
    ALARM_CONTROL_PANEL = enum.auto()
    BINARY_SENSOR = enum.auto()
    BLUEPRINT = enum.auto()
    BUTTON = enum.auto()
    CALENDAR = enum.auto()
    CAMERA = enum.auto()
    CLIMATE = enum.auto()
    COVER = enum.auto()
    DEVICE_TRACKER = enum.auto()
    FAN = enum.auto()
    GEO_LOCATION = enum.auto()
    HUMIDIFIER = enum.auto()
    IMAGE_PROCESSING = enum.auto()
    LIGHT = enum.auto()
    LOCK = enum.auto()
    MAILBOX = enum.auto()
    MEDIA_PLAYER = enum.auto()
    NOTIFY = enum.auto()
    NUMBER = enum.auto()
    REMOTE = enum.auto()
    SCENE = enum.auto()
    SELECT = enum.auto()
    SENSOR = enum.auto()
    SIREN = enum.auto()
    STT = enum.auto()
    SWITCH = enum.auto()
    TTS = enum.auto()
    VACUUM = enum.auto()
    UPDATE = enum.auto()
    WATER_HEATER = enum.auto()
    WEATHER = enum.auto()
