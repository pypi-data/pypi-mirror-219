"""
Input Boolean Component for Smart Home - The Next Generation.

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


# pylint: disable=unused-variable
class InputBoolean(core.Toggle.Entity, core.RestoreEntity):
    """Representation of a boolean input."""

    _attr_should_poll = False
    _domain: str

    def __init__(self, config: core.ConfigType) -> None:
        """Initialize a boolean input."""
        self._config = config
        self._editable = True
        self._attr_is_on = config.get(Const.CONF_INITIAL, False)
        self._attr_unique_id = config[core.Const.CONF_ID]

    @property
    def editable(self) -> bool:
        return self._editable

    @classmethod
    def from_yaml(cls, config: core.ConfigType):
        """Return entity instance initialized from yaml storage."""
        input_bool = cls(config)
        input_bool._entity_id = f"{InputBoolean._domain}.{config[core.Const.CONF_ID]}"
        input_bool._editable = False
        return input_bool

    @property
    def name(self) -> str:
        """Return name of the boolean input."""
        return self._config.get(core.Const.CONF_NAME)

    @property
    def icon(self) -> str:
        """Return the icon to be used for this entity."""
        return self._config.get(core.Const.CONF_ICON)

    @property
    def extra_state_attributes(self) -> dict[str, bool]:
        """Return the state attributes of the entity."""
        return {core.Const.ATTR_EDITABLE: self.editable}

    async def async_added_to_shc(self) -> None:
        """Call when entity about to be added to hass."""
        # Don't restore if we got an initial value.
        await super().async_added_to_shc()
        if self._config.get(Const.CONF_INITIAL) is not None:
            return

        state = await self.async_get_last_state()
        self._attr_is_on = state is not None and state.state == core.Const.STATE_ON

    async def async_turn_on(self, **kwargs: typing.Any) -> None:
        """Turn the entity on."""
        self._attr_is_on = True
        self.async_write_state()

    async def async_turn_off(self, **kwargs: typing.Any) -> None:
        """Turn the entity off."""
        self._attr_is_on = False
        self.async_write_state()

    async def async_update_config(self, config: core.ConfigType) -> None:
        """Handle when the config is updated."""
        self._config = config
        self.async_write_state()
