"""
Automation Integration for Smart Home - The Next Generation.

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
import contextlib
import logging
import typing

import voluptuous as vol
import voluptuous.humanize as vh

from ... import core
from .automation_config import AutomationConfig
from .automation_entity import AutomationEntity
from .const import Const

_cv: typing.TypeAlias = core.ConfigValidation

_LOGGER: typing.Final = logging.getLogger(__name__)
_CONDITION_SCHEMA = vol.All(_cv.ensure_list, [_cv.CONDITION_SCHEMA])

_PLATFORM_SCHEMA = vol.All(
    _cv.deprecated(Const.CONF_HIDE_ENTITY),
    core.Scripts.make_script_schema(
        {
            # str on purpose
            core.Const.CONF_ID: str,
            core.Const.CONF_ALIAS: _cv.string,
            vol.Optional(core.Const.CONF_DESCRIPTION): _cv.string,
            vol.Optional(Const.CONF_TRACE, default={}): _cv.TRACE_CONFIG_SCHEMA,
            vol.Optional(Const.CONF_INITIAL_STATE): _cv.boolean,
            vol.Optional(Const.CONF_HIDE_ENTITY): _cv.boolean,
            vol.Required(Const.CONF_TRIGGER): _cv.TRIGGER_SCHEMA,
            vol.Optional(core.Const.CONF_CONDITION): _CONDITION_SCHEMA,
            vol.Optional(core.Const.CONF_VARIABLES): _cv.SCRIPT_VARIABLES_SCHEMA,
            vol.Optional(Const.CONF_TRIGGER_VARIABLES): _cv.SCRIPT_VARIABLES_SCHEMA,
            vol.Required(Const.CONF_ACTION): _cv.SCRIPT_SCHEMA,
        },
        core.Scripts.Const.SCRIPT_MODE_SINGLE,
    ),
)


# pylint: disable=unused-variable
class Automation(
    core.AutomationComponent, core.LogbookPlatform, core.ReproduceStatePlatform
):
    """Allow to set up simple automation rules via the config file."""

    def __init__(self, path: typing.Iterable[str]):
        super().__init__(path)
        self._component: core.EntityComponent = None
        self._blueprint_component: core.BlueprintComponent | asyncio.Event = None
        self._domain_blueprints: core.DomainBlueprintsBase | asyncio.Event = None
        self._supported_platforms = frozenset(
            [
                core.Platform.RECORDER,
                core.Platform.REPRODUCE_STATE,
            ]
        )

    @property
    def entity_component(self) -> core.EntityComponent:
        return self._component

    def async_describe_events(self, async_describe_event: core.LogbookCallback) -> None:
        async_describe_event(core.Const.EVENT_AUTOMATION_TRIGGERED)

    def async_describe_event(self, event: core.LazyPartialState) -> dict[str, str]:
        data = event.data
        message = "triggered"
        if core.Const.ATTR_SOURCE in data:
            message = f"{message} by {data[core.Const.ATTR_SOURCE]}"

        return {
            core.Const.LOGBOOK_ENTRY_NAME: data.get(core.Const.ATTR_NAME),
            core.Const.LOGBOOK_ENTRY_MESSAGE: message,
            core.Const.LOGBOOK_ENTRY_ENTITY_ID: data.get(core.Const.ATTR_ENTITY_ID),
            core.Const.LOGBOOK_ENTRY_CONTEXT_ID: event.context_id,
        }

    async def async_setup(self, config: core.ConfigType) -> bool:
        """Set up all automations."""
        if not await super().async_setup(config):
            return False

        self._component = core.EntityComponent(Const.LOGGER, self.domain, self._shc)

        # Process integration platforms right away since
        # we will create entities before firing EVENT_COMPONENT_LOADED
        await self._shc.setup.async_process_integration_platform_for_component(
            self.domain
        )

        if not await self._async_process_config(config, self._component):
            blueprints = await self._async_get_blueprints()
            if blueprints is not None:
                await blueprints.async_populate()

        self._component.async_register_entity_service(
            Const.SERVICE_TRIGGER,
            {
                vol.Optional(Const.ATTR_VARIABLES, default={}): dict,
                vol.Optional(Const.CONF_SKIP_CONDITION, default=True): bool,
            },
            self._trigger_service_handler,
        )
        self._component.async_register_entity_service(
            core.Const.SERVICE_TOGGLE, {}, "async_toggle"
        )
        self._component.async_register_entity_service(
            core.Const.SERVICE_TURN_ON, {}, "async_turn_on"
        )
        self._component.async_register_entity_service(
            core.Const.SERVICE_TURN_OFF,
            {
                vol.Optional(
                    Const.CONF_STOP_ACTIONS, default=Const.DEFAULT_STOP_ACTIONS
                ): _cv.boolean
            },
            "async_turn_off",
        )

        reload_helper = core.ReloadServiceHelper(self._reload_service_handler)

        core.Service.async_register_admin_service(
            self._shc,
            self.domain,
            core.Const.SERVICE_RELOAD,
            reload_helper.execute_service,
            schema=vol.Schema({}),
        )

        return True

    async def _reload_service_handler(self, service_call: core.ServiceCall):
        """Remove all automations and load new ones from config."""
        if (conf := await self._component.async_prepare_reload()) is None:
            return
        blueprints = await self._async_get_blueprints()
        if blueprints is not None:
            blueprints.reset_cache()
        await self._async_process_config(conf, self._component)
        self._shc.bus.async_fire(
            core.Const.EVENT_AUTOMATION_RELOADED, context=service_call.context
        )

    async def _trigger_service_handler(
        self, entity: core.Entity, service_call: core.ServiceCall
    ):
        """Handle forced automation trigger, e.g. from frontend."""
        await entity.async_trigger(
            {
                **service_call.data[Const.ATTR_VARIABLES],
                "trigger": {"platform": None},
            },
            skip_condition=service_call.data[Const.CONF_SKIP_CONDITION],
            context=service_call.context,
        )

    async def async_validate_config(self, config: core.ConfigType):
        """Validate config."""
        automations = list(
            filter(
                lambda x: x is not None,
                await asyncio.gather(
                    *(
                        self._try_async_validate_config_item(p_config, config)
                        for _, p_config in self._shc.setup.config_per_platform(
                            config, self.domain
                        )
                    )
                ),
            )
        )

        # Create a copy of the configuration with all config for current
        # component removed and add validated config back in.
        config = self._shc.setup.config_without_domain(config, self.domain)
        config[self.domain] = automations

        return config

    async def async_validate_config_item(self, config: core.JsonType):
        """Validate config item."""
        comp = await self._async_get_blueprint_component()
        if comp and comp.is_blueprint_instance_config(config):
            blueprints = await self._async_get_blueprints()
            if blueprints is not None:
                return await blueprints.async_inputs_from_config(config)
            raise NotImplementedError()

        config = _PLATFORM_SCHEMA(config)

        config[Const.CONF_TRIGGER] = await core.Scripts.async_validate_trigger_config(
            self._shc, config[Const.CONF_TRIGGER]
        )

        if core.Const.CONF_CONDITION in config:
            config[
                core.Const.CONF_CONDITION
            ] = await core.ScriptCondition.async_validate_conditions_config(
                self._shc, config[core.Const.CONF_CONDITION]
            )

        config[
            Const.CONF_ACTION
        ] = await core.Scripts.async_validate_automation_actions_config(
            self._shc, config[Const.CONF_ACTION]
        )

        return config

    async def _try_async_validate_config_item(self, config, full_config=None):
        """Validate config item."""
        raw_config = None
        with contextlib.suppress(ValueError):
            raw_config = dict(config)

        try:
            config = await self.async_validate_config_item(config)
        except (
            vol.Invalid,
            core.SmartHomeControllerError,
            core.IntegrationNotFound,
            core.InvalidDeviceAutomationConfig,
        ) as ex:
            self._shc.setup.async_log_exception(ex, self.domain, full_config or config)
            return None

        if isinstance(config, core.BlueprintInputsBase):
            return config

        config = AutomationConfig(config)
        config.raw_config = raw_config
        return config

    async def _async_process_config(
        self,
        config: dict[str, typing.Any],
        component: core.EntityComponent,
    ) -> bool:
        """Process config and add automations.

        Returns if blueprints were used.
        """
        entities = []
        blueprints_used = False

        for config_key in self._shc.setup.extract_domain_configs(config, self.domain):
            conf: list[dict[str, typing.Any] | core.BlueprintInputsBase] = config[
                config_key
            ]

            for list_no, config_block in enumerate(conf):
                raw_blueprint_inputs = None
                raw_config = None
                if isinstance(config_block, core.BlueprintInputsBase):
                    blueprints_used = True
                    blueprint_inputs = config_block
                    raw_blueprint_inputs = blueprint_inputs.config_with_inputs

                    try:
                        raw_config = blueprint_inputs.async_substitute()
                        config_block = typing.cast(
                            dict[str, typing.Any],
                            await self.async_validate_config_item(raw_config),
                        )
                    except vol.Invalid as err:
                        Const.LOGGER.error(
                            f"Blueprint {blueprint_inputs.blueprint.name} generated invalid "
                            + f"automation with inputs {blueprint_inputs.inputs}: "
                            + f"{vh.humanize_error(config_block, err)}",
                        )
                        continue
                else:
                    raw_config = typing.cast(AutomationConfig, config_block).raw_config

                automation_id = config_block.get(core.Const.CONF_ID)
                name = (
                    config_block.get(core.Const.CONF_ALIAS) or f"{config_key} {list_no}"
                )

                initial_state = config_block.get(Const.CONF_INITIAL_STATE)

                action_script = core.Scripts.Script(
                    self._shc,
                    config_block[Const.CONF_ACTION],
                    name,
                    self.domain,
                    running_description="automation actions",
                    script_mode=config_block[core.Const.CONF_MODE],
                    max_runs=config_block[core.Scripts.Const.CONF_MAX],
                    max_exceeded=config_block[core.Scripts.Const.CONF_MAX_EXCEEDED],
                    logger=Const.LOGGER,
                    # We don't pass variables here
                    # Automation will already render them to use them in the condition
                    # and so will pass them on to the script.
                )

                if core.Const.CONF_CONDITION in config_block:
                    cond_func = await self._async_process_if(name, config_block)

                    if cond_func is None:
                        continue
                else:
                    cond_func = None

                # Add trigger variables to variables
                variables = None
                if Const.CONF_TRIGGER_VARIABLES in config_block:
                    variables = core.ScriptVariables(
                        dict(config_block[Const.CONF_TRIGGER_VARIABLES].as_dict())
                    )
                if core.Const.CONF_VARIABLES in config_block:
                    if variables:
                        variables.variables.update(
                            config_block[core.Const.CONF_VARIABLES].as_dict()
                        )
                    else:
                        variables = config_block[core.Const.CONF_VARIABLES]

                entity = AutomationEntity(
                    self.domain,
                    automation_id,
                    name,
                    config_block[Const.CONF_TRIGGER],
                    cond_func,
                    action_script,
                    initial_state,
                    variables,
                    config_block.get(Const.CONF_TRIGGER_VARIABLES),
                    raw_config,
                    raw_blueprint_inputs,
                    config_block[Const.CONF_TRACE],
                )

                entities.append(entity)

        if entities:
            await component.async_add_entities(entities)

        return blueprints_used

    async def _async_get_blueprint_component(self) -> core.BlueprintComponent:
        if self._blueprint_component is None:
            self._blueprint_component = event = asyncio.Event()
            blueprint = self.controller.components.blueprint
            if isinstance(blueprint, core.BlueprintComponent):
                self._blueprint_component = blueprint
            else:
                self._blueprint_component = None
            event.set()
        else:
            evt_or_obj = self._blueprint_component
            if isinstance(evt_or_obj, asyncio.Event):
                await evt_or_obj.wait()
        return self._blueprint_component

    async def _async_get_blueprints(self) -> core.DomainBlueprintsBase:
        """Get automation blueprints."""
        if self._domain_blueprints is None:
            self._domain_blueprints = event = asyncio.Event()
            comp = await self._async_get_blueprint_component()
            if comp is not None:
                self._domain_blueprints = comp.create_domain_blueprints(
                    self.domain, Const.LOGGER
                )
            else:
                self._domain_blueprints = None
            event.set()
        return self._domain_blueprints

    def _is_on(self, entity_id: str) -> bool:
        return self._shc.states.is_state(entity_id, core.Const.STATE_ON)

    @core.callback
    def automations_with_entity(self, entity_id: str) -> list[str]:
        """Return all automations that reference the entity."""
        if self._component is None:
            return []

        return [
            automation_entity.entity_id
            for automation_entity in self._component.entities
            if entity_id in automation_entity.referenced_entities
        ]

    @core.callback
    def entities_in_automation(self, automation_entity_id: str) -> list[str]:
        """Return all entities in a scene."""
        if self._component is None:
            return []

        if (
            automation_entity := self._component.get_entity(automation_entity_id)
        ) is None:
            return []

        return list(automation_entity.referenced_entities)

    @core.callback
    def automations_with_device(self, device_id: str) -> list[str]:
        """Return all automations that reference the device."""
        if self._component is None:
            return []

        return [
            automation_entity.entity_id
            for automation_entity in self._component.entities
            if device_id in automation_entity.referenced_devices
        ]

    @core.callback
    def devices_in_automation(self, automation_entity_id: str) -> list[str]:
        """Return all devices in a scene."""
        if self._component is None:
            return []

        if (
            automation_entity := self._component.get_entity(automation_entity_id)
        ) is None:
            return []

        return list(automation_entity.referenced_devices)

    @core.callback
    def automations_with_area(self, area_id: str) -> list[str]:
        """Return all automations that reference the area."""
        if self._component is None:
            return []

        return [
            automation_entity.entity_id
            for automation_entity in self._component.entities
            if area_id in automation_entity.referenced_areas
        ]

    @core.callback
    def areas_in_automation(self, automation_entity_id: str) -> list[str]:
        """Return all areas in an automation."""
        if self._component is None:
            return []

        if (
            automation_entity := self._component.get_entity(automation_entity_id)
        ) is None:
            return []

        return list(automation_entity.referenced_areas)

    async def _async_process_if(self, name, config):
        """Process if checks."""
        if_configs = config[core.Const.CONF_CONDITION]

        checks = []
        for if_config in if_configs:
            try:
                checks.append(
                    await core.ScriptCondition.async_automation_condition_from_config(
                        self._shc, if_config
                    )
                )
            except core.SmartHomeControllerError as ex:
                Const.LOGGER.warning(f"Invalid condition: {ex}")
                return None

        def if_action(variables=None):
            """AND all conditions."""
            errors = []
            for index, check in enumerate(checks):
                try:
                    with core.Trace.path(["condition", str(index)]):
                        if not check(self._shc, variables):
                            return False
                except core.ConditionError as ex:
                    errors.append(
                        core.ConditionErrorIndex(
                            "condition", index=index, total=len(checks), error=ex
                        )
                    )

            if errors:
                Const.LOGGER.warning(
                    f"Error evaluating condition in '{name}':\n"
                    + f"{core.ConditionErrorContainer('condition', errors=errors)}",
                )
                return False

            return True

        if_action.config = if_configs

        return if_action

    async def async_reproduce_states(
        self,
        states: list[core.State],
        *,
        context: core.Context = None,
        reproduce_options: dict[str, typing.Any] = None,
    ):
        """Reproduce Automation states."""
        shc = self._shc
        domain = self.domain

        await asyncio.gather(
            *(
                _async_reproduce_state(shc, domain, state, context=context)
                for state in states
            )
        )


_VALID_STATES: typing.Final = {core.Const.STATE_ON, core.Const.STATE_OFF}


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

    # Return if we are already at the right state.
    if cur_state.state == state.state:
        return

    service_data = {core.Const.ATTR_ENTITY_ID: state.entity_id}

    if state.state == core.Const.STATE_ON:
        service = core.Const.SERVICE_TURN_ON
    elif state.state == core.Const.STATE_OFF:
        service = core.Const.SERVICE_TURN_OFF

    await shc.services.async_call(
        domain, service, service_data, context=context, blocking=True
    )
