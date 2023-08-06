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

from ... import core


# pylint: disable=unused-variable
class RevokeTokenView(core.SmartHomeControllerView):
    """View to revoke tokens."""

    def __init__(self):
        url = "/auth/revoke"
        name = "api:auth:revocation"
        requires_auth = False
        cors_allowed = True
        super().__init__(
            url, name, requires_auth=requires_auth, cors_allowed=cors_allowed
        )

    async def post(self, request: web.Request) -> web.Response:
        """Revoke a token."""
        shc: core.SmartHomeController = request.app[core.Const.KEY_SHC]
        data = await request.post()

        # OAuth 2.0 Token Revocation [RFC7009]
        # 2.2 The authorization server responds with HTTP status code 200
        # if the token has been revoked successfully or if the client
        # submitted an invalid token.
        if (token := data.get("token")) is None:
            return web.Response(status=http.HTTPStatus.OK)

        refresh_token = await shc.auth.async_get_refresh_token_by_token(token)

        if refresh_token is None:
            return web.Response(status=http.HTTPStatus.OK)

        await shc.auth.async_remove_refresh_token(refresh_token)
        return web.Response(status=http.HTTPStatus.OK)
