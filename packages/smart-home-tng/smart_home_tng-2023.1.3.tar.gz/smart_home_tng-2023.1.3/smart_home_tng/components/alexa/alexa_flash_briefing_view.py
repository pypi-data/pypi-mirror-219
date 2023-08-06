"""
Amazon Alexa Integration for Smart Home - The Next Generation.

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

import copy
import hmac
import http
import logging
import typing
import uuid

from aiohttp import web

from ... import core

_alexa: typing.TypeAlias = core.Alexa
_const: typing.TypeAlias = core.Const
_template: typing.TypeAlias = core.Template

_FLASH_BRIEFINGS_API_ENDPOINT: typing.Final = "/api/alexa/flash_briefings/{briefing_id}"
_LOGGER: typing.Final = logging.getLogger(__name__)


# pylint: disable=unused-variable
class AlexaFlashBriefingView(core.SmartHomeControllerView):
    """Handle Alexa Flash Briefing skill requests."""

    def __init__(
        self, owner: core.SmartHomeControllerComponent, flash_briefings: core.ConfigType
    ):
        """Initialize Alexa view."""
        url = _FLASH_BRIEFINGS_API_ENDPOINT
        requires_auth = False
        name = "api:alexa:flash_briefings"
        super().__init__(url, name, requires_auth=requires_auth)
        self._owner = owner
        self._flash_briefings = copy.deepcopy(flash_briefings)
        _template.attach(self.controller, self._flash_briefings)

    @property
    def controller(self) -> core.SmartHomeController:
        return self._owner.controller

    @core.callback
    def get(self, request: web.Request, briefing_id: str):
        """Handle Alexa Flash Briefing request."""
        _LOGGER.debug(f"Received Alexa flash briefing request for: {briefing_id}")

        api_password = request.query.get(_alexa.API_PASSWORD)
        if api_password is None:
            err = f"No password provided for Alexa flash briefing: {briefing_id}"
            _LOGGER.error(err)
            return b"", http.HTTPStatus.UNAUTHORIZED

        if not hmac.compare_digest(
            api_password.encode("utf-8"),
            self._flash_briefings[_const.CONF_PASSWORD].encode("utf-8"),
        ):
            err = f"Wrong password for Alexa flash briefing: {briefing_id}"
            _LOGGER.error(err)
            return b"", http.HTTPStatus.UNAUTHORIZED

        briefings = self._flash_briefings.get(briefing_id)
        if not isinstance(briefings, list):
            err = f"No configured Alexa flash briefing was found for: {briefing_id}"
            _LOGGER.error(err)
            return b"", http.HTTPStatus.NOT_FOUND

        briefing = []

        for item in briefings:
            output = {}
            title = item.get(_alexa.CONF_TITLE)
            if item.get(_alexa.CONF_TITLE) is not None:
                if isinstance(title, _template):
                    output[_alexa.ATTR_TITLE_TEXT] = title.async_render(
                        parse_result=False
                    )
                else:
                    output[_alexa.ATTR_TITLE_TEXT] = title

            text = item.get(_alexa.CONF_TEXT)
            if text is not None:
                if isinstance(text, _template):
                    output[_alexa.ATTR_MAIN_TEXT] = text.async_render(
                        parse_result=False
                    )
                else:
                    output[_alexa.ATTR_MAIN_TEXT] = text

            uid = item.get(_alexa.CONF_UID, str(uuid.uuid4()))
            output[_alexa.ATTR_UID] = uid

            audio = item.get(_alexa.CONF_AUDIO)
            if audio is not None:
                if isinstance(audio, _template):
                    output[_alexa.ATTR_STREAM_URL] = audio.async_render(
                        parse_result=False
                    )
                else:
                    output[_alexa.ATTR_STREAM_URL] = audio

            display_url = item.get(_alexa.CONF_DISPLAY_URL)
            if display_url is not None:
                if isinstance(display_url, _template):
                    output[_alexa.ATTR_REDIRECTION_URL] = display_url.async_render(
                        parse_result=False
                    )
                else:
                    output[_alexa.ATTR_REDIRECTION_URL] = display_url

            output[_alexa.ATTR_UPDATE_DATE] = core.helpers.utcnow().strftime(
                _alexa.DATE_FORMAT
            )

            briefing.append(output)

        return self.json(briefing)
