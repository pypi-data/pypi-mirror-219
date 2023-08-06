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

# pylint: disable=unused-variable

import logging
import typing

from aiohue import v2
from aiohue.v2.controllers.events import EventType
from aiohue.v2.controllers.sensors import SensorsController
from aiohue.v2.models import button as v2_button
from aiohue.v2.models import device as v2_device
from aiohue.v2.models import relative_rotary as v2_relative_rotary

from .... import core
from ..const import Const
from .hue_binary_sensor_base import ControllerType as BinaryControllerType
from .hue_binary_sensor_base import SensorType as BinarySensorType
from .hue_entertainment_active_sensor import HueEntertainmentActiveSensor
from .hue_motion_sensor import HueMotionSensor
from .hue_scene import async_setup_scenes
from .hue_sensor_base import ControllerType as SensorControllerType, SensorType
from .hue_battery_sensor import HueBatterySensor
from .hue_light_level_sensor import HueLightLevelSensor
from .hue_temperature_sensor import HueTemperatureSensor
from .hue_zigbee_connectivity_sensor import HueZigbeeConnectivitySensor
from .hue_sensing_service_enabled_entity import async_setup_switches

if not typing.TYPE_CHECKING:

    class HueBridge:
        pass


if typing.TYPE_CHECKING:
    from ..hue_bridge import HueBridge


_CONF_CONTROL_ID: typing.Final = "control_id"
_CONF_DURATION: typing.Final = "duration"
_CONF_STEPS: typing.Final = "steps"

_LOGGER: typing.Final = logging.getLogger(__name__)


async def async_setup_devices(bridge: HueBridge):
    """Manage setup of devices from Hue devices."""
    entry = bridge.config_entry
    shc = bridge.controller
    api: v2.HueBridgeV2 = bridge.api  # to satisfy typing
    dev_reg = shc.device_registry
    dev_controller = api.devices
    domain = bridge.owner.domain

    @core.callback
    def add_device(hue_device: v2_device.Device) -> core.Device:
        """Register a Hue device in device registry."""
        model = f"{hue_device.product_data.product_name} ({hue_device.product_data.model_id})"
        params = {
            core.Const.ATTR_IDENTIFIERS: {(domain, hue_device.id)},
            core.Const.ATTR_SW_VERSION: hue_device.product_data.software_version,
            core.Const.ATTR_NAME: hue_device.metadata.name,
            core.Const.ATTR_MODEL: model,
            core.Const.ATTR_MANUFACTURER: hue_device.product_data.manufacturer_name,
        }
        if room := dev_controller.get_room(hue_device.id):
            params[core.Const.ATTR_SUGGESTED_AREA] = room.metadata.name
        if hue_device.metadata.archetype == v2_device.DeviceArchetypes.BRIDGE_V2:
            params[core.Const.ATTR_IDENTIFIERS].add((domain, api.config.bridge_id))
        else:
            params[core.Const.ATTR_VIA_DEVICE] = (domain, api.config.bridge_device.id)
        zigbee = dev_controller.get_zigbee_connectivity(hue_device.id)
        if zigbee and zigbee.mac_address:
            params[core.Const.ATTR_CONNECTIONS] = {
                (core.DeviceRegistry.ConnectionType.MAC, zigbee.mac_address)
            }

        return dev_reg.async_get_or_create(config_entry_id=entry.entry_id, **params)

    @core.callback
    def remove_device(hue_device_id: str) -> None:
        """Remove device from registry."""
        if device := dev_reg.async_get_device({(domain, hue_device_id)}):
            # note: removal of any underlying entities is handled by core
            dev_reg.async_remove_device(device.id)

    @core.callback
    def handle_device_event(
        evt_type: v2.EventType, hue_device: v2_device.Device
    ) -> None:
        """Handle event from Hue devices controller."""
        if evt_type == v2.EventType.RESOURCE_DELETED:
            remove_device(hue_device.id)
        else:
            # updates to existing device will also be handled by this call
            add_device(hue_device)

    # create/update all current devices found in controller
    known_devices = [add_device(hue_device) for hue_device in dev_controller]

    # Check for nodes that no longer exist and remove them
    for device in dev_reg.async_entries_for_config_entry(entry.entry_id):
        if device not in known_devices:
            # handle case where a virtual device was created for a Hue group
            hue_dev_id = next(x[1] for x in device.identifiers if x[0] == domain)
            if hue_dev_id in api.groups:
                continue
            dev_reg.async_remove_device(device.id)

    # add listener for updates on Hue devices controller
    entry.async_on_unload(dev_controller.subscribe(handle_device_event))


