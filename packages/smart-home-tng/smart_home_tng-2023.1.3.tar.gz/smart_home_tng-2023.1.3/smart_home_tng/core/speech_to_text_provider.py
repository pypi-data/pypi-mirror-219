"""
Core components of Smart Home - The Next Generation.

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

import abc
import aiohttp

from .audio_bit_rate import AudioBitRate
from .audio_channel import AudioChannel
from .audio_codec import AudioCodec
from .audio_format import AudioFormat
from .audio_sample_rate import AudioSampleRate
from .callback import callback
from .speech_metadata import SpeechMetadata
from .speech_result import SpeechResult


# pylint: disable=unused-variable
class SpeechToTextProvider(abc.ABC):
    """Represent a single STT provider."""

    @property
    def name(self) -> str:
        return None

    @property
    @abc.abstractmethod
    def supported_languages(self) -> list[str]:
        """Return a list of supported languages."""

    @property
    @abc.abstractmethod
    def supported_formats(self) -> list[AudioFormat]:
        """Return a list of supported formats."""

    @property
    @abc.abstractmethod
    def supported_codecs(self) -> list[AudioCodec]:
        """Return a list of supported codecs."""

    @property
    @abc.abstractmethod
    def supported_bit_rates(self) -> list[AudioBitRate]:
        """Return a list of supported bit rates."""

    @property
    @abc.abstractmethod
    def supported_sample_rates(self) -> list[AudioSampleRate]:
        """Return a list of supported sample rates."""

    @property
    @abc.abstractmethod
    def supported_channels(self) -> list[AudioChannel]:
        """Return a list of supported channels."""

    @abc.abstractmethod
    async def async_process_audio_stream(
        self, metadata: SpeechMetadata, stream: aiohttp.StreamReader
    ) -> SpeechResult:
        """Process an audio stream to STT service.

        Only streaming of content are allowed!
        """

    @callback
    def check_metadata(self, metadata: SpeechMetadata) -> bool:
        """Check if given metadata supported by this provider."""
        if (
            metadata.language not in self.supported_languages
            or metadata.format not in self.supported_formats
            or metadata.codec not in self.supported_codecs
            or metadata.bit_rate not in self.supported_bit_rates
            or metadata.sample_rate not in self.supported_sample_rates
            or metadata.channel not in self.supported_channels
        ):
            return False
        return True
