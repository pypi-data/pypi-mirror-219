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
from .hm_device import HMDevice

_SENSOR_TYPES_CLASS: typing.Final = {
    "IPShutterContact": core.BinarySensor.DeviceClass.OPENING,
    "IPShutterContactSabotage": core.BinarySensor.DeviceClass.OPENING,
    "MaxShutterContact": core.BinarySensor.DeviceClass.OPENING,
    "Motion": core.BinarySensor.DeviceClass.MOTION,
    "MotionV2": core.BinarySensor.DeviceClass.MOTION,
    "PresenceIP": core.BinarySensor.DeviceClass.MOTION,
    "Remote": None,
    "RemoteMotion": None,
    "ShutterContact": core.BinarySensor.DeviceClass.OPENING,
    "Smoke": core.BinarySensor.DeviceClass.SMOKE,
    "SmokeV2": core.BinarySensor.DeviceClass.SMOKE,
    "TiltSensor": None,
    "WeatherSensor": None,
    "IPContact": core.BinarySensor.DeviceClass.OPENING,
    "MotionIP": core.BinarySensor.DeviceClass.MOTION,
    "MotionIPV2": core.BinarySensor.DeviceClass.MOTION,
    "MotionIPContactSabotage": core.BinarySensor.DeviceClass.MOTION,
    "IPRemoteMotionV2": core.BinarySensor.DeviceClass.MOTION,
    "RotaryHandleSensor": core.BinarySensor.DeviceClass.WINDOW,
    "RotaryHandleSensorIP": core.BinarySensor.DeviceClass.WINDOW,
}


# pylint: disable=unused-variable
class HMBinarySensor(HMDevice, core.BinarySensor.Entity):
    """Representation of a binary HomeMatic device."""

    @property
    def is_on(self):
        """Return true if switch is on."""
        if not self.available:
            return False
        return bool(self._hm_get_state())

    @property
    def device_class(self):
        """Return the class of this sensor from DEVICE_CLASSES."""
        # If state is MOTION (Only RemoteMotion working)
        if self._state == "MOTION":
            return str(core.BinarySensor.DeviceClass.MOTION)
        return str(_SENSOR_TYPES_CLASS.get(self._hmdevice.__class__.__name__))

    def _init_data_struct(self):
        """Generate the data dictionary (self._data) from metadata."""
        # Add state to data struct
        if self._state:
            self._data.update({self._state: None})
