"""
Webhook Component for Smart Home - The Next Generation.

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
import functools
import http
import ipaddress
import logging
import secrets
import typing

import voluptuous as vol
from aiohttp import hdrs, web

from ... import core
from .webhook_view import WebhookView

_cv: typing.TypeAlias = core.ConfigValidation

_LOGGER: typing.Final = logging.getLogger(__name__)

_LIST_WEBHOOKS: typing.Final = {
    "type": "webhook/list",
}
_HANDLE_WEBHOOK: typing.Final = {
    vol.Required("type"): "webhook/handle",
    vol.Required("webhook_id"): str,
    vol.Required("method"): vol.In(["GET", "POST", "PUT"]),
    vol.Optional("body", default=""): str,
    vol.Optional("headers", default={}): {str: str},
    vol.Optional("query", default=""): str,
}
_TRIGGER_SCHEMA: typing.Final = _cv.TRIGGER_BASE_SCHEMA.extend(
    {
        vol.Required(core.Const.CONF_PLATFORM): "webhook",
        vol.Required(core.Const.CONF_WEBHOOK_ID): _cv.string,
    }
)


# pylint: disable=unused-variable
class WebhookComponent(core.WebhookComponent, core.TriggerPlatform):
    """Webhooks for Smart Home - The Next Generation."""

    def __init__(self, path: typing.Iterable[str]):
        super().__init__(path)
        self._handlers: dict[str, dict[str, typing.Any]] = {}
        self._supported_platforms = frozenset([core.Platform.TRIGGER])

    async def async_setup(self, config: core.ConfigType) -> bool:
        """Initialize the webhook component."""
        if not await super().async_setup(config):
            return False

        websocket_api = self.controller.components.websocket_api
        if not isinstance(websocket_api, core.WebSocket.Component):
            return False

        self._shc.register_view(WebhookView(self))
        websocket_api.register_command(self._list_webhooks, _LIST_WEBHOOKS)
        websocket_api.register_command(self._handle_webhook, _HANDLE_WEBHOOK)
        return True

    @core.callback
    def _list_webhooks(
        self,
        connection: core.WebSocket.Connection,
        msg: dict,
    ):
        """Return a list of webhooks."""
        handlers = self._handlers
        result = [
            {
                "webhook_id": webhook_id,
                "domain": info["domain"],
                "name": info["name"],
                "local_only": info["local_only"],
            }
            for webhook_id, info in handlers.items()
        ]

        connection.send_result(msg["id"], result)

    async def _handle_webhook(
        self,
        connection: core.WebSocket.Connection,
        msg: dict,
    ):
        """Handle an incoming webhook via the WS API."""
        request = core.MockRequest(
            content=msg["body"].encode("utf-8"),
            headers=msg["headers"],
            method=msg["method"],
            query_string=msg["query"],
            mock_source=f"{self.domain}/ws",
        )

        response = await self.async_handle_webhook(msg["webhook_id"], request)

        response_dict = core.helpers.serialize_response(response)
        body = response_dict.get("body")

        connection.send_result(
            msg["id"],
            {
                "body": body,
                "status": response_dict["status"],
                "headers": {"Content-Type": response.content_type},
            },
        )

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
        handlers = self._handlers

        if webhook_id in handlers:
            raise ValueError("Handler is already defined!")

        handlers[webhook_id] = {
            "domain": domain,
            "name": name,
            "handler": handler,
            "local_only": local_only,
        }

    def unregister_webhook(self, webhook_id: str) -> None:
        """Remove a webhook."""
        self._handlers.pop(webhook_id, None)

    def async_generate_id(self) -> str:
        """Generate a webhook_id."""
        return secrets.token_hex(32)

    def async_generate_url(self, webhook_id: str) -> str:
        """Generate the full URL for a webhook_id."""
        my_url = self._shc.get_url(prefer_external=True)
        path = self.async_generate_path(webhook_id)
        return f"{my_url}{path}"

    def async_generate_path(self, webhook_id: str) -> str:
        return f"/api/webhook/{webhook_id}"

    async def async_handle_webhook(
        self, webhook_id: str, request: web.Request
    ) -> web.Response:
        """Handle a webhook."""
        handlers = self._handlers

        # Always respond successfully to not give away if a hook exists or not.
        if (webhook := handlers.get(webhook_id)) is None:
            if isinstance(request, core.MockRequest):
                received_from = request.mock_source
            else:
                received_from = request.remote

            _LOGGER.info(
                f"Received message for unregistered webhook {webhook_id} from {received_from}",
            )
            # Look at content to provide some context for received webhook
            # Limit to 64 chars to avoid flooding the log
            content = await request.content.read(64)
            _LOGGER.debug(f"{content}")
            return web.Response(status=http.HTTPStatus.OK)

        if webhook["local_only"]:
            try:
                remote = ipaddress.ip_address(request.remote)
            except ValueError:
                _LOGGER.debug(f"Unable to parse remote ip {request.remote}")
                return web.Response(status=http.HTTPStatus.OK)

            if not core.helpers.is_local(remote):
                _LOGGER.warning(
                    f"Received remote request for local webhook {webhook_id}"
                )
                return web.Response(status=http.HTTPStatus.OK)

        try:
            response = await webhook["handler"](webhook_id, request)
            if response is None:
                response = web.Response(status=http.HTTPStatus.OK)
            return response
        except Exception:  # pylint: disable=broad-except
            _LOGGER.exception(f"Error processing webhook {webhook_id}")
            return web.Response(status=http.HTTPStatus.OK)

    async def async_attach_trigger(
        self,
        config: core.ConfigType,
        action: core.TriggerActionType,
        trigger_info: core.TriggerInfo,
    ) -> core.CallbackType:
        """Trigger based on incoming webhooks."""
        trigger_data = trigger_info["trigger_data"]
        webhook_id: str = config[core.Const.CONF_WEBHOOK_ID]
        job = core.SmartHomeControllerJob(action)
        self.register_webhook(
            trigger_info["domain"],
            trigger_info["name"],
            webhook_id,
            functools.partial(self._handle_trigger, job, trigger_data),
        )

        @core.callback
        def unregister():
            """Unregister webhook."""
            self.unregister_webhook(webhook_id)

        return unregister

    async def async_validate_trigger_config(
        self, config: core.ConfigType
    ) -> core.ConfigType:
        return _TRIGGER_SCHEMA(config)

    async def _handle_trigger(
        self,
        job: core.SmartHomeControllerJob,
        trigger_data,
        webhook_id: str,
        request: web.Request,
    ):
        """Handle incoming webhook."""
        result = {"platform": "webhook", "webhook_id": webhook_id}

        if "json" in request.headers.get(hdrs.CONTENT_TYPE, ""):
            result["json"] = await request.json()
        else:
            result["data"] = await request.post()

        result["query"] = request.query
        result["description"] = "webhook"
        result.update(**trigger_data)
        self._shc.async_run_shc_job(job, {"trigger": result})
