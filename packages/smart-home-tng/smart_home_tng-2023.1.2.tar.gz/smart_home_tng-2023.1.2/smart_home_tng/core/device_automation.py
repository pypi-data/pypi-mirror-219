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

import enum
import types
import typing

import voluptuous as vol

from .action_condition_platform import ActionConditionPlatform
from .action_platform import ActionPlatform
from .callback_type import CallbackType
from .config_type import ConfigType
from .config_validation import ConfigValidation as _cv
from .const import Const
from .context import Context
from .integration_not_found import IntegrationNotFound
from .invalid_device_automation_config import InvalidDeviceAutomationConfig
from .platform import Platform
from .smart_home_controller_component import SmartHomeControllerComponent
from .trigger import Trigger
from .trigger_action_type import TriggerActionType
from .trigger_info import TriggerInfo
from .trigger_platform import TriggerPlatform

if not typing.TYPE_CHECKING:

    class SmartHomeController:
        pass


if typing.TYPE_CHECKING:
    from .smart_home_controller import SmartHomeController

_ENTITY_TRIGGERS: typing.Final = [
    {
        # Trigger when entity is turned on or off
        Const.CONF_PLATFORM: "device",
        Const.CONF_TYPE: Const.CONF_CHANGED_STATES,
    },
]

_TRIGGER_BASE_SCHEMA: typing.Final = _cv.TRIGGER_BASE_SCHEMA.extend(
    {
        vol.Required(Const.CONF_PLATFORM): "device",
        vol.Required(Const.CONF_DOMAIN): str,
        vol.Required(Const.CONF_DEVICE_ID): str,
        vol.Remove("metadata"): dict,
    }
)
_TRIGGER_SCHEMA = _TRIGGER_BASE_SCHEMA.extend(
    {
        vol.Required(Const.CONF_ENTITY_ID): _cv.entity_id,
        vol.Required(Const.CONF_TYPE): vol.In([Const.CONF_CHANGED_STATES]),
        vol.Optional(Const.CONF_FOR): _cv.positive_time_period_dict,
    }
)


class _Details(typing.NamedTuple):
    """Details for device automation."""

    platform: Platform
    get_automations_func: str
    get_capabilities_func: str


class _Type(enum.Enum):
    """Device automation type."""

    TRIGGER = _Details(
        Platform.TRIGGER,
        "async_get_triggers",
        "async_get_trigger_capabilities",
    )
    CONDITION = _Details(
        Platform.CONDITION,
        "async_get_conditions",
        "async_get_condition_capabilities",
    )
    ACTION = _Details(
        Platform.ACTION,
        "async_get_actions",
        "async_get_action_capabilities",
    )


_PlatformType = typing.Union[
    types.ModuleType,
    TriggerPlatform,
    ActionConditionPlatform,
    ActionPlatform,
]


