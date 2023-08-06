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

import metno

from ... import core
from .cannot_connect import CannotConnect
from .const import Const

# Dedicated Home Assistant endpoint - do not change!
_URL: typing.Final = (
    "https://aa015h6buqvih86i1.api.met.no/weatherapi/locationforecast/2.0/complete"
)


# pylint: disable=unused-variable
class MetWeatherData:
    """Keep data for Met.no weather entities."""

    def __init__(
        self,
        shc: core.SmartHomeController,
        config: types.MappingProxyType[str, typing.Any],
        is_metric: bool,
    ) -> None:
        """Initialise the weather entity data."""
        self._shc = shc
        self._config = config
        self._is_metric = is_metric
        self._weather_data: metno.MetWeatherData
        self._current_weather_data: dict = {}
        self._daily_forecast: list[dict] = []
        self._hourly_forecast: list[dict] = []
        self._coordinates: dict[str, str] = None

    @property
    def current_weather_data(self) -> dict:
        return self._current_weather_data

    @property
    def daily_forecast(self) -> list[dict]:
        return self._daily_forecast

    @property
    def hourly_forecast(self) -> list[dict]:
        return self._hourly_forecast

    def set_coordinates(self) -> bool:
        """Weather data inialization - set the coordinates."""
        if self._config.get(Const.CONF_TRACK_HOME, False):
            latitude = self._shc.config.latitude
            longitude = self._shc.config.longitude
            elevation = self._shc.config.elevation
        else:
            latitude = self._config[core.Const.CONF_LATITUDE]
            longitude = self._config[core.Const.CONF_LONGITUDE]
            elevation = self._config[core.Const.CONF_ELEVATION]

        if not self._is_metric:
            elevation = int(
                round(
                    core.DistanceConverter.convert(
                        elevation,
                        core.Const.UnitOfLength.FEET,
                        core.Const.UnitOfLength.METERS,
                    )
                )
            )

        coordinates = {
            "lat": str(latitude),
            "lon": str(longitude),
            "msl": str(elevation),
        }
        if coordinates == self._coordinates:
            return False
        self._coordinates = coordinates

        self._weather_data = metno.MetWeatherData(
            coordinates,
            core.HttpClient.async_get_clientsession(self._shc),
            api_url=_URL,
        )
        return True

    async def fetch_data(self):
        """Fetch data from API - (current weather and forecast)."""
        resp = await self._weather_data.fetching_data()
        if not resp:
            raise CannotConnect()
        self._current_weather_data = self._weather_data.get_current_weather()
        time_zone = core.helpers.get_default_time_zone()
        self._daily_forecast = self._weather_data.get_forecast(time_zone, False)
        self._hourly_forecast = self._weather_data.get_forecast(time_zone, True)
        return self
