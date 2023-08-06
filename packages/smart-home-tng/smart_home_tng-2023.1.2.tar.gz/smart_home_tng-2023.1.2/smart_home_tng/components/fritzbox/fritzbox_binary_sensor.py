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

import typing

from ... import core
from .const import Const
from .fritz_binary_sensor_entity_description import FritzBinarySensorEntityDescription
from .fritzbox_data_update_coordinator import FritzboxDataUpdateCoordinator
from .fritzbox_entity import FritzboxEntity

if not typing.TYPE_CHECKING:

    class FritzboxIntegration:
        pass


if typing.TYPE_CHECKING:
    from .fritzbox_integration import FritzboxIntegration


_BINARY_SENSOR_TYPES: typing.Final[tuple[FritzBinarySensorEntityDescription, ...]] = (
    FritzBinarySensorEntityDescription(
        key="alarm",
        name="Alarm",
        device_class=core.BinarySensor.DeviceClass.WINDOW,
        suitable=lambda device: device.has_alarm,
        is_on=lambda device: device.alert_state,
    ),
    FritzBinarySensorEntityDescription(
        key="lock",
        name="Button Lock on Device",
        device_class=core.BinarySensor.DeviceClass.LOCK,
        entity_category=core.EntityCategory.CONFIG,
        suitable=lambda device: device.lock is not None,
        is_on=lambda device: not device.lock,
    ),
    FritzBinarySensorEntityDescription(
        key="device_lock",
        name="Button Lock via UI",
        device_class=core.BinarySensor.DeviceClass.LOCK,
        entity_category=core.EntityCategory.CONFIG,
        suitable=lambda device: device.device_lock is not None,
        is_on=lambda device: not device.device_lock,
    ),
)


# pylint: disable=unused-variable
class FritzboxBinarySensor(FritzboxEntity, core.BinarySensor.Entity):
    """Representation of a binary FRITZ!SmartHome device."""

    _entity_description: FritzBinarySensorEntityDescription

    def __init__(
        self,
        coordinator: FritzboxDataUpdateCoordinator,
        ain: str,
        entity_description: FritzBinarySensorEntityDescription,
    ) -> None:
        """Initialize the FritzBox entity."""
        super().__init__(coordinator, ain, entity_description)
        self._attr_name = f"{self.device.name} {entity_description.name}"
        self._attr_unique_id = f"{ain}_{entity_description.key}"

    @property
    def is_on(self) -> bool:
        """Return true if sensor is on."""
        return self.entity_description.is_on(self.device)


async def async_setup_binary_sensors(
    owner: FritzboxIntegration,
    entry: core.ConfigEntry,
    async_add_entities: core.AddEntitiesCallback,
) -> None:
    """Set up the FRITZ!SmartHome binary sensor from ConfigEntry."""
    coordinator: FritzboxDataUpdateCoordinator = owner.connection_config[
        entry.entry_id
    ][Const.CONF_COORDINATOR]

    async_add_entities(
        [
            FritzboxBinarySensor(coordinator, ain, description)
            for ain, device in coordinator.data.items()
            for description in _BINARY_SENSOR_TYPES
            if description.suitable(device)
        ]
    )
