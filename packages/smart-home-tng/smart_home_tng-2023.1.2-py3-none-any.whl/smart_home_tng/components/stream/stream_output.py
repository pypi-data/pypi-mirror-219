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

import asyncio
import collections

import async_timeout

from ... import core
from .idle_timer import IdleTimer
from .segment import Segment
from .stream_settings import StreamSettings


# pylint: disable=unused-variable
class StreamOutput:
    """Represents a stream output."""

    def __init__(
        self,
        shc: core.SmartHomeController,
        idle_timer: IdleTimer,
        stream_settings: StreamSettings,
        deque_maxlen: int = None,
    ) -> None:
        """Initialize a stream output."""
        self._shc = shc
        self._idle_timer = idle_timer
        self._stream_settings = stream_settings
        self._event = asyncio.Event()
        self._part_event = asyncio.Event()
        self._segments = collections.deque[Segment](maxlen=deque_maxlen)

    @property
    def idle_timer(self) -> IdleTimer:
        return self._idle_timer

    @property
    def name(self) -> str:
        """Return provider name."""
        return None

    @property
    def idle(self) -> bool:
        """Return True if the output is idle."""
        return self._idle_timer.idle

    @property
    def last_sequence(self) -> int:
        """Return the last sequence number without iterating."""
        if self._segments:
            return self._segments[-1].sequence
        return -1

    @property
    def sequences(self) -> list[int]:
        """Return current sequence from segments."""
        return [s.sequence for s in self._segments]

    @property
    def last_segment(self) -> Segment:
        """Return the last segment without iterating."""
        if self._segments:
            return self._segments[-1]
        return None

    def get_segment(self, sequence: int) -> Segment:
        """Retrieve a specific segment."""
        # Most hits will come in the most recent segments, so iterate reversed
        for segment in reversed(self._segments):
            if segment.sequence == sequence:
                return segment
        return None

    def get_segments(self) -> collections.deque[Segment]:
        """Retrieve all segments."""
        return self._segments

    async def part_recv(self, timeout: float = None) -> bool:
        """Wait for an event signalling the latest part segment."""
        try:
            async with async_timeout.timeout(timeout):
                await self._part_event.wait()
        except asyncio.TimeoutError:
            return False
        return True

    def part_put(self) -> None:
        """Set event signalling the latest part segment."""
        # Start idle timeout when we start receiving data
        self._part_event.set()
        self._part_event.clear()

    async def recv(self) -> bool:
        """Wait for the latest segment."""
        await self._event.wait()
        return self.last_segment is not None

    def put(self, segment: Segment) -> None:
        """Store output."""
        self._shc.call_soon_threadsafe(self._async_put, segment)

    @core.callback
    def _async_put(self, segment: Segment) -> None:
        """Store output from event loop."""
        # Start idle timeout when we start receiving data
        self._idle_timer.start()
        self._segments.append(segment)
        self._event.set()
        self._event.clear()

    def cleanup(self) -> None:
        """Handle cleanup."""
        self._event.set()
        self._idle_timer.clear()
