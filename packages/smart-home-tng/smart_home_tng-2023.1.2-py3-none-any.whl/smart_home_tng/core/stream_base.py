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
import typing

from .protocol import Protocol
from .stream_component import _Const as Const


# pylint: disable=unused-variable
class StreamBase(Protocol):
    """Required base class for Stream Implementation in Stream Component."""

    @abc.abstractmethod
    def add_provider(self, fmt: str, timeout: int = Const.OUTPUT_IDLE_TIMEOUT) -> None:
        """Add provider output stream."""

    @property
    @abc.abstractmethod
    def source(self) -> str:
        """Get stream source."""

    @property
    @abc.abstractmethod
    def pyav_options(self) -> dict[str, str]:
        """Get PPAV Options."""

    @property
    @abc.abstractmethod
    def keepalive(self) -> bool:
        """Get keep alive."""

    @abc.abstractmethod
    def endpoint_url(self, fmt: str) -> str:
        """Start the stream and returns a url for the output format."""

    @abc.abstractmethod
    def check_idle(self) -> None:
        """Reset access token if all providers are idle."""

    @property
    @abc.abstractmethod
    def available(self) -> bool:
        """Return False if the stream is started and known to be unavailable."""

    @abc.abstractmethod
    def set_update_callback(self, update_callback: typing.Callable[[], None]) -> None:
        """Set callback to run when state changes."""

    @abc.abstractmethod
    async def start(self) -> None:
        """Start a stream."""

    @abc.abstractmethod
    def update_source(self, new_source: str) -> None:
        """Restart the stream with a new stream source."""

    @abc.abstractmethod
    async def stop(self) -> None:
        """Remove outputs and access token."""

    @abc.abstractmethod
    async def async_record(
        self, video_path: str, duration: int = 30, lookback: int = 5
    ) -> None:
        """Make a .mp4 recording from a provided stream."""

    @abc.abstractmethod
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

    @abc.abstractmethod
    def get_diagnostics(self) -> dict[str, typing.Any]:
        """Return diagnostics information for the stream."""
