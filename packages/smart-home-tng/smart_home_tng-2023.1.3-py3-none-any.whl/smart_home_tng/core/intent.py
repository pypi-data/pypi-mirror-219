"""
Core components of Smart Home - The Next Generation.

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

import abc
import enum
import typing

import voluptuous as vol

from ..backports import strenum
from .callback import callback
from .config_validation import ConfigValidation as _cv
from .const import Const
from .context import Context
from .platform_implementation import PlatformImplementation
from .smart_home_controller_error import SmartHomeControllerError

if not typing.TYPE_CHECKING:

    class SmartHomeController:
        pass


if typing.TYPE_CHECKING:
    from .smart_home_controller import SmartHomeController


_SlotsType = dict[str, typing.Any]


class _SpeechType(strenum.LowercaseStrEnum):
    PLAIN = enum.auto()
    SSML = enum.auto()


class _Intent:
    """Hold the intent."""

    __slots__ = [
        "_shc",
        "_platform",
        "_intent_type",
        "_slots",
        "_text_input",
        "_context",
    ]

    def __init__(
        self,
        shc: SmartHomeController,
        platform: str,
        intent_type: str,
        slots: _SlotsType,
        text_input: str,
        context: Context,
    ) -> None:
        """Initialize an intent."""
        self._shc = shc
        self._platform = platform
        self._intent_type = intent_type
        self._slots = slots
        self._text_input = text_input
        self._context = context

    @property
    def controller(self) -> SmartHomeController:
        return self._shc

    @property
    def platform(self) -> str:
        return self._platform

    @property
    def intent_type(self) -> str:
        return self._intent_type

    @property
    def slots(self) -> _SlotsType:
        return self._slots

    @property
    def text_input(self) -> str:
        return self._text_input

    @property
    def context(self) -> Context:
        return self._context

    @callback
    def create_response(self):
        """Create a response."""
        return _Response(self)


class _Response:
    """Response to an intent."""

    def __init__(self, intent: _Intent = None) -> None:
        """Initialize an IntentResponse."""
        self._intent = intent
        self._speech: dict[str, dict[str, typing.Any]] = {}
        self._reprompt: dict[str, dict[str, typing.Any]] = {}
        self._card: dict[str, dict[str, str]] = {}

    @property
    def card(self):
        return self._card

    @property
    def reprompt(self):
        return self._reprompt

    @property
    def speech(self):
        return self._speech

    @callback
    def async_set_speech(
        self,
        speech: str,
        speech_type: str = _SpeechType.PLAIN,
        extra_data: typing.Any = None,
    ) -> None:
        """Set speech response."""
        self._speech[speech_type] = {"speech": speech, "extra_data": extra_data}

    @callback
    def async_set_reprompt(
        self,
        speech: str,
        speech_type: str = _SpeechType.PLAIN,
        extra_data: typing.Any = None,
    ) -> None:
        """Set reprompt response."""
        self.reprompt[speech_type] = {"reprompt": speech, "extra_data": extra_data}

    @callback
    def async_set_card(
        self, title: str, content: str, card_type: str = "simple"
    ) -> None:
        """Set card response."""
        self.card[card_type] = {"title": title, "content": content}

    @callback
    def as_dict(self) -> dict[str, dict[str, dict[str, typing.Any]]]:
        """Return a dictionary representation of an intent response."""
        return (
            {"speech": self.speech, "reprompt": self.reprompt, "card": self.card}
            if self.reprompt
            else {"speech": self.speech, "card": self.card}
        )


class _Handler:
    """Intent handler registration."""

    def __init__(
        self,
        intent_type: str,
        slot_schema: vol.Schema = None,
        platforms: typing.Iterable[str] = None,
    ):
        """Initialize IntentHandler."""
        self._intent_type = intent_type
        self._slot_schema = slot_schema
        self._compiled_slot_schema = None
        self._platforms = platforms

    @property
    def intent_type(self) -> str:
        return self._intent_type

    @property
    def platforms(self) -> typing.Iterable[str]:
        return self._platforms

    @property
    def slot_schema(self) -> vol.Schema:
        return self._slot_schema

    def can_handle(self, intent_obj: _Intent) -> bool:
        """Test if an intent can be handled."""
        return self.platforms is None or intent_obj.platform in self.platforms

    def validate_slots(self, slots: _SlotsType) -> _SlotsType:
        """Validate slot information."""
        if self.slot_schema is None:
            return slots

        if self._compiled_slot_schema is None:
            self._compiled_slot_schema = vol.Schema(
                {
                    key: Intent.SLOT_SCHEMA.extend({"value": validator})
                    for key, validator in self.slot_schema.items()
                },
                extra=vol.ALLOW_EXTRA,
            )

        return self._compiled_slot_schema(slots)  # type: ignore[no-any-return]

    async def async_handle_intent(self, intent_obj: _Intent) -> _Response:
        """Handle the intent."""
        raise NotImplementedError()

    def __repr__(self) -> str:
        """Represent a string of an intent handler."""
        return f"<{self.__class__.__name__} - {self.intent_type}>"


class _ServiceHandler(_Handler):
    """Service Intent handler registration.

    Service specific intent handler that calls a service by name/entity_id.
    """

    def __init__(
        self, intent_type: str, domain: str, service: str, speech: str
    ) -> None:
        """Create Service Intent Handler."""
        slot_schema = {vol.Required("name"): _cv.string}
        super().__init__(intent_type, slot_schema)
        self._domain = domain
        self._service = service
        self._speech = speech

    async def async_handle_intent(self, intent_obj: _Intent) -> _Response:
        """Handle the hass intent."""
        shc = intent_obj.controller
        slots = self.validate_slots(intent_obj.slots)
        state = shc.intents.async_match_state(slots["name"]["value"])

        await shc.services.async_call(
            self._domain,
            self._service,
            {Const.ATTR_ENTITY_ID: state.entity_id},
            context=intent_obj.context,
        )

        response = intent_obj.create_response()
        response.async_set_speech(self._speech.format(state.name))
        return response


# pylint: disable=unused-variable, invalid-name
class Intent:
    """Intent namespace."""

    INTENT_TURN_OFF: typing.Final = "ControllerTurnOff"
    INTENT_TURN_ON: typing.Final = "ControllerTurnOn"
    INTENT_TOGGLE: typing.Final = "ControllerToggle"

    SLOT_SCHEMA: typing.Final = vol.Schema({}, extra=vol.ALLOW_EXTRA)

    Handler: typing.TypeAlias = _Handler
    Intent: typing.TypeAlias = _Intent
    Response: typing.TypeAlias = _Response
    ServiceHandler: typing.TypeAlias = _ServiceHandler
    SlotsType: typing.TypeAlias = _SlotsType
    SpeechType: typing.TypeAlias = _SpeechType

    class IntentError(SmartHomeControllerError):
        """Base class for intent related errors."""

    class UnknownIntent(IntentError):
        """When the intent is not registered."""

    class InvalidSlotInfo(IntentError):
        """When the slot data is invalid."""

    class IntentHandleError(IntentError):
        """Error while handling intent."""

    class UnexpectedError(IntentError):
        """Unexpected error while handling intent."""

    class Platform(PlatformImplementation):
        """Required base class for Intent Platform implementations."""

        @abc.abstractmethod
        async def async_setup_intents(self) -> None:
            """Setup intents."""
