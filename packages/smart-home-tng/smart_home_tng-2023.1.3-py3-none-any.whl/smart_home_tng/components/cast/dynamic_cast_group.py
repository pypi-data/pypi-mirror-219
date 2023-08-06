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


from .cast_device import CastDevice
from .chromecast_info import ChromecastInfo

_LOGGER: typing.Final = logging.getLogger(__name__)


# pylint: disable=unused-variable
class DynamicCastGroup(CastDevice):
    """Representation of a Cast device on the network - for dynamic cast groups."""

    _mz_only = True

    def async_setup(self):
        """Create chromecast object."""
        self._async_setup("Dynamic group")

    async def _async_cast_removed(self, discover: ChromecastInfo):
        """Handle removal of Chromecast."""
        if self._cast_info.uuid != discover.uuid:
            # Removed is not our device.
            return

        if not discover.cast_info.services:
            # Clean up the dynamic group
            _LOGGER.debug(f"Clean up dynamic group: {discover}")
            await self._async_tear_down()
