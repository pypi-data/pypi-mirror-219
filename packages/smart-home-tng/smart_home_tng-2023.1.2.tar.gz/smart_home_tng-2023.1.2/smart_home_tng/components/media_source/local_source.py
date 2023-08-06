"""
Media Source Component for Smart Home - The Next Generation.

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

import mimetypes
import pathlib

from ... import core
from .const import Const
from .media_source_item import MediaSourceItem


# pylint: disable=unused-variable
class LocalSource(core.MediaSource):
    """Provide local directories as media sources."""

    _name: str = "Local Media"

    def __init__(self, shc: core.SmartHomeController, domain: str) -> None:
        """Initialize local source."""
        super().__init__(domain)
        self._shc = shc

    @core.callback
    def async_full_path(self, source_dir_id: str, location: str) -> pathlib.Path:
        """Return full path."""
        return pathlib.Path(self._shc.config.media_dirs[source_dir_id], location)

    @core.callback
    def async_parse_identifier(self, item: MediaSourceItem) -> tuple[str, str]:
        """Parse identifier."""
        if item.domain != self._domain:
            raise core.Unresolvable("Unknown domain.")

        source_dir_id, _, location = item.identifier.partition("/")
        if source_dir_id not in self._shc.config.media_dirs:
            raise core.Unresolvable("Unknown source directory.")

        try:
            core.helpers.raise_if_invalid_path(location)
        except ValueError as err:
            raise core.Unresolvable("Invalid path.") from err

        return source_dir_id, location

    async def async_resolve_media(self, item: MediaSourceItem) -> core.PlayMedia:
        """Resolve media to a url."""
        source_dir_id, location = self.async_parse_identifier(item)
        path = self.async_full_path(source_dir_id, location)
        mime_type, _ = mimetypes.guess_type(str(path))
        assert isinstance(mime_type, str)
        return core.PlayMedia(f"/media/{item.identifier}", mime_type)

    async def async_browse_media(self, item: MediaSourceItem) -> core.BrowseMediaSource:
        """Return media."""
        if item.identifier:
            try:
                source_dir_id, location = self.async_parse_identifier(item)
            except core.Unresolvable as err:
                raise core.MediaPlayer.BrowseError(str(err)) from err

        else:
            source_dir_id, location = None, ""

        result = await self._shc.async_add_executor_job(
            self._browse_media, source_dir_id, location
        )

        return result

    def _browse_media(
        self, source_dir_id: str, location: str
    ) -> core.BrowseMediaSource:
        """Browse media."""

        # If only one media dir is configured, use that as the local media root
        if source_dir_id is None and len(self._shc.config.media_dirs) == 1:
            source_dir_id = list(self._shc.config.media_dirs)[0]

        # Multiple folder, root is requested
        if source_dir_id is None:
            if location:
                raise core.MediaPlayer.BrowseError("Folder not found.")

            base = core.BrowseMediaSource(
                domain=self._domain,
                identifier="",
                media_class=core.MediaPlayer.MediaClass.DIRECTORY,
                media_content_type=None,
                title=self.name,
                can_play=False,
                can_expand=True,
                children_media_class=core.MediaPlayer.MediaClass.DIRECTORY,
                children=[
                    self._browse_media(source_dir_id, "")
                    for source_dir_id in self._shc.config.media_dirs
                ],
            )

            return base

        full_path = pathlib.Path(self._shc.config.media_dirs[source_dir_id], location)

        if not full_path.exists():
            if location == "":
                raise core.MediaPlayer.BrowseError("Media directory does not exist.")
            raise core.MediaPlayer.BrowseError("Path does not exist.")

        if not full_path.is_dir():
            raise core.MediaPlayer.BrowseError("Path is not a directory.")

        result = self._build_item_response(source_dir_id, full_path)
        if not result:
            raise core.MediaPlayer.BrowseError("Unknown source directory.")
        return result

    def _build_item_response(
        self, source_dir_id: str, path: pathlib.Path, is_child: bool = False
    ) -> core.BrowseMediaSource:
        mime_type, _ = mimetypes.guess_type(str(path))
        is_file = path.is_file()
        is_dir = path.is_dir()

        # Make sure it's a file or directory
        if not is_file and not is_dir:
            return None

        # Check that it's a media file
        if is_file and (
            not mime_type or mime_type.split("/")[0] not in Const.MEDIA_MIME_TYPES
        ):
            return None

        title = path.name

        media_class = core.MediaPlayer.MediaClass.DIRECTORY
        if mime_type:
            media_class = Const.MEDIA_CLASS_MAP.get(
                mime_type.split("/")[0], core.MediaPlayer.MediaClass.DIRECTORY
            )

        media = core.BrowseMediaSource(
            domain=self._domain,
            identifier=(
                f"{source_dir_id}/"
                + f"{path.relative_to(self._shc.config.media_dirs[source_dir_id])}"
            ),
            media_class=media_class,
            media_content_type=mime_type or "",
            title=title,
            can_play=is_file,
            can_expand=is_dir,
        )

        if is_file or is_child:
            return media

        # Append first level children
        for child_path in path.iterdir():
            if child_path.name[0] != ".":
                child = self._build_item_response(source_dir_id, child_path, True)
                if child:
                    media.add_child(child)

        return media
