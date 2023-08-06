"""
Climate Component for Smart Home - The Next Generation.

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

_cv: typing.TypeAlias = core.ConfigValidation
_LOGGER: typing.Final = logging.getLogger(__name__)

_SET_TEMPERATURE_SCHEMA: typing.Final = vol.All(
    _cv.has_at_least_one_key(
        core.Const.ATTR_TEMPERATURE,
        core.Climate.ATTR_TARGET_TEMP_HIGH,
        core.Climate.ATTR_TARGET_TEMP_LOW,
    ),
    _cv.make_entity_service_schema(
        {
            vol.Exclusive(core.Const.ATTR_TEMPERATURE, "temperature"): vol.Coerce(
                float
            ),
            vol.Inclusive(
                core.Climate.ATTR_TARGET_TEMP_HIGH, "temperature"
            ): vol.Coerce(float),
            vol.Inclusive(core.Climate.ATTR_TARGET_TEMP_LOW, "temperature"): vol.Coerce(
                float
            ),
            vol.Optional(core.Climate.ATTR_HVAC_MODE): vol.Coerce(
                core.Climate.HVACMode
            ),
        }
    ),
)

_HVAC_MODE_CONDITION = _cv.DEVICE_CONDITION_BASE_SCHEMA.extend(
    {
        vol.Required(core.Const.CONF_ENTITY_ID): _cv.entity_id,
        vol.Required(core.Const.CONF_TYPE): "is_hvac_mode",
        vol.Required(core.Climate.ATTR_HVAC_MODE): vol.In(core.Climate.HVAC_MODES),
    }
)

_PRESET_MODE_CONDITION: typing.Final = _cv.DEVICE_CONDITION_BASE_SCHEMA.extend(
    {
        vol.Required(core.Const.CONF_ENTITY_ID): _cv.entity_id,
        vol.Required(core.Const.CONF_TYPE): "is_preset_mode",
        vol.Required(core.Climate.ATTR_PRESET_MODE): str,
    }
)
_CONDITION_SCHEMA: typing.Final = vol.Any(_HVAC_MODE_CONDITION, _PRESET_MODE_CONDITION)

_HVAC_MODE_TRIGGER_SCHEMA: typing.Final = _cv.DEVICE_TRIGGER_BASE_SCHEMA.extend(
    {
        vol.Required(core.Const.CONF_ENTITY_ID): _cv.entity_id,
        vol.Required(core.Const.CONF_TYPE): "hvac_mode_changed",
        vol.Required(core.Const.CONF_TO): vol.In(core.Climate.HVAC_MODES),
    }
)

_CURRENT_TRIGGER_SCHEMA: typing.Final = vol.All(
    _cv.DEVICE_TRIGGER_BASE_SCHEMA.extend(
        {
            vol.Required(core.Const.CONF_ENTITY_ID): _cv.entity_id,
            vol.Required(core.Const.CONF_TYPE): vol.In(
                ["current_temperature_changed", "current_humidity_changed"]
            ),
            vol.Optional(core.Const.CONF_BELOW): vol.Any(vol.Coerce(float)),
            vol.Optional(core.Const.CONF_ABOVE): vol.Any(vol.Coerce(float)),
            vol.Optional(core.Const.CONF_FOR): _cv.positive_time_period_dict,
        }
    ),
    _cv.has_at_least_one_key(core.Const.CONF_BELOW, core.Const.CONF_ABOVE),
)

_TRIGGER_SCHEMA: typing.Final = vol.Any(
    _HVAC_MODE_TRIGGER_SCHEMA, _CURRENT_TRIGGER_SCHEMA
)


# pylint: disable=unused-variable, too-many-ancestors
class ClimateComponent(
    core.SmartHomeControllerComponent,
    core.ActionPlatform,
    core.ConditionPlatform,
    core.GroupPlatform,
    core.RecorderPlatform,
    core.ReproduceStatePlatform,
    core.TriggerPlatform,
):
    """Provides functionality to interact with climate devices."""

    def __init__(self, path: typing.Iterable[str]):
        super().__init__(path)
        self._entity_component: core.EntityComponent = None
        self._supported_platforms = frozenset(
            [
                core.Platform.ACTION,
                core.Platform.CONDITION,
                core.Platform.GROUP,
                core.Platform.RECORDER,
                core.Platform.REPRODUCE_STATE,
                core.Platform.TRIGGER,
            ]
        )

    @property
    def entity_component(self) -> core.EntityComponent:
        return self._entity_component

    @property
    def scan_interval(self) -> dt.timedelta:
        return dt.timedelta(seconds=60)

    async def async_setup(self, config: core.ConfigType) -> bool:
        """Set up climate entities."""
        if not await super().async_setup(config):
            return False
        component = self._entity_component = core.EntityComponent(
            _LOGGER, self.domain, self.controller, self.scan_interval
        )
        await component.async_setup(config)

        component.async_register_entity_service(
            core.Const.SERVICE_TURN_ON, {}, "async_turn_on"
        )
        component.async_register_entity_service(
            core.Const.SERVICE_TURN_OFF, {}, "async_turn_off"
        )
        component.async_register_entity_service(
            core.Climate.SERVICE_SET_HVAC_MODE,
            {
                vol.Required(core.Climate.ATTR_HVAC_MODE): vol.Coerce(
                    core.Climate.HVACMode
                )
            },
            "async_set_hvac_mode",
        )
        component.async_register_entity_service(
            core.Climate.SERVICE_SET_PRESET_MODE,
            {vol.Required(core.Climate.ATTR_PRESET_MODE): _cv.string},
            "async_set_preset_mode",
            [core.Climate.EntityFeature.PRESET_MODE],
        )
        component.async_register_entity_service(
            core.Climate.SERVICE_SET_AUX_HEAT,
            {vol.Required(core.Climate.ATTR_AUX_HEAT): _cv.boolean},
            core.Climate.async_service_aux_heat,
            [core.Climate.EntityFeature.AUX_HEAT],
        )
        component.async_register_entity_service(
            core.Climate.SERVICE_SET_TEMPERATURE,
            _SET_TEMPERATURE_SCHEMA,
            core.Climate.async_service_temperature_set,
            [
                core.Climate.EntityFeature.TARGET_TEMPERATURE,
                core.Climate.EntityFeature.TARGET_TEMPERATURE_RANGE,
            ],
        )
        component.async_register_entity_service(
            core.Climate.SERVICE_SET_HUMIDITY,
            {vol.Required(core.Climate.ATTR_HUMIDITY): vol.Coerce(int)},
            "async_set_humidity",
            [core.Climate.EntityFeature.TARGET_HUMIDITY],
        )
        component.async_register_entity_service(
            core.Climate.SERVICE_SET_FAN_MODE,
            {vol.Required(core.Climate.ATTR_FAN_MODE): _cv.string},
            "async_set_fan_mode",
            [core.Climate.EntityFeature.FAN_MODE],
        )
        component.async_register_entity_service(
            core.Climate.SERVICE_SET_SWING_MODE,
            {vol.Required(core.Climate.ATTR_SWING_MODE): _cv.string},
            "async_set_swing_mode",
            [core.Climate.EntityFeature.SWING_MODE],
        )

        return True

    async def async_setup_entry(self, entry: core.ConfigEntry) -> bool:
        """Set up a config entry."""
        component = self.entity_component
        return await component.async_setup_entry(entry)

    async def async_unload_entry(self, entry: core.ConfigEntry) -> bool:
        """Unload a config entry."""
        component = self.entity_component
        return await component.async_unload_entry(entry)

    # ----------------- Action Platform ------------------------------

    @property
    def action_schema(self) -> typing.Callable[[core.ConfigType], core.ConfigType]:
        """Validate action configuration."""
        _SET_HVAC_MODE_SCHEMA: typing.Final = _cv.DEVICE_ACTION_BASE_SCHEMA.extend(
            {
                vol.Required(core.Const.CONF_TYPE): "set_hvac_mode",
                vol.Required(core.Const.CONF_ENTITY_ID): _cv.entity_domain(self.domain),
                vol.Required(core.Climate.ATTR_HVAC_MODE): vol.In(
                    core.Climate.HVAC_MODES
                ),
            }
        )

        _SET_PRESET_MODE_SCHEMA: typing.Final = _cv.DEVICE_ACTION_BASE_SCHEMA.extend(
            {
                vol.Required(core.Const.CONF_TYPE): "set_preset_mode",
                vol.Required(core.Const.CONF_ENTITY_ID): _cv.entity_domain(self.domain),
                vol.Required(core.Climate.ATTR_PRESET_MODE): str,
            }
        )

        return vol.Any(_SET_HVAC_MODE_SCHEMA, _SET_PRESET_MODE_SCHEMA)

    async def async_get_actions(self, device_id: str) -> list[dict[str, str]]:
        """List device actions for Climate devices."""
        registry = self.controller.entity_registry
        actions = []

        # Get all the integrations entities for this device
        for entry in registry.async_entries_for_device(device_id):
            if entry.domain != self.domain:
                continue

            supported_features = registry.get_supported_features(entry.entity_id)

            base_action = {
                core.Const.CONF_DEVICE_ID: device_id,
                core.Const.CONF_DOMAIN: self.domain,
                core.Const.CONF_ENTITY_ID: entry.entity_id,
            }

            actions.append({**base_action, core.Const.CONF_TYPE: "set_hvac_mode"})
            if supported_features & core.Climate.EntityFeature.PRESET_MODE:
                actions.append({**base_action, core.Const.CONF_TYPE: "set_preset_mode"})

        return actions

    async def async_call_action_from_config(
        self,
        config: core.ConfigType,
        _variables: dict[str, typing.Any],
        context: core.Context,
    ) -> None:
        """Execute a device action."""
        service_data = {core.Const.ATTR_ENTITY_ID: config[core.Const.CONF_ENTITY_ID]}

        if config[core.Const.CONF_TYPE] == "set_hvac_mode":
            service = core.Climate.SERVICE_SET_HVAC_MODE
            service_data[core.Climate.ATTR_HVAC_MODE] = config[
                core.Climate.ATTR_HVAC_MODE
            ]
        elif config[core.Const.CONF_TYPE] == "set_preset_mode":
            service = core.Climate.SERVICE_SET_PRESET_MODE
            service_data[core.Climate.ATTR_PRESET_MODE] = config[
                core.Climate.ATTR_PRESET_MODE
            ]

        await self.controller.services.async_call(
            self.domain, service, service_data, blocking=True, context=context
        )

    async def async_get_action_capabilities(
        self, config: core.ConfigType
    ) -> dict[str, vol.Schema]:
        """List action capabilities."""
        action_type = config[core.Const.CONF_TYPE]
        entity_registry = self.controller.entity_registry

        fields = {}

        if action_type == "set_hvac_mode":
            try:
                hvac_modes = (
                    entity_registry.get_capability(
                        config[core.Const.ATTR_ENTITY_ID], core.Climate.ATTR_HVAC_MODES
                    )
                    or []
                )
            except core.SmartHomeControllerError:
                hvac_modes = []
            fields[vol.Required(core.Climate.ATTR_HVAC_MODE)] = vol.In(hvac_modes)
        elif action_type == "set_preset_mode":
            try:
                preset_modes = (
                    entity_registry.get_capability(
                        config[core.Const.ATTR_ENTITY_ID],
                        core.Climate.ATTR_PRESET_MODES,
                    )
                    or []
                )
            except core.SmartHomeControllerError:
                preset_modes = []
            fields[vol.Required(core.Climate.ATTR_PRESET_MODE)] = vol.In(preset_modes)

        return {"extra_fields": vol.Schema(fields)}

    # ----------------- Condition Platform ------------------------------

    @property
    def condition_schema(self) -> typing.Callable[[core.ConfigType], core.ConfigType]:
        return _CONDITION_SCHEMA

    async def async_get_conditions(
        self, device_id: str
    ) -> list[dict[str, typing.Any]] | typing.Awaitable[list[dict[str, typing.Any]]]:
        """List device conditions for Climate devices."""
        registry = self.controller.entity_registry
        conditions = []

        # Get all the integrations entities for this device
        for entry in registry.async_entries_for_device(device_id):
            if entry.domain != self.domain:
                continue

            supported_features = registry.get_supported_features(entry.entity_id)

            base_condition = {
                core.Const.CONF_CONDITION: "device",
                core.Const.CONF_DEVICE_ID: device_id,
                core.Const.CONF_DOMAIN: self.domain,
                core.Const.CONF_ENTITY_ID: entry.entity_id,
            }

            conditions.append({**base_condition, core.Const.CONF_TYPE: "is_hvac_mode"})

            if supported_features & core.Climate.EntityFeature.PRESET_MODE:
                conditions.append(
                    {**base_condition, core.Const.CONF_TYPE: "is_preset_mode"}
                )

        return conditions

    async def async_condition_from_config(
        self, config: core.ConfigType
    ) -> core.ConditionCheckerType:
        """Create a function to test a device condition."""

        def test_is_state(
            shc: core.SmartHomeController, _variables: core.TemplateVarsType
        ) -> bool:
            """Test if an entity is a certain state."""
            if (state := shc.states.get(config[core.Const.ATTR_ENTITY_ID])) is None:
                return False

            if config[core.Const.CONF_TYPE] == "is_hvac_mode":
                return state.state == config[core.Climate.ATTR_HVAC_MODE]

            return (
                state.attributes.get(core.Climate.ATTR_PRESET_MODE)
                == config[core.Climate.ATTR_PRESET_MODE]
            )

        return test_is_state

    async def async_get_condition_capabilities(
        self, config: core.ConfigType
    ) -> dict[str, vol.Schema] | typing.Awaitable[dict[str, vol.Schema]]:
        """List condition capabilities."""
        condition_type = config[core.Const.CONF_TYPE]
        entity_registry = self.controller.entity_registry

        fields = {}

        if condition_type == "is_hvac_mode":
            try:
                hvac_modes = (
                    entity_registry.get_capability(
                        config[core.Const.ATTR_ENTITY_ID], core.Climate.ATTR_HVAC_MODES
                    )
                    or []
                )
            except core.SmartHomeControllerError:
                hvac_modes = []
            fields[vol.Required(core.Climate.ATTR_HVAC_MODE)] = vol.In(hvac_modes)

        elif condition_type == "is_preset_mode":
            try:
                preset_modes = (
                    entity_registry.get_capability(
                        config[core.Const.ATTR_ENTITY_ID],
                        core.Climate.ATTR_PRESET_MODES,
                    )
                    or []
                )
            except core.SmartHomeControllerError:
                preset_modes = []
            fields[vol.Required(core.Climate.ATTR_PRESET_MODE)] = vol.In(preset_modes)

        return {"extra_fields": vol.Schema(fields)}

    # ----------------- Group Platform ------------------------------

    @core.callback
    def async_describe_on_off_states(
        self, registry: core.GroupIntegrationRegistry
    ) -> None:
        """Describe group on off states."""
        registry.on_off_states(
            set(core.Climate.HVAC_MODES) - {core.Climate.HVACMode.OFF},
            core.Const.STATE_OFF,
        )

    # ----------------- Recorder Platform ------------------------------

    @core.callback
    def exclude_attributes(self) -> set[str]:
        """Exclude static attributes from being recorded in the database."""
        return {
            core.Climate.ATTR_HVAC_MODES,
            core.Climate.ATTR_FAN_MODES,
            core.Climate.ATTR_SWING_MODES,
            core.Climate.ATTR_MIN_TEMP,
            core.Climate.ATTR_MAX_TEMP,
            core.Climate.ATTR_MIN_HUMIDITY,
            core.Climate.ATTR_MAX_HUMIDITY,
            core.Climate.ATTR_TARGET_TEMP_STEP,
            core.Climate.ATTR_PRESET_MODES,
        }

    # --------------- Reproduce State Platform ---------------------------

    async def async_reproduce_states(
        self,
        states: list[core.State],
        *,
        context: core.Context = None,
        reproduce_options: dict[str, typing.Any] = None,
    ):
        """Reproduce component states."""
        await asyncio.gather(
            *(
                _async_reproduce_states(
                    self.controller,
                    state,
                    self.domain,
                    context=context,
                )
                for state in states
            )
        )

    # ------------------ Trigger Platform ---------------------------

    @property
    def trigger_schema(self) -> typing.Callable[[core.ConfigType], core.ConfigType]:
        return _TRIGGER_SCHEMA

    async def async_get_triggers(self, device_id: str) -> list[dict[str, str]]:
        """List device triggers for Climate devices."""
        registry = self.controller.entity_registry
        triggers = []

        # Get all the integrations entities for this device
        for entry in registry.async_entries_for_device(device_id):
            if entry.domain != self.domain:
                continue

            state = self.controller.states.get(entry.entity_id)

            # Add triggers for each entity that belongs to this integration
            base_trigger = {
                core.Const.CONF_PLATFORM: "device",
                core.Const.CONF_DEVICE_ID: device_id,
                core.Const.CONF_DOMAIN: self.domain,
                core.Const.CONF_ENTITY_ID: entry.entity_id,
            }

            triggers.append(
                {
                    **base_trigger,
                    core.Const.CONF_TYPE: "hvac_mode_changed",
                }
            )

            if state and core.Climate.ATTR_CURRENT_TEMPERATURE in state.attributes:
                triggers.append(
                    {
                        **base_trigger,
                        core.Const.CONF_TYPE: "current_temperature_changed",
                    }
                )

            if state and core.Climate.ATTR_CURRENT_HUMIDITY in state.attributes:
                triggers.append(
                    {
                        **base_trigger,
                        core.Const.CONF_TYPE: "current_humidity_changed",
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
        if (trigger_type := config[core.Const.CONF_TYPE]) == "hvac_mode_changed":
            state_config = {
                core.Const.CONF_PLATFORM: "state",
                core.Const.CONF_ENTITY_ID: config[core.Const.CONF_ENTITY_ID],
                core.Const.CONF_TO: config[core.Const.CONF_TO],
                core.Const.CONF_FROM: [
                    mode
                    for mode in core.Climate.HVAC_MODES
                    if mode != config[core.Const.CONF_TO]
                ],
            }
            if core.Const.CONF_FOR in config:
                state_config[core.Const.CONF_FOR] = config[core.Const.CONF_FOR]
            state_config = await core.Trigger.async_validate_trigger_config(
                state_config
            )
            return await core.Trigger.async_attach_state_trigger(
                self.controller,
                state_config,
                action,
                trigger_info,
                platform_type="device",
            )

        numeric_state_config = {
            core.Const.CONF_PLATFORM: "numeric_state",
            core.Const.CONF_ENTITY_ID: config[core.Const.CONF_ENTITY_ID],
        }

        if trigger_type == "current_temperature_changed":
            numeric_state_config[
                core.Const.CONF_VALUE_TEMPLATE
            ] = "{{ state.attributes.current_temperature }}"
        else:
            numeric_state_config[
                core.Const.CONF_VALUE_TEMPLATE
            ] = "{{ state.attributes.current_humidity }}"

        if core.Const.CONF_ABOVE in config:
            numeric_state_config[core.Const.CONF_ABOVE] = config[core.Const.CONF_ABOVE]
        if core.Const.CONF_BELOW in config:
            numeric_state_config[core.Const.CONF_BELOW] = config[core.Const.CONF_BELOW]
        if core.Const.CONF_FOR in config:
            numeric_state_config[core.Const.CONF_FOR] = config[core.Const.CONF_FOR]

        numeric_state_config = await core.Trigger.async_validate_trigger_config(
            numeric_state_config
        )
        return await core.Trigger.async_attach_numeric_state_trigger(
            self.controller,
            numeric_state_config,
            action,
            trigger_info,
            platform_type="device",
        )

    async def async_get_trigger_capabilities(
        self, config: core.ConfigType
    ) -> dict[str, vol.Schema]:
        """List trigger capabilities."""
        trigger_type = config[core.Const.CONF_TYPE]

        if trigger_type == "hvac_action_changed":
            return {}

        if trigger_type == "hvac_mode_changed":
            return {
                "extra_fields": vol.Schema(
                    {vol.Optional(core.Const.CONF_FOR): _cv.positive_time_period_dict}
                )
            }

        if trigger_type == "current_temperature_changed":
            unit_of_measurement = self.controller.config.units.temperature_unit
        else:
            unit_of_measurement = core.Const.PERCENTAGE

        return {
            "extra_fields": vol.Schema(
                {
                    vol.Optional(
                        core.Const.CONF_ABOVE,
                        description={"suffix": unit_of_measurement},
                    ): vol.Coerce(float),
                    vol.Optional(
                        core.Const.CONF_BELOW,
                        description={"suffix": unit_of_measurement},
                    ): vol.Coerce(float),
                    vol.Optional(core.Const.CONF_FOR): _cv.positive_time_period_dict,
                }
            )
        }


async def _async_reproduce_states(
    shc: core.SmartHomeController,
    state: core.State,
    domain: str,
    *,
    context: core.Context = None,
) -> None:
    """Reproduce component states."""

    async def call_service(service: str, keys: typing.Iterable, data=None):
        """Call service with set of attributes given."""
        data = data or {}
        data["entity_id"] = state.entity_id
        for key in keys:
            if (value := state.attributes.get(key)) is not None:
                data[key] = value

        await shc.services.async_call(
            domain, service, data, blocking=True, context=context
        )

    if state.state in core.Climate.HVAC_MODES:
        await call_service(
            core.Climate.SERVICE_SET_HVAC_MODE,
            [],
            {core.Climate.ATTR_HVAC_MODE: state.state},
        )

    if core.Climate.ATTR_AUX_HEAT in state.attributes:
        await call_service(
            core.Climate.SERVICE_SET_AUX_HEAT, [core.Climate.ATTR_AUX_HEAT]
        )

    if (
        (core.Const.ATTR_TEMPERATURE in state.attributes)
        or (core.Climate.ATTR_TARGET_TEMP_HIGH in state.attributes)
        or (core.Climate.ATTR_TARGET_TEMP_LOW in state.attributes)
    ):
        await call_service(
            core.Climate.SERVICE_SET_TEMPERATURE,
            [
                core.Const.ATTR_TEMPERATURE,
                core.Climate.ATTR_TARGET_TEMP_HIGH,
                core.Climate.ATTR_TARGET_TEMP_LOW,
            ],
        )

    if core.Climate.ATTR_PRESET_MODE in state.attributes:
        await call_service(
            core.Climate.SERVICE_SET_PRESET_MODE, [core.Climate.ATTR_PRESET_MODE]
        )

    if core.Climate.ATTR_SWING_MODE in state.attributes:
        await call_service(
            core.Climate.SERVICE_SET_SWING_MODE, [core.Climate.ATTR_SWING_MODE]
        )

    if core.Climate.ATTR_FAN_MODE in state.attributes:
        await call_service(
            core.Climate.SERVICE_SET_FAN_MODE, [core.Climate.ATTR_FAN_MODE]
        )

    if core.Climate.ATTR_HUMIDITY in state.attributes:
        await call_service(
            core.Climate.SERVICE_SET_HUMIDITY, [core.Climate.ATTR_HUMIDITY]
        )
