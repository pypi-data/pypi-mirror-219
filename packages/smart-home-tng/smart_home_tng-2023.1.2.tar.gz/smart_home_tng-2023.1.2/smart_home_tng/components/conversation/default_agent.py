"""
Conversation Component for Smart Home - The Next Generation.

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

from ... import core

_cover: typing.TypeAlias = core.Cover
_const: typing.TypeAlias = core.Const
_conversation: typing.TypeAlias = core.Conversation
_intent: typing.TypeAlias = core.Intent


UTTERANCES: typing.Final = {
    "cover": {
        _cover.INTENT_OPEN_COVER: ["Open [the] [a] [an] {name}[s]"],
        _cover.INTENT_CLOSE_COVER: ["Close [the] [a] [an] {name}[s]"],
    },
    #    "shopping_list": {
    #        INTENT_ADD_ITEM: ["Add [the] [a] [an] {item} to my shopping list"],
    #        INTENT_LAST_ITEMS: ["What is on my shopping list"],
    #    },
}


# pylint: disable=unused-variable
class DefaultAgent(_conversation.AbstractAgent):
    """Default agent for conversation agent."""

    def __init__(self, owner: core.SmartHomeControllerComponent) -> None:
        """Initialize the default agent."""
        self._owner = owner
        self._intents: dict[str, list[_conversation.REGEX_TYPE]] = {}

    @property
    def controller(self):
        return self._owner.controller

    async def async_initialize(self, config: core.ConfigType):
        """Initialize the default agent."""
        if "intent" not in self.controller.config.components:
            await self.controller.setup.async_setup_component("intent", {})

        intents = self._intents

        for intent_type, utterances in config.get("intents", {}).items():
            if (conf := intents.get(intent_type)) is None:
                conf = intents[intent_type] = []

            conf.extend(
                _conversation.create_matcher(utterance) for utterance in utterances
            )

        # We strip trailing 's' from name because our state matcher will fail
        # if a letter is not there. By removing 's' we can match singular and
        # plural names.

        self._register(
            _intent.INTENT_TURN_ON,
            ["Turn [the] [a] {name}[s] on", "Turn on [the] [a] [an] {name}[s]"],
        )
        self._register(
            _intent.INTENT_TURN_OFF,
            ["Turn [the] [a] [an] {name}[s] off", "Turn off [the] [a] [an] {name}[s]"],
        )
        self._register(
            _intent.INTENT_TOGGLE,
            ["Toggle [the] [a] [an] {name}[s]", "[the] [a] [an] {name}[s] toggle"],
        )

        @core.callback
        def component_loaded(event: core.Event):
            """Handle a new component loaded."""
            self.register_utterances(event.data[_const.ATTR_COMPONENT])

        self.controller.bus.async_listen(
            _const.EVENT_COMPONENT_LOADED, component_loaded
        )

        # Check already loaded components.
        for component in self.controller.config.components:
            self.register_utterances(component)

    def _register(self, intent_type: str, utterances):
        """Register utterances and any custom intents for the default agent.

        Registrations don't require conversations to be loaded. They will become
        active once the conversation component is loaded.
        """
        intents = self._intents
        conf = intents.setdefault(intent_type, [])

        for utterance in utterances:
            if isinstance(utterance, _conversation.REGEX_TYPE):
                conf.append(utterance)
            else:
                conf.append(_conversation.create_matcher(utterance))

    @core.callback
    def register_utterances(self, component: str):
        """Register utterances for a component."""
        if component not in UTTERANCES:
            return
        for intent_type, sentences in UTTERANCES[component].items():
            self._register(intent_type, sentences)

    async def async_process(
        self, text: str, context: core.Context, conversation_id: str = None
    ) -> _intent.Response:
        """Process a sentence."""
        intents = self._intents

        for intent_type, matchers in intents.items():
            for matcher in matchers:
                if not (match := matcher.match(text)):
                    continue

                return await self.controller.intents.async_handle_intent(
                    self._owner.domain,
                    intent_type,
                    {key: {"value": value} for key, value in match.groupdict().items()},
                    text,
                    context,
                )
