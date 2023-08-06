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
import traceback
import typing

from . import helpers
from .callback import callback
from .interruptible_thread_pool_executor import InterruptibleThreadPoolExecutor

_MAX_EXECUTOR_WORKERS: typing.Final = 64


# pylint: disable=unused-variable
class EventLoopPolicy(asyncio.DefaultEventLoopPolicy):
    """Event loop policy for Home Assistant."""

    def __init__(self, debug: bool) -> None:
        """Init the event loop policy."""
        super().__init__()
        self._debug = debug

    @property
    def loop_name(self) -> str:
        """Return name of the loop."""
        return self._loop_factory.__name__

    def new_event_loop(self) -> asyncio.AbstractEventLoop:
        """Get the event loop."""
        loop: asyncio.AbstractEventLoop = super().new_event_loop()
        loop.set_exception_handler(self._async_loop_exception_handler)
        if self._debug:
            loop.set_debug(True)

        executor = InterruptibleThreadPoolExecutor(
            thread_name_prefix="SyncWorker", max_workers=_MAX_EXECUTOR_WORKERS
        )
        loop.set_default_executor(executor)
        loop.set_default_executor = helpers.warn_use(
            loop.set_default_executor, "sets default executor on the event loop"
        )
        return loop

    @staticmethod
    @callback
    def _async_loop_exception_handler(
        _: typing.Any, context: dict[str, typing.Any]
    ) -> None:
        """Handle all exception inside the core loop."""
        kwargs = {}
        if exception := context.get("exception"):
            kwargs["exc_info"] = (type(exception), exception, exception.__traceback__)

        logger = logging.getLogger(__package__)
        if source_traceback := context.get("source_traceback"):
            stack_summary = "".join(traceback.format_list(source_traceback))
            logger.error(
                f"Error doing job: {context['message']}: {stack_summary}", **kwargs
            )
            return

        logger.error(f"Error doing job: {context['message']}", **kwargs)
