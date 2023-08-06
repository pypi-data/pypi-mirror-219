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

import dataclasses
import typing

from .callback import callback

if not typing.TYPE_CHECKING:

    class SystemHealthComponent:
        pass


if typing.TYPE_CHECKING:
    from .system_health_component import SystemHealthComponent


# pylint: disable=unused-variable
@dataclasses.dataclass()
class SystemHealthRegistration:
    """Helper class to track platform registration."""

    def __init__(
        self,
        owner: SystemHealthComponent,
        domain: str,
    ) -> None:
        self._owner = owner
        self._domain = domain
        self._info_callback: typing.Callable[[], typing.Awaitable[dict]] = None
        self._manage_url: str = None

    @property
    def domain(self) -> str:
        return self._domain

    @property
    def info_callback(self) -> typing.Callable[[], typing.Awaitable[dict]]:
        return self._info_callback

    @callback
    def async_register_info(
        self,
        info_callback: typing.Callable[[], typing.Awaitable[dict]],
        manage_url: str = None,
    ):
        """Register an info callback."""
        self._info_callback = info_callback
        self._manage_url = manage_url
        self._owner.register_info(self)
