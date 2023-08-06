"""
Mobile App Component for Smart Home - The Next Generation.

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

if not typing.TYPE_CHECKING:

    class MobileAppComponent:
        pass


if typing.TYPE_CHECKING:
    from .mobile_app_component import MobileAppComponent


_ATTR_KEYS: typing.Final = (
    Const.ATTR_ALTITUDE,
    Const.ATTR_COURSE,
    Const.ATTR_SPEED,
    Const.ATTR_VERTICAL_ACCURACY,
)


# pylint: disable=unused-variable
class MobileAppTrackerEntity(core.TrackerEntity, core.RestoreEntity):
    """Represent a tracked device."""

    def __init__(self, owner: MobileAppComponent, entry: core.ConfigEntry, data=None):
        """Set up OwnTracks entity."""
        self._entry = entry
        self._data = data
        self._dispatch_unsub = None
        self._owner = owner

    @property
    def unique_id(self):
        """Return the unique ID."""
        return self._entry.data[core.Const.ATTR_DEVICE_ID]

    @property
    def battery_level(self):
        """Return the battery level of the device."""
        return self._data.get(core.Const.ATTR_BATTERY)

    @property
    def extra_state_attributes(self):
        """Return device specific attributes."""
        attrs = {}
        for key in _ATTR_KEYS:
            if (value := self._data.get(key)) is not None:
                attrs[key] = value

        return attrs

    @property
    def location_accuracy(self):
        """Return the gps accuracy of the device."""
        return self._data.get(core.Const.ATTR_GPS_ACCURACY)

    @property
    def latitude(self):
        """Return latitude value of the device."""
        if (gps := self._data.get(core.Const.ATTR_GPS)) is None:
            return None

        return gps[0]

    @property
    def longitude(self):
        """Return longitude value of the device."""
        if (gps := self._data.get(core.Const.ATTR_GPS)) is None:
            return None

        return gps[1]

    @property
    def location_name(self):
        """Return a location name for the current location of the device."""
        if location_name := self._data.get(core.Const.ATTR_LOCATION_NAME):
            return location_name
        return None

    @property
    def name(self):
        """Return the name of the device."""
        return self._entry.data[Const.ATTR_DEVICE_NAME]

    @property
    def source_type(self) -> core.TrackerSourceType:
        """Return the source type, eg gps or router, of the device."""
        return core.TrackerSourceType.GPS

    @property
    def device_info(self):
        """Return the device info."""
        # pylint: disable=protected-access
        return self._owner._device_info(self._entry.data)

    async def async_added_to_shc(self):
        """Call when entity about to be added to the Smart Home Controller."""
        await super().async_added_to_shc()
        # SIGNAL_LOCATION_UPDATE = DOMAIN + "_location_update_{}"
        signal = f"{self._owner.domain}.location_update.{self._entry.entry_id}"
        self._dispatch_unsub = self._owner.controller.dispatcher.async_connect(
            signal,
            self.update_data,
        )

        # Don't restore if we got set up with data.
        if self._data is not None:
            return

        if (state := await self.async_get_last_state()) is None:
            self._data = {}
            return

        attr = state.attributes
        data = {
            core.Const.ATTR_GPS: (
                attr.get(core.Const.ATTR_LATITUDE),
                attr.get(core.Const.ATTR_LONGITUDE),
            ),
            core.Const.ATTR_GPS_ACCURACY: attr.get(core.Const.ATTR_GPS_ACCURACY),
            core.Const.ATTR_BATTERY: attr.get(core.Const.ATTR_BATTERY_LEVEL),
        }
        data.update({key: attr[key] for key in attr if key in _ATTR_KEYS})
        self._data = data

    async def async_will_remove_from_shc(self):
        """Call when entity is being removed from the Smart Home Controller."""
        await super().async_will_remove_from_shc()

        if self._dispatch_unsub:
            self._dispatch_unsub()
            self._dispatch_unsub = None

    @core.callback
    def update_data(self, data):
        """Mark the device as seen."""
        self._data = data
        self.async_write_state()
