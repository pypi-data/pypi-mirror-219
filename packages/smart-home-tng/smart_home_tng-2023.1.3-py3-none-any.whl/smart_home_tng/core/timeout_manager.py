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
import enum
import types
import typing

from ..backports import strenum
from . import helpers

_ZONE_GLOBAL: typing.Final = "global"

_TimeoutManagerT = typing.TypeVar("_TimeoutManagerT", bound="TimeoutManager")
_ZoneTimeoutManagerT = typing.TypeVar(
    "_ZoneTimeoutManagerT", bound="_ZoneTimeoutManager"
)


class _State(strenum.UppercaseStrEnum):
    """States of a task."""

    INIT = enum.auto()
    ACTIVE = enum.auto()
    TIMEOUT = enum.auto()
    EXIT = enum.auto()


# pylint: disable=unused-variable
class _GlobalFreezeContext:
    """Context manager that freezes the global timeout."""

    def __init__(self, manager: _TimeoutManagerT) -> None:
        """Initialize internal timeout context manager."""
        self._loop: asyncio.AbstractEventLoop = asyncio.get_running_loop()
        self._manager: TimeoutManager = manager

    async def __aenter__(self):
        self._enter()
        return self

    async def __aexit__(
        self,
        _exc_type: type[BaseException],
        _exc_val: BaseException,
        _exc_tb: types.TracebackType,
    ) -> bool:
        self._exit()
        return None

    def __enter__(self):
        self._loop.call_soon_threadsafe(self._enter)
        return self

    def __exit__(
        self,
        _exc_type: type[BaseException],
        _exc_val: BaseException,
        _exc_tb: types.TracebackType,
    ) -> bool:
        self._loop.call_soon_threadsafe(self._exit)

    def _enter(self) -> None:
        """Run freeze."""
        if not self._manager.freezes_done:
            return

        # Global reset
        for task in self._manager.global_tasks:
            task.pause()

        # Zones reset
        for zone in self._manager.zones.values():
            if not zone.freezes_done:
                continue
            zone.pause()

        self._manager.global_freezes.append(self)

    def _exit(self) -> None:
        """Finish freeze."""
        self._manager.global_freezes.remove(self)
        if not self._manager.freezes_done:
            return

        # Global reset
        for task in self._manager.global_tasks:
            task.reset()

        # Zones reset
        for zone in self._manager.zones.values():
            if not zone.freezes_done:
                continue
            zone.reset()


class _GlobalTaskContext:
    """Context manager that tracks a global task."""

    def __init__(
        self,
        manager: _TimeoutManagerT,
        task: asyncio.Task[typing.Any],
        timeout: float,
        cool_down: float,
    ) -> None:
        """Initialize internal timeout context manager."""
        self._loop: asyncio.events.AbstractEventLoop = asyncio.get_running_loop()
        self._manager: TimeoutManager = manager
        self._task: asyncio.Task[typing.Any] = task
        self._time_left: float = timeout
        self._expiration_time: float = None
        self._timeout_handler: asyncio.Handle = None
        self._wait_zone: asyncio.Event = asyncio.Event()
        self._state: _State = _State.INIT
        self._cool_down: float = cool_down

    async def __aenter__(self):
        self._manager.global_tasks.append(self)
        self._start_timer()
        self._state = _State.ACTIVE
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException],
        _exc_val: BaseException,
        _exc_tb: types.TracebackType,
    ) -> bool:
        self._stop_timer()
        self._manager.global_tasks.remove(self)

        # Timeout on exit
        if exc_type is asyncio.CancelledError and self.state == _State.TIMEOUT:
            raise asyncio.TimeoutError

        self._state = _State.EXIT
        self._wait_zone.set()
        return None

    @property
    def state(self) -> _State:
        """Return state of the Global task."""
        return self._state

    def zones_done_signal(self) -> None:
        """Signal that all zones are done."""
        self._wait_zone.set()

    def _start_timer(self) -> None:
        """Start timeout handler."""
        if self._timeout_handler:
            return

        self._expiration_time = self._loop.time() + self._time_left
        self._timeout_handler = self._loop.call_at(
            self._expiration_time, self._on_timeout
        )

    def _stop_timer(self) -> None:
        """Stop zone timer."""
        if self._timeout_handler is None:
            return

        self._timeout_handler.cancel()
        self._timeout_handler = None
        # Calculate new timeout
        assert self._expiration_time
        self._time_left = self._expiration_time - self._loop.time()

    def _on_timeout(self) -> None:
        """Process timeout."""
        self._state = _State.TIMEOUT
        self._timeout_handler = None

        # Reset timer if zones are running
        if not self._manager.zones_done:
            asyncio.create_task(self._on_wait())
        else:
            self._cancel_task()

    def _cancel_task(self) -> None:
        """Cancel own task."""
        if self._task.done():
            return
        self._task.cancel()

    def pause(self) -> None:
        """Pause timers while it freeze."""
        self._stop_timer()

    def reset(self) -> None:
        """Reset timer after freeze."""
        self._start_timer()

    async def _on_wait(self) -> None:
        """Wait until zones are done."""
        await self._wait_zone.wait()
        await asyncio.sleep(self._cool_down)  # Allow context switch
        if self.state != _State.TIMEOUT:
            return
        self._cancel_task()


