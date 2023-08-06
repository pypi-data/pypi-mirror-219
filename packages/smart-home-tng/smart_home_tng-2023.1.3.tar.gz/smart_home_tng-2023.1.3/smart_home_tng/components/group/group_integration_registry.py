"""
Group Component for Smart Home - The Next Generation.

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

import contextvars

from ... import core

_current_domain: contextvars.ContextVar[str] = contextvars.ContextVar("current_domain")


# pylint: disable=unused-variable
class GroupIntegrationRegistry(core.GroupIntegrationRegistry):
    """Class to hold a registry of integrations."""

    def __init__(self) -> None:
        super().__init__()
        self._on_off_mapping: dict[str, str] = {
            core.Const.STATE_ON: core.Const.STATE_OFF
        }
        self._off_on_mapping: dict[str, str] = {
            core.Const.STATE_OFF: core.Const.STATE_ON
        }
        self._on_states_by_domain: dict[str, set] = {}
        self._exclude_domains: set = set()

    @property
    def exclude_domains(self) -> set:
        return frozenset(self._exclude_domains)

    @property
    def on_off_mapping(self):
        return self._on_off_mapping.items()

    @property
    def off_on_mapping(self):
        return self._off_on_mapping.items()

    @property
    def on_states_by_domain(self):
        return self._on_states_by_domain.items()

    def exclude_domain(self) -> None:
        """Exclude the current domain."""
        self._exclude_domains.add(_current_domain.get())

    def on_off_states(self, on_states: set, off_state: str) -> None:
        """Register on and off states for the current domain."""
        for on_state in on_states:
            if on_state not in self.on_off_mapping:
                self._on_off_mapping[on_state] = off_state

        if len(on_states) == 1 and off_state not in self.off_on_mapping:
            self._off_on_mapping[off_state] = list(on_states)[0]

        self._on_states_by_domain[_current_domain.get()] = set(on_states)
