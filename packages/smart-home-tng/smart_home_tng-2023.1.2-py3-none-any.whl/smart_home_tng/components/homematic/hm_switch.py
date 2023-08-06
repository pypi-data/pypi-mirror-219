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
from .const import Const
from .hm_device import HMDevice

if not typing.TYPE_CHECKING:

    class HomematicIntegration:
        pass


if typing.TYPE_CHECKING:
    from .homematic_integration import HomematicIntegration


class HMSwitch(HMDevice, core.Switch.Entity):
    """Representation of a HomeMatic switch."""

    @property
    def is_on(self):
        """Return True if switch is on."""
        try:
            return self._hm_get_state() > 0
        except TypeError:
            return False

    @property
    def today_energy_kwh(self):
        """Return the current power usage in kWh."""
        if "ENERGY_COUNTER" in self._data:
            try:
                return self._data["ENERGY_COUNTER"] / 1000
            except ZeroDivisionError:
                return 0

        return None

    def turn_on(self, **_kwargs: typing.Any) -> None:
        """Turn the switch on."""
        self._hmdevice.on(self._channel)

    def turn_off(self, **_kwargs: typing.Any) -> None:
        """Turn the switch off."""
        self._hmdevice.off(self._channel)

    def _init_data_struct(self):
        """Generate the data dictionary (self._data) from metadata."""
        self._state = "STATE"
        self._data.update({self._state: None})

        # Need sensor values for SwitchPowermeter
        for node in self._hmdevice.SENSORNODE:
            self._data.update({node: None})


# pylint: disable=unused-variable
async def async_setup_switches(
    comp: HomematicIntegration,
    add_entities: core.AddEntitiesCallback,
    discovery_info: core.DiscoveryInfoType = None,
) -> None:
    """Set up the HomeMatic switch platform."""
    if discovery_info is None:
        return

    devices = []
    for conf in discovery_info[Const.ATTR_DISCOVER_DEVICES]:
        new_device = HMSwitch(comp, conf)
        devices.append(new_device)

    add_entities(devices, True)
