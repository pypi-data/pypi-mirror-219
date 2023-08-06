"""
Mobile App Component for Smart Home - The Next Generation.

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

from ... import core
from .const import Const
from .mobile_app_entity import MobileAppEntity


# pylint: disable=unused-variable
class MobileAppBinarySensor(MobileAppEntity, core.BinarySensor.Entity):
    """Representation of an mobile app binary sensor."""

    @property
    def is_on(self):
        """Return the state of the binary sensor."""
        return self._config[Const.ATTR_SENSOR_STATE]

    @core.callback
    def async_restore_last_state(self, last_state):
        """Restore previous state."""

        super().async_restore_last_state(last_state)
        self._config[Const.ATTR_SENSOR_STATE] = last_state.state == core.Const.STATE_ON
