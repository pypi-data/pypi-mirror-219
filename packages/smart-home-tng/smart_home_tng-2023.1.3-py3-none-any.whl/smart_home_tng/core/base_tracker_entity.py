"""
Core components of Smart Home - The Next Generation.

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

from .const import Const
from .entity import Entity
from .entity_category import EntityCategory
from .state_type import StateType
from .tracker_source_type import TrackerSourceType


# pylint: disable=unused-variable
class BaseTrackerEntity(Entity):
    """Represent a tracked device."""

    _attr_device_info: None = None
    _attr_entity_category = EntityCategory.DIAGNOSTIC

    @property
    def battery_level(self) -> int:
        """Return the battery level of the device.

        Percentage from 0-100.
        """
        return None

    @property
    def source_type(self) -> TrackerSourceType:
        """Return the source type, eg gps or router, of the device."""
        raise NotImplementedError()

    @property
    def state_attributes(self) -> dict[str, StateType]:
        """Return the device state attributes."""
        attr: dict[str, StateType] = {Const.ATTR_SOURCE_TYPE: str(self.source_type)}

        if self.battery_level is not None:
            attr[Const.ATTR_BATTERY_LEVEL] = self.battery_level

        return attr
