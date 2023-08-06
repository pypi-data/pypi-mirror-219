"""
Multi Factor Authentication Layer for Smart Home - The Next Generation.

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

import voluptuous as vol

from ...core.flow_handler import FlowHandler
from ...core.flow_result import FlowResult
from .multi_factor_auth_module import MultiFactorAuthModule


# pylint: disable=unused-variable
class SetupFlow(FlowHandler):
    """Handler for the setup flow."""

    def __init__(
        self,
        auth_module: MultiFactorAuthModule,
        setup_schema: vol.Schema,
        user_id: str,
        handler="setup",
    ) -> None:
        """Initialize the setup flow."""
        super().__init__(handler)
        self._auth_module = auth_module
        self._setup_schema = setup_schema
        self._user_id = user_id

    async def async_step_init(self, user_input: dict[str, str] = None) -> FlowResult:
        """Handle the first step of setup flow.

        Return self.async_show_form(step_id='init') if user_input is None.
        Return self.async_create_entry(data={'result': result}) if finish.
        """
        errors: dict[str, str] = {}

        if user_input:
            result = await self._auth_module.async_setup_user(self._user_id, user_input)
            return self.async_create_entry(
                title=self._auth_module.name, data={"result": result}
            )

        return self.async_show_form(
            step_id="init", data_schema=self._setup_schema, errors=errors
        )
