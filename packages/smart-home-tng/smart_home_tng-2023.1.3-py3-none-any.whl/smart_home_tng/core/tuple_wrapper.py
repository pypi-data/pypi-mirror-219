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

from .result_wrapper import ResultWrapper


# pylint: disable=unused-variable
class TupleWrapper(tuple, ResultWrapper):
    """Wrap a tuple."""

    # This is all magic to be allowed to subclass a tuple.

    def __new__(cls, value: tuple, *, _render_result: str = None):
        """Create a new tuple class."""
        return super().__new__(cls, tuple(value))

    def __init__(self, value: tuple, *, render_result: str = None) -> None:
        """Initialize a new tuple class."""
        super().__init__(value)
        super().__init__(render_result)

    def __str__(self) -> str:
        """Return string representation."""
        if self.render_result is None:
            return super().__str__()

        return self.render_result
