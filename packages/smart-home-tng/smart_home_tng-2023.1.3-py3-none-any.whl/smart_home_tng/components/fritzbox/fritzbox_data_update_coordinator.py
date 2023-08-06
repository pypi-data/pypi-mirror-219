"""
AVM FRITZ!SmartHome Integration for Smart Home - The Next Generation.

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
import typing

import pyfritzhome as fritz
import requests

from ... import core
from .const import Const

if not typing.TYPE_CHECKING:

    class FritzboxIntegration:
        pass


if typing.TYPE_CHECKING:
    from .fritzbox_integration import FritzboxIntegration


# pylint: disable=unused-variable
class FritzboxDataUpdateCoordinator(core.DataUpdateCoordinator):
    """Fritzbox Smarthome device data update coordinator."""

    _configuration_url: str

    def __init__(self, owner: FritzboxIntegration, entry: core.ConfigEntry) -> None:
        """Initialize the Fritzbox Smarthome device coordinator."""
        self._entry = entry
        self._owner = owner
        self._fritz: fritz.Fritzhome = owner.connection_config[entry.entry_id][
            Const.CONF_CONNECTIONS
        ]
        self._configuration_url = self._fritz.get_prefixed_host()
        request_refresh_debouncer = core.Debouncer(
            owner.controller,
            Const.LOGGER,
            cooldown=1,
            immediate=False,
        )

        super().__init__(
            owner.controller,
            Const.LOGGER,
            name=entry.entry_id,
            update_interval=dt.timedelta(seconds=10),
            request_refresh_debouncer=request_refresh_debouncer,
        )

    @property
    def configuration_url(self) -> str:
        return self._configuration_url

    @property
    def owner(self) -> FritzboxIntegration:
        return self._owner

    def _update_fritz_devices(self) -> dict[str, fritz.FritzhomeDevice]:
        """Update all fritzbox device data."""
        try:
            self._fritz.update_devices()
        except requests.exceptions.ConnectionError as ex:
            raise core.UpdateFailed from ex
        except requests.exceptions.HTTPError:
            # If the device rebooted, login again
            try:
                self._fritz.login()
            except fritz.LoginError as ex:
                raise core.ConfigEntryAuthFailed from ex
            self._fritz.update_devices()

        devices = self._fritz.get_devices()
        data = {}
        for device in devices:
            # assume device as unavailable, see #55799
            if (
                device.has_powermeter
                and device.present
                and hasattr(device, "voltage")
                and device.voltage <= 0
                and device.power <= 0
                and device.energy <= 0
            ):
                Const.LOGGER.debug(f"Assume device {device.name} as unavailable")
                device.present = False

            data[device.ain] = device
        return data

    async def _async_update_data(self) -> dict[str, fritz.FritzhomeDevice]:
        """Fetch all device data."""
        return await self._shc.async_add_executor_job(self._update_fritz_devices)
