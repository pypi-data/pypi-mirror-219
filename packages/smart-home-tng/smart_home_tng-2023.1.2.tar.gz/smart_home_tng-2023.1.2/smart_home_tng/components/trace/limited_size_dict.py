"""
Trace Component for Smart Home - The Next Generation.

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


# pylint: disable=unused-variable
class LimitedSizeDict(collections.OrderedDict):
    """OrderedDict limited in size."""

    def __init__(self, *args, **kwds):
        """Initialize OrderedDict limited in size."""
        self._size_limit = kwds.pop("size_limit", None)
        super().__init__(*args, **kwds)
        self._check_size_limit()

    def __setitem__(self, key, value):
        """Set item and check dict size."""
        super().__setitem__(key, value)
        self._check_size_limit()

    def _check_size_limit(self):
        """Check dict size and evict items in FIFO order if needed."""
        if self._size_limit is not None:
            while len(self) > self._size_limit:
                self.popitem(last=False)

    @property
    def size_limit(self) -> int:
        return self._size_limit
