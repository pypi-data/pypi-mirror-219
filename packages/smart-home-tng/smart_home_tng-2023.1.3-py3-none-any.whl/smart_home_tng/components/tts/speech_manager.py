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

import hashlib
import io
import logging
import mimetypes
import os
import typing

import mutagen
from mutagen import id3

from ... import core

if not typing.TYPE_CHECKING:

    class TextToSpeechComponent:
        pass


if typing.TYPE_CHECKING:
    from .text_to_speech_component import TextToSpeechComponent

_tts: typing.TypeAlias = core.TTS

_LOGGER: typing.Final = logging.getLogger(__name__)


# pylint: disable=unused-variable
class SpeechManager:
    """Representation of a speech store."""

    def __init__(self, owner: TextToSpeechComponent) -> None:
        """Initialize a speech store."""
        self._owner = owner
        self._providers: dict[str, _tts.Provider] = {}

        self._use_cache = _tts.DEFAULT_CACHE
        self._cache_dir = _tts.DEFAULT_CACHE_DIR
        self._time_memory = _tts.DEFAULT_TIME_MEMORY
        self._base_url: str = None
        self._file_cache: dict[str, str] = {}
        self._mem_cache: dict[str, dict[str, str | bytes]] = {}

    @property
    def base_url(self) -> str:
        return self._base_url

    @property
    def owner(self) -> TextToSpeechComponent:
        return self._owner

    @property
    def controller(self) -> core.SmartHomeController:
        return self._owner.controller

    def get_provider(self, provider_domain: str) -> _tts.Provider:
        return self._providers.get(provider_domain)

    async def async_init_cache(
        self, use_cache: bool, cache_dir: str, time_memory: int, base_url: str
    ) -> None:
        """Init config folder and load file cache."""
        self._use_cache = use_cache
        self._time_memory = time_memory
        self._base_url = base_url

        try:
            self._cache_dir = await self.controller.async_add_executor_job(
                _init_tts_cache_dir, self.controller, cache_dir
            )
        except OSError as err:
            raise core.SmartHomeControllerError(f"Can't init cache dir {err}") from err

        try:
            cache_files = await self.controller.async_add_executor_job(
                _get_cache_files, self._cache_dir
            )
        except OSError as err:
            raise core.SmartHomeControllerError(f"Can't read cache dir {err}") from err

        if cache_files:
            self._file_cache.update(cache_files)

    async def async_clear_cache(self) -> None:
        """Read file cache and delete files."""
        self._mem_cache = {}

        def remove_files():
            """Remove files from filesystem."""
            for filename in self._file_cache.values():
                try:
                    os.remove(os.path.join(self._cache_dir, filename))
                except OSError as err:
                    _LOGGER.warning(f"Can't remove cache file '{filename}': {err}")

        await self.controller.async_add_executor_job(remove_files)
        self._file_cache = {}

    @core.callback
    def async_register_engine(
        self, engine: str, provider: _tts.Provider, _config: core.ConfigType
    ) -> None:
        """Register a TTS provider."""
        # pylint: disable=protected-access
        provider._shc = self.controller
        if provider.name is None:
            provider._name = engine
        self._providers[engine] = provider

        self.controller.config._components.add(
            core.Const.PLATFORM_FORMAT.format(
                domain=engine, platform=self._owner.domain
            )
        )

    @core.callback
    def process_options(
        self,
        engine: str,
        language: str = None,
        options: dict = None,
    ) -> tuple[str, dict]:
        """Validate and process options."""
        if (provider := self._providers.get(engine)) is None:
            raise core.SmartHomeControllerError(f"Provider {engine} not found")

        # Languages
        language = language or provider.default_language
        if language is None or language not in provider.supported_languages:
            raise core.SmartHomeControllerError(f"Not supported language {language}")

        # Options
        if provider.default_options and options:
            merged_options = provider.default_options.copy()
            merged_options.update(options)
            options = merged_options
        options = options or provider.default_options

        if options is not None:
            invalid_opts = [
                opt_name
                for opt_name in options.keys()
                if opt_name not in (provider.supported_options or [])
            ]
            if invalid_opts:
                raise core.SmartHomeControllerError(
                    f"Invalid options found: {invalid_opts}"
                )

        return language, options

    async def async_get_url_path(
        self,
        engine: str,
        message: str,
        cache: bool = None,
        language: str = None,
        options: dict = None,
    ) -> str:
        """Get URL for play message.

        This method is a coroutine.
        """
        language, options = self.process_options(engine, language, options)
        options_key = _hash_options(options) if options else "-"
        msg_hash = hashlib.sha1(bytes(message, "utf-8")).hexdigest()  # nosec
        use_cache = cache if cache is not None else self._use_cache

        key = _tts.KEY_PATTERN.format(
            msg_hash, language.replace("_", "-"), options_key, engine
        ).lower()

        # Is speech already in memory
        if key in self._mem_cache:
            filename = typing.cast(str, self._mem_cache[key][_tts.MEM_CACHE_FILENAME])
        # Is file store in file cache
        elif use_cache and key in self._file_cache:
            filename = self._file_cache[key]
            self.controller.async_create_task(self.async_file_to_mem(key))
        # Load speech from provider into memory
        else:
            filename = await self.async_get_tts_audio(
                engine, key, message, use_cache, language, options
            )

        return f"/api/tts_proxy/{filename}"

    async def async_get_tts_audio(
        self,
        engine: str,
        key: str,
        message: str,
        cache: bool,
        language: str,
        options: dict,
    ) -> str:
        """Receive TTS and store for view in cache.

        This method is a coroutine.
        """
        provider = self._providers[engine]
        extension, data = await provider.async_get_tts_audio(message, language, options)

        if data is None or extension is None:
            raise core.SmartHomeControllerError(f"No TTS from {engine} for '{message}'")

        # Create file infos
        filename = f"{key}.{extension}".lower()

        # Validate filename
        if not _tts.RE_VOICE_FILE.match(filename):
            raise core.SmartHomeControllerError(
                f"TTS filename '{filename}' from {engine} is invalid!"
            )

        # Save to memory
        data = self.write_tags(filename, data, provider, message, language, options)
        self._async_store_to_memcache(key, filename, data)

        if cache:
            self.controller.async_create_task(
                self.async_save_tts_audio(key, filename, data)
            )

        return filename

    async def async_save_tts_audio(self, key: str, filename: str, data: bytes) -> None:
        """Store voice data to file and file_cache.

        This method is a coroutine.
        """
        voice_file = os.path.join(self._cache_dir, filename)

        def save_speech() -> None:
            """Store speech to filesystem."""
            with open(voice_file, "wb") as speech:
                speech.write(data)

        try:
            await self.controller.async_add_executor_job(save_speech)
            self._file_cache[key] = filename
        except OSError as err:
            _LOGGER.error(f"Can't write {filename}: {err}")

    async def async_file_to_mem(self, key: str) -> None:
        """Load voice from file cache into memory.

        This method is a coroutine.
        """
        if not (filename := self._file_cache.get(key)):
            raise core.SmartHomeControllerError(f"Key {key} not in file cache!")

        voice_file = os.path.join(self._cache_dir, filename)

        def load_speech() -> bytes:
            """Load a speech from filesystem."""
            with open(voice_file, "rb") as speech:
                return speech.read()

        try:
            data = await self.controller.async_add_executor_job(load_speech)
        except OSError as err:
            del self._file_cache[key]
            raise core.SmartHomeControllerError(f"Can't read {voice_file}") from err

        self._async_store_to_memcache(key, filename, data)

    @core.callback
    def _async_store_to_memcache(self, key: str, filename: str, data: bytes) -> None:
        """Store data to memcache and set timer to remove it."""
        self._mem_cache[key] = {
            _tts.MEM_CACHE_FILENAME: filename,
            _tts.MEM_CACHE_VOICE: data,
        }

        @core.callback
        def async_remove_from_mem() -> None:
            """Cleanup memcache."""
            self._mem_cache.pop(key, None)

        self.controller.call_later(self._time_memory, async_remove_from_mem)

    async def async_read_tts(self, filename: str) -> tuple[str, bytes]:
        """Read a voice file and return binary.

        This method is a coroutine.
        """
        if not (record := _tts.RE_VOICE_FILE.match(filename.lower())):
            raise core.SmartHomeControllerError("Wrong tts file format!")

        key = _tts.KEY_PATTERN.format(
            record.group(1), record.group(2), record.group(3), record.group(4)
        )

        if key not in self._mem_cache:
            if key not in self._file_cache:
                raise core.SmartHomeControllerError(f"{key} not in cache!")
            await self.async_file_to_mem(key)

        content, _ = mimetypes.guess_type(filename)
        return content, typing.cast(bytes, self._mem_cache[key][_tts.MEM_CACHE_VOICE])

    @staticmethod
    def write_tags(
        filename: str,
        data: bytes,
        provider: _tts.Provider,
        message: str,
        language: str,
        options: dict,
    ) -> bytes:
        """Write ID3 tags to file.

        Async friendly.
        """

        data_bytes = io.BytesIO(data)
        data_bytes.name = filename
        data_bytes.seek(0)

        album = provider.name
        artist = language

        if message.startswith("<speak>"):
            message = message.replace("<speak>", "")
            message = message.replace("</speak>", "")

        if options is not None and (voice := options.get("voice")) is not None:
            artist = voice

        try:
            tts_file = mutagen.File(data_bytes)
            if tts_file is not None:
                if not tts_file.tags:
                    tts_file.add_tags()
                if isinstance(tts_file.tags, id3.ID3):
                    tts_file["artist"] = id3.TextFrame(encoding=3, text=artist)
                    tts_file["album"] = id3.TextFrame(encoding=3, text=album)
                    tts_file["title"] = id3.TextFrame(encoding=3, text=message)
                else:
                    tts_file["artist"] = artist
                    tts_file["album"] = album
                    tts_file["title"] = message
                tts_file.save(data_bytes)
        except mutagen.MutagenError as err:
            _LOGGER.error(f"ID3 tag error: {err}")

        return data_bytes.getvalue()


def _hash_options(options: dict) -> str:
    """Hashes an options dictionary."""
    opts_hash = hashlib.blake2s(digest_size=5)
    for key, value in sorted(options.items()):
        opts_hash.update(str(key).encode())
        opts_hash.update(str(value).encode())

    return opts_hash.hexdigest()


def _init_tts_cache_dir(shc: core.SmartHomeController, cache_dir: str) -> str:
    """Init cache folder."""
    if not os.path.isabs(cache_dir):
        cache_dir = shc.config.path(cache_dir)
    if not os.path.isdir(cache_dir):
        _LOGGER.info(f"Create cache dir {cache_dir}")
        os.mkdir(cache_dir)
    return cache_dir


def _get_cache_files(cache_dir: str) -> dict[str, str]:
    """Return a dict of given engine files."""
    cache = {}

    folder_data = os.listdir(cache_dir)
    for file_data in folder_data:
        if record := _tts.RE_VOICE_FILE.match(file_data):
            key = _tts.KEY_PATTERN.format(
                record.group(1), record.group(2), record.group(3), record.group(4)
            )
            cache[key.lower()] = file_data.lower()
    return cache
