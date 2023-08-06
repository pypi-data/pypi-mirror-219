"""
Mobile App Component for Smart Home - The Next Generation.

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
import collections.abc
import typing

from ... import core

_PUSH_CONFIRM_TIMEOUT: typing.Final = 10  # seconds


# pylint: disable=unused-variable
class PushChannel:
    """Class that represents a push channel."""

    def __init__(
        self,
        owner: core.SmartHomeControllerComponent,
        webhook_id: str,
        support_confirm: bool,
        send_message: collections.abc.Callable[[dict], None],
        on_teardown: collections.abc.Callable[[], None],
    ) -> None:
        """Initialize a local push channel."""
        self._owner = owner
        self._webhook_id = webhook_id
        self._support_confirm = support_confirm
        self._send_message = send_message
        self._on_teardown = on_teardown
        self._pending_confirms: dict[str, dict] = {}

    @property
    def webhook_id(self) -> str:
        return self._webhook_id

    @property
    def support_config(self) -> str:
        return self._support_confirm

    @core.callback
    def async_send_notification(self, data, fallback_send):
        """Send a push notification."""
        if not self._support_confirm:
            self._send_message(data)
            return

        confirm_id = core.helpers.random_uuid_hex()
        data["hass_confirm_id"] = confirm_id

        async def handle_push_failed(_=None):
            """Handle a failed local push notification."""
            # Remove this handler from the pending dict
            # If it didn't exist we hit a race condition between call_later and another
            # push failing and tearing down the connection.
            if self._pending_confirms.pop(confirm_id, None) is None:
                return

            # Drop local channel if it's still open
            if self._on_teardown is not None:
                await self.async_teardown()

            await fallback_send(data)

        self._pending_confirms[confirm_id] = {
            "unsub_scheduled_push_failed": self._owner.controller.tracker.async_call_later(
                _PUSH_CONFIRM_TIMEOUT, handle_push_failed
            ),
            "handle_push_failed": handle_push_failed,
        }
        self._send_message(data)

    @core.callback
    def async_confirm_notification(self, confirm_id) -> bool:
        """Confirm a push notification.

        Returns if confirmation successful.
        """
        if confirm_id not in self._pending_confirms:
            return False

        self._pending_confirms.pop(confirm_id)["unsub_scheduled_push_failed"]()
        return True

    async def async_teardown(self):
        """Tear down this channel."""
        # Tear down is in progress
        if self._on_teardown is None:
            return

        self._on_teardown()
        self._on_teardown = None

        cancel_pending_local_tasks = [
            actions["handle_push_failed"]()
            for actions in self._pending_confirms.values()
        ]

        if cancel_pending_local_tasks:
            await asyncio.gather(*cancel_pending_local_tasks)
