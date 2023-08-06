"""
Bosch SHC Integration for Smart Home - The Next Generation.

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

import boschshcpy as bosch
import voluptuous as vol

from ... import core
from .binary_sensors import _async_setup_binary_sensors
from .bosch_config_flow import BoschConfigFlow
from .bosch_entity import BoschEntity
from .bosch_switch import _async_setup_switches
from .climate_control import _async_setup_climate_controls
from .const import Const
from .intrusion_system_alarm_control_panel import _async_setup_alarm_control_panel
from .light_switch import _async_setup_light_switches
from .sensors import _async_setup_sensors
from .shutter_control_cover import _async_setup_shutter_control_covers
from .switch_device_event_listener import SwitchDeviceEventListener

_cv: typing.TypeAlias = core.ConfigValidation

_LOGGER: typing.Final = logging.getLogger(__name__)

_PLATFORMS: typing.Final = [
    core.Platform.ALARM_CONTROL_PANEL,
    core.Platform.BINARY_SENSOR,
    core.Platform.CLIMATE,
    core.Platform.COVER,
    core.Platform.LIGHT,
    core.Platform.SENSOR,
    core.Platform.SWITCH,
]


# pylint: disable=unused-variable
class BoschShcIntegration(core.SmartHomeControllerComponent, core.ConfigFlowPlatform):
    """The Bosch Smart Home Controller integration."""

    def __init__(self, path: typing.Iterable[str]):
        super().__init__(path)
        self._register_flow()
        self._sessions: dict[str, bosch.SHCSession] = {}
        self._polling_handlers: dict[str, core.CallbackType] = {}
        self._supported_platforms = frozenset(
            _PLATFORMS
            + [core.Platform.CONFIG_FLOW, core.Platform.LOGBOOK, core.Platform.TRIGGER]
        )

    async def async_setup_entry(self, entry: core.ConfigEntry) -> bool:
        """Set up Bosch SHC from a config entry."""
        data = entry.data
        shc = self.controller

        zc = self.get_component(core.Const.ZEROCONF_COMPONENT_NAME)
        if not isinstance(zc, core.ZeroconfComponent):
            return False

        zeroconf = await zc.async_get_instance()
        try:
            session = await shc.async_add_executor_job(
                bosch.SHCSession,
                data[core.Const.CONF_HOST],
                data[core.Const.CONF_SSL_CERTIFICATE],
                data[core.Const.CONF_SSL_KEY],
                False,
                zeroconf,
            )
        except bosch.SHCAuthenticationError as err:
            raise core.ConfigEntryAuthFailed from err
        except bosch.SHCConnectionError as err:
            raise core.ConfigEntryNotReady from err

        shc_info = session.information
        if shc_info.updateState.name == "UPDATE_AVAILABLE":
            _LOGGER.warning(
                "Please check for software updates in the Bosch Smart Home App"
            )
            notify: core.PersistentNotificationComponent = (
                self.controller.components.persistent_notification
            )
            if notify is not None:
                notify.async_create(
                    "Update verfügbar. Prüfe in der Bosch Smart Home App die Software-Updates.",
                    "Bosch Smart Home Controller",
                )

        self._sessions[entry.entry_id] = session

        device_registry = shc.device_registry
        device_entry = device_registry.async_get_or_create(
            config_entry_id=entry.entry_id,
            connections={
                (
                    core.DeviceRegistry.ConnectionType.MAC,
                    core.helpers.format_mac(shc_info.unique_id),
                )
            },
            identifiers={(self.domain, shc_info.unique_id)},
            manufacturer="Bosch",
            name=entry.title,
            model="SmartHomeController",
            sw_version=shc_info.version,
        )
        device_id = device_entry.id

        shc.config_entries.async_setup_platforms(entry, _PLATFORMS)

        async def stop_polling(_event):
            """Stop polling service."""
            await shc.async_add_executor_job(session.stop_polling)

        await shc.async_add_executor_job(session.start_polling)
        self._polling_handlers[entry.entry_id] = shc.bus.async_listen_once(
            core.Const.EVENT_SHC_STOP, stop_polling
        )

        @core.callback
        def _async_scenario_trigger(scenario_id, name, last_time_triggered):
            shc.bus.async_fire(
                Const.EVENT_BOSCH_SHC,
                {
                    core.Const.ATTR_DEVICE_ID: device_id,
                    core.Const.ATTR_ID: scenario_id,
                    core.Const.ATTR_NAME: shc_info.name,
                    Const.ATTR_LAST_TIME_TRIGGERED: last_time_triggered,
                    Const.ATTR_EVENT_TYPE: "SCENARIO",
                    Const.ATTR_EVENT_SUBTYPE: name,
                },
            )

        session.subscribe_scenario_callback(_async_scenario_trigger)

        for switch_device in session.device_helper.universal_switches:
            event_listener = SwitchDeviceEventListener(self, entry, switch_device)
            await event_listener.async_setup()

        self._register_services(entry)

        return True

    async def async_unload_entry(self, entry: core.ConfigEntry) -> bool:
        """Unload a config entry."""
        session = self._sessions[entry.entry_id]
        session.unsubscribe_scenario_callback()

        polling_handler = self._polling_handlers.pop(entry.entry_id)
        polling_handler()
        await self.controller.async_add_executor_job(session.stop_polling)

        unload_ok = await self.controller.config_entries.async_unload_platforms(
            entry, _PLATFORMS
        )
        if unload_ok:
            self._sessions.pop(entry.entry_id)
        return unload_ok

    def _register_services(self, entry: core.ConfigEntry):
        """Register services for the component."""
        TRIGGER_SCHEMA: typing.Final = vol.Schema(
            {
                vol.Required(core.Const.ATTR_NAME): vol.All(
                    _cv.string,
                    vol.In(self._sessions[entry.entry_id].scenario_names),
                )
            }
        )

        async def scenario_service_call(call: core.ServiceCall):
            """SHC Scenario service call."""
            name = call.data[core.Const.ATTR_NAME]
            for scenario in self._sessions[entry.entry_id].scenarios:
                if scenario.name == name:
                    self.controller.async_add_executor_job(scenario.trigger)

        self.controller.services.async_register(
            self.domain,
            Const.SERVICE_TRIGGER_SCENARIO,
            scenario_service_call,
            TRIGGER_SCHEMA,
        )

    def create_config_flow(
        self, context: dict, init_data: typing.Any
    ) -> core.ConfigFlow:
        return BoschConfigFlow(self, context=context, data=init_data)

    async def async_setup_platform_devices(
        self, entry: core.ConfigEntry, async_add_entities: core.AddEntitiesCallback
    ) -> None:
        devices = None
        session = self._sessions[entry.entry_id]

        entity_platform = core.EntityPlatform.async_get_current_platform()
        cpf = entity_platform.domain
        if cpf == core.Platform.ALARM_CONTROL_PANEL:
            devices = await _async_setup_alarm_control_panel(self, session, entry)
        elif cpf == core.Platform.BINARY_SENSOR:
            devices = await _async_setup_binary_sensors(self, session, entry)
        elif cpf == core.Platform.CLIMATE:
            devices = await _async_setup_climate_controls(self, session, entry)
        elif cpf == core.Platform.COVER:
            devices = await _async_setup_shutter_control_covers(self, session, entry)
        elif cpf == core.Platform.LIGHT:
            devices = await _async_setup_light_switches(self, session, entry)
        elif cpf == core.Platform.SENSOR:
            devices = await _async_setup_sensors(self, session, entry)
        elif cpf == core.Platform.SWITCH:
            devices = await _async_setup_switches(self, session, entry)

        if devices:
            async_add_entities(devices)

    async def async_get_device_id(self, device_id):
        """Get device id from device registry."""
        dev_registry = self.controller.device_registry
        device = dev_registry.async_get_device(
            identifiers={(self.domain, device_id)}, connections=set()
        )
        return device.id if device is not None else None

    async def async_remove_devices(self, entity: BoschEntity, entry_id: str):
        """Get item that is removed from session."""
        dev_registry = self.controller.device_registry
        device = dev_registry.async_get_device(
            identifiers={(self.domain, entity.device_id)}, connections=set()
        )
        if device is not None:
            dev_registry.async_update_device(device.id, remove_config_entry_id=entry_id)
