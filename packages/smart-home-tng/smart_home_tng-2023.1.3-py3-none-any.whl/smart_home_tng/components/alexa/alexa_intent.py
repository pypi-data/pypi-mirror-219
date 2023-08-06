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

from ... import core, auth
from .alexa_intent_response import AlexaIntentResponse

_alexa: typing.TypeAlias = core.Alexa


# pylint: disable=unused-variable
class AlexaIntent(_alexa.Intent):
    """Amazon Alexa Intent implementation."""

    def __init__(self, message: dict[str, any], user: auth.User = None):
        self._message = message
        self._locale: str = "de-DE"
        self._request: dict[str, any] = None
        self._session: dict[str, any] = None
        self._session_attributes: dict[str, str] = {}
        self._intent_info: dict[str, any] = None
        self._slots: dict[str, any] = {}
        self._application: str = ""
        self._user = user
        self._context: dict[str, any] = {}

        if message is not None:
            self._request = message.get("request", {})
            self._locale = self._request.get("locale", "de-DE")
            self._session = message.get("session", {})
            self._session_attributes = self._session.get("attributes", {})
            self._context = message.get("context", {})
            self._application = (
                self._context.get("System", {})
                .get("application", {})
                .get("applicationId", "")
            )
            if self._application == "":
                self._application = self._session.get("application", {}).get(
                    "applicationId", ""
                )
            self._intent_info = self._request.get("intent", {})
            self._slots = self._intent_info.get("slots", {})

    @property
    def new_session(self) -> bool:
        return self._message is None or self._message.get("session", {}).get(
            "new", True
        )

    @property
    def user(self) -> auth.User:
        """The user, who started the intent."""
        return self._user

    @property
    def locale(self) -> str:
        return self._locale

    @property
    def slots(self):
        return self._slots

    @property
    def session_attributes(self) -> dict[str, str]:
        return self._session_attributes.copy()

    @property
    def application(self) -> str:
        return self._application

    @property
    def type(self) -> str:
        if self._request is not None:
            return self._request.get("type", "")
        return ""

    @property
    def name(self) -> str:
        if self._request is None:
            return ""
        if self.type != "IntentRequest":
            return self.type
        return self._intent_info.get("name", "")

    @property
    def device_id(self) -> str:
        """the device, on which the intent was started."""
        if self._message is None:
            return None
        return (
            self._message.get("context", {})
            .get("System", {})
            .get("device", {})
            .get("deviceId")
        )

    @property
    def person_id(self) -> str:
        if self._message is None:
            return None
        return (
            self._message.get("context", {})
            .get("System", {})
            .get("person", {})
            .get("personId")
        )

    @property
    def dialog_state(self) -> str:
        if self._request is not None:
            return self._request.get("dialogState")
        return None

    @property
    def supported_interfaces(self) -> dict[str, any]:
        """Get the supported interfaces of the connected device."""
        if self._message is None:
            return None
        return (
            self._message.get("context", {})
            .get("System", {})
            .get("device", {})
            .get("supportedInterfaces")
        )

    def get_interface_context(self, interface: str) -> dict[str, any]:
        if self._message is None:
            return None
        return self._message.get("context", {}).get(interface)

    def create_response(self, should_end_session: bool = True) -> _alexa.IntentResponse:
        return AlexaIntentResponse(self, should_end_session)
