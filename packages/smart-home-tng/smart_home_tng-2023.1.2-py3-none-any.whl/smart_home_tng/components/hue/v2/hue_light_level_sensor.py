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

from .... import core
from .hue_sensor_base import HueSensorBase


# pylint: disable=unused-variable
class HueLightLevelSensor(HueSensorBase):
    """Representation of a Hue LightLevel (illuminance) sensor."""

    _attr_native_unit_of_measurement = core.Const.LIGHT_LUX
    _attr_device_class = core.Sensor.DeviceClass.ILLUMINANCE

    @property
    def native_value(self) -> int:
        """Return the value reported by the sensor."""
        # Light level in 10000 log10 (lux) +1 measured by sensor. Logarithm
        # scale used because the human eye adjusts to light levels and small
        # changes at low lux levels are more noticeable than at high lux
        # levels.
        return int(10 ** ((self.resource.light.light_level - 1) / 10000))

    @property
    def extra_state_attributes(self) -> dict[str, typing.Any]:
        """Return the optional state attributes."""
        return {
            "light_level": self.resource.light.light_level,
            "light_level_valid": self.resource.light.light_level_valid,
        }
