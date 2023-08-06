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
from aiohue.v2.controllers.groups import (
    GroupedLight,
    Room,
    Zone,
    GroupedLightController,
)
from aiohue.v2.models.feature import DynamicStatus

from .... import core
from .helpers import (
    normalize_hue_brightness,
    normalize_hue_colortemp,
    normalize_hue_transition,
)
from .hue_base_entity import HueBaseEntity

if not typing.TYPE_CHECKING:

    class HueBridge:
        pass


if typing.TYPE_CHECKING:
    from ..hue_bridge import HueBridge


# pylint: disable=unused-variable
class GroupedHueLight(HueBaseEntity, core.Light.Entity):
    """Representation of a Grouped Hue light."""

    _attr_icon = "mdi:lightbulb-group"

    def __init__(
        self, bridge: HueBridge, resource: GroupedLight, group: Room | Zone
    ) -> None:
        """Initialize the light."""
        controller = bridge.api.groups.grouped_light
        super().__init__(bridge, controller, resource)
        self._group = group
        self._api: HueBridgeV2 = bridge.api
        self._attr_supported_features |= core.Light.EntityFeature.FLASH
        self._attr_supported_features |= core.Light.EntityFeature.TRANSITION

        self._dynamic_mode_active = False
        self._update_values()

    @property
    def controller(self) -> GroupedLightController:
        return self._controller

    @property
    def resource(self) -> GroupedLight:
        return self._resource

    async def async_added_to_shc(self) -> None:
        """Call when entity is added."""
        await super().async_added_to_shc()

        # subscribe to group updates
        self.async_on_remove(
            self._api.groups.subscribe(self._handle_event, self._group.id)
        )
        # We need to watch the underlying lights too
        # if we want feedback about color/brightness changes
        if self._attr_supported_color_modes:
            light_ids = tuple(
                x.id for x in self.controller.get_lights(self.resource.id)
            )
            self.async_on_remove(
                self._api.lights.subscribe(self._handle_event, light_ids)
            )

    @property
    def name(self) -> str:
        """Return name of room/zone for this grouped light."""
        return self._group.metadata.name

    @property
    def is_on(self) -> bool:
        """Return true if light is on."""
        return self._resource.on.on

    @property
    def extra_state_attributes(self) -> dict[str, typing.Any]:
        """Return the optional state attributes."""
        scenes = {
            x.metadata.name for x in self._api.scenes if x.group.rid == self._group.id
        }
        lights = {
            self.controller.get_device(x.id).metadata.name
            for x in self.controller.get_lights(self.resource.id)
        }
        return {
            "is_hue_group": True,
            "hue_scenes": scenes,
            "hue_type": self._group.type.value,
            "lights": lights,
            "dynamics": self._dynamic_mode_active,
        }

    @property
    def device_info(self) -> core.DeviceInfo:
        """Return device (service) info."""
        # we create a virtual service/device for Hue zones/rooms
        # so we have a parent for grouped lights and scenes
        model = self._group.type.value.title()
        return core.DeviceInfo(
            identifiers={(self._bridge.owner.domain, self._group.id)},
            entry_type=core.DeviceRegistryEntryType.SERVICE,
            name=self._group.metadata.name,
            manufacturer=self._api.config.bridge_device.product_data.manufacturer_name,
            model=model,
            suggested_area=self._group.metadata.name if model == "Room" else None,
            via_device=(self._bridge.owner.domain, self._api.config.bridge_device.id),
        )

    async def async_turn_on(self, **kwargs: typing.Any) -> None:
        """Turn the grouped_light on."""
        transition = normalize_hue_transition(kwargs.get(core.Light.ATTR_TRANSITION))
        xy_color = kwargs.get(core.Light.ATTR_XY_COLOR)
        color_temp = normalize_hue_colortemp(kwargs.get(core.Light.ATTR_COLOR_TEMP))
        brightness = normalize_hue_brightness(kwargs.get(core.Light.ATTR_BRIGHTNESS))
        flash = kwargs.get(core.Light.ATTR_FLASH)

        if flash is not None:
            await self.async_set_flash(flash)
            return

        await self._bridge.async_request_call(
            self.controller.set_state,
            id=self.resource.id,
            on=True,
            brightness=brightness,
            color_xy=xy_color,
            color_temp=color_temp,
            transition_time=transition,
        )

    async def async_turn_off(self, **kwargs: typing.Any) -> None:
        """Turn the light off."""
        transition = normalize_hue_transition(kwargs.get(core.Light.ATTR_TRANSITION))
        flash = kwargs.get(core.Light.ATTR_FLASH)

        if flash is not None:
            await self.async_set_flash(flash)
            # flash can not be sent with other commands at the same time
            return

        await self._bridge.async_request_call(
            self.controller.set_state,
            id=self.resource.id,
            on=False,
            transition_time=transition,
        )

    async def async_set_flash(self, flash: str) -> None:
        """Send flash command to light."""
        await self._bridge.async_request_call(
            self.controller.set_flash,
            id=self.resource.id,
            short=flash == core.Light.FLASH_SHORT,
        )

    @core.callback
    def on_update(self) -> None:
        """Call on update event."""
        self._update_values()

    @core.callback
    def _update_values(self) -> None:
        """Set base values from underlying lights of a group."""
        supported_color_modes: set[core.Light.ColorMode | str] = set()
        lights_with_color_support = 0
        lights_with_color_temp_support = 0
        lights_with_dimming_support = 0
        total_brightness = 0
        all_lights = self.controller.get_lights(self.resource.id)
        lights_in_colortemp_mode = 0
        lights_in_dynamic_mode = 0
        # loop through all lights to find capabilities
        for light in all_lights:
            if color_temp := light.color_temperature:
                lights_with_color_temp_support += 1
                # we assume mired values from the first capable light
                self._attr_color_temp = color_temp.mirek
                self._attr_max_mireds = color_temp.mirek_schema.mirek_maximum
                self._attr_min_mireds = color_temp.mirek_schema.mirek_minimum
                if color_temp.mirek is not None and color_temp.mirek_valid:
                    lights_in_colortemp_mode += 1
            if color := light.color:
                lights_with_color_support += 1
                # we assume xy values from the first capable light
                self._attr_xy_color = (color.xy.x, color.xy.y)
            if dimming := light.dimming:
                lights_with_dimming_support += 1
                total_brightness += dimming.brightness
            if (
                light.dynamics
                and light.dynamics.status == DynamicStatus.DYNAMIC_PALETTE
            ):
                lights_in_dynamic_mode += 1

        # this is a bit hacky because light groups may contain lights
        # of different capabilities. We set a colormode as supported
        # if any of the lights support it
        # this means that the state is derived from only some of the lights
        # and will never be 100% accurate but it will be close
        if lights_with_color_support > 0:
            supported_color_modes.add(core.Light.ColorMode.XY)
        if lights_with_color_temp_support > 0:
            supported_color_modes.add(core.Light.ColorMode.COLOR_TEMP)
        if lights_with_dimming_support > 0:
            if len(supported_color_modes) == 0:
                # only add color mode brightness if no color variants
                supported_color_modes.add(core.Light.ColorMode.BRIGHTNESS)
            self._attr_brightness = round(
                ((total_brightness / lights_with_dimming_support) / 100) * 255
            )
        else:
            supported_color_modes.add(core.Light.ColorMode.ONOFF)
        self._dynamic_mode_active = lights_in_dynamic_mode > 0
        self._attr_supported_color_modes = supported_color_modes
        # pick a winner for the current colormode
        if (
            lights_with_color_temp_support > 0
            and lights_in_colortemp_mode == lights_with_color_temp_support
        ):
            self._attr_color_mode = core.Light.ColorMode.COLOR_TEMP
        elif lights_with_color_support > 0:
            self._attr_color_mode = core.Light.ColorMode.XY
        elif lights_with_dimming_support > 0:
            self._attr_color_mode = core.Light.ColorMode.BRIGHTNESS
        else:
            self._attr_color_mode = core.Light.ColorMode.ONOFF


async def async_setup_group_lights(
    bridge: HueBridge,
    config_entry: core.ConfigEntry,
    async_add_entities: core.AddEntitiesCallback,
) -> None:
    """Set up Hue groups on light platform."""
    api: HueBridgeV2 = bridge.api

    @core.callback
    def async_add_light(_event_type: EventType, resource: GroupedLight) -> None:
        """Add Grouped Light for Hue Room/Zone."""
        group = api.groups.grouped_light.get_zone(resource.id)
        if group is None:
            return
        light = GroupedHueLight(bridge, resource, group)
        async_add_entities([light])

    # add current items
    for item in api.groups.grouped_light.items:
        async_add_light(EventType.RESOURCE_ADDED, item)

    # register listener for new grouped_light
    config_entry.async_on_unload(
        api.groups.grouped_light.subscribe(
            async_add_light, event_filter=EventType.RESOURCE_ADDED
        )
    )
