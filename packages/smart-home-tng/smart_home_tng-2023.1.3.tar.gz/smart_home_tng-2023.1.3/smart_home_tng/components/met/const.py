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

import typing

from ... import core


# pylint: disable=unused-variable
class Const:
    """Constants for Met component."""

    HOME_LOCATION_NAME: typing.Final = "Home"

    CONF_TRACK_HOME: typing.Final = "track_home"

    DEFAULT_HOME_LATITUDE: typing.Final = 52.3731339
    DEFAULT_HOME_LONGITUDE: typing.Final = 4.8903147

    ENTITY_ID_SENSOR_FORMAT_HOME: typing.Final = (
        f"{core.Const.WEATHER_COMPONENT_NAME}.met_{HOME_LOCATION_NAME}"
    )

    CONDITIONS_MAP: typing.Final = {
        core.Const.ATTR_CONDITION_CLEAR_NIGHT: {"clearsky_night"},
        core.Const.ATTR_CONDITION_CLOUDY: {"cloudy_night", "cloudy_day", "cloudy"},
        core.Const.ATTR_CONDITION_FOG: {"fog", "fog_day", "fog_night"},
        core.Const.ATTR_CONDITION_LIGHTNING_RAINY: {
            "heavyrainandthunder",
            "heavyrainandthunder_day",
            "heavyrainandthunder_night",
            "heavyrainshowersandthunder",
            "heavyrainshowersandthunder_day",
            "heavyrainshowersandthunder_night",
            "heavysleetandthunder",
            "heavysleetandthunder_day",
            "heavysleetandthunder_night",
            "heavysleetshowersandthunder",
            "heavysleetshowersandthunder_day",
            "heavysleetshowersandthunder_night",
            "heavysnowandthunder",
            "heavysnowandthunder_day",
            "heavysnowandthunder_night",
            "heavysnowshowersandthunder",
            "heavysnowshowersandthunder_day",
            "heavysnowshowersandthunder_night",
            "lightrainandthunder",
            "lightrainandthunder_day",
            "lightrainandthunder_night",
            "lightrainshowersandthunder",
            "lightrainshowersandthunder_day",
            "lightrainshowersandthunder_night",
            "lightsleetandthunder",
            "lightsleetandthunder_day",
            "lightsleetandthunder_night",
            "lightsnowandthunder",
            "lightsnowandthunder_day",
            "lightsnowandthunder_night",
            "lightssleetshowersandthunder",
            "lightssleetshowersandthunder_day",
            "lightssleetshowersandthunder_night",
            "lightssnowshowersandthunder",
            "lightssnowshowersandthunder_day",
            "lightssnowshowersandthunder_night",
            "rainandthunder",
            "rainandthunder_day",
            "rainandthunder_night",
            "rainshowersandthunder",
            "rainshowersandthunder_day",
            "rainshowersandthunder_night",
            "sleetandthunder",
            "sleetandthunder_day",
            "sleetandthunder_night",
            "sleetshowersandthunder",
            "sleetshowersandthunder_day",
            "sleetshowersandthunder_night",
            "snowshowersandthunder",
            "snowshowersandthunder_day",
            "snowshowersandthunder_night",
        },
        core.Const.ATTR_CONDITION_PARTLYCLOUDY: {
            "fair",
            "fair_day",
            "fair_night",
            "partlycloudy",
            "partlycloudy_day",
            "partlycloudy_night",
        },
        core.Const.ATTR_CONDITION_POURING: {
            "heavyrain",
            "heavyrain_day",
            "heavyrain_night",
            "heavyrainshowers",
            "heavyrainshowers_day",
            "heavyrainshowers_night",
        },
        core.Const.ATTR_CONDITION_RAINY: {
            "lightrain",
            "lightrain_day",
            "lightrain_night",
            "lightrainshowers",
            "lightrainshowers_day",
            "lightrainshowers_night",
            "rain",
            "rain_day",
            "rain_night",
            "rainshowers",
            "rainshowers_day",
            "rainshowers_night",
        },
        core.Const.ATTR_CONDITION_SNOWY: {
            "heavysnow",
            "heavysnow_day",
            "heavysnow_night",
            "heavysnowshowers",
            "heavysnowshowers_day",
            "heavysnowshowers_night",
            "lightsnow",
            "lightsnow_day",
            "lightsnow_night",
            "lightsnowshowers",
            "lightsnowshowers_day",
            "lightsnowshowers_night",
            "snow",
            "snow_day",
            "snow_night",
            "snowandthunder",
            "snowandthunder_day",
            "snowandthunder_night",
            "snowshowers",
            "snowshowers_day",
            "snowshowers_night",
        },
        core.Const.ATTR_CONDITION_SNOWY_RAINY: {
            "heavysleet",
            "heavysleet_day",
            "heavysleet_night",
            "heavysleetshowers",
            "heavysleetshowers_day",
            "heavysleetshowers_night",
            "lightsleet",
            "lightsleet_day",
            "lightsleet_night",
            "lightsleetshowers",
            "lightsleetshowers_day",
            "lightsleetshowers_night",
            "sleet",
            "sleet_day",
            "sleet_night",
            "sleetshowers",
            "sleetshowers_day",
            "sleetshowers_night",
        },
        core.Const.ATTR_CONDITION_SUNNY: {"clearsky_day", "clearsky"},
    }

    FORECAST_MAP: typing.Final = {
        core.Const.ATTR_FORECAST_CONDITION: "condition",
        core.Const.ATTR_FORECAST_NATIVE_PRECIPITATION: "precipitation",
        core.Const.ATTR_FORECAST_PRECIPITATION_PROBABILITY: "precipitation_probability",
        core.Const.ATTR_FORECAST_NATIVE_TEMP: "temperature",
        core.Const.ATTR_FORECAST_NATIVE_TEMP_LOW: "templow",
        core.Const.ATTR_FORECAST_TIME: "datetime",
        core.Const.ATTR_FORECAST_WIND_BEARING: "wind_bearing",
        core.Const.ATTR_FORECAST_NATIVE_WIND_SPEED: "wind_speed",
    }

    ATTR_MAP: typing.Final = {
        core.Const.ATTR_WEATHER_HUMIDITY: "humidity",
        core.Const.ATTR_WEATHER_PRESSURE: "pressure",
        core.Const.ATTR_WEATHER_TEMPERATURE: "temperature",
        core.Const.ATTR_WEATHER_VISIBILITY: "visibility",
        core.Const.ATTR_WEATHER_WIND_BEARING: "wind_bearing",
        core.Const.ATTR_WEATHER_WIND_SPEED: "wind_speed",
    }
