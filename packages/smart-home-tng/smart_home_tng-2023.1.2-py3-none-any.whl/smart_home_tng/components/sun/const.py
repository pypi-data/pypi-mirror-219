"""
Sun Component for Smart Home - The Next Generation.

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


# pylint: disable=unused-variable
class Const:
    """Constants for the Sun Component."""

    DEFAULT_NAME: typing.Final = "Sun"
    ENTITY_ID: typing.Final = "sun.sun"

    STATE_ABOVE_HORIZON: typing.Final = "above_horizon"
    STATE_BELOW_HORIZON: typing.Final = "below_horizon"

    STATE_ATTR_AZIMUTH: typing.Final = "azimuth"
    STATE_ATTR_ELEVATION: typing.Final = "elevation"
    STATE_ATTR_RISING: typing.Final = "rising"
    STATE_ATTR_NEXT_DAWN: typing.Final = "next_dawn"
    STATE_ATTR_NEXT_DUSK: typing.Final = "next_dusk"
    STATE_ATTR_NEXT_MIDNIGHT: typing.Final = "next_midnight"
    STATE_ATTR_NEXT_NOON: typing.Final = "next_noon"
    STATE_ATTR_NEXT_RISING: typing.Final = "next_rising"
    STATE_ATTR_NEXT_SETTING: typing.Final = "next_setting"

    # The algorithm used here is somewhat complicated. It aims to cut down
    # the number of sensor updates over the day. It's documented best in
    # the PR for the change, see the Discussion section of:
    # https://github.com/home-assistant/core/pull/23832

    # As documented in wikipedia: https://en.wikipedia.org/wiki/Twilight
    # sun is:
    # < -18° of horizon - all stars visible
    PHASE_NIGHT: typing.Final = "night"
    # 18°-12° - some stars not visible
    PHASE_ASTRONOMICAL_TWILIGHT: typing.Final = "astronomical_twilight"
    # 12°-6° - horizon visible
    PHASE_NAUTICAL_TWILIGHT: typing.Final = "nautical_twilight"
    # 6°-0° - objects visible
    PHASE_TWILIGHT: typing.Final = "twilight"
    # 0°-10° above horizon, sun low on horizon
    PHASE_SMALL_DAY: typing.Final = "small_day"
    # > 10° above horizon
    PHASE_DAY: typing.Final = "day"
