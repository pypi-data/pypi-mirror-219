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

import voluptuous as vol

from .context import Context
from .smart_home_controller_job import SmartHomeControllerJob
from .service_call import ServiceCall


# pylint: disable=unused-variable
class ServiceDescription:
    """Representation of a callable service."""

    __slots__ = ["job", "schema", "context"]

    def __init__(
        self,
        func: typing.Callable[[ServiceCall], None | collections.abc.Awaitable[None]],
        schema: vol.Schema,
        context: Context = None,
    ) -> None:
        """Initialize a service."""
        self.job = SmartHomeControllerJob(func)
        self.schema = schema
        self.context = context or Context()
