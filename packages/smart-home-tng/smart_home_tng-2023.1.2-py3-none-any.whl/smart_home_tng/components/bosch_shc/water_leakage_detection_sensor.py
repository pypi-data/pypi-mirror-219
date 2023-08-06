"""
Bosch SHC Integration for Smart Home - The Next Generation.

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

import boschshcpy as bosch

from ... import core
from .bosch_entity import BoschEntity


# pylint: disable=unused-variable
class WaterLeakageDetectionSensor(BoschEntity, core.BinarySensor.Entity):
    """Representation of a SHC water leakage detector sensor."""

    _attr_device_class = core.BinarySensor.DeviceClass.MOISTURE

    @property
    def is_on(self):
        """Return the state of the sensor."""
        return (
            self._device.leakage_state
            != bosch.SHCWaterLeakageSensor.WaterLeakageSensorService.State.NO_LEAKAGE
        )

    @property
    def icon(self):
        """Return the icon of the sensor."""
        return "mdi:water-alert"

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        return {
            "push_notification_state": self._device.push_notification_state.name,
            "acoustic_signal_state": self._device.acoustic_signal_state.name,
        }
