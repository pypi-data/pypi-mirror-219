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
from .generic_hue_gauge_sensor import GenericHueGaugeSensor

# pylint: disable=unused-variable

_LIGHT_LEVEL_NAME_FORMAT: typing.Final = "{} light level"


class HueLightLevel(GenericHueGaugeSensor):
    """The light level sensor entity for a Hue motion sensor device."""

    _attr_device_class = core.Sensor.DeviceClass.ILLUMINANCE
    _attr_native_unit_of_measurement = core.Const.LIGHT_LUX

    @property
    def native_value(self):
        """Return the state of the device."""
        if self._sensor.lightlevel is None:
            return None

        # https://developers.meethue.com/develop/hue-api/supported-devices/#clip_zll_lightlevel
        # Light level in 10000 log10 (lux) +1 measured by sensor. Logarithm
        # scale used because the human eye adjusts to light levels and small
        # changes at low lux levels are more noticeable than at high lux
        # levels.
        return round(float(10 ** ((self._sensor.lightlevel - 1) / 10000)), 2)

    @property
    def extra_state_attributes(self):
        """Return the device state attributes."""
        attributes = super().extra_state_attributes
        attributes.update(
            {
                "lightlevel": self._sensor.lightlevel,
                "daylight": self._sensor.daylight,
                "dark": self._sensor.dark,
                "threshold_dark": self._sensor.tholddark,
                "threshold_offset": self._sensor.tholdoffset,
            }
        )
        return attributes
