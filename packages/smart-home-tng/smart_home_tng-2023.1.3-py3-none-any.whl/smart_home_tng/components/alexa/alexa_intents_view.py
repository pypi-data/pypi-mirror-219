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
from .alexa_intent import AlexaIntent

_alexa: typing.TypeAlias = core.Alexa
_intent: typing.TypeAlias = core.Intent
_const: typing.TypeAlias = core.Const

_LOGGER: typing.Final = logging.getLogger(__name__)

_HANDLERS: typing.Final[
    core.Registry[
        str,
        typing.Callable[
            [core.SmartHomeControllerComponent, _alexa.Intent],
            typing.Awaitable[_alexa.IntentResponse],
        ],
    ]
] = core.Registry()

_INTENTS_API_ENDPOINT: typing.Final = "/api/alexa"


SPEECH_MAPPINGS = {
    "plain": _alexa.SpeechType.PLAIN_TEXT,
    "ssml": _alexa.SpeechType.SSML,
    core.Intent.SpeechType.PLAIN: _alexa.SpeechType.PLAIN_TEXT,
    core.Intent.SpeechType.SSML: _alexa.SpeechType.SSML,
}


class UnknownRequest(core.SmartHomeControllerError):
    """When an unknown Alexa request is passed in."""


# pylint: disable=unused-variable
class AlexaIntentsView(core.SmartHomeControllerView):
    """Handle Alexa requests."""

    def __init__(self, owner: core.SmartHomeControllerComponent):
        url = _INTENTS_API_ENDPOINT
        name = "api:alexa"
        super().__init__(url, name)
        self._owner = owner

    async def post(self, request):
        """Handle Alexa."""
        # controller = request.app[_const.KEY_SHC]
        user = request[_const.KEY_SHC_USER]
        message: dict = await request.json()
        token = (
            message.get("context", {})
            .get("System", {})
            .get("person", {})
            .get("accessToken")
        )
        if token is not None:
            refresh_token = (
                await self._owner.controller.auth.async_validate_access_token(token)
            )
            if refresh_token is not None:
                user = refresh_token.user
        else:
            token = (
                message.get("context", {})
                .get("System", {})
                .get("user", {})
                .get("accessToken")
            )
            if token is not None:
                refresh_token = (
                    await self._owner.controller.auth.async_validate_access_token(token)
                )
                if refresh_token is not None:
                    user = refresh_token.user

        _LOGGER.debug(f"Received Alexa request: {message}")

        intent = AlexaIntent(message, user)
        try:
            response = await _async_handle_message(self._owner, intent)
            if response is None:
                return self.json(
                    {"version": "1.0", "response": {"shouldEndSession": True}}
                )
            return self.json(response.as_dict())
        except UnknownRequest as err:
            _LOGGER.warning(str(err))
            return self.json(_intent_error_response(intent, str(err)))

        except _intent.UnknownIntent as err:
            _LOGGER.warning(str(err))
            return self.json(
                _intent_error_response(
                    intent, "Diese Intention wurde noch nicht konfiguriert.", str(err)
                )
            )

        except _intent.InvalidSlotInfo as err:
            _LOGGER.error(f"Received invalid slot data from Alexa: {err}")
            return self.json(
                _intent_error_response(
                    intent,
                    "Invalid slot information received for this intent.",
                    str(err),
                )
            )

        except _intent.IntentError as err:
            _LOGGER.exception(str(err))
            return self.json(
                _intent_error_response(intent, "Error handling intent.", str(err))
            )


def _intent_error_response(intent: AlexaIntent, error: str, error_info: str = None):
    """Return an Alexa response that will speak the error message."""
    alexa_response = intent.create_error_response(error, error_info)
    return alexa_response.as_dict()


def _intent_permission_required(intent: AlexaIntent, permissions: list[str]):
    """Return an Alexa response that will speak the error message."""
    alexa_response = intent.create_response()
    alexa_response.add_card(
        _alexa.CardType.ASK_FOR_PERMISSIONS_CONSENT, None, permissions
    )
    alexa_response.add_speech(
        _alexa.SpeechType.PLAIN_TEXT,
        "Um die Anfrage abzuschließen, benötigt Jarvis Zugriff auf deinen Vornamen. "
        + "Um fortzufahren, gehe zum Startbildschirm deiner Alexa-App und gewähre die "
        + "Berechtigungen.",
    )
    return alexa_response


async def _async_handle_message(
    owner: core.SmartHomeControllerComponent, intent: AlexaIntent
):
    """Handle an Alexa intent.

    Raises:
     - UnknownRequest
     - intent.UnknownIntent
     - intent.InvalidSlotInfo
     - intent.IntentError

    """
    if intent is None:
        return None

    handler = _HANDLERS.get(intent.application)
    if handler is None and not (handler := _HANDLERS.get(intent.type)):
        raise UnknownRequest(f"Received unknown request {intent.type}")

    return await handler(owner, intent)


# Flat intent processing with intent scripts (as in home-assistant)
@_HANDLERS.register("SessionEndedRequest")
@_HANDLERS.register("IntentRequest")
@_HANDLERS.register("LaunchRequest")
async def _async_handle_intent(
    owner: core.SmartHomeControllerComponent, intent: AlexaIntent
):
    """Handle an intent request.

    Raises:
     - intent.UnknownIntent
     - intent.InvalidSlotInfo
     - intent.IntentError

    """
    alexa_response = intent.create_response()

    intent_response = await owner.controller.intents.async_handle_intent(
        owner.domain,
        intent.qualified_name,
        {key: {"value": value} for key, value in alexa_response.variables.items()},
    )

    for intent_speech, alexa_speech in SPEECH_MAPPINGS.items():
        if intent_speech in intent_response.speech:
            alexa_response.add_speech(
                alexa_speech, intent_response.speech[intent_speech]["speech"]
            )
        if intent_speech in intent_response.reprompt:
            alexa_response.add_reprompt(
                alexa_speech, intent_response.reprompt[intent_speech]["reprompt"]
            )

    if "simple" in intent_response.card:
        alexa_response.add_card(
            _alexa.CardType.SIMPLE,
            intent_response.card["simple"]["title"],
            intent_response.card["simple"]["content"],
        )

    return alexa_response
