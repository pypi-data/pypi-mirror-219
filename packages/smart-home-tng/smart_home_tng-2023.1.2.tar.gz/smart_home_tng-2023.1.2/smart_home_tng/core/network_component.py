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

import abc
import ipaddress
import typing

from .adapter import Adapter
from .smart_home_controller_component import SmartHomeControllerComponent


# pylint: disable=unused-variable
class NetworkComponent(SmartHomeControllerComponent):
    """Required base class for the Network Component."""

    _UNDEFINED: typing.Final = object()

    @abc.abstractmethod
    async def async_get_enabled_source_ips(
        self,
    ) -> list[ipaddress.IPv4Address | ipaddress.IPv6Address]:
        """Build the list of enabled source ips."""

    @abc.abstractmethod
    async def async_get_adapters(self) -> list[Adapter]:
        """Get the network adapter configuration."""

    @abc.abstractmethod
    def async_only_default_interface_enabled(self, adapters: list[Adapter]) -> bool:
        """Check to see if any non-default adapter is enabled."""

    @abc.abstractmethod
    async def async_get_source_ip(self, target_ip: str | object = _UNDEFINED) -> str:
        """Get the source ip for a target ip."""
