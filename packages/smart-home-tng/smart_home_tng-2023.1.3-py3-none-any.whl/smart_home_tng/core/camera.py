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
import asyncio
import collections
import datetime as dt
import enum
import functools
import random
import typing

import async_timeout
from aiohttp import web

from ..backports import strenum
from .callback import callback
from .entity import Entity
from .image import Image
from .rtsp_to_web_rtc_provider_type import RtspToWebRtcProviderType
from .smart_home_controller_component import SmartHomeControllerComponent
from .smart_home_controller_error import SmartHomeControllerError
from .stream_base import StreamBase
from .stream_component import StreamComponent
from .stream_type import StreamType

_MIN_STREAM_INTERVAL: typing.Final = 0.5  # seconds
_DEFAULT_CONTENT_TYPE: typing.Final = "image/jpeg"
_ENTITY_IMAGE_URL: typing.Final = "/api/camera_proxy/{0}?token={1}"
_RND: typing.Final = random.SystemRandom()
_STATE_RECORDING: typing.Final = "recording"
_STATE_STREAMING: typing.Final = "streaming"
_STATE_IDLE: typing.Final = "idle"
_RTSP_PREFIXES: typing.Final = {"rtsp://", "rtsps://", "rtmp://"}
_DATA_CAMERA_PREFS: typing.Final = "camera_prefs"
_DATA_RTSP_TO_WEB_RTC: typing.Final = "rtsp_to_web_rtc"
_PREF_PRELOAD_STREAM: typing.Final = "preload_stream"
_SERVICE_RECORD: typing.Final = "record"
_CONF_LOOKBACK: typing.Final = "lookback"
_CONF_DURATION: typing.Final = "duration"
_CAMERA_STREAM_SOURCE_TIMEOUT: typing.Final = 10
_CAMERA_IMAGE_TIMEOUT: typing.Final = 10
_SERVICE_ENABLE_MOTION: typing.Final = "enable_motion_detection"
_SERVICE_DISABLE_MOTION: typing.Final = "disable_motion_detection"
_SERVICE_SNAPSHOT: typing.Final = "snapshot"
_SERVICE_PLAY_STREAM: typing.Final = "play_stream"

_SCAN_INTERVAL: typing.Final = dt.timedelta(seconds=30)

_ATTR_FILENAME: typing.Final = "filename"
_ATTR_MEDIA_PLAYER: typing.Final = "media_player"
_ATTR_FORMAT: typing.Final = "format"


@typing.overload
class _Entity:
    pass


class _Component(SmartHomeControllerComponent):
    """Required base class for the Camera Component."""

    @abc.abstractmethod
    async def async_get_still_stream(
        self,
        request: web.Request,
        image_cb: typing.Callable[[], typing.Awaitable[bytes]],
        content_type: str,
        interval: float,
    ) -> web.StreamResponse:
        """Generate an HTTP MJPEG stream from camera images.

        This method must be run in the event loop.
        """

    @property
    @abc.abstractmethod
    def has_rtsp_to_web_rtc_providers(self) -> bool:
        """Return True, if RTSP to WebRTC providers are registered."""

    @abc.abstractmethod
    async def async_request_stream(self, entity_id: str, fmt: str) -> str:
        """Request a stream for a camera entity."""

    @abc.abstractmethod
    async def async_get_image(
        self,
        entity_id: str,
        timeout: int = 10,
        width: int = None,
        height: int = None,
    ) -> Image:
        """Fetch an image from a camera entity.

        width and height will be passed to the underlying camera.
        """

    @abc.abstractmethod
    async def async_get_stream_source(self, entity_id: str) -> str:
        """Fetch the stream source for a camera entity."""

    @abc.abstractmethod
    async def async_get_mjpeg_stream(
        self, request: web.Request, entity_id: str
    ) -> web.StreamResponse:
        """Fetch an mjpeg stream from a camera entity."""

    @abc.abstractmethod
    def register_rtsp_to_web_rtc_provider(
        self,
        domain: str,
        provider: RtspToWebRtcProviderType,
    ) -> typing.Callable[[], None]:
        """Register an RTSP to WebRTC provider.

        The first provider to satisfy the offer will be used.
        """

    @abc.abstractmethod
    def get_rtsp_to_web_rtc_providers(
        self,
    ) -> typing.Iterable[RtspToWebRtcProviderType]:
        """Return registered RTSP to WebRTC providers."""

    @abc.abstractmethod
    async def _async_stream_endpoint_url(self, camera: _Entity, fmt: str) -> str:
        """Get Stream Endpoint URL."""


