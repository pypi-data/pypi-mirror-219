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
import collections.abc

from aiohttp import web

from .callback import callback
from .smart_home_controller_component import SmartHomeControllerComponent


# pylint: disable=unused-variable
class WebhookComponent(SmartHomeControllerComponent):
    """Required base class for the Webhook Component."""

    @callback
    @abc.abstractmethod
    def register_webhook(
        self,
        domain: str,
        name: str,
        webhook_id: str,
        handler: collections.abc.Callable[
            [str, web.Request],
            collections.abc.Awaitable[web.Response],
        ],
        *,
        local_only=False,
    ) -> None:
        """Register a webhook."""

    @callback
    @abc.abstractmethod
    def unregister_webhook(self, webhook_id: str) -> None:
        """Remove a webhook."""

    @callback
    @abc.abstractmethod
    def async_generate_id(self) -> str:
        """Generate a webhook_id."""

    @callback
    @abc.abstractmethod
    def async_generate_url(self, webhook_id: str) -> str:
        """Generate the full URL for a webhook_id."""

    @callback
    @abc.abstractmethod
    def async_generate_path(self, webhook_id: str) -> str:
        """Generate the path component for a webhook_id."""

    @abc.abstractmethod
    async def async_handle_webhook(
        self, webhook_id: str, request: web.Request
    ) -> web.Response:
        """Handle a webhook."""