async def async_setup_hue_events(bridge: HueBridge):
    """Manage listeners for stateless Hue sensors that emit events."""
    shc = bridge.controller
    api: v2.HueBridgeV2 = bridge.api  # to satisfy typing
    conf_entry = bridge.config_entry
    dev_reg = shc.device_registry
    domain = bridge.owner.domain

    btn_controller = api.sensors.button
    rotary_controller = api.sensors.relative_rotary

    @core.callback
    def handle_button_event(
        _evt_type: v2.EventType, hue_resource: v2_button.Button
    ) -> None:
        """Handle event from Hue button resource controller."""
        _LOGGER.debug(f"Received button event: {hue_resource}")

        # guard for missing button object on the resource
        if hue_resource.button is None:
            return

        hue_device = btn_controller.get_device(hue_resource.id)
        device = dev_reg.async_get_device({(domain, hue_device.id)})

        # Fire event
        data = {
            # send slugified entity name as id = backwards compatibility with previous version
            core.Const.CONF_ID: core.helpers.slugify(
                f"{hue_device.metadata.name} Button"
            ),
            core.Const.CONF_DEVICE_ID: device.id,
            core.Const.CONF_UNIQUE_ID: hue_resource.id,
            core.Const.CONF_TYPE: hue_resource.button.last_event.value,
            Const.CONF_SUBTYPE: hue_resource.metadata.control_id,
        }
        shc.bus.async_fire(Const.ATTR_HUE_EVENT, data)

    # add listener for updates from `button` resource
    conf_entry.async_on_unload(
        btn_controller.subscribe(
            handle_button_event, event_filter=v2.EventType.RESOURCE_UPDATED
        )
    )

    @core.callback
    def handle_rotary_event(
        _evt_type: v2.EventType, hue_resource: v2_relative_rotary.RelativeRotary
    ) -> None:
        """Handle event from Hue relative_rotary resource controller."""
        _LOGGER.debug(f"Received relative_rotary event: {hue_resource}")

        hue_device = btn_controller.get_device(hue_resource.id)
        device = dev_reg.async_get_device({(domain, hue_device.id)})

        # Fire event
        data = {
            core.Const.CONF_DEVICE_ID: device.id,
            core.Const.CONF_UNIQUE_ID: hue_resource.id,
            core.Const.CONF_TYPE: hue_resource.relative_rotary.last_event.action.value,
            Const.CONF_SUBTYPE: hue_resource.relative_rotary.last_event.rotation.direction.value,
            _CONF_DURATION: hue_resource.relative_rotary.last_event.rotation.duration,
            _CONF_STEPS: hue_resource.relative_rotary.last_event.rotation.steps,
        }
        shc.bus.async_fire(Const.ATTR_HUE_EVENT, data)

    # add listener for updates from `relative_rotary` resource
    conf_entry.async_on_unload(
        rotary_controller.subscribe(
            handle_rotary_event, event_filter=v2.EventType.RESOURCE_UPDATED
        )
    )


async def async_setup_binary_sensors(
    bridge: HueBridge,
    config_entry: core.ConfigEntry,
    async_add_entities: core.AddEntitiesCallback,
) -> None:
    """Set up Hue Sensors from Config Entry."""
    api: v2.HueBridgeV2 = bridge.api

    @core.callback
    def register_items(
        controller: BinaryControllerType, sensor_class: BinarySensorType
    ):
        @core.callback
        def async_add_sensor(
            _event_type: EventType, resource: BinarySensorType
        ) -> None:
            """Add Hue Binary Sensor."""
            async_add_entities([sensor_class(bridge, controller, resource)])

        # add all current items in controller
        for sensor in controller:
            async_add_sensor(EventType.RESOURCE_ADDED, sensor)

        # register listener for new sensors
        config_entry.async_on_unload(
            controller.subscribe(
                async_add_sensor, event_filter=EventType.RESOURCE_ADDED
            )
        )

    # setup for each binary-sensor-type hue resource
    register_items(api.sensors.motion, HueMotionSensor)
    register_items(api.config.entertainment_configuration, HueEntertainmentActiveSensor)


async def async_setup_sensors(
    bridge: HueBridge,
    config_entry: core.ConfigEntry,
    async_add_entities: core.AddEntitiesCallback,
) -> None:
    """Set up Hue Sensors from Config Entry."""
    api: v2.HueBridgeV2 = bridge.api
    ctrl_base: SensorsController = api.sensors

    @core.callback
    def register_items(controller: SensorControllerType, sensor_class: SensorType):
        @core.callback
        def async_add_sensor(_event_type: EventType, resource: SensorType) -> None:
            """Add Hue Sensor."""
            async_add_entities([sensor_class(bridge, controller, resource)])

        # add all current items in controller
        for sensor in controller:
            async_add_sensor(EventType.RESOURCE_ADDED, sensor)

        # register listener for new sensors
        config_entry.async_on_unload(
            controller.subscribe(
                async_add_sensor, event_filter=EventType.RESOURCE_ADDED
            )
        )

    # setup for each sensor-type hue resource
    register_items(ctrl_base.temperature, HueTemperatureSensor)
    register_items(ctrl_base.light_level, HueLightLevelSensor)
    register_items(ctrl_base.device_power, HueBatterySensor)
    register_items(ctrl_base.zigbee_connectivity, HueZigbeeConnectivitySensor)