class _ZoneTaskContext:
    """Context manager that tracks an active task for a zone."""

    def __init__(
        self,
        zone: _ZoneTimeoutManagerT,
        task: asyncio.Task[typing.Any],
        timeout: float,
    ) -> None:
        """Initialize internal timeout context manager."""
        self._loop: asyncio.events.AbstractEventLoop = asyncio.get_running_loop()
        self._zone: _ZoneTimeoutManager = zone
        self._task: asyncio.Task[typing.Any] = task
        self._state: _State = _State.INIT
        self._time_left: float = timeout
        self._expiration_time: float = None
        self._timeout_handler: asyncio.Handle = None

    @property
    def state(self) -> _State:
        """Return state of the Zone task."""
        return self._state

    async def __aenter__(self):
        self._zone.enter_task(self)
        self._state = _State.ACTIVE

        # Zone is on freeze
        if self._zone.freezes_done:
            self._start_timer()

        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException],
        _exc_val: BaseException,
        _exc_tb: types.TracebackType,
    ) -> bool:
        self._zone.exit_task(self)
        self._stop_timer()

        # Timeout on exit
        if exc_type is asyncio.CancelledError and self.state == _State.TIMEOUT:
            raise asyncio.TimeoutError

        self._state = _State.EXIT
        return None

    def _start_timer(self) -> None:
        """Start timeout handler."""
        if self._timeout_handler:
            return

        self._expiration_time = self._loop.time() + self._time_left
        self._timeout_handler = self._loop.call_at(
            self._expiration_time, self._on_timeout
        )

    def _stop_timer(self) -> None:
        """Stop zone timer."""
        if self._timeout_handler is None:
            return

        self._timeout_handler.cancel()
        self._timeout_handler = None
        # Calculate new timeout
        assert self._expiration_time
        self._time_left = self._expiration_time - self._loop.time()

    def _on_timeout(self) -> None:
        """Process timeout."""
        self._state = _State.TIMEOUT
        self._timeout_handler = None

        # Timeout
        if self._task.done():
            return
        self._task.cancel()

    def pause(self) -> None:
        """Pause timers while it freeze."""
        self._stop_timer()

    def reset(self) -> None:
        """Reset timer after freeze."""
        self._start_timer()


class _ZoneFreezeContext:
    """Context manager that freezes a zone timeout."""

    def __init__(self, zone: _ZoneTimeoutManagerT) -> None:
        """Initialize internal timeout context manager."""
        self._loop: asyncio.AbstractEventLoop = asyncio.get_running_loop()
        self._zone: _ZoneTimeoutManager = zone

    async def __aenter__(self):
        self._enter()
        return self

    async def __aexit__(
        self,
        _exc_type: type[BaseException],
        _exc_val: BaseException,
        _exc_tb: types.TracebackType,
    ) -> bool:
        self._exit()
        return None

    def __enter__(self):
        self._loop.call_soon_threadsafe(self._enter)
        return self

    def __exit__(  # pylint: disable=useless-return
        self,
        _exc_type: type[BaseException],
        _exc_val: BaseException,
        _exc_tb: types.TracebackType,
    ) -> bool:
        self._loop.call_soon_threadsafe(self._exit)
        return None

    def _enter(self) -> None:
        """Run freeze."""
        if self._zone.freezes_done:
            self._zone.pause()
        self._zone.enter_freeze(self)

    def _exit(self) -> None:
        """Finish freeze."""
        self._zone.exit_freeze(self)
        if not self._zone.freezes_done:
            return
        self._zone.reset()


