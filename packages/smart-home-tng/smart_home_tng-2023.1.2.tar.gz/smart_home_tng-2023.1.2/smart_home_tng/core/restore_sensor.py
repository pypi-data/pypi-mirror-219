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

from .restore_entity import RestoreEntity
from .sensor import Sensor


# pylint: disable=unused-variable
class RestoreSensor(Sensor.Entity, RestoreEntity):
    """Mixin class for restoring previous sensor state."""

    @property
    def extra_restore_state_data(self) -> Sensor.ExtraStoredData:
        """Return sensor specific state data to be restored."""
        return Sensor.ExtraStoredData(
            self.native_value, self.native_unit_of_measurement
        )

    async def async_get_last_sensor_data(self) -> Sensor.ExtraStoredData:
        """Restore native_value and native_unit_of_measurement."""
        if (restored_last_extra_data := await self.async_get_last_extra_data()) is None:
            return None
        return Sensor.ExtraStoredData.from_dict(restored_last_extra_data.as_dict())
