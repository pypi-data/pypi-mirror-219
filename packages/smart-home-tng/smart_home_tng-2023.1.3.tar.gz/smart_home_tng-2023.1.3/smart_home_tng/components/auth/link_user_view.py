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
import typing

import voluptuous as vol

from ... import core


_REQUEST_VALIDATOR: typing.Final = core.RequestDataValidator(
    vol.Schema({"code": str, "client_id": str})
)


# pylint: disable=unused-variable
class LinkUserView(core.SmartHomeControllerView):
    """View to link existing users to new credentials."""

    def __init__(self, retrieve_credentials):
        """Initialize the link user view."""
        super().__init__("/auth/link_user", "api:auth:link_user")
        self._retrieve_credentials = retrieve_credentials

    async def post(self, request):
        """Link a user."""
        data, error = await _REQUEST_VALIDATOR.async_get_request_data(request)
        if error is not None:
            return error

        shc = request.app[core.Const.KEY_SHC]
        user = request[core.Const.KEY_SHC_USER]

        credentials = self._retrieve_credentials(data["client_id"], data["code"])

        if credentials is None:
            return self.json_message(
                "Invalid code", status_code=http.HTTPStatus.BAD_REQUEST
            )

        linked_user = await shc.auth.async_get_user_by_credentials(credentials)
        if linked_user != user and linked_user is not None:
            return self.json_message(
                "Credential already linked", status_code=http.HTTPStatus.BAD_REQUEST
            )

        # No-op if credential is already linked to the user it will be linked to
        if linked_user != user:
            await shc.auth.async_link_user(user, credentials)
        return self.json_message("User linked")
