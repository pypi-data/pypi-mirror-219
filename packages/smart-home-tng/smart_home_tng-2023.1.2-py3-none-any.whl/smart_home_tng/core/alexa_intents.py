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

from .. import auth
from ..backports import strenum


class SpeechType(strenum.PascalCaseStrEnum):
    """The Alexa speech types."""

    PLAIN_TEXT = enum.auto()
    SSML = "SSML"


class CardType(strenum.PascalCaseStrEnum):
    """The Alexa card types."""

    SIMPLE = enum.auto()
    LINK_ACCOUNT = enum.auto()
    ASK_FOR_PERMISSIONS_CONSENT = enum.auto()


class IntentResponse(abc.ABC):
    """Abstract base class for Alexa Responses."""

    @abc.abstractmethod
    def add_speech(self, speech_type: SpeechType, text: str):
        """Add speech to the response."""

    @abc.abstractmethod
    def add_card(self, card_type: CardType, title: str, content: str):
        """Add a card to the response, that is shown in the Alexa App."""

    @abc.abstractmethod
    def as_dict(self) -> dict[str, any]:
        """return the response as dictionary as required by alexa."""

    @abc.abstractmethod
    def add_reprompt(self, speech_type: SpeechType, text: str):
        """Add reprompt if user does not answer."""

    @property
    @abc.abstractmethod
    def in_active_conversation(self) -> bool:
        """Is this response part of a active conversation?"""

    @abc.abstractmethod
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


# pylint: disable=unused-variable
class Intent(abc.ABC):
    """Abstract base class for Alexa Intents."""

    @property
    @abc.abstractmethod
    def locale(self) -> str:
        """the requested locale of the skill user."""

    @property
    @abc.abstractmethod
    def slots(self) -> dict[str, any]:
        """the intent slot filled by alexa, if required"""

    @property
    @abc.abstractmethod
    def new_session(self) -> bool:
        """Is this intent part of a active conversation or the start of a new conversation."""

    @property
    @abc.abstractmethod
    def session_attributes(self) -> dict[str, str]:
        """the session attributes as defined by alexa"""

    @property
    @abc.abstractmethod
    def application(self) -> str:
        """
        the alexa application id (skill id) for the new application based
        intent handler infrastructur in smart home - the next generation
        """

    @property
    @abc.abstractmethod
    def type(self) -> str:
        """the intent type (defined by alexa)"""

    @property
    @abc.abstractmethod
    def name(self) -> str:
        """the name of the intent"""

    @property
    @abc.abstractmethod
    def device_id(self) -> str:
        """the device, on which the intent was started."""

    @property
    @abc.abstractmethod
    def person_id(self) -> str:
        """Get the id of the 'recognized speaker' from Alexa or None"""

    @property
    @abc.abstractmethod
    def user(self) -> auth.User:
        """The user, who started the intent."""

    @property
    @abc.abstractmethod
    def dialog_state(self) -> str:
        """get the dialog state, as defined by Alexa"""

    @property
    def qualified_name(self) -> str:
        """
        Fully qualified name, including application-id for flat intent handler infrastructur
        like intent scripts.
        """
        return f"{self.application}.{self.name}"

    @property
    @abc.abstractmethod
    def supported_interfaces(self) -> dict[str, any]:
        """Get the supported interfaces of the connected device."""

    def is_interface_supported(self, interface_name: str) -> bool:
        """Checks, if the requested Alexa interface is supported by the current device."""
        supported = self.supported_interfaces
        return supported is not None and supported.get(interface_name) is not None

    @abc.abstractmethod
    def get_interface_context(self, interface: str) -> dict[str, any]:
        """Get context information for the requested interface."""

    @abc.abstractmethod
    def create_response(self, should_end_session: bool = True) -> IntentResponse:
        """create the response for this intent."""

    def create_error_response(
        self, error: str, error_msg: str = None
    ) -> IntentResponse:
        """
        Create an Alexa Error Response which should be in the locale of the intent.
        The string is reported 'as-is' to alexa. No translation available.
        """
        response = self.create_response()
        title = "Fehler"
        msg = (
            "Während der Verarbeitung deiner Anfrage ist der folgende Fehler aufgetreten: "
            + error
        )
        if self.locale.startswith("en"):
            title = "Error"
            msg = (
                "During the processing of your request, the following error occurred:"
                + error
            )
        if error_msg is not None:
            error += "\n\n" + error_msg
        response.add_speech(SpeechType.PLAIN_TEXT, msg)
        response.add_card(CardType.SIMPLE, title, error)
        return response
