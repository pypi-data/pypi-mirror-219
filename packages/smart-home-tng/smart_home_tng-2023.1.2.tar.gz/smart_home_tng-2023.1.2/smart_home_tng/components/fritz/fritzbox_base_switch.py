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
from .fritzbox_base_entity import FritzboxBaseEntity
from .switch_info import SwitchInfo

_LOGGER: typing.Final = logging.getLogger(__name__)


# pylint: disable=unused-variable
class FritzboxBaseSwitch(FritzboxBaseEntity):
    """Fritz switch base class."""

    _attr_is_on: bool = False

    def __init__(
        self,
        owner: core.SmartHomeControllerComponent,
        avm_wrapper: AvmWrapper,
        device_friendly_name: str,
        switch_info: SwitchInfo,
    ) -> None:
        """Init Fritzbox port switch."""
        super().__init__(owner, avm_wrapper, device_friendly_name)

        self._description = switch_info["description"]
        self._friendly_name = switch_info["friendly_name"]
        self._icon = switch_info["icon"]
        self._type = switch_info["type"]
        self._update = switch_info["callback_update"]
        self._switch = switch_info["callback_switch"]

        self._name = f"{self._friendly_name} {self._description}"
        self._unique_id = (
            f"{self._avm_wrapper.unique_id}-{core.helpers.slugify(self._description)}"
        )

        self._attributes: dict[str, str] = {}
        self._is_available = True

    @property
    def name(self) -> str:
        """Return name."""
        return self._name

    @property
    def icon(self) -> str:
        """Return name."""
        return self._icon

    @property
    def unique_id(self) -> str:
        """Return unique id."""
        return self._unique_id

    @property
    def available(self) -> bool:
        """Return availability."""
        return self._is_available

    @property
    def extra_state_attributes(self) -> dict[str, str]:
        """Return device attributes."""
        return self._attributes

    async def async_update(self) -> None:
        """Update data."""
        _LOGGER.debug(f"Updating '{self.name}' ({self._type}) switch state")
        await self._update()

    async def async_turn_on(self, **_kwargs: typing.Any) -> None:
        """Turn on switch."""
        await self._async_handle_turn_on_off(turn_on=True)

    async def async_turn_off(self, **_kwargs: typing.Any) -> None:
        """Turn off switch."""
        await self._async_handle_turn_on_off(turn_on=False)

    async def _async_handle_turn_on_off(self, turn_on: bool) -> None:
        """Handle switch state change request."""
        await self._switch(turn_on)
        self._attr_is_on = turn_on
