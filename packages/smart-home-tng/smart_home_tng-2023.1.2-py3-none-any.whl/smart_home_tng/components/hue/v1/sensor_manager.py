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

import datetime as dt
import logging
import typing

import aiohue
import async_timeout

from .... import core
from ..const import Const
from .helpers import remove_devices
from .hue_event import EVENT_CONFIG_MAP

if not typing.TYPE_CHECKING:

    class HueBridge:
        pass


if typing.TYPE_CHECKING:
    from ..hue_bridge import HueBridge

_LOGGER: typing.Final = logging.getLogger(__name__)
_SENSOR_CONFIG_MAP: typing.Final[dict[str, typing.Any]] = {}


# pylint: disable=unused-variable
class SensorManager:
    """Class that handles registering and updating Hue sensor entities.

    Intended to be a singleton.
    """

    SCAN_INTERVAL: typing.Final = dt.timedelta(seconds=5)

    def __init__(self, bridge: HueBridge):
        """Initialize the sensor manager."""
        self._bridge = bridge
        self._component_add_entities = {}
        self._current = {}
        self._current_events = {}

        self._enabled_platforms = ("binary_sensor", "sensor")
        self._coordinator = core.DataUpdateCoordinator(
            bridge.controller,
            _LOGGER,
            name="sensor",
            update_method=self.async_update_data,
            update_interval=self.SCAN_INTERVAL,
            request_refresh_debouncer=core.Debouncer(
                bridge.controller,
                _LOGGER,
                cooldown=Const.REQUEST_REFRESH_DELAY,
                immediate=True,
            ),
        )

    @property
    def coordinator(self) -> core.DataUpdateCoordinator:
        return self._coordinator

    async def async_update_data(self):
        """Update sensor data."""
        try:
            async with async_timeout.timeout(4):
                return await self._bridge.async_request_call(
                    self._bridge.api.sensors.update
                )
        except aiohue.Unauthorized as err:
            await self._bridge.handle_unauthorized_error()
            raise core.UpdateFailed("Unauthorized") from err
        except aiohue.AiohueException as err:
            raise core.UpdateFailed(f"Hue error: {err}") from err

    async def async_register_component(self, platform, async_add_entities):
        """Register async_add_entities methods for components."""
        self._component_add_entities[platform] = async_add_entities

        if len(self._component_add_entities) < len(self._enabled_platforms):
            _LOGGER.debug(f"Aborting start with {platform}, waiting for the rest")
            return

        # We have all components available, start the updating.
        self._bridge.reset_jobs.append(
            self._coordinator.async_add_listener(self.async_update_items)
        )
        await self._coordinator.async_refresh()

    @core.callback
    def async_update_items(self):
        """Update sensors from the bridge."""
        api: aiohue.HueBridgeV1 = self._bridge.api
        sensors = api.sensors

        if len(self._component_add_entities) < len(self._enabled_platforms):
            return

        to_add = {}
        primary_sensor_devices = {}
        current = self._current

        # Physical Hue motion sensors present as three sensors in the API: a
        # presence sensor, a temperature sensor, and a light level sensor. Of
        # these, only the presence sensor is assigned the user-friendly name
        # that the user has given to the device. Each of these sensors is
        # linked by a common device_id, which is the first twenty-three
        # characters of the unique id (then followed by a hyphen and an ID
        # specific to the individual sensor).
        #
        # To set up neat values, and assign the sensor entities to the same
        # device, we first, iterate over all the sensors and find the Hue
        # presence sensors, then iterate over all the remaining sensors -
        # finding the remaining ones that may or may not be related to the
        # presence sensors.
        for item_id in sensors:
            if sensors[item_id].type != aiohue.v1.sensors.TYPE_ZLL_PRESENCE:
                continue

            primary_sensor_devices[_device_id(sensors[item_id])] = sensors[item_id]

        # Iterate again now we have all the presence sensors, and add the
        # related sensors with nice names where appropriate.
        for item_id, sensor in sensors.items():
            uniqueid = sensor.uniqueid
            if current.get(uniqueid, self._current_events.get(uniqueid)) is not None:
                continue

            sensor_type = sensor.type

            # Check for event generator devices
            event_config = EVENT_CONFIG_MAP.get(sensor_type)
            if event_config is not None:
                base_name = sensor.name
                name = event_config["name_format"].format(base_name)
                new_event = event_config["class"](sensor, name, self._bridge)
                self._bridge.controller.async_create_task(
                    new_event.async_update_device_registry()
                )
                self._current_events[uniqueid] = new_event

            sensor_config = _SENSOR_CONFIG_MAP.get(sensor_type)
            if sensor_config is None:
                continue

            base_name = sensor.name
            primary_sensor = primary_sensor_devices.get(_device_id(sensor))
            if primary_sensor is not None:
                base_name = primary_sensor.name
            name = sensor_config["name_format"].format(base_name)

            current[uniqueid] = sensor_config["class"](
                self._bridge.owner,
                sensor,
                name,
                self._bridge,
                primary_sensor=primary_sensor,
            )

            to_add.setdefault(sensor_config["platform"], []).append(current[uniqueid])

        self._bridge.controller.async_create_task(
            remove_devices(
                self._bridge,
                [value.uniqueid for value in api.values()],
                current,
            )
        )

        for platform, value in to_add.items():
            self._component_add_entities[platform](value)


def _device_id(aiohue_sensor):
    # Work out the shared device ID, as described below
    device_id = aiohue_sensor.uniqueid
    if device_id and len(device_id) > 23:
        device_id = device_id[:23]
    return device_id
