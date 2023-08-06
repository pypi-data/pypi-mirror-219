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

from ... import core
from .const import Const
from .idle_timer import IdleTimer
from .segment import Segment
from .stream_output import StreamOutput
from .stream_settings import StreamSettings


# pylint: disable=unused-variable
class HlsStreamOutput(StreamOutput):
    """Represents HLS Output formats."""

    def __init__(
        self,
        shc: core.SmartHomeController,
        idle_timer: IdleTimer,
        stream_settings: StreamSettings,
    ) -> None:
        """Initialize HLS output."""
        super().__init__(
            shc, idle_timer, stream_settings, deque_maxlen=Const.MAX_SEGMENTS
        )
        self._target_duration = stream_settings.min_segment_duration

    @property
    def name(self) -> str:
        """Return provider name."""
        return Const.HLS_PROVIDER

    def cleanup(self) -> None:
        """Handle cleanup."""
        super().cleanup()
        self._segments.clear()

    @property
    def target_duration(self) -> float:
        """Return the target duration."""
        return self._target_duration

    @core.callback
    def _async_put(self, segment: Segment) -> None:
        """Async put and also update the target duration.

        The target duration is calculated as the max duration of any given segment.
        Technically it should not change per the hls spec, but some cameras adjust
        their GOPs periodically so we need to account for this change.
        """
        super()._async_put(segment)
        self._target_duration = (
            max((s.duration for s in self._segments), default=segment.duration)
            or self._stream_settings.min_segment_duration
        )

    def discontinuity(self) -> None:
        """Fix incomplete segment at end of deque."""
        self._shc.call_soon_threadsafe(self._async_discontinuity)

    @core.callback
    def _async_discontinuity(self) -> None:
        """Fix incomplete segment at end of deque in event loop."""
        # Fill in the segment duration or delete the segment if empty
        if self._segments:
            if (last_segment := self._segments[-1]).parts:
                last_segment.duration = sum(
                    part.duration for part in last_segment.parts
                )
            else:
                self._segments.pop()
