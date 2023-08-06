"""
Core components of Smart Home - The Next Generation.

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

from aiohttp import web

from .const import Const
from .local_oauth2_implementation import _decode_jwt
from .smart_home_controller_view import SmartHomeControllerView

_AUTH_CALLBACK_PATH: typing.Final = "/auth/external/callback"


# pylint: disable=unused-variable
class OAuth2AuthorizeCallbackView(SmartHomeControllerView):
    """OAuth2 Authorization Callback View."""

    def __init__(self, extra_urls: list[str] = None, cors_allowed=False):
        super().__init__(
            _AUTH_CALLBACK_PATH,
            "auth:external:callback",
            extra_urls,
            False,
            cors_allowed,
        )

    async def get(self, request: web.Request) -> web.Response:
        """Receive authorization code."""
        if "state" not in request.query:
            return web.Response(text="Missing state parameter")

        shc = request.app[Const.KEY_SHC]

        state = _decode_jwt(shc, request.query["state"])

        if state is None:
            return web.Response(text="Invalid state")

        user_input: dict[str, typing.Any] = {"state": state}

        if "code" in request.query:
            user_input["code"] = request.query["code"]
        elif "error" in request.query:
            user_input["error"] = request.query["error"]
        else:
            return web.Response(text="Missing code or error parameter")

        await shc.config_entries.flow.async_configure(
            flow_id=state["flow_id"], user_input=user_input
        )

        return web.Response(
            headers={"content-type": "text/html"},
            text="<script>window.close()</script>",
        )