class _StreamType(strenum.LowercaseStrEnum):
    """Camera stream type.

    A camera that supports CAMERA_SUPPORT_STREAM may have a single stream
    type which is used to inform the frontend which player to use.
    Streams with RTSP sources typically use the stream component which uses
    HLS for display. WebRTC streams use the home assistant core for a signal
    path to initiate a stream, but the stream itself is between the client and
    device.
    """

    HLS = enum.auto()
    WEB_RTC = enum.auto()


class _EntityFeature(enum.IntEnum):
    """Supported features of the camera entity."""

    ON_OFF = 1
    STREAM = 2


class _Entity(Entity):
    """The base class for camera entities."""

    # Entity Properties
    _attr_brand: str | None = None
    _attr_frame_interval: float = _MIN_STREAM_INTERVAL
    _attr_frontend_stream_type: StreamType
    _attr_is_on: bool = True
    _attr_is_recording: bool = False
    _attr_is_streaming: bool = False
    _attr_model: str = None
    _attr_motion_detection_enabled: bool = False
    _attr_should_poll: bool = False  # No need to poll cameras
    _attr_state: None = None  # State is determined by is_on
    _attr_supported_features: int = 0

    def __init__(self) -> None:
        """Initialize a camera."""
        self._stream: StreamBase = None
        self._stream_options: dict[str, str | bool | float] = {}
        self._content_type: str = _DEFAULT_CONTENT_TYPE
        self._access_tokens: collections.deque = collections.deque([], 2)
        self._warned_old_signature = False
        self.async_update_token()
        self._create_stream_lock: asyncio.Lock = None
        self._rtsp_to_webrtc = False
        self._camera_component: _Component = None

    @property
    def camera(self) -> _Component:
        if self._camera_component is None:
            self._camera_component = self._shc.components.camera
        return self._camera_component

    @property
    def stream(self) -> StreamBase:
        return self._stream

    @property
    def stream_options(self) -> dict[str, str | bool | float]:
        return self._stream_options

    @property
    def content_type(self) -> str:
        return self._content_type

    @property
    def access_tokens(self) -> collections.deque:
        return self._access_tokens

    @property
    def entity_picture(self) -> str:
        """Return a link to the camera feed as entity picture."""
        if self._attr_entity_picture is not None:
            return self._attr_entity_picture
        return _ENTITY_IMAGE_URL.format(self.entity_id, self.access_tokens[-1])

    @property
    def supported_features(self) -> int:
        """Flag supported features."""
        return self._attr_supported_features

    @property
    def is_recording(self) -> bool:
        """Return true if the device is recording."""
        return self._attr_is_recording

    @property
    def is_streaming(self) -> bool:
        """Return true if the device is streaming."""
        return self._attr_is_streaming

    @property
    def brand(self) -> str:
        """Return the camera brand."""
        return self._attr_brand

    @property
    def motion_detection_enabled(self) -> bool:
        """Return the camera motion detection status."""
        return self._attr_motion_detection_enabled

    @property
    def model(self) -> str:
        """Return the camera model."""
        return self._attr_model

    @property
    def frame_interval(self) -> float:
        """Return the interval between frames of the mjpeg stream."""
        return self._attr_frame_interval

    @property
    def frontend_stream_type(self) -> StreamType:
        """Return the type of stream supported by this camera.

        A camera may have a single stream type which is used to inform the
        frontend which camera attributes and player to use. The default type
        is to use HLS, and components can override to change the type.
        """
        if hasattr(self, "_attr_frontend_stream_type"):
            return self._attr_frontend_stream_type
        if not self.supported_features & _EntityFeature.STREAM:
            return None
        if self._rtsp_to_webrtc:
            return StreamType.WEB_RTC
        return StreamType.HLS

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        if self.stream and not self.stream.available:
            return self.stream.available
        return super().available

    async def async_create_stream(self) -> StreamBase:
        """Create a Stream for stream_source."""
        # There is at most one stream (a decode worker) per camera
        if not self._create_stream_lock:
            self._create_stream_lock = asyncio.Lock()
        async with self._create_stream_lock:
            if not self.stream:
                async with async_timeout.timeout(_CAMERA_STREAM_SOURCE_TIMEOUT):
                    source = await self.stream_source()
                if not source:
                    return None
                stream_comp = self._shc.components.stream
                if not isinstance(stream_comp, StreamComponent):
                    return None

                self._stream = stream_comp.create_stream(
                    source,
                    options=self.stream_options,
                    stream_label=self.entity_id,
                )
                self.stream.set_update_callback(self.async_write_state)
            return self.stream

    async def stream_source(self) -> str:
        """Return the source of the stream.

        This is used by cameras with CameraEntityFeature.STREAM
        and StreamType.HLS.
        """
        return None

    async def async_handle_web_rtc_offer(self, offer_sdp: str) -> str:
        """Handle the WebRTC offer and return an answer.

        This is used by cameras with CameraEntityFeature.STREAM
        and StreamType.WEB_RTC.

        Integrations can override with a native WebRTC implementation.
        """
        stream_source = await self.stream_source()
        if not stream_source:
            return None
        for provider in self._get_rtsp_to_web_rtc_providers():
            answer_sdp = await provider(stream_source, offer_sdp, self.entity_id)
            if answer_sdp:
                return answer_sdp
        raise SmartHomeControllerError("WebRTC offer was not accepted by any providers")

    def camera_image(self, width: int = None, height: int = None) -> bytes:
        """Return bytes of camera image."""
        raise NotImplementedError()

    async def async_camera_image(self, width: int = None, height: int = None) -> bytes:
        """Return bytes of camera image."""
        return await self._shc.async_add_executor_job(
            functools.partial(self.camera_image, width=width, height=height)
        )

    async def handle_async_still_stream(
        self, request: web.Request, interval: float
    ) -> web.StreamResponse:
        """Generate an HTTP MJPEG stream from camera images."""
        return await self.camera.async_get_still_stream(
            request, self.async_camera_image, self.content_type, interval
        )

    async def handle_async_mjpeg_stream(
        self, request: web.Request
    ) -> web.StreamResponse:
        """Serve an HTTP MJPEG stream from the camera.

        This method can be overridden by camera platforms to proxy
        a direct stream from the camera.
        """
        return await self.handle_async_still_stream(request, self.frame_interval)

    @property
    @typing.final
    def state(self) -> str:
        """Return the camera state."""
        if self.is_recording:
            return _STATE_RECORDING
        if self.is_streaming:
            return _STATE_STREAMING
        return _STATE_IDLE

    @property
    def is_on(self) -> bool:
        """Return true if on."""
        return self._attr_is_on

    def turn_off(self) -> None:
        """Turn off camera."""
        raise NotImplementedError()

    async def async_turn_off(self) -> None:
        """Turn off camera."""
        await self._shc.async_add_executor_job(self.turn_off)

    def turn_on(self) -> None:
        """Turn off camera."""
        raise NotImplementedError()

    async def async_turn_on(self) -> None:
        """Turn off camera."""
        await self._shc.async_add_executor_job(self.turn_on)

    def enable_motion_detection(self) -> None:
        """Enable motion detection in the camera."""
        raise NotImplementedError()

    async def async_enable_motion_detection(self) -> None:
        """Call the job and enable motion detection."""
        await self._shc.async_add_executor_job(self.enable_motion_detection)

    def disable_motion_detection(self) -> None:
        """Disable motion detection in camera."""
        raise NotImplementedError()

    async def async_disable_motion_detection(self) -> None:
        """Call the job and disable motion detection."""
        await self._shc.async_add_executor_job(self.disable_motion_detection)

    @typing.final
    @property
    def state_attributes(self) -> dict[str, str]:
        """Return the camera state attributes."""
        attrs = {"access_token": self.access_tokens[-1]}

        if self.model:
            attrs["model_name"] = self.model

        if self.brand:
            attrs["brand"] = self.brand

        if self.motion_detection_enabled:
            attrs["motion_detection"] = self.motion_detection_enabled

        if self.frontend_stream_type:
            attrs["frontend_stream_type"] = self.frontend_stream_type

        return attrs

    @callback
    def async_update_token(self) -> None:
        """Update the used token."""
        self.access_tokens.append(hex(_RND.getrandbits(256))[2:])

    async def async_internal_added_to_shc(self) -> None:
        """Run when entity about to be added to the Smart Home Controller."""
        await super().async_internal_added_to_shc()
        await self.async_refresh_providers()

    async def async_refresh_providers(self) -> None:
        """Determine if any of the registered providers are suitable for this entity.

        This affects state attributes, so it should be invoked any time the registered
        providers or inputs to the state attributes change.

        Returns True if any state was updated (and needs to be written)
        """
        old_state = self._rtsp_to_webrtc
        self._rtsp_to_webrtc = await self._async_use_rtsp_to_webrtc()
        if old_state != self._rtsp_to_webrtc:
            self.async_write_state()

    async def _async_use_rtsp_to_webrtc(self) -> bool:
        """Determine if a WebRTC provider can be used for the camera."""
        if not self.supported_features & _EntityFeature.STREAM:
            return False
        if self.camera is None or not self.camera.has_rtsp_to_web_rtc_providers:
            return False
        stream_source = await self.stream_source()
        return any(
            stream_source and stream_source.startswith(prefix)
            for prefix in _RTSP_PREFIXES
        )

    def _get_rtsp_to_web_rtc_providers(
        self,
    ) -> typing.Iterable[RtspToWebRtcProviderType]:
        """Return registered RTSP to WebRTC providers."""
        if self.camera is None:
            return {}
        return self.camera.get_rtsp_to_web_rtc_providers()


