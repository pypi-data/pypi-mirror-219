"""
Philips Hue Integration for Smart Home - The Next Generation.

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

import voluptuous as vol

from ... import core
from .const import Const


# pylint: disable=unused-variable
class HueV1OptionsFlowHandler(core.OptionsFlow):
    """Handle Hue options for V1 implementation."""

    def __init__(
        self,
        config_entry: core.ConfigEntry,
        context: dict = None,
        init_data: typing.Any = None,
    ) -> None:
        """Initialize Hue options flow."""
        super().__init__(config_entry.entry_id, context, init_data)
        self._config_entry = config_entry

    async def async_step_init(
        self, user_input: dict[str, typing.Any] = None
    ) -> core.FlowResult:
        """Manage Hue options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Optional(
                        Const.CONF_ALLOW_HUE_GROUPS,
                        default=self._config_entry.options.get(
                            Const.CONF_ALLOW_HUE_GROUPS, Const.DEFAULT_ALLOW_HUE_GROUPS
                        ),
                    ): bool,
                    vol.Optional(
                        Const.CONF_ALLOW_UNREACHABLE,
                        default=self._config_entry.options.get(
                            Const.CONF_ALLOW_UNREACHABLE,
                            Const.DEFAULT_ALLOW_UNREACHABLE,
                        ),
                    ): bool,
                }
            ),
        )
