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

import typing

from ... import core
from .hm_device import HMDevice


# pylint: disable=unused-variable
class HMCover(HMDevice, core.Cover.Entity):
    """Representation a HomeMatic Cover."""

    @property
    def current_cover_position(self) -> int | None:
        """
        Return current position of cover.

        None is unknown, 0 is closed, 100 is fully open.
        """
        return int(self._hm_get_state() * 100)

    def set_cover_position(self, **kwargs: typing.Any) -> None:
        """Move the cover to a specific position."""
        if core.Cover.ATTR_POSITION in kwargs:
            position = float(kwargs[core.Const.ATTR_POSITION])
            position = min(100, max(0, position))
            level = position / 100.0
            self._hmdevice.set_level(level, self._channel)

    @property
    def is_closed(self) -> bool | None:
        """Return whether the cover is closed."""
        if self.current_cover_position is not None:
            return self.current_cover_position == 0
        return None

    def open_cover(self, **_kwargs: typing.Any) -> None:
        """Open the cover."""
        self._hmdevice.move_up(self._channel)

    def close_cover(self, **_kwargs: typing.Any) -> None:
        """Close the cover."""
        self._hmdevice.move_down(self._channel)

    def stop_cover(self, **_kwargs: typing.Any) -> None:
        """Stop the device if in motion."""
        self._hmdevice.stop(self._channel)

    def _init_data_struct(self):
        """Generate a data dictionary (self._data) from metadata."""
        self._state = "LEVEL"
        self._data.update({self._state: None})
        if "LEVEL_2" in self._hmdevice.WRITENODE:
            self._data.update({"LEVEL_2": None})

    @property
    def current_cover_tilt_position(self) -> int | None:
        """Return current position of cover tilt.

        None is unknown, 0 is closed, 100 is fully open.
        """
        if not (position := self._data.get("LEVEL_2", 0)):
            return None
        return int(position * 100)

    def set_cover_tilt_position(self, **kwargs: typing.Any) -> None:
        """Move the cover tilt to a specific position."""
        if "LEVEL_2" in self._data and core.Cover.ATTR_TILT_POSITION in kwargs:
            position = float(kwargs[core.Cover.ATTR_TILT_POSITION])
            position = min(100, max(0, position))
            level = position / 100.0
            self._hmdevice.set_cover_tilt_position(level, self._channel)

    def open_cover_tilt(self, **_kwargs: typing.Any) -> None:
        """Open the cover tilt."""
        if "LEVEL_2" in self._data:
            self._hmdevice.open_slats()

    def close_cover_tilt(self, **_kwargs: typing.Any) -> None:
        """Close the cover tilt."""
        if "LEVEL_2" in self._data:
            self._hmdevice.close_slats()

    def stop_cover_tilt(self, **kwargs: typing.Any) -> None:
        """Stop cover tilt."""
        if "LEVEL_2" in self._data:
            self.stop_cover(**kwargs)
