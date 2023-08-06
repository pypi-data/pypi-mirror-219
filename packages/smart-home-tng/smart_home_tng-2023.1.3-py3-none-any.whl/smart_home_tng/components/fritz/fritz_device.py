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

import datetime as dt

from ... import core
from .device import Device


# pylint: disable=unused-variable
class FritzDevice:
    """Representation of a device connected to the FRITZ!Box."""

    def __init__(self, mac: str, name: str) -> None:
        """Initialize device info."""
        self._connected = False
        self._connected_to: str = None
        self._connection_type: str = None
        self._ip_address: str = None
        self._last_activity: dt.datetime = None
        self._mac = mac
        self._name = name
        self._ssid: str = None
        self._wan_access: bool = False

    def update(self, dev_info: Device, consider_home: float) -> None:
        """Update device info."""
        utc_point_in_time = core.helpers.utcnow()

        if self._last_activity:
            consider_home_evaluated = (
                utc_point_in_time - self._last_activity
            ).total_seconds() < consider_home
        else:
            consider_home_evaluated = dev_info.connected

        if not self._name:
            self._name = dev_info.name or self._mac.replace(":", "_")

        self._connected = dev_info.connected or consider_home_evaluated

        if dev_info.connected:
            self._last_activity = utc_point_in_time

        self._connected_to = dev_info.connected_to
        self._connection_type = dev_info.connection_type
        self._ip_address = dev_info.ip_address
        self._ssid = dev_info.ssid
        self._wan_access = dev_info.wan_access

    @property
    def connected_to(self) -> str:
        """Return connected status."""
        return self._connected_to

    @property
    def connection_type(self) -> str:
        """Return connected status."""
        return self._connection_type

    @property
    def is_connected(self) -> bool:
        """Return connected status."""
        return self._connected

    @property
    def mac_address(self) -> str:
        """Get MAC address."""
        return self._mac

    @property
    def hostname(self) -> str:
        """Get Name."""
        return self._name

    @property
    def ip_address(self) -> str:
        """Get IP address."""
        return self._ip_address

    @property
    def last_activity(self) -> dt.datetime:
        """Return device last activity."""
        return self._last_activity

    @property
    def ssid(self) -> str:
        """Return device connected SSID."""
        return self._ssid

    @property
    def wan_access(self) -> bool:
        """Return device wan access."""
        return self._wan_access
