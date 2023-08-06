"""
Met Integration for Smart Home - The Next Generation.

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

import types
import typing

from ... import core
from .const import Const
from .met_data_update_coordinator import MetDataUpdateCoordinator


_ATTRIBUTION: typing.Final = (
    "Weather forecast from met.no, delivered by the Norwegian "
    + "Meteorological Institute."
)
_DEFAULT_NAME: typing.Final = "Met.no"


# pylint: disable=unused-variable
class MetWeather(core.CoordinatorEntity[MetDataUpdateCoordinator], core.WeatherEntity):
    """Implementation of a Met.no weather condition."""

    _attr_has_entity_name = True
    _attr_native_temperature_unit = core.Const.UnitOfTemperature.CELSIUS
    _attr_native_precipitation_unit = core.Const.UnitOfLength.MILLIMETERS
    _attr_native_pressure_unit = core.Const.UnitOfPressure.HPA
    _attr_native_wind_speed_unit = core.Const.UnitOfSpeed.KILOMETERS_PER_HOUR

    def __init__(
        self,
        coordinator: MetDataUpdateCoordinator,
        config: types.MappingProxyType[str, typing.Any],
        is_metric: bool,
        hourly: bool,
    ) -> None:
        """Initialise the platform with a data instance and site."""
        super().__init__(coordinator)
        self._config = config
        self._is_metric = is_metric
        self._hourly = hourly
        self._shc = coordinator.owner.controller

    @property
    def owner(self) -> core.SmartHomeControllerComponent:
        return self.coordinator.owner

    @property
    def track_home(self) -> typing.Any | bool:
        """Return if we are tracking home."""
        return self._config.get(Const.CONF_TRACK_HOME, False)

    @property
    def unique_id(self) -> str:
        """Return unique ID."""
        name_appendix = ""
        if self._hourly:
            name_appendix = "-hourly"
        if self.track_home:
            return f"home{name_appendix}"

        return (
            f"{self._config[core.Const.CONF_LATITUDE]}-"
            + f"{self._config[core.Const.CONF_LONGITUDE]}{name_appendix}"
        )

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        name = self._config.get(core.Const.CONF_NAME)
        name_appendix = ""
        if self._hourly:
            name_appendix = " hourly"

        if name is not None:
            return f"{name}{name_appendix}"

        if self.track_home:
            return f"{self._shc.config.location_name}{name_appendix}"

        return f"{_DEFAULT_NAME}{name_appendix}"

    @property
    def entity_registry_enabled_default(self) -> bool:
        """Return if the entity should be enabled when first added to the entity registry."""
        return not self._hourly

    @property
    def condition(self) -> str:
        """Return the current condition."""
        condition = self.coordinator.data.current_weather_data.get("condition")
        if condition is None:
            return None
        return _format_condition(condition)

    @property
    def native_temperature(self) -> float:
        """Return the temperature."""
        return self.coordinator.data.current_weather_data.get(
            Const.ATTR_MAP[core.Const.ATTR_WEATHER_TEMPERATURE]
        )

    @property
    def native_pressure(self) -> float:
        """Return the pressure."""
        return self.coordinator.data.current_weather_data.get(
            Const.ATTR_MAP[core.Const.ATTR_WEATHER_PRESSURE]
        )

    @property
    def humidity(self) -> float:
        """Return the humidity."""
        return self.coordinator.data.current_weather_data.get(
            Const.ATTR_MAP[core.Const.ATTR_WEATHER_HUMIDITY]
        )

    @property
    def native_wind_speed(self) -> float:
        """Return the wind speed."""
        return self.coordinator.data.current_weather_data.get(
            Const.ATTR_MAP[core.Const.ATTR_WEATHER_WIND_SPEED]
        )

    @property
    def wind_bearing(self) -> float | str:
        """Return the wind direction."""
        return self.coordinator.data.current_weather_data.get(
            Const.ATTR_MAP[core.Const.ATTR_WEATHER_WIND_BEARING]
        )

    @property
    def attribution(self) -> str:
        """Return the attribution."""
        return _ATTRIBUTION

    @property
    def forecast(self) -> list[core.Forecast]:
        """Return the forecast array."""
        if self._hourly:
            met_forecast = self.coordinator.data.hourly_forecast
        else:
            met_forecast = self.coordinator.data.daily_forecast
        required_keys = {"temperature", core.Const.ATTR_FORECAST_TIME}
        forecast: list[core.Forecast] = []
        for met_item in met_forecast:
            if not set(met_item).issuperset(required_keys):
                continue
            item = {
                k: met_item[v]
                for k, v in Const.FORECAST_MAP.items()
                if met_item.get(v) is not None
            }
            if item.get(core.Const.ATTR_FORECAST_CONDITION):
                item[core.Const.ATTR_FORECAST_CONDITION] = _format_condition(
                    item[core.Const.ATTR_FORECAST_CONDITION]
                )
            forecast.append(item)
        return forecast

    @property
    def device_info(self) -> core.DeviceInfo:
        """Device info."""
        return core.DeviceInfo(
            default_name="Forecast",
            entry_type=core.DeviceRegistryEntryType.SERVICE,
            identifiers={(self.owner.domain,)},
            manufacturer="Met.no",
            model="Forecast",
            configuration_url="https://www.met.no/en",
        )


def _format_condition(condition: str) -> str:
    """Return condition from dict CONDITIONS_MAP."""
    for key, value in Const.CONDITIONS_MAP.items():
        if condition in value:
            return key
    return condition
