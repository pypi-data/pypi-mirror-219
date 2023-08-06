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

import xmltodict

from ... import core
from .avm_wrapper import AvmWrapper
from .const import Const
from .fritzbox_base_switch import FritzboxBaseSwitch
from .switch_info import SwitchInfo

_LOGGER: typing.Final = logging.getLogger(__name__)


# pylint: disable=unused-variable
class FritzboxDeflectionSwitch(FritzboxBaseSwitch, core.Switch.Entity):
    """Defines a FRITZ!Box Tools PortForward switch."""

    def __init__(
        self,
        owner: core.SmartHomeControllerComponent,
        avm_wrapper: AvmWrapper,
        device_friendly_name: str,
        dict_of_deflection: typing.Any,
    ) -> None:
        """Init Fritxbox Deflection class."""

        self._dict_of_deflection = dict_of_deflection
        self._attributes = {}
        self._id = int(dict_of_deflection["DeflectionId"])
        self._attr_entity_category = core.EntityCategory.CONFIG

        switch_info = SwitchInfo(
            description=f"Call deflection {self.id}",
            friendly_name=device_friendly_name,
            icon="mdi:phone-forward",
            type=Const.SWITCH_TYPE_DEFLECTION,
            callback_update=self._async_fetch_update,
            callback_switch=self._async_switch_on_off_executor,
        )
        super().__init__(owner, avm_wrapper, device_friendly_name, switch_info)

    @property
    def id(self):
        return self._id

    async def _async_fetch_update(self) -> None:
        """Fetch updates."""

        resp = await self._avm_wrapper.async_get_ontel_deflections()
        if not resp:
            self._is_available = False
            return

        self._dict_of_deflection = xmltodict.parse(resp["NewDeflectionList"])["List"][
            "Item"
        ]
        if isinstance(self._dict_of_deflection, list):
            self._dict_of_deflection = self._dict_of_deflection[self.id]

        _LOGGER.debug(
            f"Specific {Const.SWITCH_TYPE_DEFLECTION} response: "
            + f"NewDeflectionList={self._dict_of_deflection}",
        )

        self._attr_is_on = self._dict_of_deflection["Enable"] == "1"
        self._is_available = True

        self._attributes["type"] = self._dict_of_deflection["Type"]
        self._attributes["number"] = self._dict_of_deflection["Number"]
        self._attributes["deflection_to_number"] = self._dict_of_deflection[
            "DeflectionToNumber"
        ]
        # Return mode sample: "eImmediately"
        self._attributes["mode"] = self._dict_of_deflection["Mode"][1:]
        self._attributes["outgoing"] = self._dict_of_deflection["Outgoing"]
        self._attributes["phonebook_id"] = self._dict_of_deflection["PhonebookID"]

    async def _async_switch_on_off_executor(self, turn_on: bool) -> None:
        """Handle deflection switch."""
        await self._avm_wrapper.async_set_deflection_enable(self.id, turn_on)
