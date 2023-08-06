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
from ..const import Const

if not typing.TYPE_CHECKING:

    class HueBridge:
        pass


if typing.TYPE_CHECKING:
    from ..hue_bridge import HueBridge


# pylint: disable=unused-variable
class GenericHueDevice(core.Entity):
    """Representation of a Hue device."""

    def __init__(
        self,
        owner: core.SmartHomeControllerComponent,
        sensor,
        name: str,
        bridge: HueBridge,
        primary_sensor=None,
    ):
        """Initialize the sensor."""
        self._owner = owner
        self._sensor = sensor
        self._name = name
        self._primary_sensor = primary_sensor
        self._bridge = bridge
        self._allow_unreachable = bridge.config_entry.options.get(
            Const.CONF_ALLOW_UNREACHABLE, Const.DEFAULT_ALLOW_UNREACHABLE
        )

    @property
    def primary_sensor(self):
        """Return the primary sensor entity of the physical device."""
        return self._primary_sensor or self._sensor

    @property
    def device_id(self):
        """Return the ID of the physical device this sensor is part of."""
        return self.unique_id[:23]

    @property
    def unique_id(self):
        """Return the ID of this Hue sensor."""
        return self._sensor.uniqueid

    @property
    def name(self):
        """Return a friendly name for the sensor."""
        return self._name

    @property
    def swupdatestate(self):
        """Return detail of available software updates for this device."""
        return self.primary_sensor.raw.get("swupdate", {}).get("state")

    @property
    def device_info(self) -> core.DeviceInfo:
        """Return the device info.

        Links individual entities together in the hass device registry.
        """
        return core.DeviceInfo(
            identifiers={(self._owner.domain, self.device_id)},
            manufacturer=self.primary_sensor.manufacturername,
            model=(self.primary_sensor.productname or self.primary_sensor.modelid),
            name=self.primary_sensor.name,
            sw_version=self.primary_sensor.swversion,
            via_device=(self._owner.domain, self._bridge.api.config.bridgeid),
        )
