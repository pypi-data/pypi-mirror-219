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

# pylint: disable=unused-variable

import typing

from .battery_source_type import BatterySourceType
from .const import Const
from .device_consumption import DeviceConsumption
from .energy import Energy
from .energy_cost_sensor import EnergyCostSensor
from .energy_manager import EnergyManager
from .energy_preferences import EnergyPreferences
from .energy_preferences_update import EnergyPreferencesUpdate
from .flow_from_grid_source_type import FlowFromGridSourceType
from .flow_to_grid_source_type import FlowToGridSourceType
from .gas_source_type import GasSourceType
from .grid_source_type import GridSourceType
from .sensor_manager import SensorManager
from .solar_source_type import SolarSourceType
from .source_adapter import SourceAdapter
from .source_type import SourceType


_: typing.Final = Energy(__path__)
