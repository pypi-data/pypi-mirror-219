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

import datetime as dt
import io
import logging
import types
import typing

try:
    import av

    AudioStream: typing.TypeAlias = av.audio.stream.AudioStream
    VideoStream: typing.TypeAlias = av.video.VideoStream
    BitStreamFilter: typing.TypeAlias = av.BitStreamFilter
    BitStreamFilterContext: typing.TypeAlias = av.BitStreamFilterContext
    OutputContainer: typing.TypeAlias = av.container.OutputContainer
    Packet: typing.TypeAlias = av.Packet
except ImportError:
    av: types.ModuleType = None

from ... import core
from .const import Const
from .part import Part
from .segment import Segment
from .stream_settings import StreamSettings
from .stream_state import StreamState

_LOGGER: typing.Final = logging.getLogger(__name__)


# pylint: disable=unused-variable
class StreamMuxer:
    """StreamMuxer re-packages video/audio packets for output."""

    def __init__(
        self,
        shc: core.SmartHomeController,
        video_stream: VideoStream,
        audio_stream: AudioStream,
        audio_bsf: BitStreamFilter,
        stream_state: StreamState,
        stream_settings: StreamSettings,
    ) -> None:
        """Initialize StreamMuxer."""
        self._shc = shc
        self._segment_start_dts: int = None
        self._memory_file: io.BytesIO = None
        self._av_output: av.container.OutputContainer = None
        self._input_video_stream: VideoStream = video_stream
        self._input_audio_stream: AudioStream = audio_stream
        self._audio_bsf: BitStreamFilter = audio_bsf
        self._audio_bsf_context: BitStreamFilterContext = None
        self._output_video_stream: VideoStream = None
        self._output_audio_stream: AudioStream = None
        self._segment: Segment = None
        # the following 3 member variables are used for Part formation
        self._memory_file_pos: int = None
        self._part_start_dts: int = None
        self._part_has_keyframe = False
        self._stream_settings = stream_settings
        self._stream_state = stream_state
        self._start_time = dt.datetime.utcnow()

    def make_new_av(
        self,
        memory_file: io.BytesIO,
        sequence: int,
        input_vstream: VideoStream,
        input_astream: AudioStream,
    ) -> tuple[OutputContainer, VideoStream, AudioStream]:
        """Make a new av OutputContainer and add output streams."""

        if av is None:
            _LOGGER.error(
                "Required packages 'ha-av' not installed. " + "Streaming not supported."
            )
            return None, None, None

        container = av.open(
            memory_file,
            mode="w",
            format=Const.SEGMENT_CONTAINER_FORMAT,
            container_options={
                **{
                    # Removed skip_sidx -
                    # see https://github.com/home-assistant/core/pull/39970
                    # "cmaf" flag replaces several of the movflags used,
                    # but too recent to use for now
                    "movflags": (
                        "frag_custom+empty_moov+default_base_moof+"
                        + "frag_discont+negative_cts_offsets+skip_trailer+delay_moov"
                    ),
                    # Sometimes the first segment begins with negative timestamps,
                    # and this setting just adjusts the timestamps in the output
                    # from that segment to start from 0. Helps from having to make
                    # some adjustments in test_durations
                    "avoid_negative_ts": "make_non_negative",
                    "fragment_index": str(sequence + 1),
                    "video_track_timescale": str(int(1 / input_vstream.time_base)),
                },
                # Only do extra fragmenting if we are using ll_hls
                # Let ffmpeg do the work using frag_duration
                # Fragment durations may exceed the 15% allowed variance but it seems ok
                **(
                    {
                        "movflags": (
                            "empty_moov+default_base_moof+frag_discont+"
                            + "negative_cts_offsets+skip_trailer+delay_moov"
                        ),
                        # Create a fragment every TARGET_PART_DURATION. The data
                        # from each fragment is stored in a "Part" that can be
                        # combined with the data from all the other "Part"s, plus
                        # an init # section, to reconstitute the data in a "Segment".
                        # The LL-HLS spec allows for a fragment's duration to be
                        # within the range [0.85x,1.0x] of the part target duration.
                        # We use the frag_duration option to tell ffmpeg to try to
                        # cut the fragments when they reach frag_duration. However,
                        # the resulting fragments can have variability in their
                        # durations and can end up being too short or too long.
                        # With a video track with no audio, the discrete nature
                        # of frames means that the frame at the end of a fragment
                        # will sometimes extend slightly beyond the desired
                        # frag_duration.
                        # If there are two tracks, as in the case of a video feed
                        # with audio, there is an added wrinkle as the fragment
                        # cut seems to be done on the first track that crosses
                        # the desired threshold, and cutting on the audio track
                        # may also result in a shorter video fragment than desired.
                        # Given this, our approach is to give ffmpeg a frag_duration
                        # somewhere in the middle of the range, hoping that the
                        # parts stay pretty well bounded, and we adjust the part
                        # durations a bit in the hls metadata so that everything
                        #  "looks" ok.
                        "frag_duration": str(
                            self._stream_settings.part_target_duration * 9e5
                        ),
                    }
                    if self._stream_settings.ll_hls
                    else {}
                ),
            },
        )
        output_vstream = container.add_stream(template=input_vstream)
        # Check if audio is requested
        output_astream = None
        if input_astream:
            if self._audio_bsf:
                self._audio_bsf_context = self._audio_bsf.create()
                self._audio_bsf_context.set_input_stream(input_astream)
            output_astream = container.add_stream(
                template=self._audio_bsf_context or input_astream
            )
        return container, output_vstream, output_astream

    def reset(self, video_dts: int) -> None:
        """Initialize a new stream segment."""
        self._part_start_dts = self._segment_start_dts = video_dts
        self._segment = None
        self._memory_file = io.BytesIO()
        self._memory_file_pos = 0
        (
            self._av_output,
            self._output_video_stream,
            self._output_audio_stream,
        ) = self.make_new_av(
            memory_file=self._memory_file,
            sequence=self._stream_state.next_sequence(),
            input_vstream=self._input_video_stream,
            input_astream=self._input_audio_stream,
        )
        if self._output_video_stream and self._output_video_stream.name == "hevc":
            self._output_video_stream.codec_tag = "hvc1"

    def mux_packet(self, packet: Packet) -> None:
        """Mux a packet to the appropriate output stream."""

        # Check for end of segment
        if packet.stream == self._input_video_stream:
            if (
                packet.is_keyframe
                and (packet.dts - self._segment_start_dts) * packet.time_base
                >= self._stream_settings.min_segment_duration
            ):
                # Flush segment (also flushes the stub part segment)
                self.flush(packet, last_part=True)

            # Mux the packet
            packet.stream = self._output_video_stream
            self._av_output.mux(packet)
            self.check_flush_part(packet)
            self._part_has_keyframe |= packet.is_keyframe

        elif packet.stream == self._input_audio_stream:
            if self._audio_bsf_context:
                self._audio_bsf_context.send(packet)
                while packet := self._audio_bsf_context.recv():
                    packet.stream = self._output_audio_stream
                    self._av_output.mux(packet)
                return
            packet.stream = self._output_audio_stream
            self._av_output.mux(packet)

    def create_segment(self) -> None:
        """Create a segment when the moov is ready."""
        if av is None:
            return

        self._segment = Segment(
            sequence=self._stream_state.sequence,
            stream_id=self._stream_state.stream_id,
            init=read_init(self._memory_file),
            # Fetch the latest StreamOutputs, which may have changed since the
            # worker started.
            stream_outputs=self._stream_state.outputs,
            start_time=self._start_time,
        )
        self._memory_file_pos = self._memory_file.tell()
        self._memory_file.seek(0, io.SEEK_END)

    def check_flush_part(self, packet: Packet) -> None:
        """Check for and mark a part segment boundary and record its duration."""
        if av is None:
            return

        if self._memory_file_pos == self._memory_file.tell():
            return
        if self._segment is None:
            # We have our first non-zero byte position. This means the init has just
            # been written. Create a Segment and put it to the queue of each output.
            self.create_segment()
            # When using delay_moov, the moov is not written until a moof is also ready
            # Flush the moof
            self.flush(packet, last_part=False)
        else:  # These are the ends of the part segments
            self.flush(packet, last_part=False)

    def flush(self, packet: Packet, last_part: bool) -> None:
        """Output a part from the most recent bytes in the memory_file.

        If last_part is True, also close the segment, give it a duration,
        and clean up the av_output and memory_file.
        There are two different ways to enter this function, and when
        last_part is True, packet has not yet been muxed, while when
        last_part is False, the packet has already been muxed. However,
        in both cases, packet is the next packet and is not included in
        the Part.
        This function writes the duration metadata for the Part and
        for the Segment. However, as the fragmentation done by ffmpeg
        may result in fragment durations which fall outside the
        [0.85x,1.0x] tolerance band allowed by LL-HLS, we need to fudge
        some durations a bit by reporting them as being within that
        range.
        Note that repeated adjustments may cause drift between the part
        durations in the metadata and those in the media and result in
        playback issues in some clients.
        """
        if av is None:
            return

        # Part durations should not exceed the part target duration
        adjusted_dts = min(
            packet.dts,
            self._part_start_dts
            + self._stream_settings.part_target_duration / packet.time_base,
        )
        if last_part:
            # Closing the av_output will write the remaining buffered data to the
            # memory_file as a new moof/mdat.
            self._av_output.close()
            # With delay_moov, this may be the first time the file pointer has
            # moved, so the segment may not yet have been created
            if not self._segment:
                self.create_segment()
        elif not self._part_has_keyframe:
            # Parts which are not the last part or an independent part should
            # not have durations below 0.85 of the part target duration.
            adjusted_dts = max(
                adjusted_dts,
                self._part_start_dts
                + 0.85 * self._stream_settings.part_target_duration / packet.time_base,
            )
        # Undo dts adjustments if we don't have ll_hls
        if not self._stream_settings.ll_hls:
            adjusted_dts = packet.dts
        assert self._segment
        self._memory_file.seek(self._memory_file_pos)
        self._shc.call_soon_threadsafe(
            self._segment.async_add_part,
            Part(
                duration=float(
                    (adjusted_dts - self._part_start_dts) * packet.time_base
                ),
                has_keyframe=self._part_has_keyframe,
                data=self._memory_file.read(),
            ),
            (
                segment_duration := float(
                    (adjusted_dts - self._segment_start_dts) * packet.time_base
                )
            )
            if last_part
            else 0,
        )
        if last_part:
            # If we've written the last part, we can close the memory_file.
            self._memory_file.close()  # We don't need the BytesIO object anymore
            self._start_time += dt.timedelta(seconds=segment_duration)
            # Reinitialize
            self.reset(packet.dts)
        else:
            # For the last part, these will get set again elsewhere so we can skip
            # setting them here.
            self._memory_file_pos = self._memory_file.tell()
            self._part_start_dts = adjusted_dts
        self._part_has_keyframe = False

    def close(self) -> None:
        """Close stream buffer."""
        if self._av_output is not None:
            self._av_output.close()
        if self._memory_file is not None:
            self._memory_file.close()


def read_init(bytes_io: io.BytesIO) -> bytes:
    """Read the init from a mp4 file."""
    bytes_io.seek(24)
    moov_len = int.from_bytes(bytes_io.read(4), byteorder="big")
    bytes_io.seek(0)
    return bytes_io.read(24 + moov_len)
