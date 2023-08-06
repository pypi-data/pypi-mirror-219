"""
Webhook Component for Smart Home - The Next Generation.

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

import logging
import typing
from aiohttp import web

from ... import core

if not typing.TYPE_CHECKING:

    class WebhookComponent:
        pass


if typing.TYPE_CHECKING:
    from .webhook_component import WebhookComponent

_LOGGER: typing.Final = logging.getLogger(__name__)


# pylint: disable=unused-variable
class WebhookView(core.SmartHomeControllerView):
    """Handle incoming webhook requests."""

    def __init__(self, owner: WebhookComponent):
        url = "/api/webhook/{webhook_id}"
        name = "api:webhook"
        requires_auth = False
        cors_allowed = True
        super().__init__(
            url, name, requires_auth=requires_auth, cors_allowed=cors_allowed
        )
        self._owner = owner

    async def _handle(self, request: web.Request, webhook_id: str) -> web.Response:
        """Handle webhook call."""
        _LOGGER.debug(
            f"Handling webhook {request.method} payload for {webhook_id}",
            request.method,
            webhook_id,
        )
        return await self._owner.async_handle_webhook(webhook_id, request)

    head = _handle
    post = _handle
    put = _handle
