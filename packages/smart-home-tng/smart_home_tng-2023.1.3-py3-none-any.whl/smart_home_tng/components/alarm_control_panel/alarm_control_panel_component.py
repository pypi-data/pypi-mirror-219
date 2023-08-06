"""
Alarm Control Panel Component for Smart Home - The Next Generation.

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
import datetime as dt
import logging
import typing

import voluptuous as vol

from ... import core
from .const import Const

_cv: typing.TypeAlias = core.ConfigValidation
_LOGGER: typing.Final = logging.getLogger(__name__)

_ALARM_SERVICE_SCHEMA: typing.Final = _cv.make_entity_service_schema(
    {vol.Optional(core.Const.ATTR_CODE): _cv.string}
)
_ACTION_TYPES: typing.Final[set[str]] = {
    "arm_away",
    "arm_home",
    "arm_night",
    "arm_vacation",
    "disarm",
    "trigger",
}
_CONDITION_TYPES: typing.Final[set[str]] = {
    Const.CONDITION_TRIGGERED,
    Const.CONDITION_DISARMED,
    Const.CONDITION_ARMED_HOME,
    Const.CONDITION_ARMED_AWAY,
    Const.CONDITION_ARMED_NIGHT,
    Const.CONDITION_ARMED_VACATION,
    Const.CONDITION_ARMED_CUSTOM_BYPASS,
}

_CONDITION_SCHEMA: typing.Final = _cv.DEVICE_CONDITION_BASE_SCHEMA.extend(
    {
        vol.Required(core.Const.CONF_ENTITY_ID): _cv.entity_id,
        vol.Required(core.Const.CONF_TYPE): vol.In(_CONDITION_TYPES),
    }
)
_VALID_STATES: typing.Final[set[str]] = {
    core.Const.STATE_ALARM_ARMED_AWAY,
    core.Const.STATE_ALARM_ARMED_CUSTOM_BYPASS,
    core.Const.STATE_ALARM_ARMED_HOME,
    core.Const.STATE_ALARM_ARMED_NIGHT,
    core.Const.STATE_ALARM_ARMED_VACATION,
    core.Const.STATE_ALARM_DISARMED,
    core.Const.STATE_ALARM_TRIGGERED,
}
_BASIC_TRIGGER_TYPES: typing.Final[set[str]] = {"triggered", "disarmed", "arming"}
_TRIGGER_TYPES: typing.Final[set[str]] = _BASIC_TRIGGER_TYPES | {
    "armed_home",
    "armed_away",
    "armed_night",
    "armed_vacation",
}

_TRIGGER_SCHEMA: typing.Final = _cv.DEVICE_TRIGGER_BASE_SCHEMA.extend(
    {
        vol.Required(core.Const.CONF_ENTITY_ID): _cv.entity_id,
        vol.Required(core.Const.CONF_TYPE): vol.In(_TRIGGER_TYPES),
        vol.Optional(core.Const.CONF_FOR): _cv.positive_time_period_dict,
    }
)


# pylint: disable=unused-variable
class AlarmControlPanelComponent(
    core.SmartHomeControllerComponent,
    core.ActionPlatform,
    core.ConditionPlatform,
    core.GroupPlatform,
    core.ReproduceStatePlatform,
    core.TriggerPlatform,
):
    """Component to interface with an alarm control panel."""

    def __init__(self, path: typing.Iterable[str]):
        super().__init__(path)
        self._entity_component: core.EntityComponent = None
        self._supported_platforms = frozenset(
            [
                core.Platform.ACTION,
                core.Platform.CONDITION,
                core.Platform.GROUP,
                core.Platform.REPRODUCE_STATE,
                core.Platform.TRIGGER,
            ]
        )

    @property
    def condition_schema(self) -> typing.Callable[[core.ConfigType], core.ConfigType]:
        return _CONDITION_SCHEMA

    @property
    def entity_component(self) -> core.EntityComponent:
        return self._entity_component

    @property
    def scan_interval(self) -> dt.timedelta:
        return dt.timedelta(seconds=30)

    async def async_setup(self, config: core.ConfigType) -> bool:
        """Track states and offer events for sensors."""
        if not await super().async_setup(config):
            return False

        component = self._entity_component = core.EntityComponent(
            _LOGGER, self.domain, self.controller, self.scan_interval
        )

        await component.async_setup(config)

        component.async_register_entity_service(
            core.Const.SERVICE_ALARM_DISARM, _ALARM_SERVICE_SCHEMA, "async_alarm_disarm"
        )
        component.async_register_entity_service(
            core.Const.SERVICE_ALARM_ARM_HOME,
            _ALARM_SERVICE_SCHEMA,
            "async_alarm_arm_home",
            [core.AlarmControlPanel.EntityFeature.ARM_HOME],
        )
        component.async_register_entity_service(
            core.Const.SERVICE_ALARM_ARM_AWAY,
            _ALARM_SERVICE_SCHEMA,
            "async_alarm_arm_away",
            [core.AlarmControlPanel.EntityFeature.ARM_AWAY],
        )
        component.async_register_entity_service(
            core.Const.SERVICE_ALARM_ARM_NIGHT,
            _ALARM_SERVICE_SCHEMA,
            "async_alarm_arm_night",
            [core.AlarmControlPanel.EntityFeature.ARM_NIGHT],
        )
        component.async_register_entity_service(
            core.Const.SERVICE_ALARM_ARM_VACATION,
            _ALARM_SERVICE_SCHEMA,
            "async_alarm_arm_vacation",
            [core.AlarmControlPanel.EntityFeature.ARM_VACATION],
        )
        component.async_register_entity_service(
            core.Const.SERVICE_ALARM_ARM_CUSTOM_BYPASS,
            _ALARM_SERVICE_SCHEMA,
            "async_alarm_arm_custom_bypass",
            [core.AlarmControlPanel.EntityFeature.ARM_CUSTOM_BYPASS],
        )
        component.async_register_entity_service(
            core.Const.SERVICE_ALARM_TRIGGER,
            _ALARM_SERVICE_SCHEMA,
            "async_alarm_trigger",
            [core.AlarmControlPanel.EntityFeature.TRIGGER],
        )
        return True

    async def async_setup_entry(self, entry: core.ConfigEntry) -> bool:
        """Set up a config entry."""
        return await self._entity_component.async_setup_entry(entry)

    async def async_unload_entry(self, entry: core.ConfigEntry) -> bool:
        """Unload a config entry."""
        return await self._entity_component.async_unload_entry(entry)

    # ------------------- Action Platform -------------------------------------

    async def async_validate_action_config(
        self, config: core.ConfigType
    ) -> core.ConfigType:
        """Validate Action configuration."""
        _ACTION_SCHEMA: typing.Final = _cv.DEVICE_ACTION_BASE_SCHEMA.extend(
            {
                vol.Required(core.Const.CONF_TYPE): vol.In(_ACTION_TYPES),
                vol.Required(core.Const.CONF_ENTITY_ID): _cv.entity_domain(self.domain),
                vol.Optional(core.Const.CONF_CODE): _cv.string,
            }
        )
        return _ACTION_SCHEMA(config)

    async def async_get_actions(self, device_id: str) -> list[dict[str, str]]:
        """List device actions for Alarm control panel devices."""
        registry = self.controller.entity_registry
        actions = []

        # Get all the integrations entities for this device
        for entry in registry.async_entries_for_device(device_id):
            if entry.domain != self.domain:
                continue

            supported_features = registry.get_supported_features(entry.entity_id)

            base_action: dict = {
                core.Const.CONF_DEVICE_ID: device_id,
                core.Const.CONF_DOMAIN: self.domain,
                core.Const.CONF_ENTITY_ID: entry.entity_id,
            }

            # Add actions for each entity that belongs to this integration
            if supported_features & core.AlarmControlPanel.EntityFeature.ARM_AWAY:
                actions.append({**base_action, core.Const.CONF_TYPE: "arm_away"})
            if supported_features & core.AlarmControlPanel.EntityFeature.ARM_HOME:
                actions.append({**base_action, core.Const.CONF_TYPE: "arm_home"})
            if supported_features & core.AlarmControlPanel.EntityFeature.ARM_NIGHT:
                actions.append({**base_action, core.Const.CONF_TYPE: "arm_night"})
            if supported_features & core.AlarmControlPanel.EntityFeature.ARM_VACATION:
                actions.append({**base_action, core.Const.CONF_TYPE: "arm_vacation"})
            actions.append({**base_action, core.Const.CONF_TYPE: "disarm"})
            if supported_features & core.AlarmControlPanel.EntityFeature.TRIGGER:
                actions.append({**base_action, core.Const.CONF_TYPE: "trigger"})
        return actions

    async def async_call_action_from_config(
        self,
        config: core.ConfigType,
        _variables: dict[str, typing.Any],
        context: core.Context,
    ) -> None:
        """Execute a device action."""
        service_data = {core.Const.ATTR_ENTITY_ID: config[core.Const.CONF_ENTITY_ID]}
        if core.Const.CONF_CODE in config:
            service_data[core.Const.ATTR_CODE] = config[core.Const.CONF_CODE]

        cond_type = config[core.Const.CONF_TYPE]
        if cond_type == "arm_away":
            service = core.Const.SERVICE_ALARM_ARM_AWAY
        elif cond_type == "arm_home":
            service = core.Const.SERVICE_ALARM_ARM_HOME
        elif cond_type == "arm_night":
            service = core.Const.SERVICE_ALARM_ARM_NIGHT
        elif cond_type == "arm_vacation":
            service = core.Const.SERVICE_ALARM_ARM_VACATION
        elif cond_type == "disarm":
            service = core.Const.SERVICE_ALARM_DISARM
        elif cond_type == "trigger":
            service = core.Const.SERVICE_ALARM_TRIGGER

        await self.controller.services.async_call(
            self.domain, service, service_data, blocking=True, context=context
        )

    async def async_get_action_capabilities(
        self, config: core.ConfigType
    ) -> dict[str, vol.Schema]:
        """List action capabilities."""
        # We need to refer to the state directly because ATTR_CODE_ARM_REQUIRED is not a
        # capability attribute
        state = self.controller.states.get(config[core.Const.CONF_ENTITY_ID])
        code_required = (
            state.attributes.get(core.Const.ATTR_CODE_ARM_REQUIRED) if state else False
        )

        cond_type = config[core.Const.CONF_TYPE]
        if cond_type == "trigger" or (cond_type != "disarm" and not code_required):
            return {}

        return {"extra_fields": vol.Schema({vol.Optional(core.Const.CONF_CODE): str})}

    # ------------------------ Condition Platform -----------------------------

    async def async_get_conditions(
        self, device_id: str
    ) -> list[dict[str, typing.Any]] | typing.Awaitable[list[dict[str, typing.Any]]]:
        """List device conditions for Alarm control panel devices."""
        registry = self.controller.entity_registry
        conditions = []

        # Get all the integrations entities for this device
        for entry in registry.async_entries_for_device(device_id):
            if entry.domain != self.domain:
                continue

            supported_features = registry.get_supported_features(entry.entity_id)

            # Add conditions for each entity that belongs to this integration
            base_condition = {
                core.Const.CONF_CONDITION: "device",
                core.Const.CONF_DEVICE_ID: device_id,
                core.Const.CONF_DOMAIN: self.domain,
                core.Const.CONF_ENTITY_ID: entry.entity_id,
            }

            conditions += [
                {**base_condition, core.Const.CONF_TYPE: Const.CONDITION_DISARMED},
                {**base_condition, core.Const.CONF_TYPE: Const.CONDITION_TRIGGERED},
            ]
            if supported_features & core.AlarmControlPanel.EntityFeature.ARM_HOME:
                conditions.append(
                    {**base_condition, core.Const.CONF_TYPE: Const.CONDITION_ARMED_HOME}
                )
            if supported_features & core.AlarmControlPanel.EntityFeature.ARM_AWAY:
                conditions.append(
                    {**base_condition, core.Const.CONF_TYPE: Const.CONDITION_ARMED_AWAY}
                )
            if supported_features & core.AlarmControlPanel.EntityFeature.ARM_NIGHT:
                conditions.append(
                    {
                        **base_condition,
                        core.Const.CONF_TYPE: Const.CONDITION_ARMED_NIGHT,
                    }
                )
            if supported_features & core.AlarmControlPanel.EntityFeature.ARM_VACATION:
                conditions.append(
                    {
                        **base_condition,
                        core.Const.CONF_TYPE: Const.CONDITION_ARMED_VACATION,
                    }
                )
            if (
                supported_features
                & core.AlarmControlPanel.EntityFeature.ARM_CUSTOM_BYPASS
            ):
                conditions.append(
                    {
                        **base_condition,
                        core.Const.CONF_TYPE: Const.CONDITION_ARMED_CUSTOM_BYPASS,
                    }
                )

        return conditions

    async def async_condition_from_config(
        self, config: core.ConfigType
    ) -> core.ConditionCheckerType:
        """Create a function to test a device condition."""
        default_impl = core.ScriptCondition.get_action_condition_protocol(
            self.controller
        )

        cond_type = config[core.Const.CONF_TYPE]
        if cond_type == Const.CONDITION_TRIGGERED:
            state = core.Const.STATE_ALARM_TRIGGERED
        elif cond_type == Const.CONDITION_DISARMED:
            state = core.Const.STATE_ALARM_DISARMED
        elif cond_type == Const.CONDITION_ARMED_HOME:
            state = core.Const.STATE_ALARM_ARMED_HOME
        elif cond_type == Const.CONDITION_ARMED_AWAY:
            state = core.Const.STATE_ALARM_ARMED_AWAY
        elif cond_type == Const.CONDITION_ARMED_NIGHT:
            state = core.Const.STATE_ALARM_ARMED_NIGHT
        elif cond_type == Const.CONDITION_ARMED_VACATION:
            state = core.Const.STATE_ALARM_ARMED_VACATION
        elif cond_type == Const.CONDITION_ARMED_CUSTOM_BYPASS:
            state = core.Const.STATE_ALARM_ARMED_CUSTOM_BYPASS

        def test_is_state(_shc, _variables: core.TemplateVarsType) -> bool:
            """Test if an entity is a certain state."""
            return default_impl.state(config[core.Const.ATTR_ENTITY_ID], state)

        return test_is_state

    # -------------------- Group Platform ---------------------------

    @core.callback
    def async_describe_on_off_states(
        self, registry: core.GroupIntegrationRegistry
    ) -> None:
        """Describe group on off states."""
        registry.on_off_states(
            {
                core.Const.STATE_ALARM_ARMED_AWAY,
                core.Const.STATE_ALARM_ARMED_CUSTOM_BYPASS,
                core.Const.STATE_ALARM_ARMED_HOME,
                core.Const.STATE_ALARM_ARMED_NIGHT,
                core.Const.STATE_ALARM_ARMED_VACATION,
                core.Const.STATE_ALARM_TRIGGERED,
            },
            core.Const.STATE_OFF,
        )

    # -------------------- Reproduce State Platform ---------------------

    async def async_reproduce_states(
        self,
        states: list[core.State],
        *,
        context: core.Context = None,
        reproduce_options: dict[str, typing.Any] = None,
    ):
        """Reproduce Alarm control panel states."""
        await asyncio.gather(
            *(
                _async_reproduce_state(
                    self.controller, state, self.domain, context=context
                )
                for state in states
            )
        )

    # ---------------------- Trigger Platform -------------------------------

    async def async_validate_trigger_config(
        self, config: core.ConfigType
    ) -> core.ConfigType:
        return _TRIGGER_SCHEMA(config)

    async def async_get_triggers(self, device_id: str) -> list[dict[str, str]]:
        """List device triggers for Alarm control panel devices."""
        registry = self.controller.entity_registry
        triggers: list[dict[str, str]] = []

        # Get all the integrations entities for this device
        for entry in registry.async_entries_for_device(device_id):
            if entry.domain != self.domain:
                continue

            supported_features = registry.get_supported_features(entry.entity_id)

            # Add triggers for each entity that belongs to this integration
            base_trigger = {
                core.Const.CONF_PLATFORM: "device",
                core.Const.CONF_DEVICE_ID: device_id,
                core.Const.CONF_DOMAIN: self.domain,
                core.Const.CONF_ENTITY_ID: entry.entity_id,
            }

            triggers += [
                {
                    **base_trigger,
                    core.Const.CONF_TYPE: trigger,
                }
                for trigger in _BASIC_TRIGGER_TYPES
            ]
            if supported_features & core.AlarmControlPanel.EntityFeature.ARM_HOME:
                triggers.append(
                    {
                        **base_trigger,
                        core.Const.CONF_TYPE: "armed_home",
                    }
                )
            if supported_features & core.AlarmControlPanel.EntityFeature.ARM_AWAY:
                triggers.append(
                    {
                        **base_trigger,
                        core.Const.CONF_TYPE: "armed_away",
                    }
                )
            if supported_features & core.AlarmControlPanel.EntityFeature.ARM_NIGHT:
                triggers.append(
                    {
                        **base_trigger,
                        core.Const.CONF_TYPE: "armed_night",
                    }
                )
            if supported_features & core.AlarmControlPanel.EntityFeature.ARM_VACATION:
                triggers.append(
                    {
                        **base_trigger,
                        core.Const.CONF_TYPE: "armed_vacation",
                    }
                )
        return triggers

    async def async_get_trigger_capabilities(
        self, _config: core.ConfigType
    ) -> dict[str, vol.Schema] | typing.Awaitable[dict[str, vol.Schema]]:
        """List trigger capabilities."""
        return {
            "extra_fields": vol.Schema(
                {vol.Optional(core.Const.CONF_FOR): _cv.positive_time_period_dict}
            )
        }

    async def async_attach_trigger(
        self,
        config: core.ConfigType,
        action: core.TriggerActionType,
        trigger_info: core.TriggerInfo,
    ) -> core.CallbackType:
        """Attach a trigger."""
        tr_type = config[core.Const.CONF_TYPE]
        if tr_type == "triggered":
            to_state = core.Const.STATE_ALARM_TRIGGERED
        elif tr_type == "disarmed":
            to_state = core.Const.STATE_ALARM_DISARMED
        elif tr_type == "arming":
            to_state = core.Const.STATE_ALARM_ARMING
        elif tr_type == "armed_home":
            to_state = core.Const.STATE_ALARM_ARMED_HOME
        elif tr_type == "armed_away":
            to_state = core.Const.STATE_ALARM_ARMED_AWAY
        elif tr_type == "armed_night":
            to_state = core.Const.STATE_ALARM_ARMED_NIGHT
        elif tr_type == "armed_vacation":
            to_state = core.Const.STATE_ALARM_ARMED_VACATION

        state_config = {
            core.Const.CONF_PLATFORM: "state",
            core.Const.CONF_ENTITY_ID: config[core.Const.CONF_ENTITY_ID],
            core.Const.CONF_TO: to_state,
        }
        if core.Const.CONF_FOR in config:
            state_config[core.Const.CONF_FOR] = config[core.Const.CONF_FOR]

        state_config = await core.Trigger.async_validate_trigger_config(state_config)
        return await core.Trigger.async_attach_state_trigger(
            self.controller, state_config, action, trigger_info, platform_type="device"
        )


async def _async_reproduce_state(
    shc: core.SmartHomeController,
    state: core.State,
    domain: str,
    *,
    context: core.Context = None,
) -> None:
    """Reproduce a single state."""
    if (cur_state := shc.states.get(state.entity_id)) is None:
        _LOGGER.warning(f"Unable to find entity {state.entity_id}")
        return

    if state.state not in _VALID_STATES:
        _LOGGER.warning(f"Invalid state specified for {state.entity_id}: {state.state}")
        return

    # Return if we are already at the right state.
    if cur_state.state == state.state:
        return

    service_data = {core.Const.ATTR_ENTITY_ID: state.entity_id}

    if state.state == core.Const.STATE_ALARM_ARMED_AWAY:
        service = core.Const.SERVICE_ALARM_ARM_AWAY
    elif state.state == core.Const.STATE_ALARM_ARMED_CUSTOM_BYPASS:
        service = core.Const.SERVICE_ALARM_ARM_CUSTOM_BYPASS
    elif state.state == core.Const.STATE_ALARM_ARMED_HOME:
        service = core.Const.SERVICE_ALARM_ARM_HOME
    elif state.state == core.Const.STATE_ALARM_ARMED_NIGHT:
        service = core.Const.SERVICE_ALARM_ARM_NIGHT
    elif state.state == core.Const.STATE_ALARM_ARMED_VACATION:
        service = core.Const.SERVICE_ALARM_ARM_VACATION
    elif state.state == core.Const.STATE_ALARM_DISARMED:
        service = core.Const.SERVICE_ALARM_DISARM
    elif state.state == core.Const.STATE_ALARM_TRIGGERED:
        service = core.Const.SERVICE_ALARM_TRIGGER

    await shc.services.async_call(
        domain, service, service_data, context=context, blocking=True
    )
