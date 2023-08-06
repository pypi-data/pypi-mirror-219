"""
AVM FRITZ!Box Tools Integration for Smart Home - The Next Generation.

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
from .avm_wrapper import AvmWrapper
from .const import Const
from .fritz_device import FritzDevice


# pylint: disable=unused-variable
class FritzDeviceBase(core.CoordinatorEntity[AvmWrapper]):
    """Entity base class for a device connected to a FRITZ!Box device."""

    def __init__(self, avm_wrapper: AvmWrapper, device: FritzDevice) -> None:
        """Initialize a FRITZ!Box device."""
        super().__init__(avm_wrapper)
        self._avm_wrapper = avm_wrapper
        self._mac: str = device.mac_address
        self._name: str = device.hostname or Const.DEFAULT_DEVICE_NAME

    @property
    def name(self) -> str:
        """Return device name."""
        return self._name

    @property
    def ip_address(self) -> str:
        """Return the primary ip address of the device."""
        if self._mac:
            return self._avm_wrapper.devices[self._mac].ip_address
        return None

    @property
    def mac_address(self) -> str:
        """Return the mac address of the device."""
        return self._mac

    @property
    def hostname(self) -> str:
        """Return hostname of the device."""
        if self._mac:
            return self._avm_wrapper.devices[self._mac].hostname
        return None

    async def async_process_update(self) -> None:
        """Update device."""
        raise NotImplementedError()

    async def async_on_demand_update(self) -> None:
        """Update state."""
        await self.async_process_update()
        self.async_write_state()
