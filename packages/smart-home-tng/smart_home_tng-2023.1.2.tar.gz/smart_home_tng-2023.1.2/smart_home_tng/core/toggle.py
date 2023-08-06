"""
Core components of Smart Home - The Next Generation.

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

# pylint: disable=unused-variable

import dataclasses
import functools as ft
import typing

import voluptuous as vol

from .callback_type import CallbackType
from .condition_checker_type import ConditionCheckerType
from .config_type import ConfigType
from .config_validation import ConfigValidation as _cv
from .const import Const
from .context import Context
from .device_automation import DeviceAutomation, _async_get_automations
from .entity import Entity
from .entity_description import EntityDescription
from .script_condition import ScriptCondition
from .template_vars_type import TemplateVarsType
from .trigger import Trigger
from .trigger_action_type import TriggerActionType
from .trigger_info import TriggerInfo


if not typing.TYPE_CHECKING:

    class SmartHomeController:
        pass


if typing.TYPE_CHECKING:
    from .smart_home_controller import SmartHomeController


_CONF_IS_OFF: typing.Final = "is_off"
_CONF_IS_ON: typing.Final = "is_on"
_CONF_TOGGLE: typing.Final = "toggle"
_CONF_TURN_OFF: typing.Final = "turn_off"
_CONF_TURN_ON: typing.Final = "turn_on"
_CONF_TURNED_OFF: typing.Final = "turned_off"
_CONF_TURNED_ON: typing.Final = "turned_on"

_ENTITY_ACTIONS: typing.Final = [
    {
        # Turn entity off
        Const.CONF_TYPE: _CONF_TURN_OFF
    },
    {
        # Turn entity on
        Const.CONF_TYPE: _CONF_TURN_ON
    },
    {
        # Toggle entity
        Const.CONF_TYPE: _CONF_TOGGLE
    },
]

_ENTITY_CONDITIONS: typing.Final = [
    {
        # True when entity is turned off
        Const.CONF_CONDITION: "device",
        Const.CONF_TYPE: _CONF_IS_OFF,
    },
    {
        # True when entity is turned on
        Const.CONF_CONDITION: "device",
        Const.CONF_TYPE: _CONF_IS_ON,
    },
]

_ENTITY_TRIGGERS: typing.Final = [
    {
        # Trigger when entity is turned off
        Const.CONF_PLATFORM: "device",
        Const.CONF_TYPE: _CONF_TURNED_OFF,
    },
    {
        # Trigger when entity is turned on
        Const.CONF_PLATFORM: "device",
        Const.CONF_TYPE: _CONF_TURNED_ON,
    },
]

_DEVICE_ACTION_TYPES: typing.Final = [_CONF_TOGGLE, _CONF_TURN_OFF, _CONF_TURN_ON]

_ACTION_SCHEMA: typing.Final = _cv.DEVICE_ACTION_BASE_SCHEMA.extend(
    {
        vol.Required(Const.CONF_ENTITY_ID): _cv.entity_id,
        vol.Required(Const.CONF_TYPE): vol.In(_DEVICE_ACTION_TYPES),
    }
)

_CONDITION_SCHEMA: typing.Final = _cv.DEVICE_CONDITION_BASE_SCHEMA.extend(
    {
        vol.Required(Const.CONF_ENTITY_ID): _cv.entity_id,
        vol.Required(Const.CONF_TYPE): vol.In([_CONF_IS_OFF, _CONF_IS_ON]),
        vol.Optional(Const.CONF_FOR): _cv.positive_time_period_dict,
    }
)

_TOGGLE_TRIGGER_SCHEMA: typing.Final = _cv.DEVICE_TRIGGER_BASE_SCHEMA.extend(
    {
        vol.Required(Const.CONF_ENTITY_ID): _cv.entity_id,
        vol.Required(Const.CONF_TYPE): vol.In([_CONF_TURNED_OFF, _CONF_TURNED_ON]),
        vol.Optional(Const.CONF_FOR): _cv.positive_time_period_dict,
    }
)
_TRIGGER_SCHEMA: typing.Final = vol.Any(
    DeviceAutomation.TRIGGER_SCHEMA, _TOGGLE_TRIGGER_SCHEMA
)


@dataclasses.dataclass
class _EntityDescription(EntityDescription):
    """A class that describes toggle entities."""


class _Entity(Entity):
    """An abstract class for entities that can be turned on and off."""

    _entity_description: _EntityDescription
    _attr_is_on: bool = None
    _attr_state: None = None

    @property
    def entity_description(self) -> _EntityDescription:
        return super().entity_description

    @property
    @typing.final
    def state(self) -> typing.Literal["on", "off"]:
        """Return the state."""
        if (is_on := self.is_on) is None:
            return None
        return Const.STATE_ON if is_on else Const.STATE_OFF

    @property
    def is_on(self) -> bool:
        """Return True if entity is on."""
        return self._attr_is_on

    def turn_on(self, **kwargs: typing.Any) -> None:
        """Turn the entity on."""
        raise NotImplementedError()

    async def async_turn_on(self, **kwargs: typing.Any) -> None:
        """Turn the entity on."""
        await self._shc.async_add_executor_job(ft.partial(self.turn_on, **kwargs))

    def turn_off(self, **kwargs: typing.Any) -> None:
        """Turn the entity off."""
        raise NotImplementedError()

    async def async_turn_off(self, **kwargs: typing.Any) -> None:
        """Turn the entity off."""
        await self._shc.async_add_executor_job(ft.partial(self.turn_off, **kwargs))

    @typing.final
    def toggle(self, **kwargs: typing.Any) -> None:
        """Toggle the entity.

        This method will never be called by Home Assistant and should not be implemented
        by integrations.
        """

    async def async_toggle(self, **kwargs: typing.Any) -> None:
        """Toggle the entity.

        This method should typically not be implemented by integrations, it's enough to
        implement async_turn_on + async_turn_off or turn_on + turn_off.
        """
        if self.is_on:
            await self.async_turn_off(**kwargs)
        else:
            await self.async_turn_on(**kwargs)


# pylint: disable=invalid-name
class Toggle:
    """namespace for ToggleEntities."""

    Entity: typing.TypeAlias = _Entity
    EntityDescription: typing.TypeAlias = _EntityDescription

    CONF_IS_OFF: typing.Final = _CONF_IS_OFF
    CONF_IS_ON: typing.Final = _CONF_IS_ON
    CONF_TOGGLE: typing.Final = _CONF_TOGGLE
    CONF_TURN_OFF: typing.Final = _CONF_TURN_OFF
    CONF_TURN_ON: typing.Final = _CONF_TURN_ON
    CONF_TURNED_OFF: typing.Final = _CONF_TURNED_OFF
    CONF_TURNED_ON: typing.Final = _CONF_TURNED_ON

    ACTION_SCHEMA: typing.Final = _ACTION_SCHEMA
    CONDITION_SCHEMA: typing.Final = _CONDITION_SCHEMA
    DEVICE_ACTION_TYPES: typing.Final = _DEVICE_ACTION_TYPES
    ENTITY_ACTIONS: typing.Final = _ENTITY_ACTIONS
    ENTITY_CONDITIONS: typing.Final = _ENTITY_CONDITIONS
    ENTITY_TRIGGERS: typing.Final = _ENTITY_TRIGGERS
    TOGGLE_TRIGGER_SCHEMA: typing.Final = _TOGGLE_TRIGGER_SCHEMA
    TRIGGER_SCHEMA: typing.Final = _TRIGGER_SCHEMA

    @staticmethod
    async def async_call_action_from_config(
        shc: SmartHomeController,
        config: ConfigType,
        _variables: TemplateVarsType,
        context: Context,
        domain: str,
    ) -> None:
        """Change state based on configuration."""
        action_type = config[Const.CONF_TYPE]
        if action_type == _CONF_TURN_ON:
            action = "turn_on"
        elif action_type == _CONF_TURN_OFF:
            action = "turn_off"
        else:
            action = "toggle"

        service_data = {Const.ATTR_ENTITY_ID: config[Const.CONF_ENTITY_ID]}

        await shc.services.async_call(
            domain, action, service_data, blocking=True, context=context
        )

    @staticmethod
    async def async_condition_from_config(
        shc: SmartHomeController, config: ConfigType
    ) -> ConditionCheckerType:
        """Evaluate state based on configuration."""
        if config[Const.CONF_TYPE] == _CONF_IS_ON:
            stat = "on"
        else:
            stat = "off"
        state_config = {
            Const.CONF_CONDITION: "state",
            Const.CONF_ENTITY_ID: config[Const.CONF_ENTITY_ID],
            Const.CONF_STATE: stat,
        }
        if Const.CONF_FOR in config:
            state_config[Const.CONF_FOR] = config[Const.CONF_FOR]

        state_config = _cv.state_condition_schema(state_config)
        condition: ScriptCondition = ScriptCondition.get_action_condition_protocol(shc)
        state_config = condition.state_validate_config(state_config)
        return condition.state_from_config(state_config)

    @staticmethod
    async def async_attach_trigger(
        shc: SmartHomeController,
        config: ConfigType,
        action: TriggerActionType,
        trigger_info: TriggerInfo,
    ) -> CallbackType:
        """Listen for state changes based on configuration."""
        trigger_type = config[Const.CONF_TYPE]
        if trigger_type not in [_CONF_TURNED_ON, _CONF_TURNED_OFF]:
            return await DeviceAutomation.async_attach_trigger(
                shc, config, action, trigger_info
            )

        if trigger_type == _CONF_TURNED_ON:
            to_state = "on"
        else:
            to_state = "off"
        state_config = {
            Const.CONF_PLATFORM: "state",
            Const.CONF_ENTITY_ID: config[Const.CONF_ENTITY_ID],
            Const.CONF_TO: to_state,
        }
        if Const.CONF_FOR in config:
            state_config[Const.CONF_FOR] = config[Const.CONF_FOR]

        state_config = Trigger.async_validate_trigger_config(state_config)
        return await Trigger.async_attach_state_trigger(
            shc, state_config, action, trigger_info, platform_type="device"
        )

    @staticmethod
    async def async_get_actions(
        shc: SmartHomeController, device_id: str, domain: str
    ) -> list[dict[str, str]]:
        """List device actions."""
        return await _async_get_automations(shc, device_id, _ENTITY_ACTIONS, domain)

    @staticmethod
    async def async_get_conditions(
        shc: SmartHomeController, device_id: str, domain: str
    ) -> list[dict[str, str]]:
        """List device conditions."""
        return await _async_get_automations(shc, device_id, _ENTITY_CONDITIONS, domain)

    @staticmethod
    async def async_get_triggers(
        shc: SmartHomeController, device_id: str, domain: str
    ) -> list[dict[str, str]]:
        """List device triggers."""
        triggers = await DeviceAutomation.async_get_triggers(shc, device_id, domain)
        triggers.extend(
            await _async_get_automations(shc, device_id, _ENTITY_TRIGGERS, domain)
        )
        return triggers

    @staticmethod
    async def async_get_condition_capabilities(
        _shc: SmartHomeController, _config: ConfigType
    ) -> dict[str, vol.Schema]:
        """List condition capabilities."""
        return {
            "extra_fields": vol.Schema(
                {vol.Optional(Const.CONF_FOR): _cv.positive_time_period_dict}
            )
        }

    @staticmethod
    async def async_get_trigger_capabilities(
        config: ConfigType,
    ) -> dict[str, vol.Schema]:
        """List trigger capabilities."""
        if config[Const.CONF_TYPE] not in [_CONF_TURNED_ON, _CONF_TURNED_OFF]:
            return await DeviceAutomation.async_get_trigger_capabilities()

        return {
            "extra_fields": vol.Schema(
                {vol.Optional(Const.CONF_FOR): _cv.positive_time_period_dict}
            )
        }
