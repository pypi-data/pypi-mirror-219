"""
Stream Component for Smart Home - The Next Generation.

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


# pylint: disable=unused-variable
class IdleTimer:
    """Invoke a callback after an inactivity timeout.

    The IdleTimer invokes the callback after some timeout has passed. The awake() method
    resets the internal alarm, extending the inactivity time.
    """

    def __init__(
        self,
        shc: core.SmartHomeController,
        timeout: int,
        idle_callback: typing.Callable[
            [], typing.Coroutine[typing.Any, typing.Any, None]
        ],
    ) -> None:
        """Initialize IdleTimer."""
        self._shc = shc
        self._timeout = timeout
        self._callback = idle_callback
        self._unsub: core.CallbackType = None
        self._idle = False

    @property
    def idle(self) -> bool:
        return self._idle

    def start(self) -> None:
        """Start the idle timer if not already started."""
        self._idle = False
        if self._unsub is None:
            self._unsub = self._shc.tracker.async_call_later(self._timeout, self._fire)

    def awake(self) -> None:
        """Keep the idle time alive by resetting the timeout."""
        self._idle = False
        # Reset idle timeout
        self.clear()
        self._unsub = self._shc.tracker.async_call_later(self._timeout, self._fire)

    def clear(self) -> None:
        """Clear and disable the timer if it has not already fired."""
        if self._unsub is not None:
            self._unsub()
            self._unsub = None

    @core.callback
    def _fire(self, _now: dt.datetime) -> None:
        """Invoke the idle timeout callback, called when the alarm fires."""
        self._idle = True
        self._unsub = None
        self._shc.async_create_task(self._callback())
