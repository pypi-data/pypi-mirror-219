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
import logging
import typing

import voluptuous as vol

from .callback import callback
from .const import Const
from .context import Context
from .service_call import ServiceCall
from .service_description import ServiceDescription
from .service_not_found import ServiceNotFound
from .smart_home_controller_job_type import SmartHomeControllerJobType
from .unauthorized import Unauthorized

_LOGGER: typing.Final = logging.getLogger(__name__)
# How long we wait for the result of a service call
_SERVICE_CALL_LIMIT: typing.Final = 10  # seconds


if not typing.TYPE_CHECKING:

    class SmartHomeController:
        ...


if typing.TYPE_CHECKING:
    from .smart_home_controller import SmartHomeController


# pylint: disable=unused-variable
class ServiceRegistry:
    """Offer the services over the eventbus."""

    SERVICE_CALL_LIMIT: typing.Final = _SERVICE_CALL_LIMIT

    def __init__(self, shc: SmartHomeController) -> None:
        """Initialize a service registry."""
        self._services: dict[str, dict[str, ServiceDescription]] = {}
        self._shc = shc

    @property
    def services(self) -> dict[str, dict[str, ServiceDescription]]:
        """Return dictionary with per domain a list of available services."""
        return self._shc.run_callback_threadsafe(self.async_services).result()

    @callback
    def async_services(self) -> dict[str, dict[str, ServiceDescription]]:
        """Return dictionary with per domain a list of available services.

        This method must be run in the event loop.
        """
        return {domain: service.copy() for domain, service in self._services.items()}

    def has_service(self, domain: str, service: str) -> bool:
        """Test if specified service exists.

        Async friendly.
        """
        return service.lower() in self._services.get(domain.lower(), [])

    def register(
        self,
        domain: str,
        service: str,
        service_func: typing.Callable[[ServiceCall], collections.abc.Awaitable[None]],
        schema: vol.Schema = None,
    ) -> None:
        """
        Register a service.

        Schema is called to coerce and validate the service data.
        """
        self._shc.run_callback_threadsafe(
            self.async_register, domain, service, service_func, schema
        ).result()

    @callback
    def async_register(
        self,
        domain: str,
        service: str,
        service_func: typing.Callable[[ServiceCall], collections.abc.Awaitable[None]],
        schema: vol.Schema = None,
    ) -> None:
        """
        Register a service.

        Schema is called to coerce and validate the service data.

        This method must be run in the event loop.
        """
        domain = domain.lower()
        service = service.lower()
        service_obj = ServiceDescription(service_func, schema)

        if domain in self._services:
            self._services[domain][service] = service_obj
        else:
            self._services[domain] = {service: service_obj}

        self._shc.bus.async_fire(
            Const.EVENT_SERVICE_REGISTERED,
            {Const.ATTR_DOMAIN: domain, Const.ATTR_SERVICE: service},
        )

    def remove(self, domain: str, service: str) -> None:
        """Remove a registered service from service handler."""
        self._shc.run_callback_threadsafe(self.async_remove, domain, service).result()

    @callback
    def async_remove(self, domain: str, service: str) -> None:
        """Remove a registered service from service handler.

        This method must be run in the event loop.
        """
        domain = domain.lower()
        service = service.lower()

        if service not in self._services.get(domain, {}):
            _LOGGER.warning(f"Unable to remove unknown service {domain}/{service}")
            return

        self._services[domain].pop(service)

        if not self._services[domain]:
            self._services.pop(domain)

        self._shc.bus.async_fire(
            Const.EVENT_SERVICE_REMOVED,
            {Const.ATTR_DOMAIN: domain, Const.ATTR_SERVICE: service},
        )

    def call(
        self,
        domain: str,
        service: str,
        service_data: dict[str, typing.Any] = None,
        blocking: bool = False,
        context: Context = None,
        limit: float = _SERVICE_CALL_LIMIT,
        target: dict[str, typing.Any] = None,
    ) -> bool:
        """
        Call a service.

        See description of async_call for details.
        """
        return self._shc.run_coroutine_threadsafe(
            self.async_call(
                domain, service, service_data, blocking, context, limit, target
            )
        ).result()

    async def async_call(
        self,
        domain: str,
        service: str,
        service_data: dict[str, typing.Any] = None,
        blocking: bool = False,
        context: Context = None,
        limit: float = _SERVICE_CALL_LIMIT,
        target: dict[str, typing.Any] = None,
    ) -> bool:
        """
        Call a service.

        Specify blocking=True to wait until service is executed.
        Waits a maximum of limit, which may be None for no timeout.

        If blocking = True, will return boolean if service executed
        successfully within limit.

        This method will fire an event to indicate the service has been called.

        Because the service is sent as an event you are not allowed to use
        the keys ATTR_DOMAIN and ATTR_SERVICE in your service_data.

        This method is a coroutine.
        """
        domain = domain.lower()
        service = service.lower()
        context = context or Context()
        service_data = service_data or {}

        try:
            handler = self._services[domain][service]
        except KeyError:
            raise ServiceNotFound(domain, service) from None

        if target:
            service_data.update(target)

        if handler.schema:
            try:
                processed_data: dict[str, typing.Any] = handler.schema(service_data)
            except vol.Invalid:
                _LOGGER.debug(
                    f"Invalid data for service call {domain}.{service}: {service_data}"
                )
                raise
        else:
            processed_data = service_data

        service_call = ServiceCall(domain, service, processed_data, context)

        self._shc.bus.async_fire(
            Const.EVENT_CALL_SERVICE,
            {
                Const.ATTR_DOMAIN: domain.lower(),
                Const.ATTR_SERVICE: service.lower(),
                Const.ATTR_SERVICE_DATA: service_data,
            },
            context=context,
        )

        coro = self._execute_service(handler, service_call)
        if not blocking:
            self._run_service_in_background(coro, service_call)
            return None

        task = self._shc.async_create_task(coro)
        try:
            await asyncio.wait({task}, timeout=limit)
        except asyncio.CancelledError:
            # Task calling us was cancelled, so cancel service call task, and wait for
            # it to be cancelled, within reason, before leaving.
            _LOGGER.debug(f"Service call was cancelled: {service_call}")
            task.cancel()
            await asyncio.wait({task}, timeout=_SERVICE_CALL_LIMIT)
            raise

        if task.cancelled():
            # Service call task was cancelled some other way, such as during shutdown.
            _LOGGER.debug(f"Service was cancelled: {service_call}")
            raise asyncio.CancelledError
        if task.done():
            # Propagate any exceptions that might have happened during service call.
            task.result()
            # Service call completed successfully!
            return True
        # Service call task did not complete before timeout expired.
        # Let it keep running in background.
        self._run_service_in_background(task, service_call)
        _LOGGER.debug(f"Service did not complete before timeout: {service_call}")
        return False

    def _run_service_in_background(
        self,
        coro_or_task: typing.Coroutine[typing.Any, typing.Any, None]
        | asyncio.Task[None],
        service_call: ServiceCall,
    ) -> None:
        """Run service call in background, catching and logging any exceptions."""

        async def catch_exceptions() -> None:
            try:
                await coro_or_task
            except Unauthorized:
                _LOGGER.warning(
                    f"Unauthorized service called {service_call.domain}/{service_call.service}"
                )
            except asyncio.CancelledError:
                _LOGGER.debug(f"Service was cancelled: {service_call}")
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception(f"Error executing service: {service_call}")

        self._shc.async_create_task(catch_exceptions())

    async def _execute_service(
        self, handler: ServiceDescription, service_call: ServiceCall
    ) -> None:
        """Execute a service."""
        if handler.job.job_type == SmartHomeControllerJobType.COROUTINE_FUNCTION:
            await typing.cast(
                typing.Callable[[ServiceCall], collections.abc.Awaitable[None]],
                handler.job.target,
            )(service_call)
        elif handler.job.job_type == SmartHomeControllerJobType.CALLBACK:
            typing.cast(typing.Callable[[ServiceCall], None], handler.job.target)(
                service_call
            )
        else:
            await self._shc.async_add_executor_job(
                typing.cast(typing.Callable[[ServiceCall], None], handler.job.target),
                service_call,
            )
