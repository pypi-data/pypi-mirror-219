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

import typing

from ... import core
from .avm_wrapper import AvmWrapper
from .fritz_device import FritzDevice
from .fritz_device_base import FritzDeviceBase


# pylint: disable=unused-variable
class FritzboxProfileSwitch(FritzDeviceBase, core.Switch.Entity):
    """Defines a FRITZ!Box Tools DeviceProfile switch."""

    _attr_icon = "mdi:router-wireless-settings"

    def __init__(
        self,
        owner: core.SmartHomeControllerComponent,
        avm_wrapper: AvmWrapper,
        device: FritzDevice,
    ) -> None:
        """Init Fritz profile."""
        super().__init__(avm_wrapper, device)
        self._attr_is_on: bool = False
        self._name = f"{device.hostname} Internet Access"
        self._attr_unique_id = f"{self._mac}_internet_access"
        self._attr_entity_category = core.EntityCategory.CONFIG
        self._attr_device_info = core.DeviceInfo(
            connections={(core.DeviceRegistry.ConnectionType.MAC, self._mac)},
            default_manufacturer="AVM",
            default_model="FRITZ!Box Tracked device",
            default_name=device.hostname,
            identifiers={(owner.domain, self._mac)},
            via_device=(
                owner.domain,
                avm_wrapper.unique_id,
            ),
        )

    @property
    def is_on(self) -> bool:
        """Switch status."""
        return self._avm_wrapper.devices[self._mac].wan_access

    @property
    def available(self) -> bool:
        """Return availability of the switch."""
        if self._avm_wrapper.devices[self._mac].wan_access is None:
            return False
        return super().available

    async def async_turn_on(self, **_kwargs: typing.Any) -> None:
        """Turn on switch."""
        await self._async_handle_turn_on_off(turn_on=True)

    async def async_turn_off(self, **_kwargs: typing.Any) -> None:
        """Turn off switch."""
        await self._async_handle_turn_on_off(turn_on=False)

    async def _async_handle_turn_on_off(self, turn_on: bool) -> bool:
        """Handle switch state change request."""
        if not self.ip_address:
            return False
        await self._avm_wrapper.async_set_allow_wan_access(self.ip_address, turn_on)
        self.async_write_state()
        return True
