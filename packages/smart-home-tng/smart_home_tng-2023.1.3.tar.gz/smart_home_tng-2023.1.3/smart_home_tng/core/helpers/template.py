"""
Helpers for Components of Smart Home - The Next Generation.

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

from ..render_info import RenderInfo as ri
from ..template_state import TemplateState
from ..state import State
from ..template_error import TemplateError
from .core import valid_entity_id

if not typing.TYPE_CHECKING:

    class SmartHomeController:
        ...


if typing.TYPE_CHECKING:
    from ..smart_home_controller import SmartHomeController

# pylint: disable=unused-variable


def template_state_for_entity(
    shc: SmartHomeController, entity_id: str
) -> TemplateState:
    """Get Template State for entity."""
    return _get_template_state_from_state(shc, entity_id, shc.states.get(entity_id))


def get_template_state_if_valid(
    shc: SmartHomeController, entity_id: str
) -> TemplateState:
    state = shc.states.get(entity_id)
    if state is None and not valid_entity_id(entity_id):
        raise TemplateError(f"Invalid entity ID '{entity_id}'")
    return _get_template_state_from_state(shc, entity_id, state)


def _get_template_state_from_state(
    shc: SmartHomeController, entity_id: str, state: State
) -> TemplateState:
    if state is None:
        # Only need to collect if none, if not none collect first actual
        # access to the state properties in the state wrapper.
        _collect_state(entity_id)
        return None
    return TemplateState(shc, state)


def _collect_state(entity_id: str) -> None:
    if (entity_collect := ri.current()) is not None:
        entity_collect.add_entity(entity_id)
