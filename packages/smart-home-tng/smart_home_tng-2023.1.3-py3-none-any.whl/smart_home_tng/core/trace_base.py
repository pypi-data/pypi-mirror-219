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
import typing

from .context import Context


# pylint: disable=unused-variable
class TraceBase(abc.ABC):
    """Base container for a script or automation trace."""

    @property
    @abc.abstractmethod
    def context(self) -> Context:
        """Return the trace context."""

    @property
    @abc.abstractmethod
    def key(self) -> str:
        """Return the key."""

    def as_dict(self) -> dict[str, typing.Any]:
        """Return an dictionary version of this ActionTrace for saving."""
        return {
            "extended_dict": self.as_extended_dict(),
            "short_dict": self.as_short_dict(),
        }

    @abc.abstractmethod
    def as_extended_dict(self) -> dict[str, typing.Any]:
        """Return an extended dictionary version of this ActionTrace."""

    @abc.abstractmethod
    def as_short_dict(self) -> dict[str, typing.Any]:
        """Return a brief dictionary version of this ActionTrace."""
