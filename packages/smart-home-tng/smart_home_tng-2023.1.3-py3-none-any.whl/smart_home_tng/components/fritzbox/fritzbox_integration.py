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

import typing

import pyfritzhome as fritz

from ... import core
from .const import Const
from .fritzbox_binary_sensor import async_setup_binary_sensors
from .fritzbox_config_flow import FritzboxConfigFlow
from .fritzbox_cover import async_setup_covers
from .fritzbox_data_update_coordinator import FritzboxDataUpdateCoordinator
from .fritzbox_light import async_setup_lights
from .fritzbox_sensor import async_setup_sensors
from .fritzbox_switch import async_setup_switches
from .fritzbox_thermostat import async_setup_thermostats

_TO_REDACT: typing.Final = {core.Const.CONF_USERNAME, core.Const.CONF_PASSWORD}


# pylint: disable=unused-variable
class FritzboxIntegration(
    core.SmartHomeControllerComponent, core.ConfigFlowPlatform, core.DiagnosticsPlatform
):
    """Support for AVM FRITZ!SmartHome devices."""

    def __init__(self, path: typing.Iterable[str]):
        super().__init__(path)
        self._register_flow()
        self._connection_config: dict[str, dict[str, typing.Any]] = {}
        self._supported_platforms = Const.PLATFORMS + [
            core.Platform.DIAGNOSTICS,
            core.Platform.CONFIG_FLOW,
        ]

    @property
    def connection_config(self) -> dict[str, dict[str, typing.Any]]:
        return self._connection_config

    async def async_setup_entry(self, entry: core.ConfigEntry) -> bool:
        """Set up the AVM FRITZ!SmartHome platforms."""
        fritzhome = fritz.Fritzhome(
            host=entry.data[core.Const.CONF_HOST],
            user=entry.data[core.Const.CONF_USERNAME],
            password=entry.data[core.Const.CONF_PASSWORD],
        )

        try:
            await self.controller.async_add_executor_job(fritzhome.login)
        except fritz.LoginError as err:
            raise core.ConfigEntryAuthFailed from err

        self._connection_config[entry.entry_id] = {
            Const.CONF_CONNECTIONS: fritzhome,
        }

        coordinator = FritzboxDataUpdateCoordinator(self, entry)

        await coordinator.async_config_entry_first_refresh()

        self._connection_config[entry.entry_id][Const.CONF_COORDINATOR] = coordinator

        def _update_unique_id(entry: core.EntityRegistryEntry) -> dict[str, str]:
            """Update unique ID of entity entry."""
            if (
                entry.unit_of_measurement == core.Const.UnitOfTemperature.CELSIUS
                and "_temperature" not in entry.unique_id
            ):
                new_unique_id = f"{entry.unique_id}_temperature"
                Const.LOGGER.info(
                    f"Migrating unique_id [{entry.unique_id}] to [{new_unique_id}]"
                )
                return {"new_unique_id": new_unique_id}

            if entry.domain == "binary_sensor" and "_" not in entry.unique_id:
                new_unique_id = f"{entry.unique_id}_alarm"
                Const.LOGGER.info(
                    f"Migrating unique_id [{entry.unique_id}] to [{new_unique_id}]"
                )
                return {"new_unique_id": new_unique_id}
            return None

        await self.controller.entity_registry.async_migrate_entries(
            entry.entry_id, _update_unique_id
        )

        await self.controller.config_entries.async_forward_entry_setups(
            entry, Const.PLATFORMS
        )

        def logout_fritzbox(_event: core.Event) -> None:
            """Close connections to this fritzbox."""
            fritzhome.logout()

        entry.async_on_unload(
            self.controller.bus.async_listen_once(
                core.Const.EVENT_SHC_STOP, logout_fritzbox
            )
        )

        return True

    async def async_unload_entry(self, entry: core.ConfigEntry) -> bool:
        """Unloading the AVM FRITZ!SmartHome platforms."""
        fritzhome: fritz.Fritzhome = self._connection_config[entry.entry_id][
            Const.CONF_CONNECTIONS
        ]
        await self.controller.async_add_executor_job(fritzhome.logout)

        unload_ok = await self.controller.config_entries.async_unload_platforms(
            entry, Const.PLATFORMS
        )
        if unload_ok:
            self._connection_config.pop(entry.entry_id)

        return unload_ok

    async def async_setup_platform_devices(
        self, entry: core.ConfigEntry, async_add_entities: core.AddEntitiesCallback
    ) -> None:
        entity_platform = core.EntityPlatform.async_get_current_platform()
        platform = entity_platform.domain
        if platform == core.Platform.BINARY_SENSOR:
            await async_setup_binary_sensors(self, entry, async_add_entities)
        elif platform == core.Platform.CLIMATE:
            await async_setup_thermostats(self, entry, async_add_entities)
        elif platform == core.Platform.COVER:
            await async_setup_covers(self, entry, async_add_entities)
        elif platform == core.Platform.LIGHT:
            await async_setup_lights(self, entry, async_add_entities)
        elif platform == core.Platform.SENSOR:
            await async_setup_sensors(self, entry, async_add_entities)
        elif platform == core.Platform.SWITCH:
            await async_setup_switches(self, entry, async_add_entities)

    # -------------------------- Config Flow Platform -------------------------

    def create_config_flow(
        self, context: dict, init_data: typing.Any
    ) -> core.ConfigFlow:
        return FritzboxConfigFlow(self.controller, self.domain, context, init_data)

    # -------------------------- Diagnostic Platform ------------------------------

    async def async_get_config_entry_diagnostics(
        self, config_entry: core.ConfigEntry
    ) -> typing.Any:
        """Return diagnostics for a config entry."""
        data: dict = self._connection_config[config_entry.entry_id]
        coordinator: FritzboxDataUpdateCoordinator = data[Const.CONF_COORDINATOR]

        diag_data = {
            "entry": core.Diagnostics.async_redact_data(
                config_entry.as_dict(), _TO_REDACT
            ),
            "data": {},
        }
        if not isinstance(coordinator.data, dict):
            return diag_data

        diag_data["data"] = {
            ain: {k: v for k, v in vars(dev).items() if not k.startswith("_")}
            for ain, dev in coordinator.data.items()
        }
        return diag_data
