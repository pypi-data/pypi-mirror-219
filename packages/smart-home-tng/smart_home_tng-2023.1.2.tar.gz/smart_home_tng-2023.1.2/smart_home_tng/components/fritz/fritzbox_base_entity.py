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


# pylint: disable=unused-variable
class FritzboxBaseEntity:
    """Fritz host entity base class."""

    def __init__(
        self,
        owner: core.SmartHomeControllerComponent,
        avm_wrapper: AvmWrapper,
        device_name: str,
    ) -> None:
        """Init device info class."""
        self._avm_wrapper = avm_wrapper
        self._device_name = device_name
        self._domain = owner.domain

    @property
    def mac_address(self) -> str:
        """Return the mac address of the main device."""
        return self._avm_wrapper.mac

    @property
    def device_info(self) -> core.DeviceInfo:
        """Return the device information."""
        return core.DeviceInfo(
            configuration_url=f"http://{self._avm_wrapper.host}",
            connections={(core.DeviceRegistry.ConnectionType.MAC, self.mac_address)},
            identifiers={(self._domain, self._avm_wrapper.unique_id)},
            manufacturer="AVM",
            model=self._avm_wrapper.model,
            name=self._device_name,
            sw_version=self._avm_wrapper.current_firmware,
        )
