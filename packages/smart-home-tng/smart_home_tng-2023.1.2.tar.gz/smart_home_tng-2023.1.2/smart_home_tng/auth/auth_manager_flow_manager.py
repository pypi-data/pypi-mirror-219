"""
Authentication Layer for Smart Home - The Next Generation.

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

import collections.abc
import typing

from ..core.flow_handler import FlowHandler
from ..core.flow_manager import FlowManager
from ..core.flow_result import FlowResult
from ..core.flow_result_type import FlowResultType
from . import providers
from .credentials import Credentials


if not typing.TYPE_CHECKING:

    class AuthManager:
        pass

    class SmartHomeController:
        pass


if typing.TYPE_CHECKING:
    from ..core.smart_home_controller import SmartHomeController
    from .auth_manager import AuthManager


# pylint: disable=unused-variable
class AuthManagerFlowManager(FlowManager):
    """Manage authentication flows."""

    def __init__(self, shc: SmartHomeController, auth_manager: AuthManager) -> None:
        """Init auth manager flows."""
        super().__init__(shc)
        self._auth_manager = auth_manager

    @property
    def auth_manager(self) -> AuthManager:
        return self._auth_manager

    async def async_create_flow(
        self,
        handler_key: typing.Any,
        *,
        context: dict[str, typing.Any] = None,
        data: dict[str, typing.Any] = None,
    ) -> FlowHandler:
        """Create a login flow."""
        auth_provider = self._auth_manager.get_auth_provider(*handler_key)
        if not auth_provider:
            raise KeyError(f"Unknown auth provider {handler_key}")
        return await auth_provider.async_login_flow(context)

    async def async_finish_flow(
        self, flow: FlowHandler, result: FlowResult
    ) -> FlowResult:
        """Return a user as result of login flow."""
        flow = typing.cast(providers.LoginFlow, flow)

        if result["type"] != FlowResultType.CREATE_ENTRY:
            return result

        # we got final result
        if isinstance(result["data"], Credentials):
            result["result"] = result["data"]
            return result

        auth_provider = self._auth_manager.get_auth_provider(*result["handler"])
        if not auth_provider:
            raise KeyError(f"Unknown auth provider {result['handler']}")

        credentials = await auth_provider.async_get_or_create_credentials(
            typing.cast(collections.abc.Mapping[str, str], result["data"]),
        )

        if flow.context.get("credential_only"):
            result["result"] = credentials
            return result

        # multi-factor module cannot enabled for new credential
        # which has not linked to a user yet
        if auth_provider.support_mfa and not credentials.is_new:
            user = await self._auth_manager.async_get_user_by_credentials(credentials)
            if user is not None:
                modules = await self._auth_manager.async_get_enabled_mfa(user)

                if modules:
                    # pylint: disable=protected-access
                    flow._credential = credentials
                    flow._user = user
                    flow._available_mfa_modules = modules
                    return await flow.async_step_select_mfa_module()

        result["result"] = credentials
        return result

    async def async_post_init(self, flow: FlowHandler, result: FlowResult) -> None:
        return
