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


# pylint: disable=unused-variable
class DeviceBase:
    """
    Base class for device, will be used for deleted devices
    and device registry entries.
    """

    def __init__(
        self,
        device_id: str,
        config_entries: set[str] = None,
        connections: set[tuple[str, str]] = None,
        identitifiers: set[tuple[str, str]] = None,
    ) -> None:
        self._id = device_id
        self._config_entries = config_entries or set()
        self._connections = connections or set()
        self._identifiers = identitifiers or set()

    @property
    def id(self) -> str:
        return self._id

    @property
    def config_entries(self) -> set[str]:
        return self._config_entries

    @property
    def connections(self) -> set[tuple[str, str]]:
        return self._connections

    @property
    def identifiers(self) -> set[tuple[str, str]]:
        return self._identifiers
