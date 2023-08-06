"""
System Health Component for Smart Home - The Next Generation.

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
import datetime as dt
import logging
import typing

import aiohttp
import async_timeout
import voluptuous as vol

from ... import core

_LOGGER: typing.Final = logging.getLogger(__name__)
_HANDLE_INFO: typing.Final = {vol.Required("type"): "system_health/info"}
_INFO_CALLBACK_TIMEOUT: typing.Final = 5


@core.callback
def _format_value(val):
    """Format a system health value."""
    if isinstance(val, dt.datetime):
        return {"value": val.isoformat(), "type": "date"}
    return val


# pylint: disable=unused-variable
class SystemHealthComponent(core.SystemHealthComponent):
    """Support for System health ."""

    def __init__(self, path: typing.Iterable[str]):
        super().__init__(path)
        self._registrations: dict[str, core.SystemHealthRegistration] = {}

    async def async_setup(self, config: core.ConfigType) -> bool:
        """Set up the System Health component."""
        if not await super().async_setup(config):
            return False

        websocket_api = self.controller.components.websocket_api
        if not isinstance(websocket_api, core.WebSocket.Component):
            return False

        websocket_api.register_command(self._handle_info, _HANDLE_INFO)

        await self._shc.setup.async_process_integration_platforms(
            core.Platform.SYSTEM_HEALTH, self._register_system_health_platform
        )

        return True

    async def _register_system_health_platform(
        self, integration_domain: str, platform: core.PlatformImplementation
    ) -> None:
        """Register a system health platform."""

        if not isinstance(platform, core.SystemHealthPlatform):
            return

        platform.register_system_health_info(
            core.SystemHealthRegistration(self, integration_domain)
        )

    def register_info(self, info: core.SystemHealthRegistration) -> None:
        self._registrations[info.domain] = info

    async def _get_integration_info(self, registration: core.SystemHealthRegistration):
        """Get integration system health."""
        try:
            async with async_timeout.timeout(_INFO_CALLBACK_TIMEOUT):
                data = await registration.info_callback()
        except asyncio.TimeoutError:
            data = {"error": {"type": "failed", "error": "timeout"}}
        except Exception:  # pylint: disable=broad-except
            _LOGGER.exception("Error fetching info")
            data = {"error": {"type": "failed", "error": "unknown"}}

        result = {"info": data}

        if registration.manage_url:
            result["manage_url"] = registration.manage_url

        return result

    async def _handle_info(
        self,
        connection: core.WebSocket.Connection,
        msg: dict,
    ):
        """Handle an info request via a subscription."""
        registrations = self._registrations
        data = {}
        pending_info = {}

        for domain, domain_data in zip(
            registrations,
            await asyncio.gather(
                *(
                    self._get_integration_info(registration)
                    for registration in registrations.values()
                )
            ),
        ):
            for key, value in domain_data["info"].items():
                if asyncio.iscoroutine(value):
                    value = asyncio.create_task(value)
                if isinstance(value, asyncio.Task):
                    pending_info[(domain, key)] = value
                    domain_data["info"][key] = {"type": "pending"}
                else:
                    domain_data["info"][key] = _format_value(value)

            data[domain] = domain_data

        # Confirm subscription
        connection.send_result(msg["id"])

        stop_event = asyncio.Event()
        connection.subscriptions[msg["id"]] = stop_event.set

        # Send initial data
        connection.send_event_message(msg["id"], {"type": "initial", "data": data})

        # If nothing pending, wrap it up.
        if not pending_info:
            connection.send_event_message(msg["id"], {"type": "finish"})
            return

        tasks = [asyncio.create_task(stop_event.wait()), *pending_info.values()]
        pending_lookup = {val: key for key, val in pending_info.items()}

        # One task is the stop_event.wait() and is always there
        while len(tasks) > 1 and not stop_event.is_set():
            # Wait for first completed task
            done, tasks = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)

            if stop_event.is_set():
                for task in tasks:
                    task.cancel()
                return

            # Update subscription of all finished tasks
            for result in done:
                domain, key = pending_lookup[result]
                event_msg = {
                    "type": "update",
                    "domain": domain,
                    "key": key,
                }

                if result.exception():
                    exception = result.exception()
                    _LOGGER.error(
                        f"Error fetching system info for {domain} - {key}",
                        exc_info=(type(exception), exception, exception.__traceback__),
                    )
                    event_msg["success"] = False
                    event_msg["error"] = {"type": "failed", "error": "unknown"}
                else:
                    event_msg["success"] = True
                    event_msg["data"] = _format_value(result.result())

                connection.send_event_message(msg["id"], event_msg)

        connection.send_event_message(msg["id"], {"type": "finish"})

    async def async_check_can_reach_url(
        self, url: str, more_info: str | None = None
    ) -> str:
        """Test if the url can be reached."""
        session = core.HttpClient.async_get_clientsession(self._shc)

        try:
            await session.get(url, timeout=5)
            return "ok"
        except aiohttp.ClientError:
            data = {"type": "failed", "error": "unreachable"}
        except asyncio.TimeoutError:
            data = {"type": "failed", "error": "timeout"}
        if more_info is not None:
            data["more_info"] = more_info
        return data
