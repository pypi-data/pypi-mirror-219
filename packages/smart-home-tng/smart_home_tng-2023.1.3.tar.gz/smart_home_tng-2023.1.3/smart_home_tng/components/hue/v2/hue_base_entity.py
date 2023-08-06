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

import typing

from aiohue.v2.controllers.base import BaseResourcesController
from aiohue.v2.controllers.events import EventType
from aiohue.v2.models.resource import ResourceTypes
from aiohue.v2.models.zigbee_connectivity import ConnectivityServiceStatus
from aiohue.v2.models.device_power import DevicePower
from aiohue.v2.models.grouped_light import GroupedLight
from aiohue.v2.models.light import Light
from aiohue.v2.models.light_level import LightLevel
from aiohue.v2.models.motion import Motion

from .... import core
from ..const import Const

if not typing.TYPE_CHECKING:

    class HueBridge:
        pass


if typing.TYPE_CHECKING:
    from ..hue_bridge import HueBridge

HueResource = typing.Union[Light, DevicePower, GroupedLight, LightLevel, Motion]

_RESOURCE_TYPE_NAMES: typing.Final = {
    # a simple mapping of hue resource type to Hass name
    ResourceTypes.LIGHT_LEVEL: "Illuminance",
    ResourceTypes.DEVICE_POWER: "Battery",
}


# pylint: disable=unused-variable
class HueBaseEntity(core.Entity):
    """Generic Entity Class for a Hue resource."""

    _attr_should_poll = False

    def __init__(
        self,
        bridge: HueBridge,
        controller: BaseResourcesController,
        resource: HueResource,
    ) -> None:
        """Initialize a generic Hue resource entity."""
        self._bridge = bridge
        self._controller = controller
        self._resource = resource
        self._device = controller.get_device(resource.id)
        self._logger = bridge.logger.getChild(resource.type.value)

        # Entity class attributes
        self._attr_unique_id = resource.id
        # device is precreated in main handler
        # this attaches the entity to the precreated device
        if self._device is not None:
            self._attr_device_info = core.DeviceInfo(
                identifiers={(bridge.owner.domain, self._device.id)},
            )
        # used for availability workaround
        self._ignore_availability = None
        self._last_state = None

    @property
    def name(self) -> str:
        """Return name for the entity."""
        if self._device is None:
            # this is just a guard
            # creating a pretty name for device-less entities (e.g. groups/scenes)
            # should be handled in the platform instead
            return self._resource.type.value
        # if resource is a light, use the name from metadata
        dev_name = self._device.metadata.name
        if self._resource.type == ResourceTypes.LIGHT:
            return dev_name
        # for sensors etc, use devicename + pretty name of type
        type_title = _RESOURCE_TYPE_NAMES.get(
            self._resource.type, self._resource.type.value.replace("_", " ").title()
        )
        return f"{dev_name} {type_title}"

    async def async_added_to_shc(self) -> None:
        """Call when entity is added."""
        self._check_availability()
        # Add value_changed callbacks.
        self.async_on_remove(
            self._controller.subscribe(
                self._handle_event,
                self._resource.id,
                (EventType.RESOURCE_UPDATED, EventType.RESOURCE_DELETED),
            )
        )
        # also subscribe to device update event to catch device changes (e.g. name)
        if self._device is None:
            return
        self.async_on_remove(
            self._bridge.api.devices.subscribe(
                self._handle_event,
                self._device.id,
                EventType.RESOURCE_UPDATED,
            )
        )
        # subscribe to zigbee_connectivity to catch availability changes
        if zigbee := self._bridge.api.devices.get_zigbee_connectivity(self._device.id):
            self.async_on_remove(
                self._bridge.api.sensors.zigbee_connectivity.subscribe(
                    self._handle_event,
                    zigbee.id,
                    EventType.RESOURCE_UPDATED,
                )
            )

    @property
    def available(self) -> bool:
        """Return entity availability."""
        # entities without a device attached should be always available
        if self._device is None:
            return True
        # the zigbee connectivity sensor itself should be always available
        if self._resource.type == ResourceTypes.ZIGBEE_CONNECTIVITY:
            return True
        if self._ignore_availability:
            return True
        # all device-attached entities get availability from the zigbee connectivity
        if zigbee := self._bridge.api.devices.get_zigbee_connectivity(self._device.id):
            return zigbee.status == ConnectivityServiceStatus.CONNECTED
        return True

    @core.callback
    def on_update(self) -> None:
        """Call on update event."""
        # used in subclasses

    @core.callback
    def _handle_event(self, event_type: EventType, resource: HueResource) -> None:
        """Handle status event for this resource (or it's parent)."""
        if event_type == EventType.RESOURCE_DELETED:
            # remove any services created for zones/rooms
            # regular devices are removed automatically by the logic in device.py.
            if resource.type in [ResourceTypes.ROOM, ResourceTypes.ZONE]:
                dev_reg = self._bridge.controller.device_registry
                if device := dev_reg.async_get_device(
                    {(self._bridge.owner.domain, resource.id)}
                ):
                    dev_reg.async_remove_device(device.id)
            if resource.type in [ResourceTypes.GROUPED_LIGHT, ResourceTypes.SCENE]:
                ent_reg = self._bridge.controller.entity_registry
                ent_reg.async_remove(self.entity_id)
            return
        self._logger.debug(f"Received status update for {self.entity_id}")
        self._check_availability()
        self.on_update()
        self.async_write_state()

    @core.callback
    def _check_availability(self):
        """Check availability of the device."""
        # return if we already processed this entity
        if self._ignore_availability is not None:
            return
        # only do the availability check for entities connected to a device (with `on` feature)
        if self._device is None or not hasattr(self._resource, "on"):
            self._ignore_availability = False
            return
        # ignore availability if user added device to ignore list
        if self._device.id in self._bridge.config_entry.options.get(
            Const.CONF_IGNORE_AVAILABILITY, []
        ):
            self._ignore_availability = True
            self._logger.info(
                f"Device {self.name} is configured to ignore availability status. ",
            )
            return
        # certified products (normally) report their state correctly
        # no need for workaround/reporting
        if self._device.product_data.certified:
            self._ignore_availability = False
            return
        # some (3th party) Hue lights report their connection status incorrectly
        # causing the zigbee availability to report as disconnected while in fact
        # it can be controlled. If the light is reported unavailable
        # by the zigbee connectivity but the state changes its considered as a
        # malfunctioning device and we report it.
        # While the user should actually fix this issue, we allow to
        # ignore the availability for this light/device from the config options.
        cur_state = self._resource.on.on
        if self._last_state is None:
            self._last_state = cur_state
            return
        if zigbee := self._bridge.api.devices.get_zigbee_connectivity(self._device.id):
            if (
                self._last_state != cur_state
                and zigbee.status != ConnectivityServiceStatus.CONNECTED
            ):
                # the device state changed from on->off or off->on
                # while it was reported as not connected!
                self._logger.warning(
                    f"Device {self.name} changed state while reported as disconnected. "
                    + "This might be an indicator that routing is not working for this device "
                    + "or the device is having connectivity issues. "
                    + "You can disable availability reporting for this device in the Hue options. "
                    + f"Device details: {self._device.product_data.manufacturer_name} - "
                    + f"{self._device.product_data.product_name} "
                    + f"({self._device.product_data.model_id}) fw: "
                    + f"{self._device.product_data.software_version}",
                )
                # set attribute to false because we only want to log once per light/device.
                # a user must opt-in to ignore availability through integration options
                self._ignore_availability = False
        self._last_state = cur_state
