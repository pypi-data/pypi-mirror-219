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

from .smart_home_controller_component import SmartHomeControllerComponent
from .system_health_registration import SystemHealthRegistration


# pylint: disable=unused-variable
class SystemHealthComponent(SmartHomeControllerComponent):
    """Required base class for the System Healt Component."""

    @abc.abstractmethod
    def register_info(self, info: SystemHealthRegistration) -> None:
        """Register a info callback"""

    @abc.abstractmethod
    async def async_check_can_reach_url(self, url: str, more_info: str = None) -> str:
        """Test if the url can be reached."""
