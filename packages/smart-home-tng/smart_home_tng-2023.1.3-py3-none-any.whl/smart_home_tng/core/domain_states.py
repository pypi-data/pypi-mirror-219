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

from .helpers.template import get_template_state_if_valid
from .render_info import RenderInfo as ri
from .template_state import TemplateState

if not typing.TYPE_CHECKING:

    class SmartHomeController:
        ...


if typing.TYPE_CHECKING:
    from .smart_home_controller import SmartHomeController


# pylint: disable=unused-variable
class DomainStates:
    """Class to expose a specific HA domain as attributes."""

    def __init__(self, shc: SmartHomeController, domain: str) -> None:
        """Initialize the domain states."""
        self._shc = shc
        self._domain = domain

    def __getattr__(self, name):
        """Return the states."""
        return get_template_state_if_valid(self._shc, f"{self._domain}.{name}")

    # Jinja will try __getitem__ first and it avoids the need
    # to call is_safe_attribute
    __getitem__ = __getattr__

    def _collect_domain(self) -> None:
        entity_collect = ri.current()
        if entity_collect is not None:
            entity_collect.add_domain(self._domain)

    def _collect_domain_lifecycle(self) -> None:
        entity_collect = ri.current
        if entity_collect is not None:
            entity_collect.add_domains_lifecycle(self._domain)

    def __iter__(self):
        """Return the iteration over all the states."""
        self._collect_domain()
        return TemplateState.state_generator(self._shc, self._domain)

    def __len__(self) -> int:
        """Return number of states."""
        self._collect_domain_lifecycle()
        return self._shc.states.async_entity_ids_count(self._domain)

    def __repr__(self) -> str:
        """Representation of Domain States."""
        return f"<template DomainStates('{self._domain}')>"
