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
import collections.abc
import typing

try:
    import av

    Packet: typing.TypeAlias = av.Packet
except ImportError:
    av = None


# pylint: disable=unused-variable
class PeekIterator(collections.abc.Iterator):
    """An Iterator that may allow multiple passes.

    This may be consumed like a normal Iterator, however also supports a
    peek() method that buffers consumed items from the iterator.
    """

    def __init__(self, iterator: collections.abc.Iterator[Packet]) -> None:
        """Initialize PeekIterator."""
        self._iterator = iterator
        self._buffer = collections.deque[Packet]()
        # A pointer to either _iterator or _buffer
        self._next = self._iterator.__next__

    def __iter__(self) -> collections.abc.Iterator:
        """Return an iterator."""
        return self

    def __next__(self) -> Packet:
        """Return and consume the next item available."""
        return self._next()

    def _pop_buffer(self) -> Packet:
        """Consume items from the buffer until exhausted."""
        if self._buffer:
            return self._buffer.popleft()
        # The buffer is empty, so change to consume from the iterator
        self._next = self._iterator.__next__
        return self._next()

    def peek(self) -> collections.abc.Generator[Packet, None, None]:
        """Return items without consuming from the iterator."""
        # Items consumed are added to a buffer for future calls to __next__
        # or peek. First iterate over the buffer from previous calls to peek.
        self._next = self._pop_buffer
        for packet in self._buffer:
            yield packet
        for packet in self._iterator:
            self._buffer.append(packet)
            yield packet
