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

import datetime as dt
import logging
import random
import typing

from ... import core
from .met_weather_data import MetWeatherData

_LOGGER: typing.Final = logging.getLogger(__name__)


# pylint: disable=unused-variable
class MetDataUpdateCoordinator(core.DataUpdateCoordinator["MetWeatherData"]):
    """Class to manage fetching Met data."""

    def __init__(
        self, owner: core.SmartHomeControllerComponent, config_entry: core.ConfigEntry
    ) -> None:
        """Initialize global Met data updater."""
        self._unsub_track_home: typing.Callable[[], None] = None
        self._weather = MetWeatherData(
            owner.controller, config_entry.data, owner.controller.config.units.is_metric
        )
        self._weather.set_coordinates()
        self._owner = owner

        update_interval = dt.timedelta(minutes=random.randrange(55, 65))  # nosec

        super().__init__(
            owner.controller,
            _LOGGER,
            name=owner.domain,
            update_interval=update_interval,
        )

    @property
    def owner(self) -> core.SmartHomeControllerComponent:
        return self._owner

    async def _async_update_data(self) -> MetWeatherData:
        """Fetch data from Met."""
        try:
            return await self._weather.fetch_data()
        except Exception as err:
            raise core.UpdateFailed(f"Update failed: {err}") from err

    def track_home(self) -> None:
        """Start tracking changes to HA home setting."""
        if self._unsub_track_home:
            return

        self._unsub_track_home = self._shc.bus.async_listen(
            core.Const.EVENT_CORE_CONFIG_UPDATE, self._async_update_weather_data
        )

    async def _async_update_weather_data(self, _event: core.Event = None) -> None:
        """Update weather data."""
        if self._weather.set_coordinates():
            await self.async_refresh()

    def untrack_home(self) -> None:
        """Stop tracking changes to HA home setting."""
        if self._unsub_track_home:
            self._unsub_track_home()
            self._unsub_track_home = None
