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

import abc
import logging
import typing

import pyhomematic
from pyhomematic.devicetypes import generic as hm_generic

from ... import core
from .const import Const

if not typing.TYPE_CHECKING:

    class HomematicIntegration:
        pass


if typing.TYPE_CHECKING:
    from .homematic_integration import HomematicIntegration


_LOGGER: typing.Final = logging.getLogger(__name__)


# pylint: disable=unused-variable
class HMDevice(core.Entity):
    """The HomeMatic device base object."""

    _homematic: pyhomematic.HMConnection
    _hmdevice: hm_generic.HMGeneric
    _attr_should_poll = False

    def __init__(
        self,
        owner: HomematicIntegration,
        config: dict[str, str],
        entity_description: core.EntityDescription = None,
    ) -> None:
        """Initialize a generic HomeMatic device."""
        self._owner = owner
        self._name = config.get(core.Const.ATTR_NAME)
        self._address = config.get(Const.ATTR_ADDRESS)
        self._interface = config.get(Const.ATTR_INTERFACE)
        self._channel = config.get(Const.ATTR_CHANNEL)
        self._state = config.get(Const.ATTR_PARAM)
        self._unique_id = config.get(Const.ATTR_UNIQUE_ID)
        self._data: dict[str, str] = {}
        self._connected = False
        self._available = False
        self._channel_map: dict[str, str] = {}

        if entity_description is not None:
            self._entity_description = entity_description

        # Set parameter to uppercase
        if self._state:
            self._state = self._state.upper()

    @property
    def device_info(self) -> core.DeviceInfo:
        return core.DeviceInfo(
            identifiers={(self._owner.domain, self._interface + "/" + self._address)},
            manufacturer="Homematic",
            model=self._hmdevice.TYPE,
            name=self._hmdevice.NAME,
            sw_version=self._hmdevice._FIRMWARE,  # pylint: disable=protected-access
        )

    async def async_added_to_shc(self):
        """Load data init callbacks."""
        self._subscribe_homematic_events()
        await super().async_added_to_shc()

    @property
    def unique_id(self):
        """Return unique ID. HomeMatic entity IDs are unique by default."""
        return self._unique_id.replace(" ", "_")

    @property
    def name(self):
        """Return the name of the device."""
        return self._name

    @property
    def available(self):
        """Return true if device is available."""
        return self._available

    @property
    def extra_state_attributes(self):
        """Return device specific state attributes."""
        # Static attributes
        attr = {
            "id": self._hmdevice.ADDRESS,
            "interface": self._interface,
        }

        # Generate a dictionary with attributes
        for node, data in Const.HM_ATTRIBUTE_SUPPORT.items():
            # Is an attribute and exists for this object
            if node in self._data:
                value = data[1].get(self._data[node], self._data[node])
                attr[data[0]] = value

        return attr

    def update(self):
        """Connect to HomeMatic init values."""
        if self._connected:
            return True

        # Initialize
        self._homematic = self._owner.homematic
        self._hmdevice = self._homematic.devices[self._interface][self._address]
        self._connected = True

        try:
            # Initialize datapoints of this object
            self._init_data()
            self._load_data_from_hm()

            # Link events from pyhomematic
            self._available = not self._hmdevice.UNREACH
        except Exception as err:  # pylint: disable=broad-except
            self._connected = False
            _LOGGER.error(f"Exception while linking {self._address}: {str(err)}")
        return self._connected

    def _hm_event_callback(self, device, _caller, attribute, value):
        """Handle all pyhomematic device events."""
        has_changed = False

        # Is data needed for this instance?
        if device.partition(":")[2] == self._channel_map.get(attribute):
            self._data[attribute] = value
            has_changed = True

        # Availability has changed
        if self.available != (not self._hmdevice.UNREACH):
            self._available = not self._hmdevice.UNREACH
            has_changed = True

        # If it has changed data point, update Home Assistant
        if has_changed:
            self.schedule_update_state()

    def _subscribe_homematic_events(self):
        """Subscribe all required events to handle job."""
        for metadata in (
            self._hmdevice.ACTIONNODE,
            self._hmdevice.EVENTNODE,
            self._hmdevice.WRITENODE,
            self._hmdevice.ATTRIBUTENODE,
            self._hmdevice.BINARYNODE,
            self._hmdevice.SENSORNODE,
        ):
            for node, channels in metadata.items():
                # Data is needed for this instance
                if node in self._data:
                    # chan is current channel
                    if len(channels) == 1:
                        channel = channels[0]
                    else:
                        channel = self._channel
                    # Remember the channel for this attribute to ignore invalid events later
                    self._channel_map[node] = str(channel)

        _LOGGER.debug(
            f"Channel map for {self._address}: {str(self._channel_map)}",
            self._address,
        )

        # Set callbacks
        self._hmdevice.setEventCallback(callback=self._hm_event_callback, bequeath=True)

    def _load_data_from_hm(self):
        """Load first value from pyhomematic."""
        if not self._connected:
            return False

        # Read data from pyhomematic
        for metadata, funct in (
            (self._hmdevice.ATTRIBUTENODE, self._hmdevice.getAttributeData),
            (self._hmdevice.WRITENODE, self._hmdevice.getWriteData),
            (self._hmdevice.SENSORNODE, self._hmdevice.getSensorData),
            (self._hmdevice.BINARYNODE, self._hmdevice.getBinaryData),
        ):
            for node in metadata:
                if metadata[node] and node in self._data:
                    self._data[node] = funct(name=node, channel=self._channel)

        return True

    def _hm_set_state(self, value):
        """Set data to main datapoint."""
        if self._state in self._data:
            self._data[self._state] = value

    def _hm_get_state(self):
        """Get data from main datapoint."""
        if self._state in self._data:
            return self._data[self._state]
        return None

    def _init_data(self):
        """Generate a data dict (self._data) from the HomeMatic metadata."""
        # Add all attributes to data dictionary
        for data_note in self._hmdevice.ATTRIBUTENODE:
            self._data.update({data_note: None})

        # Initialize device specific data
        self._init_data_struct()

    @abc.abstractmethod
    def _init_data_struct(self):
        """Generate a data dictionary from the HomeMatic device metadata."""
