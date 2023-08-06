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

import logging
import typing

import pychromecast

from ... import core
from .chromecast_info import ChromecastInfo
from .chromecast_zeroconf import ChromecastZeroconf
from .const import Const


if not typing.TYPE_CHECKING:

    class GoogleCastIntegration:
        pass


if typing.TYPE_CHECKING:
    from .google_cast_integration import GoogleCastIntegration

_LOGGER: typing.Final = logging.getLogger(__name__)


def discover_chromecast(
    owner: GoogleCastIntegration, cast_info: pychromecast.CastInfo
) -> None:
    """Discover a Chromecast."""

    info = ChromecastInfo(
        cast_info=cast_info,
    )

    if info.uuid is None:
        _LOGGER.error(f"Discovered chromecast without uuid {info}")
        return

    info = info.fill_out_missing_chromecast_info(owner)
    _LOGGER.debug(f"Discovered new or updated chromecast {info}")

    owner.controller.dispatcher.send(Const.SIGNAL_CAST_DISCOVERED, info)


def _remove_chromecast(owner: GoogleCastIntegration, info: ChromecastInfo) -> None:
    # Removed chromecast
    _LOGGER.debug(f"Removed chromecast {info}")

    owner.controller.dispatcher.send(Const.SIGNAL_CAST_REMOVED, info)


# pylint: disable=unused-variable
def setup_internal_discovery(
    owner: GoogleCastIntegration, config_entry: core.ConfigEntry
) -> None:
    """Set up the pychromecast internal discovery."""
    if not owner.discovery_running.acquire(blocking=False):
        # Internal discovery is already running
        return

    class CastListener(pychromecast.discovery.AbstractCastListener):
        """Listener for discovering chromecasts."""

        def add_cast(self, uuid, _):
            """Handle zeroconf discovery of a new chromecast."""
            discover_chromecast(owner, browser.devices[uuid])

        def update_cast(self, uuid, _):
            """Handle zeroconf discovery of an updated chromecast."""
            discover_chromecast(owner, browser.devices[uuid])

        def remove_cast(self, uuid, service, cast_info):
            """Handle zeroconf discovery of a removed chromecast."""
            _remove_chromecast(
                owner,
                ChromecastInfo(
                    cast_info=cast_info,
                ),
            )

    _LOGGER.debug("Starting internal pychromecast discovery")
    browser = pychromecast.discovery.CastBrowser(
        CastListener(),
        ChromecastZeroconf.get_zeroconf(),
        config_entry.data.get(Const.CONF_KNOWN_HOSTS),
    )
    owner._browser = browser  # pylint: disable=protected-access
    browser.start_discovery()

    def stop_discovery(_event):
        """Stop discovery of new chromecasts."""
        _LOGGER.debug("Stopping internal pychromecast discovery")
        browser.stop_discovery()
        owner.discovery_running.release()

    owner.controller.bus.listen_once(core.Const.EVENT_SHC_STOP, stop_discovery)

    async def config_entry_updated(
        _shc: core.SmartHomeController, config_entry: core.ConfigEntry
    ) -> None:
        """Handle config entry being updated."""
        browser = owner.browser
        browser.host_browser.update_hosts(config_entry.data.get(Const.CONF_KNOWN_HOSTS))

    config_entry.add_update_listener(config_entry_updated)
