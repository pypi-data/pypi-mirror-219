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

import logging
import typing

from ... import core

_CONF_MEDIA_PLAYER: typing.Final = "media_player"
_CONF_TTS_SERVICE: typing.Final = "tts_service"
_LOGGER: typing.Final = logging.getLogger(__name__)


# pylint: disable=unused-variable
class TextToSpeechNotificationService(core.BaseNotificationService):
    """The TTS Notification Service."""

    def __init__(self, owner: core.SmartHomeControllerComponent, config):
        """Initialize the service."""
        super().__init__(owner.controller)
        _, self._tts_service = core.helpers.split_entity_id(config[_CONF_TTS_SERVICE])
        self._media_player = config[_CONF_MEDIA_PLAYER]
        self._language = config.get(core.TTS.ATTR_LANGUAGE)
        self._owner = owner

    async def async_send_message(self, message="", **_kwargs):
        """Call TTS service to speak the notification."""
        _LOGGER.debug(f"{self._tts_service} '{message}' on {self._media_player}")

        data = {
            core.TTS.ATTR_MESSAGE: message,
            core.Const.ATTR_ENTITY_ID: self._media_player,
        }
        if self._language:
            data[core.TTS.ATTR_LANGUAGE] = self._language

        await self._shc.services.async_call(
            self._owner.domain,
            self._tts_service,
            data,
        )

    def send_message(self, message: str, **kwargs: typing.Any) -> None:
        return self._shc.run_coroutine_threadsafe(
            self.async_send_message(message, **kwargs)
        ).result()
