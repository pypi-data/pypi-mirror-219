"""
Philips Hue Integration for Smart Home - The Next Generation.

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

Hue V2 API specific platform implementation.
"""

import typing

from aiohue.v2.controllers.sensors import (
    DevicePowerController,
    LightLevelController,
    TemperatureController,
    ZigbeeConnectivityController,
)
from aiohue.v2.models.device_power import DevicePower
from aiohue.v2.models.light_level import LightLevel
from aiohue.v2.models.temperature import Temperature
from aiohue.v2.models.zigbee_connectivity import ZigbeeConnectivity

from .... import core
from .hue_base_entity import HueBaseEntity

if not typing.TYPE_CHECKING:

    class HueBridge:
        pass


if typing.TYPE_CHECKING:
    from ..hue_bridge import HueBridge


SensorType: typing.TypeAlias = typing.Union[
    DevicePower, LightLevel, Temperature, ZigbeeConnectivity
]
ControllerType: typing.TypeAlias = typing.Union[
    DevicePowerController,
    LightLevelController,
    TemperatureController,
    ZigbeeConnectivityController,
]


# pylint: disable=unused-variable
class HueSensorBase(HueBaseEntity, core.Sensor.Entity):
    """Representation of a Hue sensor."""

    _attr_state_class = core.Sensor.StateClass.MEASUREMENT

    def __init__(
        self,
        bridge: HueBridge,
        controller: ControllerType,
        resource: SensorType,
    ) -> None:
        """Initialize the light."""
        super().__init__(bridge, controller, resource)

    @property
    def controller(self) -> ControllerType:
        return self._controller

    @property
    def resource(self) -> SensorType:
        return self._resource
