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

import typing

from . import helpers
from .const import Const
from .domain_states import DomainStates
from .helpers.template import get_template_state_if_valid, template_state_for_entity
from .render_info import RenderInfo as ri
from .template_error import TemplateError
from .template_state import TemplateState

if not typing.TYPE_CHECKING:

    class SmartHomeController:
        ...


if typing.TYPE_CHECKING:
    from .smart_home_controller import SmartHomeController


# pylint: disable=unused-variable
class AllStates:
    """Class to expose all Smart Home Controller states as attributes."""

    _RESERVED_NAMES: typing.Final = {
        "contextfunction",
        "evalcontextfunction",
        "environmentfunction",
    }

    def __init__(self, shc: SmartHomeController) -> None:
        """Initialize all states."""
        self._shc = shc

    def __getattr__(self, name):
        """Return the domain state."""
        if "." in name:
            return get_template_state_if_valid(self._shc, name)

        if name in AllStates._RESERVED_NAMES:
            return None

        if not helpers.valid_entity_id(f"{name}.entity"):
            raise TemplateError(f"Invalid domain name '{name}'")

        return DomainStates(self._shc, name)

    # Jinja will try __getitem__ first and it avoids the need
    # to call is_safe_attribute
    __getitem__ = __getattr__

    def _collect_all(self) -> None:
        render_info = ri.current
        if render_info is not None:
            render_info.collect_all_states()

    def _collect_all_lifecycle(self) -> None:
        render_info = ri.current
        if render_info is not None:
            render_info.collect_all_states_lifecycle()

    def __iter__(self):
        """Return all states."""
        self._collect_all()
        return TemplateState.state_generator(self._shc, None)

    def __len__(self) -> int:
        """Return number of states."""
        self._collect_all_lifecycle()
        return self._shc.states.async_entity_ids_count()

    def __call__(self, entity_id):
        """Return the states."""
        state = template_state_for_entity(self._shc, entity_id)
        return Const.STATE_UNKNOWN if state is None else state.state

    def __repr__(self) -> str:
        """Representation of All States."""
        return "<template AllStates>"
