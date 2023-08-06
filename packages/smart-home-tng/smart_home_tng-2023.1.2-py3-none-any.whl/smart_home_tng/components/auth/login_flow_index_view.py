"""
Auth Component for Smart Home - The Next Generation.

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
import ipaddress
import typing

import voluptuous as vol
from aiohttp import web

from ... import core
from . import helpers
from .login_flow_base_view import LoginFlowBaseView

_VALIDATOR: typing.Final = core.RequestDataValidator(
    vol.Schema(
        {
            vol.Required("client_id"): str,
            vol.Required("handler"): vol.Any(str, list),
            vol.Required("redirect_uri"): str,
            vol.Optional("type", default="authorize"): str,
        }
    )
)


# pylint: disable=unused-variable
class LoginFlowIndexView(LoginFlowBaseView):
    """View to create a config flow."""

    def __init__(
        self, flow_mgr, store_result, extra_urls: list[str] = None, cors_allowed=False
    ):
        super().__init__(
            flow_mgr,
            store_result,
            "/auth/login_flow",
            "api:auth:login_flow",
            extra_urls,
            cors_allowed,
        )

    async def get(self, _request):
        """Do not allow index of flows in progress."""
        return web.Response(status=http.HTTPStatus.METHOD_NOT_ALLOWED)

    @core.SmartHomeController.log_invalid_auth
    async def post(self, request):
        """Create a new login flow."""
        data, error = await _VALIDATOR.async_get_request_data(request)
        if error is not None:
            return error

        if not await helpers.verify_redirect_uri(
            request.app[core.Const.KEY_SHC], data["client_id"], data["redirect_uri"]
        ):
            return self.json_message(
                "invalid client id or redirect uri", http.HTTPStatus.BAD_REQUEST
            )

        if isinstance(data["handler"], list):
            handler = tuple(data["handler"])
        else:
            handler = data["handler"]

        try:
            result = await self._flow_mgr.async_init(
                handler,
                context={
                    "ip_address": ipaddress.ip_address(request.remote),
                    "credential_only": data.get("type") == "link_user",
                },
            )
        except core.UnknownHandler:
            return self.json_message(
                "Invalid handler specified", http.HTTPStatus.NOT_FOUND
            )
        except core.UnknownStep:
            return self.json_message(
                "Handler does not support init", http.HTTPStatus.BAD_REQUEST
            )

        return await self._async_flow_result_to_response(
            request, data["client_id"], result
        )
