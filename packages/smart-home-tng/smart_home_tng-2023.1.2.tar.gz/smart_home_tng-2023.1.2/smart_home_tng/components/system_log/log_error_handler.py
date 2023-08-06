"""
System Log Component for Smart Home - The Next Generation.

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

import logging
import re
import traceback

from ... import __path__ as ROOT_PATH
from ... import core
from .const import Const
from .dedup_store import DedupStore
from .log_entry import LogEntry


# pylint: disable=unused-variable
class LogErrorHandler(logging.Handler):
    """Log handler for error messages."""

    def __init__(self, shc: core.SmartHomeController, maxlen: int, fire_event: bool):
        """Initialize a new LogErrorHandler."""
        super().__init__()
        self._shc = shc
        self._records = DedupStore(maxlen=maxlen)
        self._fire_event = fire_event

    @property
    def records(self) -> DedupStore:
        return self._records

    def emit(self, record):
        """Save error and warning logs.

        Everything logged with error or warning is saved in local buffer. A
        default upper limit is set to 50 (older entries are discarded) but can
        be changed if needed.
        """
        stack = []
        if not record.exc_info:
            stack = [(f[0], f[1]) for f in traceback.extract_stack()]

        entry = LogEntry(record, stack, _figure_out_source(record, stack, self._shc))
        self._records.add_entry(entry)
        if self._fire_event:
            self._shc.bus.fire(Const.EVENT_SYSTEM_LOG, entry.to_dict())


def _figure_out_source(record, call_stack, shc: core.SmartHomeController):
    paths = [ROOT_PATH[0], shc.config.config_dir]

    # If a stack trace exists, extract file names from the entire call stack.
    # The other case is when a regular "log" is made (without an attached
    # exception). In that case, just use the file where the log was made from.
    if record.exc_info:
        stack = [(x[0], x[1]) for x in traceback.extract_tb(record.exc_info[2])]
    else:
        index = -1
        for i, frame in enumerate(call_stack):
            if frame[0] == record.pathname:
                index = i
                break
        if index == -1:
            # For some reason we couldn't find pathname in the stack.
            stack = [(record.pathname, record.lineno)]
        else:
            stack = call_stack[0 : index + 1]

    # Iterate through the stack call (in reverse) and find the last call from
    # a file in Home Assistant. Try to figure out where error happened.
    x = "|".join([re.escape(x) for x in paths])
    paths_re = rf"(?:{x})/(.*)"
    for pathname in reversed(stack):
        # Try to match with a file within Home Assistant
        if match := re.match(paths_re, pathname[0]):
            return [match.group(1), pathname[1]]
    # Ok, we don't know what this is
    return (record.pathname, record.lineno)
