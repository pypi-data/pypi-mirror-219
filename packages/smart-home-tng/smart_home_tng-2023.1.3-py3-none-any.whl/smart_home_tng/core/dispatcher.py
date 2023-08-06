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
import logging
import typing

from . import helpers
from .callback import callback
from .smart_home_controller_job import SmartHomeControllerJob


if not typing.TYPE_CHECKING:

    class SmartHomeController:
        ...


if typing.TYPE_CHECKING:
    from .smart_home_controller import SmartHomeController


_LOGGER: typing.Final = logging.getLogger(__name__)


# pylint: disable=unused-variable
class Dispatcher:
    """Signal handling for Smart Home - The Next Generation."""

    def __init__(self, shc: SmartHomeController):
        self._shc = shc
        self._dispatchers: dict[str, list[SmartHomeControllerJob]] = {}

    def connect(
        self, signal: str, target: collections.abc.Callable[..., None]
    ) -> collections.abc.Callable[[], None]:
        """Connect a callable function to a signal."""
        async_unsub = self._shc.run_callback_threadsafe(
            self.async_connect, signal, target
        ).result()

        def remove_dispatcher() -> None:
            """Remove signal listener."""
            self._shc.run_callback_threadsafe(async_unsub).result()

        return remove_dispatcher

    @callback
    def async_connect(
        self, signal: str, target: collections.abc.Callable[..., typing.Any]
    ) -> collections.abc.Callable[[], None]:
        """Connect a callable function to a signal.

        This method must be run in the event loop.
        """
        job = SmartHomeControllerJob(
            helpers.catch_log_exception(
                target,
                lambda *args: f"Exception in {getattr(target, '__name__', None) or str(target)} "
                + f"when dispatching '{signal}': {args}",
            )
        )

        self._dispatchers.setdefault(signal, []).append(job)

        @callback
        def async_remove_dispatcher() -> None:
            """Remove signal listener."""
            try:
                self._dispatchers[signal].remove(job)
            except (KeyError, ValueError):
                # KeyError is key target listener did not exist
                # ValueError if listener did not exist within signal
                _LOGGER.warning(f"Unable to remove unknown dispatcher {target}")

        return async_remove_dispatcher

    def send(self, signal: str, *args: typing.Any) -> None:
        """Send signal and data."""
        self._shc.call_soon_threadsafe(self.async_send, signal, *args)

    @callback
    def async_send(self, signal: str, *args: typing.Any) -> None:
        """Send signal and data.

        This method must be run in the event loop.
        """
        target_list = self._dispatchers.get(signal, [])

        for job in target_list:
            self._shc.async_add_shc_job(job, *args)

    def has_signal_subscription(self, signal: str) -> bool:
        signal_sub = self._dispatchers.get(signal, None)
        return signal_sub is not None and signal_sub.count() > 0
