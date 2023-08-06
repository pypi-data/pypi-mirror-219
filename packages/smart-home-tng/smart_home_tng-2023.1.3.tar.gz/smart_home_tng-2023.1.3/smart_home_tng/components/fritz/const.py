"""
AVM FRITZ!Box Tools Integration for Smart Home - The Next Generation.

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
import typing

import fritzconnection.core.exceptions as fritz_exceptions

from ... import core
from ...backports import strenum


# pylint: disable=unused-variable
class Const:
    """Constants for the FRITZ!Box Tools integration."""

    class MeshRole(strenum.LowercaseStrEnum):
        """Available Mesh roles."""

        NONE = enum.auto()
        MASTER = enum.auto()
        SLAVE = enum.auto()

    PLATFORMS: typing.Final = [
        core.Platform.BUTTON,
        core.Platform.BINARY_SENSOR,
        core.Platform.DEVICE_TRACKER,
        core.Platform.SENSOR,
        core.Platform.SWITCH,
        core.Platform.UPDATE,
    ]

    CONF_OLD_DISCOVERY: typing.Final = "old_discovery"
    DEFAULT_CONF_OLD_DISCOVERY: typing.Final = False

    DSL_CONNECTION: typing.Final = "dsl"

    DEFAULT_DEVICE_NAME: typing.Final = "Unknown device"
    DEFAULT_HOST: typing.Final = "192.168.178.1"
    DEFAULT_PORT: typing.Final = 49000
    DEFAULT_USERNAME: typing.Final = ""

    ERROR_AUTH_INVALID: typing.Final = "invalid_auth"
    ERROR_CANNOT_CONNECT: typing.Final = "cannot_connect"
    ERROR_UPNP_NOT_CONFIGURED: typing.Final = "upnp_not_configured"
    ERROR_UNKNOWN: typing.Final = "unknown_error"

    FRITZ_SERVICES: typing.Final = "fritz_services"
    SERVICE_REBOOT: typing.Final = "reboot"
    SERVICE_RECONNECT: typing.Final = "reconnect"
    SERVICE_CLEANUP: typing.Final = "cleanup"
    SERVICE_SET_GUEST_WIFI_PW: typing.Final = "set_guest_wifi_password"

    SWITCH_TYPE_DEFLECTION: typing.Final = "CallDeflection"
    SWITCH_TYPE_PORTFORWARD: typing.Final = "PortForward"
    SWITCH_TYPE_PROFILE: typing.Final = "Profile"
    SWITCH_TYPE_WIFINETWORK: typing.Final = "WiFiNetwork"

    UPTIME_DEVIATION: typing.Final = 5

    FRITZ_EXCEPTIONS: typing.Final = (
        fritz_exceptions.FritzActionError,
        fritz_exceptions.FritzActionFailedError,
        fritz_exceptions.FritzInternalError,
        fritz_exceptions.FritzServiceError,
        fritz_exceptions.FritzLookUpError,
    )

    WIFI_STANDARD: typing.Final = {
        1: "2.4 Ghz",
        2: "5 Ghz",
        3: "2.4 / 5 Ghz",
        4: "Guest",
    }
