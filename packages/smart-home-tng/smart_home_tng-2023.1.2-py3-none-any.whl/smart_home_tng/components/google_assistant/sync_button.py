"""
Google Assistant Integration  for Smart Home - The Next Generation.

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
from .google_config import GoogleConfig

_google: typing.TypeAlias = core.GoogleAssistant


# pylint: disable=unused-variable
class SyncButton(core.Button.Entity):
    """Representation of a synchronization button."""

    def __init__(self, project_id: str, google_config: GoogleConfig) -> None:
        """Initialize button."""
        super().__init__()
        self._google_config = google_config
        self._attr_entity_category = core.EntityCategory.DIAGNOSTIC
        self._attr_unique_id = f"{project_id}_sync"
        self._attr_name = "Synchronize Devices"
        self._attr_device_info = core.DeviceInfo(
            identifiers={(google_config.owner.domain, project_id)}
        )

    async def async_press(self) -> None:
        """Press the button."""
        assert self._context
        agent_user_id = self._google_config.get_agent_user_id(self._context)
        result = await self._google_config.async_sync_entities(agent_user_id)
        if result != 200:
            raise core.SmartHomeControllerError(
                f"Unable to sync devices with result code: {result}, check log for more info."
            )


async def async_setup_buttons(
    config_entry: core.ConfigEntry,
    async_add_entities: core.AddEntitiesCallback,
    config: core.ConfigType,
    google_config: GoogleConfig,
):
    """Set up the platform."""
    entities = []

    if _google.CONF_SERVICE_ACCOUNT in config:
        entities.append(
            SyncButton(config_entry.data[_google.CONF_PROJECT_ID], google_config)
        )

    async_add_entities(entities)
