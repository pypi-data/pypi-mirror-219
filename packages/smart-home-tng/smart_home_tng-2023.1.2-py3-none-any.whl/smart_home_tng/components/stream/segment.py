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
import typing

import attr

from ... import core
from .part import Part

if not typing.TYPE_CHECKING:

    class StreamOutput:
        pass


if typing.TYPE_CHECKING:
    from .stream_output import StreamOutput


# pylint: disable=unused-variable
@attr.s(slots=True)
class Segment:
    """Represent a segment."""

    sequence: int = attr.ib()
    # the init of the mp4 the segment is based on
    init: bytes = attr.ib()
    # For detecting discontinuities across stream restarts
    stream_id: int = attr.ib()
    start_time: dt.datetime = attr.ib()
    _stream_outputs: typing.Iterable[StreamOutput] = attr.ib()
    duration: float = attr.ib(default=0)
    parts: list[Part] = attr.ib(factory=list)
    # Store text of this segment's hls playlist for reuse
    # Use list[str] for easy appends
    hls_playlist_template: list[str] = attr.ib(factory=list)
    hls_playlist_parts: list[str] = attr.ib(factory=list)
    # Number of playlist parts rendered so far
    hls_num_parts_rendered: int = attr.ib(default=0)
    # Set to true when all the parts are rendered
    hls_playlist_complete: bool = attr.ib(default=False)

    def __attrs_post_init__(self) -> None:
        """Run after init."""
        for output in self._stream_outputs:
            output.put(self)

    @property
    def complete(self) -> bool:
        """Return whether the Segment is complete."""
        return self.duration > 0

    @property
    def data_size_with_init(self) -> int:
        """Return the size of all part data + init in bytes."""
        return len(self.init) + self.data_size

    @property
    def data_size(self) -> int:
        """Return the size of all part data without init in bytes."""
        return sum(len(part.data) for part in self.parts)

    @core.callback
    def async_add_part(
        self,
        part: Part,
        duration: float,
    ) -> None:
        """Add a part to the Segment.

        Duration is non zero only for the last part.
        """
        self.parts.append(part)
        self.duration = duration
        for output in self._stream_outputs:
            output.part_put()

    def get_data(self) -> bytes:
        """Return reconstructed data for all parts as bytes, without init."""
        return b"".join([part.data for part in self.parts])

    def _render_hls_template(self, last_stream_id: int, render_parts: bool) -> str:
        """Render the HLS playlist section for the Segment.

        The Segment may still be in progress.
        This method stores intermediate data in hls_playlist_parts, hls_num_parts_rendered,
        and hls_playlist_complete to avoid redoing work on subsequent calls.
        """
        if self.hls_playlist_complete:
            return self.hls_playlist_template[0]
        if not self.hls_playlist_template:
            # Logically EXT-X-DISCONTINUITY makes sense above the parts, but Apple's
            # media stream validator seems to only want it before the segment
            if last_stream_id != self.stream_id:
                self.hls_playlist_template.append("#EXT-X-DISCONTINUITY")
            # This is a placeholder where the rendered parts will be inserted
            self.hls_playlist_template.append("{}")
        if render_parts:
            for part_num, part in enumerate(
                self.parts[self.hls_num_parts_rendered :], self.hls_num_parts_rendered
            ):
                self.hls_playlist_parts.append(
                    f"#EXT-X-PART:DURATION={part.duration:.3f},URI="
                    + f'"./segment/{self.sequence}.{part_num}.m4s"'
                    + f'{",INDEPENDENT=YES" if part.has_keyframe else ""}'
                )
        if self.complete:
            # Construct the final playlist_template. The placeholder will share a line with
            # the first element to avoid an extra newline when we don't render any parts.
            # Append an empty string to create a trailing newline when we do render parts
            self.hls_playlist_parts.append("")
            self.hls_playlist_template = (
                [] if last_stream_id == self.stream_id else ["#EXT-X-DISCONTINUITY"]
            )
            # Add the remaining segment metadata
            # The placeholder goes on the same line as the next element
            self.hls_playlist_template.extend(
                [
                    "{}#EXT-X-PROGRAM-DATE-TIME:"
                    + self.start_time.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]
                    + "Z",
                    f"#EXTINF:{self.duration:.3f},\n./segment/{self.sequence}.m4s",
                ]
            )

        # Store intermediate playlist data in member variables for reuse
        self.hls_playlist_template = ["\n".join(self.hls_playlist_template)]
        # lstrip discards extra preceding newline in case first render was empty
        self.hls_playlist_parts = ["\n".join(self.hls_playlist_parts).lstrip()]
        self.hls_num_parts_rendered = len(self.parts)
        self.hls_playlist_complete = self.complete

        return self.hls_playlist_template[0]

    def render_hls(
        self, last_stream_id: int, render_parts: bool, add_hint: bool
    ) -> str:
        """Render the HLS playlist section for the Segment including a hint if requested."""
        playlist_template = self._render_hls_template(last_stream_id, render_parts)
        playlist = playlist_template.format(
            self.hls_playlist_parts[0] if render_parts else ""
        )
        if not add_hint:
            return playlist
        # Preload hints help save round trips by informing the client about the next part.
        # The next part will usually be in this segment but will be first part of the next
        # segment if this segment is already complete.
        if self.complete:  # Next part belongs to next segment
            sequence = self.sequence + 1
            part_num = 0
        else:  # Next part is in the same segment
            sequence = self.sequence
            part_num = len(self.parts)
        hint = (
            f'#EXT-X-PRELOAD-HINT:TYPE=PART,URI="./segment/{sequence}.{part_num}.m4s"'
        )
        return (playlist + "\n" + hint) if playlist else hint
