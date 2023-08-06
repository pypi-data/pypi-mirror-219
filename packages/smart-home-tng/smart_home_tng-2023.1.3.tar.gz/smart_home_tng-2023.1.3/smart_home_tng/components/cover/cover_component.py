"""
Cover Integration for Smart Home - The Next Generation.

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
_cover: typing.TypeAlias = core.Cover
_intent: typing.TypeAlias = core.Intent

_LOGGER: typing.Final = logging.getLogger(__name__)

_CMD_ACTION_TYPES: typing.Final = {"open", "close", "stop", "open_tilt", "close_tilt"}
_POSITION_ACTION_TYPES: typing.Final = {"set_position", "set_tilt_position"}
_POSITION_CONDITION_TYPES: typing.Final = {"is_position", "is_tilt_position"}
_STATE_CONDITION_TYPES: typing.Final = {
    "is_open",
    "is_closed",
    "is_opening",
    "is_closing",
}
_POSITION_CONDITION_SCHEMA: typing.Final = vol.All(
    _cv.DEVICE_CONDITION_BASE_SCHEMA.extend(
        {
            vol.Required(core.Const.CONF_ENTITY_ID): _cv.entity_id,
            vol.Required(core.Const.CONF_TYPE): vol.In(_POSITION_CONDITION_TYPES),
            vol.Optional(core.Const.CONF_ABOVE): vol.All(
                vol.Coerce(int), vol.Range(min=0, max=100)
            ),
            vol.Optional(core.Const.CONF_BELOW): vol.All(
                vol.Coerce(int), vol.Range(min=0, max=100)
            ),
        }
    ),
    _cv.has_at_least_one_key(core.Const.CONF_BELOW, core.Const.CONF_ABOVE),
)
_STATE_CONDITION_SCHEMA: typing.Final = _cv.DEVICE_CONDITION_BASE_SCHEMA.extend(
    {
        vol.Required(core.Const.CONF_ENTITY_ID): _cv.entity_id,
        vol.Required(core.Const.CONF_TYPE): vol.In(_STATE_CONDITION_TYPES),
    }
)
_CONDITION_SCHEMA: typing.Final = vol.Any(
    _POSITION_CONDITION_SCHEMA, _STATE_CONDITION_SCHEMA
)
_POSITION_TRIGGER_TYPES: typing.Final = {"position", "tilt_position"}
_STATE_TRIGGER_TYPES: typing.Final = {"opened", "closed", "opening", "closing"}
_POSITION_TRIGGER_SCHEMA: typing.Final = vol.All(
    core.DeviceAutomation.TRIGGER_BASE_SCHEMA.extend(
        {
            vol.Required(core.Const.CONF_ENTITY_ID): _cv.entity_id,
            vol.Required(core.Const.CONF_TYPE): vol.In(_POSITION_TRIGGER_TYPES),
            vol.Optional(core.Const.CONF_ABOVE): vol.All(
                vol.Coerce(int), vol.Range(min=0, max=100)
            ),
            vol.Optional(core.Const.CONF_BELOW): vol.All(
                vol.Coerce(int), vol.Range(min=0, max=100)
            ),
        }
    ),
    _cv.has_at_least_one_key(core.Const.CONF_BELOW, core.Const.CONF_ABOVE),
)
_STATE_TRIGGER_SCHEMA: typing.Final = core.DeviceAutomation.TRIGGER_BASE_SCHEMA.extend(
    {
        vol.Required(core.Const.CONF_ENTITY_ID): _cv.entity_id,
        vol.Required(core.Const.CONF_TYPE): vol.In(_STATE_TRIGGER_TYPES),
        vol.Optional(core.Const.CONF_FOR): _cv.positive_time_period_dict,
    }
)
_TRIGGER_SCHEMA = vol.Any(_POSITION_TRIGGER_SCHEMA, _STATE_TRIGGER_SCHEMA)


# pylint: disable=unused-variable, too-many-ancestors
class CoverComponent(
    core.SmartHomeControllerComponent,
    core.ActionPlatform,
    core.ConditionPlatform,
    core.GroupPlatform,
    core.Intent.Platform,
    core.ReproduceStatePlatform,
    core.TriggerPlatform,
):
    """Support for Cover devices."""

    def __init__(self, path: typing.Iterable[str]):
        super().__init__(path)
        self._entity_component: core.EntityComponent = None
        self._supported_platforms = frozenset(
            [
                core.Platform.ACTION,
                core.Platform.CONDITION,
                core.Platform.GROUP,
                core.Platform.INTENT,
                core.Platform.REPRODUCE_STATE,
                core.Platform.TRIGGER,
            ]
        )

    @property
    def entity_component(self) -> core.EntityComponent:
        return self._entity_component

    @property
    def scan_interval(self) -> dt.timedelta:
        return dt.timedelta(seconds=15)

    async def async_setup(self, config: core.ConfigType) -> bool:
        """Track states and offer events for covers."""
        component = self._entity_component = core.EntityComponent(
            _LOGGER, self.domain, self.controller, self.scan_interval
        )

        await component.async_setup(config)

        component.async_register_entity_service(
            _cover.SERVICE_OPEN, {}, "async_open_cover", [_cover.EntityFeature.OPEN]
        )

        component.async_register_entity_service(
            _cover.SERVICE_CLOSE, {}, "async_close_cover", [_cover.EntityFeature.CLOSE]
        )

        component.async_register_entity_service(
            _cover.SERVICE_SET_POSITION,
            {
                vol.Required(_cover.ATTR_POSITION): vol.All(
                    vol.Coerce(int), vol.Range(min=0, max=100)
                )
            },
            "async_set_cover_position",
            [_cover.EntityFeature.SET_POSITION],
        )

        component.async_register_entity_service(
            _cover.SERVICE_STOP, {}, "async_stop_cover", [_cover.EntityFeature.STOP]
        )

        component.async_register_entity_service(
            _cover.SERVICE_TOGGLE,
            {},
            "async_toggle",
            [_cover.EntityFeature.OPEN | _cover.EntityFeature.CLOSE],
        )

        component.async_register_entity_service(
            _cover.SERVICE_OPEN_TILT,
            {},
            "async_open_cover_tilt",
            [_cover.EntityFeature.OPEN_TILT],
        )

        component.async_register_entity_service(
            _cover.SERVICE_CLOSE_TILT,
            {},
            "async_close_cover_tilt",
            [_cover.EntityFeature.CLOSE_TILT],
        )

        component.async_register_entity_service(
            _cover.SERVICE_STOP_TILT,
            {},
            "async_stop_cover_tilt",
            [_cover.EntityFeature.STOP_TILT],
        )

        component.async_register_entity_service(
            _cover.SERVICE_SET_TILT_POSITION,
            {
                vol.Required(_cover.ATTR_TILT_POSITION): vol.All(
                    vol.Coerce(int), vol.Range(min=0, max=100)
                )
            },
            "async_set_cover_tilt_position",
            [_cover.EntityFeature.SET_TILT_POSITION],
        )

        component.async_register_entity_service(
            _cover.SERVICE_TOGGLE_TILT,
            {},
            "async_toggle_tilt",
            [_cover.EntityFeature.OPEN_TILT | _cover.EntityFeature.CLOSE_TILT],
        )

        return True

    async def async_setup_entry(self, entry: core.ConfigEntry) -> bool:
        """Set up a config entry."""
        return await self.entity_component.async_setup_entry(entry)

    async def async_unload_entry(self, entry: core.ConfigEntry) -> bool:
        """Unload a config entry."""
        return await self.entity_component.async_unload_entry(entry)

    # ------------------- Action Platform ---------------------------

    @property
    def action_schema(self) -> typing.Callable[[core.ConfigType], core.ConfigType]:
        """Validate action configuration"""
        CMD_ACTION_SCHEMA: typing.Final = _cv.DEVICE_ACTION_BASE_SCHEMA.extend(
            {
                vol.Required(core.Const.CONF_TYPE): vol.In(_CMD_ACTION_TYPES),
                vol.Required(core.Const.CONF_ENTITY_ID): _cv.entity_domain(self.domain),
            }
        )

        POSITION_ACTION_SCHEMA: typing.Final = _cv.DEVICE_ACTION_BASE_SCHEMA.extend(
            {
                vol.Required(core.Const.CONF_TYPE): vol.In(_POSITION_ACTION_TYPES),
                vol.Required(core.Const.CONF_ENTITY_ID): _cv.entity_domain(self.domain),
                vol.Optional("position", default=0): vol.All(
                    vol.Coerce(int), vol.Range(min=0, max=100)
                ),
            }
        )

        ACTION_SCHEMA: typing.Final = vol.Any(CMD_ACTION_SCHEMA, POSITION_ACTION_SCHEMA)

        return ACTION_SCHEMA

    async def async_get_actions(
        self, device_id: str
    ) -> list[dict[str, typing.Any]] | typing.Awaitable[list[dict[str, typing.Any]]]:
        """List device actions for Cover devices."""
        registry = self.controller
        actions = []

        # Get all the integrations entities for this device
        for entry in registry.async_entries_for_device(device_id):
            if entry.domain != self.domain:
                continue

            supported_features = registry.get_supported_features(entry.entity_id)

            # Add actions for each entity that belongs to this integration
            base_action = {
                core.Const.CONF_DEVICE_ID: device_id,
                core.Const.CONF_DOMAIN: self.domain,
                core.Const.CONF_ENTITY_ID: entry.entity_id,
            }

            if supported_features & _cover.EntityFeature.SET_POSITION:
                actions.append({**base_action, core.Const.CONF_TYPE: "set_position"})
            else:
                if supported_features & _cover.EntityFeature.OPEN:
                    actions.append({**base_action, core.Const.CONF_TYPE: "open"})
                if supported_features & _cover.EntityFeature.CLOSE:
                    actions.append({**base_action, core.Const.CONF_TYPE: "close"})
                if supported_features & _cover.EntityFeature.STOP:
                    actions.append({**base_action, core.Const.CONF_TYPE: "stop"})

            if supported_features & _cover.EntityFeature.SET_TILT_POSITION:
                actions.append(
                    {**base_action, core.Const.CONF_TYPE: "set_tilt_position"}
                )
            else:
                if supported_features & _cover.EntityFeature.OPEN_TILT:
                    actions.append({**base_action, core.Const.CONF_TYPE: "open_tilt"})
                if supported_features & _cover.EntityFeature.CLOSE_TILT:
                    actions.append({**base_action, core.Const.CONF_TYPE: "close_tilt"})

        return actions

    async def async_get_action_capabilities(
        self, config: core.ConfigType
    ) -> dict[str, vol.Schema] | typing.Awaitable[dict[str, vol.Schema]]:
        """List action capabilities."""
        if config[core.Const.CONF_TYPE] not in _POSITION_ACTION_TYPES:
            return {}

        return {
            "extra_fields": vol.Schema(
                {
                    vol.Optional(_cover.ATTR_POSITION, default=0): vol.All(
                        vol.Coerce(int), vol.Range(min=0, max=100)
                    )
                }
            )
        }

    async def async_call_action_from_config(
        self,
        config: core.ConfigType,
        _variables: dict[str, typing.Any],
        context: core.Context,
    ) -> None:
        """Execute a device action."""
        service_data = {core.Const.ATTR_ENTITY_ID: config[core.Const.CONF_ENTITY_ID]}

        action = config[core.Const.CONF_TYPE]
        if action == "open":
            service = _cover.SERVICE_OPEN
        elif action == "close":
            service = _cover.SERVICE_CLOSE
        elif action == "stop":
            service = _cover.SERVICE_STOP
        elif action == "open_tilt":
            service = _cover.SERVICE_OPEN_TILT
        elif action == "close_tilt":
            service = _cover.SERVICE_CLOSE_TILT
        elif action == "set_position":
            service = _cover.SERVICE_SET_POSITION
            service_data[_cover.ATTR_POSITION] = config[_cover.ATTR_POSITION]
        elif action == "set_tilt_position":
            service = _cover.SERVICE_SET_TILT_POSITION
            service_data[_cover.ATTR_TILT_POSITION] = config["position"]

        await self.controller.services.async_call(
            self.domain, service, service_data, blocking=True, context=context
        )

    # ------------------- Condition Platform ---------------------------

    @property
    def condition_schema(self) -> typing.Callable[[core.ConfigType], core.ConfigType]:
        return _CONDITION_SCHEMA

    async def async_get_conditions(self, device_id: str) -> list[dict[str, typing.Any]]:
        """List device conditions for Cover devices."""
        registry = self.controller.entity_registry
        conditions: list[dict[str, str]] = []

        # Get all the integrations entities for this device
        for entry in registry.async_entries_for_device(device_id):
            if entry.domain != self.domain:
                continue

            supported_features = registry.get_supported_features(entry.entity_id)
            supports_open_close = supported_features & (
                _cover.EntityFeature.OPEN | _cover.EntityFeature.CLOSE
            )

            # Add conditions for each entity that belongs to this integration
            base_condition = {
                core.Const.CONF_CONDITION: "device",
                core.Const.CONF_DEVICE_ID: device_id,
                core.Const.CONF_DOMAIN: self.domain,
                core.Const.CONF_ENTITY_ID: entry.entity_id,
            }

            if supports_open_close:
                conditions += [
                    {**base_condition, core.Const.CONF_TYPE: cond}
                    for cond in _STATE_CONDITION_TYPES
                ]
            if supported_features & _cover.EntityFeature.SET_POSITION:
                conditions.append(
                    {**base_condition, core.Const.CONF_TYPE: "is_position"}
                )
            if supported_features & _cover.EntityFeature.SET_TILT_POSITION:
                conditions.append(
                    {**base_condition, core.Const.CONF_TYPE: "is_tilt_position"}
                )

        return conditions

    async def async_condition_from_config(
        self, config: core.ConfigType
    ) -> core.ConditionCheckerType:
        """Create a function to test a device condition."""
        cond_type = config[core.Const.CONF_TYPE]
        if cond_type in _STATE_CONDITION_TYPES:
            if cond_type == "is_open":
                state = _cover.STATE_OPEN
            elif cond_type == "is_closed":
                state = _cover.STATE_CLOSED
            elif cond_type == "is_opening":
                state = _cover.STATE_OPENING
            elif cond_type == "is_closing":
                state = _cover.STATE_CLOSING

            def test_is_state(
                _shc: core.SmartHomeController, _variables: core.TemplateVarsType
            ) -> bool:
                """Test if an entity is a certain state."""
                return self.state(config[core.Const.ATTR_ENTITY_ID], state)

            return test_is_state

        if cond_type == "is_position":
            position_attr = "current_position"
        else:
            position_attr = "current_tilt_position"
        min_pos = config.get(core.Const.CONF_ABOVE)
        max_pos = config.get(core.Const.CONF_BELOW)

        @core.callback
        def check_numeric_state(
            _shc: core.SmartHomeController, _variables: core.TemplateVarsType = None
        ) -> bool:
            """Return whether the criteria are met."""
            return self.async_numeric_state(
                config[core.Const.ATTR_ENTITY_ID],
                max_pos,
                min_pos,
                attribute=position_attr,
            )

        return check_numeric_state

    async def async_get_condition_capabilities(
        self, config: core.ConfigType
    ) -> dict[str, vol.Schema]:
        """List condition capabilities."""
        if config[core.Const.CONF_TYPE] not in ["is_position", "is_tilt_position"]:
            return {}

        return {
            "extra_fields": vol.Schema(
                {
                    vol.Optional(core.Const.CONF_ABOVE, default=0): vol.All(
                        vol.Coerce(int), vol.Range(min=0, max=100)
                    ),
                    vol.Optional(core.Const.CONF_BELOW, default=100): vol.All(
                        vol.Coerce(int), vol.Range(min=0, max=100)
                    ),
                }
            )
        }

    # ------------------- Group Platform ---------------------------

    @core.callback
    def async_describe_on_off_states(
        self, registry: core.GroupIntegrationRegistry
    ) -> None:
        """Describe group on off states."""
        # On means open, Off means closed
        registry.on_off_states({_cover.STATE_OPEN}, _cover.STATE_CLOSED)

    # -------------------- Intent Platform ----------------------------

    async def async_setup_intents(self) -> None:
        """Set up the cover intents."""
        self.controller.intents.register_handler(
            _intent.ServiceHandler(
                _cover.INTENT_OPEN_COVER,
                self.domain,
                _const.SERVICE_OPEN_COVER,
                "Opened {}",
            ),
        )
        self.controller.intents.register_handler(
            _intent.ServiceHandler(
                _cover.INTENT_CLOSE_COVER,
                self.domain,
                _const.SERVICE_CLOSE_COVER,
                "Closed {}",
            ),
        )

    # ---------------- Reproduce State Platform -----------------------

    async def async_reproduce_states(
        self,
        states: list[core.State],
        *,
        context: core.Context = None,
        reproduce_options: dict[str, typing.Any] = None,
    ):
        """Reproduce Cover states."""
        # Reproduce states in parallel.
        await asyncio.gather(
            *(_async_reproduce_state(self, state, context=context) for state in states)
        )

    # ------------------- Trigger Platform ---------------------------

    @property
    def trigger_schema(self) -> typing.Callable[[core.ConfigType], core.ConfigType]:
        return _TRIGGER_SCHEMA

    async def async_get_triggers(
        self, device_id: str
    ) -> list[dict[str, typing.Any]] | typing.Awaitable[list[dict[str, typing.Any]]]:
        """List device triggers for Cover devices."""
        registry = self.controller.entity_registry
        triggers = []

        # Get all the integrations entities for this device
        for entry in registry.async_entries_for_device(device_id):
            if entry.domain != self.domain:
                continue

            supported_features = registry.get_supported_features(entry.entity_id)
            supports_open_close = supported_features & (
                _cover.EntityFeature.OPEN | _cover.EntityFeature.CLOSE
            )

            # Add triggers for each entity that belongs to this integration
            base_trigger = {
                core.Const.CONF_PLATFORM: "device",
                core.Const.CONF_DEVICE_ID: device_id,
                core.Const.CONF_DOMAIN: self.domain,
                core.Const.CONF_ENTITY_ID: entry.entity_id,
            }

            if supports_open_close:
                triggers += [
                    {
                        **base_trigger,
                        core.Const.CONF_TYPE: trigger,
                    }
                    for trigger in _STATE_TRIGGER_TYPES
                ]
            if supported_features & _cover.EntityFeature.SET_POSITION:
                triggers.append(
                    {
                        **base_trigger,
                        core.Const.CONF_TYPE: "position",
                    }
                )
            if supported_features & _cover.EntityFeature.SET_TILT_POSITION:
                triggers.append(
                    {
                        **base_trigger,
                        core.Const.CONF_TYPE: "tilt_position",
                    }
                )

        return triggers

    async def async_get_trigger_capabilities(
        self, config: core.ConfigType
    ) -> dict[str, vol.Schema] | typing.Awaitable[dict[str, vol.Schema]]:
        """List trigger capabilities."""
        if config[core.Const.CONF_TYPE] not in _POSITION_TRIGGER_TYPES:
            return {
                "extra_fields": vol.Schema(
                    {vol.Optional(core.Const.CONF_FOR): _cv.positive_time_period_dict}
                )
            }

        return {
            "extra_fields": vol.Schema(
                {
                    vol.Optional(core.Const.CONF_ABOVE, default=0): vol.All(
                        vol.Coerce(int), vol.Range(min=0, max=100)
                    ),
                    vol.Optional(core.Const.CONF_BELOW, default=100): vol.All(
                        vol.Coerce(int), vol.Range(min=0, max=100)
                    ),
                }
            )
        }

    async def async_attach_trigger(
        self,
        config: core.ConfigType,
        action: core.TriggerActionType,
        trigger_info: core.TriggerInfo,
    ) -> core.CallbackType:
        """Attach a trigger."""
        trigger_type = config[core.Const.CONF_TYPE]
        if trigger_type in _STATE_TRIGGER_TYPES:
            if trigger_type == "opened":
                to_state = _cover.STATE_OPEN
            elif trigger_type == "closed":
                to_state = _cover.STATE_CLOSED
            elif trigger_type == "opening":
                to_state = _cover.STATE_OPENING
            elif trigger_type == "closing":
                to_state = _cover.STATE_CLOSING

            state_config = {
                core.Const.CONF_PLATFORM: "state",
                core.Const.CONF_ENTITY_ID: config[core.Const.CONF_ENTITY_ID],
                core.Const.CONF_TO: to_state,
            }
            if core.Const.CONF_FOR in config:
                state_config[core.Const.CONF_FOR] = config[core.Const.CONF_FOR]
            state_config = await core.Trigger.async_validate_trigger_config(
                state_config
            )
            return await core.Trigger.async_attach_state_trigger(
                self._shc, state_config, action, trigger_info, platform_type="device"
            )

        if config[core.Const.CONF_TYPE] == "position":
            position = "current_position"
        if config[core.Const.CONF_TYPE] == "tilt_position":
            position = "current_tilt_position"
        min_pos = config.get(core.Const.CONF_ABOVE, -1)
        max_pos = config.get(core.Const.CONF_BELOW, 101)
        value_template = f"{{{{ state.attributes.{position} }}}}"

        numeric_state_config = {
            core.Const.CONF_PLATFORM: "numeric_state",
            core.Const.CONF_ENTITY_ID: config[core.Const.CONF_ENTITY_ID],
            core.Const.CONF_BELOW: max_pos,
            core.Const.CONF_ABOVE: min_pos,
            core.Const.CONF_VALUE_TEMPLATE: value_template,
        }
        numeric_state_config = await core.Trigger.async_validate_trigger_config(
            numeric_state_config
        )
        return await core.Trigger.async_attach_numeric_state_trigger(
            self._shc,
            numeric_state_config,
            action,
            trigger_info,
            platform_type="device",
        )


_VALID_STATES: typing.Final = {
    _cover.STATE_CLOSED,
    _cover.STATE_CLOSING,
    _cover.STATE_OPEN,
    _cover.STATE_OPENING,
}


async def _async_reproduce_state(
    cover: CoverComponent,
    state: core.State,
    *,
    context: core.Context = None,
) -> None:
    """Reproduce a single state."""
    if (cur_state := cover.controller.states.get(state.entity_id)) is None:
        _LOGGER.warning(f"Unable to find entity {state.entity_id}")
        return

    if state.state not in _VALID_STATES:
        _LOGGER.warning(f"Invalid state specified for {state.entity_id}: {state.state}")
        return

    # Return if we are already at the right state.
    if (
        cur_state.state == state.state
        and cur_state.attributes.get(_cover.ATTR_CURRENT_POSITION)
        == state.attributes.get(_cover.ATTR_CURRENT_POSITION)
        and cur_state.attributes.get(_cover.ATTR_CURRENT_TILT_POSITION)
        == state.attributes.get(_cover.ATTR_CURRENT_TILT_POSITION)
    ):
        return

    service_data = {core.Const.ATTR_ENTITY_ID: state.entity_id}
    service_data_tilting = {core.Const.ATTR_ENTITY_ID: state.entity_id}

    if not (
        cur_state.state == state.state
        and cur_state.attributes.get(_cover.ATTR_CURRENT_POSITION)
        == state.attributes.get(_cover.ATTR_CURRENT_POSITION)
    ):
        # Open/Close
        if state.state in [_cover.STATE_CLOSED, _cover.STATE_CLOSING]:
            service = _cover.SERVICE_CLOSE
        elif state.state in [_cover.STATE_OPEN, _cover.STATE_OPENING]:
            if (
                _cover.ATTR_CURRENT_POSITION in cur_state.attributes
                and _cover.ATTR_CURRENT_POSITION in state.attributes
            ):
                service = _cover.SERVICE_SET_POSITION
                service_data[_cover.ATTR_POSITION] = state.attributes[
                    _cover.ATTR_CURRENT_POSITION
                ]
            else:
                service = _cover.SERVICE_OPEN

        await cover.controller.services.async_call(
            cover.domain, service, service_data, context=context, blocking=True
        )

    if (
        _cover.ATTR_CURRENT_TILT_POSITION in state.attributes
        and _cover.ATTR_CURRENT_TILT_POSITION in cur_state.attributes
        and cur_state.attributes.get(_cover.ATTR_CURRENT_TILT_POSITION)
        != state.attributes.get(_cover.ATTR_CURRENT_TILT_POSITION)
    ):
        # Tilt position
        if state.attributes.get(_cover.ATTR_CURRENT_TILT_POSITION) == 100:
            service_tilting = _cover.SERVICE_OPEN_TILT
        elif state.attributes.get(_cover.ATTR_CURRENT_TILT_POSITION) == 0:
            service_tilting = _cover.SERVICE_CLOSE_TILT
        else:
            service_tilting = _cover.SERVICE_SET_TILT_POSITION
            service_data_tilting[_cover.ATTR_TILT_POSITION] = state.attributes[
                _cover.ATTR_CURRENT_TILT_POSITION
            ]

        await cover.controller.services.async_call(
            cover.domain,
            service_tilting,
            service_data_tilting,
            context=context,
            blocking=True,
        )
