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

import typing

from . import helpers
from .context import Context
from .read_only_dict import ReadOnlyDict


# pylint: disable=unused-variable
class ServiceCall:
    """Representation of a call to a service."""

    __slots__ = ["_domain", "_service", "_data", "_context"]

    def __init__(
        self,
        domain: str,
        service: str,
        data: dict[str, typing.Any] = None,
        context: Context = None,
    ) -> None:
        """Initialize a service call."""
        self._domain = domain.lower()
        self._service = service.lower()
        self._data = ReadOnlyDict(data or {})
        self._context = context or Context()

    @property
    def data(self) -> dict[str, typing.Any]:
        return self._data

    @property
    def context(self) -> Context:
        return self._context

    @property
    def domain(self) -> str:
        return self._domain

    @property
    def service(self) -> str:
        return self._service

    def __repr__(self) -> str:
        """Return the representation of the service."""
        if self._data:
            return (
                f"<ServiceCall {self._domain}.{self._service} "
                f"(c:{self._context.context_id}): {helpers.repr_helper(self._data)}>"
            )

        return f"<ServiceCall {self._domain}.{self._service} (c:{self._context.context_id})>"