# pylint: disable=invalid-name, unused-variable
class Camera:
    """Camera namespace."""

    MIN_STREAM_INTERVAL: typing.Final = _MIN_STREAM_INTERVAL
    DEFAULT_CONTENT_TYPE: typing.Final = _DEFAULT_CONTENT_TYPE
    ENTITY_IMAGE_URL: typing.Final = _ENTITY_IMAGE_URL
    RND: typing.Final = _RND
    STATE_RECORDING: typing.Final = _STATE_RECORDING
    STATE_STREAMING: typing.Final = _STATE_STREAMING
    STATE_IDLE: typing.Final = _STATE_IDLE
    RTSP_PREFIXES: typing.Final = _RTSP_PREFIXES
    DATA_CAMERA_PREFS: typing.Final = _DATA_CAMERA_PREFS
    DATA_RTSP_TO_WEB_RTC: typing.Final = _DATA_RTSP_TO_WEB_RTC
    PREF_PRELOAD_STREAM: typing.Final = _PREF_PRELOAD_STREAM
    SERVICE_RECORD: typing.Final = _SERVICE_RECORD
    CONF_LOOKBACK: typing.Final = _CONF_LOOKBACK
    CONF_DURATION: typing.Final = _CONF_DURATION
    CAMERA_STREAM_SOURCE_TIMEOUT: typing.Final = _CAMERA_STREAM_SOURCE_TIMEOUT
    CAMERA_IMAGE_TIMEOUT: typing.Final = _CAMERA_IMAGE_TIMEOUT
    SERVICE_ENABLE_MOTION: typing.Final = _SERVICE_ENABLE_MOTION
    SERVICE_DISABLE_MOTION: typing.Final = _SERVICE_DISABLE_MOTION
    SERVICE_SNAPSHOT: typing.Final = _SERVICE_SNAPSHOT
    SERVICE_PLAY_STREAM: typing.Final = _SERVICE_PLAY_STREAM

    SCAN_INTERVAL: typing.Final = _SCAN_INTERVAL

    ATTR_FILENAME: typing.Final = _ATTR_FILENAME
    ATTR_MEDIA_PLAYER: typing.Final = _ATTR_MEDIA_PLAYER
    ATTR_FORMAT: typing.Final = _ATTR_FORMAT

    Component: typing.TypeAlias = _Component
    Entity: typing.TypeAlias = _Entity
    EntityFeature: typing.TypeAlias = _EntityFeature
    StreamType: typing.TypeAlias = _StreamType
