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

import aiohue

from .... import core
from .generic_zll_sensor import GenericZLLSensor
from .sensor_manager import _SENSOR_CONFIG_MAP

if not typing.TYPE_CHECKING:

    class HueBridge:
        pass


if typing.TYPE_CHECKING:
    from ..hue_bridge import HueBridge

_PRESENCE_NAME_FORMAT: typing.Final = "{} motion"


# pylint: disable=unused-variable
class HuePresence(GenericZLLSensor, core.BinarySensor.Entity):
    """The presence sensor entity for a Hue motion sensor device."""

    _attr_device_class = core.BinarySensor.DeviceClass.MOTION

    @property
    def is_on(self):
        """Return true if the binary sensor is on."""
        return self._sensor.presence

    @property
    def extra_state_attributes(self):
        """Return the device state attributes."""
        attributes = super().extra_state_attributes
        if "sensitivity" in self._sensor.config:
            attributes["sensitivity"] = self._sensor.config["sensitivity"]
        if "sensitivitymax" in self._sensor.config:
            attributes["sensitivity_max"] = self._sensor.config["sensitivitymax"]
        return attributes


_SENSOR_CONFIG_MAP.update(
    {
        aiohue.v1.sensors.TYPE_ZLL_PRESENCE: {
            "platform": "binary_sensor",
            "name_format": _PRESENCE_NAME_FORMAT,
            "class": HuePresence,
        }
    }
)


async def async_setup_binary_sensors(
    bridge: HueBridge, async_add_entities: core.AddEntitiesCallback
):
    """Defer binary sensor setup to the shared sensor module."""

    if not bridge.sensor_manager:
        return

    await bridge.sensor_manager.async_register_component(
        "binary_sensor", async_add_entities
    )
