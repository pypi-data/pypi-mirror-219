"""
Timer Component for Smart Home - The Next Generation.

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
import typing

from ... import core

_cv: typing.TypeAlias = core.ConfigValidation
_timer: typing.TypeAlias = core.Timer


# pylint: disable=unused-variable
class Timer(core.RestoreEntity):
    """Representation of a timer."""

    _domain: str

    def __init__(self, config: dict) -> None:
        """Initialize a timer."""
        self._config: dict = config
        self._editable: bool = True
        self._state: str = _timer.STATUS_IDLE
        self._duration = _cv.time_period_str(config[_timer.CONF_DURATION])
        self._remaining: dt.timedelta = None
        self._end: dt.datetime = None
        self._listener: typing.Callable[[], None] = None
        self._restore: bool = self._config.get(
            _timer.CONF_RESTORE, _timer.DEFAULT_RESTORE
        )

        self._attr_should_poll = False
        self._attr_force_update = True

    @property
    def editable(self) -> bool:
        return self._editable

    @classmethod
    def from_yaml(cls, config: dict):
        """Return entity instance initialized from yaml storage."""
        timer = cls(config)
        # pylint: disable=no-member
        timer._entity_id = f"{Timer._domain}.{config[core.Const.CONF_ID]}"
        timer._editable = False
        return timer

    @property
    def name(self):
        """Return name of the timer."""
        return self._config.get(core.Const.CONF_NAME)

    @property
    def icon(self):
        """Return the icon to be used for this entity."""
        return self._config.get(core.Const.CONF_ICON)

    @property
    def state(self):
        """Return the current value of the timer."""
        return self._state

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        attrs = {
            _timer.ATTR_DURATION: _format_timedelta(self._duration),
            core.Const.ATTR_EDITABLE: self.editable,
        }
        if self._end is not None:
            attrs[_timer.ATTR_FINISHES_AT] = self._end.isoformat()
        if self._remaining is not None:
            attrs[_timer.ATTR_REMAINING] = _format_timedelta(self._remaining)
        if self._restore:
            attrs[_timer.ATTR_RESTORE] = self._restore

        return attrs

    @property
    def unique_id(self) -> str | None:
        """Return unique id for the entity."""
        return self._config[core.Const.CONF_ID]

    async def async_added_to_shc(self):
        """Call when entity is about to be added to Home Assistant."""
        # If we don't need to restore a previous state or no previous state exists,
        # start at idle
        if not self._restore or (state := await self.async_get_last_state()) is None:
            self._state = _timer.STATUS_IDLE
            return

        # Begin restoring state
        self._state = state.state
        self._duration = _cv.time_period(state.attributes[_timer.ATTR_DURATION])

        # Nothing more to do if the timer is idle
        if self._state == _timer.STATUS_IDLE:
            return

        # If the timer was paused, we restore the remaining time
        if self._state == _timer.STATUS_PAUSED:
            self._remaining = _cv.time_period(state.attributes[_timer.ATTR_REMAINING])
            return
        # If we get here, the timer must have been active so we need to decide what
        # to do based on end time and the current time
        end = _cv.datetime(state.attributes[_timer.ATTR_FINISHES_AT])
        # If there is time remaining in the timer, restore the remaining time then
        # start the timer
        if (
            remaining := end - core.helpers.utcnow().replace(microsecond=0)
        ) > dt.timedelta(0):
            self._remaining = remaining
            self._state = _timer.STATUS_PAUSED
            self.async_start()
        # If the timer ended before now, finish the timer. The event will indicate
        # when the timer was expected to fire.
        else:
            self._end = end
            self.async_finish()

    @core.callback
    def async_start(self, duration: dt.timedelta = None):
        """Start a timer."""
        if self._listener:
            self._listener()
            self._listener = None

        event = _timer.EVENT_TIMER_STARTED
        if self._state in (_timer.STATUS_ACTIVE, _timer.STATUS_PAUSED):
            event = _timer.EVENT_TIMER_RESTARTED

        self._state = _timer.STATUS_ACTIVE
        start = core.helpers.utcnow().replace(microsecond=0)

        # Set remaining to new value if needed
        if duration:
            self._remaining = self._duration = duration
        elif not self._remaining:
            self._remaining = self._duration

        self._end = start + self._remaining

        self._shc.bus.async_fire(event, {core.Const.ATTR_ENTITY_ID: self.entity_id})

        self._listener = self._shc.tracker.async_track_point_in_utc_time(
            self._async_finished, self._end
        )
        self.async_write_state()

    @core.callback
    def async_pause(self):
        """Pause a timer."""
        if self._listener is None:
            return

        self._listener()
        self._listener = None
        self._remaining = self._end - core.helpers.utcnow().replace(microsecond=0)
        self._state = _timer.STATUS_PAUSED
        self._end = None
        self._shc.bus.async_fire(
            _timer.EVENT_TIMER_PAUSED, {core.Const.ATTR_ENTITY_ID: self.entity_id}
        )
        self.async_write_state()

    @core.callback
    def async_cancel(self):
        """Cancel a timer."""
        if self._listener:
            self._listener()
            self._listener = None
        self._state = _timer.STATUS_IDLE
        self._end = None
        self._remaining = None
        self._shc.bus.async_fire(
            _timer.EVENT_TIMER_CANCELLED, {core.Const.ATTR_ENTITY_ID: self.entity_id}
        )
        self.async_write_state()

    @core.callback
    def async_finish(self):
        """Reset and updates the states, fire finished event."""
        if self._state != _timer.STATUS_ACTIVE:
            return

        if self._listener:
            self._listener()
            self._listener = None
        end = self._end
        self._state = _timer.STATUS_IDLE
        self._end = None
        self._remaining = None
        self._shc.bus.async_fire(
            _timer.EVENT_TIMER_FINISHED,
            {
                core.Const.ATTR_ENTITY_ID: self.entity_id,
                _timer.ATTR_FINISHED_AT: end.isoformat(),
            },
        )
        self.async_write_state()

    @core.callback
    def _async_finished(self, _time):
        """Reset and updates the states, fire finished event."""
        if self._state != _timer.STATUS_ACTIVE:
            return

        self._listener = None
        self._state = _timer.STATUS_IDLE
        end = self._end
        self._end = None
        self._remaining = None
        self._shc.bus.async_fire(
            _timer.EVENT_TIMER_FINISHED,
            {
                core.Const.ATTR_ENTITY_ID: self.entity_id,
                _timer.ATTR_FINISHED_AT: end.isoformat(),
            },
        )
        self.async_write_state()

    async def async_update_config(self, config: dict) -> None:
        """Handle when the config is updated."""
        self._config = config
        self._duration = _cv.time_period_str(config[_timer.CONF_DURATION])
        self._restore = config.get(_timer.CONF_RESTORE, _timer.DEFAULT_RESTORE)
        self.async_write_state()


def _format_timedelta(delta: dt.timedelta):
    total_seconds = delta.total_seconds()
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{int(hours)}:{int(minutes):02}:{int(seconds):02}"
