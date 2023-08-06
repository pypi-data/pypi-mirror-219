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

from .device import Device
from .device_base import DeviceBase


# pylint: disable=unused-variable
class DeletedDevice(DeviceBase):
    """Base class for device, will be used for deleted devices."""

    def __init__(
        self,
        device_id: str,
        config_entries: set[str] = None,
        connections: set[tuple[str, str]] = None,
        identifiers: set[tuple[str, str]] = None,
        orphaned_timestamp: float = None,
    ) -> None:
        super().__init__(device_id, config_entries, connections, identifiers)
        self._orphaned_timestamp = orphaned_timestamp

    @property
    def orphaned_timestamp(self) -> float:
        return self._orphaned_timestamp

    def to_device_entry(
        self,
        config_entry_id: str,
        connections: set[tuple[str, str]],
        identifiers: set[tuple[str, str]],
    ) -> Device:
        """Create DeviceEntry from DeletedDeviceEntry."""
        return Device(
            config_entries={config_entry_id},
            connections=self.connections & connections,
            identifiers=self.identifiers & identifiers,
            device_id=self.id,
            is_new=True,
        )
