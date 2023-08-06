"""
Homematic Integration for Smart Home - The Next Generation.

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

from ... import core
from .const import Const
from .hm_battery_sensor import HMBatterySensor
from .hm_binary_sensor import HMBinarySensor

if not typing.TYPE_CHECKING:

    class HomematicIntegration:
        pass


if typing.TYPE_CHECKING:
    from .homematic_integration import HomematicIntegration


# pylint: disable=unused-variable
async def async_setup_binary_sensors(
    comp: HomematicIntegration,
    add_entities: core.AddEntitiesCallback,
    discovery_info: core.DiscoveryInfoType = None,
) -> None:
    """Set up the HomeMatic binary sensor platform."""
    if discovery_info is None:
        return

    devices: list[core.BinarySensor.Entity] = []
    for conf in discovery_info[Const.ATTR_DISCOVER_DEVICES]:
        if discovery_info[Const.ATTR_DISCOVERY_TYPE] == Const.DISCOVER_BATTERY:
            devices.append(HMBatterySensor(comp, conf))
        else:
            devices.append(HMBinarySensor(comp, conf))

    add_entities(devices, True)
