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


# pylint: disable=unused-variable
class AlexaSemantics:
    """Class for Alexa Semantics Object.

    You can optionally enable additional utterances by using semantics. When you use semantics,
    you manually map the phrases "open", "close", "raise", and "lower" to directives.

    Semantics is supported for the following interfaces only: ModeController, RangeController,
    and ToggleController.

    Semantics stateMappings are only supported for one interface of the same type on the same
    device. If a device has multiple RangeControllers only one interface may use stateMappings
    otherwise discovery will fail.

    You can support semantics actionMappings on different controllers for the same device, however
    each controller must support different phrases. For example, you can support "raise" on a
    RangeController, and "open" on a ModeController, but you can't support "open" on both
    RangeController and ModeController. Semantics stateMappings are only supported for one
    interface on the same device.

    https://developer.amazon.com/docs/device-apis/alexa-discovery.html#semantics-object
    """

    MAPPINGS_ACTION: typing.Final = "actionMappings"
    MAPPINGS_STATE: typing.Final = "stateMappings"

    ACTIONS_TO_DIRECTIVE: typing.Final = "ActionsToDirective"
    STATES_TO_VALUE: typing.Final = "StatesToValue"
    STATES_TO_RANGE: typing.Final = "StatesToRange"

    ACTION_CLOSE: typing.Final = "Alexa.Actions.Close"
    ACTION_LOWER: typing.Final = "Alexa.Actions.Lower"
    ACTION_OPEN: typing.Final = "Alexa.Actions.Open"
    ACTION_RAISE: typing.Final = "Alexa.Actions.Raise"

    STATES_OPEN: typing.Final = "Alexa.States.Open"
    STATES_CLOSED: typing.Final = "Alexa.States.Closed"

    DIRECTIVE_RANGE_SET_VALUE: typing.Final = "SetRangeValue"
    DIRECTIVE_RANGE_ADJUST_VALUE: typing.Final = "AdjustRangeValue"
    DIRECTIVE_TOGGLE_TURN_ON: typing.Final = "TurnOn"
    DIRECTIVE_TOGGLE_TURN_OFF: typing.Final = "TurnOff"
    DIRECTIVE_MODE_SET_MODE: typing.Final = "SetMode"
    DIRECTIVE_MODE_ADJUST_MODE: typing.Final = "AdjustMode"

    def __init__(self):
        """Initialize an Alexa modeResource."""
        self._action_mappings = []
        self._state_mappings = []

    def _add_action_mapping(self, semantics):
        """Add action mapping between actions and interface directives."""
        self._action_mappings.append(semantics)

    def _add_state_mapping(self, semantics):
        """Add state mapping between states and interface directives."""
        self._state_mappings.append(semantics)

    def add_states_to_value(self, states: typing.Iterable[str], value: str):
        """Add StatesToValue stateMappings."""
        self._add_state_mapping(
            {"@type": self.STATES_TO_VALUE, "states": states, "value": value}
        )

    def add_states_to_range(self, states, min_value, max_value):
        """Add StatesToRange stateMappings."""
        self._add_state_mapping(
            {
                "@type": self.STATES_TO_RANGE,
                "states": states,
                "range": {"minimumValue": min_value, "maximumValue": max_value},
            }
        )

    def add_action_to_directive(self, actions, directive, payload):
        """Add ActionsToDirective actionMappings."""
        self._add_action_mapping(
            {
                "@type": self.ACTIONS_TO_DIRECTIVE,
                "actions": actions,
                "directive": {"name": directive, "payload": payload},
            }
        )

    def serialize_semantics(self):
        """Return semantics object serialized for an API response."""
        semantics = {}
        if self._action_mappings:
            semantics[self.MAPPINGS_ACTION] = self._action_mappings
        if self._state_mappings:
            semantics[self.MAPPINGS_STATE] = self._state_mappings

        return semantics
