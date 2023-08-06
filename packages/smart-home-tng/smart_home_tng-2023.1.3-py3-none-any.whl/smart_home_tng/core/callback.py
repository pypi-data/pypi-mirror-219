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

# pylint: disable=unused-variable

import collections.abc
import typing

_CallableT = typing.TypeVar(
    "_CallableT", bound=collections.abc.Callable[..., typing.Any]
)


def callback(func: _CallableT) -> _CallableT:
    """Annotation to mark method as safe to call from within the event loop."""
    setattr(func, "_smart_home_tng_callback", True)
    return func


def is_callback(func: collections.abc.Callable[..., typing.Any]) -> bool:
    """Check if function is safe to be called in the event loop."""
    attr = getattr(func, "_smart_home_tng_callback", False)
    return attr
