"""
Google Cast Integration for Smart Home - The Next Generation.

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

# pylint: disable=unused-variable

import asyncio
import configparser
import dataclasses
import logging
import typing
import urllib.parse as url_parse

import aiohttp

from ... import core
from .errors import PlaylistError, PlaylistSupported

_LOGGER: typing.Final = logging.getLogger(__name__)
_PLS_SECTION_PLAYLIST: typing.Final = "playlist"


@dataclasses.dataclass
class PlaylistItem:
    """Playlist item."""

    length: str
    title: str
    url: str


def _is_url(url):
    """Validate the URL can be parsed and at least has scheme + netloc."""
    result = url_parse.urlparse(url)
    return all([result.scheme, result.netloc])


async def _fetch_playlist(
    shc: core.SmartHomeController, url: str, supported_content_types: tuple
):
    """Fetch a playlist from the given url."""
    try:
        session = core.HttpClient.async_get_clientsession(shc, verify_ssl=False)
        async with session.get(url, timeout=5) as resp:
            charset = resp.charset or "utf-8"
            if resp.content_type in supported_content_types:
                raise PlaylistSupported
            try:
                playlist_data = (await resp.content.read(64 * 1024)).decode(charset)
            except ValueError as err:
                raise PlaylistError(f"Could not decode playlist {url}") from err
    except asyncio.TimeoutError as err:
        raise PlaylistError(f"Timeout while fetching playlist {url}") from err
    except aiohttp.client_exceptions.ClientError as err:
        raise PlaylistError(f"Error while fetching playlist {url}") from err

    return playlist_data


async def parse_m3u(shc: core.SmartHomeController, url: str):
    """Very simple m3u parser.

    Based on https://github.com/dvndrsn/M3uParser/blob/master/m3uparser.py
    """
    # From Mozilla gecko source:
    # https://github.com/mozilla/gecko-dev/blob/c4c1adbae87bf2d128c39832d72498550ee1b4b8/
    # dom/media/DecoderTraits.cpp#L47-L52
    hls_content_types = (
        # https://tools.ietf.org/html/draft-pantos-http-live-streaming-19#section-10
        "application/vnd.apple.mpegurl",
        # Additional informal types used by Mozilla gecko not included as they
        # don't reliably indicate HLS streams
    )
    m3u_data = await _fetch_playlist(shc, url, hls_content_types)
    m3u_lines = m3u_data.splitlines()

    playlist = []

    length = None
    title = None

    for line in m3u_lines:
        line = line.strip()
        if line.startswith("#EXTINF:"):
            # Get length and title from #EXTINF line
            info = line.split("#EXTINF:")[1].split(",", 1)
            if len(info) != 2:
                _LOGGER.warning(f"Ignoring invalid extinf {line} in playlist {url}")
                continue
            length = info[0].split(" ", 1)
            title = info[1].strip()
        elif line.startswith("#EXT-X-VERSION:"):
            # HLS stream, supported by cast devices
            raise PlaylistSupported("HLS")
        elif line.startswith("#EXT-X-STREAM-INF:"):
            # HLS stream, supported by cast devices
            raise PlaylistSupported("HLS")
        elif line.startswith("#"):
            # Ignore other extensions
            continue
        elif len(line) != 0:
            # Get song path from all other, non-blank lines
            if not _is_url(line):
                raise PlaylistError(f"Invalid item {line} in playlist {url}")
            playlist.append(PlaylistItem(length=length, title=title, url=line))
            # reset the song variables so it doesn't use the same EXTINF more than once
            length = None
            title = None

    return playlist


async def parse_pls(shc: core.SmartHomeController, url: str):
    """Very simple pls parser.

    Based on https://github.com/mariob/plsparser/blob/master/src/plsparser.py
    """
    pls_data = await _fetch_playlist(shc, url, ())

    pls_parser = configparser.ConfigParser()
    try:
        pls_parser.read_string(pls_data, url)
    except configparser.Error as err:
        raise PlaylistError(f"Can't parse playlist {url}") from err

    if (
        _PLS_SECTION_PLAYLIST not in pls_parser
        or pls_parser[_PLS_SECTION_PLAYLIST].getint("Version") != 2
    ):
        raise PlaylistError(f"Invalid playlist {url}")

    try:
        num_entries = pls_parser.getint(_PLS_SECTION_PLAYLIST, "NumberOfEntries")
    except (configparser.NoOptionError, ValueError) as err:
        raise PlaylistError(f"Invalid NumberOfEntries in playlist {url}") from err

    playlist_section = pls_parser[_PLS_SECTION_PLAYLIST]

    playlist = []
    for entry in range(1, num_entries + 1):
        file_option = f"File{entry}"
        if file_option not in playlist_section:
            _LOGGER.warning(f"Missing {file_option} in pls from {url}")
            continue
        item_url = playlist_section[file_option]
        if not _is_url(item_url):
            raise PlaylistError(f"Invalid item {item_url} in playlist {url}")
        playlist.append(
            PlaylistItem(
                length=playlist_section.get(f"Length{entry}"),
                title=playlist_section.get(f"Title{entry}"),
                url=item_url,
            )
        )
    return playlist


async def parse_playlist(shc: core.SmartHomeController, url: str):
    """Parse an m3u or pls playlist."""
    if url.endswith(".m3u") or url.endswith(".m3u8"):
        playlist = await parse_m3u(shc, url)
    else:
        playlist = await parse_pls(shc, url)

    if not playlist:
        raise PlaylistError(f"Empty playlist {url}")

    return playlist
