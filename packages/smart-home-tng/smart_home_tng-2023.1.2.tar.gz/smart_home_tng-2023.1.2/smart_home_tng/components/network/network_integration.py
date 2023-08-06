"""
Network Component for Smart Home - The Next Generation.

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

import ipaddress
import typing

import voluptuous as vol

from ... import core
from .const import Const
from .network import Network

_NETWORK_ADAPTERS: typing.Final = {vol.Required("type"): "network"}
_NETWORK_ADAPTERS_CONFIGURE: typing.Final = {
    vol.Required("type"): "network/configure",
    vol.Required("config", default={}): Const.NETWORK_CONFIG_SCHEMA,
}


# pylint: disable=unused-variable
class NetworkIntegration(core.NetworkComponent):
    """Network Component for Smart Home - The Next Generation."""

    def __init__(self, path: typing.Iterable[str]):
        super().__init__(path)
        self._network: Network = None

    async def async_setup(self, config: core.ConfigType) -> bool:
        """Set up network for Home Assistant."""
        if not await super().async_setup(config):
            return False

        self._network = Network(self._shc)
        await self._network.async_setup()
        self._network.async_configure()

        websocket_api = self.controller.components.websocket_api
        if not isinstance(websocket_api, core.WebSocket.Component):
            return False

        websocket_api.register_command(self._network_adapters, _NETWORK_ADAPTERS)
        websocket_api.register_command(
            self._network_adapters_configure, _NETWORK_ADAPTERS_CONFIGURE
        )
        return True

    async def async_get_enabled_source_ips(
        self,
    ) -> list[ipaddress.IPv4Address | ipaddress.IPv6Address]:
        """Build the list of enabled source ips."""
        return await self._network.async_get_enabled_source_ips()

    def async_only_default_interface_enabled(
        self, adapters: list[core.Adapter]
    ) -> bool:
        """Check to see if any non-default adapter is enabled."""
        return self._network.async_only_default_interface_enabled(adapters)

    # pylint: disable=protected-access
    async def async_get_source_ip(
        self, target_ip: str | object = core.NetworkComponent._UNDEFINED
    ) -> str:
        """Get the source ip for a target ip."""
        return await self._network.async_get_source_ipv4(target_ip)

    async def _network_adapters(
        self,
        connection: core.WebSocket.Connection,
        msg: dict,
    ) -> None:
        """Return network preferences."""
        connection.require_admin()
        network = self._network
        connection.send_result(
            msg["id"],
            {
                Const.ATTR_ADAPTERS: network.adapters,
                Const.ATTR_CONFIGURED_ADAPTERS: network.configured_adapters,
            },
        )

    async def async_get_adapters(self) -> list[core.Adapter]:
        return await self._network.async_get_adapters()

    async def _network_adapters_configure(
        self,
        connection: core.WebSocket.Connection,
        msg: dict,
    ) -> None:
        """Update network config."""
        connection.require_admin()
        network = self._network

        await network.async_reconfig(msg["config"])

        connection.send_result(
            msg["id"],
            {Const.ATTR_CONFIGURED_ADAPTERS: network.configured_adapters},
        )
