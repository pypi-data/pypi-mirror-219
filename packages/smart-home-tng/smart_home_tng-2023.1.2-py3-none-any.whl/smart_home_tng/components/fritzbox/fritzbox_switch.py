"""
AVM FRITZ!SmartHome Integration for Smart Home - The Next Generation.

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
from .fritzbox_data_update_coordinator import FritzboxDataUpdateCoordinator
from .fritzbox_entity import FritzboxEntity

if not typing.TYPE_CHECKING:

    class FritzboxIntegration:
        pass


if typing.TYPE_CHECKING:
    from .fritzbox_integration import FritzboxIntegration


class FritzboxSwitch(FritzboxEntity, core.Switch.Entity):
    """The switch class for FRITZ!SmartHome switches."""

    @property
    def is_on(self) -> bool:
        """Return true if the switch is on."""
        return self.device.switch_state  # type: ignore [no-any-return]

    async def async_turn_on(self, **_kwargs: typing.Any) -> None:
        """Turn the switch on."""
        await self._shc.async_add_executor_job(self.device.set_switch_state_on)
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **_kwargs: typing.Any) -> None:
        """Turn the switch off."""
        await self._shc.async_add_executor_job(self.device.set_switch_state_off)
        await self.coordinator.async_request_refresh()


# pylint: disable=unused-variable
async def async_setup_switches(
    owner: FritzboxIntegration,
    entry: core.ConfigEntry,
    async_add_entities: core.AddEntitiesCallback,
) -> None:
    """Set up the FRITZ!SmartHome switch from ConfigEntry."""
    coordinator: FritzboxDataUpdateCoordinator = owner.connection_config[
        entry.entry_id
    ][Const.CONF_COORDINATOR]

    async_add_entities(
        [
            FritzboxSwitch(coordinator, ain)
            for ain, device in coordinator.data.items()
            if device.has_switch
        ]
    )
