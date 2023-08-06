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

import asyncio
import collections.abc
import functools
import typing

from .smart_home_controller import SmartHomeController

_T = typing.TypeVar("_T")

_FUNC: typing.Final = collections.abc.Callable[[], _T]
_SHC_FUNC: typing.Final = collections.abc.Callable[[SmartHomeController], _T]


@typing.overload
class Singleton:
    ...


# pylint: disable=unused-variable
class Singleton:
    """Helper to implement singletons in threaded environment."""

    data: typing.Any = None

    @staticmethod
    def singleton(helper: Singleton) -> collections.abc.Callable[[_FUNC], _FUNC]:
        """Decorate a function that should be called once per instance.

        Result will be cached and simultaneous calls will be handled.
        """

        def wrapper(func: _FUNC) -> _FUNC:
            """Wrap a function with caching logic."""
            if not asyncio.iscoroutinefunction(func):

                @functools.wraps(func)
                def wrapped() -> _T:
                    if helper.data is None:
                        helper.data = func()
                    return typing.cast(_T, helper.data)

                return wrapped

            @functools.wraps(func)
            async def async_wrapped() -> _T:
                if helper.data is None:
                    evt = helper.data = asyncio.Event()
                    result = await func()
                    helper.data = result
                    evt.set()
                    return typing.cast(_T, result)

                obj_or_evt = helper.data

                if isinstance(obj_or_evt, asyncio.Event):
                    await obj_or_evt.wait()
                    return typing.cast(_T, helper.data)

                return typing.cast(_T, obj_or_evt)

            return async_wrapped

        return wrapper

    @staticmethod
    def shc_singleton(
        helper: Singleton,
    ) -> collections.abc.Callable[[_SHC_FUNC], _SHC_FUNC]:
        """Decorate a function that should be called once per instance.

        Result will be cached and simultaneous calls will be handled.
        """

        def wrapper(func: _SHC_FUNC) -> _SHC_FUNC:
            """Wrap a function with caching logic."""
            if not asyncio.iscoroutinefunction(func):

                @functools.wraps(func)
                def wrapped(shc: SmartHomeController) -> _T:
                    if helper.data is None:
                        helper.data = func(shc)
                    return typing.cast(_T, helper.data)

                return wrapped

            @functools.wraps(func)
            async def async_wrapped(shc: SmartHomeController) -> _T:
                if helper.data is None:
                    evt = helper.data = asyncio.Event()
                    result = await func(shc)
                    helper.data = result
                    evt.set()
                    return typing.cast(_T, result)

                obj_or_evt = helper.data

                if isinstance(obj_or_evt, asyncio.Event):
                    await obj_or_evt.wait()
                    return typing.cast(_T, helper.data)

                return typing.cast(_T, obj_or_evt)

            return async_wrapped

        return wrapper
