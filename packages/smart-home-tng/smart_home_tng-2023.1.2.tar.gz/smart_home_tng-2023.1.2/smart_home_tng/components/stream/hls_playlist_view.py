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

import http
import typing

from aiohttp import web

from .const import Const
from .hls_stream_output import HlsStreamOutput
from .stream import Stream
from .stream_view import StreamView

if not typing.TYPE_CHECKING:

    class StreamComponent:
        pass


if typing.TYPE_CHECKING:
    from .stream_component import StreamComponent


# pylint: disable=unused-variable
class HlsPlaylistView(StreamView):
    """Stream view to serve a M3U8 stream."""

    def __init__(self, owner: StreamComponent):
        url = r"/api/hls/{token:[a-f0-9]+}/playlist.m3u8"
        name = "api:stream:hls:playlist"
        cors_allowed = True
        super().__init__(owner, url, name, cors_allowed=cors_allowed)

    @classmethod
    def render(cls, track: HlsStreamOutput) -> str:
        """Render HLS playlist file."""
        # NUM_PLAYLIST_SEGMENTS+1 because most recent is probably not yet complete
        segments = list(track.get_segments())[-(Const.NUM_PLAYLIST_SEGMENTS + 1) :]

        # To cap the number of complete segments at NUM_PLAYLIST_SEGMENTS,
        # remove the first segment if the last segment is actually complete
        if segments[-1].complete:
            segments = segments[-Const.NUM_PLAYLIST_SEGMENTS :]

        first_segment = segments[0]
        playlist = [
            "#EXTM3U",
            "#EXT-X-VERSION:6",
            "#EXT-X-INDEPENDENT-SEGMENTS",
            '#EXT-X-MAP:URI="init.mp4"',
            f"#EXT-X-TARGETDURATION:{track.target_duration:.0f}",
            f"#EXT-X-MEDIA-SEQUENCE:{first_segment.sequence}",
            f"#EXT-X-DISCONTINUITY-SEQUENCE:{first_segment.stream_id}",
        ]

        if track.stream_settings.ll_hls:
            time_offset = (
                Const.EXT_X_START_LL_HLS * track.stream_settings.part_target_duration
            )
            playlist.extend(
                [
                    (
                        "#EXT-X-PART-INF:PART-TARGET="
                        + f"{track.stream_settings.part_target_duration:.3f}"
                    ),
                    (
                        "#EXT-X-SERVER-CONTROL:CAN-BLOCK-RELOAD=YES,PART-HOLD-BACK="
                        + f"{2*track.stream_settings.part_target_duration:.3f}"
                    ),
                    ("#EXT-X-START:TIME-OFFSET=-" + f"{time_offset:.3f},PRECISE=YES"),
                ]
            )
        else:
            # Since our window doesn't have many segments, we don't want to start
            # at the beginning or we risk a behind live window exception in Exoplayer.
            # EXT-X-START is not supposed to be within 3 target durations of the end,
            # but a value as low as 1.5 doesn't seem to hurt.
            # A value below 3 may not be as useful for hls.js as many hls.js clients
            # don't autoplay. Also, hls.js uses the player parameter liveSyncDuration
            # which seems to take precedence for setting target delay. Yet it also
            # doesn't seem to hurt, so we can stick with it for now.
            playlist.append(
                "#EXT-X-START:TIME-OFFSET=-"
                + f"{Const.EXT_X_START_NON_LL_HLS*track.target_duration:.3f}"
                + ",PRECISE=YES"
            )

        last_stream_id = first_segment.stream_id

        # Add playlist sections for completed segments
        # Enumeration used to only include EXT-X-PART data for last 3 segments.
        # The RFC seems to suggest removing parts after 3 full segments, but Apple's
        # own example shows removing after 2 full segments and 1 part one.
        for i, segment in enumerate(segments[:-1], 3 - len(segments)):
            playlist.append(
                segment.render_hls(
                    last_stream_id=last_stream_id,
                    render_parts=i >= 0 and track.stream_settings.ll_hls,
                    add_hint=False,
                )
            )
            last_stream_id = segment.stream_id

        playlist.append(
            segments[-1].render_hls(
                last_stream_id=last_stream_id,
                render_parts=track.stream_settings.ll_hls,
                add_hint=track.stream_settings.ll_hls,
            )
        )

        return "\n".join(playlist) + "\n"

    @staticmethod
    def bad_request() -> web.Response:
        """Return a HTTP Bad Request response."""
        return web.Response(
            body=None,
            status=http.HTTPStatus.BAD_REQUEST,
        )

    @staticmethod
    def not_found() -> web.Response:
        """Return a HTTP Not Found response."""
        return web.Response(
            body=None,
            status=http.HTTPStatus.NOT_FOUND,
        )

    async def handle(
        self, request: web.Request, stream: Stream, sequence: str, part_num: str
    ) -> web.Response:
        """Return m3u8 playlist."""
        # pylint: disable=protected-access
        track: HlsStreamOutput = stream._internal_add_provider(Const.HLS_PROVIDER)

        await stream.start()

        hls_msn: str | int = request.query.get("_HLS_msn")
        hls_part: str | int = request.query.get("_HLS_part")

        # If the Playlist URI contains an _HLS_part directive but no _HLS_msn
        # directive, the Server MUST return Bad Request, such as HTTP 400.
        if hls_msn is None and hls_part:
            return web.HTTPBadRequest()

        hls_msn = int(hls_msn or 0)

        # If the _HLS_msn is greater than the Media Sequence Number of the last
        # Media Segment in the current Playlist plus two, or if the _HLS_part
        # exceeds the last Part Segment in the current Playlist by the
        # Advance Part Limit, then the server SHOULD immediately return Bad
        # Request, such as HTTP 400.
        if hls_msn > track.last_sequence + 2:
            return self.bad_request()

        if hls_part is None:
            # We need to wait for the whole segment, so effectively the next msn
            hls_part = -1
            hls_msn += 1
        else:
            hls_part = int(hls_part)

        while hls_msn > track.last_sequence:
            if not await track.recv():
                return self.not_found()
        if track.last_segment is None:
            return self.not_found()
        if (
            (last_segment := track.last_segment)
            and hls_msn == last_segment.sequence
            and hls_part
            >= len(last_segment.parts)
            - 1
            + track.stream_settings.hls_advance_part_limit
        ):
            return self.bad_request()

        # Receive parts until msn and part are met
        while (
            (last_segment := track.last_segment)
            and hls_msn == last_segment.sequence
            and hls_part >= len(last_segment.parts)
        ):
            if not await track.part_recv(
                timeout=track.stream_settings.hls_part_timeout
            ):
                return self.not_found()
        # Now we should have msn.part >= hls_msn.hls_part. However, in the case
        # that we have a rollover part request from the previous segment, we need
        # to make sure that the new segment has a part. From 6.2.5.2 of the RFC:
        # If the Client requests a Part Index greater than that of the final
        # Partial Segment of the Parent Segment, the Server MUST treat the
        # request as one for Part Index 0 of the following Parent Segment.
        if hls_msn + 1 == last_segment.sequence:
            if not (previous_segment := track.get_segment(hls_msn)) or (
                hls_part >= len(previous_segment.parts)
                and not last_segment.parts
                and not await track.part_recv(
                    timeout=track.stream_settings.hls_part_timeout
                )
            ):
                return self.not_found()

        response = web.Response(
            body=self.render(track).encode("utf-8"),
            headers={
                "Content-Type": Const.FORMAT_CONTENT_TYPE[Const.HLS_PROVIDER],
            },
        )
        response.enable_compression(web.ContentCoding.gzip)
        return response
