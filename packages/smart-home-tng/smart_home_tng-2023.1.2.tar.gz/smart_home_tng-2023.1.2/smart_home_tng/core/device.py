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
from .device_base import DeviceBase
from .device_registry_entry_disabler import DeviceRegistryEntryDisabler
from .device_registry_entry_type import DeviceRegistryEntryType


# pylint: disable=unused-variable
class Device(DeviceBase):
    """Device Registry Entry."""

    def __init__(
        self,
        device_id: str = None,
        config_entries: set[str] = None,
        connections: set[tuple[str, str]] = None,
        identifiers: set[tuple[str, str]] = None,
        area_id: str = None,
        configuration_url: str = None,
        disabled_by: DeviceRegistryEntryDisabler = None,
        entry_type: DeviceRegistryEntryType = None,
        manufacturer: str = None,
        model: str = None,
        name_by_user: str = None,
        name: str = None,
        suggested_area: str = None,
        sw_version: str = None,
        hw_version: str = None,
        via_device_id: str = None,
        is_new: bool = False,
    ) -> None:
        if device_id is None:
            device_id = helpers.random_uuid_hex()
        super().__init__(
            device_id=device_id,
            config_entries=config_entries,
            connections=connections,
            identitifiers=identifiers,
        )
        self._area_id = area_id
        self._configuration_url = configuration_url
        self._disabled_by = disabled_by
        self._entry_type = entry_type
        self._manufacturer = manufacturer
        self._model = model
        self._name_by_user = name_by_user
        self._name = name
        self._suggested_area = suggested_area
        self._sw_version = sw_version
        self._hw_version = hw_version
        self._via_device_id = via_device_id
        # This value is not stored, just used to keep track of events to fire.
        self._is_new = is_new

    @property
    def area_id(self) -> str:
        return self._area_id

    @property
    def configuration_url(self) -> str:
        return self._configuration_url

    @property
    def disabled_by(self) -> DeviceRegistryEntryDisabler:
        return self._disabled_by

    @property
    def entry_type(self) -> DeviceRegistryEntryType:
        return self._entry_type

    @property
    def manufacturer(self) -> str:
        return self._manufacturer

    @property
    def model(self) -> str:
        return self._model

    @property
    def name_by_user(self) -> str:
        return self._name_by_user

    @property
    def name(self) -> str:
        return self._name

    @property
    def suggested_area(self) -> str:
        return self._suggested_area

    @property
    def hw_version(self) -> str:
        return self._hw_version

    @property
    def sw_version(self) -> str:
        return self._sw_version

    @property
    def via_device_id(self) -> str:
        return self._via_device_id

    @property
    def is_new(self) -> bool:
        return self._is_new

    @property
    def disabled(self) -> bool:
        """Return if entry is disabled."""
        return self.disabled_by is not None
