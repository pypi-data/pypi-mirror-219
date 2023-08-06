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

import collections.abc
import datetime
import typing

import astral
import astral.location

from . import helpers
from .callback import callback
from .const import Const


if not typing.TYPE_CHECKING:

    class SmartHomeController:
        ...


if typing.TYPE_CHECKING:
    from .smart_home_controller import SmartHomeController


_DATA_LOCATION_CACHE: typing.Final = "astral_location_cache"
_ELEVATION_AGNOSTIC_EVENTS: typing.Final = ("noon", "midnight")
_AstralSunEventCallable: typing.TypeAlias = collections.abc.Callable[
    ..., datetime.datetime
]


# pylint: disable=unused-variable
class Sun:
    """Helpers for sun events."""

    def __init__(self, shc: SmartHomeController):
        self._shc = shc

    @callback
    def get_astral_location(self) -> tuple[astral.location.Location, astral.Elevation]:
        """Get an astral location for the current Home Assistant configuration."""

        latitude = self._shc.config.latitude
        longitude = self._shc.config.longitude
        timezone = str(self._shc.config.time_zone)
        elevation = self._shc.config.elevation
        info = ("", "", timezone, latitude, longitude)

        # Cache astral locations so they aren't recreated with the same args
        if _DATA_LOCATION_CACHE not in self._shc.data:
            self._shc.data[_DATA_LOCATION_CACHE] = {}

        if info not in self._shc.data[_DATA_LOCATION_CACHE]:
            self._shc.data[_DATA_LOCATION_CACHE][info] = astral.location.Location(
                astral.LocationInfo(*info)
            )

        return self._shc.data[_DATA_LOCATION_CACHE][info], elevation

    @callback
    def get_astral_event_next(
        self,
        event: str,
        utc_point_in_time: datetime.datetime = None,
        offset: datetime.timedelta = None,
    ) -> datetime.datetime:
        """Calculate the next specified solar event."""
        location, elevation = self.get_astral_location()
        return self.get_location_astral_event_next(
            location, elevation, event, utc_point_in_time, offset
        )

    @staticmethod
    @callback
    def get_location_astral_event_next(
        location: astral.location.Location,
        elevation: astral.Elevation,
        event: str,
        utc_point_in_time: datetime.datetime = None,
        offset: datetime.timedelta = None,
    ) -> datetime.datetime:
        """Calculate the next specified solar event."""

        if offset is None:
            offset = datetime.timedelta()

        if utc_point_in_time is None:
            utc_point_in_time = helpers.utcnow()

        kwargs: dict[str, typing.Any] = {"local": False}
        if event not in _ELEVATION_AGNOSTIC_EVENTS:
            kwargs["observer_elevation"] = elevation

        mod = -1
        while True:
            try:
                next_dt = (
                    typing.cast(_AstralSunEventCallable, getattr(location, event))(
                        helpers.as_local(utc_point_in_time).date()
                        + datetime.timedelta(days=mod),
                        **kwargs,
                    )
                    + offset
                )
                if next_dt > utc_point_in_time:
                    return next_dt
            except ValueError:
                pass
            mod += 1

    @callback
    def get_astral_event_date(
        self,
        event: str,
        date: datetime.date | datetime.datetime = None,
    ) -> datetime.datetime:
        """Calculate the astral event time for the specified date."""
        location, elevation = self.get_astral_location()

        if date is None:
            date = helpers.now().date()

        if isinstance(date, datetime.datetime):
            date = helpers.as_local(date).date()

        kwargs: dict[str, typing.Any] = {"local": False}
        if event not in _ELEVATION_AGNOSTIC_EVENTS:
            kwargs["observer_elevation"] = elevation

        try:
            return typing.cast(_AstralSunEventCallable, getattr(location, event))(
                date, **kwargs
            )
        except ValueError:
            # Event never occurs for specified date.
            return None

    @callback
    def is_up(self, utc_point_in_time: datetime.datetime = None) -> bool:
        """Calculate if the sun is currently up."""
        if utc_point_in_time is None:
            utc_point_in_time = helpers.utcnow()

        next_sunrise = self.get_astral_event_next(
            Const.SUN_EVENT_SUNRISE, utc_point_in_time
        )
        next_sunset = self.get_astral_event_next(
            Const.SUN_EVENT_SUNSET, utc_point_in_time
        )

        return next_sunrise > next_sunset
