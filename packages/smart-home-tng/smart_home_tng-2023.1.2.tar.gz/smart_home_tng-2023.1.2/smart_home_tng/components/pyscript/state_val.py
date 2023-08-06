"""
PyScript Component for Smart Home - The Next Generation.

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


This component is based on the custom_component

Pyscript: Python Scripting for Home Assistant, Copyright (c) 2020-2022 Craig Barrat,
which may be freely used and copied according tho the terms of the Apache 2.0 License.

Original source code and documentation can be found under:
https://github.com/custom-components/pyscript
"""

import datetime as dt
from ... import core


# pylint: disable=unused-variable
class StateVal(str):
    """Class for representing the value and attributes of a state variable."""

    _last_updated: dt.datetime
    _last_changed: dt.datetime

    def __new__(cls, state: core.State):
        """Create a new instance given a state variable."""
        self = super().__new__(cls, state.state)
        self.__dict__ = state.attributes.copy()
        # pylint: disable=protected-access
        self._last_updated = state.last_updated
        self._last_changed = state.last_changed
        return self

    @property
    def last_changed(self):
        return self._last_changed

    @property
    def last_updated(self):
        return self._last_updated
