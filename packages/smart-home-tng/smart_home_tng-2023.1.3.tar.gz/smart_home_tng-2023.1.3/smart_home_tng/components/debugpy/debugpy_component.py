"""
The Remote Python Debugger integration for Smart Home - The Next Generation.

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
import logging
import threading
import typing

import debugpy
import voluptuous as vol

from ... import core

_const: typing.TypeAlias = core.Const
_cv: typing.TypeAlias = core.ConfigValidation

_CONF_START: typing.Final = "start"
_CONF_WAIT: typing.Final = "wait"
_SERVICE_START: typing.Final = "start"
_LOGGER: typing.Final = logging.getLogger(__name__)


# pylint: disable=unused-variable
class DebugPyComponent(core.SmartHomeControllerComponent):
    """The Remote Python Debugger integration"""

    async def async_validate_config(self, config: core.ConfigType) -> core.ConfigType:
        """Validate debugpy configuration"""

        schema: typing.Final = vol.Schema(
            {
                self.domain: vol.Schema(
                    {
                        vol.Optional(
                            _const.CONF_HOST, default="0.0.0.0"  # nosec
                        ): _cv.string,
                        vol.Optional(_const.CONF_PORT, default=5678): _cv.port,
                        vol.Optional(_CONF_START, default=True): _cv.boolean,
                        vol.Optional(_CONF_WAIT, default=False): _cv.boolean,
                    }
                )
            },
            extra=vol.ALLOW_EXTRA,
        )
        return schema(config)

    async def async_setup(self, config: core.ConfigType) -> bool:
        """Set up the Remote Python Debugger component."""
        if not await super().async_setup(config) or self._config is None:
            return False

        core.Service.async_register_admin_service(
            self.controller,
            self.domain,
            _SERVICE_START,
            self.debug_start,
            schema=vol.Schema({}),
        )

        # If set to start the debugger on startup, do so
        if self._config[_CONF_START]:
            await self.debug_start(wait=self._config[_CONF_WAIT])

        return True

    async def debug_start(
        self, _call: core.ServiceCall = None, *, wait: bool = None
    ) -> None:
        """Enable asyncio debugging and start the debugger."""
        asyncio.get_running_loop().set_debug(True)
        if wait is None:
            wait = self._config[_CONF_WAIT]

        host = self._config[_const.CONF_HOST]
        port = self._config[_const.CONF_PORT]
        await self.controller.async_add_executor_job(
            debugpy.listen,
            (host, port),
        )

        if wait:
            _LOGGER.warning(f"Waiting for remote debug connection on {host}:{port}")
            ready = asyncio.Event()

            def waitfor():
                debugpy.wait_for_client()
                self.controller.call_soon_threadsafe(ready.set)

            threading.Thread(target=waitfor).start()

            await ready.wait()
        else:
            _LOGGER.warning(f"Listening for remote debug connection on {host}:{port}")
