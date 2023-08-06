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

from ... import core
from .climate_extra_attributes import ClimateExtraAttributes
from .const import Const
from .fritzbox_entity import FritzboxEntity

if not typing.TYPE_CHECKING:

    class FritzboxIntegration:
        pass


if typing.TYPE_CHECKING:
    from .fritzbox_integration import FritzboxIntegration


_OPERATION_LIST: typing.Final = [core.Climate.HVACMode.HEAT, core.Climate.HVACMode.OFF]

_MIN_TEMPERATURE: typing.Final = 8
_MAX_TEMPERATURE: typing.Final = 28

# special temperatures for on/off in Fritz!Box API (modified by pyfritzhome)
_ON_API_TEMPERATURE: typing.Final = 127.0
_OFF_API_TEMPERATURE: typing.Final = 126.5
_ON_REPORT_SET_TEMPERATURE: typing.Final = 30.0
_OFF_REPORT_SET_TEMPERATURE: typing.Final = 0.0


class FritzboxThermostat(FritzboxEntity, core.Climate.Entity):
    """The thermostat class for FRITZ!SmartHome thermostats."""

    _attr_precision = core.Const.PRECISION_HALVES
    _attr_supported_features = (
        core.Climate.EntityFeature.TARGET_TEMPERATURE
        | core.Climate.EntityFeature.PRESET_MODE
    )
    _attr_temperature_unit = core.Const.UnitOfTemperature.CELSIUS

    @property
    def current_temperature(self) -> float:
        """Return the current temperature."""
        if self.device.has_temperature_sensor and self.device.temperature is not None:
            return self.device.temperature
        return self.device.actual_temperature

    @property
    def target_temperature(self) -> float:
        """Return the temperature we try to reach."""
        if self.device.target_temperature == _ON_API_TEMPERATURE:
            return _ON_REPORT_SET_TEMPERATURE
        if self.device.target_temperature == _OFF_API_TEMPERATURE:
            return _OFF_REPORT_SET_TEMPERATURE
        return self.device.target_temperature

    async def async_set_temperature(self, **kwargs: typing.Any) -> None:
        """Set new target temperature."""
        if kwargs.get(core.Climate.ATTR_HVAC_MODE) is not None:
            hvac_mode = kwargs[core.Climate.ATTR_HVAC_MODE]
            await self.async_set_hvac_mode(hvac_mode)
        elif kwargs.get(core.Const.ATTR_TEMPERATURE) is not None:
            temperature = kwargs[core.Const.ATTR_TEMPERATURE]
            await self._shc.async_add_executor_job(
                self.device.set_target_temperature, temperature
            )
        await self.coordinator.async_refresh()

    @property
    def hvac_mode(self) -> str:
        """Return the current operation mode."""
        if self.device.target_temperature in (
            _OFF_REPORT_SET_TEMPERATURE,
            _OFF_API_TEMPERATURE,
        ):
            return core.Climate.HVACMode.OFF

        return core.Climate.HVACMode.HEAT

    @property
    def hvac_modes(self) -> list[core.Climate.HVACMode]:
        """Return the list of available operation modes."""
        return _OPERATION_LIST

    async def async_set_hvac_mode(self, hvac_mode: core.Climate.HVACMode) -> None:
        """Set new operation mode."""
        if hvac_mode == core.Climate.HVACMode.OFF:
            await self.async_set_temperature(temperature=_OFF_REPORT_SET_TEMPERATURE)
        else:
            await self.async_set_temperature(
                temperature=self.device.comfort_temperature
            )

    @property
    def preset_mode(self) -> str:
        """Return current preset mode."""
        if self.device.target_temperature == self.device.comfort_temperature:
            return core.Climate.PRESET_COMFORT
        if self.device.target_temperature == self.device.eco_temperature:
            return core.Climate.PRESET_ECO
        return None

    @property
    def preset_modes(self) -> list[str]:
        """Return supported preset modes."""
        return [core.Climate.PRESET_ECO, core.Climate.PRESET_COMFORT]

    async def async_set_preset_mode(self, preset_mode: str) -> None:
        """Set preset mode."""
        if preset_mode == core.Climate.PRESET_COMFORT:
            await self.async_set_temperature(
                temperature=self.device.comfort_temperature
            )
        elif preset_mode == core.Climate.PRESET_ECO:
            await self.async_set_temperature(temperature=self.device.eco_temperature)

    @property
    def min_temp(self) -> int:
        """Return the minimum temperature."""
        return _MIN_TEMPERATURE

    @property
    def max_temp(self) -> int:
        """Return the maximum temperature."""
        return _MAX_TEMPERATURE

    @property
    def extra_state_attributes(self) -> ClimateExtraAttributes:
        """Return the device specific state attributes."""
        attrs: ClimateExtraAttributes = {
            Const.ATTR_STATE_BATTERY_LOW: self.device.battery_low,
        }

        # the following attributes are available since fritzos 7
        if self.device.battery_level is not None:
            attrs[Const.ATTR_BATTERY_LEVEL] = self.device.battery_level
        if self.device.holiday_active is not None:
            attrs[Const.ATTR_STATE_HOLIDAY_MODE] = self.device.holiday_active
        if self.device.summer_active is not None:
            attrs[Const.ATTR_STATE_SUMMER_MODE] = self.device.summer_active
        if self.device.window_open is not None:
            attrs[Const.ATTR_STATE_WINDOW_OPEN] = self.device.window_open

        return attrs


# pylint: disable=unused-variable
async def async_setup_thermostats(
    owner: FritzboxIntegration,
    entry: core.ConfigEntry,
    async_add_entities: core.AddEntitiesCallback,
) -> None:
    """Set up the FRITZ!SmartHome thermostat from ConfigEntry."""
    coordinator = owner.connection_config[entry.entry_id][Const.CONF_COORDINATOR]

    async_add_entities(
        [
            FritzboxThermostat(coordinator, ain)
            for ain, device in coordinator.data.items()
            if device.has_thermostat
        ]
    )
