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

import typing

from .const import Const
from .diagnostic import Diagnostics
from .hls_stream_output import HlsStreamOutput
from .stream_output import StreamOutput


# pylint: disable=unused-variable
class StreamState:
    """Responsible for trakcing output and playback state for a stream.

    Holds state used for playback to interpret a decoded stream. A source stream
    may be reset (e.g. reconnecting to an rtsp stream) and this object tracks
    the state to inform the player.
    """

    def __init__(
        self,
        outputs_callback: typing.Callable[[], typing.Mapping[str, StreamOutput]],
        diagnostics: Diagnostics,
    ) -> None:
        """Initialize StreamState."""
        self._stream_id: int = 0
        self._outputs_callback = outputs_callback
        # sequence gets incremented before the first segment so the first segment
        # has a sequence number of 0.
        self._sequence = -1
        self._diagnostics = diagnostics

    @property
    def sequence(self) -> int:
        """Return the current sequence for the latest segment."""
        return self._sequence

    def next_sequence(self) -> int:
        """Increment the sequence number."""
        self._sequence += 1
        return self._sequence

    @property
    def stream_id(self) -> int:
        """Return the readonly stream_id attribute."""
        return self._stream_id

    def discontinuity(self) -> None:
        """Mark the stream as having been restarted."""
        # Preserving sequence and stream_id here keep the HLS playlist logic
        # simple to check for discontinuity at output time, and to determine
        # the discontinuity sequence number.
        self._stream_id += 1
        # Call discontinuity to fix incomplete segment in HLS output
        hls_output: HlsStreamOutput = self._outputs_callback().get(Const.HLS_PROVIDER)
        if hls_output:
            hls_output.discontinuity()

    @property
    def outputs(self) -> list[StreamOutput]:
        """Return the active stream outputs."""
        return list(self._outputs_callback().values())

    @property
    def diagnostics(self) -> Diagnostics:
        """Return diagnostics object."""
        return self._diagnostics
