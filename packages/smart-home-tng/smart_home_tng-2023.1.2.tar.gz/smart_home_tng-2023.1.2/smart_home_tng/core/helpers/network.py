"""
Helpers for Components of Smart Home - The Next Generation.

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

import ipaddress
import typing

import yarl

# RFC6890 - IP addresses of loopback interfaces
_LOOPBACK_NETWORKS: typing.Final = (
    ipaddress.ip_network("127.0.0.0/8"),
    ipaddress.ip_network("::1/128"),
    ipaddress.ip_network("::ffff:127.0.0.0/104"),
)

# RFC6890 - Address allocation for Private Internets
_PRIVATE_NETWORKS: typing.Final = (
    ipaddress.ip_network("fd00::/8"),
    ipaddress.ip_network("10.0.0.0/8"),
    ipaddress.ip_network("172.16.0.0/12"),
    ipaddress.ip_network("192.168.0.0/16"),
)

# RFC6890 - Link local ranges
_LINK_LOCAL_NETWORK: typing.Final = ipaddress.ip_network("169.254.0.0/16")

# pylint: disable=unused-variable


def is_loopback(address: ipaddress.IPv4Address | ipaddress.IPv6Address) -> bool:
    """Check if an address is a loopback address."""
    return any(address in network for network in _LOOPBACK_NETWORKS)


def is_private(address: ipaddress.IPv4Address | ipaddress.IPv6Address) -> bool:
    """Check if an address is a private address."""
    return any(address in network for network in _PRIVATE_NETWORKS)


def is_link_local(address: ipaddress.IPv4Address | ipaddress.IPv6Address) -> bool:
    """Check if an address is link local."""
    return address in _LINK_LOCAL_NETWORK


def is_local(address: ipaddress.IPv4Address | ipaddress.IPv6Address) -> bool:
    """Check if an address is loopback or private."""
    return is_loopback(address) or is_private(address)


def is_invalid(address: ipaddress.IPv4Address | ipaddress.IPv6Address) -> bool:
    """Check if an address is invalid."""
    return bool(address == ipaddress.ip_address("0.0.0.0"))  # nosec


def is_ip_address(address: str) -> bool:
    """Check if a given string is an IP address."""
    try:
        ipaddress.ip_address(address)
    except ValueError:
        return False

    return True


def is_ipv4_address(address: str) -> bool:
    """Check if a given string is an IPv4 address."""
    try:
        ipaddress.IPv4Address(address)
    except ValueError:
        return False

    return True


def is_ipv6_address(address: str) -> bool:
    """Check if a given string is an IPv6 address."""
    try:
        ipaddress.IPv6Address(address)
    except ValueError:
        return False

    return True


def normalize_url(address: str) -> str:
    """Normalize a given URL."""
    url = yarl.URL(address.rstrip("/"))
    if url.is_absolute() and url.is_default_port():
        return str(url.with_port(None))
    return str(url)
