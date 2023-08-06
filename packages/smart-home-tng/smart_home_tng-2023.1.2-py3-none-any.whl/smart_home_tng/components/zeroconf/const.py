"""
Zeroconf Component for Smart Home - The Next Generation.

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


# pylint: disable=unused-variable
class Const:
    """Constants for the Zeroconf Component."""

    ZEROCONF_TYPE: typing.Final = "_smart-home-tng._tcp.local."
    HOMEKIT_TYPES: typing.Final = [
        "_hap._tcp.local.",
        # Thread based devices
        "_hap._udp.local.",
    ]

    # Top level keys we support matching against in properties that are always matched in
    # lower case. ex: ZeroconfServiceInfo.name
    LOWER_MATCH_ATTRS: typing.Final = {"name"}

    CONF_DEFAULT_INTERFACE: typing.Final = "default_interface"
    CONF_IPV6: typing.Final = "ipv6"
    DEFAULT_DEFAULT_INTERFACE: typing.Final = True
    DEFAULT_IPV6: typing.Final = True

    HOMEKIT_PAIRED_STATUS_FLAG: typing.Final = "sf"
    HOMEKIT_MODEL: typing.Final = "md"

    # Property key=value has a max length of 255
    # so we use 230 to leave space for key=
    MAX_PROPERTY_VALUE_LEN: typing.Final = 230

    # Dns label max length
    MAX_NAME_LEN: typing.Final = 63

    ATTR_PROPERTIES: typing.Final = "properties"

    # Attributes for ZeroconfServiceInfo[ATTR_PROPERTIES]
    ATTR_PROPERTIES_ID: typing.Final = "id"

    TYPE_AAAA: typing.Final = 28
