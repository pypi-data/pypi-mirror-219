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

import logging
import re
import typing

import voluptuous as vol

from .callback import callback
from .const import Const
from .context import Context
from .intent import Intent
from .state import State

if not typing.TYPE_CHECKING:

    class SmartHomeController:
        pass


if typing.TYPE_CHECKING:
    from .smart_home_controller import SmartHomeController


_T = typing.TypeVar("_T")
_LOGGER: typing.Final = logging.getLogger(__name__)


# pylint: disable=unused-variable
class IntentManager:
    """Manages intents"""

    def __init__(self, shc: SmartHomeController) -> None:
        self._shc = shc
        self._intents: dict[str, Intent.Handler] = {}

    @property
    def controller(self) -> SmartHomeController:
        return self._shc

    def register_handler(self, handler: Intent.Handler):
        """Register an intent with Home Assistant."""
        assert handler.intent_type is not None, "intent_type cannot be None"

        if handler.intent_type in self._intents:
            _LOGGER.warning(
                f"Intent {handler.intent_type} is being overwritten by {handler}"
            )
            self._intents[handler.intent_type] = handler

    async def async_handle_intent(
        self,
        platform: str,
        intent_type: str,
        slots: Intent.SlotsType = None,
        text_input: str = None,
        context: Context = None,
    ) -> Intent.Response:
        """Handle an intent."""
        handler = self._intents.get(intent_type)

        if handler is None:
            raise Intent.UnknownIntent(f"Unknown intent {intent_type}")

        if context is None:
            context = Context()

        intent = Intent.Intent(
            self.controller, platform, intent_type, slots or {}, text_input, context
        )

        try:
            _LOGGER.info(f"Triggering intent handler {handler}")
            result = await handler.async_handle_intent(intent)
            return result
        except vol.Invalid as err:
            _LOGGER.warning(f"Received invalid slot info for {intent_type}: {err}")
            raise Intent.InvalidSlotInfo(
                f"Received invalid slot info for {intent_type}"
            ) from err
        except Intent.IntentHandleError:
            raise
        except Exception as err:
            raise Intent.UnexpectedError(f"Error handling {intent_type}") from err

    @callback
    def async_match_state(
        self, name: str, states: typing.Iterable[State] = None
    ) -> State:
        """Find a state that matches the name."""
        if states is None:
            states = self.controller.states.async_all()

        state = _fuzzymatch(name, states, lambda state: state.name)

        if state is None:
            raise Intent.IntentHandleError(f"Unable to find an entity called {name}")

        return state

    @callback
    def async_test_feature(self, state: State, feature: int, feature_name: str) -> None:
        """Test if state supports a feature."""
        if state.attributes.get(Const.ATTR_SUPPORTED_FEATURES, 0) & feature == 0:
            raise Intent.IntentHandleError(
                f"Entity {state.name} does not support {feature_name}"
            )


def _fuzzymatch(
    name: str, items: typing.Iterable[_T], key: typing.Callable[[_T], str]
) -> _T:
    """Fuzzy matching function."""
    matches = []
    pattern = ".*?".join(name)
    regex = re.compile(pattern, re.IGNORECASE)
    for idx, item in enumerate(items):
        if match := regex.search(key(item)):
            # Add key length so we prefer shorter keys with the same group and start.
            # Add index so we pick first match in case same group, start, and key length.
            matches.append(
                (len(match.group()), match.start(), len(key(item)), idx, item)
            )

    return sorted(matches)[0][4] if matches else None
