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
import logging
import secrets
import threading
import time
import types
import typing

from ... import core
from .const import Const
from .diagnostic import Diagnostics
from .idle_timer import IdleTimer
from .key_frame_converter import KeyFrameConverter
from .recorder_output import RecorderOutput
from .stream_output import StreamOutput
from .stream_settings import StreamSettings
from .stream_state import StreamState
from .stream_worker import _stream_worker

if not typing.TYPE_CHECKING:

    class StreamComponent:
        pass


if typing.TYPE_CHECKING:
    from .stream_component import StreamComponent


_LOGGER: typing.Final = logging.getLogger(__name__)


# pylint: disable=unused-variable
class Stream(core.StreamBase):
    """Represents a single stream."""

    def __init__(
        self,
        owner: StreamComponent,
        source: str,
        pyav_options: dict[str, str],
        stream_settings: StreamSettings,
        stream_label: str = None,
    ) -> None:
        """Initialize a stream."""
        self._owner = owner
        self._source = source
        self._pyav_options = pyav_options
        self._stream_settings = stream_settings
        self._stream_label = stream_label
        self._keepalive = False
        self._access_token: str = None
        self._start_stop_lock = asyncio.Lock()
        self._thread: threading.Thread | None = None
        self._thread_quit = threading.Event()
        self._outputs: dict[str, StreamOutput] = {}
        self._fast_restart_once = False
        self._keyframe_converter = KeyFrameConverter(owner.controller)
        self._available: bool = True
        self._update_callback: typing.Callable[[], None] = None
        self._logger = (
            logging.getLogger(f"{__package__}.stream.{stream_label}")
            if stream_label
            else _LOGGER
        )
        self._diagnostics = Diagnostics()

    @property
    def source(self) -> str:
        return self._source

    @property
    def pyav_options(self) -> dict[str, str]:
        return self._pyav_options

    @property
    def keepalive(self) -> bool:
        return self._keepalive

    @property
    def access_token(self) -> str:
        return self._access_token

    def endpoint_url(self, fmt: str) -> str:
        """Start the stream and returns a url for the output format."""
        if fmt not in self._outputs:
            raise ValueError(f"Stream is not configured for format '{fmt}'")
        if not self.access_token:
            self.access_token = secrets.token_hex()
        endpoint_fmt: str = self._owner.get_endpoint_format(fmt)
        return endpoint_fmt.format(self.access_token)

    def outputs(self) -> typing.Mapping[str, StreamOutput]:
        """Return a copy of the stream outputs."""
        # A copy is returned so the caller can iterate through the outputs
        # without concern about self._outputs being modified from another thread.
        return types.MappingProxyType(self._outputs.copy())

    def add_provider(self, fmt: str, timeout: int = ...) -> None:
        self._internal_add_provider(fmt, timeout)

    def _internal_add_provider(
        self, fmt: str, timeout: int = Const.OUTPUT_IDLE_TIMEOUT
    ) -> StreamOutput:
        """Add provider output stream."""
        if not (provider := self._outputs.get(fmt)):

            async def idle_callback() -> None:
                if (
                    not self.keepalive or fmt == Const.RECORDER_PROVIDER
                ) and fmt in self._outputs:
                    await self.remove_provider(self._outputs[fmt])
                self.check_idle()

            provider_class = self._owner.get_provider_class(fmt)
            provider = provider_class(
                self._owner.controller,
                IdleTimer(self._owner.controller, timeout, idle_callback),
                self._stream_settings,
            )
            self._outputs[fmt] = provider

        return provider

    async def remove_provider(self, provider: StreamOutput) -> None:
        """Remove provider output stream."""
        if provider.name in self._outputs:
            self._outputs[provider.name].cleanup()
            del self._outputs[provider.name]

        if not self._outputs:
            await self.stop()

    def check_idle(self) -> None:
        """Reset access token if all providers are idle."""
        if all(p.idle for p in self._outputs.values()):
            self._access_token = None

    @property
    def available(self) -> bool:
        """Return False if the stream is started and known to be unavailable."""
        return self._available

    def set_update_callback(self, update_callback: typing.Callable[[], None]) -> None:
        """Set callback to run when state changes."""
        self._update_callback = update_callback

    @core.callback
    def _async_update_state(self, available: bool) -> None:
        """Set state and Run callback to notify state has been updated."""
        self._available = available
        if self._update_callback:
            self._update_callback()

    async def start(self) -> None:
        """Start a stream.

        Uses an asyncio.Lock to avoid conflicts with _stop().
        """
        async with self._start_stop_lock:
            if self._thread and self._thread.is_alive():
                return
            if self._thread is not None:
                # The thread must have crashed/exited. Join to clean up the
                # previous thread.
                self._thread.join(timeout=0)
            self._thread_quit.clear()
            self._thread = threading.Thread(
                name="stream_worker",
                target=self._run_worker,
            )
            self._thread.start()
            self._logger.debug(
                f"Started stream: {self._owner.redact_credentials(str(self.source))}",
            )

    def update_source(self, new_source: str) -> None:
        """Restart the stream with a new stream source."""
        self._diagnostics.increment("update_source")
        self._logger.debug(
            f"Updating stream source {self._owner.redact_credentials(str(new_source))}"
        )
        self._source = new_source
        self._fast_restart_once = True
        self._thread_quit.set()

    def _run_worker(self) -> None:
        """Handle consuming streams and restart keepalive streams."""

        stream_state = StreamState(self.outputs, self._diagnostics)
        wait_timeout = 0
        while not self._thread_quit.wait(timeout=wait_timeout):
            start_time = time.time()
            self._owner.controller.add_job(self._async_update_state, True)
            self._diagnostics.set_value("keepalive", self.keepalive)
            self._diagnostics.increment("start_worker")
            try:
                _stream_worker(
                    self,
                    self.source,
                    self.pyav_options,
                    self._stream_settings,
                    stream_state,
                    self._keyframe_converter,
                    self._thread_quit,
                )
            except core.StreamWorkerError as err:
                self._diagnostics.increment("worker_error")
                self._logger.error(f"Error from stream worker: {str(err)}")

            stream_state.discontinuity()
            if not _should_retry() or self._thread_quit.is_set():
                if self._fast_restart_once:
                    # The stream source is updated, restart without any delay and reset the retry
                    # backoff for the new url.
                    wait_timeout = 0
                    self._fast_restart_once = False
                    self._thread_quit.clear()
                    continue
                break

            self._owner.controller.add_job(self._async_update_state, False)
            # To avoid excessive restarts, wait before restarting
            # As the required recovery time may be different for different setups, start
            # with trying a short wait_timeout and increase it on each reconnection attempt.
            # Reset the wait_timeout after the worker has been up for several minutes
            if time.time() - start_time > Const.STREAM_RESTART_RESET_TIME:
                wait_timeout = 0
            wait_timeout += Const.STREAM_RESTART_INCREMENT
            self._diagnostics.set_value("retry_timeout", wait_timeout)
            self._logger.debug(
                f"Restarting stream worker in {wait_timeout:d} seconds: "
                + f"{self._owner.redact_credentials(str(self.source))}",
            )

        self._owner.controller.create_task(self._worker_finished())

    async def _worker_finished(self) -> None:
        # The worker is no checking availability of the stream and can no longer track
        # availability so mark it as available, otherwise the frontend may not be able to
        # interact with the stream.
        if not self.available:
            self._async_update_state(True)
        # We can call remove_provider() sequentially as the wrapped _stop() function
        # which blocks internally is only called when the last provider is removed.
        for provider in self.outputs().values():
            await self.remove_provider(provider)

    async def stop(self) -> None:
        """Remove outputs and access token."""
        self._outputs = {}
        self._access_token = None

        if not self.keepalive:
            await self._stop()

    async def _stop(self) -> None:
        """Stop worker thread.

        Uses an asyncio.Lock to avoid conflicts with start().
        """
        async with self._start_stop_lock:
            if self._thread is None:
                return
            self._thread_quit.set()
            await self._owner.controller.async_add_executor_job(self._thread.join)
            self._thread = None
            self._logger.debug(
                f"Stopped stream: {self._owner.redact_credentials(str(self.source))}"
            )

    async def async_record(
        self, video_path: str, duration: int = 30, lookback: int = 5
    ) -> None:
        """Make a .mp4 recording from a provided stream."""

        # Check for file access
        if not self._owner.controller.config.is_allowed_path(video_path):
            raise core.SmartHomeControllerError(
                f"Can't write {video_path}, no access to path!"
            )

        # Add recorder
        recorder = self.outputs().get(Const.RECORDER_PROVIDER)
        if isinstance(recorder, RecorderOutput):
            raise core.SmartHomeControllerError(
                f"Stream already recording to {recorder.video_path}!"
            )

        recorder: RecorderOutput = self._internal_add_provider(
            Const.RECORDER_PROVIDER, timeout=duration
        )

        recorder.video_path = video_path

        await self.start()

        self._logger.debug(f"Started a stream recording of {duration} seconds")

        # Take advantage of lookback
        hls = self.outputs().get(Const.HLS_PROVIDER)
        if hls:
            num_segments = min(
                int(lookback / hls.target_duration) + 1, Const.MAX_SEGMENTS
            )
            # Wait for latest segment, then add the lookback
            await hls.recv()
            recorder.prepend(list(hls.get_segments())[-num_segments - 1 : -1])

        await recorder.async_record()

    async def async_get_image(
        self,
        width: int = None,
        height: int = None,
    ) -> bytes:
        """
        Fetch an image from the Stream and return it as a jpeg in bytes.

        Calls async_get_image from KeyFrameConverter. async_get_image should only be
        called directly from the main loop and not from an executor thread as it uses
        hass.add_executor_job underneath the hood.
        """

        self.add_provider(Const.HLS_PROVIDER)
        await self.start()
        return await self._keyframe_converter.async_get_image(
            width=width, height=height
        )

    def get_diagnostics(self) -> dict[str, typing.Any]:
        """Return diagnostics information for the stream."""
        return self._diagnostics.as_dict()


def _should_retry() -> bool:
    """Return true if worker failures should be retried, for disabling during tests."""
    return True
