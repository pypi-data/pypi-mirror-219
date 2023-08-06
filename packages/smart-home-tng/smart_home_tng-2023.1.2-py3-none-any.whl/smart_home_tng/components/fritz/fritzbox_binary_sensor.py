"""
AVM FRITZ!Box Tools Integration for Smart Home - The Next Generation.

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

# pylint: disable=unused-variable

import dataclasses
import logging
import typing

from ... import core
from .avm_wrapper import AvmWrapper
from .connection_info import ConnectionInfo
from .fritzbox_base_entity import FritzboxBaseEntity

if not typing.TYPE_CHECKING:

    class FritzboxToolsIntegration:
        pass


if typing.TYPE_CHECKING:
    from .fritzbox_tools_integration import FritzboxToolsIntegration

_LOGGER: typing.Final = logging.getLogger(__name__)


@dataclasses.dataclass
class FritzBinarySensorEntityDescription(core.BinarySensor.EntityDescription):
    """Describes Fritz sensor entity."""

    is_suitable: typing.Callable[[ConnectionInfo], bool] = lambda info: info.wan_enabled


_SENSOR_TYPES: typing.Final[tuple[FritzBinarySensorEntityDescription, ...]] = (
    FritzBinarySensorEntityDescription(
        key="is_connected",
        name="Connection",
        device_class=core.BinarySensor.DeviceClass.CONNECTIVITY,
        entity_category=core.EntityCategory.DIAGNOSTIC,
    ),
    FritzBinarySensorEntityDescription(
        key="is_linked",
        name="Link",
        device_class=core.BinarySensor.DeviceClass.PLUG,
        entity_category=core.EntityCategory.DIAGNOSTIC,
    ),
)


class FritzboxBinarySensor(FritzboxBaseEntity, core.BinarySensor.Entity):
    """Define FRITZ!Box connectivity class."""

    def __init__(
        self,
        owner: core.SmartHomeControllerComponent,
        avm_wrapper: AvmWrapper,
        device_friendly_name: str,
        description: core.BinarySensor.EntityDescription,
    ) -> None:
        """Init FRITZ!Box connectivity class."""
        self._entity_description = description
        self._attr_name = f"{device_friendly_name} {description.name}"
        self._attr_unique_id = f"{avm_wrapper.unique_id}-{description.key}"
        super().__init__(owner, avm_wrapper, device_friendly_name)

    def update(self) -> None:
        """Update data."""
        _LOGGER.debug("Updating FRITZ!Box binary sensors")

        if self.entity_description.key == "firmware_update":
            self._attr_is_on = self._avm_wrapper.update_available
            self._attr_extra_state_attributes = {
                "installed_version": self._avm_wrapper.current_firmware,
                "latest_available_version": self._avm_wrapper.latest_firmware,
            }
        if self.entity_description.key == "is_connected":
            self._attr_is_on = bool(self._avm_wrapper.fritz_status.is_connected)
        elif self.entity_description.key == "is_linked":
            self._attr_is_on = bool(self._avm_wrapper.fritz_status.is_linked)


# pylint: disable=unused-variable
async def async_setup_binary_sensors(
    owner: FritzboxToolsIntegration,
    entry: core.ConfigEntry,
    async_add_entities: core.AddEntitiesCallback,
) -> None:
    """Set up entry."""
    _LOGGER.debug("Setting up FRITZ!Box binary sensors")
    avm_wrapper: AvmWrapper = owner.wrappers[entry.entry_id]

    connection_info = await avm_wrapper.async_get_connection_info()

    entities = [
        FritzboxBinarySensor(owner, avm_wrapper, entry.title, description)
        for description in _SENSOR_TYPES
        if description.is_suitable(connection_info)
    ]

    async_add_entities(entities, True)
