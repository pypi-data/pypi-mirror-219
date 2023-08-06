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

from . import helpers
from .store import Store


# pylint: disable=unused-variable
class EntityRegistryStore(Store):
    """Store entity registry data."""

    async def _async_migrate_func(
        self, old_major_version: int, old_minor_version: int, old_data: dict
    ) -> dict:
        """Migrate to the new version."""
        return await self.async_migrate(old_major_version, old_minor_version, old_data)

    @staticmethod
    async def async_migrate(
        old_major_version: int, old_minor_version: int, data: dict
    ) -> dict:
        """Migrate to the new version."""
        if old_major_version == 1 and old_minor_version < 2:
            # From version 1.1
            for entity in data["entities"]:
                # Populate all keys
                entity["area_id"] = entity.get("area_id")
                entity["capabilities"] = entity.get("capabilities") or {}
                entity["config_entry_id"] = entity.get("config_entry_id")
                entity["device_class"] = entity.get("device_class")
                entity["device_id"] = entity.get("device_id")
                entity["disabled_by"] = entity.get("disabled_by")
                entity["entity_category"] = entity.get("entity_category")
                entity["icon"] = entity.get("icon")
                entity["name"] = entity.get("name")
                entity["original_icon"] = entity.get("original_icon")
                entity["original_name"] = entity.get("original_name")
                entity["platform"] = entity["platform"]
                entity["supported_features"] = entity.get("supported_features", 0)
                entity["unit_of_measurement"] = entity.get("unit_of_measurement")

        if old_major_version == 1 and old_minor_version < 3:
            # Version 1.3 adds original_device_class
            for entity in data["entities"]:
                # Move device_class to original_device_class
                entity["original_device_class"] = entity["device_class"]
                entity["device_class"] = None

        if old_major_version == 1 and old_minor_version < 4:
            # Version 1.4 adds id
            for entity in data["entities"]:
                entity["id"] = helpers.random_uuid_hex()

        if old_major_version == 1 and old_minor_version < 5:
            # Version 1.5 adds entity options
            for entity in data["entities"]:
                entity["options"] = {}

        if old_major_version == 1 and old_minor_version < 6:
            # Version 1.6 adds hidden_by
            for entity in data["entities"]:
                entity["hidden_by"] = None

        if old_major_version > 1:
            raise NotImplementedError()
        return data
