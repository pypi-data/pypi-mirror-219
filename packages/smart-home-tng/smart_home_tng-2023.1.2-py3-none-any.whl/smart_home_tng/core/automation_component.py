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

import abc

from .config_type import ConfigType
from .json_type import JsonType
from .smart_home_controller_component import SmartHomeControllerComponent


# pylint: disable=unused-variable
class AutomationComponent(SmartHomeControllerComponent):
    """Required base class for the Automation Component."""

    @abc.abstractmethod
    async def async_validate_config_item(self, config: JsonType) -> ConfigType:
        """Validate config item."""

    @abc.abstractmethod
    def automations_with_area(self, area_id: str) -> list[str]:
        """Return all automations that reference the area."""

    @abc.abstractmethod
    def automations_with_device(self, device_id: str) -> list[str]:
        """Return all automations that reference the device."""

    @abc.abstractmethod
    def automations_with_entity(self, entity_id: str) -> list[str]:
        """Return all automations that reference the entity."""

    @abc.abstractmethod
    def entities_in_automation(self, automation_entity_id: str) -> list[str]:
        """Return all entities that are referenced by the automation."""

    @abc.abstractmethod
    def devices_in_automation(self, automation_entity_id: str) -> list[str]:
        """Return all devices that are referenced by the automation."""

    @abc.abstractmethod
    def areas_in_automation(self, automation_entity_id: str) -> list[str]:
        """Return all areas that are referenced by the automation."""
