"""
PyScript Component for Smart Home - The Next Generation.

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


This component is based on the custom_component

Pyscript: Python Scripting for Home Assistant, Copyright (c) 2020-2022 Craig Barrat,
which may be freely used and copied according tho the terms of the Apache 2.0 License.

Original source code and documentation can be found under:
https://github.com/custom-components/pyscript
"""

import asyncio
import logging
import typing
import watchdog.events

from ... import core

_LOGGER: typing.Final = logging.getLogger(__name__)


# pylint: disable=unused-variable
class WatchdogHandler(watchdog.events.FileSystemEventHandler):
    """Class for handling watchdog events."""

    def __init__(
        self, shc: core.SmartHomeController, watchdog_q: asyncio.Queue
    ) -> None:
        self._watchdog_q = watchdog_q
        self._shc = shc

    def process(self, event: watchdog.events.FileSystemEvent) -> None:
        """Send watchdog events to main loop task."""
        _LOGGER.debug(f"watchdog process({event})")
        self._shc.call_soon_threadsafe(self._watchdog_q.put_nowait, event)

    def on_modified(self, event: watchdog.events.FileSystemEvent) -> None:
        """File modified."""
        self.process(event)

    def on_moved(self, event: watchdog.events.FileSystemEvent) -> None:
        """File moved."""
        self.process(event)

    def on_created(self, event: watchdog.events.FileSystemEvent) -> None:
        """File created."""
        self.process(event)

    def on_deleted(self, event: watchdog.events.FileSystemEvent) -> None:
        """File deleted."""
        self.process(event)
