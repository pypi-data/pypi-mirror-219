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

import typing

from .base_tracker_entity import BaseTrackerEntity
from .const import Const
from .smart_home_controller_component import SmartHomeControllerComponent
from .state_type import StateType
from .zone_component import ZoneComponent

_ENTITY_ID_ZONE_HOME: typing.Final = "zone.home"


# pylint: disable=unused-variable
class TrackerEntity(BaseTrackerEntity):
    """Base class for a tracked device."""

    @property
    def should_poll(self) -> bool:
        """No polling for entities that have location pushed."""
        return False

    @property
    def force_update(self) -> bool:
        """All updates need to be written to the state machine if we're not polling."""
        return not self.should_poll

    @property
    def location_accuracy(self) -> int:
        """Return the location accuracy of the device.

        Value in meters.
        """
        return 0

    @property
    def location_name(self) -> str:
        """Return a location name for the current location of the device."""
        return None

    @property
    def latitude(self) -> float:
        """Return latitude value of the device."""
        raise NotImplementedError()

    @property
    def longitude(self) -> float:
        """Return longitude value of the device."""
        raise NotImplementedError()

    @property
    def state(self) -> str:
        """Return the state of the device."""
        if self.location_name is not None:
            return self.location_name

        if self.latitude is not None and self.longitude is not None:
            zone = SmartHomeControllerComponent.get_component(Const.ZONE_COMPONENT_NAME)
            if isinstance(zone, ZoneComponent):
                zone_state = zone.get_zone_from_position(
                    self.latitude, self.longitude, self.location_accuracy
                )
                if zone_state is None:
                    state = Const.STATE_NOT_HOME
                elif zone_state.entity_id == _ENTITY_ID_ZONE_HOME:
                    state = Const.STATE_HOME
                else:
                    state = zone_state.name
                return state

        return None

    @typing.final
    @property
    def state_attributes(self) -> dict[str, StateType]:
        """Return the device state attributes."""
        attr: dict[str, StateType] = {}
        attr.update(super().state_attributes)

        if self.latitude is not None and self.longitude is not None:
            attr[Const.ATTR_LATITUDE] = self.latitude
            attr[Const.ATTR_LONGITUDE] = self.longitude
            attr[Const.ATTR_GPS_ACCURACY] = self.location_accuracy

        return attr
