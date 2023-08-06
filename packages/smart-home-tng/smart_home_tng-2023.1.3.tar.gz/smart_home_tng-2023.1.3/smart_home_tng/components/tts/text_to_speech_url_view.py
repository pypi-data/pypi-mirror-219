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
class TextToSpeechUrlView(core.SmartHomeControllerView):
    """TTS view to get a url to a generated speech file."""

    def __init__(self, tts: SpeechManager):
        """Initialize a tts view."""
        self._tts = tts
        requires_auth = True
        url = "/api/tts_get_url"
        name = "api:tts:geturl"
        super().__init__(url, name, requires_auth=requires_auth)

    async def post(self, request: web.Request) -> web.Response:
        """Generate speech and provide url."""
        try:
            data = await request.json()
        except ValueError:
            return self.json_message(
                "Invalid JSON specified", http.HTTPStatus.BAD_REQUEST
            )
        if not data.get(core.TTS.ATTR_PLATFORM) and data.get(core.TTS.ATTR_MESSAGE):
            return self.json_message(
                "Must specify platform and message", http.HTTPStatus.BAD_REQUEST
            )

        p_type = data[core.TTS.ATTR_PLATFORM]
        message = data[core.TTS.ATTR_MESSAGE]
        cache = data.get(core.TTS.ATTR_CACHE)
        language = data.get(core.TTS.ATTR_LANGUAGE)
        options = data.get(core.TTS.ATTR_OPTIONS)

        try:
            path = await self._tts.async_get_url_path(
                p_type, message, cache=cache, language=language, options=options
            )
        except core.SmartHomeControllerError as err:
            _LOGGER.error(f"Error on init tts: {err}")
            return self.json({"error": err}, http.HTTPStatus.BAD_REQUEST)

        base = self._tts.base_url or self._tts.controller.get_url()
        url = base + path

        return self.json({"url": url, "path": path})
