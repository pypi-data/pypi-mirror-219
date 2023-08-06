"""
Home Assistant Cloud Component for Smart Home - The Next Generation.

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
import typing

from ... import core
from .const import Const

_WAIT_UNTIL_CHANGE: typing.Final = 3


# pylint: disable=unused-variable
class CloudRemoteBinary(core.BinarySensor.Entity):
    """Representation of an Cloud Remote UI Connection binary sensor."""

    _attr_name = "Remote UI"
    _attr_device_class = core.BinarySensor.DeviceClass.CONNECTIVITY
    _attr_should_poll = False
    _attr_unique_id = "cloud-remote-ui-connectivity"
    _attr_entity_category = core.EntityCategory.DIAGNOSTIC

    def __init__(self, cloud):
        """Initialize the binary sensor."""
        self._cloud = cloud
        self._unsub_dispatcher = None

    @property
    def is_on(self) -> bool:
        """Return true if the binary sensor is on."""
        return self._cloud.remote.is_connected

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return self._cloud.remote.certificate is not None

    async def async_added_to_shc(self) -> None:
        """Register update dispatcher."""

        async def async_state_update(_data):
            """Update callback."""
            await asyncio.sleep(_WAIT_UNTIL_CHANGE)
            self.async_write_state()

        self._unsub_dispatcher = self._shc.dispatcher.async_connect(
            Const.DISPATCHER_REMOTE_UPDATE, async_state_update
        )

    async def async_will_remove_from_shc(self) -> None:
        """Register update dispatcher."""
        if self._unsub_dispatcher is not None:
            self._unsub_dispatcher()
            self._unsub_dispatcher = None
