"""
Stream Component for Smart Home - The Next Generation.

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
import typing


# pylint: disable=unused-variable
class Diagnostics:
    """Diagnostics for debugging.

    The stream component does not have config entries itself, and all diagnostics
    information is managed by dependent components (e.g. camera)
    """

    def __init__(self) -> None:
        """Initialize Diagnostics."""
        self._counter = collections.Counter()
        self._values = dict[str, typing.Any]()

    def increment(self, key: str) -> None:
        """Increment a counter for the spcified key/event."""
        self._counter.update(collections.Counter({key: 1}))

    def set_value(self, key: str, value: typing.Any) -> None:
        """Update a key/value pair."""
        self._values[key] = value

    def as_dict(self) -> dict[str, typing.Any]:
        """Return diagnostics as a debug dictionary."""
        result = {k: self._counter[k] for k in self._counter}
        result.update(self._values)
        return result
