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

from ... import core
from . import helpers
from .login_flow_base_view import LoginFlowBaseView

_VALIDATOR: typing.Final = core.RequestDataValidator(
    vol.Schema({"client_id": str}, extra=vol.ALLOW_EXTRA)
)


# pylint: disable=unused-variable
class LoginFlowResourceView(LoginFlowBaseView):
    """View to interact with the flow manager."""

    def __init__(
        self, flow_mgr, store_result, extra_urls: list[str] = None, cors_allowed=False
    ):
        super().__init__(
            flow_mgr,
            store_result,
            "/auth/login_flow/{flow_id}",
            "api:auth:login_flow:resource",
            extra_urls,
            cors_allowed,
        )

    async def get(self, _request):
        """Do not allow getting status of a flow in progress."""
        return self.json_message("Invalid flow specified", http.HTTPStatus.NOT_FOUND)

    @core.SmartHomeController.log_invalid_auth
    async def post(self, request, flow_id):
        """Handle progressing a login flow request."""
        data, error = await _VALIDATOR.async_get_request_data(request)
        if error is not None:
            return error

        client_id = data.pop("client_id")

        if not helpers.verify_client_id(client_id):
            return self.json_message("Invalid client id", http.HTTPStatus.BAD_REQUEST)

        try:
            # do not allow change ip during login flow
            flow = self._flow_mgr.async_get(flow_id)
            if flow["context"]["ip_address"] != ipaddress.ip_address(request.remote):
                return self.json_message(
                    "IP address changed", http.HTTPStatus.BAD_REQUEST
                )
            result = await self._flow_mgr.async_configure(flow_id, data)
        except core.UnknownFlow:
            return self.json_message(
                "Invalid flow specified", http.HTTPStatus.NOT_FOUND
            )
        except vol.Invalid:
            return self.json_message(
                "User input malformed", http.HTTPStatus.BAD_REQUEST
            )

        return await self._async_flow_result_to_response(request, client_id, result)

    async def delete(self, _request, flow_id):
        """Cancel a flow in progress."""
        try:
            self._flow_mgr.async_abort(flow_id)
        except core.UnknownFlow:
            return self.json_message(
                "Invalid flow specified", http.HTTPStatus.NOT_FOUND
            )

        return self.json_message("Flow aborted")
