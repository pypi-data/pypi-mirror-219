"""
Amazon Alexa MediaPlayer Integration for Smart Home - The Next Generation.

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

This integration is based custom_component "alexa_media_player"
from the Home Assistant Community Store (HACS), which is distributed
under the Terms of the Apache License, Version 2.0

The original source code and license terms can be found under:
https://github.com/custom_components/alexa_media_player
"""

import asyncio
import logging
import re
import typing

import alexapy

from ... import core
from .alexa_media import AlexaMedia
from .const import Const
from .helpers import _catch_login_errors

if not typing.TYPE_CHECKING:

    class AlexaAccountInfo:
        pass


if typing.TYPE_CHECKING:
    from .alexa_account_info import AlexaAccountInfo

_const: typing.TypeAlias = core.Const
_media_player: typing.TypeAlias = core.MediaPlayer

_LOGGER: typing.Final = logging.getLogger(__name__)
_SUPPORT_ALEXA: typing.Final = (
    _media_player.EntityFeature.PAUSE
    | _media_player.EntityFeature.PREVIOUS_TRACK
    | _media_player.EntityFeature.NEXT_TRACK
    | _media_player.EntityFeature.STOP
    | _media_player.EntityFeature.VOLUME_SET
    | _media_player.EntityFeature.PLAY
    | _media_player.EntityFeature.PLAY_MEDIA
    | _media_player.EntityFeature.TURN_OFF
    | _media_player.EntityFeature.TURN_ON
    | _media_player.EntityFeature.VOLUME_MUTE
    | _media_player.EntityFeature.SELECT_SOURCE
    | _media_player.EntityFeature.SHUFFLE_SET
)


