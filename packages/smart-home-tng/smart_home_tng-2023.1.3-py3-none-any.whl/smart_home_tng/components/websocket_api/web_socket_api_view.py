"""
Web Socket Api Component for Smart Home - The Next Generation.

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

from aiohttp import web

from ... import core
from .web_socket_handler import WebSocketHandler


# pylint: disable=unused-variable
class WebSocketAPIView(core.SmartHomeControllerView):
    """View to serve a websockets endpoint."""

    def __init__(self, owner: core.WebSocket.Component):
        super().__init__(core.WebSocket.URL, "websocketapi", requires_auth=False)
        self._owner = owner

    async def get(self, request: web.Request) -> web.WebSocketResponse:
        """Handle an incoming websocket connection."""
        return await WebSocketHandler(self._owner, request).async_handle()
