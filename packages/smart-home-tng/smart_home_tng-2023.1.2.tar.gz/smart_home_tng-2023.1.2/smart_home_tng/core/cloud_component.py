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

from .cloud_connection_state import CloudConnectionState
from .smart_home_controller_component import SmartHomeControllerComponent


# pylint: disable=unused-variable
class CloudComponent(SmartHomeControllerComponent):
    """Required base class for the Cloud Component."""

    @property
    @abc.abstractmethod
    def cloud(self) -> typing.Any:
        """Return the configured nabacasa cloud implementation."""

    @property
    @abc.abstractmethod
    def active_subscription(self) -> bool:
        """Test if user has an active subscription."""

    @property
    @abc.abstractmethod
    def is_connected(self) -> bool:
        """Test if connected to the cloud."""

    @property
    @abc.abstractmethod
    def is_logged_in(self) -> bool:
        """Test if user is logged in.

        Note: This returns True even if not currently connected to the cloud.
        """

    @property
    @abc.abstractmethod
    def remote_ui_url(self) -> str:
        """Get the remote UI URL."""

    @abc.abstractmethod
    def listen_connection_change(
        self,
        target: typing.Callable[[CloudConnectionState], typing.Awaitable[None] | None],
    ) -> typing.Callable[[], None]:
        """Notify on connection state changes."""

    @abc.abstractmethod
    async def async_create_cloudhook(self, webhook_id: str) -> str:
        """Create a cloudhook."""

    @abc.abstractmethod
    async def async_delete_cloudhook(self, webhook_id: str) -> None:
        """Delete a cloudhook."""

    @abc.abstractmethod
    def is_cloudhook_request(self, request):
        """Test if a request came from a cloudhook.

        Async friendly.
        """
