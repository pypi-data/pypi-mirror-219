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

import contextlib
import datetime as dt
import json
import logging
import typing

import pychromecast
import pychromecast.config
import pychromecast.const
import pychromecast.controllers.homeassistant
import pychromecast.controllers.media
import pychromecast.controllers.receiver
import pychromecast.quick_play
import pychromecast.socket_client
import yarl

from ... import core
from .cast_device import CastDevice
from .chromecast_info import ChromecastInfo
from .chromecast_zeroconf import ChromecastZeroconf
from .const import Const
from .discover import setup_internal_discovery
from .dynamic_cast_group import DynamicCastGroup
from .errors import PlaylistError, PlaylistSupported
from .playlist import parse_playlist


if not typing.TYPE_CHECKING:

    class GoogleCastIntegration:
        pass


if typing.TYPE_CHECKING:
    from .google_cast_integration import GoogleCastIntegration

_LOGGER: typing.Final = logging.getLogger(__name__)
_CAST_SPLASH: typing.Final = "https://www.home-assistant.io/images/cast/splash.png"
_APP_IDS_UNRELIABLE_MEDIA_INFO: typing.Final = ("Netflix",)


# pylint: disable=unused-variable
class CastMediaPlayerEntity(CastDevice, core.MediaPlayer.Entity):
    """Representation of a Cast device on the network."""

    _attr_has_entity_name = True
    _attr_should_poll = False
    _attr_media_image_remotely_accessible = True
    _mz_only = False

    def __init__(self, owner: GoogleCastIntegration, cast_info: ChromecastInfo) -> None:
        """Initialize the cast device."""

        CastDevice.__init__(self, owner, cast_info)

        self._cast_status = None
        self.__media_status = None
        self._media_status_received = None
        self._mz_media_status: dict[
            str, pychromecast.controllers.media.MediaStatus
        ] = {}
        self._mz_media_status_received: dict[str, dt.datetime] = {}
        self._attr_available = False
        self._cast_controller: pychromecast.controllers.homeassistant.HomeAssistantController = (
            None
        )

        self._cast_view_remove_handler: core.CallbackType = None
        self._attr_unique_id = str(cast_info.uuid)
        self._attr_device_info = core.DeviceInfo(
            identifiers={(self._owner.domain, str(cast_info.uuid).replace("-", ""))},
            manufacturer=str(cast_info.cast_info.manufacturer),
            model=cast_info.cast_info.model_name,
            name=str(cast_info.friendly_name),
        )

        if cast_info.cast_info.cast_type in [
            pychromecast.const.CAST_TYPE_AUDIO,
            pychromecast.const.CAST_TYPE_GROUP,
        ]:
            self._attr_device_class = core.MediaPlayer.DeviceClass.SPEAKER

    async def async_added_to_shc(self) -> None:
        """Create chromecast object when added to hass."""
        self._async_setup(self.entity_id)

        self._cast_view_remove_handler = self._shc.dispatcher.async_connect(
            Const.SIGNAL_CAST_SHOW_VIEW, self._handle_signal_show_view
        )

    async def async_will_remove_from_shc(self) -> None:
        """Disconnect Chromecast object when removed."""
        await self._async_tear_down()

        if self._cast_view_remove_handler:
            self._cast_view_remove_handler()
            self._cast_view_remove_handler = None

    async def _async_connect_to_chromecast(self):
        """Set up the chromecast object."""
        await super()._async_connect_to_chromecast()

        self._attr_available = False
        self._cast_status = self._chromecast.status
        self.__media_status = self._chromecast.media_controller.status
        self.async_write_state()

    async def _async_disconnect(self):
        """Disconnect Chromecast object if it is set."""
        await super()._async_disconnect()

        self._attr_available = False
        self.async_write_state()

    def _invalidate(self):
        """Invalidate some attributes."""
        super()._invalidate()

        self._cast_status = None
        self.__media_status = None
        self._media_status_received = None
        self._mz_media_status = {}
        self._mz_media_status_received = {}
        self._cast_controller = None

    # ========== Callbacks ==========
    def new_cast_status(self, cast_status):
        """Handle updates of the cast status."""
        self._cast_status = cast_status
        self._attr_volume_level = cast_status.volume_level if cast_status else None
        self._attr_is_volume_muted = cast_status.volume_muted if cast_status else None
        self.schedule_update_state()

    def new_media_status(self, media_status):
        """Handle updates of the media status."""
        if (
            media_status
            and media_status.player_is_idle
            and media_status.idle_reason == "ERROR"
        ):
            external_url = None
            internal_url = None
            tts_base_url = None
            url_description = ""
            if "tts" in self._owner.controller.config.components:
                # pylint: disable=[import-outside-toplevel]
                tts: core.TTS.Component = self._owner.controller.components.tts

                with contextlib.suppress(KeyError):  # base_url not configured
                    tts_base_url = tts.get_base_url()

            with contextlib.suppress(
                core.NoURLAvailableError
            ):  # external_url not configured
                external_url = self._owner.controller.get_url(allow_internal=False)

            with contextlib.suppress(
                core.NoURLAvailableError
            ):  # internal_url not configured
                internal_url = self._owner.controller.get_url(allow_external=False)

            if media_status.content_id:
                if tts_base_url and media_status.content_id.startswith(tts_base_url):
                    url_description = f" from tts.base_url ({tts_base_url})"
                if external_url and media_status.content_id.startswith(external_url):
                    url_description = f" from external_url ({external_url})"
                if internal_url and media_status.content_id.startswith(internal_url):
                    url_description = f" from internal_url ({internal_url})"

            _LOGGER.error(
                f"Failed to cast media {media_status.content_id}{url_description}. "
                + "Please make sure the URL is: "
                + "Reachable from the cast device and either a publicly resolvable "
                + "hostname or an IP address",
            )

        self.__media_status = media_status
        self._media_status_received = core.helpers.utcnow()
        self.schedule_update_state()

    def load_media_failed(self, item, error_code):
        """Handle load media failed."""
        error_msg = pychromecast.controllers.media.MEDIA_PLAYER_ERROR_CODES.get(
            error_code, "unknown code"
        )
        _LOGGER.debug(
            f"[{self.entity_id} {self._cast_info.friendly_name}] Load media failed "
            + f"with code {error_code}({error_msg}) for item {item}",
        )

    def new_connection_status(self, connection_status):
        """Handle updates of connection status."""
        _LOGGER.debug(
            f"[{self.entity_id} {self._cast_info.friendly_name}] "
            + f"Received cast device connection status: {connection_status.status}",
        )
        if (
            connection_status.status
            == pychromecast.socket_client.CONNECTION_STATUS_DISCONNECTED
        ):
            self._attr_available = False
            self._invalidate()
            self.schedule_update_state()
            return

        new_available = (
            connection_status.status
            == pychromecast.socket_client.CONNECTION_STATUS_CONNECTED
        )
        if new_available != self.available:
            # Connection status callbacks happen often when disconnected.
            # Only update state when availability changed to put less pressure
            # on state machine.
            _LOGGER.debug(
                f"[{self.entity_id} {self._cast_info.friendly_name}] "
                + f"Cast device availability changed: {connection_status.status}",
            )
            self._attr_available = new_available
            if new_available and not self._cast_info.is_audio_group:
                # Poll current group status
                for group_uuid in self._mz_mgr.get_multizone_memberships(
                    self._cast_info.uuid
                ):
                    group_media_controller = self._mz_mgr.get_multizone_mediacontroller(
                        group_uuid
                    )
                    if not group_media_controller:
                        continue
                    self.multizone_new_media_status(
                        group_uuid, group_media_controller.status
                    )
            self.schedule_update_state()

    def multizone_new_media_status(self, group_uuid, media_status):
        """Handle updates of audio group media status."""
        _LOGGER.debug(
            f"[{self.entity_id} {self._cast_info.friendly_name}] "
            + f"Multizone {group_uuid} media status: {media_status}",
        )
        self._mz_media_status[group_uuid] = media_status
        self._mz_media_status_received[group_uuid] = core.helpers.utcnow()
        self.schedule_update_state()

    # ========== Service Calls ==========
    def _media_controller(self):
        """
        Return media controller.

        First try from our own cast, then groups which our cast is a member in.
        """
        media_status = self.__media_status
        media_controller = self._chromecast.media_controller

        if (
            media_status is None
            or media_status.player_state
            == pychromecast.controllers.media.MEDIA_PLAYER_STATE_UNKNOWN
        ):
            groups = self._mz_media_status
            for k, val in groups.items():
                if (
                    val
                    and val.player_state
                    != pychromecast.controllers.media.MEDIA_PLAYER_STATE_UNKNOWN
                ):
                    media_controller = self._mz_mgr.get_multizone_mediacontroller(k)
                    break

        return media_controller

    def turn_on(self) -> None:
        """Turn on the cast device."""

        chromecast = self._get_chromecast()
        if not chromecast.is_idle:
            # Already turned on
            return

        if chromecast.app_id is not None:
            # Quit the previous app before starting splash screen or media player
            chromecast.quit_app()

        # The only way we can turn the Chromecast is on is by launching an app
        if chromecast.cast_type == pychromecast.const.CAST_TYPE_CHROMECAST:
            app_data = {"media_id": _CAST_SPLASH, "media_type": "image/png"}
            pychromecast.quick_play.quick_play(
                chromecast, "default_media_receiver", app_data
            )
        else:
            chromecast.start_app(pychromecast.config.APP_MEDIA_RECEIVER)

    def turn_off(self) -> None:
        """Turn off the cast device."""
        self._get_chromecast().quit_app()

    def mute_volume(self, mute: bool) -> None:
        """Mute the volume."""
        self._get_chromecast().set_volume_muted(mute)

    def set_volume_level(self, volume: float) -> None:
        """Set volume level, range 0..1."""
        self._get_chromecast().set_volume(volume)

    def media_play(self) -> None:
        """Send play command."""
        media_controller = self._media_controller()
        media_controller.play()

    def media_pause(self) -> None:
        """Send pause command."""
        media_controller = self._media_controller()
        media_controller.pause()

    def media_stop(self) -> None:
        """Send stop command."""
        media_controller = self._media_controller()
        media_controller.stop()

    def media_previous_track(self) -> None:
        """Send previous track command."""
        media_controller = self._media_controller()
        media_controller.queue_prev()

    def media_next_track(self) -> None:
        """Send next track command."""
        media_controller = self._media_controller()
        media_controller.queue_next()

    def media_seek(self, position: float) -> None:
        """Seek the media to a specific location."""
        media_controller = self._media_controller()
        media_controller.seek(position)

    async def _async_root_payload(self, content_filter):
        """Generate root node."""
        children = []
        # Add media browsers
        for platform in self._owner.cast_platforms.values():
            children.extend(
                await platform.async_get_media_browser_root_object(
                    self._chromecast.cast_type
                )
            )

        # Add media sources
        try:
            media_source: core.MediaSourceComponent = (
                self._owner.controller.components.media_source
            )
            result = await media_source.async_browse_media(
                None, content_filter=content_filter
            )
            children.extend(result.children)
        except core.MediaPlayer.BrowseError:
            if not children:
                raise

        # If there's only one media source, resolve it
        if len(children) == 1 and children[0].can_expand:
            return await self.async_browse_media(
                children[0].media_content_type,
                children[0].media_content_id,
            )

        return core.BrowseMedia(
            title="Cast",
            media_class=core.MediaPlayer.MediaClass.DIRECTORY,
            media_content_id="",
            media_content_type="",
            can_play=False,
            can_expand=True,
            children=sorted(children, key=lambda c: c.title),
        )

    async def async_browse_media(
        self, media_content_type: str = None, media_content_id: str = None
    ) -> core.BrowseMedia:
        """Implement the websocket media browsing helper."""
        content_filter = None

        chromecast = self._get_chromecast()
        if chromecast.cast_type in (
            pychromecast.const.CAST_TYPE_AUDIO,
            pychromecast.const.CAST_TYPE_GROUP,
        ):

            def audio_content_filter(item):
                """Filter non audio content."""
                return item.media_content_type.startswith("audio/")

            content_filter = audio_content_filter

        if media_content_id is None:
            return await self._async_root_payload(content_filter)

        for platform in self._owner.cast_platforms.values():
            browse_media = await platform.async_browse_media(
                media_content_type,
                media_content_id,
                chromecast.cast_type,
            )
            if browse_media:
                return browse_media

        media_source: core.MediaSourceComponent = (
            self._owner.controller.components.media_source
        )
        return await media_source.async_browse_media(
            media_content_id, content_filter=content_filter
        )

    async def async_play_media(
        self, media_type: str, media_id: str, **kwargs: typing.Any
    ) -> None:
        """Play a piece of media."""
        chromecast = self._get_chromecast()
        # Handle media_source
        media_source: core.MediaSourceComponent = (
            self._owner.controller.components.media_source
        )
        if media_source.is_media_source_id(media_id):
            sourced_media = await media_source.async_resolve_media(
                media_id, self.entity_id
            )
            media_type = sourced_media.mime_type
            media_id = sourced_media.url

        extra = kwargs.get(core.MediaPlayer.ATTR_MEDIA_EXTRA, {})

        # Handle media supported by a known cast app
        if media_type == self._owner.domain:
            try:
                app_data = json.loads(media_id)
                if metadata := extra.get("metadata"):
                    app_data["metadata"] = metadata
            except json.JSONDecodeError:
                _LOGGER.error("Invalid JSON in media_content_id")
                raise

            # Special handling for passed `app_id` parameter. This will only launch
            # an arbitrary cast app, generally for UX.
            if "app_id" in app_data:
                app_id = app_data.pop("app_id")
                _LOGGER.info(f"Starting Cast app by ID {app_id}")
                await self._owner.controller.async_add_executor_job(
                    chromecast.start_app, app_id
                )
                if app_data:
                    _LOGGER.warning(
                        f"Extra keys {app_data.keys()} were ignored. "
                        + "Please use app_name to cast media",
                    )
                return

            app_name = app_data.pop("app_name")
            try:
                await self._owner.controller.async_add_executor_job(
                    pychromecast.quick_play.quick_play, chromecast, app_name, app_data
                )
            except NotImplementedError:
                _LOGGER.error(f"App {app_name} not supported")
            return

        # Try the cast platforms
        for platform in self._owner.cast_platforms.values():
            result = await platform.async_play_media(
                self.entity_id, chromecast, media_type, media_id
            )
            if result:
                return

        # If media ID is a relative URL, we serve it from HA.
        media_player: core.MediaPlayerComponent = (
            self._owner.controller.components.media_player
        )
        media_id = media_player.async_process_play_media_url(media_id)

        # Configure play command for when playing a HLS stream
        if self._owner.controller.is_shc_url(media_id):
            parsed = yarl.URL(media_id)
            if parsed.path.startswith("/api/hls/"):
                extra = {
                    **extra,
                    "stream_type": "LIVE",
                    "media_info": {
                        "hlsVideoSegmentFormat": "fmp4",
                    },
                }
        elif (
            media_id.endswith(".m3u")
            or media_id.endswith(".m3u8")
            or media_id.endswith(".pls")
        ):
            try:
                playlist = await parse_playlist(self._owner.controller, media_id)
                _LOGGER.debug(
                    f"[{self.entity_id} {self._cast_info.friendly_name}] Playing item "
                    + f"{playlist[0].url} from playlist {media_id}",
                )
                media_id = playlist[0].url
                if title := playlist[0].title:
                    extra = {
                        **extra,
                        "metadata": {"title": title},
                    }
            except PlaylistSupported as err:
                _LOGGER.debug(
                    f"[{self.entity_id} {self._cast_info.friendly_name}] Playlist "
                    + f"{media_id} is supported: {err}",
                )
            except PlaylistError as err:
                _LOGGER.warning(
                    f"[{self.entity_id} {self._cast_info.friendly_name}] Failed "
                    + f"to parse playlist {media_id}: {err}",
                )

        # Default to play with the default media receiver
        app_data = {"media_id": media_id, "media_type": media_type, **extra}
        _LOGGER.debug(
            f"[{self.entity_id} {self._cast_info.friendly_name}] Playing "
            + f"{app_data} with default_media_receiver",
        )
        await self._owner.controller.async_add_executor_job(
            pychromecast.quick_play.quick_play,
            chromecast,
            "default_media_receiver",
            app_data,
        )

    def _media_status(self):
        """
        Return media status.

        First try from our own cast, then groups which our cast is a member in.
        """
        media_status = self.__media_status
        media_status_received = self._media_status_received

        if (
            media_status is None
            or media_status.player_state
            == pychromecast.controllers.media.MEDIA_PLAYER_STATE_UNKNOWN
        ):
            groups = self._mz_media_status
            for k, val in groups.items():
                if (
                    val
                    and val.player_state
                    != pychromecast.controllers.media.MEDIA_PLAYER_STATE_UNKNOWN
                ):
                    media_status = val
                    media_status_received = self._mz_media_status_received[k]
                    break

        return (media_status, media_status_received)

    @property
    def state(self) -> str | None:
        """Return the state of the player."""
        # The lovelace app loops media to prevent timing out, don't show that
        if self.app_id == core.Const.CAST_APP_ID_HOMEASSISTANT_LOVELACE:
            return core.Const.STATE_PLAYING
        if (media_status := self._media_status()[0]) is not None:
            if (
                media_status.player_state
                == pychromecast.controllers.media.MEDIA_PLAYER_STATE_PLAYING
            ):
                return core.Const.STATE_PLAYING
            if (
                media_status.player_state
                == pychromecast.controllers.media.MEDIA_PLAYER_STATE_BUFFERING
            ):
                return core.Const.STATE_BUFFERING
            if media_status.player_is_paused:
                return core.Const.STATE_PAUSED
            if media_status.player_is_idle:
                return core.Const.STATE_IDLE
        if self.app_id is not None and self.app_id != pychromecast.IDLE_APP_ID:
            if self.app_id in _APP_IDS_UNRELIABLE_MEDIA_INFO:
                # Some apps don't report media status, show the player as playing
                return core.Const.STATE_PLAYING
            return core.Const.STATE_IDLE
        if self._chromecast is not None and self._chromecast.is_idle:
            return core.Const.STATE_OFF
        return None

    @property
    def media_content_id(self) -> str:
        """Content ID of current playing media."""
        # The lovelace app loops media to prevent timing out, don't show that
        if self.app_id == core.Const.CAST_APP_ID_HOMEASSISTANT_LOVELACE:
            return None
        media_status = self._media_status()[0]
        return media_status.content_id if media_status else None

    @property
    def media_content_type(self) -> str:
        """Content type of current playing media."""
        # The lovelace app loops media to prevent timing out, don't show that
        if self.app_id == core.Const.CAST_APP_ID_HOMEASSISTANT_LOVELACE:
            return None
        if (media_status := self._media_status()[0]) is None:
            return None
        if media_status.media_is_tvshow:
            return core.MediaPlayer.MediaType.TVSHOW
        if media_status.media_is_movie:
            return core.MediaPlayer.MediaType.MOVIE
        if media_status.media_is_musictrack:
            return core.MediaPlayer.MediaType.MUSIC
        return None

    @property
    def media_duration(self):
        """Duration of current playing media in seconds."""
        # The lovelace app loops media to prevent timing out, don't show that
        if self.app_id == core.Const.CAST_APP_ID_HOMEASSISTANT_LOVELACE:
            return None
        media_status = self._media_status()[0]
        return media_status.duration if media_status else None

    @property
    def media_image_url(self):
        """Image url of current playing media."""
        if (media_status := self._media_status()[0]) is None:
            return None

        images = media_status.images

        return images[0].url if images and images[0].url else None

    @property
    def media_title(self):
        """Title of current playing media."""
        media_status = self._media_status()[0]
        return media_status.title if media_status else None

    @property
    def media_artist(self):
        """Artist of current playing media (Music track only)."""
        media_status = self._media_status()[0]
        return media_status.artist if media_status else None

    @property
    def media_album_name(self):
        """Album of current playing media (Music track only)."""
        media_status = self._media_status()[0]
        return media_status.album_name if media_status else None

    @property
    def media_album_artist(self):
        """Album artist of current playing media (Music track only)."""
        media_status = self._media_status()[0]
        return media_status.album_artist if media_status else None

    @property
    def media_track(self):
        """Track number of current playing media (Music track only)."""
        media_status = self._media_status()[0]
        return media_status.track if media_status else None

    @property
    def media_series_title(self):
        """Return the title of the series of current playing media."""
        media_status = self._media_status()[0]
        return media_status.series_title if media_status else None

    @property
    def media_season(self):
        """Season of current playing media (TV Show only)."""
        media_status = self._media_status()[0]
        return media_status.season if media_status else None

    @property
    def media_episode(self):
        """Episode of current playing media (TV Show only)."""
        media_status = self._media_status()[0]
        return media_status.episode if media_status else None

    @property
    def app_id(self):
        """Return the ID of the current running app."""
        return self._chromecast.app_id if self._chromecast else None

    @property
    def app_name(self):
        """Name of the current running app."""
        return self._chromecast.app_display_name if self._chromecast else None

    @property
    def supported_features(self):
        """Flag media player features that are supported."""
        support = (
            core.MediaPlayer.EntityFeature.PLAY_MEDIA
            | core.MediaPlayer.EntityFeature.TURN_OFF
            | core.MediaPlayer.EntityFeature.TURN_ON
        )
        media_status = self._media_status()[0]

        if (
            self._cast_status
            and self._cast_status.volume_control_type
            != pychromecast.controllers.receiver.VOLUME_CONTROL_TYPE_FIXED
        ):
            support |= (
                core.MediaPlayer.EntityFeature.VOLUME_MUTE
                | core.MediaPlayer.EntityFeature.VOLUME_SET
            )

        if (
            media_status
            and self.app_id != core.Const.CAST_APP_ID_HOMEASSISTANT_LOVELACE
        ):
            support |= (
                core.MediaPlayer.EntityFeature.PAUSE
                | core.MediaPlayer.EntityFeature.PLAY
                | core.MediaPlayer.EntityFeature.STOP
            )
            if media_status.supports_queue_next:
                support |= (
                    core.MediaPlayer.EntityFeature.PREVIOUS_TRACK
                    | core.MediaPlayer.EntityFeature.NEXT_TRACK
                )
            if media_status.supports_seek:
                support |= core.MediaPlayer.EntityFeature.SEEK

        if "media_source" in self._owner.controller.config.components:
            support |= core.MediaPlayer.EntityFeature.BROWSE_MEDIA

        return support

    @property
    def media_position(self):
        """Position of current playing media in seconds."""
        # The lovelace app loops media to prevent timing out, don't show that
        if self.app_id == core.Const.CAST_APP_ID_HOMEASSISTANT_LOVELACE:
            return None
        media_status = self._media_status()[0]
        if media_status is None or not (
            media_status.player_is_playing
            or media_status.player_is_paused
            or media_status.player_is_idle
        ):
            return None
        return media_status.current_time

    @property
    def media_position_updated_at(self):
        """When was the position of the current playing media valid.

        Returns value from homeassistant.util.dt.utcnow().
        """
        if self.app_id == core.Const.CAST_APP_ID_HOMEASSISTANT_LOVELACE:
            return None
        return self._media_status()[1]

    def _handle_signal_show_view(
        self,
        controller: pychromecast.controllers.homeassistant.HomeAssistantController,
        entity_id: str,
        view_path: str,
        url_path: str,
    ):
        """Handle a show view signal."""
        if entity_id != self.entity_id or self._chromecast is None:
            return

        if self._cast_controller is None:
            self._cast_controller = controller
            self._chromecast.register_handler(controller)

        self._cast_controller.show_lovelace_view(view_path, url_path)


