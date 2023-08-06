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

import abc
import collections.abc
import attr

from .smart_home_controller_error import SmartHomeControllerError


# pylint: disable=unused-variable
@attr.s
class ConditionError(SmartHomeControllerError, abc.ABC):
    """Error during condition evaluation."""

    # The type of the failed condition, such as 'and' or 'numeric_state'
    type: str = attr.ib()

    @staticmethod
    def _indent(indent: int, message: str) -> str:
        """Return indentation."""
        return "  " * indent + message

    @abc.abstractmethod
    def output(self, indent: int) -> collections.abc.Generator[str, None, None]:
        """Yield an indented representation."""

    def __str__(self) -> str:
        """Return string representation."""
        return "\n".join(list(self.output(indent=0)))
