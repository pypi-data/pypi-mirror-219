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

from .service_call import ServiceCall


# pylint: disable=unused-variable
class ReloadServiceHelper:
    """Helper for reload services to minimize unnecessary reloads."""

    def __init__(
        self,
        service_func: collections.abc.Callable[
            [ServiceCall], collections.abc.Awaitable
        ],
    ) -> None:
        """Initialize ReloadServiceHelper."""
        self._service_func = service_func
        self._service_running = False
        self._service_condition = asyncio.Condition()

    async def execute_service(self, service_call: ServiceCall) -> None:
        """Execute the service.

        If a previous reload task if currently in progress, wait for it to finish first.
        Once the previous reload task has finished, one of the waiting tasks will be
        assigned to execute the reload, the others will wait for the reload to finish.
        """

        do_reload = False
        async with self._service_condition:
            if self._service_running:
                # A previous reload task is already in progress, wait for it to finish
                await self._service_condition.wait()

        async with self._service_condition:
            if not self._service_running:
                # This task will do the reload
                self._service_running = True
                do_reload = True
            else:
                # Another task will perform the reload, wait for it to finish
                await self._service_condition.wait()

        if do_reload:
            # Reload, then notify other tasks
            await self._service_func(service_call)
            async with self._service_condition:
                self._service_running = False
                self._service_condition.notify_all()
