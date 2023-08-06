"""
Helpers for Components of Smart Home - The Next Generation.

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
import inspect
import logging
import traceback
import typing

from ..callback import callback, is_callback

_T = typing.TypeVar("_T")

# pylint: disable=unused-variable


def log_exception(
    format_err: collections.abc.Callable[..., typing.Any], *args: typing.Any
) -> None:
    """Log an exception with additional context."""
    module = inspect.getmodule(inspect.stack(context=0)[1].frame)
    if module is not None:
        module_name = module.__name__
    else:
        # If Python is unable to access the sources files, the call stack frame
        # will be missing information, so let's guard.
        # https://github.com/home-assistant/core/issues/24982
        module_name = __name__

    # Do not print the wrapper in the traceback
    frames = len(inspect.trace()) - 1
    exc_msg = traceback.format_exc(-frames)
    friendly_msg = format_err(*args)
    logging.getLogger(module_name).error(f"{friendly_msg}\n{exc_msg}")


@typing.overload
def catch_log_exception(
    func: collections.abc.Callable[
        ..., collections.abc.Coroutine[typing.Any, typing.Any, typing.Any]
    ],
    format_err: collections.abc.Callable[..., typing.Any],
    *args: typing.Any,
) -> collections.abc.Callable[
    ..., collections.abc.Coroutine[typing.Any, typing.Any, None]
]:
    """Overload for Callables that return a Coroutine."""


@typing.overload
def catch_log_exception(
    func: collections.abc.Callable[..., typing.Any],
    format_err: collections.abc.Callable[..., typing.Any],
    *args: typing.Any,
) -> collections.abc.Callable[
    ..., None | collections.abc.Coroutine[typing.Any, typing.Any, None]
]:
    """Overload for Callables that return Any."""


def catch_log_exception(
    func: collections.abc.Callable[..., typing.Any],
    format_err: collections.abc.Callable[..., typing.Any],
    *_args: typing.Any,
) -> collections.abc.Callable[
    ..., None | collections.abc.Coroutine[typing.Any, typing.Any, None]
]:
    """Decorate a callback to catch and log exceptions."""

    # Check for partials to properly determine if coroutine function
    check_func = func
    while isinstance(check_func, functools.partial):
        check_func = check_func.func

    wrapper_func: collections.abc.Callable[
        ..., None | collections.abc.Coroutine[typing.Any, typing.Any, None]
    ]
    if asyncio.iscoroutinefunction(check_func):
        async_func = typing.cast(
            collections.abc.Callable[
                ..., collections.abc.Coroutine[typing.Any, typing.Any, None]
            ],
            func,
        )

        @functools.wraps(async_func)
        async def async_wrapper(*args: typing.Any) -> None:
            """Catch and log exception."""
            try:
                await async_func(*args)
            except Exception:  # pylint: disable=broad-except
                log_exception(format_err, *args)

        wrapper_func = async_wrapper

    else:

        @functools.wraps(func)
        def wrapper(*args: typing.Any) -> None:
            """Catch and log exception."""
            try:
                func(*args)
            except Exception:  # pylint: disable=broad-except
                log_exception(format_err, *args)

        if is_callback(check_func):
            wrapper = callback(wrapper)

        wrapper_func = wrapper
    return wrapper_func


def catch_log_coro_exception(
    target: collections.abc.Coroutine[typing.Any, typing.Any, _T],
    format_err: collections.abc.Callable[..., typing.Any],
    *args: typing.Any,
) -> collections.abc.Coroutine[typing.Any, typing.Any, _T]:
    """Decorate a coroutine to catch and log exceptions."""

    async def coro_wrapper(*args: typing.Any) -> _T:
        """Catch and log exception."""
        try:
            return await target
        except Exception:  # pylint: disable=broad-except
            log_exception(format_err, *args)
            return None

    return coro_wrapper(*args)


def async_create_catching_coro(
    target: collections.abc.Coroutine[typing.Any, typing.Any, _T]
) -> collections.abc.Coroutine[typing.Any, typing.Any, _T]:
    """Wrap a coroutine to catch and log exceptions.

    The exception will be logged together with a stacktrace of where the
    coroutine was wrapped.

    target: target coroutine.
    """
    trace = traceback.extract_stack()
    wrapped_target = catch_log_coro_exception(
        target,
        lambda: f"Exception in {target.__name__} called from\n"
        + f"{''.join(traceback.format_list(trace[:-1]))}",
    )

    return wrapped_target
