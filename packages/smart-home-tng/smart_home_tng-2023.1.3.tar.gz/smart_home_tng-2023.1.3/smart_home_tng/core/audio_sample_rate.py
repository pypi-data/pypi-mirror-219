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

import enum


# pylint: disable=unused-variable
class AudioSampleRate(enum.Enum):
    """Supported Audio sample rates."""

    SAMPLERATE_8000 = 8000
    SAMPLERATE_11000 = 11000
    SAMPLERATE_16000 = 16000
    SAMPLERATE_18900 = 18900
    SAMPLERATE_22000 = 22000
    SAMPLERATE_32000 = 32000
    SAMPLERATE_37800 = 37800
    SAMPLERATE_44100 = 44100
    SAMPLERATE_48000 = 48000
