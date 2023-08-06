"""
Authentication Provider Layer for Smart Home - The Next Generation.

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

import voluptuous as vol

from ...core import helpers
from ...core.flow_handler import FlowHandler
from ...core.flow_result import FlowResult
from ...core.smart_home_controller_error import SmartHomeControllerError
from ..const import Const
from ..credentials import Credentials
from ..user import User
from .auth_provider import AuthProvider

_LOGGER: typing.Final = logging.getLogger(__name__)


# pylint: disable=unused-variable
class LoginFlow(FlowHandler):
    """Handler for the login flow."""

    def __init__(
        self,
        auth_provider: AuthProvider,
        context: dict[str, typing.Any] = None,
        data: typing.Any = None,
        version: int = 1,
    ) -> None:
        """Initialize the login flow."""
        super().__init__((auth_provider.type, None), context, data, version)
        self._auth_provider = auth_provider
        self._auth_module_id: str = None
        self._auth_manager = auth_provider.controller.auth
        self._available_mfa_modules: dict[str, str] = {}
        self._created_at = helpers.utcnow()
        self._invalid_mfa_times = 0
        self._user: User = None
        self._credential: Credentials = None

    async def async_step_init(self, _user_input: dict[str, str] = None) -> FlowResult:
        """Handle the first step of login flow.

        Return self.async_show_form(step_id='init') if user_input is None.
        Return await self.async_finish(flow_result) if login init step pass.
        """
        raise NotImplementedError()

    async def async_step_select_mfa_module(
        self, user_input: dict[str, str] = None
    ) -> FlowResult:
        """Handle the step of select mfa module."""
        errors = {}

        if user_input is not None:
            auth_module = user_input.get("multi_factor_auth_module")
            if auth_module in self._available_mfa_modules:
                self._auth_module_id = auth_module
                return await self.async_step_mfa()
            errors["base"] = "invalid_auth_module"

        if len(self._available_mfa_modules) == 1:
            self._auth_module_id = list(self._available_mfa_modules)[0]
            return await self.async_step_mfa()

        return self.async_show_form(
            step_id="select_mfa_module",
            data_schema=vol.Schema(
                {"multi_factor_auth_module": vol.In(self._available_mfa_modules)}
            ),
            errors=errors,
        )

    async def async_step_mfa(self, user_input: dict[str, str] = None) -> FlowResult:
        """Handle the step of mfa validation."""
        assert self._credential
        assert self._user

        errors = {}

        assert self._auth_module_id is not None
        auth_module = self._auth_manager.get_auth_mfa_module(self._auth_module_id)
        if auth_module is None:
            # Given an invalid input to async_step_select_mfa_module
            # will show invalid_auth_module error
            return await self.async_step_select_mfa_module(user_input={})

        if user_input is None and hasattr(
            auth_module, "async_initialize_login_mfa_step"
        ):
            try:
                await auth_module.async_initialize_login_mfa_step(  # type: ignore[attr-defined]
                    self._user.id
                )
            except SmartHomeControllerError:
                _LOGGER.exception("Error initializing MFA step")
                return self.async_abort(reason="unknown_error")

        if user_input is not None:
            expires = self._created_at + Const.MFA_SESSION_EXPIRATION
            if helpers.utcnow() > expires:
                return self.async_abort(reason="login_expired")

            result = await auth_module.async_validate(self._user.id, user_input)
            if not result:
                errors["base"] = "invalid_code"
                self._invalid_mfa_times += 1
                if self._invalid_mfa_times >= auth_module.max_retry_time > 0:
                    return self.async_abort(reason="too_many_retry")

            if not errors:
                return await self.async_finish(self._credential)

        description_placeholders: dict[str, str] = {
            "mfa_module_name": auth_module.name,
            "mfa_module_id": auth_module.id,
        }

        return self.async_show_form(
            step_id="mfa",
            data_schema=auth_module.input_schema,
            description_placeholders=description_placeholders,
            errors=errors,
        )

    async def async_finish(self, flow_result: typing.Any) -> FlowResult:
        """Handle the pass of login flow."""
        return self.async_create_entry(title=self._auth_provider.name, data=flow_result)
