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

from ... import core
from .alexa_config import AlexaConfig
from .alexa_response import AlexaResponse
from .entity_wrapper import _ENTITY_ADAPTERS

_alexa: typing.TypeAlias = core.Alexa

_LOGGER: typing.Final = logging.getLogger(__name__)


# pylint: disable=unused-variable
class AlexaDirective:
    """An incoming Alexa directive."""

    def __init__(self, request: core.JsonType):
        """Initialize a directive."""
        self._directive = request[_alexa.API_DIRECTIVE]
        self._namespace = self._directive[_alexa.API_HEADER]["namespace"]
        self._name = self._directive[_alexa.API_HEADER]["name"]
        self._payload = self._directive[_alexa.API_PAYLOAD]
        self._has_endpoint = _alexa.API_ENDPOINT in self._directive

        self._entity = self._entity_id = self._endpoint = self._instance = None

    @property
    def entity(self) -> core.State:
        return self._entity

    @property
    def entity_id(self) -> str:
        return self._entity_id

    @property
    def name(self) -> str:
        return self._name

    @property
    def namespace(self) -> str:
        return self._namespace

    @property
    def has_endpoint(self) -> bool:
        return self._has_endpoint

    @property
    def endpoint(self) -> str:
        return self._endpoint

    @property
    def instance(self) -> str:
        return self._instance

    @property
    def payload(self):
        return self._payload

    def load_entity(self, controller: core.SmartHomeController, config: AlexaConfig):
        """Set attributes related to the entity for this request.

        Sets these attributes when self.has_endpoint is True:

        - entity
        - entity_id
        - endpoint
        - instance (when header includes instance property)

        Behavior when self.has_endpoint is False is undefined.

        Will raise AlexaInvalidEndpointError if the endpoint in the request is
        malformed or nonexistent.
        """
        endpoint_id = self._directive[_alexa.API_ENDPOINT]["endpointId"]
        self._entity_id = endpoint_id.replace("#", ".")

        self._entity = controller.states.get(self._entity_id)
        if not self._entity or not config.should_expose(self._entity_id):
            raise _alexa.InvalidEndpointError(endpoint_id)

        self._endpoint = _ENTITY_ADAPTERS[self._entity.domain](
            controller, config, self._entity
        )
        if "instance" in self._directive[_alexa.API_HEADER]:
            self._instance = self._directive[_alexa.API_HEADER]["instance"]

    def response(self, name="Response", namespace="Alexa", payload=None):
        """Create an API formatted response.

        Async friendly.
        """
        response = AlexaResponse(name, namespace, payload)

        token = self._directive[_alexa.API_HEADER].get("correlationToken")
        if token:
            response.set_correlation_token(token)

        if self._has_endpoint:
            response.set_endpoint(self._directive[_alexa.API_ENDPOINT].copy())

        return response

    def error(
        self,
        namespace="Alexa",
        error_type="INTERNAL_ERROR",
        error_message="",
        payload=None,
    ):
        """Create a API formatted error response.

        Async friendly.
        """
        payload = payload or {}
        payload["type"] = error_type
        payload["message"] = error_message

        _LOGGER.info(
            f"Request {self._namespace}/{self._name} error {error_type}: {error_message}",
        )

        return self.response(name="ErrorResponse", namespace=namespace, payload=payload)