class _ZoneTimeoutManager:
    """Manage the timeouts for a zone."""

    def __init__(self, manager: _TimeoutManagerT, zone: str) -> None:
        """Initialize internal timeout context manager."""
        self._manager: TimeoutManager = manager
        self._zone: str = zone
        self._tasks: list[_ZoneTaskContext] = []
        self._freezes: list[_ZoneFreezeContext] = []

    def __repr__(self) -> str:
        """Representation of a zone."""
        return f"<{self.name}: {len(self._tasks)} / {len(self._freezes)}>"

    @property
    def name(self) -> str:
        """Return Zone name."""
        return self._zone

    @property
    def active(self) -> bool:
        """Return True if zone is active."""
        return len(self._tasks) > 0 or len(self._freezes) > 0

    @property
    def freezes_done(self) -> bool:
        """Return True if all freeze are done."""
        return len(self._freezes) == 0 and self._manager.freezes_done

    def enter_task(self, task: _ZoneTaskContext) -> None:
        """Start into new Task."""
        self._tasks.append(task)

    def exit_task(self, task: _ZoneTaskContext) -> None:
        """Exit a running Task."""
        self._tasks.remove(task)

        # On latest listener
        if not self.active:
            self._manager.drop_zone(self.name)

    def enter_freeze(self, freeze: _ZoneFreezeContext) -> None:
        """Start into new freeze."""
        self._freezes.append(freeze)

    def exit_freeze(self, freeze: _ZoneFreezeContext) -> None:
        """Exit a running Freeze."""
        self._freezes.remove(freeze)

        # On latest listener
        if not self.active:
            self._manager.drop_zone(self.name)

    def pause(self) -> None:
        """Stop timers while it freeze."""
        if not self.active:
            return

        # Forward pause
        for task in self._tasks:
            task.pause()

    def reset(self) -> None:
        """Reset timer after freeze."""
        if not self.active:
            return

        # Forward reset
        for task in self._tasks:
            task.reset()


class TimeoutManager:
    """Class to manage timeouts over different zones.

    Manages both global and zone based timeouts.
    """

    def __init__(self) -> None:
        """Initialize TimeoutManager."""
        self._loop: asyncio.AbstractEventLoop = asyncio.get_running_loop()
        self._zones: dict[str, _ZoneTimeoutManager] = {}
        self._globals: list[_GlobalTaskContext] = []
        self._freezes: list[_GlobalFreezeContext] = []

    @property
    def zones_done(self) -> bool:
        """Return True if all zones are finished."""
        return not bool(self._zones)

    @property
    def freezes_done(self) -> bool:
        """Return True if all freezes are finished."""
        return not self._freezes

    @property
    def zones(self) -> dict[str, _ZoneTimeoutManager]:
        """Return all Zones."""
        return self._zones

    @property
    def global_tasks(self) -> list[_GlobalTaskContext]:
        """Return all global Tasks."""
        return self._globals

    @property
    def global_freezes(self) -> list[_GlobalFreezeContext]:
        """Return all global Freezes."""
        return self._freezes

    def drop_zone(self, zone_name: str) -> None:
        """Drop a zone out of scope."""
        self._zones.pop(zone_name, None)
        if self._zones:
            return

        # Signal Global task, all zones are done
        for task in self._globals:
            task.zones_done_signal()

    def async_timeout(
        self, timeout: float, zone_name: str = _ZONE_GLOBAL, cool_down: float = 0
    ) -> _ZoneTaskContext | _GlobalTaskContext:
        """Timeout based on a zone.

        For using as Async Context Manager.
        """
        current_task: asyncio.Task[typing.Any] = asyncio.current_task()
        assert current_task

        # Global Zone
        if zone_name == _ZONE_GLOBAL:
            task = _GlobalTaskContext(self, current_task, timeout, cool_down)
            return task

        # Zone Handling
        if zone_name in self.zones:
            zone: _ZoneTimeoutManager = self.zones[zone_name]
        else:
            self.zones[zone_name] = zone = _ZoneTimeoutManager(self, zone_name)

        # Create Task
        return _ZoneTaskContext(zone, current_task, timeout)

    def async_freeze(
        self, zone_name: str = _ZONE_GLOBAL
    ) -> _ZoneFreezeContext | _GlobalFreezeContext:
        """Freeze all timer until job is done.

        For using as Async Context Manager.
        """
        # Global Freeze
        if zone_name == _ZONE_GLOBAL:
            return _GlobalFreezeContext(self)

        # Zone Freeze
        if zone_name in self.zones:
            zone: _ZoneTimeoutManager = self.zones[zone_name]
        else:
            self.zones[zone_name] = zone = _ZoneTimeoutManager(self, zone_name)

        return _ZoneFreezeContext(zone)

    def freeze(
        self, zone_name: str = _ZONE_GLOBAL
    ) -> _ZoneFreezeContext | _GlobalFreezeContext:
        """Freeze all timer until job is done.

        For using as Context Manager.
        """
        return helpers.run_callback_threadsafe(
            self._loop, self.async_freeze, zone_name
        ).result()
