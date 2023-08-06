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

import abc
import functools as ft
import re
import typing

import voluptuous as vol
import yarl

from . import helpers
from .config_type import ConfigType
from .config_validation import ConfigValidation as _cv
from .const import Const
from .discovery_info_type import DiscoveryInfoType
from .platform_implementation import PlatformImplementation
from .smart_home_controller_component import SmartHomeControllerComponent


if not typing.TYPE_CHECKING:

    class SmartHomeController:
        pass


if typing.TYPE_CHECKING:
    from .smart_home_controller import SmartHomeController


TtsAudioType = tuple[typing.Optional[str], typing.Optional[bytes]]

_ATTR_CACHE: typing.Final = "cache"
_ATTR_LANGUAGE: typing.Final = "language"
_ATTR_MESSAGE: typing.Final = "message"
_ATTR_OPTIONS: typing.Final = "options"
_ATTR_PLATFORM: typing.Final = "platform"

_BASE_URL_KEY: typing.Final = "tts_base_url"

_CONF_BASE_URL: typing.Final = "base_url"
_CONF_CACHE: typing.Final = "cache"
_CONF_CACHE_DIR: typing.Final = "cache_dir"
_CONF_LANG: typing.Final = "language"
_CONF_SERVICE_NAME: typing.Final = "service_name"
_CONF_TIME_MEMORY: typing.Final = "time_memory"

_CONF_FIELDS: typing.Final = "fields"

_DEFAULT_CACHE: typing.Final = True
_DEFAULT_CACHE_DIR: typing.Final = "tts"
_DEFAULT_TIME_MEMORY: typing.Final = 300

_MEM_CACHE_FILENAME: typing.Final = "filename"
_MEM_CACHE_VOICE: typing.Final = "voice"

_SERVICE_CLEAR_CACHE: typing.Final = "clear_cache"
_SERVICE_SAY: typing.Final = "say"

_RE_VOICE_FILE: typing.Final = re.compile(
    r"([a-f0-9]{40})_([^_]+)_([^_]+)_([a-z_]+)\.[a-z0-9]{3,4}"
)
_KEY_PATTERN: typing.Final = "{0}_{1}_{2}_{3}"


def _deprecated_platform(value):
    """Validate if platform is deprecated."""
    if value == "google":
        raise vol.Invalid(
            "google tts service has been renamed to google_translate,"
            + " please update your configuration."
        )
    return value


def valid_base_url(value: str) -> str:
    """Validate base url, return value."""
    url = yarl.URL(_cv.url(value))

    if url.path != "/":
        raise vol.Invalid("Path should be empty")

    return helpers.normalize_url(value)


_PLATFORM_SCHEMA: typing.Final = _cv.PLATFORM_SCHEMA.extend(
    {
        vol.Required(Const.CONF_PLATFORM): vol.All(_cv.string, _deprecated_platform),
        vol.Optional(_CONF_CACHE, default=_DEFAULT_CACHE): _cv.boolean,
        vol.Optional(_CONF_CACHE_DIR, default=_DEFAULT_CACHE_DIR): _cv.string,
        vol.Optional(_CONF_TIME_MEMORY, default=_DEFAULT_TIME_MEMORY): vol.All(
            vol.Coerce(int), vol.Range(min=60, max=57600)
        ),
        vol.Optional(_CONF_BASE_URL): valid_base_url,
        vol.Optional(_CONF_SERVICE_NAME): _cv.string,
    }
)
_PLATFORM_SCHEMA_BASE: typing.Final = _cv.PLATFORM_SCHEMA_BASE.extend(
    _PLATFORM_SCHEMA.schema
)


# pylint: disable=unused-variable
class TtsProvider:
    """Represent a single TTS provider."""

    def __init__(self, name: str = None, shc: SmartHomeController = None):
        self._shc = shc
        self._name = name

    @property
    def controller(self) -> SmartHomeController:
        return self._shc

    @property
    def name(self) -> str:
        return self._name

    @property
    def default_language(self) -> str:
        """Return the default language."""
        return None

    @property
    def supported_languages(self) -> list[str]:
        """Return a list of supported languages."""
        return None

    @property
    def supported_options(self) -> list[str]:
        """Return a list of supported options like voice, emotionen."""
        return None

    @property
    def default_options(self) -> dict[str, typing.Any]:
        """Return a dict include default options."""
        return None

    def get_tts_audio(
        self, message: str, language: str, options: dict = None
    ) -> TtsAudioType:
        """Load tts audio file from provider."""
        raise NotImplementedError()

    async def async_get_tts_audio(
        self, message: str, language: str, options: dict = None
    ) -> TtsAudioType:
        """Load tts audio file from provider.

        Return a tuple of file extension and data as bytes.
        """
        return await self.controller.async_add_executor_job(
            ft.partial(self.get_tts_audio, message, language, options=options)
        )


# pylint: disable=unused-variable, invalid-name
class TTS:
    """Text To Speech (TTS) namespace."""

    ATTR_CACHE: typing.Final = _ATTR_CACHE
    ATTR_LANGUAGE: typing.Final = _ATTR_LANGUAGE
    ATTR_MESSAGE: typing.Final = _ATTR_MESSAGE
    ATTR_OPTIONS: typing.Final = _ATTR_OPTIONS
    ATTR_PLATFORM: typing.Final = _ATTR_PLATFORM

    BASE_URL_KEY: typing.Final = _BASE_URL_KEY

    CONF_BASE_URL: typing.Final = _CONF_BASE_URL
    CONF_CACHE: typing.Final = _CONF_CACHE
    CONF_CACHE_DIR: typing.Final = _CONF_CACHE_DIR
    CONF_LANG: typing.Final = _CONF_LANG
    CONF_SERVICE_NAME: typing.Final = _CONF_SERVICE_NAME
    CONF_TIME_MEMORY: typing.Final = _CONF_TIME_MEMORY

    CONF_FIELDS: typing.Final = _CONF_FIELDS

    DEFAULT_CACHE: typing.Final = _DEFAULT_CACHE
    DEFAULT_CACHE_DIR: typing.Final = _DEFAULT_CACHE_DIR
    DEFAULT_TIME_MEMORY: typing.Final = _DEFAULT_TIME_MEMORY

    MEM_CACHE_FILENAME: typing.Final = _MEM_CACHE_FILENAME
    MEM_CACHE_VOICE: typing.Final = _MEM_CACHE_VOICE

    SERVICE_CLEAR_CACHE: typing.Final = _SERVICE_CLEAR_CACHE
    SERVICE_SAY: typing.Final = _SERVICE_SAY

    RE_VOICE_FILE: typing.Final = _RE_VOICE_FILE
    KEY_PATTERN: typing.Final = _KEY_PATTERN

    PLATFORM_SCHEMA: typing.Final = _PLATFORM_SCHEMA
    PLATFORM_SCHEMA_BASE: typing.Final = _PLATFORM_SCHEMA_BASE

    AudioType: typing.TypeAlias = TtsAudioType
    Provider: typing.TypeAlias = TtsProvider

    class Platform(PlatformImplementation):
        """Required base class for TTS platform implementations."""

        @abc.abstractmethod
        async def async_get_tts_engine(
            self, config: ConfigType, discovery_info: DiscoveryInfoType = None
        ) -> TtsProvider:
            """Set up TTS component."""

    class Component(SmartHomeControllerComponent):
        """Required base class for TTS component."""

        @abc.abstractmethod
        def get_base_url(self) -> str:
            """Get base URL."""
