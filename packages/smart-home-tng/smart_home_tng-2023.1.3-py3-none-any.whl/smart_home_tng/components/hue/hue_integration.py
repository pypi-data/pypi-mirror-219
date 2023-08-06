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

import aiohue
import voluptuous as vol

from ... import core
from .const import Const
from .hue_bridge import HueBridge
from .hue_flow_handler import HueFlowHandler
from .hue_v1_options_flow_handler import HueV1OptionsFlowHandler
from .hue_v2_options_flow_handler import HueV2OptionsFlowHandler
from .services import _hue_activate_scene_v1, _hue_activate_scene_v2
from .v1 import async_setup_binary_sensors as async_setup_binary_sensors_v1
from .v1 import async_setup_sensors as async_setup_sensors_v1
from .v1.device_trigger import async_attach_trigger as async_attach_trigger_v1
from .v1.device_trigger import async_get_triggers as async_get_triggers_v1
from .v1.device_trigger import (
    async_validate_trigger_config as async_validate_trigger_config_v1,
)
from .v1.hue_light import async_setup_lights as async_setup_lights_v1
from .v2 import async_setup_binary_sensors as async_setup_binary_sensors_v2
from .v2 import async_setup_scenes
from .v2 import async_setup_sensors as async_setup_sensors_v2
from .v2 import async_setup_switches
from .v2.device_trigger import async_attach_trigger as async_attach_trigger_v2
from .v2.device_trigger import async_get_triggers as async_get_triggers_v2
from .v2.device_trigger import (
    async_validate_trigger_config as async_validate_trigger_config_v2,
)
from .v2.grouped_hue_light import async_setup_group_lights
from .v2.hue_light import async_setup_lights as async_setup_lights_v2

_cv: typing.TypeAlias = core.ConfigValidation
_LOGGER: typing.Final = logging.getLogger(__name__)
_TRIGGER_SUBTYPE: typing.Final = {
    "button_1": "first button",
    "button_2": "second button",
    "button_3": "third button",
    "button_4": "fourth button",
    "double_buttons_1_3": "first and third buttons",
    "double_buttons_2_4": "second and fourth buttons",
    "dim_down": "dim down",
    "dim_up": "dim up",
    "turn_off": "turn off",
    "turn_on": "turn on",
    "1": "first button",
    "2": "second button",
    "3": "third button",
    "4": "fourth button",
    "clock_wise": "Rotation clockwise",
    "counter_clock_wise": "Rotation counter-clockwise",
}
_TRIGGER_TYPE: typing.Final = {
    "remote_button_long_release": "{subtype} released after long press",
    "remote_button_short_press": "{subtype} pressed",
    "remote_button_short_release": "{subtype} released",
    "remote_double_button_long_press": "both {subtype} released after long press",
    "remote_double_button_short_press": "both {subtype} released",
    "initial_press": "{subtype} pressed initially",
    "repeat": "{subtype} held down",
    "short_release": "{subtype} released after short press",
    "long_release": "{subtype} released after long press",
    "double_short_release": "both {subtype} released",
    "start": '"{subtype}" pressed initially',
}

_UNKNOWN_TYPE: typing.Final = "unknown type"
_UNKNOWN_SUB_TYPE: typing.Final = "unknown sub type"


