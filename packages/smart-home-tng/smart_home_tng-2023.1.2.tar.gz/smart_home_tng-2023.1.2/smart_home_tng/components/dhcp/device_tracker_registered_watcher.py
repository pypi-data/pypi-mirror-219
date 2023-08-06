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

import collections.abc

from ... import core
from .const import Const
from .watcher_base import WatcherBase


# pylint: disable=unused-variable
class DeviceTrackerRegisteredWatcher(WatcherBase):
    """Class to watch data from device tracker registrations."""

    def __init__(
        self,
        shc: core.SmartHomeController,
        address_data: dict[str, dict[str, str]],
        integration_matchers: list[core.DHCPMatcher],
    ) -> None:
        """Initialize class."""
        super().__init__(shc, address_data, integration_matchers)
        self._unsub: collections.abc.Callable[[], None] = None

    async def async_stop(self) -> None:
        """Stop watching for device tracker registrations."""
        if self._unsub:
            self._unsub()
            self._unsub = None

    async def async_start(self) -> None:
        """Stop watching for device tracker registrations."""
        self._unsub = self._shc.dispatcher.async_connect(
            Const.CONNECTED_DEVICE_REGISTERED, self._async_process_device_data
        )

    @core.callback
    def _async_process_device_data(self, data: dict[str, str]) -> None:
        """Process a device tracker state."""
        ip_address = data[Const.ATTR_IP]
        hostname = data[Const.ATTR_HOST_NAME] or ""
        mac_address = data[Const.ATTR_MAC]

        if ip_address is None or mac_address is None:
            return

        self.async_process_client(ip_address, hostname, self._format_mac(mac_address))
