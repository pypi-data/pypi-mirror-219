"""
Persistent Notification Component for Smart Home - The Next Generation.

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

import collections.abc
import enum
import logging
import typing

import voluptuous as vol

from ... import core
from ...backports import strenum

_cv: typing.TypeAlias = core.ConfigValidation

_ATTR_CREATED_AT: typing.Final = "created_at"
_ATTR_MESSAGE: typing.Final = "message"
_ATTR_NOTIFICATION_ID: typing.Final = "notification_id"
_ATTR_TITLE: typing.Final = "title"
_ATTR_STATUS: typing.Final = "status"

_EVENT_PERSISTENT_NOTIFICATIONS_UPDATED: typing.Final = (
    "persistent_notifications.updated"
)

_SCHEMA_SERVICE_NOTIFICATION = vol.Schema(
    {vol.Required(_ATTR_NOTIFICATION_ID): _cv.string}
)

_DEFAULT_OBJECT_ID: typing.Final = "notification"
_LOGGER: typing.Final = logging.getLogger(__name__)

_STATE: typing.Final = "notifying"
_LIST_NOTIFICATIONS: typing.Final = {
    vol.Required("type"): "persistent_notification/get"
}


class _NotificationStatus(strenum.LowercaseStrEnum):
    UNREAD = enum.auto()
    READ = enum.auto()


# pylint: disable=unused-variable
class PersistentNotification(core.PersistentNotificationComponent):
    """Support for displaying persistent notifications."""

    def __init__(self, path: typing.Iterable[str]):
        super().__init__(path)
        self._notifications: dict[str, dict[str, typing.Any]] = {}

    def create(
        self,
        message: str,
        title: str = None,
        notification_id: str = None,
    ) -> None:
        """Generate a notification."""
        self._shc.add_job(self.async_create, message, title, notification_id)

    def dismiss(self, notification_id: str) -> None:
        """Remove a notification."""
        self._shc.add_job(self.async_dismiss, notification_id)

    def async_create(
        self,
        message: str,
        title: str = None,
        notification_id: str = None,
        *,
        context: core.Context = None,
    ) -> None:
        """Generate a notification."""

        if notification_id is not None:
            entity_id = f"{self.domain}.{core.helpers.slugify(notification_id)}"
        else:
            entity_id = self._shc.entity_registry.async_generate_entity_id(
                self.domain, _DEFAULT_OBJECT_ID
            )
            notification_id = entity_id.split(".")[1]

        attr: dict[str, str] = {_ATTR_MESSAGE: message}
        if title is not None:
            attr[_ATTR_TITLE] = title
            attr[core.Const.ATTR_FRIENDLY_NAME] = title

        self._shc.states.async_set(entity_id, _STATE, attr, context=context)

        # Store notification and fire event
        # This will eventually replace state machine storage
        self._notifications[entity_id] = {
            _ATTR_MESSAGE: message,
            _ATTR_NOTIFICATION_ID: notification_id,
            _ATTR_STATUS: _NotificationStatus.UNREAD.value,
            _ATTR_TITLE: title,
            _ATTR_CREATED_AT: core.helpers.utcnow(),
        }

        self._shc.bus.async_fire(
            _EVENT_PERSISTENT_NOTIFICATIONS_UPDATED, context=context
        )

    @core.callback
    def async_dismiss(
        self,
        notification_id: str,
        *,
        context: core.Context = None,
    ) -> None:
        """Remove a notification."""

        entity_id = f"{self.domain}.{core.helpers.slugify(notification_id)}"

        if entity_id not in self._notifications:
            return

        self._shc.states.async_remove(entity_id, context)

        del self._notifications[entity_id]
        self._shc.bus.async_fire(_EVENT_PERSISTENT_NOTIFICATIONS_UPDATED)

    async def async_setup(self, config: core.ConfigType) -> bool:
        """Set up the persistent notification component."""
        api = self.controller.components.websocket_api
        if not isinstance(api, core.WebSocket.Component):
            api = None

        #  pylint: disable=no-member
        if not await super().async_setup(config):
            return False

        self._shc.services.async_register(
            self.domain,
            "create",
            self._create_service,
            vol.Schema(
                {
                    vol.Required(_ATTR_MESSAGE): vol.Any(
                        _cv.dynamic_template, _cv.string
                    ),
                    vol.Optional(_ATTR_TITLE): vol.Any(
                        _cv.dynamic_template, _cv.string
                    ),
                    vol.Optional(_ATTR_NOTIFICATION_ID): _cv.string,
                }
            ),
        )

        self._shc.services.async_register(
            self.domain,
            "dismiss",
            self._dismiss_service,
            _SCHEMA_SERVICE_NOTIFICATION,
        )

        self._shc.services.async_register(
            self.domain,
            "mark_read",
            self._mark_read_service,
            _SCHEMA_SERVICE_NOTIFICATION,
        )

        if api is not None:
            api.register_command(self._get_notifications, _LIST_NOTIFICATIONS)
        else:
            self.controller.setup.async_when_setup_or_start(
                "websocket_api", self._register_websocket_command
            )

        return True

    async def _register_websocket_command(
        self, shc: core.SmartHomeController, _domain: str
    ):
        api = shc.components.websocket_api
        if isinstance(api, core.WebSocket.Component):
            api.register_command(self._get_notifications, _LIST_NOTIFICATIONS)

    @core.callback
    def _create_service(self, call: core.ServiceCall) -> None:
        """Handle a create notification service call."""
        self.async_create(
            call.data[_ATTR_MESSAGE],
            call.data.get(_ATTR_TITLE),
            call.data.get(_ATTR_NOTIFICATION_ID),
            context=call.context,
        )

    @core.callback
    def _dismiss_service(self, call: core.ServiceCall) -> None:
        """Handle the dismiss notification service call."""
        self.async_dismiss(call.data[_ATTR_NOTIFICATION_ID], context=call.context)

    @core.callback
    def _mark_read_service(self, call: core.ServiceCall) -> None:
        """Handle the mark_read notification service call."""
        notification_id = call.data.get(_ATTR_NOTIFICATION_ID)
        entity_id = f"{self.domain}.{core.helpers.slugify(notification_id)}"

        if entity_id not in self._notifications:
            _LOGGER.error(
                "Marking persistent_notification read failed: "
                + f"Notification ID {notification_id} not found",
            )
            return

        self._notifications[entity_id][_ATTR_STATUS] = _NotificationStatus.READ.value
        self._shc.bus.async_fire(
            _EVENT_PERSISTENT_NOTIFICATIONS_UPDATED, context=call.context
        )

    @core.callback
    def _get_notifications(
        self,
        connection: core.WebSocket.Connection,
        msg: collections.abc.Mapping[str, typing.Any],
    ) -> None:
        """Return a list of persistent_notifications."""
        connection.send_result(
            msg["id"],
            [
                {
                    key: data[key]
                    for key in (
                        _ATTR_NOTIFICATION_ID,
                        _ATTR_MESSAGE,
                        _ATTR_STATUS,
                        _ATTR_TITLE,
                        _ATTR_CREATED_AT,
                    )
                }
                for data in self._notifications.values()
            ],
        )
