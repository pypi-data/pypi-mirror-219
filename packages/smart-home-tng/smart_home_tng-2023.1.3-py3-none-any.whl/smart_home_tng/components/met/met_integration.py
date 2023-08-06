"""
Met Integration for Smart Home - The Next Generation.

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

import logging
import typing

from ... import core
from .const import Const
from .met_data_update_coordinator import MetDataUpdateCoordinator
from .met_flow_handler import MetFlowHandler
from .met_weather import MetWeather

_PLATFORMS: typing.Final = [core.Platform.WEATHER]

_LOGGER = logging.getLogger(__name__)


# pylint: disable=unused-variable
class MetIntegration(core.SmartHomeControllerComponent, core.ConfigFlowPlatform):
    """The met component."""

    def __init__(self, path: typing.Iterable[str]):
        super().__init__(path)
        self._register_flow()
        self._supported_platforms = frozenset(_PLATFORMS + [core.Platform.CONFIG_FLOW])
        self._coordinators = dict[str, MetDataUpdateCoordinator]()

    async def async_setup_entry(self, entry: core.ConfigEntry) -> bool:
        """Set up Met as config entry."""
        # Don't setup if tracking home location and latitude or longitude isn't set.
        # Also, filters out our onboarding default location.

        shc = self.controller
        if entry.data.get(Const.CONF_TRACK_HOME, False) and (
            (not shc.config.latitude and not shc.config.longitude)
            or (
                shc.config.latitude == Const.DEFAULT_HOME_LATITUDE
                and shc.config.longitude == Const.DEFAULT_HOME_LONGITUDE
            )
        ):
            _LOGGER.warning(
                "Skip setting up met.no integration; No Home location has been set"
            )
            return False

        coordinator = MetDataUpdateCoordinator(self, entry)
        await coordinator.async_config_entry_first_refresh()

        if entry.data.get(Const.CONF_TRACK_HOME, False):
            coordinator.track_home()

        self._coordinators[entry.entry_id] = coordinator

        await shc.config_entries.async_forward_entry_setups(entry, _PLATFORMS)

        return True

    async def async_unload_entry(self, entry: core.ConfigEntry) -> bool:
        """Unload a config entry."""
        unload_ok = await self.controller.config_entries.async_unload_platforms(
            entry, _PLATFORMS
        )

        self._coordinators[entry.entry_id].untrack_home()
        self._coordinators.pop(entry.entry_id)

        return unload_ok

    async def async_setup_platform_devices(
        self, entry: core.ConfigEntry, async_add_entities: core.AddEntitiesCallback
    ) -> None:
        """Setup platform entities."""
        if self._current_platform == core.Platform.WEATHER:
            await self._async_setup_weather_entities(entry, async_add_entities)

    async def _async_setup_weather_entities(
        self, entry: core.ConfigEntry, async_add_entities: core.AddEntitiesCallback
    ) -> None:
        """Add a weather entity from a config_entry."""
        coordinator: MetDataUpdateCoordinator = self._coordinators[entry.entry_id]
        is_metric = self.controller.config.units.is_metric
        async_add_entities(
            [
                MetWeather(coordinator, entry.data, is_metric, False),
                MetWeather(coordinator, entry.data, is_metric, True),
            ]
        )

    def create_config_flow(
        self, context: dict, init_data: typing.Any
    ) -> core.ConfigFlow:
        return MetFlowHandler(self, context, init_data)
