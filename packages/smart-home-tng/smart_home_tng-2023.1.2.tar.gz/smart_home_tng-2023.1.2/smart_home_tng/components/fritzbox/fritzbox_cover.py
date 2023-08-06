"""
AVM FRITZ!SmartHome Integration for Smart Home - The Next Generation.

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

import typing

from ... import core
from .const import Const
from .fritzbox_entity import FritzboxEntity

if not typing.TYPE_CHECKING:

    class FritzboxIntegration:
        pass


if typing.TYPE_CHECKING:
    from .fritzbox_integration import FritzboxIntegration


class FritzboxCover(FritzboxEntity, core.Cover.Entity):
    """The cover class for FRITZ!SmartHome covers."""

    _attr_device_class = core.Cover.DeviceClass.BLIND
    _attr_supported_features = (
        core.Cover.EntityFeature.OPEN
        | core.Cover.EntityFeature.SET_POSITION
        | core.Cover.EntityFeature.CLOSE
        | core.Cover.EntityFeature.STOP
    )

    @property
    def current_cover_position(self) -> int:
        """Return the current position."""
        position = None
        if self.device.levelpercentage is not None:
            position = 100 - self.device.levelpercentage
        return position

    @property
    def is_closed(self) -> bool:
        """Return if the cover is closed."""
        if self.device.levelpercentage is None:
            return None
        return self.device.levelpercentage == 100

    async def async_open_cover(self, **_kwargs: typing.Any) -> None:
        """Open the cover."""
        await self._shc.async_add_executor_job(self.device.set_blind_open)
        await self.coordinator.async_refresh()

    async def async_close_cover(self, **_kwargs: typing.Any) -> None:
        """Close the cover."""
        await self._shc.async_add_executor_job(self.device.set_blind_close)
        await self.coordinator.async_refresh()

    async def async_set_cover_position(self, **kwargs: typing.Any) -> None:
        """Move the cover to a specific position."""
        await self._shc.async_add_executor_job(
            self.device.set_level_percentage, 100 - kwargs[core.Cover.ATTR_POSITION]
        )

    async def async_stop_cover(self, **_kwargs: typing.Any) -> None:
        """Stop the cover."""
        await self._shc.async_add_executor_job(self.device.set_blind_stop)
        await self.coordinator.async_refresh()


# pylint: disable=unused-variable
async def async_setup_covers(
    owner: FritzboxIntegration,
    entry: core.ConfigEntry,
    async_add_entities: core.AddEntitiesCallback,
) -> None:
    """Set up the FRITZ!SmartHome cover from ConfigEntry."""
    coordinator = owner.connection_config[entry.entry_id][Const.CONF_COORDINATOR]

    async_add_entities(
        FritzboxCover(coordinator, ain)
        for ain, device in coordinator.data.items()
        if device.has_blind
    )
