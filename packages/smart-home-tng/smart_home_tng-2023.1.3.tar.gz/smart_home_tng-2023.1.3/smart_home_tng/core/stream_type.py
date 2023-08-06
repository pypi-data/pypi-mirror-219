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

from ..backports import strenum


# pylint: disable=unused-variable
class StreamType(strenum.LowercaseStrEnum):
    """Camera stream type.

    A camera that supports CAMERA_SUPPORT_STREAM may have a single stream
    type which is used to inform the frontend which player to use.
    Streams with RTSP sources typically use the stream component which uses
    HLS for display. WebRTC streams use the home assistant core for a signal
    path to initiate a stream, but the stream itself is between the client and
    device.
    """

    HLS = enum.auto()
    WEB_RTC = enum.auto()
