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

import collections.abc
import attr

from .condition_error import ConditionError


# pylint: disable=unused-variable
@attr.s
class ConditionErrorIndex(ConditionError):
    """Condition error with index."""

    # The zero-based index of the failed condition, for conditions with multiple parts
    index: int = attr.ib()
    # The total number of parts in this condition, including non-failed parts
    total: int = attr.ib()
    # The error that this error wraps
    error: ConditionError = attr.ib()

    def output(self, indent: int) -> collections.abc.Generator[str, None, None]:
        """Yield an indented representation."""
        if self.total > 1:
            yield self._indent(
                indent, f"In '{self.type}' (item {self.index+1} of {self.total}):"
            )
        else:
            yield self._indent(indent, f"In '{self.type}':")

        yield from self.error.output(indent + 1)
