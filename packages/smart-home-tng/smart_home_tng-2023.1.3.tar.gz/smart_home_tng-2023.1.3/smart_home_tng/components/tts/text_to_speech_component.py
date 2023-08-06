"""
TextToSpeech (TTS) Component for Smart Home - The Next Generation.

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
import logging
import pathlib
import typing

import voluptuous as vol
import yarl

from ... import core
from .speech_manager import SpeechManager
from .text_to_speech_media_source import TextToSpeechMediaSource
from .text_to_speech_notification_service import TextToSpeechNotificationService
from .text_to_speech_url_view import TextToSpeechUrlView
from .text_to_speech_view import TextToSpeechView

_cv: typing.TypeAlias = core.ConfigValidation
_tts: typing.TypeAlias = core.TTS

_LOGGER: typing.Final = logging.getLogger(__name__)
_SCHEMA_SERVICE_SAY: typing.Final = vol.Schema(
    {
        vol.Required(_tts.ATTR_MESSAGE): _cv.string,
        vol.Optional(_tts.ATTR_CACHE): _cv.boolean,
        vol.Required(core.Const.ATTR_ENTITY_ID): _cv.comp_entity_ids,
        vol.Optional(_tts.ATTR_LANGUAGE): _cv.string,
        vol.Optional(_tts.ATTR_OPTIONS): dict,
    }
)
_SCHEMA_SERVICE_CLEAR_CACHE: typing.Final = vol.Schema({})


# pylint: disable=unused-variable
class TextToSpeechComponent(
    core.TTS.Component, core.MediaSourcePlatform, core.NotifyPlatform
):
    """Provide functionality for TTS."""

    def __init__(self, path: typing.Iterable[str]):
        super().__init__(path)
        self._tts: SpeechManager = None
        self._base_url: str = None
        self._domain_mp: str = None
        self._supported_platforms = frozenset(
            [core.Platform.MEDIA_SOURCE, core.Platform.NOTIFY]
        )

    @property
    def tts(self) -> SpeechManager:
        return self._tts

    @property
    def platform_schema(self) -> typing.Callable[[core.ConfigType], core.ConfigType]:
        return core.TTS.PLATFORM_SCHEMA

    @property
    def platform_schema_base(
        self,
    ) -> typing.Callable[[core.ConfigType], core.ConfigType]:
        return core.TTS.PLATFORM_SCHEMA_BASE

    async def async_setup(self, config: core.ConfigType) -> bool:
        """Set up TTS."""
        if not await super().async_setup(config):
            return False

        self._tts = SpeechManager(self)
        try:
            self._domain_mp = self.controller.components.media_player.domain
            conf = config[self.domain][0] if config.get(self.domain, []) else {}
            use_cache: bool = conf.get(_tts.CONF_CACHE, _tts.DEFAULT_CACHE)
            cache_dir: str = conf.get(_tts.CONF_CACHE_DIR, _tts.DEFAULT_CACHE_DIR)
            time_memory: int = conf.get(_tts.CONF_TIME_MEMORY, _tts.DEFAULT_TIME_MEMORY)
            base_url: str = conf.get(_tts.CONF_BASE_URL)
            if base_url is not None:
                _LOGGER.warning(
                    "TTS base_url option is deprecated. Configure internal/external URL instead"
                )
            self._base_url = base_url or self.get_base_url()

            await self._tts.async_init_cache(
                use_cache, cache_dir, time_memory, self._base_url
            )
        except (core.SmartHomeControllerError, KeyError):
            _LOGGER.exception("Error on cache init")
            return False

        self.controller.http.register_view(TextToSpeechView(self._tts))
        self.controller.http.register_view(TextToSpeechUrlView(self._tts))

        # Load service descriptions from tts/services.yaml
        services_yaml = pathlib.Path(__file__).parent / "services.yaml"
        services_dict = typing.cast(
            dict,
            await self.controller.async_add_executor_job(
                core.YamlLoader.load_yaml, str(services_yaml)
            ),
        )
        media_source: core.MediaSourceComponent = (
            self.controller.components.media_source
        )

        async def async_setup_platform(
            p_type: str,
            p_config: core.ConfigType = None,
            discovery_info: core.DiscoveryInfoType = None,
        ) -> None:
            """Set up a TTS platform."""
            if p_config is None:
                p_config = {}

            platform = await self.controller.setup.async_prepare_setup_platform(
                config, self.domain, p_type
            )
            if not isinstance(platform, _tts.Platform):
                return

            try:
                provider = await platform.async_get_tts_engine(p_config, discovery_info)

                if provider is None:
                    _LOGGER.error(f"Error setting up platform {p_type}", p_type)
                    return

                self._tts.async_register_engine(p_type, provider, p_config)
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception(f"Error setting up platform: {p_type}")
                return

            async def async_say_handle(service: core.ServiceCall) -> None:
                """Service handle for say."""
                entity_ids = service.data[core.Const.ATTR_ENTITY_ID]
                message = service.data[_tts.ATTR_MESSAGE]
                cache = service.data.get(_tts.ATTR_CACHE)
                language = service.data.get(_tts.ATTR_LANGUAGE)
                options = service.data.get(_tts.ATTR_OPTIONS)

                self._tts.process_options(p_type, language, options)
                params = {
                    "message": message,
                }
                if cache is not None:
                    params["cache"] = "true" if cache else "false"
                if language is not None:
                    params["language"] = language
                if options is not None:
                    params.update(options)

                await self.controller.services.async_call(
                    self._domain_mp,
                    core.MediaPlayer.SERVICE_PLAY_MEDIA,
                    {
                        core.Const.ATTR_ENTITY_ID: entity_ids,
                        core.MediaPlayer.ATTR_MEDIA_CONTENT_ID: (
                            media_source.generate_media_source_id(
                                self.domain,
                                str(yarl.URL.build(path=p_type, query=params)),
                            )
                        ),
                        core.MediaPlayer.ATTR_MEDIA_CONTENT_TYPE: core.MediaPlayer.MediaType.MUSIC,
                        core.MediaPlayer.ATTR_MEDIA_ANNOUNCE: False,
                        core.MediaPlayer.ATTR_MEDIA_EXTRA: {
                            "thumb": f"https://brands.home-assistant.io/_/{p_type}/logo.png",
                            "metadata": {
                                "metadataType": 3,
                                "artist": provider.name or p_type,
                            },
                        },
                    },
                    blocking=True,
                    context=service.context,
                )

            service_name: str = p_config.get(
                _tts.CONF_SERVICE_NAME, f"{p_type}_{_tts.SERVICE_SAY}"
            )
            self.controller.services.async_register(
                self.domain, service_name, async_say_handle, schema=_SCHEMA_SERVICE_SAY
            )

            # Register the service description
            service_desc = {
                core.Const.CONF_NAME: f"Say an TTS message with {p_type}",
                core.Const.CONF_DESCRIPTION: (
                    "Say something using text-to-speech on a media "
                    + f"player with {p_type}."
                ),
                core.Const.CONF_FIELDS: services_dict[_tts.SERVICE_SAY][
                    _tts.CONF_FIELDS
                ],
            }
            core.Service.async_set_service_schema(
                self.controller, self.domain, service_name, service_desc
            )

        setup_tasks = [
            asyncio.create_task(async_setup_platform(p_type, p_config))
            for p_type, p_config in self.controller.setup.config_per_platform(
                config, self.domain
            )
            if p_type is not None
        ]

        if setup_tasks:
            await asyncio.wait(setup_tasks)

        async def async_platform_discovered(platform, info):
            """Handle for discovered platform."""
            await async_setup_platform(platform, discovery_info=info)

        self.controller.setup.async_listen_platform(
            self.domain, async_platform_discovered
        )

        async def async_clear_cache_handle(_service: core.ServiceCall) -> None:
            """Handle clear cache service call."""
            await self._tts.async_clear_cache()

        self.controller.services.async_register(
            self.domain,
            _tts.SERVICE_CLEAR_CACHE,
            async_clear_cache_handle,
            schema=_SCHEMA_SERVICE_CLEAR_CACHE,
        )

        return True

    def get_base_url(self) -> str:
        """Get base URL."""
        if self._tts is None:
            # not configured
            return self.controller.get_url()
        if self._base_url is None:
            self._base_url = self.controller.get_url()
        return self._base_url

    # ----------------- Media Source Platform -----------------------

    async def async_get_media_source(self) -> core.MediaSource:
        """Set up tts media source."""
        return TextToSpeechMediaSource(self)

    # --------------------- Notify Platform -------------------------

    async def async_get_service(
        self, config: core.ConfigType, _discovery_info: core.DiscoveryInfoType = None
    ) -> core.BaseNotificationService:
        """Return the notify service."""

        return TextToSpeechNotificationService(self, config)
