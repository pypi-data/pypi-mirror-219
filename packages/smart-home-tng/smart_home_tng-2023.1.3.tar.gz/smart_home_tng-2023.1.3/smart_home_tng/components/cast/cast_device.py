"""
Google Cast Integration for Smart Home - The Next Generation.

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
import typing

import pychromecast as google

from ... import core
from .cast_status_listener import CastStatusListener
from .chromecast_info import ChromecastInfo
from .chromecast_zeroconf import ChromecastZeroconf
from .const import Const

if not typing.TYPE_CHECKING:

    class GoogleCastIntegration:
        pass


if typing.TYPE_CHECKING:
    from .google_cast_integration import GoogleCastIntegration

_LOGGER: typing.Final = logging.getLogger(__name__)


# pylint: disable=unused-variable
class CastDevice:
    """Representation of a Cast device or dynamic group on the network.

    This class is the holder of the pychromecast.Chromecast object and its
    socket client. It therefore handles all reconnects and audio groups changing
    "elected leader" itself.
    """

    _mz_only: bool

    def __init__(self, owner: GoogleCastIntegration, cast_info: ChromecastInfo) -> None:
        """Initialize the cast device."""

        self._owner = owner
        self._cast_info = cast_info
        self._chromecast: google.Chromecast = None
        self._mz_mgr = None
        self._status_listener: CastStatusListener = None
        self._add_remove_handler: typing.Callable[[], None] = None
        self._del_remove_handler: typing.Callable[[], None] = None
        self._name: str = None

    def _async_setup(self, name: str) -> None:
        """Create chromecast object."""
        self._name = name
        self._add_remove_handler = self._owner.controller.dispatcher.async_connect(
            Const.SIGNAL_CAST_DISCOVERED, self._async_cast_discovered
        )
        self._del_remove_handler = self._owner.controller.dispatcher.async_connect(
            Const.SIGNAL_CAST_REMOVED, self._async_cast_removed
        )
        self._owner.controller.bus.async_listen_once(
            core.Const.EVENT_SHC_STOP, self._async_stop
        )
        # asyncio.create_task is used to avoid delaying startup wrapup if the device
        # is discovered already during startup but then fails to respond
        asyncio.create_task(
            core.helpers.async_create_catching_coro(self._async_connect_to_chromecast())
        )

    async def _async_tear_down(self) -> None:
        """Disconnect chromecast object and remove listeners."""
        await self._async_disconnect()
        if self._cast_info.uuid is not None:
            # Remove the entity from the added casts so that it can dynamically
            # be re-added again.
            self._owner.added_cast_devices.remove(self._cast_info.uuid)
        if self._add_remove_handler:
            self._add_remove_handler()
            self._add_remove_handler = None
        if self._del_remove_handler:
            self._del_remove_handler()
            self._del_remove_handler = None

    async def _async_connect_to_chromecast(self):
        """Set up the chromecast object."""
        _LOGGER.debug(
            f"[{self._name} {self._cast_info.friendly_name}] Connecting to cast device "
            + f"by service {self._cast_info.cast_info.services}",
        )
        chromecast = await self._owner.controller.async_add_executor_job(
            google.get_chromecast_from_cast_info,
            self._cast_info.cast_info,
            ChromecastZeroconf.get_zeroconf(),
        )
        self._chromecast = chromecast

        self._mz_mgr = self._owner.mz_mgr

        self._status_listener = CastStatusListener(
            self, chromecast, self._mz_mgr, self._mz_only
        )
        chromecast.start()

    async def _async_disconnect(self) -> None:
        """Disconnect Chromecast object if it is set."""
        if self._chromecast is not None:
            _LOGGER.debug(
                f"[{self._name} {self._cast_info.friendly_name}] "
                + "Disconnecting from chromecast socket",
            )
            await self._owner.controller.async_add_executor_job(
                self._chromecast.disconnect
            )

        self._invalidate()

    def _invalidate(self) -> None:
        """Invalidate some attributes."""
        self._chromecast = None
        self._mz_mgr = None
        if self._status_listener is not None:
            self._status_listener.invalidate()
            self._status_listener = None

    async def _async_cast_discovered(self, discover: ChromecastInfo) -> None:
        """Handle discovery of new Chromecast."""
        if self._cast_info.uuid != discover.uuid:
            # Discovered is not our device.
            return

        _LOGGER.debug(f"Discovered chromecast with same UUID: {discover}")
        self._cast_info = discover

    async def _async_cast_removed(self, discover: ChromecastInfo) -> None:
        """Handle removal of Chromecast."""

    async def _async_stop(self, _event: core.Event) -> None:
        """Disconnect socket on Home Assistant stop."""
        await self._async_disconnect()

    def _get_chromecast(self) -> google.Chromecast:
        """Ensure chromecast is available, to facilitate type checking."""
        if self._chromecast is None:
            raise core.SmartHomeControllerError("Chromecast is not available.")
        return self._chromecast
