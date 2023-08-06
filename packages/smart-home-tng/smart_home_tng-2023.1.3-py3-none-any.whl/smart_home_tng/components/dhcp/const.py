"""
DHCP Component for Smart Home - The Next Generation.

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

import datetime
import typing


# pylint: disable=unused-variable
class Const:
    """Constants for DHCP Component."""

    FILTER: typing.Final = "udp and (port 67 or 68)"
    REQUESTED_ADDR: typing.Final = "requested_addr"
    MESSAGE_TYPE: typing.Final = "message-type"
    HOSTNAME: typing.Final = "hostname"
    MAC_ADDRESS: typing.Final = "macaddress"
    IP_ADDRESS: typing.Final = "ip"
    REGISTERED_DEVICES: typing.Final = "registered_devices"
    DHCP_REQUEST: typing.Final = 3
    SCAN_INTERVAL: typing.Final = datetime.timedelta(minutes=60)
    CONNECTED_DEVICE_REGISTERED: typing.Final = (
        "device_tracker.connected_device_registered"
    )
