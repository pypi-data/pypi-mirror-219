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
from .watcher_base import WatcherBase


# pylint: disable=unused-variable
class DeviceTrackerWatcher(WatcherBase):
    """Class to watch dhcp data from routers."""

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
        """Stop watching for new device trackers."""
        if self._unsub:
            self._unsub()
            self._unsub = None

    async def async_start(self) -> None:
        """Stop watching for new device trackers."""
        self._unsub = self._shc.tracker.async_track_state_added_domain(
            ["device_tracker"], self._async_process_device_event
        )
        for state in self._shc.states.async_all("device_tracker"):
            self._async_process_device_state(state)

    @core.callback
    def _async_process_device_event(self, event: core.Event) -> None:
        """Process a device tracker state change event."""
        self._async_process_device_state(event.data["new_state"])

    @core.callback
    def _async_process_device_state(self, state: core.State) -> None:
        """Process a device tracker state."""
        if state.state != core.Const.STATE_HOME:
            return

        attributes = state.attributes

        if attributes.get(core.Const.ATTR_SOURCE_TYPE) != core.TrackerSourceType.ROUTER:
            return

        ip_address = attributes.get(core.Const.ATTR_IP)
        hostname = attributes.get(core.Const.ATTR_HOST_NAME, "")
        mac_address = attributes.get(core.Const.ATTR_MAC)

        if ip_address is None or mac_address is None:
            return

        self.async_process_client(ip_address, hostname, self._format_mac(mac_address))
