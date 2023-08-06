"""
System Log Component for Smart Home - The Next Generation.

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

import logging
import logging.handlers
import queue
import typing

import voluptuous as vol

from ... import core
from .const import Const
from .log_error_handler import LogErrorHandler
from .log_error_queue_handler import LogErrorQueueHandler

_cv: typing.TypeAlias = core.ConfigValidation

_LIST_ERRORS: typing.Final = {vol.Required("type"): "system_log/list"}


# pylint: disable=unused-variable
class SystemLogComponent(core.SmartHomeControllerComponent):
    """Support for system log."""

    def __init__(self, path: typing.Iterable[str]):
        super().__init__(path)
        self._handler: LogErrorHandler = None
        self._queue_handler: LogErrorQueueHandler = None
        self._listener: logging.handlers.QueueListener = None

    async def async_validate_config(self, config: core.ConfigType) -> core.ConfigType:
        schema = vol.Schema(
            {
                self.domain: vol.Schema(
                    {
                        vol.Optional(
                            Const.CONF_MAX_ENTRIES, default=Const.DEFAULT_MAX_ENTRIES
                        ): _cv.positive_int,
                        vol.Optional(
                            Const.CONF_FIRE_EVENT, default=Const.DEFAULT_FIRE_EVENT
                        ): _cv.boolean,
                    }
                )
            },
            extra=vol.ALLOW_EXTRA,
        )
        return schema(config)

    async def async_setup(self, config: core.ConfigType) -> bool:
        """Set up the logger component."""
        if not await super().async_setup(config):
            return False

        if (conf := config.get(self.domain)) is None:
            conf = (await self.async_validate_config({self.domain: {}}))[self.domain]

        shc = self._shc
        simple_queue: queue.SimpleQueue = queue.SimpleQueue()
        queue_handler = LogErrorQueueHandler(simple_queue)
        queue_handler.setLevel(logging.WARN)
        logging.root.addHandler(queue_handler)

        handler = LogErrorHandler(
            shc, conf[Const.CONF_MAX_ENTRIES], conf[Const.CONF_FIRE_EVENT]
        )

        self._queue_handler = queue_handler
        self._handler = handler

        self._listener = logging.handlers.QueueListener(
            simple_queue, handler, respect_handler_level=True
        )

        self._listener.start()

        shc.bus.async_listen_once(
            core.Const.EVENT_SHC_CLOSE, self._async_stop_queue_handler
        )

        websocket_api = self.controller.components.websocket_api
        if not isinstance(websocket_api, core.WebSocket.Component):
            return False

        websocket_api.register_command(self._list_errors, _LIST_ERRORS)

        shc.bus.async_listen_once(
            core.Const.EVENT_SHC_STOP, self._async_shutdown_handler
        )

        shc.services.async_register(
            self.domain,
            Const.SERVICE_CLEAR,
            self._async_service_handler,
            schema=Const.SERVICE_CLEAR_SCHEMA,
        )
        shc.services.async_register(
            self.domain,
            Const.SERVICE_WRITE,
            self._async_service_handler,
            schema=Const.SERVICE_WRITE_SCHEMA,
        )

        return True

    @core.callback
    def _async_stop_queue_handler(self, _) -> None:
        """Cleanup handler."""
        if self._queue_handler is not None:
            logging.root.removeHandler(self._queue_handler)
            self._queue_handler = None
        if self._listener is not None:
            self._listener.stop()
            self._listener = None

    async def _async_service_handler(self, service: core.ServiceCall) -> None:
        """Handle logger services."""
        if service.service == "clear":
            if self._handler is not None:
                self._handler.records.clear()
            return
        if service.service == "write":
            logger = logging.getLogger(
                service.data.get(Const.CONF_LOGGER, f"{__name__}.external")
            )
            level = service.data[Const.CONF_LEVEL]
            getattr(logger, level)(service.data[Const.CONF_MESSAGE])

    async def _async_shutdown_handler(self, _event):
        """Remove logging handler when Home Assistant is shutdown."""
        # This is needed as older logger instances will remain
        if self._handler is not None:
            logging.getLogger().removeHandler(self._handler)
            self._handler = None

    @core.callback
    def _list_errors(
        self,
        connection: core.WebSocket.Connection,
        msg: dict,
    ):
        """List all possible diagnostic handlers."""
        connection.require_admin()
        connection.send_result(
            msg["id"],
            self._handler.records.to_list(),
        )
