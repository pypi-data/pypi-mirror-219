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

import datetime as dt
import logging
import typing

from ... import core
from .const import Const

_LOGGER: typing.Final = logging.getLogger(__name__)

# 4 mins is one degree of arc change of the sun on its circle.
# During the night and the middle of the day we don't update
# that much since it's not important.
_PHASE_UPDATES: typing.Final = {
    Const.PHASE_NIGHT: dt.timedelta(minutes=4 * 5),
    Const.PHASE_ASTRONOMICAL_TWILIGHT: dt.timedelta(minutes=4 * 2),
    Const.PHASE_NAUTICAL_TWILIGHT: dt.timedelta(minutes=4 * 2),
    Const.PHASE_TWILIGHT: dt.timedelta(minutes=4),
    Const.PHASE_SMALL_DAY: dt.timedelta(minutes=2),
    Const.PHASE_DAY: dt.timedelta(minutes=4),
}


# pylint: disable=unused-variable
class SunEntity(core.Entity):
    """Representation of the Sun."""

    _entity_id = Const.ENTITY_ID

    def __init__(self, shc: core.SmartHomeControllerComponent):
        """Initialize the sun."""

        self._shc = shc
        self._location = None
        self._elevation = 0.0
        self._state = self._next_rising = self._next_setting = None
        self._next_dawn = self._next_dusk = None
        self._next_midnight = self._next_noon = None
        self._solar_elevation = self._solar_azimuth = None
        self._rising = self._phase = None
        self._next_change = None
        self._config_listener = None
        self._update_events_listener = None
        self._update_sun_position_listener = None
        self._config_listener = self._shc.bus.async_listen(
            core.Const.EVENT_CORE_CONFIG_UPDATE, self._update_location
        )
        self._update_location()

    @core.callback
    def _update_location(self, *_):
        """Update location."""
        location, elevation = self._shc.sun.get_astral_location()
        if location == self._location:
            return
        self._location = location
        self._elevation = elevation
        if self._update_events_listener:
            self._update_events_listener()
        self._update_events()

    @core.callback
    def _remove_listeners(self):
        """Remove listeners."""
        if self._config_listener:
            self._config_listener()
        if self._update_events_listener:
            self._update_events_listener()
        if self._update_sun_position_listener:
            self._update_sun_position_listener()

    @property
    def name(self):
        """Return the name."""
        return "Sun"

    @property
    def state(self):
        """Return the state of the sun."""
        # 0.8333 is the same value as astral uses
        if self._solar_elevation > -0.833:
            return Const.STATE_ABOVE_HORIZON

        return Const.STATE_BELOW_HORIZON

    @property
    def extra_state_attributes(self):
        """Return the state attributes of the sun."""
        return {
            Const.STATE_ATTR_NEXT_DAWN: self._next_dawn.isoformat(),
            Const.STATE_ATTR_NEXT_DUSK: self._next_dusk.isoformat(),
            Const.STATE_ATTR_NEXT_MIDNIGHT: self._next_midnight.isoformat(),
            Const.STATE_ATTR_NEXT_NOON: self._next_noon.isoformat(),
            Const.STATE_ATTR_NEXT_RISING: self._next_rising.isoformat(),
            Const.STATE_ATTR_NEXT_SETTING: self._next_setting.isoformat(),
            Const.STATE_ATTR_ELEVATION: self._solar_elevation,
            Const.STATE_ATTR_AZIMUTH: self._solar_azimuth,
            Const.STATE_ATTR_RISING: self._rising,
        }

    def _check_event(self, utc_point_in_time: dt.datetime, sun_event: str, before: str):
        next_utc = self._shc.sun.get_location_astral_event_next(
            self._location, self._elevation, sun_event, utc_point_in_time
        )
        if next_utc < self._next_change:
            self._next_change = next_utc
            self._phase = before
        return next_utc

    @core.callback
    def _update_events(self, _now=None):
        """Update the attributes containing solar events."""
        # Grab current time in case system clock changed since last time we ran.
        utc_point_in_time = core.helpers.utcnow()
        self._next_change = utc_point_in_time + dt.timedelta(days=400)

        # Work our way around the solar cycle, figure out the next
        # phase. Some of these are stored.
        self._location.solar_depression = "astronomical"
        self._check_event(utc_point_in_time, "dawn", Const.PHASE_NIGHT)
        self._location.solar_depression = "nautical"
        self._check_event(utc_point_in_time, "dawn", Const.PHASE_ASTRONOMICAL_TWILIGHT)
        self._location.solar_depression = "civil"
        self._next_dawn = self._check_event(
            utc_point_in_time, "dawn", Const.PHASE_NAUTICAL_TWILIGHT
        )
        self._next_rising = self._check_event(
            utc_point_in_time, core.Const.SUN_EVENT_SUNRISE, Const.PHASE_TWILIGHT
        )
        self._location.solar_depression = -10
        self._check_event(utc_point_in_time, "dawn", Const.PHASE_SMALL_DAY)
        self._next_noon = self._check_event(utc_point_in_time, "noon", None)
        self._check_event(utc_point_in_time, "dusk", Const.PHASE_DAY)
        self._next_setting = self._check_event(
            utc_point_in_time, core.Const.SUN_EVENT_SUNSET, Const.PHASE_SMALL_DAY
        )
        self._location.solar_depression = "civil"
        self._next_dusk = self._check_event(
            utc_point_in_time, "dusk", Const.PHASE_TWILIGHT
        )
        self._location.solar_depression = "nautical"
        self._check_event(utc_point_in_time, "dusk", Const.PHASE_NAUTICAL_TWILIGHT)
        self._location.solar_depression = "astronomical"
        self._check_event(utc_point_in_time, "dusk", Const.PHASE_ASTRONOMICAL_TWILIGHT)
        self._next_midnight = self._check_event(utc_point_in_time, "midnight", None)
        self._location.solar_depression = "civil"

        # if the event was solar midday or midnight, phase will now
        # be None. Solar noon doesn't always happen when the sun is
        # even in the day at the poles, so we can't rely on it.
        # Need to calculate phase if next is noon or midnight
        if self._phase is None:
            elevation = self._location.solar_elevation(
                self._next_change, self._elevation
            )
            if elevation >= 10:
                self._phase = Const.PHASE_DAY
            elif elevation >= 0:
                self._phase = Const.PHASE_SMALL_DAY
            elif elevation >= -6:
                self._phase = Const.PHASE_TWILIGHT
            elif elevation >= -12:
                self._phase = Const.PHASE_NAUTICAL_TWILIGHT
            elif elevation >= -18:
                self._phase = Const.PHASE_ASTRONOMICAL_TWILIGHT
            else:
                self._phase = Const.PHASE_NIGHT

        self._rising = self._next_noon < self._next_midnight

        _LOGGER.debug(
            f"sun phase_update@{utc_point_in_time.isoformat()}: phase={self._phase}"
        )
        if self._update_sun_position_listener:
            self._update_sun_position_listener()
        self._update_sun_position()

        # Set timer for the next solar event
        self._update_events_listener = self._shc.tracker.async_track_point_in_utc_time(
            self._update_events, self._next_change
        )
        _LOGGER.debug(f"next time: {self._next_change.isoformat}")

    @core.callback
    def _update_sun_position(self, _now=None):
        """Calculate the position of the sun."""
        # Grab current time in case system clock changed since last time we ran.
        utc_point_in_time = core.helpers.utcnow()
        self._solar_azimuth = round(
            self._location.solar_azimuth(utc_point_in_time, self._elevation), 2
        )
        self._solar_elevation = round(
            self._location.solar_elevation(utc_point_in_time, self._elevation), 2
        )

        _LOGGER.debug(
            f"sun position_update@{utc_point_in_time.isoformat()}: "
            + f"elevation={self._solar_elevation} azimuth={self._solar_azimuth}",
        )
        self.async_write_state()

        # Next update as per the current phase
        delta = _PHASE_UPDATES[self._phase]
        # if the next update is within 1.25 of the next
        # position update just drop it
        if utc_point_in_time + delta * 1.25 > self._next_change:
            self._update_sun_position_listener = None
            return
        self._update_sun_position_listener = (
            self._shc.tracker.async_track_point_in_utc_time(
                self._update_sun_position, utc_point_in_time + delta
            )
        )
