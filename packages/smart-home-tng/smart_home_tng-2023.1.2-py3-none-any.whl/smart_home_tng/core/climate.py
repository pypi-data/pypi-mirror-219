"""
Core components of Smart Home - The Next Generation.

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

# pylint: disable=unused-variable

import dataclasses
import enum
import functools as ft
import typing

from ..backports import strenum
from .helpers import display_temp
from .const import Const
from .entity import Entity
from .entity_description import EntityDescription
from .service_call import ServiceCall
from .unit_conversion import TemperatureConverter

_DEFAULT_MIN_TEMP: typing.Final = 7
_DEFAULT_MAX_TEMP: typing.Final = 35
_DEFAULT_MIN_HUMIDITY: typing.Final = 30
_DEFAULT_MAX_HUMIDITY: typing.Final = 99

_ATTR_AUX_HEAT: typing.Final = "aux_heat"
_ATTR_CURRENT_HUMIDITY: typing.Final = "current_humidity"
_ATTR_CURRENT_TEMPERATURE: typing.Final = "current_temperature"
_ATTR_FAN_MODES: typing.Final = "fan_modes"
_ATTR_FAN_MODE: typing.Final = "fan_mode"
_ATTR_PRESET_MODE: typing.Final = "preset_mode"
_ATTR_PRESET_MODES: typing.Final = "preset_modes"
_ATTR_HUMIDITY: typing.Final = "humidity"
_ATTR_MAX_HUMIDITY: typing.Final = "max_humidity"
_ATTR_MIN_HUMIDITY: typing.Final = "min_humidity"
_ATTR_MAX_TEMP: typing.Final = "max_temp"
_ATTR_MIN_TEMP: typing.Final = "min_temp"
_ATTR_HVAC_ACTION: typing.Final = "hvac_action"
_ATTR_HVAC_MODES: typing.Final = "hvac_modes"
_ATTR_HVAC_MODE: typing.Final = "hvac_mode"
_ATTR_SWING_MODES: typing.Final = "swing_modes"
_ATTR_SWING_MODE: typing.Final = "swing_mode"
_ATTR_TARGET_TEMP_HIGH: typing.Final = "target_temp_high"
_ATTR_TARGET_TEMP_LOW: typing.Final = "target_temp_low"
_ATTR_TARGET_TEMP_STEP: typing.Final = "target_temp_step"
_CONVERTIBLE_ATTRIBUTE: typing.Final = [
    Const.ATTR_TEMPERATURE,
    _ATTR_TARGET_TEMP_LOW,
    _ATTR_TARGET_TEMP_HIGH,
]


@dataclasses.dataclass
class _EntityDescription(EntityDescription):
    """A class that describes climate entities."""


class _HVACMode(strenum.LowercaseStrEnum):
    """HVAC mode for climate devices."""

    # All activity disabled / Device is off/standby
    OFF = enum.auto()

    # Heating
    HEAT = enum.auto()

    # Cooling
    COOL = enum.auto()

    # The device supports heating/cooling to a range
    HEAT_COOL = enum.auto()

    # The temperature is set based on a schedule, learned behavior, AI or some
    # other related mechanism. User is not able to adjust the temperature
    AUTO = enum.auto()

    # Device is in Dry/Humidity mode
    DRY = enum.auto()

    # Only the fan is on, not fan and another mode like cool
    FAN_ONLY = enum.auto()


class _HVACAction(strenum.LowercaseStrEnum):
    """HVAC action for climate devices."""

    COOLING = enum.auto()
    DRYING = enum.auto()
    FAN = enum.auto()
    HEATING = enum.auto()
    IDLE = enum.auto()
    OFF = enum.auto()


class _EntityFeature(enum.IntEnum):
    """Supported features of the climate entity."""

    TARGET_TEMPERATURE = 1
    TARGET_TEMPERATURE_RANGE = 2
    TARGET_HUMIDITY = 4
    FAN_MODE = 8
    PRESET_MODE = 16
    SWING_MODE = 32
    AUX_HEAT = 64


_HVAC_MODES: typing.Final[list[str]] = [cls.value for cls in _HVACMode]


class _Entity(Entity):
    """Base class for climate entities."""

    _entity_description: _EntityDescription
    _attr_current_humidity: int = None
    _attr_current_temperature: float = None
    _attr_fan_mode: str
    _attr_fan_modes: list[str]
    _attr_hvac_action: _HVACAction | str = None
    _attr_hvac_mode: _HVACMode | str
    _attr_hvac_modes: list[_HVACMode] | list[str]
    _attr_is_aux_heat: bool
    _attr_max_humidity: int = _DEFAULT_MAX_HUMIDITY
    _attr_max_temp: float
    _attr_min_humidity: int = _DEFAULT_MIN_HUMIDITY
    _attr_min_temp: float
    _attr_precision: float
    _attr_preset_mode: str
    _attr_preset_modes: list[str]
    _attr_supported_features: int
    _attr_swing_mode: str
    _attr_swing_modes: list[str]
    _attr_target_humidity: int = None
    _attr_target_temperature_high: float
    _attr_target_temperature_low: float
    _attr_target_temperature_step: float = None
    _attr_target_temperature: float = None
    _attr_temperature_unit: str

    @typing.final
    @property
    def state(self) -> str:
        """Return the current state."""
        if self.hvac_mode is None:
            return None
        if not isinstance(self.hvac_mode, _HVACMode):
            return _HVACMode(self.hvac_mode).value
        return self.hvac_mode.value

    @property
    def precision(self) -> float:
        """Return the precision of the system."""
        if hasattr(self, "_attr_precision"):
            return self._attr_precision
        if self._shc.config.units.temperature_unit == Const.UnitOfTemperature.CELSIUS:
            return Const.PRECISION_TENTHS
        return Const.PRECISION_WHOLE

    @property
    def capability_attributes(self) -> dict[str, typing.Any]:
        """Return the capability attributes."""
        supported_features = self.supported_features
        data: dict[str, typing.Any] = {
            _ATTR_HVAC_MODES: self.hvac_modes,
            _ATTR_MIN_TEMP: display_temp(
                self._shc, self.min_temp, self.temperature_unit, self.precision
            ),
            _ATTR_MAX_TEMP: display_temp(
                self._shc, self.max_temp, self.temperature_unit, self.precision
            ),
        }

        if self.target_temperature_step:
            data[_ATTR_TARGET_TEMP_STEP] = self.target_temperature_step

        if supported_features & _EntityFeature.TARGET_HUMIDITY:
            data[_ATTR_MIN_HUMIDITY] = self.min_humidity
            data[_ATTR_MAX_HUMIDITY] = self.max_humidity

        if supported_features & _EntityFeature.FAN_MODE:
            data[_ATTR_FAN_MODES] = self.fan_modes

        if supported_features & _EntityFeature.PRESET_MODE:
            data[_ATTR_PRESET_MODES] = self.preset_modes

        if supported_features & _EntityFeature.SWING_MODE:
            data[_ATTR_SWING_MODES] = self.swing_modes

        return data

    @typing.final
    @property
    def state_attributes(self) -> dict[str, typing.Any]:
        """Return the optional state attributes."""
        supported_features = self.supported_features
        data: dict[str, str | float] = {
            _ATTR_CURRENT_TEMPERATURE: display_temp(
                self._shc,
                self.current_temperature,
                self.temperature_unit,
                self.precision,
            ),
        }

        if supported_features & _EntityFeature.TARGET_TEMPERATURE:
            data[Const.ATTR_TEMPERATURE] = display_temp(
                self._shc,
                self.target_temperature,
                self.temperature_unit,
                self.precision,
            )

        if supported_features & _EntityFeature.TARGET_TEMPERATURE_RANGE:
            data[_ATTR_TARGET_TEMP_HIGH] = display_temp(
                self._shc,
                self.target_temperature_high,
                self.temperature_unit,
                self.precision,
            )
            data[_ATTR_TARGET_TEMP_LOW] = display_temp(
                self._shc,
                self.target_temperature_low,
                self.temperature_unit,
                self.precision,
            )

        if self.current_humidity is not None:
            data[_ATTR_CURRENT_HUMIDITY] = self.current_humidity

        if supported_features & _EntityFeature.TARGET_HUMIDITY:
            data[_ATTR_HUMIDITY] = self.target_humidity

        if supported_features & _EntityFeature.FAN_MODE:
            data[_ATTR_FAN_MODE] = self.fan_mode

        if self.hvac_action:
            data[_ATTR_HVAC_ACTION] = self.hvac_action

        if supported_features & _EntityFeature.PRESET_MODE:
            data[_ATTR_PRESET_MODE] = self.preset_mode

        if supported_features & _EntityFeature.SWING_MODE:
            data[_ATTR_SWING_MODE] = self.swing_mode

        if supported_features & _EntityFeature.AUX_HEAT:
            data[_ATTR_AUX_HEAT] = (
                Const.STATE_ON if self.is_aux_heat else Const.STATE_OFF
            )

        return data

    @property
    def temperature_unit(self) -> str:
        """Return the unit of measurement used by the platform."""
        return self._attr_temperature_unit

    @property
    def current_humidity(self) -> int:
        """Return the current humidity."""
        return self._attr_current_humidity

    @property
    def target_humidity(self) -> int:
        """Return the humidity we try to reach."""
        return self._attr_target_humidity

    @property
    def hvac_mode(self) -> _HVACMode | str:
        """Return hvac operation ie. heat, cool mode."""
        return self._attr_hvac_mode

    @property
    def hvac_modes(self) -> list[_HVACMode] | list[str]:
        """Return the list of available hvac operation modes."""
        return self._attr_hvac_modes

    @property
    def hvac_action(self) -> _HVACAction | str:
        """Return the current running hvac operation if supported."""
        return self._attr_hvac_action

    @property
    def current_temperature(self) -> float:
        """Return the current temperature."""
        return self._attr_current_temperature

    @property
    def target_temperature(self) -> float:
        """Return the temperature we try to reach."""
        return self._attr_target_temperature

    @property
    def target_temperature_step(self) -> float:
        """Return the supported step of target temperature."""
        return self._attr_target_temperature_step

    @property
    def target_temperature_high(self) -> float:
        """Return the highbound target temperature we try to reach.

        Requires ClimateEntityFeature.TARGET_TEMPERATURE_RANGE.
        """
        return self._attr_target_temperature_high

    @property
    def target_temperature_low(self) -> float:
        """Return the lowbound target temperature we try to reach.

        Requires ClimateEntityFeature.TARGET_TEMPERATURE_RANGE.
        """
        return self._attr_target_temperature_low

    @property
    def preset_mode(self) -> str:
        """Return the current preset mode, e.g., home, away, temp.

        Requires ClimateEntityFeature.PRESET_MODE.
        """
        return self._attr_preset_mode

    @property
    def preset_modes(self) -> list[str]:
        """Return a list of available preset modes.

        Requires ClimateEntityFeature.PRESET_MODE.
        """
        return self._attr_preset_modes

    @property
    def is_aux_heat(self) -> bool:
        """Return true if aux heater.

        Requires ClimateEntityFeature.AUX_HEAT.
        """
        return self._attr_is_aux_heat

    @property
    def fan_mode(self) -> str:
        """Return the fan setting.

        Requires ClimateEntityFeature.FAN_MODE.
        """
        return self._attr_fan_mode

    @property
    def fan_modes(self) -> list[str]:
        """Return the list of available fan modes.

        Requires ClimateEntityFeature.FAN_MODE.
        """
        return self._attr_fan_modes

    @property
    def swing_mode(self) -> str:
        """Return the swing setting.

        Requires ClimateEntityFeature.SWING_MODE.
        """
        return self._attr_swing_mode

    @property
    def swing_modes(self) -> list[str]:
        """Return the list of available swing modes.

        Requires ClimateEntityFeature.SWING_MODE.
        """
        return self._attr_swing_modes

    def set_temperature(self, **kwargs) -> None:
        """Set new target temperature."""
        raise NotImplementedError()

    async def async_set_temperature(self, **kwargs) -> None:
        """Set new target temperature."""
        await self._shc.async_add_executor_job(
            ft.partial(self.set_temperature, **kwargs)
        )

    def set_humidity(self, humidity: int) -> None:
        """Set new target humidity."""
        raise NotImplementedError()

    async def async_set_humidity(self, humidity: int) -> None:
        """Set new target humidity."""
        await self._shc.async_add_executor_job(self.set_humidity, humidity)

    def set_fan_mode(self, fan_mode: str) -> None:
        """Set new target fan mode."""
        raise NotImplementedError()

    async def async_set_fan_mode(self, fan_mode: str) -> None:
        """Set new target fan mode."""
        await self._shc.async_add_executor_job(self.set_fan_mode, fan_mode)

    def set_hvac_mode(self, hvac_mode: _HVACMode) -> None:
        """Set new target hvac mode."""
        raise NotImplementedError()

    async def async_set_hvac_mode(self, hvac_mode: _HVACMode) -> None:
        """Set new target hvac mode."""
        await self._shc.async_add_executor_job(self.set_hvac_mode, hvac_mode)

    def set_swing_mode(self, swing_mode: str) -> None:
        """Set new target swing operation."""
        raise NotImplementedError()

    async def async_set_swing_mode(self, swing_mode: str) -> None:
        """Set new target swing operation."""
        await self._shc.async_add_executor_job(self.set_swing_mode, swing_mode)

    def set_preset_mode(self, preset_mode: str) -> None:
        """Set new preset mode."""
        raise NotImplementedError()

    async def async_set_preset_mode(self, preset_mode: str) -> None:
        """Set new preset mode."""
        await self._shc.async_add_executor_job(self.set_preset_mode, preset_mode)

    def turn_aux_heat_on(self) -> None:
        """Turn auxiliary heater on."""
        raise NotImplementedError()

    async def async_turn_aux_heat_on(self) -> None:
        """Turn auxiliary heater on."""
        await self._shc.async_add_executor_job(self.turn_aux_heat_on)

    def turn_aux_heat_off(self) -> None:
        """Turn auxiliary heater off."""
        raise NotImplementedError()

    async def async_turn_aux_heat_off(self) -> None:
        """Turn auxiliary heater off."""
        await self._shc.async_add_executor_job(self.turn_aux_heat_off)

    async def async_turn_on(self) -> None:
        """Turn the entity on."""
        if hasattr(self, "turn_on"):
            await self._shc.async_add_executor_job(self.turn_on)  # type: ignore[attr-defined]
            return

        # Fake turn on
        for mode in (_HVACMode.HEAT_COOL, _HVACMode.HEAT, _HVACMode.COOL):
            if mode not in self.hvac_modes:
                continue
            await self.async_set_hvac_mode(mode)
            break

    async def async_turn_off(self) -> None:
        """Turn the entity off."""
        if hasattr(self, "turn_off"):
            await self._shc.async_add_executor_job(self.turn_off)  # type: ignore[attr-defined]
            return

        # Fake turn off
        if _HVACMode.OFF in self.hvac_modes:
            await self.async_set_hvac_mode(_HVACMode.OFF)

    @property
    def supported_features(self) -> int:
        """Return the list of supported features."""
        return self._attr_supported_features

    @property
    def min_temp(self) -> float:
        """Return the minimum temperature."""
        if not hasattr(self, "_attr_min_temp"):
            return TemperatureConverter.convert(
                _DEFAULT_MIN_TEMP, Const.TEMP_CELSIUS, self.temperature_unit
            )
        return self._attr_min_temp

    @property
    def max_temp(self) -> float:
        """Return the maximum temperature."""
        if not hasattr(self, "_attr_max_temp"):
            return TemperatureConverter.convert(
                _DEFAULT_MAX_TEMP, Const.TEMP_CELSIUS, self.temperature_unit
            )
        return self._attr_max_temp

    @property
    def min_humidity(self) -> int:
        """Return the minimum humidity."""
        return self._attr_min_humidity

    @property
    def max_humidity(self) -> int:
        """Return the maximum humidity."""
        return self._attr_max_humidity


# pylint: disable=invalid-name
class Climate:
    """Provides functionality to interact with climate devices."""

    Entity: typing.TypeAlias = _Entity
    EntityDescription: typing.TypeAlias = _EntityDescription
    EntityFeature: typing.TypeAlias = _EntityFeature
    HVACMode: typing.TypeAlias = _HVACMode
    HVACAction: typing.TypeAlias = _HVACAction

    HVAC_MODES: typing.Final = _HVAC_MODES

    ATTR_AUX_HEAT: typing.Final = _ATTR_AUX_HEAT
    ATTR_CURRENT_HUMIDITY: typing.Final = _ATTR_CURRENT_HUMIDITY
    ATTR_CURRENT_TEMPERATURE: typing.Final = _ATTR_CURRENT_TEMPERATURE
    ATTR_FAN_MODES: typing.Final = _ATTR_FAN_MODES
    ATTR_FAN_MODE: typing.Final = _ATTR_FAN_MODE
    ATTR_PRESET_MODE: typing.Final = _ATTR_PRESET_MODE
    ATTR_PRESET_MODES: typing.Final = _ATTR_PRESET_MODES
    ATTR_HUMIDITY: typing.Final = _ATTR_HUMIDITY
    ATTR_MAX_HUMIDITY: typing.Final = _ATTR_MAX_HUMIDITY
    ATTR_MIN_HUMIDITY: typing.Final = _ATTR_MIN_HUMIDITY
    ATTR_MAX_TEMP: typing.Final = _ATTR_MAX_TEMP
    ATTR_MIN_TEMP: typing.Final = _ATTR_MIN_TEMP
    ATTR_HVAC_ACTION: typing.Final = _ATTR_HVAC_ACTION
    ATTR_HVAC_MODES: typing.Final = _ATTR_HVAC_MODES
    ATTR_HVAC_MODE: typing.Final = _ATTR_HVAC_MODE
    ATTR_SWING_MODES: typing.Final = _ATTR_SWING_MODES
    ATTR_SWING_MODE: typing.Final = _ATTR_SWING_MODE
    ATTR_TARGET_TEMP_HIGH: typing.Final = _ATTR_TARGET_TEMP_HIGH
    ATTR_TARGET_TEMP_LOW: typing.Final = _ATTR_TARGET_TEMP_LOW
    ATTR_TARGET_TEMP_STEP: typing.Final = _ATTR_TARGET_TEMP_STEP

    DEFAULT_MIN_TEMP: typing.Final = _DEFAULT_MIN_TEMP
    DEFAULT_MAX_TEMP: typing.Final = _DEFAULT_MAX_TEMP
    DEFAULT_MIN_HUMIDITY: typing.Final = _DEFAULT_MIN_HUMIDITY
    DEFAULT_MAX_HUMIDITY: typing.Final = _DEFAULT_MAX_HUMIDITY

    # No preset is active
    PRESET_NONE: typing.Final = "none"

    # Device is running an energy-saving mode
    PRESET_ECO: typing.Final = "eco"

    # Device is in away mode
    PRESET_AWAY: typing.Final = "away"

    # Device turn all valve full up
    PRESET_BOOST: typing.Final = "boost"

    # Device is in comfort mode
    PRESET_COMFORT: typing.Final = "comfort"

    # Device is in home mode
    PRESET_HOME: typing.Final = "home"

    # Device is prepared for sleep
    PRESET_SLEEP: typing.Final = "sleep"

    # Device is reacting to activity (e.g. movement sensors)
    PRESET_ACTIVITY: typing.Final = "activity"

    # Possible fan state
    FAN_ON: typing.Final = "on"
    FAN_OFF: typing.Final = "off"
    FAN_AUTO: typing.Final = "auto"
    FAN_LOW: typing.Final = "low"
    FAN_MEDIUM: typing.Final = "medium"
    FAN_HIGH: typing.Final = "high"
    FAN_TOP: typing.Final = "top"
    FAN_MIDDLE: typing.Final = "middle"
    FAN_FOCUS: typing.Final = "focus"
    FAN_DIFFUSE: typing.Final = "diffuse"

    # Possible swing state
    SWING_ON: typing.Final = "on"
    SWING_OFF: typing.Final = "off"
    SWING_BOTH: typing.Final = "both"
    SWING_VERTICAL: typing.Final = "vertical"
    SWING_HORIZONTAL: typing.Final = "horizontal"

    SERVICE_SET_AUX_HEAT: typing.Final = "set_aux_heat"
    SERVICE_SET_FAN_MODE: typing.Final = "set_fan_mode"
    SERVICE_SET_PRESET_MODE: typing.Final = "set_preset_mode"
    SERVICE_SET_HUMIDITY: typing.Final = "set_humidity"
    SERVICE_SET_HVAC_MODE: typing.Final = "set_hvac_mode"
    SERVICE_SET_SWING_MODE: typing.Final = "set_swing_mode"
    SERVICE_SET_TEMPERATURE: typing.Final = "set_temperature"

    @staticmethod
    async def async_service_aux_heat(entity: Entity, service_call: ServiceCall) -> None:
        """Handle aux heat service."""
        if service_call.data[_ATTR_AUX_HEAT]:
            await entity.async_turn_aux_heat_on()
        else:
            await entity.async_turn_aux_heat_off()

    @staticmethod
    async def async_service_temperature_set(
        entity: Entity, service_call: ServiceCall
    ) -> None:
        """Handle set temperature service."""
        shc = entity._shc  # pylint: disable=protected-access
        kwargs = {}

        for value, temp in service_call.data.items():
            if value in _CONVERTIBLE_ATTRIBUTE:
                kwargs[value] = TemperatureConverter.convert(
                    temp, shc.config.units.temperature_unit, entity.temperature_unit
                )
            else:
                kwargs[value] = temp

        await entity.async_set_temperature(**kwargs)
