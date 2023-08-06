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
from .state import State


# pylint: disable=unused-variable
class ZoneComponent(SmartHomeControllerComponent):
    """Required base class for the Zone Component."""

    @abc.abstractmethod
    def get_zone_from_position(
        self, latitude: float, longitude: float, radius: int = 0
    ) -> State:
        """Find the active zone for given latitude, longitude.

        This method must be run in the event loop.
        """

    @abc.abstractmethod
    def in_zone(
        self, zone: State, latitude: float, longitude: float, radius: float = 0
    ) -> bool:
        """Test if given latitude, longitude is in given zone.

        Async friendly.
        """
