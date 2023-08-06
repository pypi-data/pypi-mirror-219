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

import aiohue
from aiohue.v2.controllers.events import EventType
from aiohue.v2.controllers.scenes import Scene, ScenePut, ScenesController
import voluptuous as vol

from .... import core
from ..const import Const
from .helpers import normalize_hue_brightness, normalize_hue_transition
from .hue_base_entity import HueBaseEntity

if not typing.TYPE_CHECKING:

    class HueBridge:
        pass


if typing.TYPE_CHECKING:
    from ..hue_bridge import HueBridge

_SERVICE_ACTIVATE_SCENE: typing.Final = "activate_scene"
_ATTR_SPEED: typing.Final = "speed"


# pylint: disable=unused-variable
class HueScene(HueBaseEntity, core.Scene):
    """Representation of a Scene entity from Hue Scenes."""

    def __init__(
        self,
        bridge: HueBridge,
        controller: ScenesController,
        resource: Scene,
    ) -> None:
        """Initialize the entity."""
        super().__init__(bridge, controller, resource)
        self._group = self.controller.get_group(self.resource.id)

    @property
    def controller(self) -> ScenesController:
        return self._controller

    @property
    def resource(self) -> Scene:
        return self._resource

    async def async_added_to_shc(self) -> None:
        """Call when entity is added."""
        await super().async_added_to_shc()
        # Add value_changed callback for group to catch name changes.
        self.async_on_remove(
            self._bridge.api.groups.subscribe(
                self._handle_event,
                self._group.id,
                (EventType.RESOURCE_UPDATED),
            )
        )

    @property
    def name(self) -> str:
        """Return default entity name."""
        return f"{self._group.metadata.name} {self.resource.metadata.name}"

    @property
    def is_dynamic(self) -> bool:
        """Return if this scene has a dynamic color palette."""
        if self.resource.palette.color and len(self.resource.palette.color) > 1:
            return True
        if (
            self.resource.palette.color_temperature
            and len(self.resource.palette.color_temperature) > 1
        ):
            return True
        return False

    async def async_activate(self, **kwargs: typing.Any) -> None:
        """Activate Hue scene."""
        transition = normalize_hue_transition(kwargs.get(core.Light.ATTR_TRANSITION))
        # the options below are advanced only
        # as we're not allowed to override the default scene turn_on service
        # we've implemented a `activate_scene` entity service
        dynamic = kwargs.get(Const.ATTR_DYNAMIC, False)
        speed = kwargs.get(_ATTR_SPEED)
        brightness = normalize_hue_brightness(kwargs.get(core.Light.ATTR_BRIGHTNESS))

        if speed is not None:
            await self._bridge.async_request_call(
                self.controller.update,
                self.resource.id,
                ScenePut(speed=speed / 100),
            )

        await self._bridge.async_request_call(
            self.controller.recall,
            self.resource.id,
            dynamic=dynamic,
            duration=transition,
            brightness=brightness,
        )

    @property
    def extra_state_attributes(self) -> dict[str, typing.Any]:
        """Return the optional state attributes."""
        brightness = None
        if palette := self.resource.palette:
            if palette.dimming:
                brightness = palette.dimming[0].brightness
        if brightness is None:
            # get brightness from actions
            for action in self.resource.actions:
                if action.action.dimming:
                    brightness = action.action.dimming.brightness
                    break
        return {
            "group_name": self._group.metadata.name,
            "group_type": self._group.type.value,
            "name": self.resource.metadata.name,
            "speed": self.resource.speed,
            "brightness": brightness,
            "is_dynamic": self.is_dynamic,
        }

    @property
    def device_info(self) -> core.DeviceInfo:
        """Return device (service) info."""
        # we create a virtual service/device for Hue scenes
        # so we have a parent for grouped lights and scenes
        return core.DeviceInfo(
            identifiers={(self._bridge.owner.domain, self._group.id)},
            entry_type=core.DeviceRegistryEntryType.SERVICE,
            name=self._group.metadata.name,
            manufacturer=self._bridge.api.config.bridge_device.product_data.manufacturer_name,
            model=self._group.type.value.title(),
            suggested_area=self._group.metadata.name,
            via_device=(
                self._bridge.owner.domain,
                self._bridge.api.config.bridge_device.id,
            ),
        )


async def async_setup_scenes(
    bridge: HueBridge,
    config_entry: core.ConfigEntry,
    async_add_entities: core.AddEntitiesCallback,
) -> None:
    """Set up scene platform from Hue group scenes."""
    if bridge.api_version == 1:
        # should not happen, but just in case
        raise NotImplementedError("Scene support is only available for V2 bridges")

    api: aiohue.HueBridgeV2 = bridge.api

    # add entities for all scenes
    @core.callback
    def async_add_entity(_event_type: EventType, resource: Scene) -> None:
        """Add entity from Hue resource."""
        async_add_entities([HueScene(bridge, api.scenes, resource)])

    # add all current items in controller
    for item in api.scenes:
        async_add_entity(EventType.RESOURCE_ADDED, item)

    # register listener for new items only
    config_entry.async_on_unload(
        api.scenes.subscribe(async_add_entity, event_filter=EventType.RESOURCE_ADDED)
    )

    # add platform service to turn_on/activate scene with advanced options
    platform = core.EntityPlatform.async_get_current_platform()
    platform.async_register_entity_service(
        _SERVICE_ACTIVATE_SCENE,
        {
            vol.Optional(Const.ATTR_DYNAMIC): vol.Coerce(bool),
            vol.Optional(_ATTR_SPEED): vol.All(
                vol.Coerce(int), vol.Range(min=0, max=100)
            ),
            vol.Optional(core.Light.ATTR_TRANSITION): vol.All(
                vol.Coerce(float), vol.Range(min=0, max=600)
            ),
            vol.Optional(core.Light.ATTR_BRIGHTNESS): vol.All(
                vol.Coerce(int), vol.Range(min=0, max=255)
            ),
        },
        "_async_activate",
    )
