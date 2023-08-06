"""
Diagnostics Component for Smart Home - The Next Generation.

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

import voluptuous as vol

from ... import core
from .diagnostic_platforms import _DIAGNOSTIC_PLATFORMS
from .download_diagnostics_view import DownloadDiagnosticsView

_INFO: typing.Final = {vol.Required("type"): "diagnostics/list"}
_GET: typing.Final = {
    vol.Required("type"): "diagnostics/get",
    vol.Required("domain"): str,
}


# pylint: disable=unused-variable
class Diagnostics(core.SmartHomeControllerComponent):
    """The Diagnostics integration."""

    async def async_setup(self, config: core.ConfigType) -> bool:
        """Set up Diagnostics from a config entry."""
        if not await super().async_setup(config):
            return False

        websocket_api = self.controller.components.websocket_api
        if not isinstance(websocket_api, core.WebSocket.Component):
            return False

        shc = self._shc
        await shc.setup.async_process_integration_platforms(
            core.Platform.DIAGNOSTICS, _register_diagnostic_platform
        )

        websocket_api.register_command(self._handle_info, _INFO)
        websocket_api.register_command(self._handle_get, _GET)
        shc.register_view(DownloadDiagnosticsView())

        return True

    @core.callback
    def _handle_info(
        self,
        connection: core.WebSocket.Connection,
        msg: dict,
    ):
        """List all possible diagnostic handlers."""
        connection.require_admin()

        connection.send_result(
            msg["id"],
            [
                {
                    "domain": domain,
                    "handlers": {
                        # fmt: off
                        core.Diagnostics.Type.CONFIG_ENTRY.value:
                            platform.supports_config_entry_diagnostics,
                        core.Diagnostics.SubType.DEVICE.value:
                            platform.support_device_diagnostic,
                        # fmt: on
                    },
                }
                for domain, platform in _DIAGNOSTIC_PLATFORMS.items()
            ],
        )

    @core.callback
    def _handle_get(
        self,
        connection: core.WebSocket.Connection,
        msg: dict,
    ):
        """List all possible diagnostic handlers."""
        connection.require_admin()

        domain = msg["domain"]

        if (platform := _DIAGNOSTIC_PLATFORMS.get(domain)) is None:
            connection.send_error(
                msg["id"], core.WebSocket.ERR_NOT_FOUND, "Domain not supported"
            )
            return

        connection.send_result(
            msg["id"],
            {
                "domain": domain,
                "handlers": {
                    # fmt: off
                    core.Diagnostics.Type.CONFIG_ENTRY.value:
                        platform.supports_config_entry_diagnostics,
                    core.Diagnostics.SubType.DEVICE.value:
                        platform.support_device_diagnostic,
                    # fmt: on
                },
            },
        )


async def _register_diagnostic_platform(
    integration_domain: str,
    platform: core.PlatformImplementation,
):
    """Register a diagnostics platform."""
    if isinstance(platform, core.DiagnosticsPlatform):
        _DIAGNOSTIC_PLATFORMS[integration_domain] = platform
