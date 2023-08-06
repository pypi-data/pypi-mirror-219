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

from aiohue.v2.models.entertainment_configuration import EntertainmentStatus

from .... import core
from .hue_binary_sensor_base import HueBinarySensorBase


# pylint: disable=unused-variable
class HueEntertainmentActiveSensor(HueBinarySensorBase):
    """Representation of a Hue Entertainment Configuration as binary sensor."""

    _attr_device_class = core.BinarySensor.DeviceClass.RUNNING

    @property
    def is_on(self) -> bool | None:
        """Return true if the binary sensor is on."""
        return self.resource.status == EntertainmentStatus.ACTIVE

    @property
    def name(self) -> str:
        """Return sensor name."""
        type_title = self.resource.type.value.replace("_", " ").title()
        return f"{self.resource.metadata.name}: {type_title}"
