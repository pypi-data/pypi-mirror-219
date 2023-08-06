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
import typing

from .smart_home_controller_component import SmartHomeControllerComponent

if not typing.TYPE_CHECKING:

    class StreamBase:
        pass


if typing.TYPE_CHECKING:
    from .stream_base import StreamBase


class _Const:
    """Constants for Stream component."""

    ATTR_ENDPOINTS: typing.Final = "endpoints"
    ATTR_SETTINGS: typing.Final = "settings"
    ATTR_STREAMS: typing.Final = "streams"

    RECORDER_PROVIDER: typing.Final = "recorder"

    HLS_PROVIDER: typing.Final = "hls"
    OUTPUT_FORMATS: typing.Final = [HLS_PROVIDER]

    SEGMENT_CONTAINER_FORMAT: typing.Final = "mp4"  # format for segments
    RECORDER_CONTAINER_FORMAT: typing.Final = "mp4"  # format for recorder output
    AUDIO_CODECS: typing.Final = {"aac", "mp3"}

    FORMAT_CONTENT_TYPE: typing.Final = {HLS_PROVIDER: "application/vnd.apple.mpegurl"}

    OUTPUT_IDLE_TIMEOUT: typing.Final = 300  # Idle timeout due to inactivity

    NUM_PLAYLIST_SEGMENTS: typing.Final = 3  # Number of segments to use in HLS playlist
    MAX_SEGMENTS: typing.Final = 5  # Max number of segments to keep around
    TARGET_SEGMENT_DURATION_NON_LL_HLS: typing.Final = (
        2.0  # Each segment is about this many seconds
    )
    SEGMENT_DURATION_ADJUSTER: typing.Final = (
        0.1  # Used to avoid missing keyframe boundaries
    )
    # Number of target durations to start before the end of the playlist.
    # 1.5 should put us in the middle of the second to last segment even with
    # variable keyframe intervals.
    EXT_X_START_NON_LL_HLS: typing.Final = 1.5
    # Number of part durations to start before the end of the playlist with LL-HLS
    EXT_X_START_LL_HLS: typing.Final = 2

    PACKETS_TO_WAIT_FOR_AUDIO: typing.Final = (
        20  # Some streams have an audio stream with no audio
    )
    MAX_TIMESTAMP_GAP: typing.Final = (
        10000  # seconds - anything from 10 to 50000 is probably reasonable
    )

    MAX_MISSING_DTS: typing.Final = 6  # Number of packets missing DTS to allow
    SOURCE_TIMEOUT: typing.Final = 30  # Timeout for reading stream source

    STREAM_RESTART_INCREMENT: typing.Final = (
        10  # Increase wait_timeout by this amount each retry
    )
    STREAM_RESTART_RESET_TIME: typing.Final = (
        300  # Reset wait_timeout after this many seconds
    )

    CONF_LL_HLS: typing.Final = "ll_hls"
    CONF_PART_DURATION: typing.Final = "part_duration"
    CONF_SEGMENT_DURATION: typing.Final = "segment_duration"

    CONF_PREFER_TCP: typing.Final = "prefer_tcp"
    CONF_RTSP_TRANSPORT: typing.Final = "rtsp_transport"
    # The first dict entry below may be used as the default when populating options
    RTSP_TRANSPORTS: typing.Final = {
        "tcp": "TCP",
        "udp": "UDP",
        "udp_multicast": "UDP Multicast",
        "http": "HTTP",
    }
    CONF_USE_WALLCLOCK_AS_TIMESTAMPS: typing.Final = "use_wallclock_as_timestamps"
    CONF_EXTRA_PART_WAIT_TIME: typing.Final = "extra_part_wait_time"


# pylint: disable=unused-variable


class StreamComponent(SmartHomeControllerComponent):
    """Required base class for Stream Component."""

    # pylint: disable=invalid-name
    Const: typing.TypeAlias = _Const

    @abc.abstractmethod
    def redact_credentials(self, data: str) -> str:
        """Redact credentials from string data."""

    @abc.abstractmethod
    def create_stream(
        self,
        stream_source: str,
        options: typing.Mapping[str, str | bool | float],
        stream_label: str = None,
    ) -> StreamBase:
        """Create a stream with the specified identfier based on the source url.

        The stream_source is typically an rtsp url (though any url accepted by ffmpeg is fine) and
        options (see STREAM_OPTIONS_SCHEMA) are converted and passed into pyav / ffmpeg.

        The stream_label is a string used as an additional message in logging.
        """


class StreamWorkerError(Exception):
    """An exception thrown while processing a stream."""


class StreamEndedError(StreamWorkerError):
    """Raised when the stream is complete, exposed for facilitating testing."""
