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

from .async_zero_conf import AsyncZeroConf
from .smart_home_controller_component import SmartHomeControllerComponent
from .zero_conf import ZeroConf


# pylint: disable=unused-variable
class ZeroconfComponent(SmartHomeControllerComponent):
    """Required base class for Zeroconf Component."""

    @abc.abstractmethod
    async def async_get_instance(self) -> ZeroConf:
        """Zeroconf instance to be shared with other integrations that use it."""

    @abc.abstractmethod
    async def async_get_async_instance(self) -> AsyncZeroConf:
        """Zeroconf instance to be shared with other integrations that use it."""
