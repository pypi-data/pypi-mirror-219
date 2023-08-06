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
import datetime
import functools
import threading
import typing

from . import helpers


# pylint: disable=unused-variable
class Throttle:
    """A class for throttling the execution of tasks.

    This method decorator adds a cooldown to a method to prevent it from being
    called more then 1 time within the timedelta interval `min_time` after it
    returned its result.

    Calling a method a second time during the interval will return None.

    Pass keyword argument `no_throttle=True` to the wrapped method to make
    the call not throttled.

    Decorator takes in an optional second timedelta interval to throttle the
    'no_throttle' calls.

    Adds a datetime attribute `last_call` to the method.
    """

    def __init__(
        self,
        min_time: datetime.timedelta,
        limit_no_throttle: datetime.timedelta = None,
    ) -> None:
        """Initialize the throttle."""
        self.min_time = min_time
        self.limit_no_throttle = limit_no_throttle

    def __call__(self, method: typing.Callable) -> typing.Callable:
        """Caller for the throttle."""
        # Make sure we return a coroutine if the method is async.
        if asyncio.iscoroutinefunction(method):

            async def throttled_value() -> None:
                """Stand-in function for when real func is being throttled."""
                return None

        else:

            def throttled_value() -> None:  # type: ignore[misc]
                """Stand-in function for when real func is being throttled."""
                return None

        if self.limit_no_throttle is not None:
            method = Throttle(self.limit_no_throttle)(method)

        # Different methods that can be passed in:
        #  - a function
        #  - an unbound function on a class
        #  - a method (bound function on a class)

        # We want to be able to differentiate between function and unbound
        # methods (which are considered functions).
        # All methods have the classname in their qualname separated by a '.'
        # Functions have a '.' in their qualname if defined inline, but will
        # be prefixed by '.<locals>.' so we strip that out.
        is_func = (
            not hasattr(method, "__self__")
            and "." not in method.__qualname__.split(".<locals>.")[-1]
        )

        @functools.wraps(method)
        def wrapper(
            *args: typing.Any, **kwargs: typing.Any
        ) -> typing.Callable | typing.Coroutine:
            """Wrap that allows wrapped to be called only once per min_time.

            If we cannot acquire the lock, it is running so return None.
            """
            if hasattr(method, "__self__"):
                host = getattr(method, "__self__")
            elif is_func:
                host = wrapper
            else:
                host = args[0] if args else wrapper

            # pylint: disable=protected-access # to _throttle
            if not hasattr(host, "_throttle"):
                host._throttle = {}

            if id(self) not in host._throttle:
                host._throttle[id(self)] = [threading.Lock(), None]
            throttle = host._throttle[id(self)]
            # pylint: enable=protected-access

            if not throttle[0].acquire(False):
                return throttled_value()

            # Check if method is never called or no_throttle is given
            force = kwargs.pop("no_throttle", False) or not throttle[1]

            try:
                if force or helpers.utcnow() - throttle[1] > self.min_time:
                    result = method(*args, **kwargs)
                    throttle[1] = helpers.utcnow()
                    return result  # type: ignore[no-any-return]

                return throttled_value()
            finally:
                throttle[0].release()

        return wrapper
