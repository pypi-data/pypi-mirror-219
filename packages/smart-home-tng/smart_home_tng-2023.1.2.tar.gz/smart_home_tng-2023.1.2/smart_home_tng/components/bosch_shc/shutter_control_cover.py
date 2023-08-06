"""
Bosch SHC Integration for Smart Home - The Next Generation.

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
import boschshcpy as bosch

from ... import core
from .bosch_entity import BoschEntity

if not typing.TYPE_CHECKING:

    class BoschShcIntegration:
        pass


if typing.TYPE_CHECKING:
    from .bosch_shc_integration import BoschShcIntegration


# pylint: disable=unused-variable
class ShutterControlCover(BoschEntity, core.Cover.Entity):
    """Representation of a SHC shutter control device."""

    _attr_device_class = core.Cover.DeviceClass.SHUTTER
    _attr_supported_features = (
        core.Cover.EntityFeature.OPEN
        | core.Cover.EntityFeature.CLOSE
        | core.Cover.EntityFeature.STOP
        | core.Cover.EntityFeature.SET_POSITION
    )

    @property
    def current_cover_position(self):
        """Return the current cover position."""
        return round(self._device.level * 100.0)

    def stop_cover(self, **kwargs):
        """Stop the cover."""
        self._device.stop()

    @property
    def is_closed(self):
        """Return if the cover is closed or not."""
        return self.current_cover_position == 0

    @property
    def is_opening(self):
        """Return if the cover is opening or not."""
        return (
            self._device.operation_state
            == bosch.SHCShutterControl.ShutterControlService.State.OPENING
        )

    @property
    def is_closing(self):
        """Return if the cover is closing or not."""
        return (
            self._device.operation_state
            == bosch.SHCShutterControl.ShutterControlService.State.CLOSING
        )

    def open_cover(self, **kwargs):
        """Open the cover."""
        self._device.level = 1.0

    def close_cover(self, **kwargs):
        """Close cover."""
        self._device.level = 0.0

    def set_cover_position(self, **kwargs):
        """Move the cover to a specific position."""
        position = kwargs[core.Cover.ATTR_POSITION]
        self._device.level = position / 100.0


# pylint: disable=unused-variable
async def _async_setup_shutter_control_covers(
    owner: BoschShcIntegration,
    session: bosch.SHCSession,
    config_entry: core.ConfigEntry,
) -> typing.Iterable[core.Entity]:
    """Set up the SHC cover platform."""
    entities = []

    for cover in session.device_helper.shutter_controls:
        entities.append(
            ShutterControlCover(
                owner,
                device=cover,
                parent_id=session.information.unique_id,
                entry_id=config_entry.entry_id,
            )
        )

    return entities
