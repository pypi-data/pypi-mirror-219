"""
Home Assistant Cloud Component for Smart Home - The Next Generation.

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

import typing

import hass_nabucasa as nabucasa  # pylint: disable=import-error

from ... import core

_CONF_GENDER: typing.Final = "gender"
_SUPPORT_LANGUAGES: typing.Final = list({key[0] for key in nabucasa.voice.MAP_VOICE})


# pylint: disable=unused-variable
class TextToSpeechProvider(core.TTS.Provider):
    """NabuCasa Cloud speech API provider."""

    def __init__(
        self,
        shc: core.SmartHomeController,
        cloud: nabucasa.Cloud,
        language: str,
        gender: str,
    ) -> None:
        """Initialize cloud provider."""
        super().__init__(shc, "Cloud")
        self._cloud = cloud
        self._language = language
        self._gender = gender

        if self._language is not None:
            return

        self._language, self._gender = cloud.client.prefs.tts_default_voice
        cloud.client.prefs.async_listen_updates(self._sync_prefs)

    async def _sync_prefs(self, prefs):
        """Sync preferences."""
        self._language, self._gender = prefs.tts_default_voice

    @property
    def default_language(self):
        """Return the default language."""
        return self._language

    @property
    def supported_languages(self):
        """Return list of supported languages."""
        return _SUPPORT_LANGUAGES

    @property
    def supported_options(self):
        """Return list of supported options like voice, emotion."""
        return [_CONF_GENDER]

    @property
    def default_options(self):
        """Return a dict include default options."""
        return {_CONF_GENDER: self._gender}

    def get_tts_audio(
        self, message: str, language: str, options: dict = None
    ) -> core.TTS.AudioType:
        return self.controller.run_coroutine_threadsafe(
            self.async_get_tts_audio(message, language, options)
        ).result()

    async def async_get_tts_audio(
        self, message, language, options=None
    ) -> core.TTS.AudioType:
        """Load TTS from NabuCasa Cloud."""
        # Process TTS
        try:
            data = await self._cloud.voice.process_tts(
                message, language, gender=options[_CONF_GENDER]
            )
        except nabucasa.voice.VoiceError:
            return (None, None)

        return ("mp3", data)
