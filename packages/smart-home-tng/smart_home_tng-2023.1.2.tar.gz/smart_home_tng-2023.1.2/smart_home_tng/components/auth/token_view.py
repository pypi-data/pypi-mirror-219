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

from aiohttp import web

from ... import auth, core
from . import helpers


# pylint: disable=unused-variable
class TokenView(core.SmartHomeControllerView):
    """View to issue or revoke tokens."""

    def __init__(self, retrieve_auth):
        """Initialize the token view."""
        super().__init__(
            "/auth/token", "api:auth:token", requires_auth=False, cors_allowed=True
        )
        self._retrieve_auth = retrieve_auth

    @core.SmartHomeController.log_invalid_auth
    async def post(self, request):
        """Grant a token."""
        shc = request.app[core.Const.KEY_SHC]
        data = await request.post()

        grant_type = data.get("grant_type")

        # IndieAuth 6.3.5
        # The revocation endpoint is the same as the token endpoint.
        # The revocation request includes an additional parameter,
        # action=revoke.
        if data.get("action") == "revoke":
            return await self._async_handle_revoke_token(shc, data)

        if grant_type == "authorization_code":
            return await self._async_handle_auth_code(shc, data, request.remote)

        if grant_type == "refresh_token":
            return await self._async_handle_refresh_token(shc, data, request.remote)

        return self.json(
            {"error": "unsupported_grant_type"}, status_code=http.HTTPStatus.BAD_REQUEST
        )

    async def _async_handle_revoke_token(self, hass, data):
        """Handle revoke token request."""

        # OAuth 2.0 Token Revocation [RFC7009]
        # 2.2 The authorization server responds with HTTP status code 200
        # if the token has been revoked successfully or if the client
        # submitted an invalid token.
        if (token := data.get("token")) is None:
            return web.Response(status=http.HTTPStatus.OK)

        refresh_token = await hass.auth.async_get_refresh_token_by_token(token)

        if refresh_token is None:
            return web.Response(status=http.HTTPStatus.OK)

        await hass.auth.async_remove_refresh_token(refresh_token)
        return web.Response(status=http.HTTPStatus.OK)

    async def _async_handle_auth_code(
        self, shc: core.SmartHomeController, data, remote_addr
    ):
        """Handle authorization code request."""
        client_id = data.get("client_id")
        if client_id is None or not helpers.verify_client_id(client_id):
            return self.json(
                {"error": "invalid_request", "error_description": "Invalid client id"},
                status_code=http.HTTPStatus.BAD_REQUEST,
            )

        if (code := data.get("code")) is None:
            return self.json(
                {"error": "invalid_request", "error_description": "Invalid code"},
                status_code=http.HTTPStatus.BAD_REQUEST,
            )

        credential = self._retrieve_auth(client_id, code)

        if credential is None or not isinstance(credential, auth.Credentials):
            return self.json(
                {"error": "invalid_request", "error_description": "Invalid code"},
                status_code=http.HTTPStatus.BAD_REQUEST,
            )

        user = await shc.auth.async_get_or_create_user(credential)

        if user_access_error := shc.http.async_user_not_allowed_do_auth(user):
            return self.json(
                {
                    "error": "access_denied",
                    "error_description": user_access_error,
                },
                status_code=http.HTTPStatus.FORBIDDEN,
            )

        refresh_token = await shc.auth.async_create_refresh_token(
            user, client_id, credential=credential
        )
        try:
            access_token = shc.auth.async_create_access_token(
                refresh_token, remote_addr
            )
        except auth.InvalidAuthError as exc:
            return self.json(
                {"error": "access_denied", "error_description": str(exc)},
                status_code=http.HTTPStatus.FORBIDDEN,
            )

        return self.json(
            {
                "access_token": access_token,
                "token_type": "Bearer",
                "refresh_token": refresh_token.token,
                "expires_in": int(
                    refresh_token.access_token_expiration.total_seconds()
                ),
                "ha_auth_provider": credential.auth_provider_type,
            },
            headers={
                "Cache-Control": "no-store",
                "Pragma": "no-cache",
            },
        )

    async def _async_handle_refresh_token(
        self, shc: core.SmartHomeController, data, remote_addr
    ):
        """Handle authorization code request."""
        client_id = data.get("client_id")
        if client_id is not None and not helpers.verify_client_id(client_id):
            return self.json(
                {"error": "invalid_request", "error_description": "Invalid client id"},
                status_code=http.HTTPStatus.BAD_REQUEST,
            )

        if (token := data.get("refresh_token")) is None:
            return self.json(
                {"error": "invalid_request"}, status_code=http.HTTPStatus.BAD_REQUEST
            )

        refresh_token = await shc.auth.async_get_refresh_token_by_token(token)

        if refresh_token is None:
            return self.json(
                {"error": "invalid_grant"}, status_code=http.HTTPStatus.BAD_REQUEST
            )

        if refresh_token.client_id != client_id:
            return self.json(
                {"error": "invalid_request"}, status_code=http.HTTPStatus.BAD_REQUEST
            )

        if user_access_error := shc.http.async_user_not_allowed_do_auth(
            refresh_token.user
        ):
            return self.json(
                {
                    "error": "access_denied",
                    "error_description": user_access_error,
                },
                status_code=http.HTTPStatus.FORBIDDEN,
            )

        try:
            access_token = shc.auth.async_create_access_token(
                refresh_token, remote_addr
            )
        except auth.InvalidAuthError as exc:
            return self.json(
                {"error": "access_denied", "error_description": str(exc)},
                status_code=http.HTTPStatus.FORBIDDEN,
            )

        return self.json(
            {
                "access_token": access_token,
                "token_type": "Bearer",
                "expires_in": int(
                    refresh_token.access_token_expiration.total_seconds()
                ),
            },
            headers={
                "Cache-Control": "no-store",
                "Pragma": "no-cache",
            },
        )
