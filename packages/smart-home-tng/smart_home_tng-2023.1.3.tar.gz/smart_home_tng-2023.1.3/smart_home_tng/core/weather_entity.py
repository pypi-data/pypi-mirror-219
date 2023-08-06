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

import contextlib
import inspect
import logging
import typing

from .callback import callback
from .const import Const
from .entity import Entity
from .forecast import Forecast
from .platform import Platform
from .unit_conversion import (
    DistanceConverter,
    PressureConverter,
    SpeedConverter,
    TemperatureConverter,
)
from .unit_system import UnitSystem
from .weather_entity_description import WeatherEntityDescription

_LOGGER: typing.Final = logging.getLogger(__name__)
_ROUNDING_PRECISION: typing.Final = 2


# pylint: disable=unused-variable
class WeatherEntity(Entity):
    """ABC for weather data."""

    _entity_description: WeatherEntityDescription
    _attr_condition: str
    _attr_forecast: list[Forecast] = None
    _attr_humidity: float = None
    _attr_ozone: float = None
    _attr_precision: float
    _attr_state: None = None
    _attr_wind_bearing: float | str = None

    _attr_native_pressure: float = None
    _attr_native_pressure_unit: str = None
    _attr_native_temperature: float = None
    _attr_native_temperature_unit: str = None
    _attr_native_visibility: float = None
    _attr_native_visibility_unit: str = None
    _attr_native_precipitation_unit: str = None
    _attr_native_wind_speed: float = None
    _attr_native_wind_speed_unit: str = None

    _weather_option_temperature_unit: str = None
    _weather_option_pressure_unit: str = None
    _weather_option_visibility_unit: str = None
    _weather_option_precipitation_unit: str = None
    _weather_option_wind_speed_unit: str = None

    def __init_subclass__(cls, **kwargs: typing.Any) -> None:
        """Post initialisation processing."""
        super().__init_subclass__(**kwargs)
        _reported = False
        if any(
            method in cls.__dict__
            for method in (
                "_attr_temperature",
                "temperature",
                "_attr_temperature_unit",
                "temperature_unit",
                "_attr_pressure",
                "pressure",
                "_attr_pressure_unit",
                "pressure_unit",
                "_attr_wind_speed",
                "wind_speed",
                "_attr_wind_speed_unit",
                "wind_speed_unit",
                "_attr_visibility",
                "visibility",
                "_attr_visibility_unit",
                "visibility_unit",
                "_attr_precipitation_unit",
                "precipitation_unit",
            )
        ):
            if _reported is False:
                module = inspect.getmodule(cls)
                _reported = True
                if (
                    module
                    and module.__file__
                    and "custom_components" in module.__file__
                ):
                    report_issue = "report it to the custom integration author."
                else:
                    report_issue = (
                        "create a bug report at "
                        + "https://github.com/home-assistant/core/issues?q=is%3Aopen+"
                        + "is%3Aissue"
                    )
                _LOGGER.warning(
                    f"{cls.__module__}::{cls.__name__} is overriding deprecated methods"
                    + " on an instance of WeatherEntity, this is not valid and will be "
                    + f"unsupported from Home Assistant 2023.1. Please {report_issue}",
                )

    async def async_internal_added_to_shc(self) -> None:
        """Call when the sensor entity is added to hass."""
        await super().async_internal_added_to_shc()
        if not self.registry_entry:
            return
        self.async_registry_entry_updated()

    @property
    def native_temperature(self) -> float:
        """Return the temperature in native units."""
        return self._attr_native_temperature

    @property
    def native_temperature_unit(self) -> str:
        """Return the native unit of measurement for temperature."""

        return self._attr_native_temperature_unit

    @typing.final
    @property
    def _default_temperature_unit(self) -> str:
        """Return the default unit of measurement for temperature.

        Should not be set by integrations.
        """
        return self._shc.config.units.temperature_unit

    @typing.final
    @property
    def _temperature_unit(self) -> str:
        """Return the converted unit of measurement for temperature.

        Should not be set by integrations.
        """
        if (
            weather_option_temperature_unit := self._weather_option_temperature_unit
        ) is not None:
            return weather_option_temperature_unit

        return self._default_temperature_unit

    @property
    def native_pressure(self) -> float:
        """Return the pressure in native units."""
        return self._attr_native_pressure

    @property
    def native_pressure_unit(self) -> str:
        """Return the native unit of measurement for pressure."""
        return self._attr_native_pressure_unit

    @typing.final
    @property
    def _default_pressure_unit(self) -> str:
        """Return the default unit of measurement for pressure.

        Should not be set by integrations.
        """
        return self._shc.config.units.pressure_unit

    @typing.final
    @property
    def _pressure_unit(self) -> str:
        """Return the converted unit of measurement for pressure.

        Should not be set by integrations.
        """
        if (
            weather_option_pressure_unit := self._weather_option_pressure_unit
        ) is not None:
            return weather_option_pressure_unit

        return self._default_pressure_unit

    @property
    def humidity(self) -> float:
        """Return the humidity in native units."""
        return self._attr_humidity

    @property
    def native_wind_speed(self) -> float:
        """Return the wind speed in native units."""
        return self._attr_native_wind_speed

    @property
    def native_wind_speed_unit(self) -> str:
        """Return the native unit of measurement for wind speed."""
        return self._attr_native_wind_speed_unit

    @typing.final
    @property
    def _default_wind_speed_unit(self) -> str:
        """Return the default unit of measurement for wind speed.

        Should not be set by integrations.
        """
        return (
            Const.UnitOfSpeed.KILOMETERS_PER_HOUR
            if self._shc.config.units.is_metric
            else Const.UnitOfSpeed.MILES_PER_HOUR
        )

    @typing.final
    @property
    def _wind_speed_unit(self) -> str:
        """Return the converted unit of measurement for wind speed.

        Should not be set by integrations.
        """
        if (
            weather_option_wind_speed_unit := self._weather_option_wind_speed_unit
        ) is not None:
            return weather_option_wind_speed_unit

        return self._default_wind_speed_unit

    @property
    def wind_bearing(self) -> float | str:
        """Return the wind bearing."""
        return self._attr_wind_bearing

    @property
    def ozone(self) -> float:
        """Return the ozone level."""
        return self._attr_ozone

    @property
    def native_visibility(self) -> float:
        """Return the visibility in native units."""
        return self._attr_native_visibility

    @property
    def native_visibility_unit(self) -> str:
        """Return the native unit of measurement for visibility."""
        return self._attr_native_visibility_unit

    @typing.final
    @property
    def _default_visibility_unit(self) -> str:
        """Return the default unit of measurement for visibility.

        Should not be set by integrations.
        """
        return self._shc.config.units.length_unit

    @typing.final
    @property
    def _visibility_unit(self) -> str:
        """Return the converted unit of measurement for visibility.

        Should not be set by integrations.
        """
        if (
            weather_option_visibility_unit := self._weather_option_visibility_unit
        ) is not None:
            return weather_option_visibility_unit

        return self._default_visibility_unit

    @property
    def forecast(self) -> list[Forecast]:
        """Return the forecast in native units."""
        return self._attr_forecast

    @property
    def native_precipitation_unit(self) -> str:
        """Return the native unit of measurement for accumulated precipitation."""
        return self._attr_native_precipitation_unit

    @typing.final
    @property
    def _default_precipitation_unit(self) -> str:
        """Return the default unit of measurement for precipitation.

        Should not be set by integrations.
        """
        return self._shc.config.units.accumulated_precipitation_unit

    @typing.final
    @property
    def _precipitation_unit(self) -> str:
        """Return the converted unit of measurement for precipitation.

        Should not be set by integrations.
        """
        if (
            weather_option_precipitation_unit := self._weather_option_precipitation_unit
        ) is not None:
            return weather_option_precipitation_unit

        return self._default_precipitation_unit

    @property
    def precision(self) -> float:
        """Return the precision of the temperature value, after unit conversion."""
        if hasattr(self, "_attr_precision"):
            return self._attr_precision
        return (
            Const.PRECISION_TENTHS
            if self._temperature_unit == Const.UnitOfTemperature.CELSIUS
            else Const.PRECISION_WHOLE
        )

    @typing.final
    @property
    def state_attributes(self):
        """Return the state attributes, converted from native units to user-configured units."""
        data = {}

        precision = self.precision
        temp_from_unit = self.native_temperature_unit or self._default_temperature_unit
        temp_to_unit = self._temperature_unit
        pressure_from_unit = self.native_pressure_unit or self._default_pressure_unit
        pressure_to_unit = self._pressure_unit
        wind_from_unit = self.native_wind_speed_unit or self._default_wind_speed_unit
        wind_to_unit = self._wind_speed_unit
        visibility_from_unit = (
            self.native_visibility_unit or self._default_visibility_unit
        )
        visibility_to_unit = self._visibility_unit
        precipitation_from_unit = (
            self.native_precipitation_unit or self._default_precipitation_unit
        )
        precipitation_to_unit = self._precipitation_unit

        if (temperature := self.native_temperature) is not None:
            try:
                temperature_f = float(temperature)
                value_temp = TemperatureConverter.convert(
                    temperature_f, temp_from_unit, temp_to_unit
                )
                data[Const.ATTR_WEATHER_TEMPERATURE] = round_temperature(
                    value_temp, precision
                )
            except (TypeError, ValueError):
                data[Const.ATTR_WEATHER_TEMPERATURE] = temperature

        data[Const.ATTR_WEATHER_TEMPERATURE_UNIT] = self._temperature_unit

        if (humidity := self.humidity) is not None:
            data[Const.ATTR_WEATHER_HUMIDITY] = round(humidity)

        if (ozone := self.ozone) is not None:
            data[Const.ATTR_WEATHER_OZONE] = ozone

        if (pressure := self.native_pressure) is not None:
            try:
                pressure_f = float(pressure)
                value_pressure = PressureConverter.convert(
                    pressure_f, pressure_from_unit, pressure_to_unit
                )
                data[Const.ATTR_WEATHER_PRESSURE] = round(
                    value_pressure, _ROUNDING_PRECISION
                )
            except (TypeError, ValueError):
                data[Const.ATTR_WEATHER_PRESSURE] = pressure

        data[Const.ATTR_WEATHER_PRESSURE_UNIT] = self._pressure_unit

        if (wind_bearing := self.wind_bearing) is not None:
            data[Const.ATTR_WEATHER_WIND_BEARING] = wind_bearing

        if (wind_speed := self.native_wind_speed) is not None:
            try:
                wind_speed_f = float(wind_speed)
                value_wind_speed = SpeedConverter.convert(
                    wind_speed_f, wind_from_unit, wind_to_unit
                )
                data[Const.ATTR_WEATHER_WIND_SPEED] = round(
                    value_wind_speed, _ROUNDING_PRECISION
                )
            except (TypeError, ValueError):
                data[Const.ATTR_WEATHER_WIND_SPEED] = wind_speed

        data[Const.ATTR_WEATHER_WIND_SPEED_UNIT] = self._wind_speed_unit

        if (visibility := self.native_visibility) is not None:
            try:
                visibility_f = float(visibility)
                value_visibility = DistanceConverter.convert(
                    visibility_f, visibility_from_unit, visibility_to_unit
                )
                data[Const.ATTR_WEATHER_VISIBILITY] = round(
                    value_visibility, _ROUNDING_PRECISION
                )
            except (TypeError, ValueError):
                data[Const.ATTR_WEATHER_VISIBILITY] = visibility

        data[Const.ATTR_WEATHER_VISIBILITY_UNIT] = self._visibility_unit
        data[Const.ATTR_WEATHER_PRECIPITATION_UNIT] = self._precipitation_unit

        if self.forecast is not None:
            forecast = []
            for forecast_entry in self.forecast:
                forecast_entry = dict(forecast_entry)

                temperature = forecast_entry.pop(
                    Const.ATTR_FORECAST_NATIVE_TEMP,
                    forecast_entry.get(Const.ATTR_FORECAST_TEMP),
                )

                if temperature is not None:
                    with contextlib.suppress(TypeError, ValueError):
                        temperature_f = float(temperature)
                        value_temp = TemperatureConverter.convert(
                            temperature_f,
                            temp_from_unit,
                            temp_to_unit,
                        )
                        forecast_entry[Const.ATTR_FORECAST_TEMP] = round_temperature(
                            value_temp, precision
                        )

                if (
                    forecast_temp_low := forecast_entry.pop(
                        Const.ATTR_FORECAST_NATIVE_TEMP_LOW,
                        forecast_entry.get(Const.ATTR_FORECAST_TEMP_LOW),
                    )
                ) is not None:
                    with contextlib.suppress(TypeError, ValueError):
                        forecast_temp_low_f = float(forecast_temp_low)
                        value_temp_low = TemperatureConverter.convert(
                            forecast_temp_low_f,
                            temp_from_unit,
                            temp_to_unit,
                        )

                        forecast_entry[
                            Const.ATTR_FORECAST_TEMP_LOW
                        ] = round_temperature(value_temp_low, precision)

                if (
                    forecast_pressure := forecast_entry.pop(
                        Const.ATTR_FORECAST_NATIVE_PRESSURE,
                        forecast_entry.get(Const.ATTR_FORECAST_PRESSURE),
                    )
                ) is not None:
                    with contextlib.suppress(TypeError, ValueError):
                        forecast_pressure_f = float(forecast_pressure)
                        forecast_entry[Const.ATTR_FORECAST_PRESSURE] = round(
                            PressureConverter.convert(
                                forecast_pressure_f,
                                pressure_from_unit,
                                pressure_to_unit,
                            ),
                            _ROUNDING_PRECISION,
                        )

                if (
                    forecast_wind_speed := forecast_entry.pop(
                        Const.ATTR_FORECAST_NATIVE_WIND_SPEED,
                        forecast_entry.get(Const.ATTR_FORECAST_WIND_SPEED),
                    )
                ) is not None:
                    with contextlib.suppress(TypeError, ValueError):
                        forecast_wind_speed_f = float(forecast_wind_speed)
                        forecast_entry[Const.ATTR_FORECAST_WIND_SPEED] = round(
                            SpeedConverter.convert(
                                forecast_wind_speed_f,
                                wind_from_unit,
                                wind_to_unit,
                            ),
                            _ROUNDING_PRECISION,
                        )

                if (
                    forecast_precipitation := forecast_entry.pop(
                        Const.ATTR_FORECAST_NATIVE_PRECIPITATION,
                        forecast_entry.get(Const.ATTR_FORECAST_PRECIPITATION),
                    )
                ) is not None:
                    with contextlib.suppress(TypeError, ValueError):
                        forecast_precipitation_f = float(forecast_precipitation)
                        forecast_entry[Const.ATTR_FORECAST_PRECIPITATION] = round(
                            DistanceConverter.convert(
                                forecast_precipitation_f,
                                precipitation_from_unit,
                                precipitation_to_unit,
                            ),
                            _ROUNDING_PRECISION,
                        )

                forecast.append(forecast_entry)

            data[Const.ATTR_FORECAST] = forecast

        return data

    @property
    @typing.final
    def state(self) -> str:
        """Return the current state."""
        return self.condition

    @property
    def condition(self) -> str:
        """Return the current condition."""
        return self._attr_condition

    @callback
    def async_registry_entry_updated(self) -> None:
        """Run when the entity registry entry has been updated."""
        assert self.registry_entry
        self._weather_option_temperature_unit = None
        self._weather_option_pressure_unit = None
        self._weather_option_precipitation_unit = None
        self._weather_option_wind_speed_unit = None
        self._weather_option_visibility_unit = None
        if weather_options := self.registry_entry.options.get(Platform.WEATHER.value):
            if (
                custom_unit_temperature := weather_options.get(
                    Const.ATTR_WEATHER_TEMPERATURE_UNIT
                )
            ) and UnitSystem.is_valid_unit(custom_unit_temperature, Const.TEMPERATURE):
                self._weather_option_temperature_unit = custom_unit_temperature
            if (
                custom_unit_pressure := weather_options.get(
                    Const.ATTR_WEATHER_PRESSURE_UNIT
                )
            ) and UnitSystem.is_valid_unit(custom_unit_pressure, Const.PRESSURE):
                self._weather_option_pressure_unit = custom_unit_pressure
            if (
                custom_unit_precipitation := weather_options.get(
                    Const.ATTR_WEATHER_PRECIPITATION_UNIT
                )
            ) and UnitSystem.is_valid_unit(custom_unit_precipitation, Const.LENGTH):
                self._weather_option_precipitation_unit = custom_unit_precipitation
            if (
                custom_unit_wind_speed := weather_options.get(
                    Const.ATTR_WEATHER_WIND_SPEED_UNIT
                )
            ) and UnitSystem.is_valid_unit(custom_unit_wind_speed, Const.SPEED):
                self._weather_option_wind_speed_unit = custom_unit_wind_speed
            if (
                custom_unit_visibility := weather_options.get(
                    Const.ATTR_WEATHER_VISIBILITY_UNIT
                )
            ) and UnitSystem.is_valid_unit(custom_unit_visibility, Const.LENGTH):
                self._weather_option_visibility_unit = custom_unit_visibility


def round_temperature(temperature: float, precision: float) -> float:
    """Convert temperature into preferred precision for display."""
    if temperature is None:
        return None

    # Round in the units appropriate
    if precision == Const.PRECISION_HALVES:
        temperature = round(temperature * 2) / 2.0
    elif precision == Const.PRECISION_TENTHS:
        temperature = round(temperature, 1)
    # Integer as a fall back (PRECISION_WHOLE)
    else:
        temperature = round(temperature)

    return temperature
