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

import typing
import uuid

from ... import core

_alexa: typing.TypeAlias = core.Alexa


# pylint: disable=unused-variable
class AlexaResponse:
    """Class to hold a response."""

    def __init__(self, name: str, namespace: str, payload=None):
        """Initialize the response."""
        payload = payload or {}
        self._response = {
            _alexa.API_EVENT: {
                _alexa.API_HEADER: {
                    "namespace": namespace,
                    "name": name,
                    "messageId": str(uuid.uuid4()),
                    "payloadVersion": "3",
                },
                _alexa.API_PAYLOAD: payload,
            }
        }

    @property
    def name(self):
        """Return the name of this response."""
        return self._response[_alexa.API_EVENT][_alexa.API_HEADER]["name"]

    @property
    def namespace(self):
        """Return the namespace of this response."""
        return self._response[_alexa.API_EVENT][_alexa.API_HEADER]["namespace"]

    def set_correlation_token(self, token: str):
        """Set the correlationToken.

        This should normally mirror the value from a request, and is set by
        AlexaDirective.response() usually.
        """
        self._response[_alexa.API_EVENT][_alexa.API_HEADER]["correlationToken"] = token

    def set_endpoint_full(self, bearer_token: str, endpoint_id: str, cookie=None):
        """Set the endpoint dictionary.

        This is used to send proactive messages to Alexa.
        """
        self._response[_alexa.API_EVENT][_alexa.API_ENDPOINT] = {
            _alexa.API_SCOPE: {"type": "BearerToken", "token": bearer_token}
        }

        if endpoint_id is not None:
            self._response[_alexa.API_EVENT][_alexa.API_ENDPOINT][
                "endpointId"
            ] = endpoint_id

        if cookie is not None:
            self._response[_alexa.API_EVENT][_alexa.API_ENDPOINT]["cookie"] = cookie

    def set_endpoint(self, endpoint: str):
        """Set the endpoint.

        This should normally mirror the value from a request, and is set by
        AlexaDirective.response() usually.
        """
        self._response[_alexa.API_EVENT][_alexa.API_ENDPOINT] = endpoint

    @property
    def _properties(self):
        context = self._response.setdefault(_alexa.API_CONTEXT, {})
        return context.setdefault("properties", [])

    def add_context_property(self, prop):
        """Add a property to the response context.

        The Alexa response includes a list of properties which provides
        feedback on how states have changed. For example if a user asks,
        "Alexa, set thermostat to 20 degrees", the API expects a response with
        the new value of the property, and Alexa will respond to the user
        "Thermostat set to 20 degrees".

        async_handle_message() will call .merge_context_properties() for every
        request automatically, however often handlers will call services to
        change state but the effects of those changes are applied
        asynchronously. Thus, handlers should call this method to confirm
        changes before returning.
        """
        self._properties.append(prop)

    def merge_context_properties(self, endpoint):
        """Add all properties from given endpoint if not already set.

        Handlers should be using .add_context_property().
        """
        properties = self._properties
        already_set = {(p["namespace"], p["name"]) for p in properties}

        for prop in endpoint.serialize_properties():
            if (prop["namespace"], prop["name"]) not in already_set:
                self.add_context_property(prop)

    def serialize(self):
        """Return response as a JSON-able data structure."""
        return self._response
