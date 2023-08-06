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

_alexa: typing.TypeAlias = core.Alexa

_LOGGER: typing.Final = logging.getLogger(__name__)


# pylint: disable=unused-variable
class AlexaIntentResponse(_alexa.IntentResponse):
    """Help generating the response for Alexa."""

    def __init__(self, intent: _alexa.Intent, should_end_session: bool = True):
        """Initialize the response."""
        self._speech = None
        self._card = None
        self._reprompt = None
        self._session_attributes = {}
        self._should_end_session = should_end_session
        self._variables: dict[str, any] = {}
        self._directives: list[dict[str, any]] = None
        self._new_session: bool = False

        # Intent is None if request was a LaunchRequest or SessionEndedRequest
        if intent is not None:
            for key, value in intent.slots.items():
                # Only include slots with values
                if "value" not in value:
                    continue

                _key = key.replace(".", "_")

                self._variables[_key] = _resolve_slot_synonyms(key, value)
            self._session_attributes = intent.session_attributes
            self._new_session = intent.new_session

    @property
    def in_active_conversation(self) -> bool:
        return not self._new_session

    @property
    def variables(self):
        return self._variables

    def add_card(self, card_type: _alexa.CardType, title: str, content: str):
        """Add a card to the response."""
        assert self._card is None

        card = {"type": card_type.value}

        if card_type == _alexa.CardType.LINK_ACCOUNT:
            self._card = card
            return
        if card_type == _alexa.CardType.ASK_FOR_PERMISSIONS_CONSENT:
            card["permissions"] = content
            self._card = card
            return

        card["title"] = title
        card["content"] = content
        self._card = card

    def add_speech(self, speech_type: _alexa.SpeechType, text: str):
        """Add speech to the response."""
        assert self._speech is None

        key = "ssml" if speech_type == _alexa.SpeechType.SSML else "text"

        self._speech = {"type": speech_type.value, key: text}

    def add_reprompt(self, speech_type: _alexa.SpeechType, text: str):
        """Add reprompt if user does not answer."""
        assert self._reprompt is None

        key = "ssml" if speech_type == _alexa.SpeechType.SSML else "text"

        self._should_end_session = False

        self._reprompt = {"type": speech_type.value, key: text}

    def audio_player_play(
        self,
        stream: str,
        title: str,
        sub_title: str,
        image: str,
        play_behaviour: str = "REPLACE_ALL",
        token: str = None,
        previous_token: str = None,
        offset: int = 0,
    ) -> None:
        """Add a AudioPlayer.Play directive to the response."""
        directive: dict[str, any] = {}
        directive["type"] = "AudioPlayer.Play"
        directive["playBehavior"] = play_behaviour
        stream: dict[str, any] = {
            "url": stream,
            "token": token,
            "offsetInMilliseconds": offset,
        }
        if play_behaviour == "ENQUEUE":
            stream["expectedPreviousToken"] = previous_token
        directive["audioItem"] = {
            "stream": stream,
            "metadata": {
                "title": title,
                "subtitle": sub_title,
                "art": {"sources": [{"url": image}]},
            },
        }
        if self._directives is None:
            self._directives = []
        self._directives.append(directive)

    def as_dict(self):
        """Return response in an Alexa valid dict."""
        response = {"shouldEndSession": self._should_end_session}

        if self._card is not None:
            response["card"] = self._card

        if self._speech is not None:
            response["outputSpeech"] = self._speech

        if self._reprompt is not None:
            response["reprompt"] = {"outputSpeech": self._reprompt}

        if self._directives is not None and len(self._directives) > 0:
            response["directives"] = self._directives

        return {
            "version": "1.0",
            "sessionAttributes": self._session_attributes,
            "response": response,
        }


def _resolve_slot_synonyms(key: str, request: dict):
    """Check slot request for synonym resolutions."""
    # Default to the spoken slot value if more than one or none are found. For
    # reference to the request object structure, see the Alexa docs:
    # https://tinyurl.com/ybvm7jhs
    resolved_value = request["value"]

    if (
        "resolutions" in request
        and "resolutionsPerAuthority" in request["resolutions"]
        and len(request["resolutions"]["resolutionsPerAuthority"]) >= 1
    ):
        # Extract all of the possible values from each authority with a
        # successful match
        possible_values = []

        for entry in request["resolutions"]["resolutionsPerAuthority"]:
            if entry["status"]["code"] != _alexa.SYN_RESOLUTION_MATCH:
                continue

            possible_values.extend([item["value"]["name"] for item in entry["values"]])

        # If there is only one match use the resolved value, otherwise the
        # resolution cannot be determined, so use the spoken slot value
        if len(possible_values) == 1:
            resolved_value = possible_values[0]
        else:
            _LOGGER.debug(
                "Found multiple synonym resolutions for slot value: {"
                + f"{key}: {resolved_value}"
                + "}",
            )

    return resolved_value
