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

import collections.abc
import operator
import typing

from .state import State
from .template_state_base import TemplateStateBase


if not typing.TYPE_CHECKING:

    class SmartHomeController:
        ...


if typing.TYPE_CHECKING:
    from .smart_home_controller import SmartHomeController


# pylint: disable=unused-variable
class TemplateState(TemplateStateBase):
    """Class to represent a state object in a template."""

    # Inheritance is done so functions that check against State keep working
    def __init__(
        self, shc: SmartHomeController, state: State, collect: bool = True
    ) -> None:
        """Initialize template state."""
        super().__init__(shc, collect, state.entity_id)
        self._wrapped_state = state

    def __repr__(self) -> str:
        """Representation of Template State."""
        return f"<template TemplateState({self.state!r})>"

    @staticmethod
    def state_generator(
        shc: SmartHomeController, domain: str
    ) -> collections.abc.Generator:
        """State generator for a domain or all states."""
        for state in sorted(
            shc.states.async_all(domain), key=operator.attrgetter("entity_id")
        ):
            yield TemplateState(shc, state, collect=False)