# pylint: disable=unused-variable
class AlexaClient(core.MediaPlayer.Entity, AlexaMedia):
    """Representation of a Alexa device."""

    def __init__(
        self,
        owner: AlexaAccountInfo,
        device,
        login,
        second_account_index=0,
    ):
        # pylint: disable=unused-argument, protected-access
        """Initialize the Alexa device."""
        super().__init__(owner._owner, device, login)

        # Logged in info
        self._authenticated = None
        self._can_access_prime_music = None
        self._customer_email = None
        self._customer_id = None
        self._customer_name = None

        # Device info
        self._device = device
        self._device_name = None
        self._device_serial_number = None
        self._device_type = None
        self._device_family = None
        self._device_owner_customer_id = None
        self._software_version = None
        self._available = None
        self._assumed_state = False
        self._capabilities = []
        self._cluster_members = []
        self._locale = None
        # Media
        self._session = None
        self._media_duration = None
        self._media_image_url = None
        self._media_title = None
        self._media_pos = None
        self._media_album_name = None
        self._media_artist = None
        self._media_player_state = None
        self._media_is_muted = None
        self._media_vol_level = None
        self._previous_volume = None
        self._source = None
        self._source_list = []
        self._connected_bluetooth = None
        self._bluetooth_list = []
        self._shuffle = None
        self._repeat = None
        self._playing_parent = None
        # Last Device
        self._last_called = None
        self._last_called_timestamp = None
        self._last_called_summary = None
        # Do not Disturb state
        self._dnd = None
        # Polling state
        self._should_poll = True
        self._last_update = core.helpers.utcnow()
        self._listener = None
        self._bluetooth_state = None
        self._app_device_list = None
        self._parent_clusters = None
        self._timezone = None
        self._second_account_index = second_account_index
        self._info = owner

    async def init(self, device):
        """Initialize."""
        await self.refresh(device, skip_api=True)

    async def async_added_to_shc(self):
        """Perform tasks after loading."""
        # Register event handler on bus
        await self.refresh(self._device)
        self._listener = self._shc.dispatcher.async_connect(
            f"{self._owner.domain}_{alexapy.hide_email(self._login.email)}"[0:32],
            self._handle_event,
        )
        # Register to coordinator:
        coordinator = self._info.coordinator
        if coordinator:
            coordinator.async_add_listener(self.update)

    async def async_will_remove_from_shc(self):
        """Prepare to remove entity."""
        # Register event handler on bus
        self._listener()
        coordinator = self._info.coordinator
        if coordinator:
            try:
                coordinator.async_remove_listener(self.update)
            except AttributeError:
                pass  # ignore missing listener

    async def _handle_event(self, event):
        """Handle events.

        This will update last_called and player_state events.
        Each MediaClient reports if it's the last_called MediaClient and will
        listen for HA events to determine it is the last_called.
        When polling instead of websockets, all devices on same account will
        update to handle starting music with other devices. If websocket is on
        only the updated alexa will update.
        Last_called events are only sent if it's a new device or timestamp.
        Without polling, we must schedule the HA update manually.
        https://developers.home-assistant.io/docs/en/entity_index.html#subscribing-to-updates
        The difference between self.update and self.schedule_update_ha_state
        is self.update will pull data from Amazon, while schedule_update
        assumes the MediaClient state is already updated.
        """

        async def _refresh_if_no_audiopush(already_refreshed=False):
            seen_commands = self._info.seen_commands
            if (
                not already_refreshed
                and seen_commands
                and not (
                    "PUSH_AUDIO_PLAYER_STATE" in seen_commands
                    or "PUSH_MEDIA_CHANGE" in seen_commands
                    or "PUSH_MEDIA_PROGRESS_CHANGE" in seen_commands
                )
            ):
                # force refresh if player_state update not found, see #397
                _LOGGER.debug(
                    f"{self.account}: No PUSH_AUDIO_PLAYER_STATE/"
                    + f"PUSH_MEDIA_CHANGE/PUSH_MEDIA_PROGRESS_CHANGE in {seen_commands};"
                    + "forcing refresh",
                )
                await self.async_update()

        try:
            if not self.enabled:
                return
        except AttributeError:
            pass
        already_refreshed = False
        event_serial = None
        if "last_called_change" in event:
            event_serial = (
                event["last_called_change"]["serialNumber"]
                if event["last_called_change"]
                else None
            )
        elif "bluetooth_change" in event:
            event_serial = (
                event["bluetooth_change"]["deviceSerialNumber"]
                if event["bluetooth_change"]
                else None
            )
        elif "player_state" in event:
            event_serial = (
                event["player_state"]["dopplerId"]["deviceSerialNumber"]
                if event["player_state"]
                else None
            )
        elif "queue_state" in event:
            event_serial = (
                event["queue_state"]["dopplerId"]["deviceSerialNumber"]
                if event["queue_state"]
                else None
            )
        elif "push_activity" in event:
            event_serial = (
                event.get("push_activity", {}).get("key", {}).get("serialNumber")
            )
        if not event_serial:
            return
        if event_serial == self.device_serial_number:
            self._available = True
            self.async_write_state()
        if "last_called_change" in event:
            if (
                event_serial == self.device_serial_number
                or any(
                    item["serialNumber"] == event_serial
                    for item in self._app_device_list
                )
                and self._last_called_timestamp
                != event["last_called_change"]["timestamp"]
            ):
                _LOGGER.debug(
                    f"{self.account}: {self} is last_called: "
                    + f"{alexapy.hide_serial(self.device_serial_number)}",
                )
                self._last_called = True
                self._last_called_timestamp = event["last_called_change"]["timestamp"]
                self._last_called_summary = event["last_called_change"].get("summary")
                if self._shc and self.async_write_state:
                    self.async_write_state()
                await self._update_notify_targets()
            else:
                self._last_called = False
            if self._shc and self.async_schedule_update_state:
                force_refresh = not self._info.websocket_enabled
                self.async_schedule_update_state(force_refresh=force_refresh)
        elif "bluetooth_change" in event:
            if event_serial == self.device_serial_number:
                _LOGGER.debug(
                    f"{self.account}: {self.name} bluetooth_state update: "
                    + f"{alexapy.hide_serial(event['bluetooth_change'])}",
                )
                self._bluetooth_state = event["bluetooth_change"]
                # the setting of bluetooth_state is not consistent as this
                # takes from the event instead of the hass storage. We're
                # setting the value twice. Architectually we should have a
                # single authoritative source of truth.
                self._source = self._get_source()
                self._source_list = self._get_source_list()
                self._connected_bluetooth = self._get_connected_bluetooth()
                self._bluetooth_list = self._get_bluetooth_list()
                if self._shc and self.async_write_state:
                    self.async_write_state()
        elif "player_state" in event:
            player_state = event["player_state"]
            if event_serial == self.device_serial_number:
                if "audioPlayerState" in player_state:
                    _LOGGER.debug(
                        f"{self.account}: {self.name} state update: "
                        + f"{player_state['audioPlayerState']}",
                    )
                    # allow delay before trying to refresh to avoid http 400 errors
                    await asyncio.sleep(2)
                    await self.async_update()
                    already_refreshed = True
                elif "mediaReferenceId" in player_state:
                    _LOGGER.debug(
                        f"{self.account}: {self.name} media update: "
                        + f"%{player_state['mediaReferenceId']}",
                    )
                    await self.async_update()
                    already_refreshed = True
                elif "volumeSetting" in player_state:
                    _LOGGER.debug(
                        f"{self.account}: {self.name} volume updated: "
                        + f"{player_state['volumeSetting']}",
                    )
                    self._media_vol_level = player_state["volumeSetting"] / 100
                    if self._shc and self.async_write_state:
                        self.async_write_state()
                elif "dopplerConnectionState" in player_state:
                    self.available = player_state["dopplerConnectionState"] == "ONLINE"
                    if self._shc and self.async_write_state:
                        self.async_write_state()
                await _refresh_if_no_audiopush(already_refreshed)
        elif "push_activity" in event:
            if self.state in {
                _const.STATE_IDLE,
                _const.STATE_PAUSED,
                _const.STATE_PLAYING,
            }:
                _LOGGER.debug(
                    f"{self.account}: {self.name} checking for potential state update due "
                    + f"to push activity on {alexapy.hide_serial(event_serial)}",
                )
                # allow delay before trying to refresh to avoid http 400 errors
                await asyncio.sleep(2)
                await self.async_update()
                already_refreshed = True
        if "queue_state" in event:
            queue_state = event["queue_state"]
            if event_serial == self.device_serial_number:
                if (
                    "trackOrderChanged" in queue_state
                    and not queue_state["trackOrderChanged"]
                    and "loopMode" in queue_state
                ):
                    self._repeat = queue_state["loopMode"] == "LOOP_QUEUE"
                    _LOGGER.debug(
                        f"{self.account}: {self.name} repeat updated to: "
                        + f"{self._repeat} {queue_state['loopMode']}",
                    )
                elif "playBackOrder" in queue_state:
                    self._shuffle = queue_state["playBackOrder"] == "SHUFFLE_ALL"
                    _LOGGER.debug(
                        f"{self.account}: {self.name} shuffle updated to: "
                        + f"{self._shuffle} {queue_state['plyBackOrder']}",
                    )
                await _refresh_if_no_audiopush(already_refreshed)

    def _clear_media_details(self):
        """Set all Media Items to None."""
        # General
        self._media_duration = None
        self._media_image_url = None
        self._media_title = None
        self._media_pos = None
        self._media_album_name = None
        self._media_artist = None
        self._media_player_state = None
        self._media_is_muted = None
        # volume is also used for announce/tts so state should remain
        # self._media_vol_level = None

    def _set_authentication_details(self, auth):
        """Set Authentication based off auth."""
        self._authenticated = auth["authenticated"]
        self._can_access_prime_music = auth["canAccessPrimeMusicContent"]
        self._customer_email = auth["customerEmail"]
        self._customer_id = auth["customerId"]
        self._customer_name = auth["customerName"]

    @core.Throttle(Const.MIN_TIME_BETWEEN_SCANS, Const.MIN_TIME_BETWEEN_FORCED_SCANS)
    @_catch_login_errors
    async def refresh(self, device=None, skip_api: bool = False):
        """Refresh device data.

        This is a per device refresh and for many Alexa devices can result in
        many refreshes from each individual device. This will call the
        AlexaAPI directly.

        Args:
        device (json): A refreshed device json from Amazon. For efficiency,
                       an individual device does not refresh if it's reported
                       as offline.
        skip_api (bool): Whether to only due a device json update and not hit the API

        """
        if device is not None:
            self._device_name = device["accountName"]
            self._device_family = device["deviceFamily"]
            self._device_type = device["deviceType"]
            self._device_serial_number = device["serialNumber"]
            self._app_device_list = device["appDeviceList"]
            self._device_owner_customer_id = device["deviceOwnerCustomerId"]
            self._software_version = device["softwareVersion"]
            self._available = device["online"]
            self._capabilities = device["capabilities"]
            self._cluster_members = device["clusterMembers"]
            self._parent_clusters = device["parentClusters"]
            self._bluetooth_state = device.get("bluetooth_state", {})
            self._locale = device.get("locale", "en-US")
            self._timezone = device.get("timeZoneId", "UTC")
            self._dnd = device.get("dnd")
            self._set_authentication_details(device["auth_info"])
        session = None
        if self.available:
            _LOGGER.debug(f"{self.account}: Refreshing {self}")
            self._assumed_state = False
            if "PAIR_BT_SOURCE" in self._capabilities:
                self._source = self._get_source()
                self._source_list = self._get_source_list()
                self._connected_bluetooth = self._get_connected_bluetooth()
                self._bluetooth_list = self._get_bluetooth_list()
            new_last_called = self._get_last_called()
            if new_last_called and self._last_called != new_last_called:
                last_called = self._info.last_called
                self._last_called = new_last_called
                self._last_called_timestamp = last_called["timestamp"]
                self._last_called_summary = last_called.get("summary")
                await self._update_notify_targets()
            if skip_api and self._shc:
                self.async_write_state()
                return
            if "MUSIC_SKILL" in self._capabilities:
                if self._parent_clusters and self._shc:
                    media_players = self._info.media_players
                    playing_parents = list(
                        filter(
                            lambda x: (
                                media_players.get(x)
                                and media_players[x].state == _const.STATE_PLAYING
                            ),
                            self._parent_clusters,
                        )
                    )
                else:
                    playing_parents = []
                parent_session = {}
                if playing_parents:
                    if len(playing_parents) > 1:
                        _LOGGER.warning(
                            "Found multiple playing parents! Please file an issue"
                        )
                    parent = media_players[playing_parents[0]]
                    self._playing_parent = parent
                    parent_session = parent.session
                if parent_session:
                    session = parent_session.copy()
                    session["isPlayingInLemur"] = False
                    session["lemurVolume"] = None
                    session["volume"] = (
                        parent_session["lemurVolume"]["memberVolume"][
                            self.device_serial_number
                        ]
                        if parent_session.get("lemurVolume")
                        and parent_session.get("lemurVolume", {})
                        .get("memberVolume", {})
                        .get(self.device_serial_number)
                        else session["volume"]
                    )
                    session = {"playerInfo": session}
                else:
                    self._playing_parent = None
                    session = await self._alexa_api.get_state()
        self._clear_media_details()
        # update the session if it exists
        self._session = session if session else None
        if self._session and self._session.get("playerInfo"):
            self._session = self._session["playerInfo"]
            if self._session.get("transport"):
                self._shuffle = (
                    self._session["transport"]["shuffle"] == "SELECTED"
                    if (
                        "shuffle" in self._session["transport"]
                        and self._session["transport"]["shuffle"] != "DISABLED"
                    )
                    else None
                )
                self._repeat = (
                    self._session["transport"]["repeat"] == "SELECTED"
                    if (
                        "repeat" in self._session["transport"]
                        and self._session["transport"]["repeat"] != "DISABLED"
                    )
                    else None
                )
            if self._session.get("state"):
                self._media_player_state = self._session["state"]
                self._media_title = self._session.get("infoText", {}).get("title")
                self._media_artist = self._session.get("infoText", {}).get("subText1")
                self._media_album_name = self._session.get("infoText", {}).get(
                    "subText2"
                )
                self._media_image_url = (
                    self._session.get("mainArt", {}).get("url")
                    if self._session.get("mainArt")
                    else None
                )
                self._media_pos = (
                    self._session.get("progress", {}).get("mediaProgress")
                    if self._session.get("progress")
                    else None
                )
                self._media_duration = (
                    self._session.get("progress", {}).get("mediaLength")
                    if self._session.get("progress")
                    else None
                )
                if not self._session.get("lemurVolume"):
                    self._media_is_muted = (
                        self._session.get("volume", {}).get("muted")
                        if self._session.get("volume")
                        else self._media_is_muted
                    )
                    self._media_vol_level = (
                        self._session["volume"]["volume"] / 100
                        if self._session.get("volume")
                        and self._session.get("volume", {}).get("volume")
                        else self._media_vol_level
                    )
                else:
                    self._media_is_muted = (
                        self._session.get("lemurVolume", {})
                        .get("compositeVolume", {})
                        .get("muted")
                    )
                    self._media_vol_level = (
                        self._session["lemurVolume"]["compositeVolume"]["volume"] / 100
                        if (
                            self._session.get("lemurVolume", {})
                            .get("compositeVolume", {})
                            .get("volume")
                        )
                        else self._media_vol_level
                    )
                if self._session.get("isPlayingInLemur"):
                    media_players = self._info.media_players
                    asyncio.gather(
                        *map(
                            lambda x: (media_players[x].async_update()),
                            filter(
                                lambda x: (
                                    media_players.get(x) and media_players[x].available
                                ),
                                self._cluster_members,
                            ),
                        )
                    )
        if self._shc:
            self.async_write_state()

    @property
    def source(self):
        """Return the current input source."""
        return self._source

    @property
    def source_list(self):
        """List of available input sources."""
        return self._source_list

    @_catch_login_errors
    async def async_select_source(self, source):
        """Select input source."""
        if source == "Local Speaker":
            if self._shc:
                self._shc.async_create_task(self._alexa_api.disconnect_bluetooth())
            else:
                await self._alexa_api.disconnect_bluetooth()
            self._source = "Local Speaker"
        elif self._bluetooth_state.get("pairedDeviceList"):
            for devices in self._bluetooth_state["pairedDeviceList"]:
                if devices["friendlyName"] == source:
                    if self._shc:
                        self._shc.async_create_task(
                            self._alexa_api.set_bluetooth(devices["address"])
                        )
                    else:
                        await self._alexa_api.set_bluetooth(devices["address"])
                    self._source = source
        if not self._info.websocket_enabled:
            await self.async_update()

    def _get_source(self):
        source = "Local Speaker"
        if self._bluetooth_state.get("pairedDeviceList"):
            for device in self._bluetooth_state["pairedDeviceList"]:
                if (
                    device["connected"] is True
                    and device["friendlyName"] in self.source_list
                ):
                    return device["friendlyName"]
        return source

    def _get_source_list(self):
        sources = []
        if self._bluetooth_state.get("pairedDeviceList"):
            for devices in self._bluetooth_state["pairedDeviceList"]:
                if devices["profiles"] and "A2DP-SOURCE" in devices["profiles"]:
                    sources.append(devices["friendlyName"])
        return ["Local Speaker"] + sources

    def _get_connected_bluetooth(self):
        source = None
        if self._bluetooth_state.get("pairedDeviceList"):
            for device in self._bluetooth_state["pairedDeviceList"]:
                if device["connected"] is True:
                    return device["friendlyName"]
        return source

    def _get_bluetooth_list(self):
        sources = []
        if self._bluetooth_state.get("pairedDeviceList"):
            for devices in self._bluetooth_state["pairedDeviceList"]:
                sources.append(devices["friendlyName"])
        return sources

    def _get_last_called(self):
        try:
            last_called_serial = (
                None if self._shc is None else (self._info.last_called["serialNumber"])
            )
        except (TypeError, KeyError):
            last_called_serial = None
        _LOGGER.debug(
            f"{self.account}: {self._device_name}: Last_called check: self: "
            + f"{alexapy.hide_serial(self._device_serial_number)} reported: "
            + f"{alexapy.hide_serial(last_called_serial)}",
        )
        return last_called_serial is not None and (
            self._device_serial_number == last_called_serial
            or any(
                item["serialNumber"] == last_called_serial
                for item in self._app_device_list
            )
        )

    @property
    def available(self):
        """Return the availability of the client."""
        return self._available

    @available.setter
    def available(self, state):
        """Set the availability state."""
        self._available = state

    @property
    def assumed_state(self):
        """Return whether the state is an assumed_state."""
        return self._assumed_state

    @property
    def hidden(self):
        """Return whether the sensor should be hidden."""
        return "MUSIC_SKILL" not in self._capabilities

    @property
    def unique_id(self):
        """Return the id of this Alexa client."""
        email = self.email
        return (
            core.helpers.slugify(f"{self.device_serial_number}_{email}")
            if self._second_account_index
            else self.device_serial_number
        )

    @property
    def name(self):
        """Return the name of the device."""
        return self._device_name

    @property
    def device_serial_number(self):
        """Return the machine identifier of the device."""
        return self._device_serial_number

    @property
    def session(self):
        """Return the session, if any."""
        return self._session

    @property
    def state(self):
        """Return the state of the device."""
        if not self.available:
            return _const.STATE_UNAVAILABLE
        if self._media_player_state == "PLAYING":
            return _const.STATE_PLAYING
        if self._media_player_state == "PAUSED":
            return _const.STATE_PAUSED
        if self._media_player_state == "IDLE":
            return _const.STATE_IDLE
        return _const.STATE_STANDBY

    def update(self):
        """Get the latest details on a media player synchronously."""
        return self._shc.add_job(self.async_update)

    @_catch_login_errors
    async def async_update(self):
        """Get the latest details on a media player.

        Because media players spend the majority of time idle, an adaptive
        update should be used to avoid flooding Amazon focusing on known
        play states. An initial version included an update_devices call on
        every update. However, this quickly floods the network for every new
        device added. This should only call refresh() to call the AlexaAPI.
        """
        try:
            if not self.enabled:
                return
        except AttributeError:
            pass
        email = self.email
        if (
            self.entity_id is None  # Device has not initialized yet
            or not self._owner.is_account_defined(email)
            or self._login.session.closed
        ):
            self._assumed_state = True
            self.available = False
            return
        device = self._info.media_player_devices[self.device_serial_number]
        seen_commands = self._info.seen_commands

        await self.refresh(  # pylint: disable=unexpected-keyword-arg
            device, no_throttle=True
        )
        websocket_enabled = self._info.websocket_enabled
        if (
            self.state == _const.STATE_PLAYING
            and
            #  only enable polling if websocket not connected
            (
                not websocket_enabled
                or not seen_commands
                or not (
                    "PUSH_AUDIO_PLAYER_STATE" in seen_commands
                    or "PUSH_MEDIA_CHANGE" in seen_commands
                    or "PUSH_MEDIA_PROGRESS_CHANGE" in seen_commands
                )
            )
        ):
            self._should_poll = False  # disable polling since manual update
            if (
                self._last_update == 0
                or core.helpers.as_timestamp(core.helpers.utcnow())
                - core.helpers.as_timestamp(self._last_update)
                > Const.PLAY_SCAN_INTERVAL
            ):
                _LOGGER.debug(
                    f"{self.account}: {self.name} playing; scheduling update in "
                    + f"{Const.PLAY_SCAN_INTERVAL} seconds",
                )
                self._shc.call_later(
                    Const.PLAY_SCAN_INTERVAL,
                    lambda: self.async_schedule_update_state(force_refresh=True),
                )
        elif self._should_poll:  # Not playing, one last poll
            self._should_poll = False
            if not websocket_enabled:
                _LOGGER.debug(
                    f"{self.account}: Disabling polling and scheduling last update in"
                    + f" 300 seconds for {self.name}",
                )
                self._shc.call_later(
                    300,
                    lambda: self.async_schedule_update_state(force_refresh=True),
                )
            else:
                _LOGGER.debug(
                    f"{self.account}: Disabling polling for {self.name}",
                )
        self._last_update = core.helpers.utcnow()
        self.async_write_state()

    @property
    def media_content_type(self):
        """Return the content type of current playing media."""
        if self.state in [_const.STATE_PLAYING, _const.STATE_PAUSED]:
            return str(core.MediaPlayer.MediaType.MUSIC)
        return _const.STATE_STANDBY

    @property
    def media_artist(self):
        """Return the artist of current playing media, music track only."""
        return self._media_artist

    @property
    def media_album_name(self):
        """Return the album name of current playing media, music track only."""
        return self._media_album_name

    @property
    def media_duration(self):
        """Return the duration of current playing media in seconds."""
        return self._media_duration

    @property
    def media_position(self):
        """Return the duration of current playing media in seconds."""
        return self._media_pos

    @property
    def media_position_updated_at(self):
        """When was the position of the current playing media valid."""
        return self._last_update

    @property
    def media_image_url(self) -> str:
        """Return the image URL of current playing media."""
        if self._media_image_url:
            return re.sub("\\(", "%28", re.sub("\\)", "%29", self._media_image_url))
            # fix failure of HA media player ui to quote "(" or ")"
        return None

    @property
    def media_image_remotely_accessible(self):
        """Return whether image is accessible outside of the home network."""
        return bool(self._media_image_url)

    @property
    def media_title(self):
        """Return the title of current playing media."""
        return self._media_title

    @property
    def device_family(self):
        """Return the make of the device (ex. Echo, Other)."""
        return self._device_family

    @property
    def dnd_state(self):
        """Return the Do Not Disturb state."""
        return self._dnd

    @dnd_state.setter
    def dnd_state(self, state):
        """Set the Do Not Disturb state."""
        self._dnd = state

    @_catch_login_errors
    async def async_set_shuffle(self, shuffle):
        """Enable/disable shuffle mode."""
        if self._shc:
            self._shc.async_create_task(self._alexa_api.shuffle(shuffle))
        else:
            await self._alexa_api.shuffle(shuffle)
        self._shuffle = shuffle

    @property
    def shuffle(self):
        """Return the Shuffle state."""
        return self._shuffle

    @shuffle.setter
    def shuffle(self, state):
        """Set the Shuffle state."""
        self._shuffle = state
        self.async_write_state()

    @property
    def repeat_state(self):
        """Return the Repeat state."""
        return self._repeat

    @repeat_state.setter
    def repeat_state(self, state):
        """Set the Repeat state."""
        self._repeat = state
        self.async_write_state()

    @property
    def supported_features(self):
        """Flag media player features that are supported."""
        return _SUPPORT_ALEXA

    @_catch_login_errors
    async def async_set_volume_level(self, volume):
        """Set volume level, range 0..1."""
        if not self.available:
            return
        if self._shc:
            self._shc.async_create_task(self._alexa_api.set_volume(volume))
        else:
            await self._alexa_api.set_volume(volume)
        self._media_vol_level = volume
        if not self._info.websocket_enabled:
            await self.async_update()

    @property
    def volume_level(self):
        """Return the volume level of the client (0..1)."""
        return self._media_vol_level

    @property
    def is_volume_muted(self):
        """Return boolean if volume is currently muted."""
        if self.volume_level == 0:
            return True
        return False

    @_catch_login_errors
    async def async_mute_volume(self, mute):
        """Mute the volume.

        Since we can't actually mute, we'll:
        - On mute, store volume and set volume to 0
        - On unmute, set volume to previously stored volume
        """
        if not self.available:
            return

        self._media_is_muted = mute
        if mute:
            self._previous_volume = self.volume_level
            if self._shc:
                self._shc.async_create_task(self._alexa_api.set_volume(0))
            else:
                await self._alexa_api.set_volume(0)
        else:
            if self._previous_volume is not None:
                if self._shc:
                    self._shc.async_create_task(
                        self._alexa_api.set_volume(self._previous_volume)
                    )
                else:
                    await self._alexa_api.set_volume(self._previous_volume)
            else:
                if self._shc:
                    self._shc.async_create_task(self._alexa_api.set_volume(50))
                else:
                    await self._alexa_api.set_volume(50)
        if not self._info.websocket_enabled:
            await self.async_update()

    @_catch_login_errors
    async def async_media_play(self):
        """Send play command."""
        if not (
            self.state in [_const.STATE_PLAYING, _const.STATE_PAUSED] and self.available
        ):
            return
        if self._playing_parent:
            await self._playing_parent.async_media_play()
        else:
            if self._shc:
                self._shc.async_create_task(self._alexa_api.play())
            else:
                await self._alexa_api.play()
        if not self._info.websocket_enabled:
            await self.async_update()

    @_catch_login_errors
    async def async_media_pause(self):
        """Send pause command."""
        if not (
            self.state in [_const.STATE_PLAYING, _const.STATE_PAUSED] and self.available
        ):
            return
        if self._playing_parent:
            await self._playing_parent.async_media_pause()
        else:
            if self._shc:
                self._shc.async_create_task(self._alexa_api.pause())
            else:
                await self._alexa_api.pause()
        if not self._info.websocket_enabled:
            await self.async_update()

    @_catch_login_errors
    async def async_media_stop(self):
        """Send stop command."""
        if not self.available:
            return
        if self._playing_parent:
            await self._playing_parent.async_media_stop()
        else:
            if self._shc:
                self._shc.async_create_task(
                    self._alexa_api.stop(
                        customer_id=self._customer_id,
                        queue_delay=self._info.queue_delay,
                    )
                )
            else:
                await self._alexa_api.stop(
                    customer_id=self._customer_id,
                    queue_delay=self._info.queue_delay,
                )
        if not self._info.websocket_enabled:
            await self.async_update()

    @_catch_login_errors
    async def async_turn_off(self):
        """Turn the client off.

        While Alexa's do not have on/off capability, we can use this as another
        trigger to do updates. For turning off, we can clear media_details.
        """
        self._should_poll = False
        await self.async_media_pause()
        self._clear_media_details()

    @_catch_login_errors
    async def async_turn_on(self):
        """Turn the client on.

        While Alexa's do not have on/off capability, we can use this as another
        trigger to do updates.
        """
        self._should_poll = True
        await self.async_media_pause()

    @_catch_login_errors
    async def async_media_next_track(self):
        """Send next track command."""
        if not (
            self.state in [_const.STATE_PLAYING, _const.STATE_PAUSED] and self.available
        ):
            return
        if self._playing_parent:
            await self._playing_parent.async_media_next_track()
        else:
            if self._shc:
                self._shc.async_create_task(self._alexa_api.next())
            else:
                await self._alexa_api.next()
        if not self._info.websocket_enabled:
            await self.async_update()

    @_catch_login_errors
    async def async_media_previous_track(self):
        """Send previous track command."""
        if not (
            self.state in [_const.STATE_PLAYING, _const.STATE_PAUSED] and self.available
        ):
            return
        if self._playing_parent:
            await self._playing_parent.async_media_previous_track()
        else:
            if self._shc:
                self._shc.async_create_task(self._alexa_api.previous())
            else:
                await self._alexa_api.previous()
        if not self._info.websocket_enabled:
            await self.async_update()

    @_catch_login_errors
    async def async_send_tts(self, message, **kwargs):
        """Send TTS to Device.

        NOTE: Does not work on WHA Groups.
        """
        if self._shc:
            self._shc.async_create_task(
                self._alexa_api.send_tts(
                    message, customer_id=self._customer_id, **kwargs
                )
            )
        else:
            await self._alexa_api.send_tts(
                message, customer_id=self._customer_id, **kwargs
            )

    @_catch_login_errors
    async def async_send_announcement(self, message, **kwargs):
        """Send announcement to the media player."""
        if self._shc:
            self._shc.async_create_task(
                self._alexa_api.send_announcement(
                    message, customer_id=self._customer_id, **kwargs
                )
            )
        else:
            await self._alexa_api.send_announcement(
                message, customer_id=self._customer_id, **kwargs
            )

    @_catch_login_errors
    async def async_send_mobilepush(self, message, **kwargs):
        """Send push to the media player's associated mobile devices."""
        if self._shc:
            self._shc.async_create_task(
                self._alexa_api.send_mobilepush(
                    message, customer_id=self._customer_id, **kwargs
                )
            )
        else:
            await self._alexa_api.send_mobilepush(
                message, customer_id=self._customer_id, **kwargs
            )

    @_catch_login_errors
    async def async_send_dropin_notification(self, message, **kwargs):
        """Send notification dropin to the media player's associated mobile devices."""
        if self._shc:
            self._shc.async_create_task(
                self._alexa_api.send_dropin_notification(
                    message, customer_id=self._customer_id, **kwargs
                )
            )
        else:
            await self._alexa_api.send_dropin_notification(
                message, customer_id=self._customer_id, **kwargs
            )

    @_catch_login_errors
    async def async_play_media(self, media_type, media_id, enqueue=None, **kwargs):
        # pylint: disable=unused-argument
        """Send the play_media command to the media player."""
        queue_delay = self._info.queue_delay
        if media_type == "music":
            await self.async_send_tts(
                "Sorry, text to speech can only be called"
                + " with the notify.alexa_media service."
                + " Please see the alexa_media wiki for details."
            )
            _LOGGER.warning(
                "Sorry, text to speech can only be called"
                + " with the notify.alexa_media service."
                + " Please see the alexa_media wiki for details."
                + "https://github.com/custom-components/alexa_media_player/wiki/"
                + "Configuration%3A-Notification-Component#use-the-notifyalexa_media-service"
            )
        elif media_type == "sequence":
            _LOGGER.debug(
                f"{self.account}: {self}: Running sequence {media_id} with queue_delay "
                + f"{queue_delay}",
            )
            if self._shc:
                self._shc.async_create_task(
                    self._alexa_api.send_sequence(
                        media_id,
                        customer_id=self._customer_id,
                        queue_delay=queue_delay,
                        **kwargs,
                    )
                )
            else:
                await self._alexa_api.send_sequence(
                    media_id,
                    customer_id=self._customer_id,
                    queue_delay=queue_delay,
                    **kwargs,
                )
        elif media_type == "routine":
            _LOGGER.debug(
                f"{self.account}: {self}: Running routine {media_id} with queue_delay "
                + f"{queue_delay}",
            )
            if self._shc:
                self._shc.async_create_task(
                    self._alexa_api.run_routine(
                        media_id,
                        queue_delay=queue_delay,
                    )
                )
            else:
                await self._alexa_api.run_routine(
                    media_id,
                    queue_delay=queue_delay,
                )
        elif media_type == "sound":
            _LOGGER.debug(
                f"{self.account}: {self}: Playing sound {media_id} with queue_delay {queue_delay}",
            )
            if self._shc:
                self._shc.async_create_task(
                    self._alexa_api.play_sound(
                        media_id,
                        customer_id=self._customer_id,
                        queue_delay=queue_delay,
                        **kwargs,
                    )
                )
            else:
                await self._alexa_api.play_sound(
                    media_id,
                    customer_id=self._customer_id,
                    queue_delay=queue_delay,
                    **kwargs,
                )
        elif media_type == "skill":
            _LOGGER.debug(
                f"{self.account}: {self}: Running skill {media_id} with queue_delay {queue_delay}",
            )
            if self._shc:
                self._shc.async_create_task(
                    self._alexa_api.run_skill(
                        media_id,
                        queue_delay=queue_delay,
                    )
                )
            else:
                await self._alexa_api.run_skill(
                    media_id,
                    queue_delay=queue_delay,
                )
        elif media_type == "image":
            _LOGGER.debug(
                f"{self.account}: {self}: Setting background to {media_id}",
            )
            if self._shc:
                self._shc.async_create_task(self._alexa_api.set_background(media_id))
            else:
                await self._alexa_api.set_background(media_id)
        elif media_type == "custom":
            _LOGGER.debug(
                f'{self.account}: self: Running custom command: "{media_id}" '
                + f"with queue_delay {queue_delay}",
            )
            if self._shc:
                self._shc.async_create_task(
                    self._alexa_api.run_custom(
                        media_id,
                        customer_id=self._customer_id,
                        queue_delay=queue_delay,
                        **kwargs,
                    )
                )
            else:
                await self._alexa_api.run_custom(
                    media_id,
                    customer_id=self._customer_id,
                    queue_delay=queue_delay,
                    **kwargs,
                )
        else:
            _LOGGER.debug(
                f"{self.account}: {self}: Playing music {media_id} on {media_type} with "
                + f"queue_delay {queue_delay}",
            )
            if self._shc:
                self._shc.async_create_task(
                    self._alexa_api.play_music(
                        media_type,
                        media_id,
                        customer_id=self._customer_id,
                        queue_delay=queue_delay,
                        timer=kwargs.get("extra", {}).get("timer", None),
                        **kwargs,
                    )
                )
            else:
                await self._alexa_api.play_music(
                    media_type,
                    media_id,
                    customer_id=self._customer_id,
                    queue_delay=queue_delay,
                    timer=kwargs.get("extra", {}).get("timer", None),
                    **kwargs,
                )
        if not self._info.websocket_enabled:
            await self.async_update()

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        attr = {
            "available": self.available,
            "last_called": self._last_called,
            "last_called_timestamp": self._last_called_timestamp,
            "last_called_summary": self._last_called_summary,
            "connected_bluetooth": self._connected_bluetooth,
            "bluetooth_list": self._bluetooth_list,
        }
        return attr

    @property
    def should_poll(self):
        """Return the polling state."""
        return self._should_poll

    @property
    def device_info(self):
        """Return the device_info of the device."""
        return {
            "identifiers": {(self._owner.domain, self.unique_id)},
            "name": self.name,
            "manufacturer": "Amazon",
            "model": f"{self._device_family} {self._device_type}",
            "sw_version": self._software_version,
        }

    async def _update_notify_targets(self) -> None:
        """Update notification service targets."""
        notify = self._owner.notify_service
        if notify and notify.registered_targets:
            await notify.async_register_services()
            entity_name_last_called = (
                f"{self._owner.domain}_last_called"
                + f"{'_'+ self._login.email if self.unique_id[-1:].isdigit() else ''}"
            )
            await asyncio.sleep(2)
            if (
                notify.last_called
                and notify.registered_targets.get(entity_name_last_called)
                != self.unique_id
            ):
                # pylint: disable=protected-access
                notify._last_called = False
                await notify.async_register_services()
                await asyncio.sleep(2)
                notify._last_called = True
                await notify.async_register_services()
