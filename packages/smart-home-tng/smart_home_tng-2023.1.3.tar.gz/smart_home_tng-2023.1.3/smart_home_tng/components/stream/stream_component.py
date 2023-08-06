"""
Stream Component for Smart Home - The Next Generation.

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
import copy
import logging
import re
import typing

import voluptuous as vol

from ... import core
from .const import Const
from .hls_init_view import HlsInitView
from .hls_master_playlist_view import HlsMasterPlaylistView
from .hls_part_view import HlsPartView
from .hls_playlist_view import HlsPlaylistView
from .hls_segment_view import HlsSegmentView
from .hls_stream_output import HlsStreamOutput
from .recorder_output import RecorderOutput
from .stream import Stream
from .stream_output import StreamOutput
from .stream_settings import STREAM_SETTINGS_NON_LL_HLS, StreamSettings

_cv: typing.TypeAlias = core.ConfigValidation

_LOGGER: typing.Final = logging.getLogger(__name__)
_DOMAIN_SCHEMA: typing.Final = vol.Schema(
    {
        vol.Optional(Const.CONF_LL_HLS, default=True): _cv.boolean,
        vol.Optional(Const.CONF_SEGMENT_DURATION, default=6): vol.All(
            _cv.positive_float, vol.Range(min=2, max=10)
        ),
        vol.Optional(Const.CONF_PART_DURATION, default=1): vol.All(
            _cv.positive_float, vol.Range(min=0.2, max=1.5)
        ),
    }
)
_STREAM_SOURCE_REDACT_PATTERN: typing.Final = [
    (re.compile(r"//.*:.*@"), "//****:****@"),
    (re.compile(r"\?auth=.*"), "?auth=****"),
]


# pylint: disable=unused-variable
class StreamComponent(core.StreamComponent):
    """Provide functionality to stream video source.

    Components use create_stream with a stream source (e.g. an rtsp url) to create
    a new Stream object. Stream manages:
    - Background work to fetch and decode a stream
    - Desired output formats
    - Home Assistant URLs for viewing a stream
    - Access tokens for URLs for viewing a stream

    A Stream consists of a background worker, and one or more output formats each
    with their own idle timeout managed by the stream component. When an output
    format is no longer in use, the stream component will expire it. When there
    are no active output formats, the background worker is shut down and access
    tokens are expired. Alternatively, a Stream can be configured with keepalive
    to always keep workers active.
    """

    def __init__(self, path: typing.Iterable[str]):
        super().__init__(path)
        self._stream_settings: StreamSettings = None
        self._endpoints: dict[str, str] = {}
        self._streams: list[Stream] = []
        self._providers = dict[str, type[StreamOutput]]()
        self._providers[Const.HLS_PROVIDER] = HlsStreamOutput
        self._providers[Const.RECORDER_PROVIDER] = RecorderOutput

    @property
    def streams(self) -> typing.Iterable[Stream]:
        return iter(self._streams)

    async def async_validate_config(self, config: core.ConfigType) -> core.ConfigType:
        """Validate configuration."""
        schema = vol.Schema(
            {
                self.domain: _DOMAIN_SCHEMA,
            },
            extra=vol.ALLOW_EXTRA,
        )
        return schema(config)

    async def async_setup(self, config: core.ConfigType) -> bool:
        """Set up stream."""
        if not await super().async_setup(config):
            return False

        # Drop libav log messages if stream logging is above DEBUG
        _filter_libav_logging()

        conf = _DOMAIN_SCHEMA(config.get(self.domain, {}))
        if conf[Const.CONF_LL_HLS]:
            assert isinstance(conf[Const.CONF_SEGMENT_DURATION], float)
            assert isinstance(conf[Const.CONF_PART_DURATION], float)
            self._stream_settings = StreamSettings(
                ll_hls=True,
                min_segment_duration=conf[Const.CONF_SEGMENT_DURATION]
                - Const.SEGMENT_DURATION_ADJUSTER,
                part_target_duration=conf[Const.CONF_PART_DURATION],
                hls_advance_part_limit=max(int(3 / conf[Const.CONF_PART_DURATION]), 3),
                hls_part_timeout=2 * conf[Const.CONF_PART_DURATION],
            )
        else:
            self._stream_settings = STREAM_SETTINGS_NON_LL_HLS

        # Set up api endpoints.
        shc = self.controller
        shc.http.register_view(HlsPlaylistView(self))
        shc.http.register_view(HlsSegmentView(self))
        shc.http.register_view(HlsInitView(self))
        shc.http.register_view(HlsMasterPlaylistView(self))
        shc.http.register_view(HlsPartView(self))
        self._endpoints[Const.HLS_PROVIDER] = "/api/hls/{}/master_playlist.m3u8"

        self.controller.bus.async_listen_once(core.Const.EVENT_SHC_STOP, self._shutdown)

        return True

    def get_provider_class(self, provider: str) -> type[StreamOutput]:
        return self._providers.get(provider)

    async def _shutdown(self, _event: core.Event) -> None:
        """Stop all stream workers."""
        for stream in self._streams:
            stream.keepalive = False
        if awaitables := [
            asyncio.create_task(stream.stop()) for stream in self._streams
        ]:
            await asyncio.wait(awaitables)
        _LOGGER.debug("Stopped stream workers")

    def create_stream(
        self,
        stream_source: str,
        options: typing.Mapping[str, str | bool | float],
        stream_label: str = None,
    ) -> core.StreamBase:
        """Create a stream with the specified identfier based on the source url.

        The stream_source is typically an rtsp url (though any url accepted by ffmpeg is fine) and
        options (see STREAM_OPTIONS_SCHEMA) are converted and passed into pyav / ffmpeg.

        The stream_label is a string used as an additional message in logging.
        """

        if self.domain not in self._shc.config.components:
            raise core.SmartHomeControllerError("Stream integration is not set up.")

        # Convert extra stream options into PyAV options and stream settings
        pyav_options, stream_settings = self._convert_stream_options(options)
        # For RTSP streams, prefer TCP
        if isinstance(stream_source, str) and stream_source[:7] == "rtsp://":
            pyav_options = {
                "rtsp_flags": "prefer_tcp",
                "stimeout": "5000000",
                **pyav_options,
            }

        stream = Stream(
            self,
            stream_source,
            pyav_options=pyav_options,
            stream_settings=stream_settings,
            stream_label=stream_label,
        )
        self._streams.append(stream)
        return stream

    def _convert_stream_options(
        self, stream_options: typing.Mapping[str, str | bool | float]
    ) -> tuple[dict[str, str], StreamSettings]:
        """Convert options from stream options into PyAV options and stream settings."""
        stream_settings = copy.copy(self._stream_settings)
        pyav_options: dict[str, str] = {}
        try:
            stream_options = _STREAM_OPTIONS_SCHEMA(stream_options)
        except vol.Invalid as exc:
            raise core.SmartHomeControllerError("Invalid stream options") from exc

        if extra_wait_time := stream_options.get(Const.CONF_EXTRA_PART_WAIT_TIME):
            stream_settings.hls_part_timeout += extra_wait_time
        if rtsp_transport := stream_options.get(Const.CONF_RTSP_TRANSPORT):
            assert isinstance(rtsp_transport, str)
            # The PyAV options currently match the stream CONF constants, but this
            # will not necessarily always be the case, so they are hard coded here
            pyav_options["rtsp_transport"] = rtsp_transport
        if stream_options.get(Const.CONF_USE_WALLCLOCK_AS_TIMESTAMPS):
            pyav_options["use_wallclock_as_timestamps"] = "1"

        return pyav_options, stream_settings

    def redact_credentials(self, data: str) -> str:
        """Redact credentials from string data."""
        for pattern, repl in _STREAM_SOURCE_REDACT_PATTERN:
            data = pattern.sub(repl, data)
        return data


def _filter_libav_logging() -> None:
    """Filter libav logging to only log when the stream logger is at DEBUG."""

    def libav_filter(_record: logging.LogRecord) -> bool:
        return logging.getLogger(__name__).isEnabledFor(logging.DEBUG)

    for logging_namespace in (
        "libav.NULL",
        "libav.h264",
        "libav.hevc",
        "libav.hls",
        "libav.mp4",
        "libav.mpegts",
        "libav.rtsp",
        "libav.tcp",
        "libav.tls",
    ):
        logging.getLogger(logging_namespace).addFilter(libav_filter)

    # Set log level to error for libav.mp4
    logging.getLogger("libav.mp4").setLevel(logging.ERROR)
    # Suppress "deprecated pixel format" WARNING
    logging.getLogger("libav.swscaler").setLevel(logging.ERROR)


_STREAM_OPTIONS_SCHEMA: typing.Final = vol.Schema(
    {
        vol.Optional(Const.CONF_RTSP_TRANSPORT): vol.In(Const.RTSP_TRANSPORTS),
        vol.Optional(Const.CONF_USE_WALLCLOCK_AS_TIMESTAMPS): bool,
        vol.Optional(Const.CONF_EXTRA_PART_WAIT_TIME): _cv.positive_float,
    }
)
