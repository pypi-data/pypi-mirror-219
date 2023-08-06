"""
Camera Component for Smart Home - The Next Generation.

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
from .camera_entity_preferences import CameraEntityPreferences

_UNDEFINED: typing.Final = object()


# pylint: disable=unused-variable
class CameraPreferences:
    """Handle camera preferences."""

    def __init__(self, owner: core.SmartHomeControllerComponent) -> None:
        """Initialize camera prefs."""
        self._owner = owner
        self._store = core.Store[dict[str, dict[str, bool]]](
            owner.controller, owner.storage_version, owner.storage_key
        )
        self._prefs: dict[str, dict[str, bool]] = None

    async def async_initialize(self) -> None:
        """Finish initializing the preferences."""
        if (prefs := await self._store.async_load()) is None:
            prefs = {}

        self._prefs = prefs

    async def async_update(
        self,
        entity_id: str,
        *,
        preload_stream: bool | object = _UNDEFINED,
        _stream_options: dict[str, str] | object = _UNDEFINED,
    ) -> None:
        """Update camera preferences."""
        # Prefs already initialized.
        assert self._prefs is not None
        if not self._prefs.get(entity_id):
            self._prefs[entity_id] = {}

        for key, value in ((core.Camera.PREF_PRELOAD_STREAM, preload_stream),):
            if value is not _UNDEFINED:
                self._prefs[entity_id][key] = value

        await self._store.async_save(self._prefs)

    def get(self, entity_id: str) -> CameraEntityPreferences:
        """Get preferences for an entity."""
        # Prefs are already initialized.
        assert self._prefs is not None
        return CameraEntityPreferences(self._prefs.get(entity_id, {}))
