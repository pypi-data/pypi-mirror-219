"""
Core components of Smart Home - The Next Generation.

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
import contextlib
import dataclasses
import datetime as dt
import enum
import functools as ft
import hashlib
import http
import logging
import secrets
import typing
import urllib.parse

import aiohttp
import async_timeout
import voluptuous as vol
import yarl

from ..backports import strenum
from .config_validation import ConfigValidation as _cv
from .const import Const
from .entity import Entity
from .entity_description import EntityDescription
from .http_client import HttpClient
from .smart_home_controller_error import SmartHomeControllerError

if not typing.TYPE_CHECKING:

    class SmartHomeController:
        pass

    class BrowseMedia:
        pass


if typing.TYPE_CHECKING:
    from .smart_home_controller import SmartHomeController
    from .browse_media import BrowseMedia


_LOGGER: typing.Final = logging.getLogger(__name__)

# How long our auth signature on the content should be valid for
_CONTENT_AUTH_EXPIRY_TIME: typing.Final = 3600 * 24

_ATTR_APP_ID: typing.Final = "app_id"
_ATTR_APP_NAME: typing.Final = "app_name"
_ATTR_ENTITY_PICTURE_LOCAL: typing.Final = "entity_picture_local"
_ATTR_GROUP_MEMBERS: typing.Final = "group_members"
_ATTR_INPUT_SOURCE: typing.Final = "source"
_ATTR_INPUT_SOURCE_LIST: typing.Final = "source_list"
_ATTR_MEDIA_ANNOUNCE: typing.Final = "announce"
_ATTR_MEDIA_ALBUM_ARTIST: typing.Final = "media_album_artist"
_ATTR_MEDIA_ALBUM_NAME: typing.Final = "media_album_name"
_ATTR_MEDIA_ARTIST: typing.Final = "media_artist"
_ATTR_MEDIA_CHANNEL: typing.Final = "media_channel"
_ATTR_MEDIA_CONTENT_ID: typing.Final = "media_content_id"
_ATTR_MEDIA_CONTENT_TYPE: typing.Final = "media_content_type"
_ATTR_MEDIA_DURATION: typing.Final = "media_duration"
_ATTR_MEDIA_ENQUEUE: typing.Final = "enqueue"
_ATTR_MEDIA_EXTRA: typing.Final = "extra"
_ATTR_MEDIA_EPISODE: typing.Final = "media_episode"
_ATTR_MEDIA_PLAYLIST: typing.Final = "media_playlist"
_ATTR_MEDIA_POSITION: typing.Final = "media_position"
_ATTR_MEDIA_POSITION_UPDATED_AT: typing.Final = "media_position_updated_at"
_ATTR_MEDIA_REPEAT: typing.Final = "repeat"
_ATTR_MEDIA_SEASON: typing.Final = "media_season"
_ATTR_MEDIA_SEEK_POSITION: typing.Final = "seek_position"
_ATTR_MEDIA_SERIES_TITLE: typing.Final = "media_series_title"
_ATTR_MEDIA_SHUFFLE: typing.Final = "shuffle"
_ATTR_MEDIA_TITLE: typing.Final = "media_title"
_ATTR_MEDIA_TRACK: typing.Final = "media_track"
_ATTR_MEDIA_VOLUME_LEVEL: typing.Final = "volume_level"
_ATTR_MEDIA_VOLUME_MUTED: typing.Final = "is_volume_muted"
_ATTR_SOUND_MODE: typing.Final = "sound_mode"
_ATTR_SOUND_MODE_LIST: typing.Final = "sound_mode_list"


class _MediaClass(strenum.LowercaseStrEnum):
    ALBUM = enum.auto()
    APP = enum.auto()
    ARTIST = enum.auto()
    CHANNEL = enum.auto()
    COMPOSER = enum.auto()
    CONTRIBUTING_ARTIST = enum.auto()
    DIRECTORY = enum.auto()
    EPISODE = enum.auto()
    GAME = enum.auto()
    GENRE = enum.auto()
    IMAGE = enum.auto()
    MOVIE = enum.auto()
    MUSIC = enum.auto()
    PLAYLIST = enum.auto()
    PODCAST = enum.auto()
    SEASON = enum.auto()
    TRACK = enum.auto()
    TV_SHOW = enum.auto()
    URL = enum.auto()
    VIDEO = enum.auto()


class _MediaType(strenum.LowercaseStrEnum):
    ALBUM = enum.auto()
    APP = enum.auto()
    APPS = enum.auto()
    ARTIST = enum.auto()
    CHANNEL = enum.auto()
    CHANNELS = enum.auto()
    COMPOSER = enum.auto()
    CONTRIBUTITING_ARTIST = enum.auto()
    EPISODE = enum.auto()
    GAME = enum.auto()
    GENRE = enum.auto()
    IMAGE = enum.auto()
    MOVIE = enum.auto()
    MUSIC = enum.auto()
    PLAYLIST = enum.auto()
    PODCAST = enum.auto()
    SEASON = enum.auto()
    TRACK = enum.auto()
    TVSHOW = enum.auto()
    URL = enum.auto()
    VIDEO = enum.auto()


class _Enqueue(strenum.LowercaseStrEnum):
    """Enqueue types for playing media."""

    # add given media item to end of the queue
    ADD = enum.auto()
    # play the given media item next, keep queue
    NEXT = enum.auto()
    # play the given media item now, keep queue
    PLAY = enum.auto()
    # play the given media item now, clear queue
    REPLACE = enum.auto()


class _Exception(SmartHomeControllerError):
    """Base class for Media Player exceptions."""


# pylint: disable=unused-variable
class _BrowseError(_Exception):
    """Error while browsing."""


_SERVICE_CLEAR_PLAYLIST: typing.Final = "clear_playlist"
_SERVICE_JOIN: typing.Final = "join"
_SERVICE_PLAY_MEDIA: typing.Final = "play_media"
_SERVICE_SELECT_SOUND_MODE: typing.Final = "select_sound_mode"
_SERVICE_SELECT_SOURCE: typing.Final = "select_source"
_SERVICE_UNJOIN: typing.Final = "unjoin"

_REPEAT_MODE_ALL: typing.Final = "all"
_REPEAT_MODE_OFF: typing.Final = "off"
_REPEAT_MODE_ONE: typing.Final = "one"
_REPEAT_MODES: typing.Final = [_REPEAT_MODE_OFF, _REPEAT_MODE_ALL, _REPEAT_MODE_ONE]

_PLAY_MEDIA_SCHEMA: typing.Final = {
    vol.Required(_ATTR_MEDIA_CONTENT_TYPE): _cv.string,
    vol.Required(_ATTR_MEDIA_CONTENT_ID): _cv.string,
    vol.Exclusive(_ATTR_MEDIA_ENQUEUE, "enqueue_announce"): vol.Any(
        _cv.boolean, vol.Coerce(_Enqueue)
    ),
    vol.Exclusive(_ATTR_MEDIA_ANNOUNCE, "enqueue_announce"): _cv.boolean,
    vol.Optional(_ATTR_MEDIA_EXTRA, default={}): dict,
}

_ATTR_TO_PROPERTY = [
    _ATTR_MEDIA_VOLUME_LEVEL,
    _ATTR_MEDIA_VOLUME_MUTED,
    _ATTR_MEDIA_CONTENT_ID,
    _ATTR_MEDIA_CONTENT_TYPE,
    _ATTR_MEDIA_DURATION,
    _ATTR_MEDIA_POSITION,
    _ATTR_MEDIA_POSITION_UPDATED_AT,
    _ATTR_MEDIA_TITLE,
    _ATTR_MEDIA_ARTIST,
    _ATTR_MEDIA_ALBUM_NAME,
    _ATTR_MEDIA_ALBUM_ARTIST,
    _ATTR_MEDIA_TRACK,
    _ATTR_MEDIA_SERIES_TITLE,
    _ATTR_MEDIA_SEASON,
    _ATTR_MEDIA_EPISODE,
    _ATTR_MEDIA_CHANNEL,
    _ATTR_MEDIA_PLAYLIST,
    _ATTR_APP_ID,
    _ATTR_APP_NAME,
    _ATTR_INPUT_SOURCE,
    _ATTR_SOUND_MODE,
    _ATTR_MEDIA_SHUFFLE,
    _ATTR_MEDIA_REPEAT,
]


class _EntityFeature(enum.IntEnum):
    """Supported features of the media player entity."""

    PAUSE = 1
    SEEK = 2
    VOLUME_SET = 4
    VOLUME_MUTE = 8
    PREVIOUS_TRACK = 16
    NEXT_TRACK = 32

    TURN_ON = 128
    TURN_OFF = 256
    PLAY_MEDIA = 512
    VOLUME_STEP = 1024
    SELECT_SOURCE = 2048
    STOP = 4096
    CLEAR_PLAYLIST = 8192
    PLAY = 16384
    SHUFFLE_SET = 32768
    SELECT_SOUND_MODE = 65536
    BROWSE_MEDIA = 131072
    REPEAT_SET = 262144
    GROUPING = 524288


_CACHE_IMAGES: typing.Final = "images"
_CACHE_MAXSIZE: typing.Final = "maxsize"
_CACHE_LOCK: typing.Final = "lock"
_CACHE_URL: typing.Final = "url"
_CACHE_CONTENT: typing.Final = "content"
_ENTITY_IMAGE_CACHE: typing.Final = {
    _CACHE_IMAGES: typing.OrderedDict(),
    _CACHE_MAXSIZE: 16,
}

_SCAN_INTERVAL: typing.Final = dt.timedelta(seconds=10)


class _DeviceClass(strenum.LowercaseStrEnum):
    """Device class for media players."""

    TV = enum.auto()
    SPEAKER = enum.auto()
    RECEIVER = enum.auto()


_DEVICE_CLASSES_SCHEMA = vol.All(vol.Lower, vol.Coerce(_DeviceClass))


@dataclasses.dataclass
class _EntityDescription(EntityDescription):
    """A class that describes media player entities."""

    device_class: _DeviceClass | str = None


class _Entity(Entity):
    """ABC for media player entities."""

    _entity_description: _EntityDescription
    _access_token: str = None

    _attr_app_id: str = None
    _attr_app_name: str = None
    _attr_device_class: _DeviceClass | str
    _attr_group_members: list[str] = None
    _attr_is_volume_muted: bool = None
    _attr_media_album_artist: str = None
    _attr_media_album_name: str = None
    _attr_media_artist: str = None
    _attr_media_channel: str = None
    _attr_media_content_id: str = None
    _attr_media_content_type: str = None
    _attr_media_duration: int = None
    _attr_media_episode: str = None
    _attr_media_image_hash: str
    _attr_media_image_remotely_accessible: bool = False
    _attr_media_image_url: str = None
    _attr_media_playlist: str = None
    _attr_media_position_updated_at: dt.datetime = None
    _attr_media_position: int = None
    _attr_media_season: str = None
    _attr_media_series_title: str = None
    _attr_media_title: str = None
    _attr_media_track: int = None
    _attr_repeat: str = None
    _attr_shuffle: bool = None
    _attr_sound_mode_list: list[str] = None
    _attr_sound_mode: str = None
    _attr_source_list: list[str] = None
    _attr_source: str = None
    _attr_state: str = None
    _attr_supported_features: int = 0
    _attr_volume_level: float = None

    # Implement these for your media player
    @property
    def device_class(self) -> str:
        """Return the class of this entity."""
        if hasattr(self, "_attr_device_class"):
            return str(self._attr_device_class)
        if hasattr(self, "_entity_description"):
            return str(self.entity_description.device_class)
        return None

    @property
    def entity_description(self) -> _EntityDescription:
        return super().entity_description

    @property
    def state(self) -> str:
        """State of the player."""
        return self._attr_state

    @property
    def access_token(self) -> str:
        """Access token for this media player."""
        if self._access_token is None:
            self._access_token = secrets.token_hex(32)
        return self._access_token

    @property
    def volume_level(self) -> float:
        """Volume level of the media player (0..1)."""
        return self._attr_volume_level

    @property
    def is_volume_muted(self) -> bool:
        """Boolean if volume is currently muted."""
        return self._attr_is_volume_muted

    @property
    def media_content_id(self) -> str:
        """Content ID of current playing media."""
        return self._attr_media_content_id

    @property
    def media_content_type(self) -> str:
        """Content type of current playing media."""
        return self._attr_media_content_type

    @property
    def media_duration(self) -> int:
        """Duration of current playing media in seconds."""
        return self._attr_media_duration

    @property
    def media_position(self) -> int:
        """Position of current playing media in seconds."""
        return self._attr_media_position

    @property
    def media_position_updated_at(self) -> dt.datetime:
        """When was the position of the current playing media valid.

        Returns value from homeassistant.util.dt.utcnow().
        """
        return self._attr_media_position_updated_at

    @property
    def media_image_url(self) -> str:
        """Image url of current playing media."""
        return self._attr_media_image_url

    @property
    def media_image_remotely_accessible(self) -> bool:
        """If the image url is remotely accessible."""
        return self._attr_media_image_remotely_accessible

    @property
    def media_image_hash(self) -> str:
        """Hash value for media image."""
        if hasattr(self, "_attr_media_image_hash"):
            return self._attr_media_image_hash

        if (url := self.media_image_url) is not None:
            return hashlib.sha256(url.encode("utf-8")).hexdigest()[:16]

        return None

    async def async_get_media_image(self) -> tuple[bytes, str]:
        """Fetch media image of current playing image."""
        if (url := self.media_image_url) is None:
            return None, None

        return await self._async_fetch_image_from_cache(url)

    # pylint: disable=unused-argument
    async def async_get_browse_image(
        self,
        media_content_type: str,
        media_content_id: str,
        media_image_id: str = None,
    ) -> tuple[bytes, str]:
        """
        Optionally fetch internally accessible image for media browser.

        Must be implemented by integration.
        """
        return None, None

    @property
    def media_title(self) -> str:
        """Title of current playing media."""
        return self._attr_media_title

    @property
    def media_artist(self) -> str:
        """Artist of current playing media, music track only."""
        return self._attr_media_artist

    @property
    def media_album_name(self) -> str:
        """Album name of current playing media, music track only."""
        return self._attr_media_album_name

    @property
    def media_album_artist(self) -> str:
        """Album artist of current playing media, music track only."""
        return self._attr_media_album_artist

    @property
    def media_track(self) -> int:
        """Track number of current playing media, music track only."""
        return self._attr_media_track

    @property
    def media_series_title(self) -> str:
        """Title of series of current playing media, TV show only."""
        return self._attr_media_series_title

    @property
    def media_season(self) -> str:
        """Season of current playing media, TV show only."""
        return self._attr_media_season

    @property
    def media_episode(self) -> str:
        """Episode of current playing media, TV show only."""
        return self._attr_media_episode

    @property
    def media_channel(self) -> str:
        """Channel currently playing."""
        return self._attr_media_channel

    @property
    def media_playlist(self) -> str:
        """Title of Playlist currently playing."""
        return self._attr_media_playlist

    @property
    def app_id(self) -> str:
        """ID of the current running app."""
        return self._attr_app_id

    @property
    def app_name(self) -> str:
        """Name of the current running app."""
        return self._attr_app_name

    @property
    def source(self) -> str:
        """Name of the current input source."""
        return self._attr_source

    @property
    def source_list(self) -> list[str]:
        """List of available input sources."""
        return self._attr_source_list

    @property
    def sound_mode(self) -> str:
        """Name of the current sound mode."""
        return self._attr_sound_mode

    @property
    def sound_mode_list(self) -> list[str]:
        """List of available sound modes."""
        return self._attr_sound_mode_list

    @property
    def shuffle(self) -> bool:
        """Boolean if shuffle is enabled."""
        return self._attr_shuffle

    @property
    def repeat(self) -> str:
        """Return current repeat mode."""
        return self._attr_repeat

    @property
    def group_members(self) -> list[str]:
        """List of members which are currently grouped together."""
        return self._attr_group_members

    @property
    def supported_features(self) -> int:
        """Flag media player features that are supported."""
        return self._attr_supported_features

    def turn_on(self) -> None:
        """Turn the media player on."""
        raise NotImplementedError()

    async def async_turn_on(self) -> None:
        """Turn the media player on."""
        await self._shc.async_add_executor_job(self.turn_on)

    def turn_off(self) -> None:
        """Turn the media player off."""
        raise NotImplementedError()

    async def async_turn_off(self) -> None:
        """Turn the media player off."""
        await self._shc.async_add_executor_job(self.turn_off)

    def mute_volume(self, mute: bool) -> None:
        """Mute the volume."""
        raise NotImplementedError()

    async def async_mute_volume(self, mute: bool) -> None:
        """Mute the volume."""
        await self._shc.async_add_executor_job(self.mute_volume, mute)

    def set_volume_level(self, volume: float) -> None:
        """Set volume level, range 0..1."""
        raise NotImplementedError()

    async def async_set_volume_level(self, volume: float) -> None:
        """Set volume level, range 0..1."""
        await self._shc.async_add_executor_job(self.set_volume_level, volume)

    def media_play(self) -> None:
        """Send play command."""
        raise NotImplementedError()

    async def async_media_play(self) -> None:
        """Send play command."""
        await self._shc.async_add_executor_job(self.media_play)

    def media_pause(self) -> None:
        """Send pause command."""
        raise NotImplementedError()

    async def async_media_pause(self) -> None:
        """Send pause command."""
        await self._shc.async_add_executor_job(self.media_pause)

    def media_stop(self) -> None:
        """Send stop command."""
        raise NotImplementedError()

    async def async_media_stop(self) -> None:
        """Send stop command."""
        await self._shc.async_add_executor_job(self.media_stop)

    def media_previous_track(self) -> None:
        """Send previous track command."""
        raise NotImplementedError()

    async def async_media_previous_track(self) -> None:
        """Send previous track command."""
        await self._shc.async_add_executor_job(self.media_previous_track)

    def media_next_track(self) -> None:
        """Send next track command."""
        raise NotImplementedError()

    async def async_media_next_track(self) -> None:
        """Send next track command."""
        await self._shc.async_add_executor_job(self.media_next_track)

    def media_seek(self, position: float) -> None:
        """Send seek command."""
        raise NotImplementedError()

    async def async_media_seek(self, position: float) -> None:
        """Send seek command."""
        await self._shc.async_add_executor_job(self.media_seek, position)

    def play_media(self, media_type: str, media_id: str, **kwargs: typing.Any) -> None:
        """Play a piece of media."""
        raise NotImplementedError()

    async def async_play_media(
        self, media_type: str, media_id: str, **kwargs: typing.Any
    ) -> None:
        """Play a piece of media."""
        await self._shc.async_add_executor_job(
            ft.partial(self.play_media, media_type, media_id, **kwargs)
        )

    def select_source(self, source: str) -> None:
        """Select input source."""
        raise NotImplementedError()

    async def async_select_source(self, source: str) -> None:
        """Select input source."""
        await self._shc.async_add_executor_job(self.select_source, source)

    def select_sound_mode(self, sound_mode: str) -> None:
        """Select sound mode."""
        raise NotImplementedError()

    async def async_select_sound_mode(self, sound_mode: str) -> None:
        """Select sound mode."""
        await self._shc.async_add_executor_job(self.select_sound_mode, sound_mode)

    def clear_playlist(self) -> None:
        """Clear players playlist."""
        raise NotImplementedError()

    async def async_clear_playlist(self) -> None:
        """Clear players playlist."""
        await self._shc.async_add_executor_job(self.clear_playlist)

    def set_shuffle(self, shuffle: bool) -> None:
        """Enable/disable shuffle mode."""
        raise NotImplementedError()

    async def async_set_shuffle(self, shuffle: bool) -> None:
        """Enable/disable shuffle mode."""
        await self._shc.async_add_executor_job(self.set_shuffle, shuffle)

    def set_repeat(self, repeat: str) -> None:
        """Set repeat mode."""
        raise NotImplementedError()

    async def async_set_repeat(self, repeat: str) -> None:
        """Set repeat mode."""
        await self._shc.async_add_executor_job(self.set_repeat, repeat)

    # No need to overwrite these.
    @typing.final
    @property
    def support_play(self) -> bool:
        """Boolean if play is supported."""
        return bool(self.supported_features & _EntityFeature.PLAY)

    @typing.final
    @property
    def support_pause(self) -> bool:
        """Boolean if pause is supported."""
        return bool(self.supported_features & _EntityFeature.PAUSE)

    @typing.final
    @property
    def support_stop(self) -> bool:
        """Boolean if stop is supported."""
        return bool(self.supported_features & _EntityFeature.STOP)

    @typing.final
    @property
    def support_seek(self) -> bool:
        """Boolean if seek is supported."""
        return bool(self.supported_features & _EntityFeature.SEEK)

    @typing.final
    @property
    def support_volume_set(self) -> bool:
        """Boolean if setting volume is supported."""
        return bool(self.supported_features & _EntityFeature.VOLUME_SET)

    @typing.final
    @property
    def support_volume_mute(self) -> bool:
        """Boolean if muting volume is supported."""
        return bool(self.supported_features & _EntityFeature.VOLUME_MUTE)

    @typing.final
    @property
    def support_previous_track(self) -> bool:
        """Boolean if previous track command supported."""
        return bool(self.supported_features & _EntityFeature.PREVIOUS_TRACK)

    @typing.final
    @property
    def support_next_track(self) -> bool:
        """Boolean if next track command supported."""
        return bool(self.supported_features & _EntityFeature.NEXT_TRACK)

    @typing.final
    @property
    def support_play_media(self) -> bool:
        """Boolean if play media command supported."""
        return bool(self.supported_features & _EntityFeature.PLAY_MEDIA)

    @typing.final
    @property
    def support_select_source(self) -> bool:
        """Boolean if select source command supported."""
        return bool(self.supported_features & _EntityFeature.SELECT_SOURCE)

    @typing.final
    @property
    def support_select_sound_mode(self) -> bool:
        """Boolean if select sound mode command supported."""
        return bool(self.supported_features & _EntityFeature.SELECT_SOUND_MODE)

    @typing.final
    @property
    def support_clear_playlist(self) -> bool:
        """Boolean if clear playlist command supported."""
        return bool(self.supported_features & _EntityFeature.CLEAR_PLAYLIST)

    @typing.final
    @property
    def support_shuffle_set(self) -> bool:
        """Boolean if shuffle is supported."""
        return bool(self.supported_features & _EntityFeature.SHUFFLE_SET)

    @typing.final
    @property
    def support_grouping(self) -> bool:
        """Boolean if player grouping is supported."""
        return bool(self.supported_features & _EntityFeature.GROUPING)

    async def async_toggle(self) -> None:
        """Toggle the power on the media player."""
        if hasattr(self, "toggle"):
            await self._shc.async_add_executor_job(self.toggle)
            return

        if self.state in (Const.STATE_OFF, Const.STATE_IDLE, Const.STATE_STANDBY):
            await self.async_turn_on()
        else:
            await self.async_turn_off()

    async def async_volume_up(self) -> None:
        """Turn volume up for media player.

        This method is a coroutine.
        """
        if hasattr(self, "volume_up"):
            await self._shc.async_add_executor_job(self.volume_up)
            return

        if (
            self.volume_level is not None
            and self.volume_level < 1
            and self.supported_features & _EntityFeature.VOLUME_SET
        ):
            await self.async_set_volume_level(min(1, self.volume_level + 0.1))

    async def async_volume_down(self) -> None:
        """Turn volume down for media player.

        This method is a coroutine.
        """
        if hasattr(self, "volume_down"):
            await self._shc.async_add_executor_job(self.volume_down)
            return

        if (
            self.volume_level is not None
            and self.volume_level > 0
            and self.supported_features & _EntityFeature.VOLUME_SET
        ):
            await self.async_set_volume_level(max(0, self.volume_level - 0.1))

    async def async_media_play_pause(self) -> None:
        """Play or pause the media player."""
        if hasattr(self, "media_play_pause"):
            await self._shc.async_add_executor_job(self.media_play_pause)
            return

        if self.state == Const.STATE_PLAYING:
            await self.async_media_pause()
        else:
            await self.async_media_play()

    @property
    def entity_picture(self) -> str:
        """Return image of the media playing."""
        if self.state == Const.STATE_OFF:
            return None

        if self.media_image_remotely_accessible:
            return self.media_image_url

        return self.media_image_local

    @property
    def media_image_local(self) -> str:
        """Return local url to media image."""
        if (image_hash := self.media_image_hash) is None:
            return None

        return (
            f"/api/media_player_proxy/{self.entity_id}?"
            f"token={self.access_token}&cache={image_hash}"
        )

    @property
    def capability_attributes(self) -> dict[str, typing.Any]:
        """Return capability attributes."""
        supported_features = self.supported_features or 0
        data: dict[str, typing.Any] = {}

        if supported_features & _EntityFeature.SELECT_SOURCE and (
            source_list := self.source_list
        ):
            data[_ATTR_INPUT_SOURCE_LIST] = source_list

        if supported_features & _EntityFeature.SELECT_SOUND_MODE and (
            sound_mode_list := self.sound_mode_list
        ):
            data[_ATTR_SOUND_MODE_LIST] = sound_mode_list

        return data

    @typing.final
    @property
    def state_attributes(self) -> dict[str, typing.Any]:
        """Return the state attributes."""
        state_attr: dict[str, typing.Any] = {}

        if self.support_grouping:
            state_attr[_ATTR_GROUP_MEMBERS] = self.group_members

        if self.state == Const.STATE_OFF:
            return state_attr

        for attr in _ATTR_TO_PROPERTY:
            if (value := getattr(self, attr)) is not None:
                state_attr[attr] = value

        if self.media_image_remotely_accessible:
            state_attr[_ATTR_ENTITY_PICTURE_LOCAL] = self.media_image_local

        return state_attr

    async def async_browse_media(
        self,
        media_content_type: str = None,
        media_content_id: str = None,
    ) -> BrowseMedia:
        """Return a BrowseMedia instance.

        The BrowseMedia instance will be used by the
        "media_player/browse_media" websocket command.
        """
        raise NotImplementedError()

    def join_players(self, group_members: list[str]) -> None:
        """Join `group_members` as a player group with the current player."""
        raise NotImplementedError()

    async def async_join_players(self, group_members: list[str]) -> None:
        """Join `group_members` as a player group with the current player."""
        await self._shc.async_add_executor_job(self.join_players, group_members)

    def unjoin_player(self) -> None:
        """Remove this player from any group."""
        raise NotImplementedError()

    async def async_unjoin_player(self) -> None:
        """Remove this player from any group."""
        await self._shc.async_add_executor_job(self.unjoin_player)

    async def _async_fetch_image_from_cache(self, url: str) -> tuple[bytes, str]:
        """Fetch image.

        Images are cached in memory (the images are typically 10-100kB in size).
        """
        cache_images = typing.cast(
            typing.OrderedDict, _ENTITY_IMAGE_CACHE[_CACHE_IMAGES]
        )
        cache_maxsize = typing.cast(int, _ENTITY_IMAGE_CACHE[_CACHE_MAXSIZE])

        if urllib.parse.urlparse(url).hostname is None:
            url = f"{self._shc.get_url()}{url}"

        if url not in cache_images:
            cache_images[url] = {_CACHE_LOCK: asyncio.Lock()}

        async with cache_images[url][_CACHE_LOCK]:
            if _CACHE_CONTENT in cache_images[url]:
                return cache_images[url][_CACHE_CONTENT]

        (content, content_type) = await self._async_fetch_image(url)

        async with cache_images[url][_CACHE_LOCK]:
            cache_images[url][_CACHE_CONTENT] = content, content_type
            while len(cache_images) > cache_maxsize:
                cache_images.popitem(last=False)

        return content, content_type

    async def _async_fetch_image(self, url: str) -> tuple[bytes, str]:
        """Retrieve an image."""
        return await MediaPlayer.async_fetch_image(_LOGGER, self._shc, url)

    def get_browse_image_url(
        self,
        media_content_type: str,
        media_content_id: str,
        media_image_id: str = None,
    ) -> str:
        """Generate an url for a media browser image."""
        url_path = (
            f"/api/media_player_proxy/{self.entity_id}/browse_media"
            f"/{media_content_type}/{media_content_id}"
        )

        url_query = {"token": self.access_token}
        if media_image_id:
            url_query["media_image_id"] = media_image_id

        return str(yarl.URL(url_path).with_query(url_query))


# pylint: disable=unused-variable, invalid-name
class MediaPlayer:
    """MediaPlayer namespace."""

    CONTENT_AUTH_EXPIRY_TIME: typing.Final = _CONTENT_AUTH_EXPIRY_TIME

    ATTR_APP_ID: typing.Final = _ATTR_APP_ID
    ATTR_APP_NAME: typing.Final = _ATTR_APP_NAME
    ATTR_ENTITY_PICTURE_LOCAL: typing.Final = _ATTR_ENTITY_PICTURE_LOCAL
    ATTR_GROUP_MEMBERS: typing.Final = _ATTR_GROUP_MEMBERS
    ATTR_INPUT_SOURCE: typing.Final = _ATTR_INPUT_SOURCE
    ATTR_INPUT_SOURCE_LIST: typing.Final = _ATTR_INPUT_SOURCE_LIST
    ATTR_MEDIA_ANNOUNCE: typing.Final = _ATTR_MEDIA_ANNOUNCE
    ATTR_MEDIA_ALBUM_ARTIST: typing.Final = _ATTR_MEDIA_ALBUM_ARTIST
    ATTR_MEDIA_ALBUM_NAME: typing.Final = _ATTR_MEDIA_ALBUM_NAME
    ATTR_MEDIA_ARTIST: typing.Final = _ATTR_MEDIA_ARTIST
    ATTR_MEDIA_CHANNEL: typing.Final = _ATTR_MEDIA_CHANNEL
    ATTR_MEDIA_CONTENT_ID: typing.Final = _ATTR_MEDIA_CONTENT_ID
    ATTR_MEDIA_CONTENT_TYPE: typing.Final = _ATTR_MEDIA_CONTENT_TYPE
    ATTR_MEDIA_DURATION: typing.Final = _ATTR_MEDIA_DURATION
    ATTR_MEDIA_ENQUEUE: typing.Final = _ATTR_MEDIA_ENQUEUE
    ATTR_MEDIA_EXTRA: typing.Final = _ATTR_MEDIA_EXTRA
    ATTR_MEDIA_EPISODE: typing.Final = _ATTR_MEDIA_EPISODE
    ATTR_MEDIA_PLAYLIST: typing.Final = _ATTR_MEDIA_PLAYLIST
    ATTR_MEDIA_POSITION: typing.Final = _ATTR_MEDIA_POSITION
    ATTR_MEDIA_POSITION_UPDATED_AT: typing.Final = _ATTR_MEDIA_POSITION_UPDATED_AT
    ATTR_MEDIA_REPEAT: typing.Final = _ATTR_MEDIA_REPEAT
    ATTR_MEDIA_SEASON: typing.Final = _ATTR_MEDIA_SEASON
    ATTR_MEDIA_SEEK_POSITION: typing.Final = _ATTR_MEDIA_SEEK_POSITION
    ATTR_MEDIA_SERIES_TITLE: typing.Final = _ATTR_MEDIA_SERIES_TITLE
    ATTR_MEDIA_SHUFFLE: typing.Final = _ATTR_MEDIA_SHUFFLE
    ATTR_MEDIA_TITLE: typing.Final = _ATTR_MEDIA_TITLE
    ATTR_MEDIA_TRACK: typing.Final = _ATTR_MEDIA_TRACK
    ATTR_MEDIA_VOLUME_LEVEL: typing.Final = _ATTR_MEDIA_VOLUME_LEVEL
    ATTR_MEDIA_VOLUME_MUTED: typing.Final = _ATTR_MEDIA_VOLUME_MUTED
    ATTR_SOUND_MODE: typing.Final = _ATTR_SOUND_MODE
    ATTR_SOUND_MODE_LIST: typing.Final = _ATTR_SOUND_MODE_LIST

    SERVICE_CLEAR_PLAYLIST: typing.Final = _SERVICE_CLEAR_PLAYLIST
    SERVICE_JOIN: typing.Final = _SERVICE_JOIN
    SERVICE_PLAY_MEDIA: typing.Final = _SERVICE_PLAY_MEDIA
    SERVICE_SELECT_SOUND_MODE: typing.Final = _SERVICE_SELECT_SOUND_MODE
    SERVICE_SELECT_SOURCE: typing.Final = _SERVICE_SELECT_SOURCE
    SERVICE_UNJOIN: typing.Final = _SERVICE_UNJOIN

    REPEAT_MODE_ALL: typing.Final = _REPEAT_MODE_ALL
    REPEAT_MODE_OFF: typing.Final = _REPEAT_MODE_OFF
    REPEAT_MODE_ONE: typing.Final = _REPEAT_MODE_ONE
    REPEAT_MODES: typing.Final = _REPEAT_MODES

    PLAY_MEDIA_SCHEMA: typing.Final = _PLAY_MEDIA_SCHEMA

    CACHE_IMAGES: typing.Final = _CACHE_IMAGES
    CACHE_MAXSIZE: typing.Final = _CACHE_MAXSIZE
    CACHE_LOCK: typing.Final = _CACHE_LOCK
    CACHE_URL: typing.Final = _CACHE_URL
    CACHE_CONTENT: typing.Final = _CACHE_CONTENT

    ENTITY_IMAGE_CACHE = _ENTITY_IMAGE_CACHE
    SCAN_INTERVAL: typing.Final = _SCAN_INTERVAL
    DEVICE_CLASSES_SCHEMA: typing.Final = _DEVICE_CLASSES_SCHEMA

    BrowseError: typing.TypeAlias = _BrowseError
    Enqueue: typing.TypeAlias = _Enqueue
    DeviceClass: typing.TypeAlias = _DeviceClass
    Entity: typing.TypeAlias = _Entity
    EntityDescription: typing.TypeAlias = _EntityDescription
    EntityFeature: typing.TypeAlias = _EntityFeature
    Exception: typing.TypeAlias = _Exception

    MediaClass: typing.TypeAlias = _MediaClass
    MediaType: typing.TypeAlias = _MediaType

    @staticmethod
    async def async_fetch_image(
        logger: logging.Logger, shc: SmartHomeController, url: str
    ) -> tuple[bytes, str]:
        """Retrieve an image."""
        content, content_type = (None, None)
        websession = HttpClient.async_get_clientsession(shc)
        with contextlib.suppress(asyncio.TimeoutError), async_timeout.timeout(10):
            response = await websession.get(url)
            if response.status == http.HTTPStatus.OK:
                content = await response.read()
                if content_type := response.headers.get(aiohttp.hdrs.CONTENT_TYPE):
                    content_type = content_type.split(";")[0]

        if content is None:
            url_parts = yarl.URL(url)
            if url_parts.user is not None:
                url_parts = url_parts.with_user("xxxx")
            if url_parts.password is not None:
                url_parts = url_parts.with_password("xxxxxxxx")
            url = str(url_parts)
            logger.warning(f"Error retrieving proxied image from {url}")

        return content, content_type
