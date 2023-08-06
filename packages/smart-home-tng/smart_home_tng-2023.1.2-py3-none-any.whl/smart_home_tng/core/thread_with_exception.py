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

import ctypes
import inspect
import logging
import threading
import typing

_LOGGER = logging.getLogger(__name__)


# pylint: disable=unused-variable
class ThreadWithException(threading.Thread):
    """A thread class that supports raising exception in the thread from another thread.

    Based on
    https://stackoverflow.com/questions/323972/is-there-any-way-to-kill-a-thread/49877671

    """

    _THREADING_SHUTDOWN_TIMEOUT: typing.Final = 10

    def raise_exc(self, exctype: typing.Any) -> None:
        """Raise the given exception type in the context of this thread."""
        assert self.ident
        self.async_raise(self.ident, exctype)

    @staticmethod
    def deadlock_safe_shutdown() -> None:
        """Shutdown that will not deadlock."""
        # threading._shutdown can deadlock forever
        # see https://github.com/justengel/continuous_threading#shutdown-update
        # for additional detail
        remaining_threads = [
            thread
            for thread in threading.enumerate()
            if thread is not threading.main_thread()
            and not thread.daemon
            and thread.is_alive()
        ]

        if not remaining_threads:
            return

        timeout_per_thread = ThreadWithException._THREADING_SHUTDOWN_TIMEOUT / len(
            remaining_threads
        )
        for thread in remaining_threads:
            try:
                thread.join(timeout_per_thread)
            except Exception as err:  # pylint: disable=broad-except
                _LOGGER.warning(f"Failed to join thread: {err}")

    @staticmethod
    def async_raise(tid: int, exctype: typing.Any) -> None:
        """Raise an exception in the threads with id tid."""
        if not inspect.isclass(exctype):
            raise TypeError("Only types can be raised (not instances)")

        c_tid = ctypes.c_ulong(tid)  # changed in python 3.7+
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(
            c_tid, ctypes.py_object(exctype)
        )

        if res == 1:
            return

        # "if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"
        ctypes.pythonapi.PyThreadState_SetAsyncExc(c_tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")
