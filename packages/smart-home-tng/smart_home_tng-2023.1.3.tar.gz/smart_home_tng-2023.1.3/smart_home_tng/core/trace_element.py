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

import contextvars
import typing

from . import helpers
from .template_vars_type import TemplateVarsType


# pylint: disable=unused-variable
class TraceElement:
    """Container for trace data."""

    def __init__(
        self,
        variables: TemplateVarsType,
        path: str,
        variables_cv: contextvars.ContextVar[TemplateVarsType],
    ) -> None:
        """Container for trace data."""
        self._child_key: str = None
        self._child_run_id: str = None
        self._error: Exception = None
        self._path: str = path
        self._result: dict[str, typing.Any] = None
        self._reuse_by_child = False
        self._timestamp = helpers.utcnow()

        if variables is None:
            variables = {}
        if variables_cv is not None:
            cv = variables_cv
            last_variables = cv.get() or {}
            cv.set(dict(variables))
        else:
            last_variables = {}

        changed_variables = {
            key: value
            for key, value in variables.items()
            if key not in last_variables or last_variables[key] != value
        }
        self._variables = changed_variables

    @property
    def path(self) -> str:
        return self._path

    def __repr__(self) -> str:
        """Container for trace data."""
        return str(self.as_dict())

    def set_child_id(self, child_key: str, child_run_id: str) -> None:
        """Set trace id of a nested script run."""
        self._child_key = child_key
        self._child_run_id = child_run_id

    def set_error(self, ex: Exception) -> None:
        """Set error."""
        self._error = ex

    def set_result(self, **kwargs: typing.Any) -> None:
        """Set result."""
        self._result = {**kwargs}

    def update_result(self, **kwargs: typing.Any) -> None:
        """Set result."""
        old_result = self._result or {}
        self._result = {**old_result, **kwargs}

    def as_dict(self) -> dict[str, typing.Any]:
        """Return dictionary version of this TraceElement."""
        result: dict[str, typing.Any] = {
            "path": self._path,
            "timestamp": self._timestamp,
        }
        if self._child_key is not None:
            domain, item_id = self._child_key.split(".", 1)
            result["child_id"] = {
                "domain": domain,
                "item_id": item_id,
                "run_id": str(self._child_run_id),
            }
        if self._variables:
            result["changed_variables"] = self._variables
        if self._error is not None:
            result["error"] = str(self._error)
        if self._result is not None:
            result["result"] = self._result
        return result
