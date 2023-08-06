"""
Vacuum Component for Smart Home - The Next Generation.

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

import voluptuous as vol

from ... import core

_cv: typing.TypeAlias = core.ConfigValidation
_const: typing.TypeAlias = core.Const
_vacuum: typing.TypeAlias = core.Vacuum

_LOGGER: typing.Final = logging.getLogger(__name__)
_ACTION_TYPES: typing.Final = {"clean", "dock"}
_CONDITION_TYPES: typing.Final = {"is_cleaning", "is_docked"}
_VALID_STATES_TOGGLE: typing.Final = {_const.STATE_ON, _const.STATE_OFF}
_VALID_STATES_STATE = {
    _vacuum.STATE_CLEANING,
    _vacuum.STATE_DOCKED,
    _const.STATE_IDLE,
    _vacuum.STATE_RETURNING,
    _const.STATE_PAUSED,
}
_TRIGGER_TYPES: typing.Final = {"cleaning", "docked"}
_TRIGGER_SCHEMA: typing.Final = _cv.DEVICE_TRIGGER_BASE_SCHEMA.extend(
    {
        vol.Required(_const.CONF_ENTITY_ID): _cv.entity_id,
        vol.Required(_const.CONF_TYPE): vol.In(_TRIGGER_TYPES),
        vol.Optional(_const.CONF_FOR): _cv.positive_time_period_dict,
    }
)


# pylint: disable=unused-variable, too-many-ancestors
class VacuumComponent(
    core.SmartHomeControllerComponent,
    core.ActionPlatform,
    core.ConditionPlatform,
    core.GroupPlatform,
    core.RecorderPlatform,
    core.ReproduceStatePlatform,
    core.TriggerPlatform,
):
    """Support for vacuum cleaner robots (botvacs)."""

    def __init__(self, path: typing.Iterable[str]):
        super().__init__(path)
        self._entities: core.EntityComponent = None
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
        return self._entities

    @property
    def platform_schema(self) -> typing.Callable[[core.ConfigType], core.ConfigType]:
        return _cv.PLATFORM_SCHEMA

    @property
    def platform_schema_base(
        self,
    ) -> typing.Callable[[core.ConfigType], core.ConfigType]:
        return _cv.PLATFORM_SCHEMA_BASE

    def _is_on(self, entity_id: str) -> bool:
        """Return if the vacuum is on based on the statemachine."""
        return self.controller.states.is_state(entity_id, _const.STATE_ON)

    async def async_setup(self, config: core.ConfigType) -> bool:
        """Set up the vacuum component."""
        if not await super().async_setup(config):
            return False

        component = self._entities = core.EntityComponent(
            _LOGGER, self.domain, self.controller, self.scan_interval
        )

        await component.async_setup(config)

        component.async_register_entity_service(
            _const.SERVICE_TURN_ON, {}, "async_turn_on"
        )
        component.async_register_entity_service(
            _const.SERVICE_TURN_OFF, {}, "async_turn_off"
        )
        component.async_register_entity_service(
            _const.SERVICE_TOGGLE, {}, "async_toggle"
        )
        component.async_register_entity_service(
            _vacuum.SERVICE_START_PAUSE, {}, "async_start_pause"
        )
        component.async_register_entity_service(
            _vacuum.SERVICE_START, {}, "async_start"
        )
        component.async_register_entity_service(
            _vacuum.SERVICE_PAUSE, {}, "async_pause"
        )
        component.async_register_entity_service(
            _vacuum.SERVICE_RETURN_TO_BASE, {}, "async_return_to_base"
        )
        component.async_register_entity_service(
            _vacuum.SERVICE_CLEAN_SPOT, {}, "async_clean_spot"
        )
        component.async_register_entity_service(
            _vacuum.SERVICE_LOCATE, {}, "async_locate"
        )
        component.async_register_entity_service(_vacuum.SERVICE_STOP, {}, "async_stop")
        component.async_register_entity_service(
            _vacuum.SERVICE_SET_FAN_SPEED,
            {vol.Required(_vacuum.ATTR_FAN_SPEED): _cv.string},
            "async_set_fan_speed",
        )
        component.async_register_entity_service(
            _vacuum.SERVICE_SEND_COMMAND,
            {
                vol.Required(_const.ATTR_COMMAND): _cv.string,
                vol.Optional(_vacuum.ATTR_PARAMS): vol.Any(dict, _cv.ensure_list),
            },
            "async_send_command",
        )

        return True

    async def async_setup_entry(self, entry: core.ConfigEntry) -> bool:
        """Set up a config entry."""
        return await self.entity_component.async_setup_entry(entry)

    async def async_unload_entry(self, entry: core.ConfigEntry) -> bool:
        """Unload a config entry."""
        return await self.entity_component.async_unload_entry(entry)

    # --------------------------- Action Platform ---------------------------------

    @property
    def action_schema(self) -> typing.Callable[[core.ConfigType], core.ConfigType]:
        return _cv.DEVICE_ACTION_BASE_SCHEMA.extend(
            {
                vol.Required(_const.CONF_TYPE): vol.In(_ACTION_TYPES),
                vol.Required(_const.CONF_ENTITY_ID): _cv.entity_domain(self.domain),
            }
        )

    async def async_get_actions(self, device_id: str) -> list[dict[str, str]]:
        """List device actions for Vacuum devices."""
        registry = self.controller.entity_registry
        actions = []

        # Get all the integrations entities for this device
        for entry in registry.async_entries_for_device(device_id):
            if entry.domain != self.domain:
                continue

            base_action = {
                _const.CONF_DEVICE_ID: device_id,
                _const.CONF_DOMAIN: self.domain,
                _const.CONF_ENTITY_ID: entry.entity_id,
            }

            actions.append({**base_action, _const.CONF_TYPE: "clean"})
            actions.append({**base_action, _const.CONF_TYPE: "dock"})

        return actions

    async def async_call_action_from_config(
        self,
        config: core.ConfigType,
        _variables: dict[str, typing.Any],
        context: core.Context,
    ) -> None:
        """Execute a device action."""
        config = self.action_schema(config)  # pylint: disable=not-callable

        service_data = {_const.ATTR_ENTITY_ID: config[_const.CONF_ENTITY_ID]}

        if config[_const.CONF_TYPE] == "clean":
            service = _vacuum.SERVICE_START
        elif config[_const.CONF_TYPE] == "dock":
            service = _vacuum.SERVICE_RETURN_TO_BASE

        await self.controller.services.async_call(
            self.domain, service, service_data, blocking=True, context=context
        )

    # ---------------------------- Condition Platform --------------------------

    @property
    def condition_schema(self) -> typing.Callable[[core.ConfigType], core.ConfigType]:
        return _cv.DEVICE_CONDITION_BASE_SCHEMA.extend(
            {
                vol.Required(_const.CONF_ENTITY_ID): _cv.entity_id,
                vol.Required(_const.CONF_TYPE): vol.In(_CONDITION_TYPES),
            }
        )

    async def async_get_conditions(self, device_id: str) -> list[dict[str, str]]:
        """List device conditions for Vacuum devices."""
        registry = self.controller.entity_registry
        conditions = []

        # Get all the integrations entities for this device
        for entry in registry.async_entries_for_device(device_id):
            if entry.domain != self.domain:
                continue

            base_condition = {
                _const.CONF_CONDITION: "device",
                _const.CONF_DEVICE_ID: device_id,
                _const.CONF_DOMAIN: self.domain,
                _const.CONF_ENTITY_ID: entry.entity_id,
            }

            conditions += [
                {**base_condition, _const.CONF_TYPE: cond} for cond in _CONDITION_TYPES
            ]

        return conditions

    async def async_condition_from_config(
        self, config: core.ConfigType
    ) -> core.ConditionCheckerType:
        """Create a function to test a device condition."""
        if config[_const.CONF_TYPE] == "is_docked":
            test_states = [_vacuum.STATE_DOCKED]
        else:
            test_states = [_vacuum.STATE_CLEANING, _vacuum.STATE_RETURNING]

        def test_is_state(
            shc: core.SmartHomeController, _variables: core.TemplateVarsType
        ) -> bool:
            """Test if an entity is a certain state."""
            state = shc.states.get(config[_const.ATTR_ENTITY_ID])
            return state is not None and state.state in test_states

        return test_is_state

    # ---------------------- Group Platform ----------------------------------

    def async_describe_on_off_states(
        self, registry: core.GroupIntegrationRegistry
    ) -> None:
        """Describe group on off states."""
        registry.on_off_states(
            {
                _vacuum.STATE_CLEANING,
                _const.STATE_ON,
                _vacuum.STATE_RETURNING,
                _vacuum.STATE_ERROR,
            },
            _const.STATE_OFF,
        )

    # --------------------- Recorder Platform -----------------------------------

    def exclude_attributes(self) -> set[str]:
        """Exclude static attributes from being recorded in the database."""
        return {_vacuum.ATTR_FAN_SPEED_LIST}

    # -------------------- Reproduce State Platform ------------------------------

    # pylint: disable=unused-argument
    async def async_reproduce_states(
        self,
        states: list[core.State],
        *,
        context: core.Context = None,
        reproduce_options: dict[str, typing.Any] = None,
    ):
        """Reproduce Vacuum states."""
        # Reproduce states in parallel.
        await asyncio.gather(
            *(self._async_reproduce_state(state, context=context) for state in states)
        )

    async def _async_reproduce_state(
        self,
        state: core.State,
        *,
        context: core.Context = None,
    ) -> None:
        """Reproduce a single state."""
        if (cur_state := self.controller.states.get(state.entity_id)) is None:
            _LOGGER.warning(f"Unable to find entity {state.entity_id}")
            return

        if not (
            state.state in _VALID_STATES_TOGGLE or state.state in _VALID_STATES_STATE
        ):
            _LOGGER.warning(
                f"Invalid state specified for {state.entity_id}: {state.state}"
            )
            return

        # Return if we are already at the right state.
        if cur_state.state == state.state and cur_state.attributes.get(
            _vacuum.ATTR_FAN_SPEED
        ) == state.attributes.get(_vacuum.ATTR_FAN_SPEED):
            return

        service_data = {_const.ATTR_ENTITY_ID: state.entity_id}

        if cur_state.state != state.state:
            # Wrong state
            if state.state == _const.STATE_ON:
                service = _const.SERVICE_TURN_ON
            elif state.state == _const.STATE_OFF:
                service = _const.SERVICE_TURN_OFF
            elif state.state == _vacuum.STATE_CLEANING:
                service = _vacuum.SERVICE_START
            elif state.state in [_vacuum.STATE_DOCKED, _vacuum.STATE_RETURNING]:
                service = _vacuum.SERVICE_RETURN_TO_BASE
            elif state.state == _const.STATE_IDLE:
                service = _vacuum.SERVICE_STOP
            elif state.state == _const.STATE_PAUSED:
                service = _vacuum.SERVICE_PAUSE

            await self.controller.services.async_call(
                self.domain, service, service_data, context=context, blocking=True
            )

        if cur_state.attributes.get(_vacuum.ATTR_FAN_SPEED) != state.attributes.get(
            _vacuum.ATTR_FAN_SPEED
        ):
            # Wrong fan speed
            service_data["fan_speed"] = state.attributes[_vacuum.ATTR_FAN_SPEED]
            await self.controller.services.async_call(
                self.domain,
                _vacuum.SERVICE_SET_FAN_SPEED,
                service_data,
                context=context,
                blocking=True,
            )

    # ------------------------- Trigger Platform ------------------------------

    @property
    def trigger_schema(self) -> typing.Callable[[core.ConfigType], core.ConfigType]:
        return _TRIGGER_SCHEMA

    async def async_get_triggers(self, device_id: str) -> list[dict[str, str]]:
        """List device triggers for Vacuum devices."""
        registry = self.controller.entity_registry
        triggers = []

        # Get all the integrations entities for this device
        for entry in registry.async_entries_for_device(device_id):
            if entry.domain != self.domain:
                continue

            triggers += [
                {
                    _const.CONF_PLATFORM: "device",
                    _const.CONF_DEVICE_ID: device_id,
                    _const.CONF_DOMAIN: self.domain,
                    _const.CONF_ENTITY_ID: entry.entity_id,
                    _const.CONF_TYPE: trigger,
                }
                for trigger in _TRIGGER_TYPES
            ]

        return triggers

    async def async_get_trigger_capabilities(
        self, config: core.ConfigType
    ) -> dict[str, vol.Schema]:
        """List trigger capabilities."""
        return {
            "extra_fields": vol.Schema(
                {vol.Optional(_const.CONF_FOR): _cv.positive_time_period_dict}
            )
        }

    async def async_attach_trigger(
        self,
        config: core.ConfigType,
        action: core.TriggerActionType,
        trigger_info: core.TriggerInfo,
    ) -> core.CallbackType:
        """Attach a trigger."""
        if config[_const.CONF_TYPE] == "cleaning":
            to_state = _vacuum.STATE_CLEANING
        else:
            to_state = _vacuum.STATE_DOCKED

        state_config = {
            _const.CONF_PLATFORM: "state",
            _const.CONF_ENTITY_ID: config[_const.CONF_ENTITY_ID],
            _const.CONF_TO: to_state,
        }
        if _const.CONF_FOR in config:
            state_config[_const.CONF_FOR] = config[_const.CONF_FOR]
        state_config = await core.Trigger.async_validate_trigger_config(state_config)
        return await core.Trigger.async_attach_state_trigger(
            self.controller, state_config, action, trigger_info, platform_type="device"
        )
