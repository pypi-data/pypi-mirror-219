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

import threading

from ... import core
from .watcher_base import WatcherBase


# pylint: disable=unused-variable
class DHCPWatcher(WatcherBase):
    """Class to watch dhcp requests."""

    def __init__(
        self,
        shc: core.SmartHomeController,
        address_data: dict[str, dict[str, str]],
        integration_matchers: list[core.DHCPMatcher],
    ) -> None:
        """Initialize class."""
        super().__init__(shc, address_data, integration_matchers)
        self._started = threading.Event()

    async def async_stop(self) -> None:
        """Stop watching for new device trackers."""
        await self._shc.async_add_executor_job(self._stop)

    def _stop(self) -> None:
        """Stop the thread."""
        if self._started.is_set():
            pass
            # assert self._sniffer is not None
            # self._sniffer.stop()

    async def async_start(self) -> None:
        """Start watching for dhcp packets."""
        await self._shc.async_add_executor_job(self._start)

    def _start(self) -> None:
        """Start watching for dhcp packets."""
        # Local import because importing from scapy has side effects such as opening
        # sockets

        #
        # Importing scapy.sendrecv will cause a scapy resync which will
        # import scapy.arch.read_routes which will import scapy.sendrecv
        #
        # We avoid this circular import by importing arch above to ensure
        # the module is loaded and avoid the problem
        #

        # disable scapy promiscuous mode as we do not need it
