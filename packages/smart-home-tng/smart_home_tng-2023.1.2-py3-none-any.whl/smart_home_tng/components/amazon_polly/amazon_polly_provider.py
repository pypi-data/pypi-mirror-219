"""
Amazon Polly Integration for Smart Home - The Next Generation.

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

import boto3

from ... import core
from .const import Const

# pylint: disable=invalid-name
_tts: typing.TypeAlias = core.TTS
_LOGGER: typing.Final = logging.getLogger(__name__)


# pylint: disable=unused-variable
class AmazonPollyProvider(_tts.Provider):
    """Amazon Polly speech api provider."""

    def __init__(
        self,
        polly_client: boto3.client,
        config: core.ConfigType,
        supported_languages: list[str],
        all_voices: dict[str, dict[str, str]],
    ) -> None:
        """Initialize Amazon Polly provider for TTS."""
        super().__init__("Amazon Polly")
        self._client = polly_client
        self._config = config
        self._supported_langs = supported_languages
        self._all_voices = all_voices
        self._default_voice: str = self._config[Const.CONF_VOICE]

    @property
    def supported_languages(self) -> list[str]:
        """Return a list of supported languages."""
        return self._supported_langs

    @property
    def default_language(self) -> str | None:
        """Return the default language."""
        return self._all_voices.get(self._default_voice, {}).get("LanguageCode")

    @property
    def default_options(self) -> dict[str, str]:
        """Return dict include default options."""
        return {Const.CONF_VOICE: self._default_voice}

    @property
    def supported_options(self) -> list[str]:
        """Return a list of supported options."""
        return [
            Const.CONF_VOICE,
            Const.CONF_ENGINE,
            Const.CONF_OUTPUT_FORMAT,
            Const.CONF_SAMPLE_RATE,
            Const.CONF_TEXT_TYPE,
        ]

    def get_tts_audio(
        self,
        message: str,
        language: str = None,
        options: dict[str, str] = None,
    ) -> _tts.AudioType:
        """Request TTS file from Polly."""
        if options is None or language is None:
            _LOGGER.debug("language and/or options were missing")
            return None, None
        voice_id = options.get(Const.CONF_VOICE, self._default_voice)
        voice_in_dict = self._all_voices[voice_id]
        if language != voice_in_dict.get("LanguageCode"):
            _LOGGER.error(f"{voice_id} does not support the {language} language")
            return None, None

        engine = options.get(Const.CONF_ENGINE, None)
        output_format = options.get(Const.CONF_OUTPUT_FORMAT, None)
        sample_rate = options.get(Const.CONF_SAMPLE_RATE, None)
        text_type = options.get(Const.CONF_TEXT_TYPE, None)
        if not bool(engine):
            engine = self._config[Const.CONF_ENGINE]
        if not bool(output_format):
            output_format = self._config[Const.CONF_OUTPUT_FORMAT]
        if not bool(sample_rate):
            sample_rate = self._config[Const.CONF_SAMPLE_RATE]
        if not bool(text_type):
            text_type = self._config[Const.CONF_TEXT_TYPE]

        _LOGGER.debug(f"Requesting TTS file for text: {message}")
        resp = self._client.synthesize_speech(
            Engine=engine,
            OutputFormat=output_format,
            SampleRate=sample_rate,
            Text=message,
            TextType=text_type,
            VoiceId=voice_id,
        )

        _LOGGER.debug(f"Reply received for TTS: {message}")
        return (
            Const.CONTENT_TYPE_EXTENSIONS[resp.get("ContentType")],
            resp.get("AudioStream").read(),
        )
