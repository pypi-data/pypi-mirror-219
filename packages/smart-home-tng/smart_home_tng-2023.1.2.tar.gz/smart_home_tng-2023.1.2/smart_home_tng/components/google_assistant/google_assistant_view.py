"""
Google Assistant Integration  for Smart Home - The Next Generation.

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


# pylint: disable=unused-variable
class GoogleAssistantView(core.SmartHomeControllerView):
    """Handle Google Assistant requests."""

    def __init__(self, owner: core.GoogleAssistant.Component, config):
        """Initialize the Google Assistant request handler."""
        self._config = config
        url = core.GoogleAssistant.GOOGLE_ASSISTANT_API_ENDPOINT
        name = "api:google_assistant"
        requires_auth = True
        super().__init__(url, name, requires_auth=requires_auth)
        self._owner = owner

    async def post(self, request: web.Request) -> web.Response:
        """Handle Google Assistant requests."""
        message: dict = await request.json()
        result = await self._owner.async_handle_message(
            self._config,
            request[core.Const.KEY_SHC_USER].id,
            message,
            core.GoogleAssistant.SOURCE_CLOUD,
        )
        return self.json(result)
