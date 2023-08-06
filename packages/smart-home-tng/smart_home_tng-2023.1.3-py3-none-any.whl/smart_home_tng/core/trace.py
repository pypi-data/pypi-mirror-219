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

import collections
import collections.abc
import contextlib
import contextvars
import copy
import functools
import typing

from .condition_checker_type import ConditionCheckerType
from .stop_reason import StopReason
from .template_vars_type import TemplateVarsType
from .trace_element import TraceElement

# Context variables for tracing
# copy of last variables
_VARIABLES_CV: typing.Final = contextvars.ContextVar[TemplateVarsType](
    "variables_cv", default=None
)
"""Copy of last variables"""

# current trace
_TRACE_CV: typing.Final[
    contextvars.ContextVar[dict[str, collections.deque[TraceElement]]]
] = contextvars.ContextVar("trace_cv", default=None)
"""Current Trace"""

# Stack of TraceElements
_TRACE_STACK_CV: typing.Final[
    contextvars.ContextVar[list[TraceElement]]
] = contextvars.ContextVar("trace_stack_cv", default=None)
"""Stack of TraceElements"""

# Current location in config tree
_TRACE_PATH_STACK_CV: typing.Final[
    contextvars.ContextVar[list[str]]
] = contextvars.ContextVar("trace_path_stack_cv", default=None)
"""Current location in config tree"""

# (domain.item_id, Run ID)
_TRACE_ID_CV: typing.Final[
    contextvars.ContextVar[tuple[str, str]]
] = contextvars.ContextVar("trace_id_cv", default=None)
"""(domain.item_id, Run ID"""

# Reason for stopped script execution
_SCRIPT_EXECUTION_CV: typing.Final[
    contextvars.ContextVar[StopReason]
] = contextvars.ContextVar("script_execution_cv", default=None)
"""Reason for stopped script execution"""


