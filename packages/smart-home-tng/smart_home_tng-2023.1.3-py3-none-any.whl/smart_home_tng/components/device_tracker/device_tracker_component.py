"""
Device Tracker Component for Smart Home - The Next Generation.

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

import voluptuous as vol

from ... import core
from .const import Const

_cv: typing.TypeAlias = core.ConfigValidation

_CONDITION_TYPES: typing.Final = {"is_home", "is_not_home"}
_CONDITION_SCHEMA: typing.Final = _cv.DEVICE_CONDITION_BASE_SCHEMA.extend(
    {
        vol.Required(core.Const.CONF_ENTITY_ID): _cv.entity_id,
        vol.Required(core.Const.CONF_TYPE): vol.In(_CONDITION_TYPES),
    }
)

_TRIGGER_TYPES: typing.Final[set[str]] = {"enters", "leaves"}
_TRIGGER_SCHEMA: typing.Final = _cv.DEVICE_TRIGGER_BASE_SCHEMA.extend(
    {
        vol.Required(core.Const.CONF_ENTITY_ID): _cv.entity_id,
        vol.Required(core.Const.CONF_TYPE): vol.In(_TRIGGER_TYPES),
        vol.Required(core.Const.CONF_ZONE): _cv.entity_domain(
            core.Const.ZONE_COMPONENT_NAME
        ),
    }
)
_EVENT_ZONE_ENTER: typing.Final = "zone.enter"
_EVENT_ZONE_LEAVE: typing.Final = "zone.leave"


# pylint: disable=unused-variable
class DeviceTrackerComponent(
    core.DeviceTrackerComponent,
    core.ConditionPlatform,
    core.TriggerPlatform,
    core.GroupPlatform,
):
    """Provide functionality to keep track of devices."""

    def __init__(self, path: typing.Iterable[str]):
        super().__init__(path)
        self._component: core.EntityComponent = None
        self._registered_macs: dict[str, tuple[str, str]] = None
        self._supported_platforms = frozenset(
            [core.Platform.CONDITION, core.Platform.TIMER, core.Platform.GROUP]
        )
        self._zone: core.ZoneComponent = None

    @property
    def entity_component(self) -> core.EntityComponent:
        return self._component

    def _is_on(self, entity_id: str) -> bool:
        """Return the state if any or a specified device is home."""
        return self._shc.states.is_state(entity_id, core.Const.STATE_HOME)

    async def async_setup(self, config: core.ConfigType) -> bool:
        """Set up the device tracker."""
        # Legacy Device Tracker will not be support in Smart Home - The Next Generation
        # await async_setup_legacy_integration(hass, config)

        return await super().async_setup(config)

    async def async_setup_entry(self, entry: core.ConfigEntry) -> bool:
        """Set up an entry."""
        component = self._component

        if component is not None:
            return await component.async_setup_entry(entry)

        zone = self.get_component(core.Const.ZONE_COMPONENT_NAME)
        if isinstance(zone, core.ZoneComponent):
            self._zone = zone

        component = core.EntityComponent(Const.LOGGER, self.domain, self._shc)
        self._component = component

        # Clean up old devices created by device tracker entities in the past.
        # Can be removed after 2022.6
        ent_reg = self._shc.entity_registry
        dev_reg = self._shc.device_registry

        devices_with_trackers = set()
        devices_with_non_trackers = set()

        for entity in ent_reg.entities.values():
            if entity.device_id is None:
                continue

            if entity.domain == self.domain:
                devices_with_trackers.add(entity.device_id)
            else:
                devices_with_non_trackers.add(entity.device_id)

        for device_id in devices_with_trackers - devices_with_non_trackers:
            for entity in ent_reg.async_entries_for_device(device_id, True):
                ent_reg.async_update_entity(entity.entity_id, device_id=None)
            dev_reg.async_remove_device(device_id)

        return await component.async_setup_entry(entry)

    async def async_unload_entry(self, entry: core.ConfigEntry) -> bool:
        """Unload an entry."""
        return await self._component.async_unload_entry(entry)

    def register_mac(self, domain: str, mac: str, unique_id: str) -> None:
        """Register a mac address with a unique ID."""
        mac = core.helpers.format_mac(mac)
        if self._registered_macs is not None:
            self._registered_macs[mac] = (domain, unique_id)
            return

        # Setup listening.

        # dict mapping mac -> partial unique ID
        self._registered_macs = {mac: (domain, unique_id)}

        self._shc.bus.async_listen(
            core.Const.EVENT_DEVICE_REGISTRY_UPDATED, self._handle_device_event
        )

    @core.callback
    def _handle_device_event(self, event: core.Event) -> None:
        """Enable the online status entity for the mac of a newly created device."""
        # Only for new devices
        if event.data["action"] != "create":
            return

        dev_reg = self._shc.device_registry
        device_entry = dev_reg.async_get(event.data["device_id"])

        if device_entry is None:
            return

        # Check if device has a mac
        mac = None
        for conn in device_entry.connections:
            if conn[0] == core.DeviceRegistry.ConnectionType.MAC:
                mac = conn[1]
                break

        if mac is None:
            return

        # Check if we have an entity for this mac
        if (unique_id := self._registered_macs.get(mac)) is None:
            return

        ent_reg = self._shc.entity_registry

        if (entity_id := ent_reg.async_get_entity_id(self.domain, *unique_id)) is None:
            return

        if (entity_entry := ent_reg.async_get(entity_id)) is None:
            return

        # Make sure entity has a config entry and was disabled by the
        # default disable logic in the integration and new entities
        # are allowed to be added.
        if (
            entity_entry.config_entry_id is None
            or (
                (
                    config_entry := self._shc.config_entries.async_get_entry(
                        entity_entry.config_entry_id
                    )
                )
                is not None
                and config_entry.pref_disable_new_entities
            )
            or entity_entry.disabled_by != core.EntityRegistryEntryDisabler.INTEGRATION
        ):
            return

        # Enable entity
        ent_reg.async_update_entity(entity_id, disabled_by=None)

    def connected_device_registered(
        self, mac: str, ip_address: str, hostname: str
    ) -> None:
        """Register a newly seen connected device.

        This is currently used by the dhcp integration
        to listen for newly registered connected devices
        for discovery.
        """
        self._shc.dispatcher.async_send(
            core.DeviceTracker.CONNECTED_DEVICE_REGISTERED,
            {
                core.Const.ATTR_IP: ip_address,
                core.Const.ATTR_MAC: mac,
                core.Const.ATTR_HOST_NAME: hostname,
            },
        )

    async def async_get_conditions(
        self, device_id: str
    ) -> list[dict[str, typing.Any]] | typing.Awaitable[list[dict[str, typing.Any]]]:
        """List device conditions for Device tracker devices."""
        registry = self._shc.entity_registry
        conditions = []

        # Get all the integrations entities for this device
        for entry in registry.async_entries_for_device(device_id):
            if entry.domain != self.domain:
                continue

            # Add conditions for each entity that belongs to this integration
            base_condition = {
                core.Const.CONF_CONDITION: "device",
                core.Const.CONF_DEVICE_ID: device_id,
                core.Const.CONF_DOMAIN: self.domain,
                core.Const.CONF_ENTITY_ID: entry.entity_id,
            }

            conditions += [
                {**base_condition, core.Const.CONF_TYPE: cond}
                for cond in _CONDITION_TYPES
            ]

        return conditions

    async def async_condition_from_config(
        self, config: core.ConfigType
    ) -> core.ConditionCheckerType:
        """Create a function to test a device condition."""
        reverse = config[core.Const.CONF_TYPE] == "is_not_home"
        platform = core.ScriptCondition.get_action_condition_protocol(self._shc)

        @core.callback
        def test_is_state(
            _shc: core.SmartHomeController, _variables: core.TemplateVarsType
        ) -> bool:
            """Test if an entity is a certain state."""
            result = platform.state(
                config[core.Const.ATTR_ENTITY_ID], core.Const.STATE_HOME
            )
            if reverse:
                result = not result
            return result

        return test_is_state

    async def async_validate_condition_config(
        self, config: core.ConfigType
    ) -> core.ConfigType:
        return _CONDITION_SCHEMA(config)

    async def async_validate_trigger_config(
        self, config: core.ConfigType
    ) -> core.ConfigType:
        return _TRIGGER_SCHEMA(config)

    async def async_get_triggers(self, device_id: str) -> list[dict[str, str]]:
        """List device triggers for Device Tracker devices."""
        registry = self._shc.entity_registry
        triggers = []

        # Get all the integrations entities for this device
        for entry in registry.async_entries_for_device(device_id):
            if entry.domain != self.domain:
                continue

            triggers.append(
                {
                    core.Const.CONF_PLATFORM: "device",
                    core.Const.CONF_DEVICE_ID: device_id,
                    core.Const.CONF_DOMAIN: self.domain,
                    core.Const.CONF_ENTITY_ID: entry.entity_id,
                    core.Const.CONF_TYPE: "enters",
                }
            )
            triggers.append(
                {
                    core.Const.CONF_PLATFORM: "device",
                    core.Const.CONF_DEVICE_ID: device_id,
                    core.Const.CONF_DOMAIN: self.domain,
                    core.Const.CONF_ENTITY_ID: entry.entity_id,
                    core.Const.CONF_TYPE: "leaves",
                }
            )

        return triggers

    async def async_attach_trigger(
        self,
        config: core.ConfigType,
        action: core.TriggerActionType,
        trigger_info: core.TriggerInfo,
    ) -> core.CallbackType:
        """Attach a trigger."""
        if config[core.Const.CONF_TYPE] == "enters":
            event = _EVENT_ZONE_ENTER
        else:
            event = _EVENT_ZONE_LEAVE

        zone_config = {
            core.Const.CONF_PLATFORM: "zone",
            core.Const.CONF_ENTITY_ID: config[core.Const.CONF_ENTITY_ID],
            core.Const.CONF_ZONE: config[core.Const.CONF_ZONE],
            core.Const.CONF_EVENT: event,
        }
        zone_config = await core.Trigger.async_validate_trigger_config(config)
        return await core.Zone.async_attach_trigger(
            self.controller, zone_config, action, trigger_info, platform_type="device"
        )

    async def async_get_trigger_capabilities(
        self, _config: core.ConfigType
    ) -> dict[str, vol.Schema]:
        """List trigger capabilities."""
        zones = {
            ent.entity_id: ent.name
            for ent in sorted(
                self._shc.states.async_all(core.Const.ZONE_COMPONENT_NAME),
                key=lambda ent: ent.name,
            )
        }
        return {
            "extra_fields": vol.Schema(
                {
                    vol.Required(core.Const.CONF_ZONE): vol.In(zones),
                }
            )
        }

    def async_describe_on_off_states(
        self, registry: core.GroupIntegrationRegistry
    ) -> None:
        """Describe group on off states."""
        registry.on_off_states({core.Const.STATE_HOME}, core.Const.STATE_NOT_HOME)
