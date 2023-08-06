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

import typing
import boschshcpy as bosch

from ... import core
from .bosch_entity import BoschEntity

if not typing.TYPE_CHECKING:

    class BoschShcIntegration:
        pass


if typing.TYPE_CHECKING:
    from .bosch_shc_integration import BoschShcIntegration

_light: typing.TypeAlias = core.Light
_color: typing.TypeAlias = core.helpers.Color


class LightSwitch(BoschEntity, core.Light.Entity):
    """Representation of a SHC controlled light."""

    @property
    def supported_color_modes(self):
        """Flag supported features."""
        modes = set[_light.ColorMode]()
        if self._device.supports_color_hsb:
            modes.add(_light.ColorMode.HS)
            modes.add(_light.ColorMode.COLOR_TEMP)
        elif self._device.supports_color_temp:
            modes.add(_light.ColorMode.COLOR_TEMP)
        elif self._device.supports_brightness:
            modes.add(_light.ColorMode.BRIGHTNESS)
        if len(modes) == 0:
            modes.add(_light.ColorMode.ONOFF)
        return modes

    @property
    def is_on(self):
        """Return light state."""
        return self._device.state

    @property
    def brightness(self) -> int:
        """Return the brightness of this light between 0..255."""
        brightness_value = (
            round(self._device.brightness * 255 / 100)
            if self._device.brightness
            else None
        )
        return brightness_value

    @property
    def hs_color(self):
        """Return the rgb color of this light."""
        rgb_raw = self._device.rgb
        rgb = ((rgb_raw >> 16) & 0xFF, (rgb_raw >> 8) & 0xFF, rgb_raw & 0xFF)
        return _color.RGB_to_hs(*rgb)

    @property
    def color_temp(self):
        """Return the color temp of this light."""
        if self._device.supports_color_temp:
            return self._device.color
        return None

    def turn_on(self, **kwargs):
        """Turn the light on."""
        hs_color = kwargs.get(_light.ATTR_HS_COLOR)
        color_temp = kwargs.get(_light.ATTR_COLOR_TEMP)
        brightness = kwargs.get(_light.ATTR_BRIGHTNESS)

        if brightness is not None and self._device.supports_brightness:
            self._device.brightness = round(brightness * 100 / 255)
        if self._device.supports_color_hsb:
            if color_temp is not None:
                if color_temp < self._device.min_color_temperature:
                    color_temp = self._device.min_color_temperature
                if color_temp > self._device.max_color_temperature:
                    color_temp = self._device.max_color_temperature
                hs_color = _color.temperature_to_hs(
                    _color.temperature_mired_to_kelvin(color_temp)
                )
            if hs_color is not None:
                rgb = _color.hs_to_RGB(*hs_color)
                raw_rgb = (rgb[0] << 16) + (rgb[1] << 8) + rgb[2]
                self._device.rgb = raw_rgb
        if color_temp is not None and self._device.supports_color_temp:
            self._device.color = color_temp

        if not self.is_on:
            self._device.state = True

    def turn_off(self, **kwargs):
        """Turn the light off."""
        self._device.state = False


# pylint: disable=unused-variable
async def _async_setup_light_switches(
    owner: BoschShcIntegration,
    session: bosch.SHCSession,
    config_entry: core.ConfigEntry,
) -> typing.Iterable[core.Entity]:
    """Set up the light platform."""
    entities = []

    for light in session.device_helper.ledvance_lights:
        entities.append(
            LightSwitch(
                owner,
                device=light,
                parent_id=session.information.unique_id,
                entry_id=config_entry.entry_id,
            )
        )

    return entities