# pylint: disable=unused-variable
class Trace:
    """Helpers for script and condition tracing."""

    @staticmethod
    def create_element(
        variables: TemplateVarsType,
        path: str,
    ) -> TraceElement:
        return TraceElement(variables, path, _VARIABLES_CV)

    @staticmethod
    def set_id(trace_id: tuple[str, str]) -> None:
        """Set id of the current trace."""
        _TRACE_ID_CV.set(trace_id)

    @staticmethod
    def get_id() -> tuple[str, str]:
        """Get id if the current trace."""
        return _TRACE_ID_CV.get()

    @staticmethod
    def stack_push(
        node: typing.Any, trace_stack_var: contextvars.ContextVar = _TRACE_STACK_CV
    ) -> None:
        """Push an element to the top of a trace stack."""
        if (trace_stack := trace_stack_var.get()) is None:
            trace_stack = []
            trace_stack_var.set(trace_stack)
        trace_stack.append(node)

    @staticmethod
    def stack_pop(trace_stack_var: contextvars.ContextVar = _TRACE_STACK_CV) -> None:
        """Remove the top element from a trace stack."""
        trace_stack = trace_stack_var.get()
        trace_stack.pop()

    @staticmethod
    def stack_top(
        trace_stack_var: contextvars.ContextVar = _TRACE_STACK_CV,
    ) -> typing.Any:
        """Return the element at the top of a trace stack."""
        trace_stack = trace_stack_var.get()
        return trace_stack[-1] if trace_stack else None

    @staticmethod
    def path_push(suffix: str | list[str]) -> int:
        """Go deeper in the config tree."""
        if isinstance(suffix, str):
            suffix = [suffix]
        for node in suffix:
            Trace.stack_push(node, _TRACE_PATH_STACK_CV)
        return len(suffix)

    @staticmethod
    def path_pop(count: int) -> None:
        """Go n levels up in the config tree."""
        for _ in range(count):
            Trace.stack_pop(_TRACE_PATH_STACK_CV)

    @staticmethod
    def get_path() -> str:
        """Return a string representing the current location in the config tree."""
        if not (path := _TRACE_PATH_STACK_CV.get()):
            return ""
        return "/".join(path)

    @staticmethod
    def append_element(
        trace_element: TraceElement,
        maxlen: int = None,
    ) -> None:
        """Append a TraceElement to trace[path]."""
        if (trace := _TRACE_CV.get()) is None:
            trace = {}
            _TRACE_CV.set(trace)
        if (path := trace_element.path) not in trace:
            trace[path] = collections.deque(maxlen=maxlen)
        trace[path].append(trace_element)

    @staticmethod
    def get(clear: bool = True) -> dict[str, collections.deque[TraceElement]]:
        """Return the current trace."""
        if clear:
            Trace.clear()
        return _TRACE_CV.get()

    @staticmethod
    def clear() -> None:
        """Clear the trace."""
        _TRACE_CV.set({})
        _TRACE_STACK_CV.set(None)
        _TRACE_PATH_STACK_CV.set(None)
        _VARIABLES_CV.set(None)
        _SCRIPT_EXECUTION_CV.set(StopReason())

    @staticmethod
    def set_child_id(child_key: str, child_run_id: str) -> None:
        """Set child trace_id of TraceElement at the top of the stack."""
        node = typing.cast(TraceElement, Trace.stack_top(_TRACE_STACK_CV))
        if node:
            node.set_child_id(child_key, child_run_id)

    @staticmethod
    def set_result(**kwargs: typing.Any) -> None:
        """Set the result of TraceElement at the top of the stack."""
        node = typing.cast(TraceElement, Trace.stack_top(_TRACE_STACK_CV))
        if node is not None:
            node.set_result(**kwargs)

    @staticmethod
    def set_condition_result(result: bool, **kwargs: typing.Any) -> None:
        node = Trace.stack_top(_TRACE_STACK_CV)

        # The condition function may be called directly, in which case tracing
        # is not setup
        if not node:
            return

        node.set_result(result=result, **kwargs)

    @staticmethod
    def update_result(**kwargs: typing.Any) -> None:
        """Update the result of TraceElement at the top of the stack."""
        node = typing.cast(TraceElement, Trace.stack_top(_TRACE_STACK_CV))
        if node is not None:
            node.update_result(**kwargs)

    @staticmethod
    def set_stop_reason(reason: str) -> None:
        """Set stop reason."""
        if (data := _SCRIPT_EXECUTION_CV.get()) is None:
            return
        data.script_execution = reason

    @staticmethod
    def get_stop_reasaon() -> str:
        """Return the stop reason."""
        if (data := _SCRIPT_EXECUTION_CV.get()) is None:
            return None
        return data.script_execution

    @staticmethod
    @contextlib.contextmanager
    def path(suffix: str | list[str]) -> collections.abc.Generator:
        """Go deeper in the config tree.

        Can not be used as a decorator on couroutine functions.
        """
        count = Trace.path_push(suffix)
        try:
            yield
        finally:
            Trace.path_pop(count)

    @staticmethod
    def async_path(suffix: str | list[str]) -> collections.abc.Callable:
        """Go deeper in the config tree.

        To be used as a decorator on coroutine functions.
        """

        def _trace_path_decorator(
            func: collections.abc.Callable,
        ) -> collections.abc.Callable:
            """Decorate a coroutine function."""

            @functools.wraps(func)
            async def async_wrapper(*args: typing.Any) -> None:
                """Catch and log exception."""
                with Trace.path(suffix):
                    await func(*args)

            return async_wrapper

        return _trace_path_decorator

    @staticmethod
    def condition_function(condition: ConditionCheckerType) -> ConditionCheckerType:
        """Wrap a condition function to enable basic tracing."""

        @functools.wraps(condition)
        def wrapper(variables: TemplateVarsType = None) -> bool:
            """Trace condition."""
            with Trace.condition(variables):
                result = condition(variables)
                Trace.update_result(result=result)
                return result

        return wrapper

    @contextlib.contextmanager
    @staticmethod
    def condition(
        variables: TemplateVarsType,
    ) -> collections.abc.Generator[TraceElement, None, None]:
        """Trace condition evaluation."""
        should_pop = True
        trace_element = Trace.stack_top()
        if trace_element and trace_element.reuse_by_child:
            should_pop = False
            trace_element.reuse_by_child = False
        else:
            trace_element = Trace.append_condition(variables, Trace.get_path())
            Trace.stack_push(trace_element)
        try:
            yield trace_element
        except Exception as ex:
            trace_element.set_error(ex)
            raise ex
        finally:
            if should_pop:
                Trace.stack_pop()

    @staticmethod
    def append_condition(variables: TemplateVarsType, path: str) -> TraceElement:
        """Append a TraceElement to trace[path]."""
        trace_element = TraceElement(variables, path, _VARIABLES_CV)
        Trace.append_element(trace_element)
        return trace_element

    @staticmethod
    def start_parallel_run():
        _TRACE_PATH_STACK_CV.set(copy.copy(_TRACE_PATH_STACK_CV.get()))
