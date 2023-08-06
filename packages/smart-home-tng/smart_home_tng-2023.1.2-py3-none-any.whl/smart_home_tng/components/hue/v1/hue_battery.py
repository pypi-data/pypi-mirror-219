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

Hue V1 API specific platform implementation.
"""

import typing

from .... import core
from .generic_hue_sensor import GenericHueSensor

# pylint: disable=unused-variable

_BATTERY_NAME_FORMAT: typing.Final = "{} battery level"


class HueBattery(GenericHueSensor, core.Sensor.Entity):
    """Battery class for when a batt-powered device is only represented as an event."""

    _attr_device_class = core.Sensor.DeviceClass.BATTERY
    _attr_state_class = core.Sensor.StateClass.MEASUREMENT
    _attr_native_unit_of_measurement = core.Const.PERCENTAGE
    _attr_entity_category = core.EntityCategory.DIAGNOSTIC

    @property
    def unique_id(self):
        """Return a unique identifier for this device."""
        return f"{self._sensor.uniqueid}-battery"

    @property
    def native_value(self):
        """Return the state of the battery."""
        return self._sensor.battery