# pylint: disable=unused-variable, invalid-name
class DeviceAutomation:
    """namespace class"""

    Details: typing.TypeAlias = _Details
    PlatformType: typing.TypeAlias = _PlatformType
    Type: typing.TypeAlias = _Type

    ENTITY_TRIGGERS: typing.Final = _ENTITY_TRIGGERS
    TRIGGER_BASE_SCHEMA: typing.Final = _TRIGGER_BASE_SCHEMA
    TRIGGER_SCHEMA: typing.Final = _TRIGGER_SCHEMA

    @staticmethod
    async def async_validate_action_config(
        shc: SmartHomeController, config: ConfigType
    ) -> ConfigType:
        """Validate config."""
        try:
            platform = await _async_get_device_automation_platform(
                shc, config[Const.CONF_DOMAIN], _Type.ACTION
            )
            if isinstance(platform, ActionPlatform):
                return await platform.async_validate_action_config(config)
            raise InvalidDeviceAutomationConfig("Action Platform not implemented.")
        except InvalidDeviceAutomationConfig as err:
            raise vol.Invalid(str(err) or "Invalid action configuration") from err

    @staticmethod
    async def async_call_action_from_config(
        shc: SmartHomeController,
        config: ConfigType,
        variables: dict[str, typing.Any],
        context: Context,
    ) -> None:
        """Execute a device action."""
        platform = await _async_get_device_automation_platform(
            shc,
            config[Const.CONF_DOMAIN],
            _Type.ACTION,
        )
        await platform.async_call_action_from_config(config, variables, context)

    @staticmethod
    async def async_attach_trigger(
        shc: SmartHomeController,
        config: ConfigType,
        action: TriggerActionType,
        trigger_info: TriggerInfo,
    ) -> CallbackType:
        """Listen for state changes based on configuration."""
        to_state = None
        state_config = {
            Const.CONF_PLATFORM: "state",
            Const.CONF_ENTITY_ID: config[Const.CONF_ENTITY_ID],
            Const.CONF_TO: to_state,
        }
        if Const.CONF_FOR in config:
            state_config[Const.CONF_FOR] = config[Const.CONF_FOR]

        state_config = Trigger.async_validate_trigger_config(state_config)
        return await Trigger.async_attach_state_trigger(
            shc, config, action, trigger_info, platform_type="device"
        )

    @staticmethod
    async def async_get_triggers(
        shc: SmartHomeController, device_id: str, domain: str
    ) -> list[dict[str, str]]:
        """List device triggers."""
        return await _async_get_automations(shc, device_id, _ENTITY_TRIGGERS, domain)

    @staticmethod
    async def async_get_trigger_capabilities() -> dict[str, vol.Schema]:
        """List trigger capabilities."""
        return {
            "extra_fields": vol.Schema(
                {vol.Optional(Const.CONF_FOR): _cv.positive_time_period_dict}
            )
        }


async def _async_get_automations(
    shc: SmartHomeController,
    device_id: str,
    automation_templates: list[dict[str, str]],
    domain: str,
) -> list[dict[str, str]]:
    """List device automations."""
    automations: list[dict[str, str]] = []
    entity_registry = shc.entity_registry

    entries = [
        entry
        for entry in entity_registry.async_entries_for_device(device_id)
        if entry.domain == domain
    ]

    for entry in entries:
        automations.extend(
            {
                **template,
                "device_id": device_id,
                "entity_id": entry.entity_id,
                "domain": domain,
            }
            for template in automation_templates
        )

    return automations


@typing.overload
async def _async_get_device_automation_platform(  # noqa: D103
    shc: SmartHomeController,
    domain: str,
    automation_type: typing.Literal[_Type.TRIGGER],
) -> TriggerPlatform:
    ...


@typing.overload
async def _async_get_device_automation_platform(  # noqa: D103
    shc: SmartHomeController,
    domain: str,
    automation_type: typing.Literal[_Type.CONDITION],
) -> ActionConditionPlatform:
    ...


@typing.overload
async def _async_get_device_automation_platform(  # noqa: D103
    shc: SmartHomeController,
    domain: str,
    automation_type: typing.Literal[_Type.ACTION],
) -> ActionPlatform:
    ...


@typing.overload
async def _async_get_device_automation_platform(  # noqa: D103
    shc: SmartHomeController, domain: str, automation_type: _Type
) -> _PlatformType:
    ...


async def _async_get_device_automation_platform(
    shc: SmartHomeController, domain: str, automation_type: _Type
) -> _PlatformType:
    """Load device automation platform for integration.

    Throws InvalidDeviceAutomationConfig if the integration is not found or
    does not support device automation.
    """
    platform_name: Platform = automation_type.value.platform
    try:
        integration = await shc.setup.async_get_integration_with_requirements(domain)
        # import implementation if not already done
        integration.get_component()
        shc_comp = SmartHomeControllerComponent.get_component(domain)
        if shc_comp is None:
            raise InvalidDeviceAutomationConfig(
                f"Integration {domain} is not compatible with Smart Home - The Next Generation."
            )
        platform = shc_comp.get_platform(platform_name)
        if platform is None:
            raise InvalidDeviceAutomationConfig(
                f"Integration '{domain}' does not support device automation "
                + f"{automation_type.name.lower()}s"
            )
    except IntegrationNotFound as err:
        raise InvalidDeviceAutomationConfig(
            f"Integration '{domain}' not found"
        ) from err
    except ImportError as err:
        raise InvalidDeviceAutomationConfig(
            f"Integration '{domain}' does not support device automation "
            + f"{automation_type.name.lower()}s"
        ) from err

    return platform
