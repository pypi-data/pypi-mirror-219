"""
Sun Component for Smart Home - The Next Generation.

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
class SunConfigFlow(core.ConfigFlow):
    """Config flow for Sun."""

    def __init__(
        self,
        owner: core.SmartHomeControllerComponent,
        context: dict[str, typing.Any] = None,
        data: typing.Any = None,
    ):
        version = 1
        super().__init__(owner.controller, owner.domain, context, data, version)

    async def async_step_user(
        self, user_input: dict[str, typing.Any] = None
    ) -> core.FlowResult:
        """Handle a flow initialized by the user."""
        if self._async_current_entries():
            return self.async_abort(reason="single_instance_allowed")

        if user_input is not None:
            return self.async_create_entry(title=Const.DEFAULT_NAME, data={})

        return self.async_show_form(step_id="user")

    async def async_step_import(
        self, user_input: dict[str, typing.Any]
    ) -> core.FlowResult:
        """Handle import from configuration.yaml."""
        return await self.async_step_user(user_input)
