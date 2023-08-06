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
import datetime
import typing

from . import helpers
from .context import Context
from .trace import Trace
from .trace_base import TraceBase
from .trace_element import TraceElement


# pylint: disable=unused-variable
class ActionTrace(TraceBase):
    """Base container for a script or automation trace."""

    def __init__(
        self,
        domain: str,
        item_id: str,
        config: dict[str, typing.Any],
        blueprint_inputs: dict[str, typing.Any],
        context: Context,
    ) -> None:
        """Container for script trace."""
        self._domain = domain
        self._trace: dict[str, collections.deque[TraceElement]] = None
        self._config: dict[str, typing.Any] = config
        self._blueprint_inputs: dict[str, typing.Any] = blueprint_inputs
        self._context: Context = context
        self._error: Exception = None
        self._state: str = "running"
        self._script_execution: str = None
        self._run_id: str = helpers.random_uuid_hex()
        self._timestamp_finish: datetime.datetime = None
        self._timestamp_start: datetime.datetime = helpers.utcnow()
        self._key = f"{self._domain}.{item_id}"
        self._dict: dict[str, typing.Any] = None
        self._short_dict: dict[str, typing.Any] = None
        self._domain: str = None

        if Trace.get_id():
            Trace.set_child_id(self._key, self._run_id)
        Trace.set_id((self._key, self._run_id))

    @property
    def key(self) -> str:
        return self._key

    @property
    def run_id(self) -> str:
        return self._run_id

    @property
    def context(self) -> Context:
        return self._context

    def set_trace(self, trace: dict[str, collections.deque[TraceElement]]) -> None:
        """Set action trace."""
        self._trace = trace

    def set_error(self, ex: Exception) -> None:
        """Set error."""
        self._error = ex

    def finished(self) -> None:
        """Set finish time."""
        self._timestamp_finish = helpers.utcnow()
        self._state = "stopped"
        self._script_execution = Trace.get_stop_reasaon()

    def as_extended_dict(self) -> dict[str, typing.Any]:
        """Return an extended dictionary version of this ActionTrace."""
        if self._dict:
            return self._dict

        result = dict(self.as_short_dict())

        traces = {}
        if self._trace:
            for key, trace_list in self._trace.items():
                traces[key] = [item.as_dict() for item in trace_list]

        result.update(
            {
                "trace": traces,
                "config": self._config,
                "blueprint_inputs": self._blueprint_inputs,
                "context": self._context,
            }
        )

        if self._state == "stopped":
            # Execution has stopped, save the result
            self._dict = result
        return result

    def as_short_dict(self) -> dict[str, typing.Any]:
        """Return a brief dictionary version of this ActionTrace."""
        if self._short_dict:
            return self._short_dict

        last_step = None

        if self._trace:
            last_step = list(self._trace)[-1]
        domain, item_id = self.key.split(".", 1)

        result = {
            "last_step": last_step,
            "run_id": self._run_id,
            "state": self._state,
            "script_execution": self._script_execution,
            "timestamp": {
                "start": self._timestamp_start,
                "finish": self._timestamp_finish,
            },
            "domain": domain,
            "item_id": item_id,
        }
        if self._error is not None:
            result["error"] = str(self._error)

        if self._state == "stopped":
            # Execution has stopped, save the result
            self._short_dict = result
        return result
