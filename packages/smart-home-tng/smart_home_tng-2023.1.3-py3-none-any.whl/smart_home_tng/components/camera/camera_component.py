"""
Camera Component for Smart Home - The Next Generation.

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
import os
import typing

import voluptuous as vol
from aiohttp import web

from ... import core
from .camera_image_view import CameraImageView, _async_get_image
from .camera_media_source import CameraMediaSource
from .camera_mjpeg_stream import CameraMjpegStream
from .camera_preferences import CameraPreferences

_cv: typing.TypeAlias = core.ConfigValidation
_camera: typing.TypeAlias = core.Camera

_LOGGER: typing.Final = logging.getLogger(__name__)


_TOKEN_CHANGE_INTERVAL: typing.Final = dt.timedelta(minutes=5)

_CAMERA_SERVICE_SNAPSHOT: typing.Final = {
    vol.Required(_camera.ATTR_FILENAME): _cv.template
}
_CAMERA_SERVICE_PLAY_STREAM: typing.Final = {
    vol.Required(_camera.ATTR_MEDIA_PLAYER): _cv.entities_domain("media_player"),
    vol.Optional(_camera.ATTR_FORMAT, default="hls"): vol.In(
        core.StreamComponent.Const.OUTPUT_FORMATS
    ),
}
_CAMERA_SERVICE_RECORD: typing.Final = {
    vol.Required(core.Const.CONF_FILENAME): _cv.template,
    vol.Optional(_camera.CONF_DURATION, default=30): vol.Coerce(int),
    vol.Optional(_camera.CONF_LOOKBACK, default=0): vol.Coerce(int),
}

_WS_CAMERA_STREAM: typing.Final = {
    vol.Required("type"): "camera/stream",
    vol.Required("entity_id"): _cv.entity_id,
    vol.Optional("format", default="hls"): vol.In(
        core.StreamComponent.Const.OUTPUT_FORMATS
    ),
}
_WS_CAMERA_RTC_OFFER: typing.Final = {
    vol.Required("type"): "camera/web_rtc_offer",
    vol.Required("entity_id"): _cv.entity_id,
    vol.Required("offer"): str,
}
_WS_CAMERA_GET_PREFS: typing.Final = {
    vol.Required("type"): "camera/get_prefs",
    vol.Required("entity_id"): _cv.entity_id,
}
_WS_CAMERA_UPDATE_PREFS: typing.Final = {
    vol.Required("type"): "camera/update_prefs",
    vol.Required("entity_id"): _cv.entity_id,
    vol.Optional("preload_stream"): bool,
}


# pylint: disable=unused-variable
class CameraComponent(
    _camera.Component,
    core.DiagnosticsPlatform,
    core.MediaSourcePlatform,
    core.RecorderPlatform,
):
    """Component to interface with cameras."""

    def __init__(self, path: typing.Iterable[str]):
        super().__init__(path)
        self._component: core.EntityComponent = None
        self._prefs: CameraPreferences = None
        self._rtsp_to_web_rtc_providers: dict[str, core.RtspToWebRtcProviderType] = None
        self._supported_platforms = frozenset(
            [
                core.Platform.DIAGNOSTICS,
                core.Platform.MEDIA_SOURCE,
                core.Platform.RECORDER,
            ]
        )

    @property
    def entity_component(self) -> core.EntityComponent:
        return self._component

    @property
    def has_rtsp_to_web_rtc_providers(self) -> bool:
        return self._rtsp_to_web_rtc_providers is not None

    @property
    def scan_interval(self) -> dt.timedelta:
        return _camera.SCAN_INTERVAL

    async def async_setup(self, config: core.ConfigType) -> bool:
        """Set up the camera component."""
        if not await super().async_setup(config):
            return False

        websocket_api = self.controller.components.websocket_api
        if not isinstance(websocket_api, core.WebSocket.Component):
            return False

        component = self._component = core.EntityComponent(
            _LOGGER, self.domain, self.controller, self.scan_interval
        )

        prefs = CameraPreferences(self)
        await prefs.async_initialize()
        self._prefs = prefs

        shc = self.controller
        shc.http.register_view(CameraImageView(component))
        shc.http.register_view(CameraMjpegStream(component))

        websocket_api.register_command(self._camera_stream, _WS_CAMERA_STREAM)
        websocket_api.register_command(self._camera_web_rtc_offer, _WS_CAMERA_RTC_OFFER)
        websocket_api.register_command(self._camera_get_prefs, _WS_CAMERA_GET_PREFS)
        websocket_api.register_command(
            self._camera_update_prefs, _WS_CAMERA_UPDATE_PREFS
        )

        await component.async_setup(config)

        shc.bus.async_listen_once(core.Const.EVENT_SHC_STARTED, self._preload_stream)

        shc.tracker.async_track_time_interval(
            self._update_tokens, _TOKEN_CHANGE_INTERVAL
        )

        component.async_register_entity_service(
            _camera.SERVICE_ENABLE_MOTION, {}, "async_enable_motion_detection"
        )
        component.async_register_entity_service(
            _camera.SERVICE_DISABLE_MOTION, {}, "async_disable_motion_detection"
        )
        component.async_register_entity_service(
            core.Const.SERVICE_TURN_OFF, {}, "async_turn_off"
        )
        component.async_register_entity_service(
            core.Const.SERVICE_TURN_ON, {}, "async_turn_on"
        )
        component.async_register_entity_service(
            _camera.SERVICE_SNAPSHOT,
            _CAMERA_SERVICE_SNAPSHOT,
            self._async_handle_snapshot_service,
        )
        component.async_register_entity_service(
            _camera.SERVICE_PLAY_STREAM,
            _CAMERA_SERVICE_PLAY_STREAM,
            self._async_handle_play_stream_service,
        )
        component.async_register_entity_service(
            _camera.SERVICE_RECORD,
            _CAMERA_SERVICE_RECORD,
            self._async_handle_record_service,
        )
        return True

    async def async_setup_entry(self, entry: core.ConfigEntry) -> bool:
        """Set up a config entry."""
        return await self._component.async_setup_entry(entry)

    async def async_unload_entry(self, entry: core.ConfigEntry) -> bool:
        """Unload a config entry."""
        return await self._component.async_unload_entry(entry)

    async def _preload_stream(self, _event: core.Event) -> None:
        for camera in self._component.entities:
            camera = typing.cast(core.Camera, camera)
            camera_prefs = self._prefs.get(camera.entity_id)
            if not camera_prefs.preload_stream:
                continue
            stream = await camera.async_create_stream()
            if not stream:
                continue
            stream.keepalive = True
            stream.add_provider("hls")
            await stream.start()

    @core.callback
    def _update_tokens(self, _time: dt.datetime) -> None:
        """Update tokens of the entities."""
        for entity in self._component.entities:
            entity = typing.cast(core.Camera, entity)
            entity.async_update_token()
            entity.async_write_state()

    async def _async_handle_snapshot_service(
        self, camera: core.Camera, service_call: core.ServiceCall
    ) -> None:
        """Handle snapshot services calls."""
        shc = self.controller
        filename = service_call.data[_camera.ATTR_FILENAME]
        filename.controller = shc

        snapshot_file = filename.async_render(
            variables={core.Const.ATTR_ENTITY_ID: camera}
        )

        # check if we allow to access to that file
        if not shc.config.is_allowed_path(snapshot_file):
            _LOGGER.error(f"Can't write {snapshot_file}, no access to path!")
            return

        image = await camera.async_camera_image()

        if image is None:
            return

        try:
            await shc.async_add_executor_job(_write_image, snapshot_file, image)
        except OSError as err:
            _LOGGER.error(f"Can't write image to file: {err}")

    async def _async_handle_play_stream_service(
        self, camera: core.Camera, service_call: core.ServiceCall
    ) -> None:
        """Handle play stream services calls."""
        shc = self.controller
        fmt = service_call.data[_camera.ATTR_FORMAT]
        url = await self._async_stream_endpoint_url(camera, fmt)
        url = f"{shc.get_url()}{url}"

        await shc.services.async_call(
            "media_player",
            core.Const.SERVICE_MEDIA_PLAY,
            {
                core.Const.ATTR_ENTITY_ID: service_call.data[_camera.ATTR_MEDIA_PLAYER],
                core.Const.ATTR_MEDIA_CONTENT_ID: url,
                core.Const.ATTR_MEDIA_CONTENT_TYPE: (
                    core.StreamComponent.Const.FORMAT_CONTENT_TYPE[fmt]
                ),
            },
            blocking=True,
            context=service_call.context,
        )

    async def _async_stream_endpoint_url(self, camera: core.Camera, fmt: str) -> str:
        stream = await camera.async_create_stream()
        if not stream:
            raise core.SmartHomeControllerError(
                f"{camera.entity_id} does not support play stream service"
            )

        # Update keepalive setting which manages idle shutdown
        camera_prefs = self._prefs.get(camera.entity_id)
        stream.keepalive = camera_prefs.preload_stream

        stream.add_provider(fmt)
        await stream.start()
        return stream.endpoint_url(fmt)

    async def _async_handle_record_service(
        self, camera: core.Camera, service_call: core.ServiceCall
    ) -> None:
        """Handle stream recording service calls."""
        stream = await camera.async_create_stream()

        if not stream:
            raise core.SmartHomeControllerError(
                f"{camera.entity_id} does not support record service"
            )

        shc = self.controller
        filename = service_call.data[core.Const.CONF_FILENAME]
        filename.controller = shc
        video_path = filename.async_render(
            variables={core.Const.ATTR_ENTITY_ID: camera}
        )

        await stream.async_record(
            video_path,
            duration=service_call.data[_camera.CONF_DURATION],
            lookback=service_call.data[_camera.CONF_LOOKBACK],
        )

    async def _camera_stream(
        self,
        connection: core.WebSocket.Connection,
        msg: dict,
    ) -> None:
        """Handle get camera stream websocket command.

        Async friendly.
        """
        try:
            entity_id = msg["entity_id"]
            camera = self._get_camera_from_entity_id(entity_id)
            url = await self._async_stream_endpoint_url(camera, fmt=msg["format"])
            connection.send_result(msg["id"], {"url": url})
        except core.SmartHomeControllerError as ex:
            _LOGGER.error(f"Error requesting stream: {ex}")
            connection.send_error(msg["id"], "start_stream_failed", str(ex))
        except asyncio.TimeoutError:
            _LOGGER.error("Timeout getting stream source")
            connection.send_error(
                msg["id"], "start_stream_failed", "Timeout getting stream source"
            )

    def _get_camera_from_entity_id(self, entity_id: str) -> core.Camera:
        """Get camera component from entity_id."""
        if self._component is None:
            raise core.SmartHomeControllerError("Camera integration not set up")

        if (camera := self._component.get_entity(entity_id)) is None:
            raise core.SmartHomeControllerError("Camera not found")

        if not camera.is_on:
            raise core.SmartHomeControllerError("Camera is off")

        return typing.cast(core.Camera, camera)

    async def _camera_web_rtc_offer(
        self,
        connection: core.WebSocket.Connection,
        msg: dict,
    ) -> None:
        """Handle the signal path for a WebRTC stream.

        This signal path is used to route the offer created by the client to the
        camera device through the integration for negotiation on initial setup,
        which returns an answer. The actual streaming is handled entirely between
        the client and camera device.

        Async friendly.
        """
        entity_id = msg["entity_id"]
        offer = msg["offer"]
        camera = self._get_camera_from_entity_id(entity_id)
        if camera.frontend_stream_type != core.StreamType.WEB_RTC:
            connection.send_error(
                msg["id"],
                "web_rtc_offer_failed",
                (
                    "Camera does not support WebRTC, frontend_stream_type="
                    + f"{camera.frontend_stream_type}"
                ),
            )
            return
        try:
            answer = await camera.async_handle_web_rtc_offer(offer)
        except (core.SmartHomeControllerError, ValueError) as ex:
            _LOGGER.error(f"Error handling WebRTC offer: {ex}")
            connection.send_error(msg["id"], "web_rtc_offer_failed", str(ex))
        except asyncio.TimeoutError:
            _LOGGER.error("Timeout handling WebRTC offer")
            connection.send_error(
                msg["id"], "web_rtc_offer_failed", "Timeout handling WebRTC offer"
            )
        else:
            connection.send_result(msg["id"], {"answer": answer})

    async def _camera_get_prefs(
        self,
        connection: core.WebSocket.Connection,
        msg: dict,
    ) -> None:
        """Handle request for account info."""
        prefs = self._prefs.get(msg["entity_id"])
        connection.send_result(msg["id"], prefs.as_dict())

    async def _camera_update_prefs(
        self,
        connection: core.WebSocket.Connection,
        msg: dict,
    ) -> None:
        """Handle request for account info."""
        prefs = self._prefs

        changes = dict(msg)
        changes.pop("id")
        changes.pop("type")
        entity_id = changes.pop("entity_id")
        await prefs.async_update(entity_id, **changes)

        connection.send_result(msg["id"], prefs.get(entity_id).as_dict())

    async def async_get_image(
        self, entity_id: str, timeout: int = 10, width: int = None, height: int = None
    ) -> core.Image:
        """Fetch an image from a camera entity.

        width and height will be passed to the underlying camera.
        """
        camera = self._get_camera_from_entity_id(entity_id)
        return await _async_get_image(camera, timeout, width, height)

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
        response = web.StreamResponse()
        response.content_type = core.Const.CONTENT_TYPE_MULTIPART.format(
            "--frameboundary"
        )
        await response.prepare(request)

        last_image = None

        while True:
            img_bytes = await image_cb()
            if not img_bytes:
                break

            if img_bytes != last_image:
                await _write_to_mjpeg_stream(response, content_type, img_bytes)

                # Chrome seems to always ignore first picture,
                # print it twice.
                if last_image is None:
                    await _write_to_mjpeg_stream(response, content_type, img_bytes)
                last_image = img_bytes

            await asyncio.sleep(interval)

        return response

    async def async_get_stream_source(self, entity_id: str) -> str:
        """Fetch the stream source for a camera entity."""
        camera = self._get_camera_from_entity_id(entity_id)
        return await camera.stream_source()

    async def async_request_stream(self, entity_id: str, fmt: str) -> str:
        """Request a stream for a camera entity."""
        camera = self._get_camera_from_entity_id(entity_id)
        return await self._async_stream_endpoint_url(camera, fmt)

    async def async_get_mjpeg_stream(
        self, request: web.Request, entity_id: str
    ) -> web.StreamResponse:
        """Fetch an mjpeg stream from a camera entity."""
        camera = self._get_camera_from_entity_id(entity_id)

        try:
            stream = await camera.handle_async_mjpeg_stream(request)
        except ConnectionResetError:
            stream = None
            _LOGGER.debug("Error while writing MJPEG stream to transport")
        return stream

    def register_rtsp_to_web_rtc_provider(
        self, domain: str, provider: core.RtspToWebRtcProviderType
    ) -> typing.Callable[[], None]:
        """Register an RTSP to WebRTC provider.

        The first provider to satisfy the offer will be used.
        """
        if self._component is None:
            raise ValueError("Unexpected state, camera not loaded")

        def remove_provider() -> None:
            if domain in self._rtsp_to_web_rtc_providers:
                self._rtsp_to_web_rtc_providers = None
            self.controller.async_create_task(self._async_refresh_providers())

        if self._rtsp_to_web_rtc_providers is None:
            self._rtsp_to_web_rtc_providers = {}
        self._rtsp_to_web_rtc_providers[domain] = provider
        self.controller.async_create_task(self._async_refresh_providers())
        return remove_provider

    async def _async_refresh_providers(self) -> None:
        """Check all cameras for any state changes for registered providers."""

        await asyncio.gather(
            *(
                typing.cast(core.Camera, camera).async_refresh_providers()
                for camera in self._component.entities
            )
        )

    def get_rtsp_to_web_rtc_providers(
        self,
    ) -> typing.Iterable[core.RtspToWebRtcProviderType]:
        """Return registered RTSP to WebRTC providers."""
        if self._rtsp_to_web_rtc_providers is None:
            return {}
        return self._rtsp_to_web_rtc_providers.values()

    # -------- Diagnostic Platform ----------------------

    async def async_get_config_entry_diagnostics(
        self, config_entry: core.ConfigEntry
    ) -> typing.Any:
        """Return diagnostics for a config entry."""
        entity_registry = self.controller.entity_registry
        entities = entity_registry.async_entries_for_config_entry(config_entry.entry_id)
        diagnostics = {}
        for entity in entities:
            if entity.domain != self.domain:
                continue
            try:
                camera = self._get_camera_from_entity_id(entity.entity_id)
            except core.SmartHomeControllerError:
                continue
            diagnostics[entity.entity_id] = (
                camera.stream.get_diagnostics() if camera.stream else {}
            )
        return diagnostics

    # ----------- Media Source Platform -----------------------

    async def async_get_media_source(self) -> core.MediaSource:
        return CameraMediaSource(self)

    # ------------ Recorder Platform --------------------------

    def exclude_attributes(self) -> set[str]:
        """Exclude access_token and entity_picture from being recorded in the database."""
        return {"access_token", "entity_picture"}


def _write_image(to_file: str, image_data: bytes) -> None:
    """Executor helper to write image."""
    os.makedirs(os.path.dirname(to_file), exist_ok=True)
    with open(to_file, "wb") as img_file:
        img_file.write(image_data)


async def _write_to_mjpeg_stream(
    response: web.Response, content_type: str, img_bytes: bytes
) -> None:
    """Write image to stream."""
    await response.write(
        bytes(
            "--frameboundary\r\n"
            + f"Content-Type: {content_type}\r\n"
            + f"Content-Length: {len(img_bytes)}"
            + "\r\n\r\n",
            "utf-8",
        )
        + img_bytes
        + b"\r\n"
    )
