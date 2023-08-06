"""
PyScript Component for Smart Home - The Next Generation.

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


This component is based on the custom_component

Pyscript: Python Scripting for Home Assistant, Copyright (c) 2020-2022 Craig Barrat,
which may be freely used and copied according tho the terms of the Apache 2.0 License.

Original source code and documentation can be found under:
https://github.com/custom-components/pyscript
"""

import typing

import voluptuous as vol

from ... import core
from .const import Const


# pylint: disable=unused-variable
class PyscriptOptionsConfigFlow(core.OptionsFlow):
    """Handle a pyscript options flow."""

    def __init__(
        self, owner: core.SmartHomeControllerComponent, config_entry: core.ConfigEntry
    ) -> None:
        """Initialize pyscript options flow."""
        super().__init__(None)
        self._config_entry = config_entry
        self._show_form = False
        self._owner = owner

    async def async_step_init(
        self, user_input: dict[str, typing.Any] = None
    ) -> dict[str, typing.Any]:
        """Manage the pyscript options."""
        if self._config_entry.source == core.ConfigEntrySource.IMPORT:
            self._show_form = True
            return await self.async_step_no_ui_configuration_allowed()

        if user_input is None:
            return self.async_show_form(
                step_id="init",
                data_schema=vol.Schema(
                    {
                        vol.Optional(
                            name, default=self._config_entry.data.get(name, False)
                        ): bool
                        for name in Const.CONF_BOOL_ALL
                    },
                    extra=vol.ALLOW_EXTRA,
                ),
            )

        if any(
            name not in self._config_entry.data
            or user_input[name] != self._config_entry.data[name]
            for name in Const.CONF_BOOL_ALL
        ):
            updated_data = self._config_entry.data.copy()
            updated_data.update(user_input)
            self._owner.controller.config_entries.async_update_entry(
                entry=self._config_entry, data=updated_data
            )
            return self.async_create_entry(title="", data={})

        self._show_form = True
        return await self.async_step_no_update()

    async def async_step_no_ui_configuration_allowed(
        self, _user_input: dict[str, typing.Any] = None
    ) -> dict[str, typing.Any]:
        """Tell user no UI configuration is allowed."""
        if self._show_form:
            self._show_form = False
            return self.async_abort(reason="no_ui_configuration_allowed")

        return self.async_create_entry(title="", data={})

    async def async_step_no_update(
        self, _user_input: dict[str, typing.Any] = None
    ) -> dict[str, typing.Any]:
        """Tell user no update to process."""
        if self._show_form:
            self._show_form = False
            return self.async_abort(reason="no_update")

        return self.async_create_entry(title="", data={})
