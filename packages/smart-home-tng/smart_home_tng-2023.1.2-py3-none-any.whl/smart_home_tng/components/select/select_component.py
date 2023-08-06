"""
Select Component for Smart Home - The Next Generation.

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
_const: typing.TypeAlias = core.Const
_select: typing.TypeAlias = core.Select

_LOGGER: typing.Final = logging.getLogger(__name__)
_SCAN_INTERVAL: typing.Final = dt.timedelta(seconds=30)
_ACTION_TYPES: typing.Final = {"select_option"}
_CONDITION_TYPES: typing.Final = {"selected_option"}
_TRIGGER_TYPES: typing.Final = {"current_option_changed"}


# pylint: disable=unused-variable, too-many-ancestors
class SelectComponent(
    core.SmartHomeControllerComponent,
    core.ActionPlatform,
    core.ConditionPlatform,
    core.RecorderPlatform,
    core.ReproduceStatePlatform,
    core.SignificantChangePlatform,
    core.TriggerPlatform,
):
    """Component to allow selecting an option from a list as platforms."""

    def __init__(self, path: typing.Iterable[str]):
        super().__init__(path)
        self._entities: core.EntityComponent = None
        self._supported_platforms = frozenset(
            [
                core.Platform.ACTION,
                core.Platform.CONDITION,
                core.Platform.RECORDER,
                core.Platform.REPRODUCE_STATE,
                core.Platform.SIGNIFICANT_CHANGE,
                core.Platform.TRIGGER,
            ]
        )

    @property
    def scan_interval(self) -> dt.timedelta:
        return _SCAN_INTERVAL

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

    async def async_setup(self, config: core.ConfigType) -> bool:
        """Set up Select entities."""
        if not await super().async_setup(config):
            return False

        component = self._entities = core.EntityComponent(
            _LOGGER, self.domain, self.controller, self.scan_interval
        )
        await component.async_setup(config)

        component.async_register_entity_service(
            core.Select.SERVICE_SELECT_OPTION,
            {vol.Required(core.Select.ATTR_OPTION): _cv.string},
            _async_select_option,
        )
        return True

    async def async_setup_entry(self, entry: core.ConfigEntry) -> bool:
        """Set up a config entry."""
        return await self.entity_component.async_setup_entry(entry)

    async def async_unload_entry(self, entry: core.ConfigEntry) -> bool:
        return await self.entity_component.async_unload_entry(entry)

    # --------------------- Action Platform ---------------------------

    @property
    def action_schema(self) -> typing.Callable[[core.ConfigType], core.ConfigType]:
        return _cv.DEVICE_ACTION_BASE_SCHEMA.extend(
            {
                vol.Required(_const.CONF_TYPE): vol.In(_ACTION_TYPES),
                vol.Required(_const.CONF_ENTITY_ID): _cv.entity_domain(self.domain),
                vol.Required(_select.CONF_OPTION): str,
            }
        )

    async def async_get_actions(self, device_id: str) -> list[dict[str, str]]:
        """List device actions for Select devices."""
        registry = self.controller.entity_registry
        return [
            {
                _const.CONF_DEVICE_ID: device_id,
                _const.CONF_DOMAIN: self.domain,
                _const.CONF_ENTITY_ID: entry.entity_id,
                _const.CONF_TYPE: "select_option",
            }
            for entry in registry.async_entries_for_device(device_id)
            if entry.domain == self.domain
        ]

    async def async_call_action_from_config(
        self,
        config: core.ConfigType,
        _variables: dict[str, typing.Any],
        context: core.Context,
    ) -> None:
        """Execute a device action."""
        await self.controller.services.async_call(
            self.domain,
            _select.SERVICE_SELECT_OPTION,
            {
                _const.ATTR_ENTITY_ID: config[_const.CONF_ENTITY_ID],
                _select.ATTR_OPTION: config[_select.CONF_OPTION],
            },
            blocking=True,
            context=context,
        )

    async def async_get_action_capabilities(
        self, config: core.ConfigType
    ) -> dict[str, vol.Schema]:
        """List action capabilities."""
        try:
            options = (
                self.controller.entity_registry.get_capability(
                    config[_const.CONF_ENTITY_ID], _select.ATTR_OPTIONS
                )
                or []
            )
        except core.SmartHomeControllerError:
            options = []

        return {
            "extra_fields": vol.Schema(
                {vol.Required(_select.CONF_OPTION): vol.In(options)}
            )
        }

    # ----------------------- Condition Platform -------------------------

    @property
    def condition_schema(self) -> typing.Callable[[core.ConfigType], core.ConfigType]:
        return _cv.DEVICE_CONDITION_BASE_SCHEMA.extend(
            {
                vol.Required(_const.CONF_ENTITY_ID): _cv.entity_id,
                vol.Required(_const.CONF_TYPE): vol.In(_CONDITION_TYPES),
                vol.Required(_select.CONF_OPTION): str,
                vol.Optional(_const.CONF_FOR): _cv.positive_time_period_dict,
            }
        )

    async def async_get_conditions(self, device_id: str) -> list[dict[str, str]]:
        """List device conditions for Select devices."""
        registry = self.controller.entity_registry
        return [
            {
                _const.CONF_CONDITION: "device",
                _const.CONF_DEVICE_ID: device_id,
                _const.CONF_DOMAIN: self.domain,
                _const.CONF_ENTITY_ID: entry.entity_id,
                _const.CONF_TYPE: "selected_option",
            }
            for entry in registry.async_entries_for_device(device_id)
            if entry.domain == self.domain
        ]

    async def async_condition_from_config(
        self, config: core.ConfigType
    ) -> core.ConditionCheckerType:
        """Create a function to test a device condition."""

        @core.callback
        def test_is_state(
            _shc: core.SmartHomeController, _variables: core.TemplateVarsType
        ) -> bool:
            """Test if an entity is a certain state."""
            return self.state(
                config[_const.CONF_ENTITY_ID],
                config[_select.CONF_OPTION],
                config.get(_const.CONF_FOR),
            )

        return test_is_state

    async def async_get_condition_capabilities(
        self, config: core.ConfigType
    ) -> dict[str, vol.Schema]:
        """List condition capabilities."""
        try:
            options = (
                self.controller.get_capability(
                    config[_const.CONF_ENTITY_ID], _select.ATTR_OPTIONS
                )
                or []
            )
        except core.SmartHomeControllerError:
            options = []

        return {
            "extra_fields": vol.Schema(
                {
                    vol.Required(_select.CONF_OPTION): vol.In(options),
                    vol.Optional(_const.CONF_FOR): _cv.positive_time_period_dict,
                }
            )
        }

    # ------------------------ Recorder Platform -----------------------------

    def exclude_attributes(self) -> set[str]:
        """Exclude static attributes from being recorded in the database."""
        return {_select.ATTR_OPTIONS}

    # ---------------------- Reproduce State Platform -------------------------

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

        if state.state not in cur_state.attributes.get(_select.ATTR_OPTIONS, []):
            _LOGGER.warning(
                f"Invalid state specified for {state.entity_id}: {state.state}"
            )
            return

        # Return if we are already at the right state.
        if cur_state.state == state.state:
            return

        await self.controller.services.async_call(
            self.domain,
            _select.SERVICE_SELECT_OPTION,
            {_const.ATTR_ENTITY_ID: state.entity_id, _select.ATTR_OPTION: state.state},
            context=context,
            blocking=True,
        )

    # pylint: disable=unused-argument
    async def async_reproduce_states(
        self,
        states: list[core.State],
        *,
        context: core.Context = None,
        reproduce_options: dict[str, typing.Any] = None,
    ):
        """Reproduce multiple select states."""
        await asyncio.gather(
            *(self._async_reproduce_state(state, context=context) for state in states)
        )

    # ------------------- Significant Change Platform ------------------------------

    def check_significant_change(
        self,
        old_state: str,
        old_attrs: dict,
        new_state: str,
        new_attrs: dict,
        **kwargs: typing.Any,
    ) -> bool:
        """Test if state significantly changed."""
        return old_state != new_state

    # ----------------------- Trigger Platform ---------------------------------------

    @property
    def trigger_schema(self) -> typing.Callable[[core.ConfigType], core.ConfigType]:
        return _cv.DEVICE_TRIGGER_BASE_SCHEMA.extend(
            {
                vol.Required(_const.CONF_ENTITY_ID): _cv.entity_id,
                vol.Required(_const.CONF_TYPE): vol.In(_TRIGGER_TYPES),
                vol.Optional(_const.CONF_TO): vol.Any(vol.Coerce(str)),
                vol.Optional(_const.CONF_FROM): vol.Any(vol.Coerce(str)),
                vol.Optional(_const.CONF_FOR): _cv.positive_time_period_dict,
            }
        )

    async def async_get_triggers(self, device_id: str) -> list[dict[str, str]]:
        """List device triggers for Select devices."""
        registry = self.controller.entity_registry
        return [
            {
                _const.CONF_PLATFORM: "device",
                _const.CONF_DEVICE_ID: device_id,
                _const.CONF_DOMAIN: self.domain,
                _const.CONF_ENTITY_ID: entry.entity_id,
                _const.CONF_TYPE: "current_option_changed",
            }
            for entry in registry.async_entries_for_device(device_id)
            if entry.domain == self.domain
        ]

    async def async_attach_trigger(
        self,
        config: core.ConfigType,
        action: core.TriggerActionType,
        trigger_info: core.TriggerInfo,
    ) -> core.CallbackType:
        """Attach a trigger."""
        state_config = {
            _const.CONF_PLATFORM: "state",
            _const.CONF_ENTITY_ID: config[_const.CONF_ENTITY_ID],
        }

        if _const.CONF_TO in config:
            state_config[_const.CONF_TO] = config[_const.CONF_TO]

        if _const.CONF_FROM in config:
            state_config[_const.CONF_FROM] = config[_const.CONF_FROM]

        if _const.CONF_FOR in config:
            state_config[_const.CONF_FOR] = config[_const.CONF_FOR]

        state_config = await core.Trigger.async_validate_trigger_config(state_config)
        return await core.Trigger.async_attach_state_trigger(
            self.controller, state_config, action, trigger_info, platform_type="device"
        )

    async def async_get_trigger_capabilities(
        self, config: core.ConfigType
    ) -> dict[str, vol.Schema]:
        """List trigger capabilities."""
        try:
            options = (
                self.controller.entity_registry.get_capability(
                    config[_const.CONF_ENTITY_ID], _select.ATTR_OPTIONS
                )
                or []
            )
        except core.SmartHomeControllerError:
            options = []

        return {
            "extra_fields": vol.Schema(
                {
                    vol.Optional(_const.CONF_FROM): vol.In(options),
                    vol.Optional(_const.CONF_TO): vol.In(options),
                    vol.Optional(_const.CONF_FOR): _cv.positive_time_period_dict,
                }
            )
        }


async def _async_select_option(
    entity: core.Select.Entity, service_call: core.ServiceCall
) -> None:
    """Service call wrapper to set a new value."""
    option = service_call.data[core.Select.ATTR_OPTION]
    if option not in entity.options:
        raise ValueError(f"Option {option} not valid for {entity.name}")
    await entity.async_select_option(option)
