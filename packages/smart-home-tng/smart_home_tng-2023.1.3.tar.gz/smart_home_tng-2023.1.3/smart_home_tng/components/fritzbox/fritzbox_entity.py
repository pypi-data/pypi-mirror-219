"""
AVM FRITZ!SmartHome Integration for Smart Home - The Next Generation.

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

import pyfritzhome as fritz
from ... import core
from .fritzbox_data_update_coordinator import FritzboxDataUpdateCoordinator


# pylint: disable=unused-variable
class FritzboxEntity(core.CoordinatorEntity[FritzboxDataUpdateCoordinator]):
    """Basis FritzBox entity."""

    def __init__(
        self,
        coordinator: FritzboxDataUpdateCoordinator,
        ain: str,
        entity_description: core.EntityDescription = None,
    ) -> None:
        """Initialize the FritzBox entity."""
        super().__init__(coordinator)

        self._ain = ain
        if entity_description is not None:
            self._entity_description = entity_description
            self._attr_name = f"{self.device.name} {entity_description.name}"
            self._attr_unique_id = f"{ain}_{entity_description.key}"
        else:
            self._attr_name = self.device.name
            self._attr_unique_id = ain

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return super().available and self.device.present

    @property
    def device(self) -> fritz.FritzhomeDevice:
        """Return device object from coordinator."""
        return self.coordinator.data[self._ain]

    @property
    def device_info(self) -> core.DeviceInfo:
        """Return device specific attributes."""
        return core.DeviceInfo(
            name=self.device.name,
            identifiers={(self.coordinator.owner.domain, self._ain)},
            manufacturer=self.device.manufacturer,
            model=self.device.productname,
            sw_version=self.device.fw_version,
            configuration_url=self.coordinator.configuration_url,
        )
