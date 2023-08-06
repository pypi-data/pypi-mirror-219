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
import functools
import logging
import typing

from . import helpers
from .callback import callback, is_callback
from .callback_type import CallbackType
from .const import Const
from .context import Context
from .event import Event
from .event_origin import EventOrigin
from .max_length_exceeded import MaxLengthExceeded
from .smart_home_controller_error import SmartHomeControllerError
from .smart_home_controller_job import SmartHomeControllerJob


if not typing.TYPE_CHECKING:

    class SmartHomeController:
        ...


if typing.TYPE_CHECKING:
    from .smart_home_controller import SmartHomeController

_LOGGER: typing.Final = logging.getLogger(__name__)


class _FilterableJob(typing.NamedTuple):
    """Event listener job to be executed with optional filter."""

    job: SmartHomeControllerJob[collections.abc.Awaitable[None]]
    event_filter: typing.Callable[[Event], bool] = None
    run_immediately: bool = False


# pylint: disable=unused-variable
class EventBus:
    """Allow the firing of and listening for events."""

    def __init__(
        self, shc: SmartHomeController, loop: asyncio.AbstractEventLoop
    ) -> None:
        """Initialize a new event bus."""
        self._shc = shc
        self._loop = loop
        self._listeners: dict[str, list[_FilterableJob]] = {}

    @callback
    def async_listeners(self) -> dict[str, int]:
        """Return dictionary with events and the number of listeners.

        This method must be run in the event loop.
        """
        return {key: len(listeners) for key, listeners in self._listeners.items()}

    @property
    def listeners(self) -> dict[str, int]:
        """Return dictionary with events and the number of listeners."""
        return helpers.run_callback_threadsafe(
            self._loop, self.async_listeners
        ).result()

    def fire(
        self,
        event_type: str,
        event_data: dict[str, typing.Any] = None,
        origin: EventOrigin = EventOrigin.LOCAL,
        context: Context = None,
    ) -> None:
        """Fire an event."""
        helpers.run_callback_threadsafe(
            self._loop, self.async_fire, event_type, event_data, origin, context
        )

    @callback
    def async_fire(
        self,
        event_type: str,
        event_data: dict[str, typing.Any] = None,
        origin: EventOrigin = EventOrigin.LOCAL,
        context: Context = None,
        time_fired: datetime.datetime = None,
    ) -> None:
        """Fire an event.

        This method must be run in the event loop.
        """
        if len(event_type) > Const.MAX_LENGTH_EVENT_EVENT_TYPE:
            raise MaxLengthExceeded(
                event_type, "event_type", Const.MAX_LENGTH_EVENT_EVENT_TYPE
            )

        listeners = self._listeners.get(event_type, [])

        # EVENT_ASSISTANT_CLOSE should go only to this listeners
        match_all_listeners = self._listeners.get(Const.MATCH_ALL)
        if match_all_listeners is not None and event_type != Const.EVENT_SHC_CLOSE:
            listeners = match_all_listeners + listeners

        event = Event(event_type, event_data, origin, time_fired, context)

        _LOGGER.debug(f"Bus:Handling {event}")

        if not listeners:
            return

        for job, event_filter, run_immediately in listeners:
            if event_filter is not None:
                try:
                    if not event_filter(event):
                        continue
                except Exception:  # pylint: disable=broad-except
                    _LOGGER.exception("Error in event filter")
                    continue
            if run_immediately:
                try:
                    job.target(event)
                except Exception:  # pylint: disable=broad-except
                    _LOGGER.exception(f"Error running job: {job}")
            else:
                self._shc.async_add_shc_job(job, event)

    def listen(
        self,
        event_type: str,
        listener: typing.Callable[[Event], None | collections.abc.Awaitable[None]],
    ) -> CallbackType:
        """Listen for all events or events of a specific type.

        To listen to all events specify the constant ``MATCH_ALL``
        as event_type.
        """
        async_remove_listener = helpers.run_callback_threadsafe(
            self._loop, self.async_listen, event_type, listener
        ).result()

        def remove_listener() -> None:
            """Remove the listener."""
            helpers.run_callback_threadsafe(self._loop, async_remove_listener).result()

        return remove_listener

    @callback
    def async_listen(
        self,
        event_type: str,
        listener: typing.Callable[[Event], None | collections.abc.Awaitable[None]],
        event_filter: typing.Callable[[Event], bool] = None,
        run_immediately: bool = False,
    ) -> CallbackType:
        """Listen for all events or events of a specific type.

        To listen to all events specify the constant ``MATCH_ALL``
        as event_type.

        An optional event_filter, which must be a callable decorated with
        @callback that returns a boolean value, determines if the
        listener callable should run.

        If run_immediately is passed, the callback will be run
        right away instead of using call_soon. Only use this if
        the callback results in scheduling another task.

        This method must be run in the event loop.
        """
        if event_filter is not None and not is_callback(event_filter):
            raise SmartHomeControllerError(
                f"Event filter {event_filter} is not a callback"
            )
        if run_immediately and not is_callback(listener):
            raise SmartHomeControllerError(
                f"Event listener {listener} is not a callback"
            )
        return self._async_listen_filterable_job(
            event_type,
            _FilterableJob(
                SmartHomeControllerJob(listener), event_filter, run_immediately
            ),
        )

    @callback
    def _async_listen_filterable_job(
        self, event_type: str, filterable_job: _FilterableJob
    ) -> CallbackType:
        self._listeners.setdefault(event_type, []).append(filterable_job)

        def remove_listener() -> None:
            """Remove the listener."""
            self._async_remove_listener(event_type, filterable_job)

        return remove_listener

    def listen_once(
        self,
        event_type: str,
        listener: typing.Callable[[Event], None | collections.abc.Awaitable[None]],
    ) -> CallbackType:
        """Listen once for event of a specific type.

        To listen to all events specify the constant ``MATCH_ALL``
        as event_type.

        Returns function to unsubscribe the listener.
        """
        async_remove_listener = helpers.run_callback_threadsafe(
            self._loop, self.async_listen_once, event_type, listener
        ).result()

        def remove_listener() -> None:
            """Remove the listener."""
            helpers.run_callback_threadsafe(self._loop, async_remove_listener).result()

        return remove_listener

    @callback
    def async_listen_once(
        self,
        event_type: str,
        listener: typing.Callable[[Event], None | collections.abc.Awaitable[None]],
    ) -> CallbackType:
        """Listen once for event of a specific type.

        To listen to all events specify the constant ``MATCH_ALL``
        as event_type.

        Returns registered listener that can be used with remove_listener.

        This method must be run in the event loop.
        """
        filterable_job: _FilterableJob = None

        @callback
        def _onetime_listener(event: Event) -> None:
            """Remove listener from event bus and then fire listener."""
            nonlocal filterable_job
            if hasattr(_onetime_listener, "run"):
                return
            # Set variable so that we will never run twice.
            # Because the event bus loop might have async_fire queued multiple
            # times, its possible this listener may already be lined up
            # multiple times as well.
            # This will make sure the second time it does nothing.
            setattr(_onetime_listener, "run", True)
            assert filterable_job is not None
            self._async_remove_listener(event_type, filterable_job)
            self._shc.async_run_job(listener, event)

        functools.update_wrapper(
            _onetime_listener, listener, ("__name__", "__qualname__", "__module__"), []
        )

        filterable_job = _FilterableJob(
            SmartHomeControllerJob(_onetime_listener), None, False
        )

        return self._async_listen_filterable_job(event_type, filterable_job)

    @callback
    def _async_remove_listener(
        self, event_type: str, filterable_job: _FilterableJob
    ) -> None:
        """Remove a listener of a specific event_type.

        This method must be run in the event loop.
        """
        try:
            self._listeners[event_type].remove(filterable_job)

            # delete event_type list if empty
            if not self._listeners[event_type]:
                self._listeners.pop(event_type)
        except (KeyError, ValueError):
            # KeyError is key event_type listener did not exist
            # ValueError if listener did not exist within event_type
            _LOGGER.exception(f"Unable to remove unknown job listener {filterable_job}")
