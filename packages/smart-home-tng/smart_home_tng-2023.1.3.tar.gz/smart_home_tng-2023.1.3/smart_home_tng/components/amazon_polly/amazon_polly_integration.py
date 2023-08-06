"""
Amazon Polly Integration for Smart Home - The Next Generation.

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

import logging
import typing

import boto3
import botocore.client
import voluptuous as vol

from ... import core
from .amazon_polly_provider import AmazonPollyProvider
from .const import Const

_cv: typing.TypeAlias = core.ConfigValidation
_tts: typing.TypeAlias = core.TTS
_LOGGER: typing.Final = logging.getLogger(__name__)

PLATFORM_SCHEMA: typing.Final = _tts.PLATFORM_SCHEMA.extend(
    {
        vol.Optional(Const.CONF_REGION, default=Const.DEFAULT_REGION): vol.In(
            Const.SUPPORTED_REGIONS
        ),
        vol.Inclusive(
            Const.CONF_ACCESS_KEY_ID, core.Const.ATTR_CREDENTIALS
        ): _cv.string,
        vol.Inclusive(
            Const.CONF_SECRET_ACCESS_KEY, core.Const.ATTR_CREDENTIALS
        ): _cv.string,
        vol.Exclusive(
            core.Const.CONF_PROFILE_NAME, core.Const.ATTR_CREDENTIALS
        ): _cv.string,
        vol.Optional(Const.CONF_VOICE, default=Const.DEFAULT_VOICE): vol.In(
            Const.SUPPORTED_VOICES
        ),
        vol.Optional(Const.CONF_ENGINE, default=Const.DEFAULT_ENGINE): vol.In(
            Const.SUPPORTED_ENGINES
        ),
        vol.Optional(
            Const.CONF_OUTPUT_FORMAT, default=Const.DEFAULT_OUTPUT_FORMAT
        ): vol.In(Const.SUPPORTED_OUTPUT_FORMATS),
        vol.Optional(Const.CONF_SAMPLE_RATE): vol.All(
            _cv.string, vol.In(Const.SUPPORTED_SAMPLE_RATES)
        ),
        vol.Optional(Const.CONF_TEXT_TYPE, default=Const.DEFAULT_TEXT_TYPE): vol.In(
            Const.SUPPORTED_TEXT_TYPES
        ),
    }
)


# pylint: disable=unused-variable
class AmazonPollyIntegration(core.SmartHomeControllerComponent, core.TTS.Platform):
    """Support for Amazon Polly integration."""

    def __init__(self, path: typing.Iterable[str]):
        super().__init__(path)
        self._supported_platforms = frozenset([core.Platform.TTS])

    @property
    def platform_config_schema(
        self,
    ) -> typing.Callable[[core.ConfigType], core.ConfigType]:
        if self._current_platform == core.Platform.TTS:
            return PLATFORM_SCHEMA
        return super().platform_config_schema

    async def async_get_tts_engine(
        self, config: core.ConfigType, discovery_info: core.DiscoveryInfoType = None
    ) -> _tts.Provider:
        # pylint: disable=unused-argument

        """Set up Amazon Polly speech component."""
        output_format: str = config[Const.CONF_OUTPUT_FORMAT]
        sample_rate: str = config.get(
            Const.CONF_SAMPLE_RATE, Const.DEFAULT_SAMPLE_RATES[output_format]
        )
        if sample_rate not in Const.SUPPORTED_SAMPLE_RATES_MAP[output_format]:
            _LOGGER.error(
                f"{sample_rate} is not a valid sample rate for {output_format}"
            )
            return None

        config[Const.CONF_SAMPLE_RATE] = sample_rate

        profile: str = config.get(core.Const.CONF_PROFILE_NAME)

        if bool(profile):
            boto3.setup_default_session(profile_name=profile)

        aws_config = {
            Const.CONF_REGION: config[Const.CONF_REGION],
            Const.CONF_ACCESS_KEY_ID: config.get(Const.CONF_ACCESS_KEY_ID),
            Const.CONF_SECRET_ACCESS_KEY: config.get(Const.CONF_SECRET_ACCESS_KEY),
            Const.CONF_CONFIG: botocore.client.Config(
                connect_timeout=Const.AWS_CONF_CONNECT_TIMEOUT,
                read_timeout=Const.AWS_CONF_READ_TIMEOUT,
                max_pool_connections=Const.AWS_CONF_MAX_POOL_CONNECTIONS,
            ),
        }

        del config[Const.CONF_REGION]
        del config[Const.CONF_ACCESS_KEY_ID]
        del config[Const.CONF_SECRET_ACCESS_KEY]

        polly_client = boto3.client("polly", **aws_config)

        supported_languages: list[str] = []

        all_voices: dict[str, dict[str, str]] = {}

        all_voices_req = await self.controller.async_add_executor_job(
            polly_client.describe_voices
        )

        for voice in all_voices_req.get("Voices", []):
            voice_id: str = voice.get("Id")
            if voice_id is None:
                continue
            all_voices[voice_id] = voice
            language_code: str = voice.get("LanguageCode")
            if bool(language_code) and language_code not in supported_languages:
                supported_languages.append(str(language_code))

        return AmazonPollyProvider(
            polly_client, config, supported_languages, all_voices
        )
