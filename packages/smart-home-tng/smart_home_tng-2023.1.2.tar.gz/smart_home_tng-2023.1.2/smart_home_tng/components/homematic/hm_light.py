"""
Homematic Integration for Smart Home - The Next Generation.

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

from ... import core
from .const import Const
from .hm_device import HMDevice

if not typing.TYPE_CHECKING:

    class HomematicIntegration:
        pass


if typing.TYPE_CHECKING:
    from .homematic_integration import HomematicIntegration


# pylint: disable=unused-variable
class HMLight(HMDevice, core.Light.Entity):
    """Representation of a Homematic light."""

    @property
    def brightness(self):
        """Return the brightness of this light between 0..255."""
        # Is dimmer?
        if self._state == "LEVEL":
            return int(self._hm_get_state() * 255)
        return None

    @property
    def is_on(self):
        """Return true if light is on."""
        try:
            return self._hm_get_state() > 0
        except TypeError:
            return False

    @property
    def color_mode(self) -> core.Light.ColorMode:
        """Return the color mode of the light."""
        if "COLOR" in self._hmdevice.WRITENODE:
            return core.Light.ColorMode.HS
        if hasattr(self._hmdevice, "get_color_temp"):
            return core.Light.ColorMode.COLOR_TEMP
        return core.Light.ColorMode.BRIGHTNESS

    @property
    def supported_color_modes(self) -> set[core.Light.ColorMode | str]:
        """Flag supported color modes."""
        color_modes: set[core.Light.ColorMode | str] = set()

        if "COLOR" in self._hmdevice.WRITENODE:
            color_modes.add(core.Light.ColorMode.HS)
        if hasattr(self._hmdevice, "get_color_temp"):
            color_modes.add(core.Light.ColorMode.COLOR_TEMP)
        if not color_modes:
            color_modes.add(core.Light.ColorMode.BRIGHTNESS)

        return color_modes

    @property
    def supported_features(self) -> int:
        """Flag supported features."""
        features: int = core.Light.EntityFeature.TRANSITION
        if "PROGRAM" in self._hmdevice.WRITENODE:
            features |= core.Light.EntityFeature.EFFECT
        return features

    @property
    def hs_color(self):
        """Return the hue and saturation color value [float, float]."""
        if core.Light.ColorMode.HS not in self.supported_color_modes:
            return None
        hue, sat = self._hmdevice.get_hs_color(self._channel)
        return hue * 360.0, sat * 100.0

    @property
    def color_temp(self):
        """Return the color temp in mireds [int]."""
        if core.Light.ColorMode.COLOR_TEMP not in self.supported_color_modes:
            return None
        hm_color_temp = self._hmdevice.get_color_temp(self._channel)
        return self.max_mireds - (self.max_mireds - self.min_mireds) * hm_color_temp

    @property
    def effect_list(self):
        """Return the list of supported effects."""
        if not self.supported_features & core.Light.EntityFeature.EFFECT:
            return None
        return self._hmdevice.get_effect_list()

    @property
    def effect(self):
        """Return the current color change program of the light."""
        if not self.supported_features & core.Light.EntityFeature.EFFECT:
            return None
        return self._hmdevice.get_effect()

    def turn_on(self, **kwargs: typing.Any) -> None:
        """Turn the light on and/or change color or color effect settings."""
        if core.Light.ATTR_TRANSITION in kwargs:
            self._hmdevice.setValue(
                "RAMP_TIME", kwargs[core.Light.ATTR_TRANSITION], self._channel
            )

        if core.Light.ATTR_BRIGHTNESS in kwargs and self._state == "LEVEL":
            percent_bright = float(kwargs[core.Light.ATTR_BRIGHTNESS]) / 255
            self._hmdevice.set_level(percent_bright, self._channel)
        elif (
            core.Light.ATTR_HS_COLOR not in kwargs
            and core.Light.ATTR_COLOR_TEMP not in kwargs
            and core.Light.ATTR_EFFECT not in kwargs
        ):
            self._hmdevice.on(self._channel)

        if core.Light.ATTR_HS_COLOR in kwargs:
            self._hmdevice.set_hs_color(
                hue=kwargs[core.Light.ATTR_HS_COLOR][0] / 360.0,
                saturation=kwargs[core.Light.ATTR_HS_COLOR][1] / 100.0,
                channel=self._channel,
            )
        if core.Light.ATTR_COLOR_TEMP in kwargs:
            hm_temp = (self.max_mireds - kwargs[core.Light.ATTR_COLOR_TEMP]) / (
                self.max_mireds - self.min_mireds
            )
            self._hmdevice.set_color_temp(hm_temp)
        if core.Light.ATTR_EFFECT in kwargs:
            self._hmdevice.set_effect(kwargs[core.Light.ATTR_EFFECT])

    def turn_off(self, **kwargs: typing.Any) -> None:
        """Turn the light off."""
        if core.Light.ATTR_TRANSITION in kwargs:
            self._hmdevice.setValue(
                "RAMP_TIME", kwargs[core.Light.ATTR_TRANSITION], self._channel
            )

        self._hmdevice.off(self._channel)

    def _init_data_struct(self):
        """Generate a data dict (self._data) from the Homematic metadata."""
        # Use LEVEL
        self._state = "LEVEL"
        self._data[self._state] = None

        if core.Light.ColorMode.HS in self.supported_color_modes:
            self._data.update({"COLOR": None})
        if self.supported_features & core.Light.EntityFeature.EFFECT:
            self._data.update({"PROGRAM": None})


async def async_setup_lights(
    comp: HomematicIntegration,
    add_entities: core.AddEntitiesCallback,
    discovery_info: core.DiscoveryInfoType = None,
) -> None:
    """Set up the Homematic light platform."""
    if discovery_info is None:
        return

    devices = []
    for conf in discovery_info[Const.ATTR_DISCOVER_DEVICES]:
        new_device = HMLight(comp, conf)
        devices.append(new_device)

    add_entities(devices, True)
