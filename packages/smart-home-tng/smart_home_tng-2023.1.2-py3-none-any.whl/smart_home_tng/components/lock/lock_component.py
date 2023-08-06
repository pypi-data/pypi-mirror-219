"""
Lock Component for Smart Home - The Next Generation.

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
_ACTION_TYPES: typing.Final = {"lock", "unlock", "open"}
_CONDITION_TYPES: typing.Final = {
    "is_locked",
    "is_unlocked",
    "is_locking",
    "is_unlocking",
    "is_jammed",
}
_CONDITION_SCHEMA: typing.Final = _cv.DEVICE_CONDITION_BASE_SCHEMA.extend(
    {
        vol.Required(core.Const.CONF_ENTITY_ID): _cv.entity_id,
        vol.Required(core.Const.CONF_TYPE): vol.In(_CONDITION_TYPES),
    }
)
_VALID_STATES: typing.Final = {
    core.Const.STATE_LOCKED,
    core.Const.STATE_UNLOCKED,
    core.Const.STATE_LOCKING,
    core.Const.STATE_UNLOCKING,
}
_TRIGGER_TYPES: typing.Final = {"locked", "unlocked", "locking", "unlocking", "jammed"}
_TRIGGER_SCHEMA: typing.Final = _cv.DEVICE_TRIGGER_BASE_SCHEMA.extend(
    {
        vol.Required(core.Const.CONF_ENTITY_ID): _cv.entity_id,
        vol.Required(core.Const.CONF_TYPE): vol.In(_TRIGGER_TYPES),
        vol.Optional(core.Const.CONF_FOR): _cv.positive_time_period_dict,
    }
)


# pylint: disable=unused-variable, too-many-ancestors
class LockComponent(
    core.SmartHomeControllerComponent,
    core.ActionPlatform,
    core.ConditionPlatform,
    core.GroupPlatform,
    core.ReproduceStatePlatform,
    core.SignificantChangePlatform,
    core.TriggerPlatform,
):
    """Component to interface with locks that can be controlled remotely."""

    def __init__(self, path: typing.Iterable[str]):
        super().__init__(path)
        self._entities: core.EntityPlatform = None
        self._supported_platforms = frozenset(
            [
                core.Platform.ACTION,
                core.Platform.CONDITION,
                core.Platform.GROUP,
                core.Platform.REPRODUCE_STATE,
                core.Platform.SIGNIFICANT_CHANGE,
                core.Platform.TRIGGER,
            ]
        )

    @property
    def entity_component(self) -> core.EntityComponent:
        return self._entities

    @property
    def scan_interval(self) -> dt.timedelta:
        return core.Lock.SCAN_INTERVAL

    async def async_setup(self, config: core.ConfigType) -> bool:
        """Track states and offer events for locks."""
        component = self._entities = core.EntityComponent(
            _LOGGER, self.domain, self.controller, self.scan_interval
        )

        await component.async_setup(config)

        component.async_register_entity_service(
            core.Const.SERVICE_UNLOCK, core.Lock.LOCK_SERVICE_SCHEMA, "async_unlock"
        )
        component.async_register_entity_service(
            core.Const.SERVICE_LOCK, core.Lock.LOCK_SERVICE_SCHEMA, "async_lock"
        )
        component.async_register_entity_service(
            core.Const.SERVICE_OPEN, core.Lock.LOCK_SERVICE_SCHEMA, "async_open"
        )

        return True

    async def async_setup_entry(self, entry: core.ConfigEntry) -> bool:
        """Set up a config entry."""
        component = self._entities
        return await component.async_setup_entry(entry)

    async def async_unload_entry(self, entry: core.ConfigEntry) -> bool:
        """Unload a config entry."""
        component = self._entities
        return await component.async_unload_entry(entry)

    # ----------------------- Action Platform ----------------------------

    @property
    def action_schema(self) -> typing.Callable[[core.ConfigType], core.ConfigType]:
        ACTION_SCHEMA: typing.Final = _cv.DEVICE_ACTION_BASE_SCHEMA.extend(
            {
                vol.Required(core.Const.CONF_TYPE): vol.In(_ACTION_TYPES),
                vol.Required(core.Const.CONF_ENTITY_ID): _cv.entity_domain(self.domain),
            }
        )
        return ACTION_SCHEMA

    async def async_get_actions(self, device_id: str) -> list[dict[str, str]]:
        """List device actions for Lock devices."""
        registry = self.controller.entity_registry
        actions = []

        # Get all the integrations entities for this device
        for entry in registry.async_entries_for_device(registry, device_id):
            if entry.domain != self.domain:
                continue

            supported_features = registry.get_supported_features(entry.entity_id)

            # Add actions for each entity that belongs to this integration
            base_action = {
                core.Const.CONF_DEVICE_ID: device_id,
                core.Const.CONF_DOMAIN: self.domain,
                core.Const.CONF_ENTITY_ID: entry.entity_id,
            }

            actions.append({**base_action, core.Const.CONF_TYPE: "lock"})
            actions.append({**base_action, core.Const.CONF_TYPE: "unlock"})

            if supported_features & (core.Lock.EntityFeature.OPEN):
                actions.append({**base_action, core.Const.CONF_TYPE: "open"})

        return actions

    async def async_call_action_from_config(
        self,
        config: core.ConfigType,
        _variables: dict[str, typing.Any],
        context: core.Context,
    ) -> None:
        """Execute a device action."""
        service_data = {core.Const.ATTR_ENTITY_ID: config[core.Const.CONF_ENTITY_ID]}

        if config[core.Const.CONF_TYPE] == "lock":
            service = core.Const.SERVICE_LOCK
        elif config[core.Const.CONF_TYPE] == "unlock":
            service = core.Const.SERVICE_UNLOCK
        elif config[core.Const.CONF_TYPE] == "open":
            service = core.Const.SERVICE_OPEN

        await self.controller.services.async_call(
            self.domain, service, service_data, blocking=True, context=context
        )

    # ----------------------- Condition Platform ----------------------------------

    @property
    def condition_schema(self) -> typing.Callable[[core.ConfigType], core.ConfigType]:
        return _CONDITION_SCHEMA

    async def async_get_conditions(self, device_id: str) -> list[dict[str, str]]:
        """List device conditions for Lock devices."""
        registry = self.controller.entity_registry
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
        condition_type = config[core.Const.CONF_TYPE]
        if condition_type == "is_jammed":
            state = core.Const.STATE_JAMMED
        elif condition_type == "is_locking":
            state = core.Const.STATE_LOCKING
        elif condition_type == "is_unlocking":
            state = core.Const.STATE_UNLOCKING
        elif condition_type == "is_locked":
            state = core.Const.STATE_LOCKED
        else:
            state = core.Const.STATE_UNLOCKED

        def test_is_state(
            shc: core.SmartHomeController, _variables: core.TemplateVarsType
        ) -> bool:
            """Test if an entity is a certain state."""
            return self.state(shc, config[core.Const.ATTR_ENTITY_ID], state)

        return test_is_state

    # ---------------------- Group Platform ------------------------------

    def async_describe_on_off_states(
        self, registry: core.GroupIntegrationRegistry
    ) -> None:
        """Describe group on off states."""
        registry.on_off_states({core.Const.STATE_UNLOCKED}, core.Const.STATE_LOCKED)

    # ------------------- Reproduce State Platform ------------------------

    async def async_reproduce_states(
        self,
        states: list[core.State],
        *,
        context: core.Context = None,
        reproduce_options: dict[str, typing.Any] = None,
    ):
        """Reproduce Lock states."""
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

    # ----------------- Significant Change Platform -------------------------

    def check_significant_change(
        self,
        old_state: str,
        _old_attrs: dict,
        new_state: str,
        _new_attrs: dict,
        **_kwargs: typing.Any,
    ) -> bool:
        """Test if state significantly changed."""
        if old_state != new_state:
            return True

        return False

    # ------------------------ Trigger Platform --------------------------------

    @property
    def trigger_schema(self) -> typing.Callable[[core.ConfigType], core.ConfigType]:
        return _TRIGGER_SCHEMA

    async def async_get_triggers(self, device_id: str) -> list[dict[str, str]]:
        """List device triggers for Lock devices."""
        registry = self.controller.entity_registry
        triggers = []

        # Get all the integrations entities for this device
        for entry in registry.async_entries_for_device(device_id):
            if entry.domain != self.domain:
                continue

            # Add triggers for each entity that belongs to this integration
            triggers += [
                {
                    core.Const.CONF_PLATFORM: "device",
                    core.Const.CONF_DEVICE_ID: device_id,
                    core.Const.CONF_DOMAIN: self.domain,
                    core.Const.CONF_ENTITY_ID: entry.entity_id,
                    core.Const.CONF_TYPE: trigger,
                }
                for trigger in _TRIGGER_TYPES
            ]

        return triggers

    async def async_get_trigger_capabilities(
        self, _config: core.ConfigType
    ) -> dict[str, vol.Schema]:
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
        trigger_type = config[core.Const.CONF_TYPE]
        if trigger_type == "jammed":
            to_state = core.Const.STATE_JAMMED
        elif trigger_type == "locking":
            to_state = core.Const.STATE_LOCKING
        elif trigger_type == "unlocking":
            to_state = core.Const.STATE_UNLOCKING
        elif trigger_type == "locked":
            to_state = core.Const.STATE_LOCKED
        else:
            to_state = core.Const.STATE_UNLOCKED

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

    if state.state in {core.Const.STATE_LOCKED, core.Const.STATE_LOCKING}:
        service = core.Const.SERVICE_LOCK
    elif state.state in {core.Const.STATE_UNLOCKED, core.Const.STATE_UNLOCKING}:
        service = core.Const.SERVICE_UNLOCK

    await shc.services.async_call(
        domain, service, service_data, context=context, blocking=True
    )
