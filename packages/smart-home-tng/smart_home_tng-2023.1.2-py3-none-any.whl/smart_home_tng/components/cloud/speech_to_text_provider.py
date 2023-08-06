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

import aiohttp
import hass_nabucasa as nabucasa  # pylint: disable=import-error

from ... import core

_SUPPORT_LANGUAGES: typing.Final = [
    "da-DK",
    "de-DE",
    "en-AU",
    "en-CA",
    "en-GB",
    "en-US",
    "es-ES",
    "fi-FI",
    "fr-CA",
    "fr-FR",
    "it-IT",
    "ja-JP",
    "nl-NL",
    "pl-PL",
    "pt-PT",
    "ru-RU",
    "sv-SE",
    "th-TH",
    "zh-CN",
    "zh-HK",
]


# pylint: disable=unused-variable
class SpeechToTextProvider(core.SpeechToTextProvider):
    """NabuCasa speech API provider."""

    def __init__(self, cloud: nabucasa.Cloud) -> None:
        """Home Assistant NabuCasa Speech to text."""
        self._cloud = cloud

    @property
    def supported_languages(self) -> list[str]:
        """Return a list of supported languages."""
        return _SUPPORT_LANGUAGES

    @property
    def supported_formats(self) -> list[core.AudioFormat]:
        """Return a list of supported formats."""
        return [core.AudioFormat.WAV, core.AudioFormat.OGG]

    @property
    def supported_codecs(self) -> list[core.AudioCodec]:
        """Return a list of supported codecs."""
        return [core.AudioCodec.PCM, core.AudioCodec.OPUS]

    @property
    def supported_bit_rates(self) -> list[core.AudioBitRate]:
        """Return a list of supported bitrates."""
        return [core.AudioBitRate.BITRATE_16]

    @property
    def supported_sample_rates(self) -> list[core.AudioSampleRate]:
        """Return a list of supported samplerates."""
        return [core.AudioSampleRate.SAMPLERATE_16000]

    @property
    def supported_channels(self) -> list[core.AudioChannel]:
        """Return a list of supported channels."""
        return [core.AudioChannel.MONO]

    async def async_process_audio_stream(
        self, metadata: core.SpeechMetadata, stream: aiohttp.StreamReader
    ) -> core.SpeechResult:
        """Process an audio stream to STT service."""
        content = f"audio/{metadata.format!s}; codecs=audio/{metadata.codec!s}; samplerate=16000"

        # Process STT
        try:
            result = await self._cloud.voice.process_stt(
                stream, content, metadata.language
            )
        except nabucasa.voice.VoiceError:
            return core.SpeechResult(None, core.SpeechResultState.ERROR)

        # Return Speech as Text
        return core.SpeechResult(
            result.text,
            core.SpeechResultState.SUCCESS
            if result.success
            else core.SpeechResultState.ERROR,
        )
