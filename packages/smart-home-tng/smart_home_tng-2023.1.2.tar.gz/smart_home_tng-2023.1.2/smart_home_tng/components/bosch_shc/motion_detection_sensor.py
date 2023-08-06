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

import datetime as dt
import logging
import typing

from ... import core
from .bosch_entity import BoschEntity
from .const import Const

if not typing.TYPE_CHECKING:

    class BoschShcIntegration:
        pass


if typing.TYPE_CHECKING:
    from .bosch_shc_integration import BoschShcIntegration

_LOGGER: typing.Final = logging.getLogger(__name__)


# pylint: disable=unused-variable
class MotionDetectionSensor(BoschEntity, core.BinarySensor.Entity):
    """Representation of a SHC motion detection sensor."""

    _attr_device_class = core.BinarySensor.DeviceClass.MOTION

    def __init__(
        self, owner: BoschShcIntegration, device, parent_id: str, entry_id: str
    ):
        """Initialize the motion detection device."""
        self._service = None
        super().__init__(owner, device=device, parent_id=parent_id, entry_id=entry_id)

        for service in self._device.device_services:
            if service.id == "LatestMotion":
                self._service = service
                self._service.subscribe_callback(
                    self._device.id + "_eventlistener", self._async_input_events_handler
                )

        self._owner.controller.bus.async_listen_once(
            core.Const.EVENT_SHC_STOP, self._handle_shc_stop
        )

    @core.callback
    def _async_input_events_handler(self):
        """Handle device input events."""
        self._owner.controller.bus.async_fire(
            Const.EVENT_BOSCH_SHC,
            {
                core.Const.ATTR_DEVICE_ID: self._owner.controller.run_coroutine_threadsafe(
                    self._owner.async_get_device_id(self._device.id)
                ).result(),
                core.Const.ATTR_ID: self._device.id,
                core.Const.ATTR_NAME: self._device.name,
                Const.ATTR_LAST_TIME_TRIGGERED: self._device.latestmotion,
                Const.ATTR_EVENT_TYPE: "MOTION",
                Const.ATTR_EVENT_SUBTYPE: "",
            },
        )

    @core.callback
    def _handle_shc_stop(self, _):
        """Handle Home Assistant stopping."""
        _LOGGER.debug(
            f"Stopping motion detection event listener for {self._device.name}"
        )
        self._service.unsubscribe_callback(self._device.id + "_eventlistener")

    @property
    def is_on(self):
        """Return the state of the sensor."""
        try:
            latestmotion = dt.datetime.strptime(
                self._device.latestmotion, "%Y-%m-%dT%H:%M:%S.%fZ"
            )
        except ValueError:
            return False

        elapsed = core.helpers.utcnow() - latestmotion
        if elapsed > dt.timedelta(seconds=4 * 60):
            return False
        return True

    @property
    def should_poll(self):
        """Retrieve motion state."""
        return True

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        return {
            "last_motion_detected": self._device.latestmotion,
        }
