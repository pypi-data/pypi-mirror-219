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
from aiohue.v2.controllers.lights import LightsController
from aiohue.v2.models.feature import EffectStatus, TimedEffectStatus
from aiohue.v2.models.light import Light

from .... import core
from ..hue_bridge import HueBridge
from .helpers import (
    normalize_hue_brightness,
    normalize_hue_colortemp,
    normalize_hue_transition,
)
from .hue_base_entity import HueBaseEntity


_EFFECT_NONE: typing.Final = "None"


# pylint: disable=unused-variable
class HueLight(HueBaseEntity, core.Light.Entity):
    """Representation of a Hue light."""

    def __init__(
        self, bridge: HueBridge, controller: LightsController, resource: Light
    ) -> None:
        """Initialize the light."""
        super().__init__(bridge, controller, resource)
        if self.resource.alert and self.resource.alert.action_values:
            self._attr_supported_features |= core.Light.EntityFeature.FLASH
        self._supported_color_modes: set[core.Light.ColorMode | str] = set()
        if self.resource.supports_color:
            self._supported_color_modes.add(core.Light.ColorMode.XY)
        if self.resource.supports_color_temperature:
            self._supported_color_modes.add(core.Light.ColorMode.COLOR_TEMP)
        if self.resource.supports_dimming:
            if len(self._supported_color_modes) == 0:
                # only add color mode brightness if no color variants
                self._supported_color_modes.add(core.Light.ColorMode.BRIGHTNESS)
            # support transition if brightness control
            self._attr_supported_features |= core.Light.EntityFeature.TRANSITION
        # get list of supported effects (combine effects and timed_effects)
        self._attr_effect_list = []
        if effects := resource.effects:
            self._attr_effect_list = [
                x.value for x in effects.status_values if x != EffectStatus.NO_EFFECT
            ]
        if timed_effects := resource.timed_effects:
            self._attr_effect_list += [
                x.value
                for x in timed_effects.status_values
                if x != TimedEffectStatus.NO_EFFECT
            ]
        if len(self._attr_effect_list) > 0:
            self._attr_effect_list.insert(0, _EFFECT_NONE)
            self._attr_supported_features |= core.Light.EntityFeature.EFFECT

    @property
    def resource(self) -> Light:
        return self._resource

    @property
    def controller(self) -> LightsController:
        return self._controller

    @property
    def brightness(self) -> int | None:
        """Return the brightness of this light between 0..255."""
        if dimming := self.resource.dimming:
            # Hue uses a range of [0, 100] to control brightness.
            return round((dimming.brightness / 100) * 255)
        return None

    @property
    def is_on(self) -> bool:
        """Return true if device is on (brightness above 0)."""
        return self.resource.on.on

    @property
    def color_mode(self) -> core.Light.ColorMode:
        """Return the color mode of the light."""
        if color_temp := self.resource.color_temperature:
            # Hue lights return `mired_valid` to indicate CT is active
            if color_temp.mirek_valid and color_temp.mirek is not None:
                return core.Light.ColorMode.COLOR_TEMP
        if self.resource.supports_color:
            return core.Light.ColorMode.XY
        if self.resource.supports_dimming:
            return core.Light.ColorMode.BRIGHTNESS
        # fallback to on_off
        return core.Light.ColorMode.ONOFF

    @property
    def xy_color(self) -> tuple[float, float]:
        """Return the xy color."""
        if color := self.resource.color:
            return (color.xy.x, color.xy.y)
        return None

    @property
    def color_temp(self) -> int:
        """Return the color temperature."""
        if color_temp := self.resource.color_temperature:
            return color_temp.mirek
        return 0

    @property
    def min_mireds(self) -> int:
        """Return the coldest color_temp that this light supports."""
        if color_temp := self.resource.color_temperature:
            return color_temp.mirek_schema.mirek_minimum
        return 0

    @property
    def max_mireds(self) -> int:
        """Return the warmest color_temp that this light supports."""
        if color_temp := self.resource.color_temperature:
            return color_temp.mirek_schema.mirek_maximum
        return 0

    @property
    def supported_color_modes(self) -> set:
        """Flag supported features."""
        return self._supported_color_modes

    @property
    def extra_state_attributes(self) -> dict[str, str]:
        """Return the optional state attributes."""
        return {
            "mode": self.resource.mode.value,
            "dynamics": self.resource.dynamics.status.value,
        }

    @property
    def effect(self) -> str:
        """Return the current effect."""
        if effects := self.resource.effects:
            if effects.status != EffectStatus.NO_EFFECT:
                return effects.status.value
        if timed_effects := self.resource.timed_effects:
            if timed_effects.status != TimedEffectStatus.NO_EFFECT:
                return timed_effects.status.value
        return _EFFECT_NONE

    async def async_turn_on(self, **kwargs: typing.Any) -> None:
        """Turn the device on."""
        transition = normalize_hue_transition(kwargs.get(core.Light.ATTR_TRANSITION))
        xy_color = kwargs.get(core.Light.ATTR_XY_COLOR)
        color_temp = normalize_hue_colortemp(kwargs.get(core.Light.ATTR_COLOR_TEMP))
        brightness = normalize_hue_brightness(kwargs.get(core.Light.ATTR_BRIGHTNESS))
        flash = kwargs.get(core.Light.ATTR_FLASH)
        effect = effect_str = kwargs.get(core.Light.ATTR_EFFECT)
        if effect_str in (_EFFECT_NONE, _EFFECT_NONE.lower()):
            effect = EffectStatus.NO_EFFECT
        elif effect_str is not None:
            # work out if we got a regular effect or timed effect
            effect = EffectStatus(effect_str)
            if effect == EffectStatus.UNKNOWN:
                effect = TimedEffectStatus(effect_str)
                if transition is None:
                    # a transition is required for timed effect, default to 10 minutes
                    transition = 600000

        if flash is not None:
            await self.async_set_flash(flash)
            # flash can not be sent with other commands at the same time or result will be flaky
            # Hue's default behavior is that a light returns to its previous state for short
            # flash (identify) and the light is kept turned on for long flash (breathe effect)
            # Why is this flash alert/effect hidden in the turn_on/off commands ?
            return

        await self._bridge.async_request_call(
            self.controller.set_state,
            id=self.resource.id,
            on=True,
            brightness=brightness,
            color_xy=xy_color,
            color_temp=color_temp,
            transition_time=transition,
            effect=effect,
        )

    async def async_turn_off(self, **kwargs: typing.Any) -> None:
        """Turn the light off."""
        transition = normalize_hue_transition(kwargs.get(core.Light.ATTR_TRANSITION))
        flash = kwargs.get(core.Light.ATTR_FLASH)

        if flash is not None:
            await self.async_set_flash(flash)
            # flash can not be sent with other commands at the same time or result will be flaky
            # Hue's default behavior is that a light returns to its previous state for short
            # flash (identify) and the light is kept turned on for long flash (breathe effect)
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


async def async_setup_lights(
    bridge: HueBridge,
    config_entry: core.ConfigEntry,
    async_add_entities: core.AddEntitiesCallback,
) -> None:
    """Set up Hue Light from Config Entry."""
    api: HueBridgeV2 = bridge.api
    controller: LightsController = api.lights

    @core.callback
    def async_add_light(_event_type: EventType, resource: Light) -> None:
        """Add Hue Light."""
        light = HueLight(bridge, controller, resource)
        async_add_entities([light])

    # add all current items in controller
    for light in controller:
        async_add_light(EventType.RESOURCE_ADDED, resource=light)

    # register listener for new lights
    config_entry.async_on_unload(
        controller.subscribe(async_add_light, event_filter=EventType.RESOURCE_ADDED)
    )
