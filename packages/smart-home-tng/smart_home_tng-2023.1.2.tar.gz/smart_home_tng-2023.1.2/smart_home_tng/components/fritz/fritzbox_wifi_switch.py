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

import logging
import typing

from ... import core
from .avm_wrapper import AvmWrapper
from .const import Const
from .fritzbox_base_switch import FritzboxBaseSwitch
from .switch_info import SwitchInfo

_LOGGER: typing.Final = logging.getLogger(__name__)


# pylint: disable=unused-variable
class FritzboxWifiSwitch(FritzboxBaseSwitch, core.Switch.Entity):
    """Defines a FRITZ!Box Tools Wifi switch."""

    def __init__(
        self,
        owner: core.SmartHomeControllerComponent,
        avm_wrapper: AvmWrapper,
        device_friendly_name: str,
        network_num: int,
        network_name: str,
    ) -> None:
        """Init Fritz Wifi switch."""
        self._attributes = {}
        self._attr_entity_category = core.EntityCategory.CONFIG
        self._network_num = network_num

        switch_info = SwitchInfo(
            description=f"Wi-Fi {network_name}",
            friendly_name=device_friendly_name,
            icon="mdi:wifi",
            type=Const.SWITCH_TYPE_WIFINETWORK,
            callback_update=self._async_fetch_update,
            callback_switch=self._async_switch_on_off_executor,
        )
        super().__init__(owner, avm_wrapper, device_friendly_name, switch_info)

    async def _async_fetch_update(self) -> None:
        """Fetch updates."""

        wifi_info = await self._avm_wrapper.async_get_wlan_configuration(
            self._network_num
        )
        _LOGGER.debug(
            f"Specific {Const.SWITCH_TYPE_WIFINETWORK} response: GetInfo={wifi_info}"
        )

        if not wifi_info:
            self._is_available = False
            return

        self._attr_is_on = wifi_info["NewEnable"] is True
        self._is_available = True

        std = wifi_info["NewStandard"]
        self._attributes["standard"] = std if std else None
        self._attributes["bssid"] = wifi_info["NewBSSID"]
        self._attributes["mac_address_control"] = wifi_info[
            "NewMACAddressControlEnabled"
        ]

    async def _async_switch_on_off_executor(self, turn_on: bool) -> None:
        """Handle wifi switch."""
        await self._avm_wrapper.async_set_wlan_configuration(self._network_num, turn_on)
