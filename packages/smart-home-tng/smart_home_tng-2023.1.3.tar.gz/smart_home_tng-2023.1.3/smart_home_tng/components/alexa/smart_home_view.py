"""
Amazon Alexa Integration for Smart Home - The Next Generation.

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
import typing

from aiohttp import web

from ... import core
from .alexa_config import AlexaConfig
from .alexa_directive import AlexaDirective
from .handlers import _HANDLERS

_alexa: typing.TypeAlias = core.Alexa
_const: typing.TypeAlias = core.Const

_LOGGER: typing.Final = logging.getLogger(__name__)
_SMART_HOME_HTTP_ENDPOINT: typing.Final = "/api/alexa/smart_home"


# pylint: disable=unused-variable
class SmartHomeView(core.SmartHomeControllerView):
    """Expose Smart Home v3 payload interface via HTTP POST."""

    def __init__(self, owner: core.Alexa.Component, smart_home_config: AlexaConfig):
        """Initialize."""
        url = _SMART_HOME_HTTP_ENDPOINT
        name = "api:alexa:smart_home"
        super().__init__(url, name)
        self._smart_home_config = smart_home_config
        self._owner = owner

    async def post(self, request: web.Request):
        """Handle Alexa Smart Home requests.

        The Smart Home API requires the endpoint to be implemented in AWS
        Lambda, which will need to forward the requests to here and pass back
        the response.
        """
        controller = request.app[_const.KEY_SHC]
        user = request[_const.KEY_SHC_USER]
        message: dict = await request.json()

        _LOGGER.debug(f"Received Alexa Smart Home request: {message}")

        response = await self.async_handle_message(
            controller,
            self._smart_home_config,
            message,
            context=core.Context(user_id=user.id),
        )
        _LOGGER.debug(f"Sending Alexa Smart Home response: {response}")
        return b"" if response is None else self.json(response)

    async def async_handle_message(
        self,
        controller: core.SmartHomeController,
        config: _alexa.AbstractConfig,
        request: dict,
        context=None,
        enabled=True,
    ):
        """Handle incoming API messages.

        If enabled is False, the response to all messages will be a
        BRIDGE_UNREACHABLE error. This can be used if the API has been disabled in
        configuration.
        """
        assert request[_alexa.API_DIRECTIVE][_alexa.API_HEADER]["payloadVersion"] == "3"

        if context is None:
            context = core.Context()

        directive = AlexaDirective(request)

        try:
            if not enabled:
                raise _alexa.BridgeUnreachableError(
                    "Alexa API not enabled in Home Assistant configuration"
                )

            await config.set_authorized(True)

            if directive.has_endpoint:
                directive.load_entity(controller, config)

            funct_ref = _HANDLERS.get((directive.namespace, directive.name))
            if funct_ref:
                response = await funct_ref(self._owner, config, directive, context)
                if directive.has_endpoint:
                    response.merge_context_properties(directive.endpoint)
            else:
                _LOGGER.warning(
                    f"Unsupported API request {directive.namespace}/{directive.name}"
                )
                response = directive.error()
        except _alexa.Error as err:
            response = directive.error(
                error_type=err.error_type,
                error_message=err.error_message,
                payload=err.payload,
            )
        except Exception:  # pylint: disable=broad-except
            _LOGGER.exception(
                f"Uncaught exception processing Alexa {directive.namespace}/{directive.name} "
                + f"request ({directive.entity_id or '-'})",
            )
            response = directive.error(error_message="Unknown error")

        request_info = {"namespace": directive.namespace, "name": directive.name}

        if directive.has_endpoint:
            request_info["entity_id"] = directive.entity_id

        controller.bus.async_fire(
            _alexa.EVENT_ALEXA_SMART_HOME,
            {
                "request": request_info,
                "response": {"namespace": response.namespace, "name": response.name},
            },
            context=context,
        )

        return response.serialize()
