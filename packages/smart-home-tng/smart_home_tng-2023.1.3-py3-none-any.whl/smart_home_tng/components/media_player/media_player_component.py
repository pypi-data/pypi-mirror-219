"""
Media Player Component for Smart Home - The Next Generation.

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

import asyncio
import datetime as dt
import logging
import typing
import urllib.parse

import voluptuous as vol
import yarl

from ... import core
from .media_player_image_view import MediaPlayerImageView

_cv: typing.TypeAlias = core.ConfigValidation
_LOGGER: typing.Final = logging.getLogger(__name__)
_BROWSE_MEDIA: typing.Final = {
    vol.Required("type"): "media_player/browse_media",
    vol.Required("entity_id"): _cv.entity_id,
    vol.Inclusive(
        core.MediaPlayer.ATTR_MEDIA_CONTENT_TYPE,
        "media_ids",
        "media_content_type and media_content_id must be provided together",
    ): str,
    vol.Inclusive(
        core.MediaPlayer.ATTR_MEDIA_CONTENT_ID,
        "media_ids",
        "media_content_type and media_content_id must be provided together",
    ): str,
}
_CONDITION_TYPES: typing.Final = {
    "is_on",
    "is_off",
    "is_buffering",
    "is_idle",
    "is_paused",
    "is_playing",
}

_CONDITION_SCHEMA: typing.Final = _cv.DEVICE_CONDITION_BASE_SCHEMA.extend(
    {
        vol.Required(core.Const.CONF_ENTITY_ID): _cv.entity_id,
        vol.Required(core.Const.CONF_TYPE): vol.In(_CONDITION_TYPES),
    }
)
_TRIGGER_TYPES: typing.Final = {
    "turned_on",
    "turned_off",
    "buffering",
    "idle",
    "paused",
    "playing",
}
_MEDIA_PLAYER_TRIGGER_SCHEMA: typing.Final = _cv.DEVICE_TRIGGER_BASE_SCHEMA.extend(
    {
        vol.Required(core.Const.CONF_ENTITY_ID): _cv.entity_id,
        vol.Required(core.Const.CONF_TYPE): vol.In(_TRIGGER_TYPES),
        vol.Optional(core.Const.CONF_FOR): _cv.positive_time_period_dict,
    }
)
# Paths that we don't need to sign
_PATHS_WITHOUT_AUTH: typing.Final = ("/api/tts_proxy/",)


# pylint: disable=unused-variable, too-many-ancestors
class MediaPlayerComponent(
    core.MediaPlayerComponent,
    core.ConditionPlatform,
    core.GroupPlatform,
    core.RecorderPlatform,
    core.ReproduceStatePlatform,
    core.TriggerPlatform,
):
    """Component to interface with various media players."""

    def __init__(self, path: typing.Iterable[str]):
        super().__init__(path)
        self._entities: core.EntityComponent = None
        self._supported_platforms = frozenset(
            [
                core.Platform.CONDITION,
                core.Platform.GROUP,
                core.Platform.RECORDER,
                core.Platform.REPRODUCE_STATE,
                core.Platform.TRIGGER,
            ]
        )

    @property
    def entity_component(self) -> core.EntityComponent:
        return self._entities

    @property
    def scan_interval(self) -> dt.timedelta:
        return core.MediaPlayer.SCAN_INTERVAL

    def _is_on(self, entity_id: str) -> bool:
        """
        Return true if specified media player entity_id is on.

        Check all media player if no entity_id specified.
        """
        entity_ids = (
            [entity_id] if entity_id else self.controller.states.entity_ids(self.domain)
        )
        return any(
            not self.controller.states.is_state(entity_id, core.Const.STATE_OFF)
            for entity_id in entity_ids
        )

    async def async_setup(self, config: core.ConfigType) -> bool:
        """Track states and offer events for media_players."""
        component = self._entities = core.EntityComponent(
            _LOGGER,
            self.domain,
            self.controller,
            self.scan_interval,
        )

        websocket_api: core.WebSocket.Component = (
            self.controller.components.websocket_api
        )
        websocket_api.register_command(self._browse_media, _BROWSE_MEDIA)
        self.controller.http.register_view(MediaPlayerImageView(component))

        await component.async_setup(config)

        component.async_register_entity_service(
            core.Const.SERVICE_TURN_ON,
            {},
            "async_turn_on",
            [core.MediaPlayer.EntityFeature.TURN_ON],
        )
        component.async_register_entity_service(
            core.Const.SERVICE_TURN_OFF,
            {},
            "async_turn_off",
            [core.MediaPlayer.EntityFeature.TURN_OFF],
        )
        component.async_register_entity_service(
            core.Const.SERVICE_TOGGLE,
            {},
            "async_toggle",
            [
                core.MediaPlayer.EntityFeature.TURN_OFF
                | core.MediaPlayer.EntityFeature.TURN_ON
            ],
        )
        component.async_register_entity_service(
            core.Const.SERVICE_VOLUME_UP,
            {},
            "async_volume_up",
            [
                core.MediaPlayer.EntityFeature.VOLUME_SET,
                core.MediaPlayer.EntityFeature.VOLUME_STEP,
            ],
        )
        component.async_register_entity_service(
            core.Const.SERVICE_VOLUME_DOWN,
            {},
            "async_volume_down",
            [
                core.MediaPlayer.EntityFeature.VOLUME_SET,
                core.MediaPlayer.EntityFeature.VOLUME_STEP,
            ],
        )
        component.async_register_entity_service(
            core.Const.SERVICE_MEDIA_PLAY_PAUSE,
            {},
            "async_media_play_pause",
            [
                core.MediaPlayer.EntityFeature.PLAY
                | core.MediaPlayer.EntityFeature.PAUSE
            ],
        )
        component.async_register_entity_service(
            core.Const.SERVICE_MEDIA_PLAY,
            {},
            "async_media_play",
            [core.MediaPlayer.EntityFeature.PLAY],
        )
        component.async_register_entity_service(
            core.Const.SERVICE_MEDIA_PAUSE,
            {},
            "async_media_pause",
            [core.MediaPlayer.EntityFeature.PAUSE],
        )
        component.async_register_entity_service(
            core.Const.SERVICE_MEDIA_STOP,
            {},
            "async_media_stop",
            [core.MediaPlayer.EntityFeature.STOP],
        )
        component.async_register_entity_service(
            core.Const.SERVICE_MEDIA_NEXT_TRACK,
            {},
            "async_media_next_track",
            [core.MediaPlayer.EntityFeature.NEXT_TRACK],
        )
        component.async_register_entity_service(
            core.Const.SERVICE_MEDIA_PREVIOUS_TRACK,
            {},
            "async_media_previous_track",
            [core.MediaPlayer.EntityFeature.PREVIOUS_TRACK],
        )
        component.async_register_entity_service(
            core.MediaPlayer.SERVICE_CLEAR_PLAYLIST,
            {},
            "async_clear_playlist",
            [core.MediaPlayer.EntityFeature.CLEAR_PLAYLIST],
        )
        component.async_register_entity_service(
            core.Const.SERVICE_VOLUME_SET,
            vol.All(
                _cv.make_entity_service_schema(
                    {
                        vol.Required(
                            core.MediaPlayer.ATTR_MEDIA_VOLUME_LEVEL
                        ): _cv.small_float
                    }
                ),
                _rename_keys(volume=core.MediaPlayer.ATTR_MEDIA_VOLUME_LEVEL),
            ),
            "async_set_volume_level",
            [core.MediaPlayer.EntityFeature.VOLUME_SET],
        )
        component.async_register_entity_service(
            core.Const.SERVICE_VOLUME_MUTE,
            vol.All(
                _cv.make_entity_service_schema(
                    {
                        vol.Required(
                            core.MediaPlayer.ATTR_MEDIA_VOLUME_MUTED
                        ): _cv.boolean
                    }
                ),
                _rename_keys(mute=core.MediaPlayer.ATTR_MEDIA_VOLUME_MUTED),
            ),
            "async_mute_volume",
            [core.MediaPlayer.EntityFeature.VOLUME_MUTE],
        )
        component.async_register_entity_service(
            core.Const.SERVICE_MEDIA_SEEK,
            vol.All(
                _cv.make_entity_service_schema(
                    {
                        vol.Required(
                            core.MediaPlayer.ATTR_MEDIA_SEEK_POSITION
                        ): _cv.positive_float
                    }
                ),
                _rename_keys(position=core.MediaPlayer.ATTR_MEDIA_SEEK_POSITION),
            ),
            "async_media_seek",
            [core.MediaPlayer.EntityFeature.SEEK],
        )
        component.async_register_entity_service(
            core.MediaPlayer.SERVICE_JOIN,
            {
                vol.Required(core.MediaPlayer.ATTR_GROUP_MEMBERS): vol.All(
                    _cv.ensure_list, [_cv.entity_id]
                )
            },
            "async_join_players",
            [core.MediaPlayer.EntityFeature.GROUPING],
        )
        component.async_register_entity_service(
            core.MediaPlayer.SERVICE_SELECT_SOURCE,
            {vol.Required(core.MediaPlayer.ATTR_INPUT_SOURCE): _cv.string},
            "async_select_source",
            [core.MediaPlayer.EntityFeature.SELECT_SOURCE],
        )
        component.async_register_entity_service(
            core.MediaPlayer.SERVICE_SELECT_SOUND_MODE,
            {vol.Required(core.MediaPlayer.ATTR_SOUND_MODE): _cv.string},
            "async_select_sound_mode",
            [core.MediaPlayer.EntityFeature.SELECT_SOUND_MODE],
        )

        # Remove in Home Assistant 2022.9
        def _rewrite_enqueue(value):
            """Rewrite the enqueue value."""
            if core.MediaPlayer.ATTR_MEDIA_ENQUEUE not in value:
                pass
            elif value[core.MediaPlayer.ATTR_MEDIA_ENQUEUE] is True:
                value[
                    core.MediaPlayer.ATTR_MEDIA_ENQUEUE
                ] = core.MediaPlayer.Enqueue.ADD
                _LOGGER.warning(
                    "Playing media with enqueue set to True is deprecated. Use 'add' instead"
                )
            elif value[core.MediaPlayer.ATTR_MEDIA_ENQUEUE] is False:
                value[
                    core.MediaPlayer.ATTR_MEDIA_ENQUEUE
                ] = core.MediaPlayer.Enqueue.PLAY
                _LOGGER.warning(
                    "Playing media with enqueue set to False is deprecated. Use 'play' instead"
                )

            return value

        component.async_register_entity_service(
            core.MediaPlayer.SERVICE_PLAY_MEDIA,
            vol.All(
                _cv.make_entity_service_schema(core.MediaPlayer.PLAY_MEDIA_SCHEMA),
                _rewrite_enqueue,
                _rename_keys(
                    media_type=core.MediaPlayer.ATTR_MEDIA_CONTENT_TYPE,
                    media_id=core.MediaPlayer.ATTR_MEDIA_CONTENT_ID,
                    enqueue=core.MediaPlayer.ATTR_MEDIA_ENQUEUE,
                ),
            ),
            "async_play_media",
            [core.MediaPlayer.EntityFeature.PLAY_MEDIA],
        )
        component.async_register_entity_service(
            core.Const.SERVICE_SHUFFLE_SET,
            {vol.Required(core.MediaPlayer.ATTR_MEDIA_SHUFFLE): _cv.boolean},
            "async_set_shuffle",
            [core.MediaPlayer.EntityFeature.SHUFFLE_SET],
        )
        component.async_register_entity_service(
            core.MediaPlayer.SERVICE_UNJOIN,
            {},
            "async_unjoin_player",
            [core.MediaPlayer.EntityFeature.GROUPING],
        )

        component.async_register_entity_service(
            core.Const.SERVICE_REPEAT_SET,
            {
                vol.Required(core.MediaPlayer.ATTR_MEDIA_REPEAT): vol.In(
                    core.MediaPlayer.REPEAT_MODES
                )
            },
            "async_set_repeat",
            [core.MediaPlayer.EntityFeature.REPEAT_SET],
        )

        return True

    async def async_setup_entry(self, entry: core.ConfigEntry) -> bool:
        """Set up a config entry."""
        component = self._entities
        return await component.async_setup_entry(entry)

    async def async_unload_entry(self, entry: core.ConfigEntry) -> bool:
        """Unload a config entry."""
        component = self._entities
        return await component.async_unload_entry(entry)

    async def _browse_media(
        self,
        connection: core.WebSocket.Connection,
        msg: dict,
    ):
        """
        Browse media available to the media_player entity.

        To use, media_player integrations can implement MediaPlayerEntity.async_browse_media()
        """
        component = self._entities
        player: core.MediaPlayer.Entity = component.get_entity(msg["entity_id"])

        if player is None:
            connection.send_error(msg["id"], "entity_not_found", "Entity not found")
            return

        if not player.supported_features & core.MediaPlayer.EntityFeature.BROWSE_MEDIA:
            connection.send_error(
                msg["id"],
                core.WebSocket.ERR_NOT_SUPPORTED,
                "Player does not support browsing media",
            )
            return

        media_content_type = msg.get(core.MediaPlayer.ATTR_MEDIA_CONTENT_TYPE)
        media_content_id = msg.get(core.MediaPlayer.ATTR_MEDIA_CONTENT_ID)

        try:
            payload = await player.async_browse_media(
                media_content_type, media_content_id
            )
        except NotImplementedError:
            _LOGGER.error(
                f"{player.entity_id} allows media browsing but its integration "
                + f"({player.platform.platform_name}) does not",
            )
            connection.send_error(
                msg["id"],
                core.WebSocket.ERR_NOT_SUPPORTED,
                "Integration does not support browsing media",
            )
            return
        except core.MediaPlayer.BrowseError as err:
            connection.send_error(msg["id"], core.WebSocket.ERR_UNKNOWN_ERROR, str(err))
            return

        # For backwards compat
        if isinstance(payload, core.BrowseMedia):
            payload = payload.as_dict()
        else:
            _LOGGER.warning("Browse Media should use new BrowseMedia class")

        connection.send_result(msg["id"], payload)

    def async_process_play_media_url(
        self,
        media_content_id: str,
        *,
        allow_relative_url: bool = False,
    ) -> str:
        """
        Update a media URL with authentication
        if it points at Smart Home - The Next Generation.
        """
        parsed = yarl.URL(media_content_id)
        shc = self.controller

        if parsed.scheme and parsed.scheme not in ("http", "https"):
            return media_content_id

        if parsed.is_absolute():
            if not shc.is_shc_url(media_content_id):
                return media_content_id
        else:
            if media_content_id[0] != "/":
                raise ValueError("URL is relative, but does not start with a /")

        if parsed.query:
            logging.getLogger(__name__).debug(
                "Not signing path for content with query param"
            )
        elif parsed.path.startswith(_PATHS_WITHOUT_AUTH):
            # We don't sign this path if it doesn't need auth. Although signing itself can't hurt,
            # some devices are unable to handle long URLs and the auth signature might push it over.
            pass
        else:
            signed_path = shc.http.async_sign_path(
                urllib.parse.quote(parsed.path),
                dt.timedelta(seconds=core.MediaPlayer.CONTENT_AUTH_EXPIRY_TIME),
            )
            media_content_id = str(parsed.join(yarl.URL(signed_path)))

        # convert relative URL to absolute URL
        if not parsed.is_absolute() and not allow_relative_url:
            base_url = None

            try:
                base_url = shc.get_url()
            except core.NoURLAvailableError as err:
                msg = "Unable to determine URL to send to device"
                if (
                    shc.config.api
                    and shc.config.api.use_ssl
                    and (not shc.config.external_url or not shc.config.internal_url)
                ):
                    msg += ". Configure internal and external URL in general settings."
                raise core.SmartHomeControllerError(msg) from err

            media_content_id = f"{base_url}{media_content_id}"

        return media_content_id

    # ------------------------ Condition Platform -----------------------------

    @property
    def condition_schema(self) -> typing.Callable[[core.ConfigType], core.ConfigType]:
        return _CONDITION_SCHEMA

    async def async_get_conditions(self, device_id: str) -> list[dict[str, str]]:
        """List device conditions for Media player devices."""
        registry = self.controller.entity_registry
        conditions = []

        # Get all the integrations entities for this device
        for entry in registry.async_entries_for_device(device_id):
            if entry.domain != self.domain:
                continue

            # Add conditions for each entity that belongs to this integration
            base_condition = {
                core.Const.CONF_CONDITION: "device",
                core.Const.CONF_DEVICE_ID: device_id,
                core.Const.CONF_DOMAIN: self.domain,
                core.Const.CONF_ENTITY_ID: entry.entity_id,
            }

            conditions += [
                {**base_condition, core.Const.CONF_TYPE: cond}
                for cond in _CONDITION_TYPES
            ]

        return conditions

    async def async_condition_from_config(
        self, config: core.ConfigType
    ) -> core.ConditionCheckerType:
        """Create a function to test a device condition."""
        condition_type = config[core.Const.CONF_TYPE]
        if condition_type == "is_buffering":
            state = core.Const.STATE_BUFFERING
        elif condition_type == "is_idle":
            state = core.Const.STATE_IDLE
        elif condition_type == "is_off":
            state = core.Const.STATE_OFF
        elif condition_type == "is_on":
            state = core.Const.STATE_ON
        elif condition_type == "is_paused":
            state = core.Const.STATE_PAUSED
        else:  # is_playing
            state = core.Const.STATE_PLAYING

        def test_is_state(
            _shc: core.SmartHomeController, _variables: core.TemplateVarsType
        ) -> bool:
            """Test if an entity is a certain state."""
            return self.state(config[core.Const.ATTR_ENTITY_ID], state)

        return test_is_state

    # ------------------------ Group Platform -----------------------------

    def async_describe_on_off_states(
        self, registry: core.GroupIntegrationRegistry
    ) -> None:
        """Describe group on off states."""
        registry.on_off_states(
            {
                core.Const.STATE_ON,
                core.Const.STATE_PAUSED,
                core.Const.STATE_PLAYING,
                core.Const.STATE_IDLE,
            },
            core.Const.STATE_OFF,
        )

    # ----------------------- Recorder Platform -----------------------------

    def exclude_attributes(self) -> set[str]:
        """Exclude static and token attributes from being recorded in the database."""
        return {
            core.MediaPlayer.ATTR_ENTITY_PICTURE_LOCAL,
            core.Const.ATTR_ENTITY_PICTURE,
            core.MediaPlayer.ATTR_INPUT_SOURCE_LIST,
            core.MediaPlayer.ATTR_MEDIA_POSITION_UPDATED_AT,
            core.MediaPlayer.ATTR_MEDIA_POSITION,
            core.MediaPlayer.ATTR_SOUND_MODE_LIST,
        }

    # ------------------- Reproduce State Platform -----------------------------

    async def async_reproduce_states(
        self,
        states: list[core.State],
        *,
        context: core.Context = None,
        reproduce_options: dict[str, typing.Any] = None,
    ):
        """Reproduce component states."""
        await asyncio.gather(
            *(self._async_reproduce_states(state, context=context) for state in states)
        )

    async def _async_reproduce_states(
        self,
        state: core.State,
        *,
        context: core.Context = None,
    ) -> None:
        """Reproduce component states."""
        shc = self.controller
        domain = self.domain
        cur_state = shc.states.get(state.entity_id)
        features = (
            cur_state.attributes[core.Const.ATTR_SUPPORTED_FEATURES] if cur_state else 0
        )

        async def call_service(service: str, keys: typing.Iterable) -> None:
            """Call service with set of attributes given."""
            data = {"entity_id": state.entity_id}
            for key in keys:
                if key in state.attributes:
                    data[key] = state.attributes[key]

            await shc.services.async_call(
                domain, service, data, blocking=True, context=context
            )

        if state.state == core.Const.STATE_OFF:
            if features & core.MediaPlayer.EntityFeature.TURN_OFF:
                await call_service(core.Const.SERVICE_TURN_OFF, [])
            # entities that are off have no other attributes to restore
            return

        if (
            state.state
            in (
                core.Const.STATE_BUFFERING,
                core.Const.STATE_IDLE,
                core.Const.STATE_ON,
                core.Const.STATE_PAUSED,
                core.Const.STATE_PLAYING,
            )
            and features & core.MediaPlayer.EntityFeature.TURN_ON
        ):
            await call_service(core.Const.SERVICE_TURN_ON, [])

        cur_state = shc.states.get(state.entity_id)
        features = (
            cur_state.attributes[core.Const.ATTR_SUPPORTED_FEATURES] if cur_state else 0
        )

        # First set source & sound mode to match the saved supported features
        input_source = core.MediaPlayer.ATTR_INPUT_SOURCE
        if (
            input_source in state.attributes
            and features & core.MediaPlayer.EntityFeature.SELECT_SOURCE
        ):
            await call_service(
                core.MediaPlayer.SERVICE_SELECT_SOURCE,
                [input_source],
            )

        sound_mode = core.MediaPlayer.ATTR_SOUND_MODE
        if (
            sound_mode in state.attributes
            and features & core.MediaPlayer.EntityFeature.SELECT_SOUND_MODE
        ):
            await call_service(core.MediaPlayer.SERVICE_SELECT_SOUND_MODE, [sound_mode])

        volume_level = core.MediaPlayer.ATTR_MEDIA_VOLUME_LEVEL
        if (
            volume_level in state.attributes
            and features & core.MediaPlayer.EntityFeature.VOLUME_SET
        ):
            await call_service(core.Const.SERVICE_VOLUME_SET, [volume_level])

        volume_muted = core.MediaPlayer.ATTR_MEDIA_VOLUME_MUTED
        if (
            volume_muted in state.attributes
            and features & core.MediaPlayer.EntityFeature.VOLUME_MUTE
        ):
            await call_service(core.Const.SERVICE_VOLUME_MUTE, [volume_muted])

        already_playing = False

        content_type = core.MediaPlayer.ATTR_MEDIA_CONTENT_TYPE
        content_id = core.MediaPlayer.ATTR_MEDIA_CONTENT_ID
        if (content_type in state.attributes) and (content_id in state.attributes):
            if features & core.MediaPlayer.EntityFeature.PLAY_MEDIA:
                await call_service(
                    core.MediaPlayer.SERVICE_PLAY_MEDIA,
                    [content_type, content_id],
                )
            already_playing = True

        if (
            not already_playing
            and state.state in (core.Const.STATE_BUFFERING, core.Const.STATE_PLAYING)
            and features & core.MediaPlayer.EntityFeature.PLAY
        ):
            await call_service(core.Const.SERVICE_MEDIA_PLAY, [])
        elif state.state == core.Const.STATE_IDLE:
            if features & core.MediaPlayer.EntityFeature.STOP:
                await call_service(core.Const.SERVICE_MEDIA_STOP, [])
        elif state.state == core.Const.STATE_PAUSED:
            if features & core.MediaPlayer.EntityFeature.PAUSE:
                await call_service(core.Const.SERVICE_MEDIA_PAUSE, [])

    # ----------------------- Trigger Platform -----------------------------

    @property
    def trigger_schema(self) -> typing.Callable[[core.ConfigType], core.ConfigType]:
        """Return trigger validation schema."""
        TRIGGER_SCHEMA: typing.Final = vol.All(
            vol.Any(
                _MEDIA_PLAYER_TRIGGER_SCHEMA,
                core.DeviceAutomation.TRIGGER_SCHEMA,
            ),
            vol.Schema(
                {vol.Required(core.Const.CONF_DOMAIN): self.domain},
                extra=vol.ALLOW_EXTRA,
            ),
        )
        return TRIGGER_SCHEMA

    async def async_get_triggers(self, device_id: str) -> list[dict[str, str]]:
        """List device triggers for Media player entities."""
        registry = self.controller.entity_registry
        triggers = await core.DeviceAutomation.async_get_triggers(
            self.controller, device_id, self.domain
        )

        # Get all the integration entities for this device
        for entry in registry.async_entries_for_device(device_id):
            if entry.domain != self.domain:
                continue

            # Add triggers for each entity that belongs to this integration
            triggers += [
                {
                    core.Const.CONF_PLATFORM: "device",
                    core.Const.CONF_DEVICE_ID: device_id,
                    core.Const.CONF_DOMAIN: self.domain,
                    core.Const.CONF_ENTITY_ID: entry.entity_id,
                    core.Const.CONF_TYPE: trigger,
                }
                for trigger in _TRIGGER_TYPES
            ]

        return triggers

    async def async_get_trigger_capabilities(
        self, config: core.ConfigType
    ) -> dict[str, vol.Schema]:
        """List trigger capabilities."""
        if config[core.Const.CONF_TYPE] not in _TRIGGER_TYPES:
            return await core.DeviceAutomation.async_get_trigger_capabilities()
        return {
            "extra_fields": vol.Schema(
                {vol.Optional(core.Const.CONF_FOR): _cv.positive_time_period_dict}
            )
        }

    async def async_attach_trigger(
        self,
        config: core.ConfigType,
        action: core.TriggerActionType,
        trigger_info: core.TriggerInfo,
    ) -> core.CallbackType:
        """Attach a trigger."""
        trigger_type = config[core.Const.CONF_TYPE]
        if trigger_type not in _TRIGGER_TYPES:
            return await core.DeviceAutomation.async_attach_trigger(
                self.controller, config, action, trigger_info
            )
        if trigger_type == "buffering":
            to_state = core.Const.STATE_BUFFERING
        elif trigger_type == "idle":
            to_state = core.Const.STATE_IDLE
        elif trigger_type == "turned_off":
            to_state = core.Const.STATE_OFF
        elif trigger_type == "turned_on":
            to_state = core.Const.STATE_ON
        elif trigger_type == "paused":
            to_state = core.Const.STATE_PAUSED
        else:  # "playing"
            to_state = core.Const.STATE_PLAYING

        state_config = {
            core.Const.CONF_PLATFORM: "state",
            core.Const.CONF_ENTITY_ID: config[core.Const.CONF_ENTITY_ID],
            core.Const.CONF_TO: to_state,
        }
        if core.Const.CONF_FOR in config:
            state_config[core.Const.CONF_FOR] = config[core.Const.CONF_FOR]
        state_config = await core.Trigger.async_validate_trigger_config(state_config)
        return await core.Trigger.async_attach_state_trigger(
            self.controller, state_config, action, trigger_info, platform_type="device"
        )


def _rename_keys(
    **keys: typing.Any,
) -> typing.Callable[[dict[str, typing.Any]], dict[str, typing.Any]]:
    """Create validator that renames keys.

    Necessary because the service schema names do not match the command parameters.

    Async friendly.
    """

    def rename(value: dict[str, typing.Any]) -> dict[str, typing.Any]:
        for to_key, from_key in keys.items():
            if from_key in value:
                value[to_key] = value.pop(from_key)
        return value

    return rename
