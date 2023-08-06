"""
AVM FRITZ!Box Tools Integration for Smart Home - The Next Generation.

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

import fritzconnection.core.exceptions as fritz_exceptions

from ... import core
from .avm_wrapper import AvmWrapper
from .const import Const
from .fritz_button import async_setup_buttons
from .fritz_data import FritzData
from .fritzbox_binary_sensor import async_setup_binary_sensors
from .fritzbox_sensor import async_setup_sensors
from .fritzbox_tools_flow_handler import FritzboxToolsFlowHandler
from .fritzbox_tools_options_flow_handler import FritzboxToolsOptionsFlowHandler
from .fritzbox_tracker import async_setup_device_trackers
from .fritzbox_update_entity import FritzboxUpdateEntity
from .services import async_setup_services, async_unload_services
from .switches import async_setup_switches

_LOGGER: typing.Final = logging.getLogger(__name__)
_TO_REDACT: typing.Final = {core.Const.CONF_USERNAME, core.Const.CONF_PASSWORD}


# pylint: disable=unused-variable
class FritzboxToolsIntegration(
    core.SmartHomeControllerComponent, core.ConfigFlowPlatform, core.DiagnosticsPlatform
):
    """Support for AVM Fritz!Box functions."""

    def __init__(self, path: typing.Iterable[str]):
        super().__init__(path)
        self._register_flow()
        self._wrappers: dict[str, AvmWrapper] = {}
        self._fritz_data = FritzData()
        self._services_registered = False
        self._supported_platforms = frozenset(
            Const.PLATFORMS
            + [
                core.Platform.CONFIG_FLOW,
                core.Platform.DIAGNOSTICS,
                core.Platform.SENSOR,
            ]
        )

    @property
    def data(self):
        return self._fritz_data

    @property
    def services_registered(self):
        return self._services_registered

    @property
    def wrappers(self):
        return self._wrappers

    async def async_setup_entry(self, entry: core.ConfigEntry) -> bool:
        """Set up fritzboxtools from config entry."""
        _LOGGER.debug("Setting up FRITZ!Box Tools component")
        avm_wrapper = AvmWrapper(
            owner=self,
            host=entry.data[core.Const.CONF_HOST],
            port=entry.data[core.Const.CONF_PORT],
            username=entry.data[core.Const.CONF_USERNAME],
            password=entry.data[core.Const.CONF_PASSWORD],
        )

        try:
            await avm_wrapper.async_setup(entry.options)
        except Const.FRITZ_EXCEPTIONS as ex:
            raise core.ConfigEntryNotReady from ex
        except fritz_exceptions.FritzConnectionException as ex:
            raise core.ConfigEntryAuthFailed from ex

        if (
            "X_AVM-DE_UPnP1" in avm_wrapper.connection.services
            and not (await avm_wrapper.async_get_upnp_configuration())["NewEnable"]
        ):
            raise core.ConfigEntryAuthFailed("Missing UPnP configuration")

        self._wrappers[entry.entry_id] = avm_wrapper

        entry.async_on_unload(entry.add_update_listener(update_listener))

        await avm_wrapper.async_config_entry_first_refresh()

        # Load the other platforms like switch
        await self.controller.config_entries.async_forward_entry_setups(
            entry, Const.PLATFORMS
        )

        if not self._services_registered:
            self._services_registered = await async_setup_services(self)

        return True

    async def async_unload_entry(self, entry: core.ConfigEntry) -> bool:
        """Unload FRITZ!Box Tools config entry."""
        avm_wrapper = self._wrappers[entry.entry_id]

        fritz_data = self._fritz_data
        fritz_data.tracked.pop(avm_wrapper.unique_id)

        unload_ok = await self.controller.config_entries.async_unload_platforms(
            entry, Const.PLATFORMS
        )
        if unload_ok:
            self._wrappers.pop(entry.entry_id)

        await async_unload_services(self)
        self._services_registered = False

        return unload_ok

    async def async_setup_platform_devices(
        self, entry: core.ConfigEntry, async_add_entities: core.AddEntitiesCallback
    ) -> None:
        entity_platform = core.EntityPlatform.async_get_current_platform()
        platform = entity_platform.domain
        if platform == core.Platform.BINARY_SENSOR:
            await async_setup_binary_sensors(self, entry, async_add_entities)
        elif platform == core.Platform.BUTTON:
            await async_setup_buttons(self, entry, async_add_entities)
        elif platform == core.Platform.DEVICE_TRACKER:
            await async_setup_device_trackers(self, entry, async_add_entities)
        elif platform == core.Platform.SENSOR:
            await async_setup_sensors(self, entry, async_add_entities)
        elif platform == core.Platform.SWITCH:
            await async_setup_switches(self, entry, async_add_entities)
        elif platform == core.Platform.UPDATE:
            # Set up AVM FRITZ!Box update entities.
            _LOGGER.debug("Setting up AVM FRITZ!Box update entities")
            avm_wrapper = self.wrappers[entry.entry_id]

            entities = [FritzboxUpdateEntity(self, avm_wrapper, entry.title)]

            async_add_entities(entities)

    # ---------------------- ConfigFlow Platform ---------------------------

    def create_config_flow(
        self, context: dict, init_data: typing.Any
    ) -> core.ConfigFlow:
        return FritzboxToolsFlowHandler(
            self.controller, self.domain, context, init_data
        )

    async def async_get_options_flow(
        self,
        entry: core.ConfigEntry,
        context: dict = None,
        init_data: typing.Any = None,
    ) -> core.OptionsFlow:
        """Get the options flow for this handler."""
        return FritzboxToolsOptionsFlowHandler(entry, context, init_data)

    # ---------------------- ConfigFlow Platform ---------------------------

    async def async_get_config_entry_diagnostics(
        self, config_entry: core.ConfigEntry
    ) -> typing.Any:
        """Return diagnostics for a config entry."""
        avm_wrapper: AvmWrapper = self.wrappers[config_entry.entry_id]

        diag_data = {
            "entry": core.Diagnostics.async_redact_data(
                config_entry.as_dict(), _TO_REDACT
            ),
            "device_info": {
                "model": avm_wrapper.model,
                "unique_id": avm_wrapper.unique_id.replace(
                    avm_wrapper.unique_id[6:11], "XX:XX"
                ),
                "current_firmware": avm_wrapper.current_firmware,
                "latest_firmware": avm_wrapper.latest_firmware,
                "update_available": avm_wrapper.update_available,
                "connection_type": avm_wrapper.device_conn_type,
                "is_router": avm_wrapper.device_is_router,
                "mesh_role": avm_wrapper.mesh_role,
                "last_update success": avm_wrapper.last_update_success,
                "last_exception": avm_wrapper.last_exception,
                "discovered_services": list(avm_wrapper.connection.services),
                "client_devices": [
                    {
                        "connected_to": device.connected_to,
                        "connection_type": device.connection_type,
                        "hostname": device.hostname,
                        "is_connected": device.is_connected,
                        "last_activity": device.last_activity,
                        "wan_access": device.wan_access,
                    }
                    for _, device in avm_wrapper.devices.items()
                ],
                "wan_link_properties": await avm_wrapper.async_get_wan_link_properties(),
            },
        }

        return diag_data


async def update_listener(
    shc: core.SmartHomeController, entry: core.ConfigEntry
) -> None:
    """Update when config_entry options update."""
    if entry.options:
        await shc.config_entries.async_reload(entry.entry_id)
