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
from .fritzbox_base_entity import FritzboxBaseEntity


# pylint: disable=unused-variable
class FritzboxUpdateEntity(FritzboxBaseEntity, core.Update.Entity):
    """Mixin for update entity specific attributes."""

    _attr_supported_features = core.Update.EntityFeature.INSTALL
    _attr_title = "FRITZ!OS"

    def __init__(
        self,
        owner: core.SmartHomeControllerComponent,
        avm_wrapper: AvmWrapper,
        device_friendly_name: str,
    ) -> None:
        """Init FRITZ!Box connectivity class."""
        self._attr_name = f"{device_friendly_name} FRITZ!OS"
        self._attr_unique_id = f"{avm_wrapper.unique_id}-update"
        super().__init__(owner, avm_wrapper, device_friendly_name)

    @property
    def installed_version(self) -> str:
        """Version currently in use."""
        return self._avm_wrapper.current_firmware

    @property
    def latest_version(self) -> str:
        """Latest version available for install."""
        if self._avm_wrapper.update_available:
            return self._avm_wrapper.latest_firmware
        return self._avm_wrapper.current_firmware

    @property
    def release_url(self) -> str:
        """URL to the full release notes of the latest version available."""
        return self._avm_wrapper.release_url

    async def async_install(
        self, _version: str, _backup: bool, **_kwargs: typing.Any
    ) -> None:
        """Install an update."""
        await self._avm_wrapper.async_trigger_firmware_update()
