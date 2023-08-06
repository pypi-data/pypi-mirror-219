"""
TextToSpeech (TTS) Component for Smart Home - The Next Generation.

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

from aiohttp import web

from ... import core
from .speech_manager import SpeechManager

_LOGGER: typing.Final = logging.getLogger(__name__)


# pylint: disable=unused-variable
class TextToSpeechView(core.SmartHomeControllerView):
    """TTS view to serve a speech audio."""

    def __init__(self, tts: SpeechManager) -> None:
        """Initialize a tts view."""
        requires_auth = False
        url = "/api/tts_proxy/{filename}"
        name = "api:tts_speech"
        super().__init__(url, name, requires_auth=requires_auth)
        self._tts = tts

    async def get(self, _request: web.Request, filename: str) -> web.Response:
        """Start a get request."""
        try:
            content, data = await self._tts.async_read_tts(filename)
        except core.SmartHomeControllerError as err:
            _LOGGER.error(f"Error on load tts: {err}")
            return web.Response(status=http.HTTPStatus.NOT_FOUND)

        return web.Response(body=data, content_type=content)
