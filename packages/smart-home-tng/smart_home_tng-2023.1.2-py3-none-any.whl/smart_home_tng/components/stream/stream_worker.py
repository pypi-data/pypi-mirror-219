"""
Stream Component for Smart Home - The Next Generation.

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

import contextlib
import logging
import threading
import typing

import attr

try:
    import av

    AVError: typing.TypeAlias = av.AVError
    BitStreamFilter: typing.TypeAlias = av.BitStreamFilter
    Packet: typing.TypeAlias = av.Packet
except ImportError:
    av = None

from ... import core
from .const import Const
from .key_frame_converter import KeyFrameConverter
from .peek_iterator import PeekIterator
from .stream_muxer import StreamMuxer
from .stream_settings import STREAM_SETTINGS_NON_LL_HLS, StreamSettings
from .stream_state import StreamState
from .timestamp_validator import TimestampValidator

_LOGGER: typing.Final = logging.getLogger(__name__)


# pylint: disable=unused-variable
def _stream_worker(
    owner: core.StreamComponent,
    source: str,
    pyav_options: dict[str, str],
    stream_settings: StreamSettings,
    stream_state: StreamState,
    keyframe_converter: KeyFrameConverter,
    quit_event: threading.Event,
) -> None:
    """Handle consuming streams."""
    if av is None:
        return

    if av.library_versions["libavformat"][0] >= 59 and "stimeout" in pyav_options:
        # the stimeout option was renamed to timeout as of ffmpeg 5.0
        pyav_options["timeout"] = pyav_options["stimeout"]
        del pyav_options["stimeout"]
    try:
        container = av.open(source, options=pyav_options, timeout=Const.SOURCE_TIMEOUT)
    except AVError as err:
        # pylint: disable=no-member
        raise core.StreamWorkerError(
            f"Error opening stream ({err.type}, {err.strerror}) "
            + f"{owner.redact_credentials(str(source))}"
        ) from err
    try:
        video_stream = container.streams.video[0]
    except (KeyError, IndexError) as ex:
        raise core.StreamWorkerError("Stream has no video") from ex
    keyframe_converter.create_codec_context(codec_context=video_stream.codec_context)
    try:
        audio_stream = container.streams.audio[0]
    except (KeyError, IndexError):
        audio_stream = None
    if audio_stream and audio_stream.name not in Const.AUDIO_CODECS:
        audio_stream = None
    # Some audio streams do not have a profile and throw errors when remuxing
    if audio_stream and audio_stream.profile is None:
        audio_stream = None
    # Disable ll-hls for hls inputs
    if container.format.name == "hls":
        for field in attr.fields(StreamSettings):
            setattr(
                stream_settings,
                field.name,
                getattr(STREAM_SETTINGS_NON_LL_HLS, field.name),
            )
    stream_state.diagnostics.set_value("container_format", container.format.name)
    stream_state.diagnostics.set_value("video_codec", video_stream.name)
    if audio_stream:
        stream_state.diagnostics.set_value("audio_codec", audio_stream.name)

    dts_validator = TimestampValidator()
    container_packets = PeekIterator(
        filter(dts_validator.is_valid, container.demux((video_stream, audio_stream)))
    )

    # Have to work around two problems with RTSP feeds in ffmpeg
    # 1 - first frame has bad pts/dts https://trac.ffmpeg.org/ticket/5018
    # 2 - seeking can be problematic https://trac.ffmpeg.org/ticket/7815
    #
    # Use a peeking iterator to peek into the start of the stream, ensuring
    # everything looks good, then go back to the start when muxing below.
    try:
        # Get the required bitstream filter
        audio_bsf = _get_audio_bitstream_filter(container_packets.peek(), audio_stream)
        # Advance to the first keyframe for muxing, then rewind so the muxing
        # loop below can consume.
        first_keyframe = next(
            filter(lambda pkt: _is_keyframe(pkt) and _is_video(pkt), container_packets)
        )
        # Deal with problem #1 above (bad first packet pts/dts) by recalculating
        # using pts/dts from second packet. Use the peek iterator to advance
        # without consuming from container_packets. Skip over the first keyframe
        # then use the duration from the second video packet to adjust dts.
        next_video_packet = next(filter(_is_video, container_packets.peek()))
        # Since the is_valid filter has already been applied before the following
        # adjustment, it does not filter out the case where the duration below is
        # 0 and both the first_keyframe and next_video_packet end up with the same
        # dts. Use "or 1" to deal with this.
        start_dts = next_video_packet.dts - (next_video_packet.duration or 1)
        first_keyframe.dts = first_keyframe.pts = start_dts
    except core.StreamWorkerError as ex:
        container.close()
        raise ex
    except StopIteration as ex:
        container.close()
        raise core.StreamEndedError("Stream ended; no additional packets") from ex
    except AVError as ex:
        container.close()
        raise core.StreamWorkerError(
            f"Error demuxing stream while finding first packet: {str(ex)}"
        ) from ex

    muxer = StreamMuxer(
        stream_state.hass,
        video_stream,
        audio_stream,
        audio_bsf,
        stream_state,
        stream_settings,
    )
    muxer.reset(start_dts)

    # Mux the first keyframe, then proceed through the rest of the packets
    muxer.mux_packet(first_keyframe)

    with contextlib.closing(container), contextlib.closing(muxer):
        while not quit_event.is_set():
            try:
                packet = next(container_packets)
            except core.StreamWorkerError as ex:
                raise ex
            except StopIteration as ex:
                raise core.StreamEndedError(
                    "Stream ended; no additional packets"
                ) from ex
            except av.AVError as ex:
                raise core.StreamWorkerError(
                    f"Error demuxing stream: {str(ex)}"
                ) from ex

            muxer.mux_packet(packet)

            if packet.is_keyframe and _is_video(packet):
                keyframe_converter.packet = packet


def _get_audio_bitstream_filter(
    packets: typing.Iterator[Packet], audio_stream: typing.Any
) -> BitStreamFilter:
    """Return the aac_adtstoasc bitstream filter if ADTS AAC is detected."""
    if not audio_stream:
        return None
    for count, packet in enumerate(packets):
        if count >= Const.PACKETS_TO_WAIT_FOR_AUDIO:
            # Some streams declare an audio stream and never send any packets
            _LOGGER.warning("Audio stream not found")
            break
        if packet.stream == audio_stream:
            # detect ADTS AAC and disable audio
            if audio_stream.codec.name == "aac" and packet.size > 2:
                with memoryview(packet) as packet_view:
                    if packet_view[0] == 0xFF and packet_view[1] & 0xF0 == 0xF0:
                        _LOGGER.debug(
                            "ADTS AAC detected. Adding aac_adtstoaac bitstream filter"
                        )
                        return BitStreamFilter("aac_adtstoasc")
            break
    return None


def _is_keyframe(packet: Packet) -> bool:
    """Return true if the packet is a keyframe."""
    return packet.is_keyframe


def _is_video(packet: Packet) -> bool:
    """Return true if the packet is for the video stream."""
    return packet.stream.type == "video"
