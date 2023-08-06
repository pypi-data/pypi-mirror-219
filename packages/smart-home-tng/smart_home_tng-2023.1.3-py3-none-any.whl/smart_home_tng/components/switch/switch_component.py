"""
Switch Component for Smart Home - The Next Generation.

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
from .light_switch import LightSwitch

_cv: typing.TypeAlias = core.ConfigValidation

_LOGGER: typing.Final = logging.getLogger(__name__)
_DEFAULT_LIGHT_NAME: typing.Final = "Light Switch"


# pylint: disable=unused-variable, too-many-ancestors
class SwitchComponent(
    core.SmartHomeControllerComponent,
    core.ActionPlatform,
    core.ConditionPlatform,
    core.GroupPlatform,
    core.ReproduceStatePlatform,
    core.SignificantChangePlatform,
    core.TriggerPlatform,
):
    """Component to interface with switches that can be controlled remotely."""

    def __init__(self, path: typing.Iterable[str]):
        super().__init__(path)
        self._entity_component: core.EntityComponent = None
        self._supported_platforms = frozenset(
            [
                core.Platform.ACTION,
                core.Platform.CONDITION,
                core.Platform.GROUP,
                core.Platform.LIGHT,
                core.Platform.REPRODUCE_STATE,
                core.Platform.SIGNIFICANT_CHANGE,
                core.Platform.TRIGGER,
            ]
        )

    @property
    def entity_component(self) -> core.EntityComponent:
        return self._entity_component

    @property
    def scan_interval(self) -> dt.timedelta:
        return dt.timedelta(seconds=30)

    def _is_on(self, entity_id: str) -> bool:
        """Return if the switch is on based on the statemachine.

        Async friendly.
        """
        return self.controller.states.is_state(entity_id, core.Const.STATE_ON)

    async def async_setup(self, config: core.ConfigType) -> bool:
        """Track states and offer events for switches."""
        if not await super().async_setup(config):
            return False

        component = self._entity_component = core.EntityComponent(
            _LOGGER, self.domain, self.controller, self.scan_interval
        )
        await component.async_setup(config)

        component.async_register_entity_service(
            core.Const.SERVICE_TURN_OFF, {}, "async_turn_off"
        )
        component.async_register_entity_service(
            core.Const.SERVICE_TURN_ON, {}, "async_turn_on"
        )
        component.async_register_entity_service(
            core.Const.SERVICE_TOGGLE, {}, "async_toggle"
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

    # --------------------- Action Platform ----------------------------

    @property
    def action_schema(self) -> typing.Callable[[core.ConfigType], core.ConfigType]:
        return core.Toggle.ACTION_SCHEMA.extend(
            {vol.Required(core.Const.CONF_DOMAIN): self.domain}
        )

    async def async_call_action_from_config(
        self,
        config: core.ConfigType,
        variables: dict[str, typing.Any],
        context: core.Context,
    ) -> None:
        """Change state based on configuration."""
        await core.Toggle.async_call_action_from_config(
            self.controller, config, variables, context, self.domain
        )

    async def async_get_actions(
        self, device_id: str
    ) -> list[dict[str, typing.Any]] | typing.Awaitable[list[dict[str, typing.Any]]]:
        """List device actions."""
        return await core.Toggle.async_get_actions(
            self.controller, device_id, self.domain
        )

    # --------------------- Condition Platform ----------------------------

    @property
    def condition_schema(self) -> typing.Callable[[core.ConfigType], core.ConfigType]:
        CONDITION_SCHEMA: typing.Final = core.Toggle.CONDITION_SCHEMA.extend(
            {vol.Required(core.Const.CONF_DOMAIN): self.domain}
        )
        return CONDITION_SCHEMA

    async def async_condition_from_config(
        self, config: core.ConfigType
    ) -> core.ConditionCheckerType:
        """Evaluate state based on configuration."""
        return await core.Toggle.async_condition_from_config(self.controller, config)

    async def async_get_conditions(self, device_id: str) -> list[dict[str, str]]:
        """List device conditions."""
        return await core.Toggle.async_get_conditions(
            self.controller, device_id, self.domain
        )

    async def async_get_condition_capabilities(
        self, config: core.ConfigType
    ) -> dict[str, vol.Schema]:
        """List condition capabilities."""
        return await core.Toggle.async_get_condition_capabilities(
            self.controller, config
        )

    # --------------------- Group Platform ----------------------------

    @core.callback
    def async_describe_on_off_states(
        self, registry: core.GroupIntegrationRegistry
    ) -> None:
        """Describe group on off states."""
        registry.on_off_states({core.Const.STATE_ON}, core.Const.STATE_OFF)

    # --------------------- Light Platform ----------------------------

    @property
    def _light_platform_schema(self):
        """Validate platform configuration."""
        PLATFORM_SCHEMA: typing.Final = core.Light.PLATFORM_SCHEMA.extend(
            {
                vol.Optional(
                    core.Const.CONF_NAME, default=_DEFAULT_LIGHT_NAME
                ): _cv.string,
                vol.Required(core.Const.CONF_ENTITY_ID): _cv.entity_domain(self.domain),
            }
        )
        return PLATFORM_SCHEMA

    async def async_setup_platform(
        self,
        platform_config: core.ConfigType,
        add_entities: core.AddEntitiesCallback,
        _discovery_info: core.DiscoveryInfoType,
    ):
        """Initialize Light Switch platform."""
        entities = []
        registry = self.controller.entity_registry
        if self._current_platform == core.Platform.LIGHT:
            # TODO: Allgemeingültiger implementieren
            platform_config = self._light_platform_schema(platform_config)
            wrapped_switch = registry.async_get(
                platform_config[core.Const.CONF_ENTITY_ID]
            )
            unique_id = wrapped_switch.unique_id if wrapped_switch else None
            entities.append(
                LightSwitch(
                    self,
                    platform_config[core.Const.CONF_NAME],
                    platform_config[core.Const.CONF_ENTITY_ID],
                    unique_id,
                )
            )

        if entities:
            add_entities(entities)

    # ------------------ Reproduce State Platform -------------------------

    async def async_reproduce_states(
        self,
        states: list[core.State],
        *,
        context: core.Context = None,
        reproduce_options: dict[str, typing.Any] = None,
    ):
        """Reproduce Switch states."""
        await asyncio.gather(
            *(
                _async_reproduce_state(
                    self,
                    state,
                    context=context,
                )
                for state in states
            )
        )

    # ------------------ Significant Change Platform -------------------------

    @core.callback
    def check_significant_change(
        self,
        old_state: str,
        _old_attrs: dict,
        new_state: str,
        _new_attrs: dict,
        **_kwargs: typing.Any,
    ) -> bool:
        """Test if state significantly changed."""
        return old_state != new_state

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

    async def async_get_triggers(self, device_id: str) -> list[dict[str, str]]:
        """List device triggers."""
        return await core.Toggle.async_get_triggers(
            self.controller, device_id, self.domain
        )

    async def async_get_trigger_capabilities(
        self, config: core.ConfigType
    ) -> dict[str, vol.Schema]:
        """List trigger capabilities."""
        return await core.Toggle.async_get_trigger_capabilities(config)


_VALID_STATES: typing.Final = {core.Const.STATE_ON, core.Const.STATE_OFF}


async def _async_reproduce_state(
    switch: SwitchComponent,
    state: core.State,
    *,
    context: core.Context = None,
) -> None:
    """Reproduce a single state."""
    if (cur_state := switch.controller.states.get(state.entity_id)) is None:
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

    await switch.services.async_call(
        switch.domain, service, service_data, context=context, blocking=True
    )
