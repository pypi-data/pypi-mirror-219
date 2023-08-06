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
import typing

try:
    import av

    CodecContext: typing.TypeAlias = av.CodecContext
    Packet: typing.TypeAlias = av.Packet
except ImportError:
    av = None

from ... import core


_LOGGER: typing.Final = logging.getLogger(__name__)


# pylint: disable=unused-variable
class KeyFrameConverter:
    """
    Enables generating and getting an image from the last keyframe seen in the stream.

    An overview of the thread and state interaction:
        the worker thread sets a packet
        get_image is called from the main asyncio loop
        get_image schedules _generate_image in an executor thread
        _generate_image will try to create an image from the packet
        _generate_image will clear the packet, so there will only be one attempt per packet
    If successful, self._image will be updated and returned by get_image
    If unsuccessful, get_image will return the previous image
    """

    def __init__(self, shc: core.SmartHomeController) -> None:
        """Initialize."""

        self._packet: Packet = None
        self._shc = shc
        self._image: bytes = None
        self._turbojpeg = core.TurboJPEGSingleton.instance()
        self._lock = asyncio.Lock()
        self._codec_context: CodecContext = None

    @property
    def packet(self) -> Packet:
        return self._packet

    @packet.setter
    def packet(self, value: Packet) -> None:
        if value and value.is_keyframe and value.stream.type == "video":
            self._packet = value

    def create_codec_context(self, codec_context: CodecContext) -> None:
        """
        Create a codec context to be used for decoding the keyframes.

        This is run by the worker thread and will only be called once per worker.
        """

        if self._codec_context:
            return

        self._codec_context = CodecContext.create(codec_context.name, "r")
        self._codec_context.extradata = codec_context.extradata
        self._codec_context.skip_frame = "NONKEY"
        self._codec_context.thread_type = "NONE"

    def _generate_image(self, width: int, height: int) -> None:
        """
        Generate the keyframe image.

        This is run in an executor thread, but since it is called within an
        the asyncio lock from the main thread, there will only be one entry
        at a time per instance.
        """

        if av is None:
            return

        if not (self._turbojpeg and self._packet and self._codec_context):
            return
        packet = self._packet
        self._packet = None
        for _ in range(2):  # Retry once if codec context needs to be flushed
            try:
                # decode packet (flush afterwards)
                frames = self._codec_context.decode(packet)
                for _i in range(2):
                    if frames:
                        break
                    frames = self._codec_context.decode(None)
                break
            except EOFError:
                _LOGGER.debug("Codec context needs flushing, attempting to reopen")
                self._codec_context.close()
                self._codec_context.open()
        else:
            _LOGGER.debug("Unable to decode keyframe")
            return
        if frames:
            frame = frames[0]
            if width and height:
                frame = frame.reformat(width=width, height=height)
            bgr_array = frame.to_ndarray(format="bgr24")
            self._image = bytes(self._turbojpeg.encode(bgr_array))

    async def async_get_image(
        self,
        width: int = None,
        height: int = None,
    ) -> bytes:
        """Fetch an image from the Stream and return it as a jpeg in bytes."""

        # Use a lock to ensure only one thread is working on the keyframe at a time
        async with self._lock:
            await self._shc.async_add_executor_job(self._generate_image, width, height)
        return self._image
