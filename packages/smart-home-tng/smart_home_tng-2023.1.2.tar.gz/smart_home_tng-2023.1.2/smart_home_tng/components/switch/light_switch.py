"""
Switch Component for Smart Home - The Next Generation.

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


# pylint: disable=unused-variable
class LightSwitch(core.Light.Entity):
    """Represents a Switch as a Light."""

    _attr_color_mode = core.Light.ColorMode.ONOFF
    _attr_should_poll = False
    _attr_supported_color_modes = {core.Light.ColorMode.ONOFF}

    def __init__(
        self,
        owner: core.SmartHomeControllerComponent,
        name: str,
        switch_entity_id: str,
        unique_id: str,
    ) -> None:
        """Initialize Light Switch."""
        self._attr_name = name
        self._attr_unique_id = unique_id
        self._switch_entity_id = switch_entity_id
        self._owner = owner

    async def async_turn_on(self, **kwargs: typing.Any) -> None:
        """Forward the turn_on command to the switch in this light switch."""
        await self._shc.services.async_call(
            self._owner.domain,
            core.Const.SERVICE_TURN_ON,
            {core.Const.ATTR_ENTITY_ID: self._switch_entity_id},
            blocking=True,
            context=self._context,
        )

    async def async_turn_off(self, **kwargs: typing.Any) -> None:
        """Forward the turn_off command to the switch in this light switch."""
        await self._owner.controller.services.async_call(
            self._owner.domain,
            core.Const.SERVICE_TURN_OFF,
            {core.Const.ATTR_ENTITY_ID: self._switch_entity_id},
            blocking=True,
            context=self._context,
        )

    async def async_added_to_shc(self) -> None:
        """Register callbacks."""

        @core.callback
        def async_state_changed_listener(_event: core.Event = None) -> None:
            """Handle child updates."""
            if (
                state := self._shc.states.get(self._switch_entity_id)
            ) is None or state.state == core.Const.STATE_UNAVAILABLE:
                self._attr_available = False
                return
            self._attr_available = True
            self._attr_is_on = state.state == core.Const.STATE_ON
            self.async_write_state()

        self.async_on_remove(
            self._shc.tracker.async_track_state_change_event(
                [self._switch_entity_id], async_state_changed_listener
            )
        )
        # Call once on adding
        async_state_changed_listener()
