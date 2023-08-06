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

from aiohttp import web

from .const import Const
from .stream import Stream
from .stream_output import StreamOutput
from .stream_view import StreamView

if not typing.TYPE_CHECKING:

    class StreamComponent:
        pass


if typing.TYPE_CHECKING:
    from .stream_component import StreamComponent


# pylint: disable=unused-variable
class HlsMasterPlaylistView(StreamView):
    """Stream view used only for Chromecast compatibility."""

    def __init__(self, owner: StreamComponent):
        url = r"/api/hls/{token:[a-f0-9]+}/master_playlist.m3u8"
        name = "api:stream:hls:master_playlist"
        cors_allowed = True
        super().__init__(owner, url, name, cors_allowed=cors_allowed)

    @staticmethod
    def render(track: StreamOutput) -> str:
        """Render M3U8 file."""
        # Need to calculate max bandwidth as input_container.bit_rate doesn't seem to work
        # Calculate file size / duration and use a small multiplier to account for variation
        # hls spec already allows for 25% variation
        if not (segment := track.get_segment(track.sequences[-2])):
            return ""
        bandwidth = round(segment.data_size_with_init * 8 / segment.duration * 1.2)
        codecs = _get_codec_string(segment.init)
        lines = [
            "#EXTM3U",
            f'#EXT-X-STREAM-INF:BANDWIDTH={bandwidth},CODECS="{codecs}"',
            "playlist.m3u8",
        ]
        return "\n".join(lines) + "\n"

    async def handle(
        self, request: web.Request, stream: Stream, sequence: str, part_num: str
    ) -> web.Response:
        """Return m3u8 playlist."""
        track = stream.add_provider(Const.HLS_PROVIDER)
        await stream.start()
        # Make sure at least two segments are ready (last one may not be complete)
        if not track.sequences and not await track.recv():
            return web.HTTPNotFound()
        if len(track.sequences) == 1 and not await track.recv():
            return web.HTTPNotFound()
        response = web.Response(
            body=self.render(track).encode("utf-8"),
            headers={
                "Content-Type": Const.FORMAT_CONTENT_TYPE[Const.HLS_PROVIDER],
            },
        )
        response.enable_compression(web.ContentCoding.gzip)
        return response


def _get_codec_string(mp4_bytes: bytes) -> str:
    """Get RFC 6381 codec string."""
    codecs = []

    # Find moov
    moov_location = next(_find_box(mp4_bytes, b"moov"))

    # Find tracks
    for trak_location in _find_box(mp4_bytes, b"trak", moov_location):
        # Drill down to media info
        mdia_location = next(_find_box(mp4_bytes, b"mdia", trak_location))
        minf_location = next(_find_box(mp4_bytes, b"minf", mdia_location))
        stbl_location = next(_find_box(mp4_bytes, b"stbl", minf_location))
        stsd_location = next(_find_box(mp4_bytes, b"stsd", stbl_location))

        # Get stsd box
        stsd_length = int.from_bytes(
            mp4_bytes[stsd_location : stsd_location + 4], byteorder="big"
        )
        stsd_box = mp4_bytes[stsd_location : stsd_location + stsd_length]

        # Base Codec
        codec = stsd_box[20:24].decode("utf-8")

        # Handle H264
        if (
            codec in ("avc1", "avc2", "avc3", "avc4")
            and stsd_length > 110
            and stsd_box[106:110] == b"avcC"
        ):
            profile = stsd_box[111:112].hex()
            compatibility = stsd_box[112:113].hex()
            # Cap level at 4.1 for compatibility with some Google Cast devices
            level = hex(min(stsd_box[113], 41))[2:]
            codec += "." + profile + compatibility + level

        # Handle H265
        elif (
            codec in ("hev1", "hvc1")
            and stsd_length > 110
            and stsd_box[106:110] == b"hvcC"
        ):
            tmp_byte = int.from_bytes(stsd_box[111:112], byteorder="big")

            # Profile Space
            codec += "."
            profile_space_map = {0: "", 1: "A", 2: "B", 3: "C"}
            profile_space = tmp_byte >> 6
            codec += profile_space_map[profile_space]
            general_profile_idc = tmp_byte & 31
            codec += str(general_profile_idc)

            # Compatibility
            codec += "."
            general_profile_compatibility = int.from_bytes(
                stsd_box[112:116], byteorder="big"
            )
            reverse = 0
            for i in range(0, 32):
                reverse |= general_profile_compatibility & 1
                if i == 31:
                    break
                reverse <<= 1
                general_profile_compatibility >>= 1
            codec += hex(reverse)[2:]

            # Tier Flag
            if (tmp_byte & 32) >> 5 == 0:
                codec += ".L"
            else:
                codec += ".H"
            codec += str(int.from_bytes(stsd_box[122:123], byteorder="big"))

            # Constraint String
            has_byte = False
            constraint_string = ""
            for i in range(121, 115, -1):
                gci = int.from_bytes(stsd_box[i : i + 1], byteorder="big")
                if gci or has_byte:
                    constraint_string = "." + hex(gci)[2:] + constraint_string
                    has_byte = True
            codec += constraint_string

        # Handle Audio
        elif codec == "mp4a":
            oti = None
            dsi = None

            # Parse ES Descriptors
            oti_loc = stsd_box.find(b"\x04\x80\x80\x80")
            if oti_loc > 0:
                oti = stsd_box[oti_loc + 5 : oti_loc + 6].hex()
                codec += f".{oti}"

            dsi_loc = stsd_box.find(b"\x05\x80\x80\x80")
            if dsi_loc > 0:
                dsi_length = int.from_bytes(
                    stsd_box[dsi_loc + 4 : dsi_loc + 5], byteorder="big"
                )
                dsi_data = stsd_box[dsi_loc + 5 : dsi_loc + 5 + dsi_length]
                dsi0 = int.from_bytes(dsi_data[0:1], byteorder="big")
                dsi = (dsi0 & 248) >> 3
                if dsi == 31 and len(dsi_data) >= 2:
                    dsi1 = int.from_bytes(dsi_data[1:2], byteorder="big")
                    dsi = 32 + ((dsi0 & 7) << 3) + ((dsi1 & 224) >> 5)
                codec += f".{dsi}"

        codecs.append(codec)

    return ",".join(codecs)


def _find_box(
    mp4_bytes: bytes, target_type: bytes, box_start: int = 0
) -> typing.Generator[int, None, None]:
    """Find location of first box (or sub_box if box_start provided) of given type."""
    if box_start == 0:
        index = 0
        box_end = len(mp4_bytes)
    else:
        box_end = box_start + int.from_bytes(
            mp4_bytes[box_start : box_start + 4], byteorder="big"
        )
        index = box_start + 8
    while 1:
        if index > box_end - 8:  # End of box, not found
            break
        box_header = mp4_bytes[index : index + 8]
        if box_header[4:8] == target_type:
            yield index
        index += int.from_bytes(box_header[0:4], byteorder="big")
