"""
Analytics Component for Smart Home - The Next Generation.

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

import typing

import voluptuous as vol

from ... import core
from .analytics import Analytics
from .const import Const

_SEND_PREFERENCES: typing.Final = {vol.Required("type"): "analytics"}
_UPDATE_PREFERENCES: typing.Final = {
    vol.Required("type"): "analytics/preferences",
    vol.Required("preferences", default={}): Const.PREFERENCE_SCHEMA,
}


# pylint: disable=unused-variable
class AnalyticsComponent(core.SmartHomeControllerComponent):
    """Send instance and usage analytics."""

    def __init__(self, path: typing.Iterable[str]):
        super().__init__(path)
        self._analytics: Analytics = None

    @property
    def storage_key(self) -> str:
        # pylint: disable=no-member
        return "core." + super().storage_key

    async def async_setup(self, config: core.ConfigType) -> bool:
        """Set up the analytics integration."""
        if not await super().async_setup(config):
            return False

        api = self.controller.components.websocket_api
        if not isinstance(api, core.WebSocket.Component):
            return False

        self._analytics = Analytics(self)

        # Load stored data
        await self._analytics.load()

        shc = self._shc
        shc.bus.async_listen_once(core.Const.EVENT_SHC_STARTED, self._start_schedule)

        api.register_command(self._send_analytics_preferences, _SEND_PREFERENCES)
        api.register_command(self._update_analytics_preferences, _UPDATE_PREFERENCES)

        return True

    async def _start_schedule(self, _event):
        """Start the send schedule after the started event."""
        # Wait 15 min after started
        self._shc.tracker.async_call_later(900, self._analytics.send_analytics)

        # Send every day
        self._shc.tracker.async_track_time_interval(
            self._analytics.send_analytics, Const.INTERVAL
        )

    async def _send_analytics_preferences(
        self,
        connection: core.WebSocket.Connection,
        msg: dict,
    ) -> None:
        """Return analytics preferences."""
        connection.require_admin()

        connection.send_result(
            msg["id"],
            {
                Const.ATTR_PREFERENCES: self._analytics.preferences,
                Const.ATTR_ONBOARDED: self._analytics.onboarded,
            },
        )

    async def _update_analytics_preferences(
        self,
        connection: core.WebSocket.Connection,
        msg: dict,
    ) -> None:
        """Update analytics preferences."""
        connection.require_admin()

        preferences = msg[Const.ATTR_PREFERENCES]

        # Never send any data to Home Assistant
        preferences[Const.ATTR_BASE] = False

        await self._analytics.save_preferences(preferences)
        await self._analytics.send_analytics()

        connection.send_result(
            msg["id"],
            {Const.ATTR_PREFERENCES: self._analytics.preferences},
        )
