"""
AVM FRITZ!SmartHome Integration for Smart Home - The Next Generation.

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

import requests

from ... import core
from .const import Const
from .fritzbox_data_update_coordinator import FritzboxDataUpdateCoordinator
from .fritzbox_entity import FritzboxEntity

if not typing.TYPE_CHECKING:

    class FritzboxIntegration:
        pass


if typing.TYPE_CHECKING:
    from .fritzbox_integration import FritzboxIntegration


_SUPPORTED_COLOR_MODES: typing.Final = {
    core.Light.ColorMode.COLOR_TEMP,
    core.Light.ColorMode.HS,
}


class FritzboxLight(FritzboxEntity, core.Light.Entity):
    """The light class for FRITZ!SmartHome lightbulbs."""

    def __init__(
        self,
        coordinator: FritzboxDataUpdateCoordinator,
        ain: str,
        supported_colors: dict,
        supported_color_temps: list[str],
    ) -> None:
        """Initialize the FritzboxLight entity."""
        super().__init__(coordinator, ain, None)

        max_kelvin = int(max(supported_color_temps))
        min_kelvin = int(min(supported_color_temps))

        # max kelvin is min mireds and min kelvin is max mireds
        self._attr_min_mireds = core.helpers.Color.temperature_kelvin_to_mired(
            max_kelvin
        )
        self._attr_max_mireds = core.helpers.Color.temperature_kelvin_to_mired(
            min_kelvin
        )

        # Fritz!DECT 500 only supports 12 values for hue, with 3 saturations each.
        # Map supported colors to dict {hue: [sat1, sat2, sat3]} for easier lookup
        self._supported_hs = {}
        for values in supported_colors.values():
            hue = int(values[0][0])
            self._supported_hs[hue] = [
                int(values[0][1]),
                int(values[1][1]),
                int(values[2][1]),
            ]

    @property
    def is_on(self) -> bool:
        """If the light is currently on or off."""
        return self.device.state

    @property
    def brightness(self) -> int:
        """Return the current Brightness."""
        return self.device.level

    @property
    def hs_color(self) -> tuple[float, float] | None:
        """Return the hs color value."""
        if self.device.color_mode != Const.COLOR_MODE:
            return None

        hue = self.device.hue
        saturation = self.device.saturation

        return (hue, float(saturation) * 100.0 / 255.0)

    @property
    def color_temp(self) -> int | None:
        """Return the CT color value."""
        if self.device.color_mode != Const.COLOR_TEMP_MODE:
            return None

        kelvin = self.device.color_temp
        return core.helpers.Color.temperature_kelvin_to_mired(kelvin)

    @property
    def color_mode(self) -> core.Light.ColorMode:
        """Return the color mode of the light."""
        if self.device.color_mode == Const.COLOR_MODE:
            return core.Light.ColorMode.HS
        return core.Light.ColorMode.COLOR_TEMP

    @property
    def supported_color_modes(self) -> set[core.Light.ColorMode]:
        """Flag supported color modes."""
        return _SUPPORTED_COLOR_MODES

    async def async_turn_on(self, **kwargs: typing.Any) -> None:
        """Turn the light on."""
        if kwargs.get(core.Light.ATTR_BRIGHTNESS) is not None:
            level = kwargs[core.Light.ATTR_BRIGHTNESS]
            await self._shc.async_add_executor_job(self.device.set_level, level)
        if kwargs.get(core.Light.ATTR_HS_COLOR) is not None:
            # Try setunmappedcolor first. This allows free color selection,
            # but we don't know if its supported by all devices.
            try:
                # HA gives 0..360 for hue, fritz light only supports 0..359
                unmapped_hue = int(kwargs[core.Light.ATTR_HS_COLOR][0] % 360)
                unmapped_saturation = round(
                    kwargs[core.Light.ATTR_HS_COLOR][1] * 255.0 / 100.0
                )
                await self._shc.async_add_executor_job(
                    self.device.set_unmapped_color, (unmapped_hue, unmapped_saturation)
                )
            # This will raise 400 BAD REQUEST if the setunmappedcolor is not available
            except requests.exceptions.HTTPError as err:
                if err.response.status_code != 400:
                    raise
                Const.LOGGER.debug(
                    "fritzbox does not support method 'setunmappedcolor', fallback to 'setcolor'"
                )
                # find supported hs values closest to what user selected
                hue = min(
                    self._supported_hs.keys(), key=lambda x: abs(x - unmapped_hue)
                )
                saturation = min(
                    self._supported_hs[hue],
                    key=lambda x: abs(x - unmapped_saturation),
                )
                await self._shc.async_add_executor_job(
                    self.device.set_color, (hue, saturation)
                )

        if kwargs.get(core.Light.ATTR_COLOR_TEMP) is not None:
            kelvin = core.helpers.Color.temperature_kelvin_to_mired(
                kwargs[core.Light.ATTR_COLOR_TEMP]
            )
            await self._shc.async_add_executor_job(self.device.set_color_temp, kelvin)

        await self._shc.async_add_executor_job(self.device.set_state_on)
        await self.coordinator.async_refresh()

    async def async_turn_off(self, **_kwargs: typing.Any) -> None:
        """Turn the light off."""
        await self._shc.async_add_executor_job(self.device.set_state_off)
        await self.coordinator.async_refresh()


# pylint: disable=unused-variable
async def async_setup_lights(
    owner: FritzboxIntegration,
    entry: core.ConfigEntry,
    async_add_entities: core.AddEntitiesCallback,
) -> None:
    """Set up the FRITZ!SmartHome light from ConfigEntry."""
    entities: list[FritzboxLight] = []
    coordinator = owner.connection_config[entry.entry_id][Const.CONF_COORDINATOR]

    for ain, device in coordinator.data.items():
        if not device.has_lightbulb:
            continue

        supported_color_temps = await owner.controller.async_add_executor_job(
            device.get_color_temps
        )

        supported_colors = await owner.controller.async_add_executor_job(
            device.get_colors
        )

        entities.append(
            FritzboxLight(
                coordinator,
                ain,
                supported_colors,
                supported_color_temps,
            )
        )

    async_add_entities(entities)
