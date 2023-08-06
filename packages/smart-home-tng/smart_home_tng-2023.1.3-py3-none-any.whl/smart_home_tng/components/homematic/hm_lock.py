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


class HMLock(HMDevice, core.Lock.Entity):
    """Representation of a Homematic lock aka KeyMatic."""

    _attr_supported_features = core.Lock.EntityFeature.OPEN

    @property
    def is_locked(self) -> bool:
        """Return true if the lock is locked."""
        return not bool(self._hm_get_state())

    def lock(self, **_kwargs: typing.Any) -> None:
        """Lock the lock."""
        self._hmdevice.lock()

    def unlock(self, **_kwargs: typing.Any) -> None:
        """Unlock the lock."""
        self._hmdevice.unlock()

    def open(self, **_kwargs: typing.Any) -> None:
        """Open the door latch."""
        self._hmdevice.open()

    def _init_data_struct(self):
        """Generate the data dictionary (self._data) from metadata."""
        self._state = "STATE"
        self._data.update({self._state: None})


# pylint: disable=unused-variable
async def async_setup_locks(
    comp: HomematicIntegration,
    add_entities: core.AddEntitiesCallback,
    discovery_info: core.DiscoveryInfoType = None,
) -> None:
    """Set up the Homematic lock platform."""
    if discovery_info is None:
        return

    devices = []
    for conf in discovery_info[Const.ATTR_DISCOVER_DEVICES]:
        devices.append(HMLock(comp, conf))

    add_entities(devices, True)
