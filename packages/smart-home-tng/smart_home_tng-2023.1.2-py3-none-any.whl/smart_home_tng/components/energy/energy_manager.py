"""
Energy Component for Smart Home - The Next Generation.

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

import asyncio
import collections.abc
import typing

from ... import core
from .energy_preferences import EnergyPreferences
from .energy_preferences_update import EnergyPreferencesUpdate


# pylint: disable=unused-variable
class EnergyManager:
    """Manage the instance energy prefs."""

    def __init__(
        self, shc: core.SmartHomeController, storage_version: int, storage_key: str
    ) -> None:
        """Initialize energy manager."""
        self._shc = shc
        self._store = core.Store[EnergyPreferences](shc, storage_version, storage_key)
        self._data: EnergyPreferences = None
        self._update_listeners: list[
            collections.abc.Callable[[], collections.abc.Awaitable]
        ] = []

    async def async_initialize(self) -> None:
        """Initialize the energy integration."""
        self._data = await self._store.async_load()

    @property
    def data(self) -> EnergyPreferences:
        return self._data

    @staticmethod
    def default_preferences() -> EnergyPreferences:
        """Return default preferences."""
        return {
            "energy_sources": [],
            "device_consumption": [],
        }

    async def async_update(self, update: EnergyPreferencesUpdate) -> None:
        """Update the preferences."""
        if self._data is None:
            data = EnergyManager.default_preferences()
        else:
            data = self._data.copy()

        for key in (
            "energy_sources",
            "device_consumption",
        ):
            if key in update:
                data[key] = update[key]

        self._data = data
        self._store.async_delay_save(lambda: typing.cast(dict, self._data), 60)

        if not self._update_listeners:
            return

        await asyncio.gather(*(listener() for listener in self._update_listeners))

    @core.callback
    def async_listen_updates(
        self, update_listener: collections.abc.Callable[[], collections.abc.Awaitable]
    ) -> None:
        """Listen for data updates."""
        self._update_listeners.append(update_listener)
