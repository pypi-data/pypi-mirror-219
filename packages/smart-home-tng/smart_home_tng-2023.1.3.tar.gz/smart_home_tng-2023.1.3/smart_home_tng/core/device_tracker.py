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

import datetime as dt
import enum
import typing

from ..backports import strenum


# pylint: disable=unused-variable
class DeviceTracker:
    """Device Tracker namespace."""

    CONF_SCAN_INTERVAL: typing.Final = "interval_seconds"
    SCAN_INTERVAL: typing.Final = dt.timedelta(seconds=12)

    CONF_TRACK_NEW: typing.Final = "track_new_devices"
    DEFAULT_TRACK_NEW: typing.Final = True

    CONF_CONSIDER_HOME: typing.Final = "consider_home"
    DEFAULT_CONSIDER_HOME: typing.Final = dt.timedelta(seconds=180)

    CONF_NEW_DEVICE_DEFAULTS: typing.Final = "new_device_defaults"

    ATTR_ATTRIBUTES: typing.Final = "attributes"
    ATTR_BATTERY: typing.Final = "battery"
    ATTR_DEV_ID: typing.Final = "dev_id"
    ATTR_CONSIDER_HOME: typing.Final = "consider_home"
    ATTR_GPS: typing.Final = "gps"
    ATTR_HOST_NAME: typing.Final = "host_name"
    ATTR_LOCATION_NAME: typing.Final = "location_name"
    ATTR_MAC: typing.Final = "mac"
    ATTR_SOURCE_TYPE: typing.Final = "source_type"
    ATTR_IP: typing.Final = "ip"

    CONNECTED_DEVICE_REGISTERED: typing.Final = (
        "device_tracker.connected_device_registered"
    )

    PLATFORM_TYPE_LEGACY: typing.Final = "legacy"
    PLATFORM_TYPE_ENTITY: typing.Final = "entity_platform"

    class SourceType(strenum.LowercaseStrEnum):
        """Source type for device trackers."""

        GPS = enum.auto()
        ROUTER = enum.auto()
        BLUETOOTH = enum.auto()
        BLUETOOTH_LE = enum.auto()
