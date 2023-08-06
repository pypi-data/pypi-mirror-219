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
import typing

_KT = typing.TypeVar("_KT", bound=collections.abc.Hashable)
_VT = typing.TypeVar("_VT", bound=typing.Callable[..., typing.Any])


# pylint: disable=unused-variable
class Registry(dict[_KT, _VT]):
    """Registry of items."""

    def register(self, name: _KT) -> typing.Callable[[_VT], _VT]:
        """Return decorator to register item with a specific name."""

        def decorator(func: _VT) -> _VT:
            """Register decorated function."""
            self[name] = func
            return func

        return decorator
