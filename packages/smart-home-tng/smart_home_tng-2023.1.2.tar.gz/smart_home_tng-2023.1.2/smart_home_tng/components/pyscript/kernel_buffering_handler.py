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
import logging.handlers
import typing

_LOGGER: typing.Final = logging.getLogger(__name__)


# pylint: disable=unused-variable
class KernelBufferingHandler(logging.handlers.BufferingHandler):
    """Memory-based handler for logging; send via stdout queue."""

    def __init__(self, housekeep_q: asyncio.Queue):
        """Initialize KernelBufferingHandler instance."""
        super().__init__(0)
        self._housekeep_q = housekeep_q

    def flush(self):
        """Flush is a no-op."""

    def shouldFlush(self, record):
        """Write the buffer to the housekeeping queue."""
        try:
            self._housekeep_q.put_nowait(["stdout", self.format(record)])
        except asyncio.QueueFull:
            _LOGGER.error("housekeep_q unexpectedly full")
