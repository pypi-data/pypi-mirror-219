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

import datetime
import collections
import traceback


# pylint: disable=unused-variable
class LogEntry:
    """Store HA log entries."""

    def __init__(self, record, _stack, source):
        """Initialize a log entry."""
        self._first_occurred = self._timestamp = record.created
        self._name = record.name
        self._level = record.levelname
        self._message = collections.deque([record.getMessage()], maxlen=5)
        self._exception = ""
        self._root_cause = None
        if record.exc_info:
            self._exception = "".join(traceback.format_exception(*record.exc_info))
            _, _, tb = record.exc_info  # pylint: disable=invalid-name
            # Last line of traceback contains the root cause of the exception
            if traceback.extract_tb(tb):
                self._root_cause = str(traceback.extract_tb(tb)[-1])
        self._source = source
        self._count = 1
        self._hash = str([self._name, *self._source, self._root_cause])

    @property
    def count(self) -> int:
        return self._count

    @count.setter
    def count(self, value: int) -> None:
        self._count = value

    @property
    def hash(self) -> str:
        return self._hash

    @property
    def timestamp(self) -> datetime.datetime:
        return self._timestamp

    @timestamp.setter
    def timestamp(self, value: datetime.datetime) -> None:
        self._timestamp = value

    @property
    def message(self) -> collections.deque:
        return self._message

    def to_dict(self):
        """Convert object into dict to maintain backward compatibility."""
        return {
            "name": self._name,
            "message": list(self._message),
            "level": self._level,
            "source": self._source,
            "timestamp": self._timestamp,
            "exception": self._exception,
            "count": self._count,
            "first_occurred": self._first_occurred,
        }
