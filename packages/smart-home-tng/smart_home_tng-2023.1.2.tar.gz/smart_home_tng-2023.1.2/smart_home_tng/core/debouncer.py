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
import logging
import typing

from .callback import callback
from .smart_home_controller_job import SmartHomeControllerJob


if not typing.TYPE_CHECKING:

    class SmartHomeController:
        ...


if typing.TYPE_CHECKING:
    from .smart_home_controller import SmartHomeController

_R_co = typing.TypeVar("_R_co", covariant=True)


# pylint: disable=unused-variable
class Debouncer(typing.Generic[_R_co]):
    """Class to rate limit calls to a specific command."""

    def __init__(
        self,
        shc: SmartHomeController,
        logger: logging.Logger,
        *,
        cooldown: float,
        immediate: bool,
        function: typing.Callable[..., typing.Awaitable[typing.Any]] = None,
    ) -> None:
        """Initialize debounce.

        immediate: indicate if the function needs to be called right away and
                   wait <cooldown> until executing next invocation.
        function: optional and can be instantiated later.
        """
        self._shc = shc
        self._logger = logger
        self._function = function
        self._cooldown = cooldown
        self._immediate = immediate
        self._timer_task: asyncio.TimerHandle = None
        self._execute_at_end_of_timer: bool = False
        self._execute_lock = asyncio.Lock()
        self._job: SmartHomeControllerJob = (
            None if function is None else SmartHomeControllerJob(function)
        )

    @property
    def function(self) -> typing.Callable[..., typing.Awaitable[typing.Any]]:
        """Return the function being wrapped by the Debouncer."""
        return self._function

    @function.setter
    def function(
        self, function: typing.Callable[..., typing.Awaitable[typing.Any]]
    ) -> None:
        """Update the function being wrapped by the Debouncer."""
        self._function = function
        if self._job is None or function != self._job.target:
            self._job = SmartHomeControllerJob(function)

    async def async_call(self) -> None:
        """Call the function."""
        assert self._job is not None

        if self._timer_task:
            if not self._execute_at_end_of_timer:
                self._execute_at_end_of_timer = True

            return

        # Locked means a call is in progress. Any call is good, so abort.
        if self._execute_lock.locked():
            return

        if not self._immediate:
            self._execute_at_end_of_timer = True
            self._schedule_timer()
            return

        async with self._execute_lock:
            # Abort if timer got set while we're waiting for the lock.
            if self._timer_task:
                return

            task = self._shc.async_run_shc_job(self._job)
            if task:
                await task

            self._schedule_timer()

    async def _handle_timer_finish(self) -> None:
        """Handle a finished timer."""
        assert self._job is not None

        self._timer_task = None

        if not self._execute_at_end_of_timer:
            return

        self._execute_at_end_of_timer = False

        # Locked means a call is in progress. Any call is good, so abort.
        if self._execute_lock.locked():
            return

        async with self._execute_lock:
            # Abort if timer got set while we're waiting for the lock.
            if self._timer_task:
                return

            try:
                task = self._shc.async_run_shc_job(self._job)
                if task:
                    await task
            except Exception:  # pylint: disable=broad-except
                self._logger.exception(f"Unexpected exception from {self.function}")

            self._schedule_timer()

    @callback
    def async_cancel(self) -> None:
        """Cancel any scheduled call."""
        if self._timer_task:
            self._timer_task.cancel()
            self._timer_task = None

        self._execute_at_end_of_timer = False

    @callback
    def _schedule_timer(self) -> None:
        """Schedule a timer."""
        self._timer_task = self._shc.call_later(
            self._cooldown,
            lambda: self._shc.async_create_task(self._handle_timer_finish()),
        )
