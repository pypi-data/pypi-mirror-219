"""
Recorder Component for Smart Home - The Next Generation.

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
import typing
from concurrent.futures.thread import _threads_queues, _worker
import threading
import weakref
from ... import core


def _worker_with_shutdown_hook(
    shutdown_hook: collections.abc.Callable[[], None],
    *args: typing.Any,
    **kwargs: typing.Any,
) -> None:
    """Create a worker that calls a function after its finished."""
    _worker(*args, **kwargs)
    shutdown_hook()


# pylint: disable=unused-variable
class DBInterruptibleThreadPoolExecutor(core.InterruptibleThreadPoolExecutor):
    """A database instance that will not deadlock on shutdown."""

    def __init__(self, *args: typing.Any, **kwargs: typing.Any) -> None:
        """Init the executor with a shutdown hook support."""
        self._shutdown_hook: collections.abc.Callable[[], None] = kwargs.pop(
            "shutdown_hook"
        )
        super().__init__(*args, **kwargs)

    def _adjust_thread_count(self) -> None:
        """Overridden to add support for shutdown hook.

        Based on the CPython 3.10 implementation.
        """
        # if idle threads are available, don't spin new threads
        if self._idle_semaphore.acquire(  # pylint: disable=consider-using-with
            timeout=0
        ):
            return

        # When the executor gets lost, the weakref callback will wake up
        # the worker threads.
        # pylint: disable=invalid-name
        def weakref_cb(_: typing.Any, q=self._work_queue) -> None:
            q.put(None)

        num_threads = len(self._threads)
        if num_threads < self._max_workers:
            thread_name = f"{self._thread_name_prefix or self}_{num_threads:d}"
            executor_thread = threading.Thread(
                name=thread_name,
                target=_worker_with_shutdown_hook,
                args=(
                    self._shutdown_hook,
                    weakref.ref(self, weakref_cb),
                    self._work_queue,
                    self._initializer,
                    self._initargs,
                ),
            )
            executor_thread.start()
            self._threads.add(executor_thread)
            _threads_queues[executor_thread] = self._work_queue
