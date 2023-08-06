"""
Onboarding Component for Smart Home - The Next Generation.

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

import http
import typing

import voluptuous as vol

from ... import core
from ..auth import helpers
from .base_onboarding_view import _BaseOnboardingView
from .step import Step


if not typing.TYPE_CHECKING:

    class Onboarding:
        ...


if typing.TYPE_CHECKING:
    from .onboarding import Onboarding

_VALIDATOR: typing.Final = core.RequestDataValidator(
    vol.Schema({vol.Required("client_id"): str, vol.Required("redirect_uri"): str})
)


# pylint: disable=unused-variable
class IntegrationOnboardingView(_BaseOnboardingView):
    """View to finish integration onboarding step."""

    def __init__(self, owner: Onboarding, data, store):
        url = "/api/onboarding/integration"
        name = "api:onboarding:integration"
        super().__init__(
            owner,
            url,
            name,
            step=Step.INTEGRATION,
            data=data,
            store=store,
        )

    async def post(self, request):
        """Handle token creation."""
        shc: core.SmartHomeController = request.app[core.Const.KEY_SHC]
        refresh_token_id = request[core.Const.KEY_SHC_REFRESH_TOKEN_ID]
        data, error = await _VALIDATOR.async_get_request_data(request)
        if error is not None:
            return error

        async with self._lock:
            if self._async_is_done():
                return self.json_message(
                    "Integration step already done", http.HTTPStatus.FORBIDDEN
                )

            await self._async_mark_done(shc)

            # Validate client ID and redirect uri
            if not await helpers.verify_redirect_uri(
                shc, data["client_id"], data["redirect_uri"]
            ):
                return self.json_message(
                    "invalid client id or redirect uri", http.HTTPStatus.BAD_REQUEST
                )

            refresh_token = await shc.auth.async_get_refresh_token(refresh_token_id)
            if refresh_token is None or refresh_token.credential is None:
                return self.json_message(
                    "Credentials for user not available", http.HTTPStatus.FORBIDDEN
                )

            # Return authorization code so we can redirect user and log them in
            auth_code = ""
            comp = core.SmartHomeControllerComponent.get_component("auth")
            if isinstance(comp, core.AuthComponent):
                auth_code = comp.create_auth_code(
                    data["client_id"], refresh_token.credential
                )
            return self.json({"auth_code": auth_code})
