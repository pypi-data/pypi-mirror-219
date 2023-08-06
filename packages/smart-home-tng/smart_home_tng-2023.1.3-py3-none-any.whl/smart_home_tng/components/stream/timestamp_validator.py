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
import typing

try:
    import av

    Stream: typing.TypeAlias = av.stream.Stream
    Packet: typing.TypeAlias = av.Packet
except ImportError:
    av = None

from ... import core
from .const import Const


# pylint: disable=unused-variable
class TimestampValidator:
    """Validate ordering of timestamps for packets in a stream."""

    def __init__(self) -> None:
        """Initialize the TimestampValidator."""
        # Decompression timestamp of last packet in each stream
        self._last_dts: dict[Stream, int | float] = collections.defaultdict(
            lambda: float("-inf")
        )
        # Number of consecutive missing decompression timestamps
        self._missing_dts = 0

    def is_valid(self, packet: Packet) -> bool:
        """Validate the packet timestamp based on ordering within the stream."""
        # Discard packets missing DTS. Terminate if too many are missing.
        if av is None:
            return False

        if packet.dts is None:
            if self._missing_dts >= Const.MAX_MISSING_DTS:
                raise core.StreamWorkerError(
                    f"No dts in {Const.MAX_MISSING_DTS+1} consecutive packets"
                )
            self._missing_dts += 1
            return False
        self._missing_dts = 0
        # Discard when dts is not monotonic. Terminate if gap is too wide.
        prev_dts = self._last_dts[packet.stream]
        if packet.dts <= prev_dts:
            gap = packet.time_base * (prev_dts - packet.dts)
            if gap > Const.MAX_TIMESTAMP_GAP:
                raise core.StreamWorkerError(
                    f"Timestamp overflow detected: last dts = {prev_dts}, dts = {packet.dts}"
                )
            return False
        self._last_dts[packet.stream] = packet.dts
        return True
