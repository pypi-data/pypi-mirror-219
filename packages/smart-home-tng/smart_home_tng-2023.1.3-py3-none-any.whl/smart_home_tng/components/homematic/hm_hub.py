"""
Homematic Integration for Smart Home - The Next Generation.

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

import datetime as dt
import logging
import typing

from ... import core

if not typing.TYPE_CHECKING:

    class HomematicIntegration:
        pass


if typing.TYPE_CHECKING:
    from .homematic_integration import HomematicIntegration


_cv: typing.TypeAlias = core.ConfigValidation

_LOGGER: typing.Final = logging.getLogger(__name__)
_SCAN_INTERVAL_HUB: typing.Final = dt.timedelta(seconds=300)
_SCAN_INTERVAL_VARIABLES: typing.Final = dt.timedelta(seconds=30)


# pylint: disable=unused-variable
class HMHub(core.Entity):
    """The HomeMatic hub. (CCU2/HomeGear)."""

    _attr_should_poll = False

    def __init__(self, owner: HomematicIntegration, name: str):
        """Initialize HomeMatic hub."""
        self._shc = owner.controller
        self._owner = owner
        self._entity_id = f"{owner.domain}.{name.lower()}"
        self._homematic = owner.homematic
        self._variables = {}
        self._name = name
        self._state = None

        # Load data
        self.controller.tracker.track_time_interval(
            self._update_hub, _SCAN_INTERVAL_HUB
        )
        self.controller.add_job(self._update_hub, None)

        self.controller.tracker.track_time_interval(
            self._update_variables, _SCAN_INTERVAL_VARIABLES
        )
        self.controller.add_job(self._update_variables, None)

    @property
    def controller(self) -> core.SmartHomeController:
        return self._owner.controller

    @property
    def name(self):
        """Return the name of the device."""
        return self._name

    @property
    def state(self):
        """Return the state of the entity."""
        return self._state

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        return self._variables.copy()

    @property
    def icon(self):
        """Return the icon to use in the frontend, if any."""
        return "mdi:gradient-vertical"

    def _update_hub(self, _now):
        """Retrieve latest state."""
        service_message = self._homematic.getServiceMessages(self._name)
        state = None if service_message is None else len(service_message)

        # state have change?
        if self._state != state:
            self._state = state
            self.schedule_update_state()

    def _update_variables(self, _now):
        """Retrieve all variable data and update hmvariable states."""
        variables = self._homematic.getAllSystemVariables(self._name)
        if variables is None:
            return

        state_change = False
        for key, value in variables.items():
            if key in self._variables and value == self._variables[key]:
                continue

            state_change = True
            self._variables.update({key: value})

        if state_change:
            self.schedule_update_state()

    def hm_set_variable(self, name, value):
        """Set variable value on CCU/Homegear."""
        if name not in self._variables:
            _LOGGER.error(f"Variable {name} not found on {self.name}")
            return
        old_value = self._variables.get(name)
        if isinstance(old_value, bool):
            value = _cv.boolean(value)
        else:
            value = float(value)
        self._homematic.setSystemVariable(self.name, name, value)

        self._variables.update({name: value})
        self.schedule_update_state()
