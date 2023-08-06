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

import typing

from .store import Store
from .device_registry_entry_type import DeviceRegistryEntryType


# pylint: disable=unused-variable
class DeviceRegistryStore(Store[dict[str, list[dict[str, typing.Any]]]]):
    """Store entity registry data."""

    async def _async_migrate_func(
        self,
        old_major_version: int,
        old_minor_version: int,
        old_data: dict[str, typing.Any],
    ) -> dict[str, typing.Any]:
        """Migrate to the new version."""
        if old_major_version < 2:
            if old_minor_version < 2:
                # From version 1.1
                for device in old_data["devices"]:
                    # Introduced in 0.110
                    try:
                        device["entry_type"] = DeviceRegistryEntryType(
                            device.get("entry_type")
                        )
                    except ValueError:
                        device["entry_type"] = None

                    # Introduced in 0.79
                    # renamed in 0.95
                    device["via_device_id"] = device.get("via_device_id") or device.get(
                        "hub_device_id"
                    )
                    # Introduced in 0.87
                    device["area_id"] = device.get("area_id")
                    device["name_by_user"] = device.get("name_by_user")
                    # Introduced in 0.119
                    device["disabled_by"] = device.get("disabled_by")
                    # Introduced in 2021.11
                    device["configuration_url"] = device.get("configuration_url")
                # Introduced in 0.111
                old_data["deleted_devices"] = old_data.get("deleted_devices", [])
                for device in old_data["deleted_devices"]:
                    # Introduced in 2021.2
                    device["orphaned_timestamp"] = device.get("orphaned_timestamp")
            if old_minor_version < 3:
                # Introduced in 2022.2
                for device in old_data["devices"]:
                    device["hw_version"] = device.get("hw_version")

        if old_major_version > 1:
            raise NotImplementedError()
        return old_data
