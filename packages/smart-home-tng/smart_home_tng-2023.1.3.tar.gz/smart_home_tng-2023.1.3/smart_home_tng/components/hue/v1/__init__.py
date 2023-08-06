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

# pylint: disable=unused-variable

import typing

import aiohue

from .hue_battery import _BATTERY_NAME_FORMAT, HueBattery
from .hue_light_level import _LIGHT_LEVEL_NAME_FORMAT, HueLightLevel
from .hue_presence import async_setup_binary_sensors
from .hue_temperature import _TEMPERATURE_NAME_FORMAT, HueTemperature
from .sensor_manager import _SENSOR_CONFIG_MAP, SensorManager

if not typing.TYPE_CHECKING:

    class HueBridge:
        pass


if typing.TYPE_CHECKING:
    from ..hue_bridge import HueBridge


async def async_setup_sensors(bridge: HueBridge, async_add_entities):
    """Defer sensor setup to the shared sensor module."""
    if not bridge.sensor_manager:
        return

    await bridge.sensor_manager.async_register_component("sensor", async_add_entities)


_SENSOR_CONFIG_MAP.update(
    {
        aiohue.v1.sensors.TYPE_ZLL_LIGHTLEVEL: {
            "platform": "sensor",
            "name_format": _LIGHT_LEVEL_NAME_FORMAT,
            "class": HueLightLevel,
        },
        aiohue.v1.sensors.TYPE_ZLL_TEMPERATURE: {
            "platform": "sensor",
            "name_format": _TEMPERATURE_NAME_FORMAT,
            "class": HueTemperature,
        },
        aiohue.v1.sensors.TYPE_ZLL_SWITCH: {
            "platform": "sensor",
            "name_format": _BATTERY_NAME_FORMAT,
            "class": HueBattery,
        },
        aiohue.v1.sensors.TYPE_ZLL_ROTARY: {
            "platform": "sensor",
            "name_format": _BATTERY_NAME_FORMAT,
            "class": HueBattery,
        },
    }
)
