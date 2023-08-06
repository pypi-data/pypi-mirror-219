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
class ConfigEntrySource(strenum.LowercaseStrEnum):
    """Source of the Config Entry."""

    DHCP = enum.auto()
    DISCOVERY = enum.auto()
    # SOURCE_HASSIO = "hassio"
    HOMEKIT = enum.auto()
    IMPORT = enum.auto()
    INTEGRATION_DISCOVERY = enum.auto()
    MQTT = enum.auto()
    SSDP = enum.auto()
    USB = enum.auto()
    USER = enum.auto()
    ZEROCONF = enum.auto()

    # If a user wants to hide a discovery from the UI they can "Ignore" it.
    # The config_entries/ignore_flow websocket command creates a config entry
    # with this source and while it exists normal discoveries with the same
    # unique id are ignored.
    IGNORE = enum.auto()

    # This is used when a user uses the "Stop Ignoring" button in the UI (the
    # config_entries/ignore_flow websocket command). It's triggered after the
    # "ignore" config entry has been removed and unloaded.
    UNIGNORE = enum.auto()

    # This is used to signal that re-authentication is required by the user.
    REAUTH = enum.auto()
