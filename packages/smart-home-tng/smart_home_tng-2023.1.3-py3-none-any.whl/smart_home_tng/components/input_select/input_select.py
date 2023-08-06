"""
Input Select Component for Smart Home - The Next Generation.

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
from .const import Const

_LOGGER: typing.Final = logging.getLogger(__name__)


# pylint: disable=unused-variable
class InputSelect(core.Select.Entity, core.RestoreEntity):
    """Representation of a select input."""

    _attr_should_poll = False

    def __init__(
        self,
        config: core.ConfigType,
        owner: core.SmartHomeControllerComponent = None,
        editable=True,
    ) -> None:
        """Initialize a select input."""
        self._attr_current_option = config.get(Const.CONF_INITIAL)
        self._attr_icon = config.get(core.Const.CONF_ICON)
        self._attr_name = config.get(core.Const.CONF_NAME)
        self._attr_options = config[Const.CONF_OPTIONS]
        self._attr_unique_id = config[core.Const.CONF_ID]
        self._editable = editable
        if config and core.Const.CONF_ID in config and owner:
            self._entity_id = f"{owner.domain}.{config[core.Const.CONF_ID]}"

    @property
    def editable(self) -> bool:
        return self._editable

    async def async_added_to_shc(self) -> None:
        """Run when entity about to be added."""
        await super().async_added_to_shc()
        if self.current_option is not None:
            return

        state = await self.async_get_last_state()
        if not state or state.state not in self.options:
            self._attr_current_option = self.options[0]
        else:
            self._attr_current_option = state.state

    @property
    def extra_state_attributes(self) -> dict[str, bool]:
        """Return the state attributes."""
        return {core.Const.ATTR_EDITABLE: self.editable}

    async def async_select_option(self, option: str) -> None:
        """Select new option."""
        if option not in self.options:
            _LOGGER.warning(
                f"Invalid option: {option} (possible options: "
                + f"{', '.join(self.options)})",
            )
            return
        self._attr_current_option = option
        self.async_write_state()

    @core.callback
    def async_select_index(self, idx: int) -> None:
        """Select new option by index."""
        new_index = idx % len(self.options)
        self._attr_current_option = self.options[new_index]
        self.async_write_state()

    @core.callback
    def async_offset_index(self, offset: int, cycle: bool) -> None:
        """Offset current index."""

        current_index = (
            self.options.index(self.current_option)
            if self.current_option is not None
            else 0
        )

        new_index = current_index + offset
        if cycle:
            new_index = new_index % len(self.options)
        elif new_index < 0:
            new_index = 0
        elif new_index >= len(self.options):
            new_index = len(self.options) - 1

        self._attr_current_option = self.options[new_index]
        self.async_write_state()

    @core.callback
    def async_next(self, cycle: bool) -> None:
        """Select next option."""
        # If there is no current option, first item is the next
        if self.current_option is None:
            self.async_select_index(0)
            return
        self.async_offset_index(1, cycle)

    @core.callback
    def async_previous(self, cycle: bool) -> None:
        """Select previous option."""
        # If there is no current option, last item is the previous
        if self.current_option is None:
            self.async_select_index(-1)
            return
        self.async_offset_index(-1, cycle)

    async def async_set_options(self, options: list[str]) -> None:
        """Set options."""
        unique_options = list(dict.fromkeys(options))
        if len(unique_options) != len(options):
            raise core.SmartHomeControllerError(f"Duplicated options: {options}")

        self._attr_options = options

        if self.current_option not in self.options:
            _LOGGER.warning(
                f"Current option: {self.current_option} no longer valid (possible "
                + f"options: {', '.join(self.options)})",
            )
            self._attr_current_option = options[0]

        self.async_write_state()

    async def async_update_config(self, config: core.ConfigType) -> None:
        """Handle when the config is updated."""
        self._attr_icon = config.get(core.Const.CONF_ICON)
        self._attr_name = config.get(core.Const.CONF_NAME)
        self._attr_options = config[Const.CONF_OPTIONS]
        self.async_write_state()
