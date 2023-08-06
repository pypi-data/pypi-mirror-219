"""
Switch As X Component for Smart Home - The Next Generation.

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
from .base_entity import BaseEntity


# pylint: disable=unused-variable
class BaseToggleEntity(BaseEntity, core.Toggle.Entity):
    """Represents a Switch as a ToggleEntity."""

    async def async_turn_on(self, **_kwargs: typing.Any) -> None:
        """Forward the turn_on command to the switch in this light switch."""
        await self._shc.services.async_call(
            self._shc.components.switch.domain,
            core.Const.SERVICE_TURN_ON,
            {core.Const.ATTR_ENTITY_ID: self._switch_entity_id},
            blocking=True,
            context=self._context,
        )

    async def async_turn_off(self, **_kwargs: typing.Any) -> None:
        """Forward the turn_off command to the switch in this light switch."""
        await self._shc.services.async_call(
            self._shc.components.switch.domain,
            core.Const.SERVICE_TURN_OFF,
            {core.Const.ATTR_ENTITY_ID: self._switch_entity_id},
            blocking=True,
            context=self._context,
        )

    # pylint: disable=attribute-defined-outside-init
    @core.callback
    def async_state_changed_listener(self, event: core.Event = None) -> None:
        """Handle child updates."""
        super().async_state_changed_listener(event)
        if (
            not self.available
            or (state := self._shc.states.get(self._switch_entity_id)) is None
        ):
            return

        self._attr_is_on = state.state == core.Const.STATE_ON