async def async_setup_media_players(
    owner: GoogleCastIntegration,
    entry: core.ConfigEntry,
    async_add_entities: core.AddEntitiesCallback,
):
    """Setup MediaPlayer entities"""
    # Import CEC IGNORE attributes
    pychromecast.IGNORE_CEC += entry.data.get(Const.CONF_IGNORE_CEC) or []

    wanted_uuids = entry.data.get(Const.CONF_UUID) or None

    @core.callback
    def async_cast_discovered(discover: ChromecastInfo) -> None:
        """Handle discovery of a new chromecast."""
        # If wanted_uuids is set, we're only accepting specific cast devices identified
        # by UUID
        if wanted_uuids is not None and str(discover.uuid) not in wanted_uuids:
            # UUID not matching, ignore.
            return

        cast_device = _async_create_cast_device(owner, discover)
        if cast_device is not None:
            async_add_entities([cast_device])

    owner.controller.dispatcher.async_connect(
        Const.SIGNAL_CAST_DISCOVERED, async_cast_discovered
    )
    zeroconf: core.ZeroconfComponent = owner.controller.components.zeroconf
    ChromecastZeroconf.set_zeroconf(await zeroconf.async_get_instance())
    owner.controller.async_add_executor_job(setup_internal_discovery, owner, entry)


@core.callback
def _async_create_cast_device(owner: GoogleCastIntegration, info: ChromecastInfo):
    """Create a CastDevice entity or dynamic group from the chromecast object.

    Returns None if the cast device has already been added.
    """
    _LOGGER.debug(f"_async_create_cast_device: {info}")
    if info.uuid is None:
        _LOGGER.error(f"_async_create_cast_device uuid none: {info}")
        return None

    # Found a cast with UUID
    added_casts = owner.added_cast_devices
    if info.uuid in added_casts:
        # Already added this one, the entity will take care of moved hosts
        # itself
        return None
    # -> New cast device
    added_casts.add(info.uuid)

    if info.is_dynamic_group:
        # This is a dynamic group, do not add it but connect to the service.
        group = DynamicCastGroup(owner, info)
        group.async_setup()
        return None

    return CastMediaPlayerEntity(owner, info)
