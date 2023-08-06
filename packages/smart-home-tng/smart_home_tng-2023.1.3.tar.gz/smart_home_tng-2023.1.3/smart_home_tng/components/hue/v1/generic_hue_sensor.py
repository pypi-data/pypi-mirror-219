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

from .... import core
from .generic_hue_device import GenericHueDevice


# pylint: disable=unused-variable
class GenericHueSensor(GenericHueDevice, core.Entity):
    """Representation of a Hue sensor."""

    _attr_should_poll = False

    @property
    def available(self):
        """Return if sensor is available."""
        return self._bridge.sensor_manager.coordinator.last_update_success and (
            self._allow_unreachable
            # remotes like Hue Tap (ZGPSwitchSensor) have no _reachability_
            or self._sensor.config.get("reachable", True)
        )

    @property
    def state_class(self):
        """Return the state class of this entity, from STATE_CLASSES, if any."""
        return core.Sensor.StateClass.MEASUREMENT

    async def async_added_to_shc(self):
        """When entity is added to hass."""
        await super().async_added_to_shc()
        self.async_on_remove(
            self._bridge.sensor_manager.coordinator.async_add_listener(
                self.async_write_state
            )
        )

    async def async_update(self):
        """Update the entity.

        Only used by the generic entity update service.
        """
        await self._bridge.sensor_manager.coordinator.async_request_refresh()
