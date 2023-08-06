"""
Bosch SHC Integration for Smart Home - The Next Generation.

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
import boschshcpy as bosch

from ... import core
from .bosch_entity import BoschEntity

if not typing.TYPE_CHECKING:

    class BoschShcIntegration:
        pass


if typing.TYPE_CHECKING:
    from .bosch_shc_integration import BoschShcIntegration

_sensor: typing.TypeAlias = core.Sensor


# pylint: disable=unused-variable
class PurityRatingSensor(BoschEntity, _sensor.Entity):
    """Representation of an SHC purity rating sensor."""

    def __init__(
        self,
        owner: BoschShcIntegration,
        device: bosch.SHCDevice,
        parent_id: str,
        entry_id: str,
    ) -> None:
        """Initialize an SHC purity rating sensor."""
        super().__init__(owner, device, parent_id, entry_id)
        self._attr_name = f"{device.name} Purity Rating"
        self._attr_unique_id = f"{device.serial}_purity_rating"

    @property
    def native_value(self):
        """Return the state of the sensor."""
        return self._device.purity_rating.name
