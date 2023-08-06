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
import functools
import http
import logging
import typing

import aiohttp
import async_timeout

from ... import core
from .const import Const

_LOGGER: typing.Final = logging.getLogger(__name__)


# pylint: disable=unused-variable
class MobileAppNotificationService(core.BaseNotificationService):
    """Implement the notification service for mobile_app."""

    def __init__(self, owner: core.SmartHomeControllerComponent):
        """Initialize the service."""
        super().__init__(owner.controller)
        self._local_push_channels = None
        self._config_entries = dict[str, core.ConfigEntry]()

    @property
    def targets(self):
        """Return a dictionary of registered targets."""
        return self.push_registrations()

    def push_registrations(self):
        """Return a dictionary of push enabled registrations."""
        targets = {}

        for webhook_id, entry in self._config_entries.items():
            if not self._supports_push(webhook_id):
                continue

            targets[entry.data[Const.ATTR_DEVICE_NAME]] = webhook_id
        return targets

    def send_message(self, message: str, **kwargs: typing.Any) -> None:
        raise NotImplementedError()

    async def async_send_message(self, message="", **kwargs):
        """Send a message to the Lambda APNS gateway."""
        data = {core.Const.ATTR_MESSAGE: message}

        # Remove default title from notifications.
        if (
            kwargs.get(core.Const.ATTR_TITLE) is not None
            and kwargs.get(core.Const.ATTR_TITLE) != core.Const.ATTR_TITLE_DEFAULT
        ):
            data[core.Const.ATTR_TITLE] = kwargs.get(core.Const.ATTR_TITLE)

        if not (targets := kwargs.get(core.Const.ATTR_TARGET)):
            targets = self.push_registrations().values()

        if kwargs.get(core.Const.ATTR_DATA) is not None:
            data[core.Const.ATTR_DATA] = kwargs.get(core.Const.ATTR_DATA)

        local_push_channels = self._local_push_channels

        for target in targets:
            registration = self._config_entries[target].data

            if target in local_push_channels:
                local_push_channels[target].async_send_notification(
                    data,
                    functools.partial(
                        self._async_send_remote_message_target, target, registration
                    ),
                )
                continue

            # Test if local push only.
            if Const.ATTR_PUSH_URL not in registration[Const.ATTR_APP_DATA]:
                raise core.SmartHomeControllerError(
                    "Device not connected to local push notifications"
                )

            await self._async_send_remote_message_target(target, registration, data)

    async def _async_send_remote_message_target(self, target, registration, data):
        """Send a message to a target."""
        app_data = registration[Const.ATTR_APP_DATA]
        push_token = app_data[Const.ATTR_PUSH_TOKEN]
        push_url = app_data[Const.ATTR_PUSH_URL]

        target_data = dict(data)
        target_data[Const.ATTR_PUSH_TOKEN] = push_token

        reg_info = {
            Const.ATTR_APP_ID: registration[Const.ATTR_APP_ID],
            Const.ATTR_APP_VERSION: registration[Const.ATTR_APP_VERSION],
            Const.ATTR_WEBHOOK_ID: target,
        }
        if Const.ATTR_OS_VERSION in registration:
            reg_info[Const.ATTR_OS_VERSION] = registration[Const.ATTR_OS_VERSION]

        target_data["registration_info"] = reg_info

        try:
            async with async_timeout.timeout(10):
                response = await core.HttpClient.async_get_clientsession(
                    self._shc
                ).post(push_url, json=target_data)
                result = await response.json()

            if response.status in (
                http.HTTPStatus.OK,
                http.HTTPStatus.CREATED,
                http.HTTPStatus.ACCEPTED,
            ):
                _log_rate_limits(registration[Const.ATTR_DEVICE_NAME], result)
                return

            fallback_error = result.get("errorMessage", "Unknown error")
            fallback_message = (
                f"Internal server error, please try again later: {fallback_error}"
            )
            message = result.get("message", fallback_message)

            if "message" in result:
                if message[-1] not in [".", "?", "!"]:
                    message += "."
                message += " This message is generated externally to Home Assistant."

            if response.status == http.HTTPStatus.TOO_MANY_REQUESTS:
                _LOGGER.warning(message)
                _log_rate_limits(
                    registration[Const.ATTR_DEVICE_NAME], result, logging.WARNING
                )
            else:
                _LOGGER.error(message)

        except asyncio.TimeoutError:
            _LOGGER.error(f"Timeout sending notification to {push_url}")
        except aiohttp.ClientError as err:
            _LOGGER.error(f"Error sending notification to {push_url}: {err:r}")

    @core.callback
    def _supports_push(self, webhook_id: str) -> bool:
        """Return if push notifications is supported."""
        config_entry = self._config_entries.get(webhook_id, None)
        if config_entry is None:
            return False

        app_data = config_entry.data[Const.ATTR_APP_DATA]
        return (
            Const.ATTR_PUSH_TOKEN in app_data and Const.ATTR_PUSH_URL in app_data
        ) or Const.ATTR_PUSH_WEBSOCKET_CHANNEL in app_data


def _log_rate_limits(device_name, resp: dict, level=logging.INFO):
    """Output rate limit log line at given level."""
    if Const.ATTR_PUSH_RATE_LIMITS not in resp:
        return

    rate_limits = resp[Const.ATTR_PUSH_RATE_LIMITS]
    resetsAt = rate_limits[Const.ATTR_PUSH_RATE_LIMITS_RESETS_AT]
    resetsAtTime = core.helpers.parse_datetime(resetsAt) - core.helpers.utcnow()
    rate_limit_msg = (
        f"mobile_app push notification rate limits for {device_name}: "
        + f"{rate_limits[Const.ATTR_PUSH_RATE_LIMITS_SUCCESSFUL]:d} sent, "
        + f"{rate_limits[Const.ATTR_PUSH_RATE_LIMITS_MAXIMUM]:d} allowed, "
        + f"{rate_limits[Const.ATTR_PUSH_RATE_LIMITS_ERRORS]} errors, "
        + f"resets in {str(resetsAtTime).split('.', maxsplit=1)[0]}"
    )
    _LOGGER.log(
        level,
        rate_limit_msg,
    )
