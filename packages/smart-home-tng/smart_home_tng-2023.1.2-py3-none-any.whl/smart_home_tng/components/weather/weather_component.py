"""
Weather Component for Smart Home - The Next Generation.

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

import datetime as dt
import logging
import typing

from ... import core

_LOGGER: typing.Final = logging.getLogger(__name__)


# pylint: disable=unused-variable
class WeatherComponent(
    core.SmartHomeControllerComponent, core.GroupPlatform, core.RecorderPlatform
):
    """Weather component that handles meteorological data for your location."""

    def __init__(self, path: typing.Iterable[str]):
        super().__init__(path)
        self._component: core.EntityComponent = None
        self._supported_platforms = frozenset(
            [core.Platform.GROUP, core.Platform.RECORDER]
        )

    @property
    def entity_component(self) -> core.EntityComponent:
        return self._component

    @property
    def scan_interval(self) -> dt.timedelta:
        return dt.timedelta(seconds=30)

    async def async_setup(self, config: core.ConfigType) -> bool:
        """Set up the weather component."""
        if not await super().async_setup(config):
            return False

        self._component = core.EntityComponent(
            _LOGGER, self.domain, self._shc, self.scan_interval
        )
        await self._component.async_setup(config)
        return True

    async def async_setup_entry(self, entry: core.ConfigEntry) -> bool:
        """Set up a config entry."""

        return await self._component.async_setup_entry(entry)

    async def async_unload_entry(self, entry: core.ConfigEntry) -> bool:
        """Unload a config entry."""

        return await self._component.async_unload_entry(entry)

    def async_describe_on_off_states(
        self, registry: core.GroupIntegrationRegistry
    ) -> None:
        """Describe group on off states."""
        return registry.exclude_domain()

    def exclude_attributes(self) -> set[str]:
        """Exclude (often large) forecasts from being recorded in the database."""
        return {core.Const.ATTR_FORECAST}
