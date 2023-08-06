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

import contextlib
import logging
import sys
import threading
import time
import traceback
import typing
from concurrent import futures

from .thread_with_exception import ThreadWithException

_JOIN_ATTEMPTS: typing.Final = 10
_EXECUTOR_SHUTDOWN_TIMEOUT: typing.Final = 10
_MAX_LOG_ATTEMPTS: typing.Final = 2

_LOGGER: typing.Final = logging.getLogger(__name__)


# pylint: disable=unused-variable
class InterruptibleThreadPoolExecutor(futures.ThreadPoolExecutor):
    """A ThreadPoolExecutor instance that will not deadlock on shutdown."""

    def shutdown(self, *_args: typing.Any, **_kwargs: typing.Any) -> None:
        """Shutdown with interrupt support added."""
        super().shutdown(wait=False, cancel_futures=True)
        self.join_threads_or_timeout()

    def join_threads_or_timeout(self) -> None:
        """Join threads or timeout."""
        remaining_threads = set(self._threads)
        start_time = time.monotonic()
        timeout_remaining: float = _EXECUTOR_SHUTDOWN_TIMEOUT
        attempt = 0

        while True:
            if not remaining_threads:
                return

            attempt += 1

            remaining_threads -= self._join_or_interrupt_threads(
                remaining_threads,
                timeout_remaining / _JOIN_ATTEMPTS,
                attempt <= _MAX_LOG_ATTEMPTS,
            )

            timeout_remaining = _EXECUTOR_SHUTDOWN_TIMEOUT - (
                time.monotonic() - start_time
            )
            if timeout_remaining <= 0:
                return

    @staticmethod
    def _join_or_interrupt_threads(
        threads: set[threading.Thread], timeout: float, log: bool
    ) -> set[threading.Thread]:
        """Attempt to join or interrupt a set of threads."""
        joined = set()
        timeout_per_thread = timeout / len(threads)

        for thread in threads:
            thread.join(timeout=timeout_per_thread)

            if not thread.is_alive() or thread.ident is None:
                joined.add(thread)
                continue

            if log:
                InterruptibleThreadPoolExecutor._log_thread_running_at_shutdown(
                    thread.name, thread.ident
                )

            with contextlib.suppress(SystemError):
                # SystemError at this stage is usually a race condition
                # where the thread happens to die right before we force
                # it to raise the exception
                ThreadWithException.async_raise(thread.ident, SystemExit)

        return joined

    @staticmethod
    def _log_thread_running_at_shutdown(name: str, ident: int) -> None:
        """Log the stack of a thread that was still running at shutdown."""
        frames = sys._current_frames()  # pylint: disable=protected-access
        stack = frames.get(ident)
        formatted_stack = traceback.format_stack(stack)
        _LOGGER.warning(
            f"Thread[{name}] is still running at shutdown: "
            + f"{''.join(formatted_stack).strip()}"
        )
