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

import collections.abc
import pathlib
import typing
import voluptuous as vol

from ... import core
from .local_media_view import LocalMediaView
from .local_source import LocalSource
from .media_source_item import MediaSourceItem
from .upload_media_view import UploadMediaView


_MEDIA_SOURCES: typing.Final = dict[str, core.MediaSource]()
_UNDEFINED: typing.Final = object()

_BROWSE_MEDIA: typing.Final = {
    vol.Required("type"): "media_source/browse_media",
    vol.Optional(core.MediaPlayer.ATTR_MEDIA_CONTENT_ID, default=""): str,
}
_RESOLVE_MEDIA: typing.Final = {
    vol.Required("type"): "media_source/resolve_media",
    vol.Required(core.MediaPlayer.ATTR_MEDIA_CONTENT_ID): str,
    vol.Optional("expires", default=core.MediaPlayer.CONTENT_AUTH_EXPIRY_TIME): int,
}
_REMOVE_MEDIA: typing.Final = {
    vol.Required("type"): "media_source/local_source/remove",
    vol.Required("media_content_id"): str,
}


# pylint: disable=unused-variable
class MediaSourceComponent(core.MediaSourceComponent):
    """The media_source integration."""

    def __init__(self, path: typing.Iterable[str]):
        super().__init__(path)
        self._source: LocalSource = None

    async def async_setup(self, config: core.ConfigType) -> bool:
        """Set up the media_source component."""
        if not await super().async_setup(config):
            return False

        shc: core.SmartHomeController = self._shc

        websocket_api = self.controller.components.websocket_api
        if not isinstance(websocket_api, core.WebSocket.Component):
            return False

        frontend = self.controller.components.frontend
        if not isinstance(frontend, core.FrontendComponent):
            return False

        frontend.async_register_built_in_panel(
            "media-browser", "media_browser", "hass:play-box-multiple"
        )

        source = LocalSource(self._shc, self.domain)
        self._source = source
        _MEDIA_SOURCES[self.domain] = source
        shc.register_view(LocalMediaView(shc, source))
        shc.register_view(UploadMediaView(self, source))

        websocket_api.register_command(self._browse_media, _BROWSE_MEDIA)
        websocket_api.register_command(self._resolve_media, _RESOLVE_MEDIA)
        websocket_api.register_command(self._remove_media, _REMOVE_MEDIA)

        await shc.setup.async_process_integration_platforms(
            core.Platform.MEDIA_SOURCE, self._process_media_source_platform
        )
        return True

    async def _process_media_source_platform(
        self, domain: str, platform: core.PlatformImplementation
    ) -> None:
        """Process a media source platform."""
        if isinstance(platform, core.MediaSourcePlatform):
            _MEDIA_SOURCES[domain] = await platform.async_get_media_source()

    def items(self) -> collections.abc.Iterable[core.MediaSource]:
        return _MEDIA_SOURCES.values()

    def get_item(self, domain: str) -> core.MediaSource:
        return _MEDIA_SOURCES.get(domain, None)

    async def _remove_media(
        self,
        connection: core.WebSocket.Connection,
        msg: dict,
    ) -> None:
        """Remove media."""
        connection.require_admin()
        try:
            item = MediaSourceItem.from_uri(self, msg["media_content_id"], None)
        except ValueError as err:
            connection.send_error(
                msg["id"], core.WebSocket.ERR_INVALID_FORMAT, str(err)
            )
            return

        source = self._source

        try:
            source_dir_id, location = source.async_parse_identifier(item)
        except core.Unresolvable as err:
            connection.send_error(
                msg["id"], core.WebSocket.ERR_INVALID_FORMAT, str(err)
            )
            return

        item_path = source.async_full_path(source_dir_id, location)

        try:
            error = await connection.owner.controller.async_add_executor_job(
                self._do_delete, item_path
            )
        except OSError as err:
            error = (core.WebSocket.ERR_UNKNOWN_ERROR, str(err))

        if error:
            connection.send_error(msg["id"], *error)
        else:
            connection.send_result(msg["id"])

    def _do_delete(self, item_path: pathlib.Path) -> tuple[str, str]:
        if not item_path.exists():
            return core.WebSocket.ERR_NOT_FOUND, "Path does not exist"

        if not item_path.is_file():
            return core.WebSocket.ERR_NOT_SUPPORTED, "Path is not a file"

        item_path.unlink()
        return None

    async def _browse_media(
        self,
        connection: core.WebSocket.Connection,
        msg: dict,
    ) -> None:
        """Browse available media."""
        try:
            media = await self.async_browse_media(msg.get("media_content_id", ""))
            connection.send_result(
                msg["id"],
                media.as_dict(),
            )
        except core.MediaPlayer.BrowseError as err:
            connection.send_error(msg["id"], "browse_media_failed", str(err))

    async def _resolve_media(
        self,
        connection: core.WebSocket.Connection,
        msg: dict,
    ) -> None:
        """Resolve media."""
        try:
            media = await self.async_resolve_media(msg["media_content_id"])
        except core.Unresolvable as err:
            connection.send_error(msg["id"], "resolve_media_failed", str(err))
            return

        comp = self.controller.components.media_player
        if isinstance(comp, core.MediaPlayerComponent):
            connection.send_result(
                msg["id"],
                {
                    "url": comp.async_process_play_media_url(
                        media.url, allow_relative_url=True
                    ),
                    "mime_type": media.mime_type,
                },
            )
        else:
            connection.send_error(
                msg["id"], "resolve_media_failed", "Media Player Component not loaded."
            )

    def is_media_source_id(self, media_content_id: str) -> bool:
        """Test if identifier is a media source."""
        return (
            core.Const.MEDIA_SOURCE_URI_SCHEME_REGEX.match(media_content_id) is not None
        )

    def generate_media_source_id(self, domain: str, identifier: str) -> str:
        """Generate a media source ID."""
        uri = f"{core.Const.MEDIA_SOURCE_URI_SCHEME}{domain or ''}"
        if identifier:
            uri += f"/{identifier}"
        return uri

    async def async_browse_media(
        self,
        media_content_id: str,
        *,
        content_filter: collections.abc.Callable[[core.BrowseMedia], bool] = None,
    ) -> core.BrowseMediaSource:
        """Return media player browse media results."""
        if self.domain not in _MEDIA_SOURCES:
            raise core.MediaPlayer.BrowseError("Media Source not loaded")

        try:
            item = await self._get_media_item(media_content_id, None).async_browse()
        except ValueError as err:
            raise core.MediaPlayer.BrowseError(str(err)) from err

        if content_filter is None or item.children is None:
            return item

        # pylint: disable=protected-access
        old_count = len(item._children)
        item._children = [
            child
            for child in item.children
            if child.can_expand or content_filter(child)
        ]
        item.not_shown += old_count - len(item._children)
        return item

    def _get_media_item(
        self, media_content_id: str, target_media_player: str
    ) -> MediaSourceItem:
        """Return media item."""
        if media_content_id:
            item = MediaSourceItem.from_uri(self, media_content_id, target_media_player)
        else:
            # We default to our own domain if its only one registered
            domain = None if len(_MEDIA_SOURCES) > 1 else self.domain
            return MediaSourceItem(self, domain, "", target_media_player)

        if item.domain is not None and item.domain not in _MEDIA_SOURCES:
            raise ValueError("Unknown media source")

        return item

    async def async_resolve_media(
        self,
        media_content_id: str,
        target_media_player: str | object = _UNDEFINED,
    ) -> core.PlayMedia:
        """Get info to play media."""
        if self.domain not in _MEDIA_SOURCES:
            raise core.Unresolvable("Media Source not loaded")

        if target_media_player is _UNDEFINED:
            target_media_player = None

        try:
            item = self._get_media_item(media_content_id, target_media_player)
        except ValueError as err:
            raise core.Unresolvable(str(err)) from err

        return await item.async_resolve()
