"""
Conversation Component for Smart Home - The Next Generation.

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
import logging
import typing

import voluptuous as vol
from aiohttp import web

from ... import core

if not typing.TYPE_CHECKING:

    class ConversationComponent:
        pass


if typing.TYPE_CHECKING:
    from .conversation_component import ConversationComponent

_intent: typing.TypeAlias = core.Intent

_LOGGER: typing.Final = logging.getLogger(__name__)
_VALIDATOR: typing.Final = core.RequestDataValidator(
    vol.Schema({vol.Required("text"): str, vol.Optional("conversation_id"): str})
)


# pylint: disable=unused-variable
class ConversationProcessView(core.SmartHomeControllerView):
    """View to process text."""

    def __init__(
        self,
        owner: ConversationComponent,
        extra_urls: list[str] = None,
        requires_auth=True,
        cors_allowed=False,
    ):
        url = "/api/conversation/process"
        name = "api:conversation:process"
        super().__init__(url, name, extra_urls, requires_auth, cors_allowed)
        self._owner = owner

    async def post(self, request: web.Request):
        """Send a request for processing."""
        data, error = _VALIDATOR.async_get_request_data(request)
        if error:
            return error

        try:
            # pylint: disable=protected-access
            intent_result = await self._owner._async_converse(
                data["text"], data.get("conversation_id"), self.context(request)
            )
        except _intent.IntentError as err:
            _LOGGER.error(f"Error handling intent: {err}")
            return self.json(
                {
                    "success": False,
                    "error": {
                        "code": str(err.__class__.__name__).lower(),
                        "message": str(err),
                    },
                },
                status_code=http.HTTPStatus.INTERNAL_SERVER_ERROR,
            )

        return self.json(intent_result)
