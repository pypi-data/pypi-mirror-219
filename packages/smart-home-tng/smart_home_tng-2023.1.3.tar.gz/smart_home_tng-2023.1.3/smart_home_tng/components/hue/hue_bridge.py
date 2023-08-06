"""
Philips Hue Integration for Smart Home - The Next Generation.

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
import logging
import typing

import aiohttp
import aiohue
import async_timeout

from ... import core
from .v1 import SensorManager
from .v2 import async_setup_devices, async_setup_hue_events

_PLATFORMS_V1: typing.Final = [
    core.Platform.BINARY_SENSOR,
    core.Platform.LIGHT,
    core.Platform.SENSOR,
]
_PLATFORMS_V2: typing.Final = [
    core.Platform.BINARY_SENSOR,
    core.Platform.LIGHT,
    core.Platform.SCENE,
    core.Platform.SENSOR,
    core.Platform.SWITCH,
]


# pylint: disable=unused-variable
class HueBridge:
    """Manages a single Hue bridge."""

    def __init__(
        self, owner: core.SmartHomeControllerComponent, config_entry: core.ConfigEntry
    ) -> None:
        """Initialize the system."""
        self._config_entry = config_entry
        self._owner = owner
        self._authorized = False
        # Jobs to be executed when API is reset.
        self._reset_jobs: list[core.CallbackType] = []
        self._sensor_manager: SensorManager = None
        self._logger = logging.getLogger(__name__)
        # store actual api connection to bridge as api
        app_key: str = config_entry.data[core.Const.CONF_API_KEY]
        if self.api_version == 1:
            self._api = aiohue.HueBridgeV1(
                self.host,
                app_key,
                core.HttpClient.async_get_clientsession(owner.controller),
            )
        else:
            self._api = aiohue.HueBridgeV2(self.host, app_key)

    @property
    def api(self) -> aiohue.HueBridgeV1 | aiohue.HueBridgeV2:
        return self._api

    @property
    def config_entry(self) -> core.ConfigEntry:
        return self._config_entry

    @property
    def controller(self) -> core.SmartHomeController:
        return self._owner.controller

    @property
    def owner(self) -> core.SmartHomeControllerComponent:
        return self._owner

    @property
    def logger(self) -> logging.Logger:
        return self._logger

    @property
    def reset_jobs(self) -> list[core.CallbackType]:
        return self._reset_jobs

    @property
    def sensor_manager(self) -> SensorManager:
        return self._sensor_manager

    @property
    def host(self) -> str:
        """Return the host of this bridge."""
        return self._config_entry.data[core.Const.CONF_HOST]

    @property
    def api_version(self) -> int:
        """Return api version we're set-up for."""
        return self._config_entry.data[core.Const.CONF_API_VERSION]

    async def async_initialize_bridge(self) -> bool:
        """Initialize Connection with the Hue API."""
        try:
            with async_timeout.timeout(10):
                await self._api.initialize()

        except (aiohue.LinkButtonNotPressed, aiohue.Unauthorized):
            # Usernames can become invalid if hub is reset or user removed.
            # We are going to fail the config entry setup and initiate a new
            # linking procedure. When linking succeeds, it will remove the
            # old config entry.
            _create_config_flow(self._owner, self.host)
            return False
        except (
            asyncio.TimeoutError,
            aiohttp.ClientOSError,
            aiohttp.ServerDisconnectedError,
            aiohttp.ContentTypeError,
            aiohue.BridgeBusy,
        ) as err:
            raise core.ConfigEntryNotReady(
                f"Error connecting to the Hue bridge at {self.host}"
            ) from err
        except Exception:  # pylint: disable=broad-except
            self._logger.exception("Unknown error connecting to Hue bridge")
            return False

        # v1 specific initialization/setup code here
        if self.api_version == 1:
            if self._api.sensors is not None:
                self._sensor_manager = SensorManager(self)
            await self._owner.controller.config_entries.async_forward_entry_setups(
                self._config_entry, _PLATFORMS_V1
            )

        # v2 specific initialization/setup code here
        else:
            await async_setup_devices(self)
            await async_setup_hue_events(self)
            await self._owner.controller.config_entries.async_forward_entry_setups(
                self._config_entry, _PLATFORMS_V2
            )

        # add listener for config entry updates.
        self._reset_jobs.append(
            self._config_entry.add_update_listener(_update_listener)
        )
        self._authorized = True
        return True

    async def async_request_call(
        self, task: typing.Callable, *args, **kwargs
    ) -> typing.Any:
        """Send request to the Hue bridge."""
        try:
            return await task(*args, **kwargs)
        except aiohue.AiohueException as err:
            # The (new) Hue api can be a bit fanatic with throwing errors so
            # we have some logic to treat some responses as warning only.
            msg = f"Request failed: {err}"
            if "may not have effect" in str(err):
                # log only
                self._logger.debug(msg)
                return None
            raise core.SmartHomeControllerError(msg) from err
        except aiohttp.ClientError as err:
            raise core.SmartHomeControllerError(
                f"Request failed due connection error: {err}"
            ) from err

    async def async_reset(self) -> bool:
        """Reset this bridge to default state.

        Will cancel any scheduled setup retry and will unload
        the config entry.
        """
        # The bridge can be in 3 states:
        #  - Setup was successful, self.api is not None
        #  - Authentication was wrong, self.api is None, not retrying setup.

        # If the authentication was wrong.
        if self._api is None:
            return True

        while self._reset_jobs:
            self._reset_jobs.pop()()

        # Unload platforms
        return await self._owner.controller.config_entries.async_unload_platforms(
            self._config_entry,
            _PLATFORMS_V1 if self.api_version == 1 else _PLATFORMS_V2,
        )

    async def handle_unauthorized_error(self) -> None:
        """Create a new config flow when the authorization is no longer valid."""
        if not self._authorized:
            # we already created a new config flow, no need to do it again
            return
        self._logger.error(
            f"Unable to authorize to bridge {self.host}, setup the linking again"
        )
        self._authorized = False
        _create_config_flow(self._owner, self.host)


async def _update_listener(
    shc: core.SmartHomeController, entry: core.ConfigEntry
) -> None:
    """Handle ConfigEntry options update."""
    await shc.config_entries.async_reload(entry.entry_id)


def _create_config_flow(comp: core.SmartHomeControllerComponent, host: str) -> None:
    """Start a config flow."""
    comp.controller.async_create_task(
        comp.controller.config_entries.flow.async_init(
            comp.domain,
            context={"source": core.ConfigEntrySource.IMPORT},
            data={"host": host},
        )
    )
