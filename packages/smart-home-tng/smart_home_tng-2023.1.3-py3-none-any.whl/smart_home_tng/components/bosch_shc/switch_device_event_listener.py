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

import logging
import typing

import boschshcpy as bosch

from ... import core
from .const import Const

_LOGGER: typing.Final = logging.getLogger(__name__)


# pylint: disable=unused-variable
class SwitchDeviceEventListener:
    """Event listener for a Switch device."""

    def __init__(
        self,
        owner: core.SmartHomeControllerComponent,
        entry: core.ConfigEntry,
        device: bosch.SHCUniversalSwitch,
    ):
        """Initialize the Switch device event listener."""
        self._owner = owner
        self._entry = entry
        self._device = device
        self._service = None
        self._device_id = None

        for service in self._device.device_services:
            if service.id == "Keypad":
                self._service = service
                self._service.subscribe_callback(
                    self._device.id, self._async_input_events_handler
                )

        owner.controller.bus.async_listen_once(
            core.Const.EVENT_SHC_STOP, self._handle_shc_stop
        )

    @core.callback
    def _async_input_events_handler(self):
        """Handle device input events."""
        event_type = self._device.eventtype.name

        if event_type in Const.SUPPORTED_INPUTS_EVENTS_TYPES:
            self._owner.controller.bus.async_fire(
                Const.EVENT_BOSCH_SHC,
                {
                    core.Const.ATTR_DEVICE_ID: self._device_id,
                    core.Const.ATTR_ID: self._device.id,
                    core.Const.ATTR_NAME: self._device.name,
                    Const.ATTR_LAST_TIME_TRIGGERED: self._device.eventtimestamp,
                    Const.ATTR_EVENT_SUBTYPE: self._device.keyname.name,
                    Const.ATTR_EVENT_TYPE: self._device.eventtype.name,
                },
            )
        else:
            _LOGGER.warning(
                f"Switch input event {event_type} for device {self._device.name} is not supported, "
                + "please open issue",
            )

    async def async_setup(self):
        """Set up the listener."""
        device_registry = self._owner.controller.device_registry
        device_entry = device_registry.async_get_or_create(
            config_entry_id=self._entry.entry_id,
            name=self._device.name,
            identifiers={(self._owner.domain, self._device.id)},
            manufacturer=self._device.manufacturer,
            model=self._device.device_model,
            via_device=(self._owner.domain, self._device.parent_device_id),
        )
        self._device_id = device_entry.id

    def shutdown(self):
        """Shutdown the listener."""
        self._service.unsubscribe_callback(self._device.id)

    @core.callback
    def _handle_shc_stop(self, _):
        """Handle Home Assistant stopping."""
        _LOGGER.debug(f"Stopping Switch event listener for {self._device.name}")
        self.shutdown()
