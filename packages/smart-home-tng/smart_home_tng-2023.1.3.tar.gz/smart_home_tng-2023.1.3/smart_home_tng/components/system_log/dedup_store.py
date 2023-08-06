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

import collections

from .log_entry import LogEntry


# pylint: disable=unused-variable
class DedupStore(collections.OrderedDict[str, LogEntry]):
    """Data store to hold max amount of deduped entries."""

    def __init__(self, maxlen=50):
        """Initialize a new DedupStore."""
        super().__init__()
        self._maxlen = maxlen

    def add_entry(self, entry: LogEntry):
        """Add a new entry."""
        key = entry.hash

        if key in self:
            # Update stored entry
            existing = self[key]
            existing.count += 1
            existing.timestamp = entry.timestamp

            if entry.message[0] not in existing.message:
                existing.message.append(entry.message[0])

            self.move_to_end(key)
        else:
            self[key] = entry

        if len(self) > self._maxlen:
            # Removes the first record which should also be the oldest
            self.popitem(last=False)

    def to_list(self):
        """Return reversed list of log entries - LIFO."""
        return [value.to_dict() for value in reversed(self.values())]
