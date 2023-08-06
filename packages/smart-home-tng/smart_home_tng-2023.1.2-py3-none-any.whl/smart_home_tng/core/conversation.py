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
import re
import typing

import voluptuous as vol

from .config_validation import ConfigValidation as _cv
from .context import Context
from .intent import Intent
from .smart_home_controller_component import SmartHomeControllerComponent


class _AbstractAgent(abc.ABC):
    """Abstract conversation agent."""

    @property
    def attribution(self):
        """Return the attribution."""
        return None

    async def async_get_onboarding(self):
        """Get onboard data."""
        return None

    # pylint: disable=unused-argument
    async def async_set_onboarding(self, shown: bool):
        """Set onboard data."""
        return True

    @abc.abstractmethod
    async def async_process(
        self, text: str, context: Context, conversation_id: str = None
    ) -> Intent.Response:
        """Process a sentence."""


# pylint: disable=unused-variable, invalid-name
class Conversation:
    """Conversation namespace."""

    ATTR_TEXT: typing.Final = "text"
    REGEX_TYPE = type(re.compile(""))
    SERVICE_PROCESS: typing.Final = "process"

    SERVICE_PROCESS_SCHEMA = vol.Schema({vol.Required(ATTR_TEXT): _cv.string})

    AbstractAgent: typing.TypeAlias = _AbstractAgent

    class Component(SmartHomeControllerComponent):
        """Required base class for the Conversation component."""

        @abc.abstractmethod
        def set_agent(self, agent: _AbstractAgent):
            """Set the agent to handle the conversations."""

    @staticmethod
    def create_matcher(utterance):
        """Create a regex that matches the utterance."""
        # Split utterance into parts that are type: NORMAL, GROUP or OPTIONAL
        # Pattern matches (GROUP|OPTIONAL): Change light to [the color] {name}
        parts = re.split(r"({\w+}|\[[\w\s]+\] *)", utterance)
        # Pattern to extract name from GROUP part. Matches {name}
        group_matcher = re.compile(r"{(\w+)}")
        # Pattern to extract text from OPTIONAL part. Matches [the color]
        optional_matcher = re.compile(r"\[([\w ]+)\] *")

        pattern = ["^"]
        for part in parts:
            group_match = group_matcher.match(part)
            optional_match = optional_matcher.match(part)

            # Normal part
            if group_match is None and optional_match is None:
                pattern.append(part)
                continue

            # Group part
            if group_match is not None:
                pattern.append(rf"(?P<{group_match.groups()[0]}>[\w ]+?)\s*")

            # Optional part
            elif optional_match is not None:
                pattern.append(rf"(?:{optional_match.groups()[0]} *)?")

        pattern.append("$")
        return re.compile("".join(pattern), re.I)
