"""
DHCP Component for Smart Home - The Next Generation.

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
import typing

import aiodiscover

from ... import core
from .const import Const
from .watcher_base import WatcherBase


# pylint: disable=unused-variable
class NetworkWatcher(WatcherBase):
    """Class to query ptr records routers."""

    def __init__(
        self,
        shc: core.SmartHomeController,
        address_data: dict[str, dict[str, str]],
        integration_matchers: list[core.DHCPMatcher],
    ) -> None:
        """Initialize class."""
        super().__init__(shc, address_data, integration_matchers)
        self._unsub: collections.abc.Callable[[], None] = None
        self._discover_hosts: aiodiscover.DiscoverHosts = None
        self._discover_task: asyncio.Task = None

    async def async_stop(self) -> None:
        """Stop scanning for new devices on the network."""
        if self._unsub:
            self._unsub()
            self._unsub = None
        if self._discover_task:
            self._discover_task.cancel()
            self._discover_task = None

    async def async_start(self) -> None:
        """Start scanning for new devices on the network."""
        self._discover_hosts = aiodiscover.DiscoverHosts()
        self._unsub = self._shc.tracker.async_track_time_interval(
            self.async_start_discover, Const.SCAN_INTERVAL
        )
        self.async_start_discover()

    @core.callback
    def async_start_discover(self, *_: typing.Any) -> None:
        """Start a new discovery task if one is not running."""
        if self._discover_task and not self._discover_task.done():
            return
        self._discover_task = self._shc.async_create_task(self.async_discover())

    async def async_discover(self) -> None:
        """Process discovery."""
        assert self._discover_hosts is not None
        for host in await self._discover_hosts.async_discover():
            self.async_process_client(
                host[aiodiscover.discovery.IP_ADDRESS],
                host[aiodiscover.discovery.HOSTNAME],
                self._format_mac(host[aiodiscover.discovery.MAC_ADDRESS]),
            )
