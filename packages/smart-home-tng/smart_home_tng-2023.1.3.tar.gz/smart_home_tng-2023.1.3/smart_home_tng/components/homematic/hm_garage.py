"""
Homematic Integration for Smart Home - The Next Generation.

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
from .hm_cover import HMCover


# pylint: disable=unused-variable
class HMGarage(HMCover):
    """
    Represents a Homematic Garage cover.
    Homematic garage covers do not support position attributes.
    """

    _attr_device_class = core.Cover.DeviceClass.GARAGE

    @property
    def current_cover_position(self) -> None:
        """
        Return current position of cover.

        None is unknown, 0 is closed, 100 is fully open.
        """
        # Garage covers do not support position; always return None
        return None

    @property
    def is_closed(self) -> bool:
        """Return whether the cover is closed."""
        return self._hmdevice.is_closed(self._hm_get_state())

    def _init_data_struct(self):
        """Generate a data dictionary (self._data) from metadata."""
        self._state = "DOOR_STATE"
        self._data.update({self._state: None})