# pylint: disable=unused-variable
class HueIntegration(
    core.SmartHomeControllerComponent,
    core.ConfigFlowPlatform,
    core.DiagnosticsPlatform,
    core.LogbookPlatform,
    core.TriggerPlatform,
):
    """Support for the Philips Hue system."""

    def __init__(self, path: typing.Iterable[str]):
        super().__init__(path)
        self._register_flow()
        self._supported_platforms = frozenset(
            [
                core.Platform.BINARY_SENSOR,
                core.Platform.CONFIG_FLOW,
                core.Platform.DIAGNOSTICS,
                core.Platform.LIGHT,
                core.Platform.LOGBOOK,
                core.Platform.SCENE,
                core.Platform.SENSOR,
                core.Platform.SWITCH,
                core.Platform.TRIGGER,
            ]
        )
        self._bridges: dict[str, HueBridge] = {}

    async def async_setup_entry(self, entry: core.ConfigEntry) -> bool:
        """Set up a bridge from a config entry."""

        shc = self.controller

        # check (and run) migrations if needed
        # await check_migration(hass, entry)

        # setup the bridge instance
        bridge = HueBridge(self, entry)
        self._bridges[entry.entry_id] = bridge
        if not await bridge.async_initialize_bridge():
            return False

        # register Hue domain services
        self._async_register_services()

        api = bridge.api

        # For backwards compat
        unique_id = aiohue.util.normalize_bridge_id(api.config.bridge_id)
        if entry.unique_id is None:
            shc.config_entries.async_update_entry(entry, unique_id=unique_id)

        # For recovering from bug where we incorrectly assumed homekit ID = bridge ID
        # Remove this logic after Home Assistant 2022.4
        elif entry.unique_id != unique_id:
            # Find entries with this unique ID
            other_entry = next(
                (
                    entry
                    for entry in shc.config_entries.async_entries(self.domain)
                    if entry.unique_id == unique_id
                ),
                None,
            )
            if other_entry is None:
                # If no other entry, update unique ID of this entry ID.
                shc.config_entries.async_update_entry(entry, unique_id=unique_id)

            elif other_entry.source == core.ConfigEntrySource.IGNORE:
                # There is another entry but it is ignored, delete that one and
                # update this one
                shc.async_create_task(
                    shc.config_entries.async_remove(other_entry.entry_id)
                )
                shc.config_entries.async_update_entry(entry, unique_id=unique_id)
            else:
                # There is another entry that already has the right unique ID.
                # Delete this entry
                shc.async_create_task(shc.config_entries.async_remove(entry.entry_id))
                return False

        # add bridge device to device registry
        device_registry = shc.device_registry
        if bridge.api_version == 1:
            device_registry.async_get_or_create(
                config_entry_id=entry.entry_id,
                connections={
                    (device_registry.ConnectionType.MAC, api.config.mac_address)
                },
                identifiers={(self.domain, api.config.bridge_id)},
                manufacturer="Signify",
                name=api.config.name,
                model=api.config.model_id,
                sw_version=api.config.software_version,
            )
            # create persistent notification if we found a bridge version with
            # security vulnerability
            if (
                api.config.model_id == "BSB002"
                and api.config.software_version < "1935144040"
            ):
                shc.components.persistent_notification.async_create(
                    "Your Hue hub has a known security vulnerability ([CVE-2020-6007] "
                    + "(https://cve.circl.lu/cve/CVE-2020-6007)). "
                    + "Go to the Hue app and check for software updates.",
                    "Signify Hue",
                    "hue_hub_firmware",
                )
        else:
            device_registry.async_get_or_create(
                config_entry_id=entry.entry_id,
                connections={
                    (device_registry.ConnectionType.MAC, api.config.mac_address)
                },
                identifiers={
                    (self.domain, api.config.bridge_id),
                    (self.domain, api.config.bridge_device.id),
                },
                manufacturer=api.config.bridge_device.product_data.manufacturer_name,
                name=api.config.name,
                model=api.config.model_id,
                sw_version=api.config.software_version,
            )

        return True

    async def async_unload_entry(self, entry: core.ConfigEntry) -> bool:
        """Unload a config entry."""
        unload_success = await self._bridges[entry.entry_id].async_reset()
        if unload_success:
            self._bridges.pop(entry.entry_id)
            if len(self._bridges) == 0:
                self.controller.services.async_remove(
                    self.domain, Const.SERVICE_HUE_ACTIVATE_SCENE
                )
        return unload_success

    def _async_register_services(self) -> None:
        """Register services for Hue integration."""

        async def hue_activate_scene(call: core.ServiceCall) -> None:
            """Handle activation of Hue scene."""
            # Get parameters
            group_name = call.data[Const.ATTR_GROUP_NAME]
            scene_name = call.data[Const.ATTR_SCENE_NAME]
            transition = call.data.get(Const.ATTR_TRANSITION)
            dynamic = call.data.get(Const.ATTR_DYNAMIC, False)

            # Call the set scene function on each bridge
            tasks = [
                _hue_activate_scene_v1(bridge, group_name, scene_name, transition)
                if bridge.api_version == 1
                else _hue_activate_scene_v2(
                    bridge, group_name, scene_name, transition, dynamic
                )
                for bridge in self._bridges.values()
                if isinstance(bridge, HueBridge)
            ]
            results = await asyncio.gather(*tasks)

            # Did *any* bridge succeed?
            # Note that we'll get a "True" value for a successful call
            if True not in results:
                _LOGGER.warning(
                    f"No bridge was able to activate scene {scene_name} in group "
                    + f"{group_name}",
                )

        if not self.controller.services.has_service(
            self.domain, Const.SERVICE_HUE_ACTIVATE_SCENE
        ):
            # Register a local handler for scene activation
            self.controller.services.async_register(
                self.domain,
                Const.SERVICE_HUE_ACTIVATE_SCENE,
                core.Service.verify_domain_control(self.controller, self.domain)(
                    hue_activate_scene
                ),
                schema=vol.Schema(
                    {
                        vol.Required(Const.ATTR_GROUP_NAME): _cv.string,
                        vol.Required(Const.ATTR_SCENE_NAME): _cv.string,
                        vol.Optional(Const.ATTR_TRANSITION): _cv.positive_int,
                        vol.Optional(Const.ATTR_DYNAMIC): _cv.boolean,
                    }
                ),
            )

    def create_config_flow(
        self, context: dict, init_data: typing.Any
    ) -> core.ConfigFlow:
        """ConfigFlow Platform implement."""
        return HueFlowHandler(self, context, init_data)

    async def async_get_options_flow(
        self, entry: core.ConfigEntry, context: dict, init_data: typing.Any
    ) -> HueV1OptionsFlowHandler | HueV2OptionsFlowHandler:
        """Get the options flow for this handler."""
        if entry.data.get(Const.CONF_API_VERSION, 1) == 1:
            return HueV1OptionsFlowHandler(entry, context, init_data)
        return HueV2OptionsFlowHandler(self, entry, context, init_data)

    async def async_setup_platform_devices(
        self, entry: core.ConfigEntry, async_add_entities: core.AddEntitiesCallback
    ) -> None:
        """Setup Hue Entities."""
        entity_platform = core.EntityPlatform.async_get_current_platform()
        current_platform = entity_platform.domain
        bridge = self._bridges[entry.entry_id]
        is_v1 = bridge.api_version == 1

        if current_platform == core.Platform.BINARY_SENSOR:
            if is_v1:
                await async_setup_binary_sensors_v1(bridge, async_add_entities)
            else:
                await async_setup_binary_sensors_v2(bridge, entry, async_add_entities)

        elif current_platform == core.Platform.LIGHT:
            if is_v1:
                await async_setup_lights_v1(bridge, entry, async_add_entities)
            else:
                await async_setup_lights_v2(bridge, entry, async_add_entities)
                await async_setup_group_lights(bridge, entry, async_add_entities)

        elif current_platform == core.Platform.SCENE and not is_v1:
            await async_setup_scenes(bridge, entry, async_add_entities)

        elif current_platform == core.Platform.SENSOR:
            if is_v1:
                await async_setup_sensors_v1(bridge, async_add_entities)
            else:
                await async_setup_sensors_v2(bridge, entry, async_add_entities)

        elif current_platform == core.Platform.SWITCH and not is_v1:
            await async_setup_switches(bridge, entry, async_add_entities)

    # ----------------------- Diagnostic Platform ----------------------------

    async def async_get_config_entry_diagnostics(
        self, config_entry: core.ConfigEntry
    ) -> typing.Any:
        bridge = self._bridges[config_entry.entry_id]
        if bridge.api_version == 1:
            # diagnostics is only implemented for V2 bridges.
            return {}
        # Hue diagnostics are already redacted
        return await bridge.api.get_diagnostics()

    # ------------------------- Logbook Platform ------------------------------

    @core.callback
    def async_describe_events(
        self,
        async_describe_event: core.LogbookCallback,
    ) -> None:
        """Describe hue logbook events."""
        async_describe_event(Const.ATTR_HUE_EVENT)

    def async_describe_event(self, event: core.LazyPartialState) -> dict[str, str]:
        """Describe hue logbook event."""
        data = event.data
        name: str = None
        if dev_ent := self.controller.device_registry.async_get(
            data[core.Const.CONF_DEVICE_ID]
        ):
            name = dev_ent.name
        if name is None:
            name = data[core.Const.CONF_ID]
        if core.Const.CONF_TYPE in data:  # v2
            subtype = _TRIGGER_SUBTYPE.get(
                str(data[Const.CONF_SUBTYPE]), _UNKNOWN_SUB_TYPE
            )
            message = _TRIGGER_TYPE.get(
                data[core.Const.CONF_TYPE], _UNKNOWN_TYPE
            ).format(subtype=subtype)
        else:
            message = f"Event {data[core.Const.CONF_EVENT]}"  # v1
        return {
            self.LOGBOOK_ENTRY_NAME: name,
            self.LOGBOOK_ENTRY_MESSAGE: message,
        }

    # -------------------------- Trigger Platform ------------------------------

    async def async_validate_trigger_config(
        self, config: core.ConfigType
    ) -> core.ConfigType:
        """Validate config."""
        if len(self._bridges) == 0:
            # happens at startup
            return config
        device_id = config[core.Const.CONF_DEVICE_ID]
        # lookup device in HASS DeviceRegistry
        dev_reg = self.controller.device_registry
        if (device_entry := dev_reg.async_get(device_id)) is None:
            raise core.InvalidDeviceAutomationConfig(
                f"Device ID {device_id} is not valid"
            )

        for conf_entry_id in device_entry.config_entries:
            if conf_entry_id not in self._bridges:
                continue
            bridge = self._bridges[conf_entry_id]
            if bridge.api_version == 1:
                return await async_validate_trigger_config_v1(device_entry, config)
            return await async_validate_trigger_config_v2(config)
        return config

    async def async_attach_trigger(
        self,
        config: core.ConfigType,
        action: core.TriggerActionType,
        trigger_info: core.TriggerInfo,
    ) -> core.CallbackType:
        """Listen for state changes based on configuration."""
        device_id = config[core.Const.CONF_DEVICE_ID]
        # lookup device in HASS DeviceRegistry
        dev_reg = self.controller.device_registry
        if (device_entry := dev_reg.async_get(device_id)) is None:
            raise core.InvalidDeviceAutomationConfig(
                f"Device ID {device_id} is not valid"
            )

        for conf_entry_id in device_entry.config_entries:
            if conf_entry_id not in self._bridges:
                continue
            bridge = self._bridges[conf_entry_id]
            if bridge.api_version == 1:
                return await async_attach_trigger_v1(
                    self.controller,
                    self._bridges,
                    device_entry,
                    config,
                    action,
                    trigger_info,
                )
            return await async_attach_trigger_v2(bridge, config, action, trigger_info)
        raise core.InvalidDeviceAutomationConfig(
            f"Device ID {device_id} is not found on any Hue bridge"
        )

    async def async_get_triggers(self, device_id: str) -> list[dict[str, str]]:
        """Get device triggers for given (hass) device id."""
        if len(self._bridges) == 0:
            return []
        # lookup device in HASS DeviceRegistry
        dev_reg = self.controller.device_registry
        if (device_entry := dev_reg.async_get(device_id)) is None:
            raise ValueError(f"Device ID {device_id} is not valid")

        # Iterate all config entries for this device
        # and work out the bridge version
        for conf_entry_id in device_entry.config_entries:
            if conf_entry_id not in self._bridges:
                continue
            bridge = self._bridges[conf_entry_id]

            if bridge.api_version == 1:
                return async_get_triggers_v1(bridge, device_entry)
            return async_get_triggers_v2(bridge, device_entry)
        return []
