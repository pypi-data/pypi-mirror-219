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

import logging
import typing

import aiohue

from .... import core
from ..const import Const
from .generic_hue_device import GenericHueDevice

_EVENT_NAME_FORMAT: typing.Final = "{}"
_CONF_LAST_UPDATED: typing.Final = "last_updated"
_LOGGER: typing.Final = logging.getLogger(__name__)


# pylint: disable=unused-variable
class HueEvent(GenericHueDevice):
    """When you want signals instead of entities.

    Stateless sensors such as remotes are expected to generate an event
    instead of a sensor entity in hass.
    """

    def __init__(
        self,
        owner: core.SmartHomeControllerComponent,
        sensor,
        name,
        bridge,
        primary_sensor=None,
    ):
        """Register callback that will be used for signals."""
        super().__init__(owner, sensor, name, bridge, primary_sensor)
        self._device_registry_id = None

        self._event_id = core.helpers.slugify(sensor.name)
        # Use the aiohue sensor 'state' dict to detect new remote presses
        self._last_state = dict(sensor.state)

        # Register callback in coordinator and add job to remove it on bridge reset.
        self._bridge.reset_jobs.append(
            self._bridge.sensor_manager.coordinator.async_add_listener(
                self.async_update_callback
            )
        )

    @core.callback
    def async_update_callback(self):
        """Fire the event if reason is that state is updated."""
        if (
            self._sensor.state == self._last_state
            # Filter out non-button events if last event type is available
            or (
                self._sensor.last_event is not None
                and self._sensor.last_event["type"] != aiohue.v1.sensors.EVENT_BUTTON
            )
        ):
            return

        # Filter out old states. Can happen when events fire while refreshing
        now_updated = core.helpers.parse_datetime(self._sensor.state["lastupdated"])
        last_updated = core.helpers.parse_datetime(self._last_state["lastupdated"])

        if (
            now_updated is not None
            and last_updated is not None
            and now_updated <= last_updated
        ):
            return

        # Extract the press code as state
        if hasattr(self._sensor, "rotaryevent"):
            state = self._sensor.rotaryevent
        else:
            state = self._sensor.buttonevent

        self._last_state = dict(self._sensor.state)

        # Fire event
        data = {
            core.Const.CONF_ID: self._event_id,
            core.Const.CONF_DEVICE_ID: self._device_registry_id,
            core.Const.CONF_UNIQUE_ID: self.unique_id,
            core.Const.CONF_EVENT: state,
            _CONF_LAST_UPDATED: self._sensor.lastupdated,
        }
        self._bridge.controller.bus.async_fire(Const.ATTR_HUE_EVENT, data)

    async def async_update_device_registry(self):
        """Update device registry."""
        device_registry = self._owner.controller.device_registry

        entry = device_registry.async_get_or_create(
            config_entry_id=self._bridge.config_entry.entry_id, **self.device_info
        )
        self._device_registry_id = entry.id
        _LOGGER.debug(
            f"Event registry with entry_id: {self._device_registry_id} and device_id: "
            + f"{self.device_id}",
            self._device_registry_id,
            self.device_id,
        )


EVENT_CONFIG_MAP: typing.Final = {
    aiohue.v1.sensors.TYPE_ZGP_SWITCH: {
        "name_format": _EVENT_NAME_FORMAT,
        "class": HueEvent,
    },
    aiohue.v1.sensors.TYPE_ZLL_SWITCH: {
        "name_format": _EVENT_NAME_FORMAT,
        "class": HueEvent,
    },
    aiohue.v1.sensors.TYPE_ZLL_ROTARY: {
        "name_format": _EVENT_NAME_FORMAT,
        "class": HueEvent,
    },
}
