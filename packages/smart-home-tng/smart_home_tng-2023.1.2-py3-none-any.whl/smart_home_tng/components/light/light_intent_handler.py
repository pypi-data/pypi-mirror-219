"""
Light Component for Smart Home - The Next Generation.

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

import voluptuous as vol

from ... import core

_cv: typing.TypeAlias = core.ConfigValidation
_const: typing.TypeAlias = core.Const
_intent: typing.TypeAlias = core.Intent
_light: typing.TypeAlias = core.Light

_INTENT_SET: typing.Final = "ControllerLightSet"


# pylint: disable=unused-variable
class LightIntentHandler(_intent.Handler):
    """Handle set color intents."""

    def __init__(
        self,
        owner: core.SmartHomeControllerComponent,
        platforms: typing.Iterable[str] = None,
    ):
        intent_type = _INTENT_SET
        slot_schema = {
            vol.Required("name"): _cv.string,
            vol.Optional("color"): core.helpers.Color.name_to_rgb,
            vol.Optional("brightness"): vol.All(vol.Coerce(int), vol.Range(0, 100)),
        }
        super().__init__(intent_type, slot_schema, platforms)
        self._owner = owner

    async def async_handle_intent(self, intent_obj: _intent.Intent) -> _intent.Response:
        """Handle the hass intent."""
        controller = intent_obj.controller
        slots = self.validate_slots(intent_obj.slots)
        state = controller.intents.async_match_state(
            slots["name"]["value"], controller.states.async_all(self._owner.domain)
        )

        service_data = {_const.ATTR_ENTITY_ID: state.entity_id}
        speech_parts = []

        if "color" in slots:
            _test_supports_color(state)
            service_data[_const.ATTR_RGB_COLOR] = slots["color"]["value"]
            # Use original passed in value of the color because we don't have
            # human readable names for that internally.
            speech_parts.append(f"the color {intent_obj.slots['color']['value']}")

        if "brightness" in slots:
            _test_supports_brightness(state)
            service_data[_const.ATTR_BRIGHTNESS_PCT] = slots["brightness"]["value"]
            speech_parts.append(f"{slots['brightness']['value']}% brightness")

        await controller.services.async_call(
            self._owner.domain,
            _const.SERVICE_TURN_ON,
            service_data,
            context=intent_obj.context,
        )

        response = intent_obj.create_response()

        if not speech_parts:  # No attributes changed
            speech = f"Turned on {state.name}"
        else:
            parts = [f"Changed {state.name} to"]
            for index, part in enumerate(speech_parts):
                if index == 0:
                    parts.append(f" {part}")
                elif index != len(speech_parts) - 1:
                    parts.append(f", {part}")
                else:
                    parts.append(f" and {part}")
            speech = "".join(parts)

        response.async_set_speech(speech)
        return response


def _test_supports_color(state: core.State) -> None:
    """Test if state supports colors."""
    supported_color_modes = state.attributes.get(_light.ATTR_SUPPORTED_COLOR_MODES)
    if not _light.color_supported(supported_color_modes):
        raise _intent.IntentHandleError(
            f"Entity {state.name} does not support changing colors"
        )


def _test_supports_brightness(state: core.State) -> None:
    """Test if state supports brightness."""
    supported_color_modes = state.attributes.get(_light.ATTR_SUPPORTED_COLOR_MODES)
    if not _light.brightness_supported(supported_color_modes):
        raise _intent.IntentHandleError(
            f"Entity {state.name} does not support changing brightness"
        )
