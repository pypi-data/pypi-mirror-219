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
class CoverSwitch(BaseEntity, core.Cover.Entity):
    """Represents a Switch as a Cover."""

    _attr_supported_features = (
        core.Cover.EntityFeature.OPEN | core.Cover.EntityFeature.CLOSE
    )

    async def async_open_cover(self, **_kwargs: typing.Any) -> None:
        """Open the cover."""
        await self._shc.services.async_call(
            self._shc.components.switch.domain,
            core.Const.SERVICE_TURN_ON,
            {core.Const.ATTR_ENTITY_ID: self._switch_entity_id},
            blocking=True,
            context=self._context,
        )

    async def async_close_cover(self, **_kwargs: typing.Any) -> None:
        """Close cover."""
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

        self._attr_is_closed = state.state != core.Const.STATE_ON


async def async_setup_covers(
    owner: core.SmartHomeControllerComponent,
    config_entry: core.ConfigEntry,
    async_add_entities: core.AddEntitiesCallback,
) -> None:
    """Initialize Cover Switch config entry."""
    registry = owner.controller.entity_registry
    entity_id = registry.async_validate_entity_id(
        config_entry.options[core.Const.CONF_ENTITY_ID]
    )
    wrapped_switch = registry.async_get(entity_id)
    device_id = wrapped_switch.device_id if wrapped_switch else None

    async_add_entities(
        [
            CoverSwitch(
                config_entry.title,
                entity_id,
                config_entry.entry_id,
                device_id,
            )
        ]
    )
