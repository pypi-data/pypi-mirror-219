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

from .const import Const
from .smart_home_controller import SmartHomeController
from .state import State
from .template_state_base import TemplateStateBase


# pylint: disable=unused-variable
class TemplateStateFromEntityId(TemplateStateBase):
    """Class to represent a state object in a template."""

    def __init__(
        self, shc: SmartHomeController, entity_id: str, collect: bool = True
    ) -> None:
        """Initialize template state."""
        super().__init__(shc, collect, entity_id)

    @property
    def _state(self) -> State:  # type: ignore[override] # mypy issue 4125
        state = self._shc.states.get(self._entity_id)
        if not state:
            state = State(self._entity_id, Const.STATE_UNKNOWN)
        return state

    def __repr__(self) -> str:
        """Representation of Template State."""
        return f"<template TemplateStateFromEntityId({self._entity_id})>"
