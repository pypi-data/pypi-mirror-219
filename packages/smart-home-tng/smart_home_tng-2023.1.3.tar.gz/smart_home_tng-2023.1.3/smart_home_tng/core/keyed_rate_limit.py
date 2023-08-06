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

import asyncio
import collections.abc
import datetime
import logging
import typing

from . import helpers
from .callback import callback


if not typing.TYPE_CHECKING:

    class SmartHomeController:
        ...


if typing.TYPE_CHECKING:
    from .smart_home_controller import SmartHomeController

_LOGGER: typing.Final = logging.getLogger(__name__)


# pylint: disable=unused-variable
class KeyedRateLimit:
    """Class to track rate limits."""

    def __init__(
        self,
        shc: SmartHomeController,
    ) -> None:
        """Initialize ratelimit tracker."""
        self._shc = shc
        self._last_triggered: dict[collections.abc.Hashable, datetime.datetime] = {}
        self._rate_limit_timers: dict[
            collections.abc.Hashable, asyncio.TimerHandle
        ] = {}

    @callback
    def async_has_timer(self, key: collections.abc.Hashable) -> bool:
        """Check if a rate limit timer is running."""
        if not self._rate_limit_timers:
            return False
        return key in self._rate_limit_timers

    @callback
    def async_triggered(
        self, key: collections.abc.Hashable, now: datetime.datetime = None
    ) -> None:
        """Call when the action we are tracking was triggered."""
        self.async_cancel_timer(key)
        self._last_triggered[key] = now or helpers.utcnow()

    @callback
    def async_cancel_timer(self, key: collections.abc.Hashable) -> None:
        """Cancel a rate limit time that will call the action."""
        if not self._rate_limit_timers or not self.async_has_timer(key):
            return

        self._rate_limit_timers.pop(key).cancel()

    @callback
    def async_remove(self) -> None:
        """Remove all timers."""
        for timer in self._rate_limit_timers.values():
            timer.cancel()
        self._rate_limit_timers.clear()

    @callback
    def async_schedule_action(
        self,
        key: collections.abc.Hashable,
        rate_limit: datetime.timedelta,
        now: datetime.datetime,
        action: collections.abc.Callable,
        *args: typing.Any,
    ) -> datetime.datetime:
        """Check rate limits and schedule an action if we hit the limit.

        If the rate limit is hit:
            Schedules the action for when the rate limit expires
            if there are no pending timers. The action must
            be called in async.

            Returns the time the rate limit will expire

        If the rate limit is not hit:

            Return None
        """
        if rate_limit is None:
            return None

        if not (last_triggered := self._last_triggered.get(key)):
            return None

        next_call_time = last_triggered + rate_limit

        if next_call_time <= now:
            self.async_cancel_timer(key)
            return None

        _LOGGER.debug(
            f"Reached rate limit of {rate_limit} for {key} and "
            + f"deferred action until {next_call_time}"
        )

        if key not in self._rate_limit_timers:
            self._rate_limit_timers[key] = self._shc.loop.call_later(
                (next_call_time - now).total_seconds(),
                action,
                *args,
            )

        return next_call_time
