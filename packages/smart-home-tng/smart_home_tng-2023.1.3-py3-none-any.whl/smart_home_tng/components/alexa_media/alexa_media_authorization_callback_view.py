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

import logging
import typing

from aiohttp import web, web_response, web_exceptions

from ... import core
from .const import Const

_const: typing.TypeAlias = core.Const

_LOGGER: typing.Final = logging.getLogger(__name__)


# pylint: disable=unused-variable
class AlexaMediaAuthorizationCallbackView(core.SmartHomeControllerView):
    """Handle callback from external auth."""

    def __init__(self):
        """Initialize instance"""
        url = Const.AUTH_CALLBACK_PATH
        name = Const.AUTH_CALLBACK_NAME
        requires_auth = False
        super().__init__(url=url, name=name, requires_auth=requires_auth)

    async def get(self, request: web.Request):
        """Receive authorization confirmation."""
        controller = request.app[_const.KEY_SHC]
        try:
            await controller.config_entries.flow.async_configure(
                flow_id=request.query["flow_id"], user_input=None
            )
        except (KeyError, core.UnknownFlow) as ex:
            _LOGGER.debug("Callback flow_id is invalid.")
            raise web_exceptions.HTTPBadRequest() from ex
        return web_response.Response(
            headers={"content-type": "text/html"},
            text="<script>window.close()</script>Success! This window can be closed",
        )
