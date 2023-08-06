"""
Energy Component for Smart Home - The Next Generation.

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

from ... import core
from .energy_manager import EnergyManager
from .sensor_manager import SensorManager


# pylint: disable=unused-variable
class SensorPlatform(core.PlatformImplementation):
    """Implementation of the Sensor Platform."""

    def __init__(self, shc: core.SmartHomeController, manager: EnergyManager) -> None:
        super().__init__()
        self._shc = shc
        self._manager = manager

    async def async_setup_platform(
        self,
        platform_config: core.ConfigType,
        add_entities: core.AddEntitiesCallback,
        discovery_info: core.DiscoveryInfoType,
    ):
        """Set up the energy sensors."""
        sensor_manager = SensorManager(self._manager, add_entities)
        await sensor_manager.async_start()
