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

from ... import core
from .device_tracker_registered_watcher import DeviceTrackerRegisteredWatcher
from .device_tracker_watcher import DeviceTrackerWatcher
from .dhcp_watcher import DHCPWatcher
from .network_watcher import NetworkWatcher
from .watcher_base import WatcherBase


# pylint: disable=unused-variable
class DHCP(core.SmartHomeControllerComponent):
    """The dhcp integration."""

    async def async_setup(self, config: core.ConfigType) -> bool:
        """Set up the dhcp component."""
        if not await super().async_setup(config):
            return False

        watchers: list[WatcherBase] = []
        address_data: dict[str, dict[str, str]] = {}
        integration_matchers = await self._shc.setup.async_get_dhcp()
        # For the passive classes we need to start listening
        # for state changes and connect the dispatchers before
        # everything else starts up or we will miss events
        for passive_cls in (DeviceTrackerRegisteredWatcher, DeviceTrackerWatcher):
            passive_watcher = passive_cls(self._shc, address_data, integration_matchers)
            await passive_watcher.async_start()
            watchers.append(passive_watcher)

        async def _initialize(_event: core.Event) -> None:
            for active_cls in (DHCPWatcher, NetworkWatcher):
                active_watcher = active_cls(
                    self._shc, address_data, integration_matchers
                )
                await active_watcher.async_start()
                watchers.append(active_watcher)

            async def _async_stop(_event: core.Event) -> None:
                for watcher in watchers:
                    await watcher.async_stop()

            self._shc.bus.async_listen_once(core.Const.EVENT_SHC_STOP, _async_stop)

        self._shc.bus.async_listen_once(core.Const.EVENT_SHC_STARTED, _initialize)
        return True
