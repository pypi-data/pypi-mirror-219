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

from aiohue.v2 import HueBridgeV2
from aiohue.v2.controllers.events import EventType
from aiohue.v2.controllers.sensors import (
    LightLevel,
    LightLevelController,
    Motion,
    MotionController,
)

from .... import core
from .hue_base_entity import HueBaseEntity

if not typing.TYPE_CHECKING:

    class HueBridge:
        pass


if typing.TYPE_CHECKING:
    from ..hue_bridge import HueBridge

ControllerType: typing.TypeAlias = typing.Union[LightLevelController, MotionController]

SensingService: typing.TypeAlias = typing.Union[LightLevel, Motion]


# pylint: disable=unused-variable
class HueSensingServiceEnabledEntity(HueBaseEntity, core.Switch.Entity):
    """Representation of a Switch entity from Hue SensingService."""

    _attr_entity_category = core.EntityCategory.CONFIG
    _attr_device_class = core.Switch.DeviceClass.SWITCH

    def __init__(
        self,
        bridge: HueBridge,
        controller: LightLevelController | MotionController,
        resource: SensingService,
    ) -> None:
        """Initialize the entity."""
        super().__init__(bridge, controller, resource)

    @property
    def controller(self) -> ControllerType:
        return self._controller

    @property
    def resource(self) -> SensingService:
        return self._resource

    @property
    def is_on(self) -> bool:
        """Return true if the switch is on."""
        return self.resource.enabled

    async def async_turn_on(self, **kwargs: typing.Any) -> None:
        """Turn the entity on."""
        await self._bridge.async_request_call(
            self.controller.set_enabled, self.resource.id, enabled=True
        )

    async def async_turn_off(self, **kwargs: typing.Any) -> None:
        """Turn the entity on."""
        await self._bridge.async_request_call(
            self.controller.set_enabled, self.resource.id, enabled=False
        )


async def async_setup_switches(
    bridge: HueBridge,
    config_entry: core.ConfigEntry,
    async_add_entities: core.AddEntitiesCallback,
) -> None:
    """Set up Hue switch platform from Hue resources."""
    api: HueBridgeV2 = bridge.api

    if bridge.api_version == 1:
        # should not happen, but just in case
        raise NotImplementedError("Switch support is only available for V2 bridges")

    @core.callback
    def register_items(controller: ControllerType):
        @core.callback
        def async_add_entity(_event_type: EventType, resource: SensingService) -> None:
            """Add entity from Hue resource."""
            async_add_entities(
                [HueSensingServiceEnabledEntity(bridge, controller, resource)]
            )

        # add all current items in controller
        for item in controller:
            async_add_entity(EventType.RESOURCE_ADDED, item)

        # register listener for new items only
        config_entry.async_on_unload(
            controller.subscribe(
                async_add_entity, event_filter=EventType.RESOURCE_ADDED
            )
        )

    # setup for each switch-type hue resource
    register_items(api.sensors.motion)
    register_items(api.sensors.light_level)
