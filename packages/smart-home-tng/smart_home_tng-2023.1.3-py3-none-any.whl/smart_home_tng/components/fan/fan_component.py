"""
Fan Component for Smart Home - The Next Generation.

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
_CONDITION_TYPES: typing.Final = {"is_on", "is_off"}
_CONDITION_SCHEMA: typing.Final = _cv.DEVICE_CONDITION_BASE_SCHEMA.extend(
    {
        vol.Required(core.Const.CONF_ENTITY_ID): _cv.entity_id,
        vol.Required(core.Const.CONF_TYPE): vol.In(_CONDITION_TYPES),
    }
)
_VALID_STATES: typing.Final = {core.Const.STATE_ON, core.Const.STATE_OFF}

# These are used as parameters to fan.turn_on service.
_SPEED_AND_MODE_ATTRIBUTES: typing.Final = {
    core.Fan.ATTR_PERCENTAGE: core.Fan.SERVICE_SET_PERCENTAGE,
    core.Fan.ATTR_PRESET_MODE: core.Fan.SERVICE_SET_PRESET_MODE,
}

_SIMPLE_ATTRIBUTES: typing.Final = {  # attribute: service
    core.Fan.ATTR_DIRECTION: core.Fan.SERVICE_SET_DIRECTION,
    core.Fan.ATTR_OSCILLATING: core.Fan.SERVICE_OSCILLATE,
}


# pylint: disable=unused-variable, too-many-ancestors
class FanComponent(
    core.SmartHomeControllerComponent,
    core.ActionPlatform,
    core.ConditionPlatform,
    core.TriggerPlatform,
    core.GroupPlatform,
    core.RecorderPlatform,
    core.ReproduceStatePlatform,
):
    """Provides functionality to interact with fans."""

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
    def scan_interval(self) -> dt.timedelta:
        return core.Fan.SCAN_INTERVAL

    def _is_on(self, entity_id: str) -> bool:
        entity = self.controller.states.get(entity_id)
        assert entity
        return entity.state == core.Const.STATE_ON

    async def async_setup(self, config: core.ConfigType) -> bool:
        """Expose fan control via statemachine and services."""
        component = self._entities = core.EntityComponent(
            _LOGGER, self.domain, self.controller, self.scan_interval
        )

        await component.async_setup(config)

        # After the transition to percentage and preset_modes concludes,
        # switch this back to async_turn_on and remove async_turn_on_compat
        component.async_register_entity_service(
            core.Const.SERVICE_TURN_ON,
            {
                vol.Optional(core.Fan.ATTR_PERCENTAGE): vol.All(
                    vol.Coerce(int), vol.Range(min=0, max=100)
                ),
                vol.Optional(core.Fan.ATTR_PRESET_MODE): _cv.string,
            },
            "async_turn_on",
        )
        component.async_register_entity_service(
            core.Const.SERVICE_TURN_OFF, {}, "async_turn_off"
        )
        component.async_register_entity_service(
            core.Const.SERVICE_TOGGLE, {}, "async_toggle"
        )
        component.async_register_entity_service(
            core.Fan.SERVICE_INCREASE_SPEED,
            {
                vol.Optional(core.Fan.ATTR_PERCENTAGE_STEP): vol.All(
                    vol.Coerce(int), vol.Range(min=0, max=100)
                )
            },
            "async_increase_speed",
            [core.Fan.EntityFeature.SET_SPEED],
        )
        component.async_register_entity_service(
            core.Fan.SERVICE_DECREASE_SPEED,
            {
                vol.Optional(core.Fan.ATTR_PERCENTAGE_STEP): vol.All(
                    vol.Coerce(int), vol.Range(min=0, max=100)
                )
            },
            "async_decrease_speed",
            [core.Fan.EntityFeature.SET_SPEED],
        )
        component.async_register_entity_service(
            core.Fan.SERVICE_OSCILLATE,
            {vol.Required(core.Fan.ATTR_OSCILLATING): _cv.boolean},
            "async_oscillate",
            [core.Fan.EntityFeature.OSCILLATE],
        )
        component.async_register_entity_service(
            core.Fan.SERVICE_SET_DIRECTION,
            {vol.Optional(core.Fan.ATTR_DIRECTION): _cv.string},
            "async_set_direction",
            [core.Fan.EntityFeature.DIRECTION],
        )
        component.async_register_entity_service(
            core.Fan.SERVICE_SET_PERCENTAGE,
            {
                vol.Required(core.Fan.ATTR_PERCENTAGE): vol.All(
                    vol.Coerce(int), vol.Range(min=0, max=100)
                )
            },
            "async_set_percentage",
            [core.Fan.EntityFeature.SET_SPEED],
        )
        component.async_register_entity_service(
            core.Fan.SERVICE_SET_PRESET_MODE,
            {vol.Required(core.Fan.ATTR_PRESET_MODE): _cv.string},
            "async_set_preset_mode",
            [core.Fan.EntityFeature.SET_SPEED, core.Fan.EntityFeature.PRESET_MODE],
        )

        return True

    async def async_setup_entry(self, entry: core.ConfigEntry) -> bool:
        """Set up a config entry."""
        component: core.EntityComponent = self._entities
        return await component.async_setup_entry(entry)

    async def async_unload_entry(self, entry: core.ConfigEntry) -> bool:
        """Unload a config entry."""
        component: core.EntityComponent = self._entities
        return await component.async_unload_entry(entry)

    # ------------------- Action Platform --------------------------------

    @property
    def action_schema(self) -> typing.Callable[[core.ConfigType], core.ConfigType]:
        ACTION_SCHEMA: typing.Final = core.Toggle.ACTION_SCHEMA.extend(
            {vol.Required(core.Const.CONF_DOMAIN): self.domain}
        )
        return ACTION_SCHEMA

    async def async_get_actions(self, device_id: str) -> list[dict[str, str]]:
        """List device actions for Fan devices."""
        return await core.Toggle.async_get_actions(
            self.controller, device_id, self.domain
        )

    async def async_call_action_from_config(
        self,
        config: core.ConfigType,
        variables: dict[str, typing.Any],
        context: core.Context,
    ) -> None:
        """Execute a device action."""
        await core.Toggle.async_call_action_from_config(
            self.controller, config, variables, context, self.domain
        )

    # --------------------- Condition Platform -----------------------------

    @property
    def condition_schema(self) -> typing.Callable[[core.ConfigType], core.ConfigType]:
        return _CONDITION_SCHEMA

    async def async_get_conditions(self, device_id: str) -> list[dict[str, str]]:
        """List device conditions for Fan devices."""
        registry = self.controller.entity_registry
        conditions = []

        # Get all the integrations entities for this device
        for entry in registry.async_entries_for_device(device_id):
            if entry.domain != self.domain:
                continue

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

    @core.callback
    async def async_condition_from_config(
        self, config: core.ConfigType
    ) -> core.ConditionCheckerType:
        """Create a function to test a device condition."""
        if config[core.Const.CONF_TYPE] == "is_on":
            state = core.Const.STATE_ON
        else:
            state = core.Const.STATE_OFF

        @core.callback
        def test_is_state(
            _shc: core.SmartHomeController, _variables: core.TemplateVarsType
        ) -> bool:
            """Test if an entity is a certain state."""
            return self.state(config[core.Const.ATTR_ENTITY_ID], state)

        return test_is_state

    # ------------------- Group Platform ---------------------------

    def async_describe_on_off_states(
        self, registry: core.GroupIntegrationRegistry
    ) -> None:
        """Describe group on off states."""
        registry.on_off_states({core.Const.STATE_ON}, core.Const.STATE_OFF)

    # -------------------- Recorder Platform -------------------------

    def exclude_attributes(self) -> set[str]:
        """Exclude static attributes from being recorded in the database."""
        return {core.Fan.ATTR_PRESET_MODES}

    # ------------------- Reproduce State Platform ----------------------

    async def async_reproduce_states(
        self,
        states: list[core.State],
        *,
        context: core.Context = None,
        reproduce_options: dict[str, typing.Any] = None,
    ):
        """Reproduce Fan states."""
        await asyncio.gather(
            *(
                _async_reproduce_state(
                    self.controller,
                    self.domain,
                    state,
                    context=context,
                )
                for state in states
            )
        )

    # ------------------- Trigger Platform ------------------------------

    @property
    def trigger_schema(self) -> typing.Callable[[core.ConfigType], core.ConfigType]:
        TRIGGER_SCHEMA: typing.Final = vol.All(
            core.Toggle.TRIGGER_SCHEMA,
            vol.Schema(
                {vol.Required(core.Const.CONF_DOMAIN): self.domain},
                extra=vol.ALLOW_EXTRA,
            ),
        )
        return TRIGGER_SCHEMA

    async def async_get_triggers(self, device_id: str) -> list[dict[str, str]]:
        """List device triggers for Fan devices."""
        return await core.Toggle.async_get_triggers(
            self.controller, device_id, self.domain
        )

    async def async_get_trigger_capabilities(
        self, config: core.ConfigType
    ) -> dict[str, vol.Schema]:
        """List trigger capabilities."""
        return await core.Toggle.async_get_trigger_capabilities(config)

    async def async_attach_trigger(
        self,
        config: core.ConfigType,
        action: core.TriggerActionType,
        trigger_info: core.TriggerInfo,
    ) -> core.CallbackType:
        """Listen for state changes based on configuration."""
        return await core.Toggle.async_attach_trigger(
            self.controller, config, action, trigger_info
        )


async def _async_reproduce_state(
    shc: core.SmartHomeController,
    domain: str,
    state: core.State,
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

    service_calls: dict[str, dict[str, typing.Any]] = {}

    if state.state == core.Const.STATE_ON:
        # The fan should be on
        if cur_state.state != core.Const.STATE_ON:
            # Turn on the fan with all the speed and modes attributes.
            # The `turn_on` method will figure out in which mode to
            # turn the fan on.
            service_calls[core.Const.SERVICE_TURN_ON] = {
                attr: state.attributes.get(attr)
                for attr in _SPEED_AND_MODE_ATTRIBUTES
                if state.attributes.get(attr) is not None
            }
        else:
            # If the fan is already on, we need to set speed or mode
            # based on the state.
            #
            # Speed and preset mode are mutually exclusive, so one of
            # them is always going to be stored as None. If we were to
            # try to set it, it will raise an error. So instead we
            # only update the one that is non-None.
            for attr, service in _SPEED_AND_MODE_ATTRIBUTES.items():
                value = state.attributes.get(attr)
                if value is not None and value != cur_state.attributes.get(attr):
                    service_calls[service] = {attr: value}

        # The simple attributes are copied directly. They can only be
        # None if the fan does not support the feature in the first
        # place, so the equality check ensures we don't call the
        # services with invalid parameters.
        for attr, service in _SIMPLE_ATTRIBUTES.items():
            if (value := state.attributes.get(attr)) != cur_state.attributes.get(attr):
                service_calls[service] = {attr: value}
    elif state.state == core.Const.STATE_OFF and cur_state.state != state.state:
        service_calls[core.Const.SERVICE_TURN_OFF] = {}

    for service, data in service_calls.items():
        await shc.services.async_call(
            domain,
            service,
            {core.Const.ATTR_ENTITY_ID: state.entity_id, **data},
            context=context,
            blocking=True,
        )
