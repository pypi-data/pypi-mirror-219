"""
Amazon Alexa MediaPlayer Integration for Smart Home - The Next Generation.

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

This integration is based custom_component "alexa_media_player"
from the Home Assistant Community Store (HACS), which is distributed
under the Terms of the Apache License, Version 2.0

The original source code and license terms can be found under:
https://github.com/custom_components/alexa_media_player
"""

import datetime as dt
import logging
import typing

import httpx
from aiohttp import web

from ... import core
from .const import Const

_const: typing.TypeAlias = core.Const

_LOGGER: typing.Final = logging.getLogger(__name__)


# pylint: disable=unused-variable
class AlexaMediaAuthorizationProxyView(core.SmartHomeControllerView):
    """Handle proxy connections."""

    _known_ips: dict[str, dt.datetime] = {}
    _auth_seconds: int = 300

    def __init__(self, handler: web.RequestHandler):
        """Initialize routes for view.

        Args:
            handler (web.RequestHandler): Handler to apply to all method types

        """
        url = Const.AUTH_PROXY_PATH
        extra_urls = [f"{Const.AUTH_PROXY_PATH}/{{tail:.*}}"]
        name = Const.AUTH_PROXY_NAME
        requires_auth: bool = False
        super().__init__(url, name, extra_urls, requires_auth)
        AlexaMediaAuthorizationProxyView._handler = handler
        for method in ("get", "post", "delete", "put", "patch", "head", "options"):
            setattr(self, method, self.check_auth())

    @classmethod
    def check_auth(cls):
        """Wrap authentication into the handler."""

        async def wrapped(request: web.Request, **kwargs):
            """Notify that the API is running."""
            controller: core.SmartHomeController = request.app[_const.KEY_SHC]
            success = False
            if (
                request.remote not in cls._known_ips
                or (dt.datetime.now() - cls._known_ips.get(request.remote)).seconds
                > cls._auth_seconds
            ):
                try:
                    flow_id = request.url.query["config_flow_id"]
                except KeyError as ex:
                    raise core.Unauthorized() from ex
                for flow in controller.config_entries.flow.async_progress():
                    if flow["flow_id"] == flow_id:
                        _LOGGER.debug(
                            f"Found flow_id; adding {request.remote} to known_ips for "
                            + f"{cls._auth_seconds} seconds",
                        )
                        success = True
                if not success:
                    raise core.Unauthorized()
                cls._known_ips[request.remote] = dt.datetime.now()
            try:
                return await cls._handler(request, **kwargs)
            except httpx.ConnectError as ex:  # pylyint: disable=broad-except
                _LOGGER.warning(f"Detected Connection error: {ex}")
                return web.Response(
                    headers={"content-type": "text/html"},
                    text=f"Connection Error! Please try refreshing.<br /><pre>{ex}</pre>",
                )

        return wrapped

    @classmethod
    def reset(cls) -> None:
        """Reset the view."""
        cls._known_ips = {}
