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

import collections
import io
import logging
import os
import typing

try:
    import av

    # pylint: disable=no-member
    OutputContainer: typing.TypeAlias = av.OutputContainer
except ImportError:
    av = None

from ... import core
from .const import Const
from .idle_timer import IdleTimer
from .segment import Segment
from .stream_output import StreamOutput
from .stream_settings import StreamSettings

_LOGGER: typing.Final = logging.getLogger(__name__)


# pylint: disable=unused-variable
class RecorderOutput(StreamOutput):
    """Represents the Recorder Output format."""

    def __init__(
        self,
        shc: core.SmartHomeController,
        idle_timer: IdleTimer,
        stream_settings: StreamSettings,
    ) -> None:
        """Initialize recorder output."""
        super().__init__(shc, idle_timer, stream_settings)
        self.video_path: str

    @property
    def name(self) -> str:
        """Return provider name."""
        return Const.RECORDER_PROVIDER

    def prepend(self, segments: list[Segment]) -> None:
        """Prepend segments to existing list."""
        self._segments.extendleft(reversed(segments))

    def cleanup(self) -> None:
        """Handle cleanup."""
        self.idle_timer.idle = True
        super().cleanup()

    async def async_record(self) -> None:
        """Handle saving stream."""

        if av is None:
            _LOGGER.error("Required packet AV not installed. Recording not supported.")
            return

        os.makedirs(os.path.dirname(self.video_path), exist_ok=True)

        pts_adjuster: dict[str, int | None] = {"video": None, "audio": None}
        output: av.container.OutputContainer | None = None
        output_v = None
        output_a = None

        last_stream_id = -1
        # The running duration of processed segments. Note that this is in av.time_base
        # units which seem to be defined inversely to how stream time_bases are defined
        running_duration = 0

        last_sequence = float("-inf")

        def write_segment(segment: Segment) -> None:
            """Write a segment to output."""
            nonlocal output, output_v, output_a, last_stream_id, running_duration, last_sequence
            # Because the stream_worker is in a different thread from the record service,
            # the lookback segments may still have some overlap with the recorder segments
            if segment.sequence <= last_sequence:
                return
            last_sequence = segment.sequence

            # Open segment
            source = av.open(
                io.BytesIO(segment.init + segment.get_data()),
                "r",
                format=Const.SEGMENT_CONTAINER_FORMAT,
            )
            # Skip this segment if it doesn't have data
            if source.duration is None:
                source.close()
                return
            source_v = source.streams.video[0]
            source_a = (
                source.streams.audio[0] if len(source.streams.audio) > 0 else None
            )

            # Create output on first segment
            if not output:
                output = av.open(
                    self.video_path + ".tmp",
                    "w",
                    format=Const.RECORDER_CONTAINER_FORMAT,
                    container_options={
                        "video_track_timescale": str(int(1 / source_v.time_base))
                    },
                )

            # Add output streams if necessary
            if not output_v:
                output_v = output.add_stream(template=source_v)
                context = output_v.codec_context
                context.flags |= "GLOBAL_HEADER"
            if source_a and not output_a:
                output_a = output.add_stream(template=source_a)

            # Recalculate pts adjustments on first segment and on any discontinuity
            # We are assuming time base is the same across all discontinuities
            if last_stream_id != segment.stream_id:
                last_stream_id = segment.stream_id
                pts_adjuster["video"] = int(
                    (running_duration - source.start_time)
                    / (av.time_base * source_v.time_base)
                )
                if source_a:
                    pts_adjuster["audio"] = int(
                        (running_duration - source.start_time)
                        / (av.time_base * source_a.time_base)
                    )

            # Remux video
            for packet in source.demux():
                if packet.dts is None:
                    continue
                packet.pts += pts_adjuster[packet.stream.type]
                packet.dts += pts_adjuster[packet.stream.type]
                packet.stream = output_v if packet.stream.type == "video" else output_a
                output.mux(packet)

            running_duration += source.duration - source.start_time

            source.close()

        def finish_writing(
            segments: collections.deque[Segment],
            output: OutputContainer,
            video_path: str,
        ) -> None:
            """Finish writing output."""
            # Should only have 0 or 1 segments, but loop through just in case
            while segments:
                write_segment(segments.popleft())
            if output is None:
                _LOGGER.error("Recording failed to capture anything")
                return
            output.close()
            try:
                os.rename(video_path + ".tmp", video_path)
            except FileNotFoundError:
                _LOGGER.error(
                    f"Error writing to '{video_path}'. There are likely multiple "
                    + "recordings writing to the same file",
                )

        # Write lookback segments
        while len(self._segments) > 1:  # The last segment is in progress
            await self._shc.async_add_executor_job(
                write_segment, self._segments.popleft()
            )
        # Make sure the first segment has been added
        if not self._segments:
            await self.recv()
        # Write segments as soon as they are completed
        while not self.idle:
            await self.recv()
            await self._shc.async_add_executor_job(
                write_segment, self._segments.popleft()
            )
        # Write remaining segments and close output
        await self._shc.async_add_executor_job(
            finish_writing, self._segments, output, self.video_path
        )
