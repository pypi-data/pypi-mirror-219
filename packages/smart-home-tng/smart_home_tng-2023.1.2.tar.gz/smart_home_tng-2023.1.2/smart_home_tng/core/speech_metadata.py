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

import attr

from .audio_bit_rate import AudioBitRate
from .audio_channel import AudioChannel
from .audio_codec import AudioCodec
from .audio_format import AudioFormat
from .audio_sample_rate import AudioSampleRate


# pylint: disable=unused-variable
@attr.s
class SpeechMetadata:
    """Metadata of audio stream."""

    language: str = attr.ib()
    format: AudioFormat = attr.ib()
    codec: AudioCodec = attr.ib()
    bit_rate: AudioBitRate = attr.ib(converter=int)
    sample_rate: AudioSampleRate = attr.ib(converter=int)
    channel: AudioChannel = attr.ib(converter=int)
