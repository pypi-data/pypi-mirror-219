"""
Device Automation Integration for Smart Home - The Next Generation.

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
import collections.abc
import logging
import typing
import voluptuous as vol
import voluptuous_serialize

from ... import core
from .action import Action
from .condition import Condition
from .trigger import Trigger

_cv: typing.TypeAlias = core.ConfigValidation

_LOGGER: typing.Final = logging.getLogger(__name__)

_LIST_ACTIONS: typing.Final = {
    vol.Required("type"): "device_automation/action/list",
    vol.Required("device_id"): str,
}
_LIST_CONDITIONS: typing.Final = {
    vol.Required("type"): "device_automation/condition/list",
    vol.Required("device_id"): str,
}
_LIST_TRIGGERS: typing.Final = {
    vol.Required("type"): "device_automation/trigger/list",
    vol.Required("device_id"): str,
}
_ACTION_CAPABILITIES: typing.Final = {
    vol.Required("type"): "device_automation/action/capabilities",
    vol.Required("action"): dict,
}
_CONDITION_CAPABILITIES: typing.Final = {
    vol.Required("type"): "device_automation/condition/capabilities",
    vol.Required("condition"): _cv.DEVICE_CONDITION_BASE_SCHEMA.extend(
        {}, extra=vol.ALLOW_EXTRA
    ),
}
_TRIGGER_CAPABILITIES: typing.Final = {
    vol.Required("type"): "device_automation/trigger/capabilities",
    vol.Required("trigger"): _cv.DEVICE_TRIGGER_BASE_SCHEMA.extend(
        {}, extra=vol.ALLOW_EXTRA
    ),
}


# pylint: disable=unused-variable
class DeviceAutomation(core.SmartHomeControllerComponent):
    """Helpers for device automations."""

    def __init__(self, path: typing.Iterable[str]):
        super().__init__(path)
        self._actions: core.ActionPlatform = None
        self._conditions: core.ConditionPlatform = None
        self._triggers: core.TriggerPlatform = None

    def get_platform(self, platform: core.Platform) -> core.PlatformImplementation:
        if platform == core.Platform.ACTION:
            if self._actions is None:
                self._actions = Action(self)
            return self._actions

        if platform == core.Platform.CONDITION:
            if self._conditions is None:
                self._conditions = Condition(self)
            return self._conditions

        if platform == core.Platform.TRIGGER:
            if self._triggers is None:
                self._triggers = Trigger(self)
            return self._triggers

        return None

    async def async_setup(self, config: core.ConfigType) -> bool:
        """Set up device automation."""
        if not await super().async_setup(config):
            return False

        api = self.controller.components.websocket_api
        if not isinstance(api, core.WebSocket.Component):
            return False

        api.register_command(self._list_actions, _LIST_ACTIONS)
        api.register_command(self._list_conditions, _LIST_CONDITIONS)
        api.register_command(self._list_triggers, _LIST_TRIGGERS)
        api.register_command(self._action_capabilities, _ACTION_CAPABILITIES)
        api.register_command(self._condition_capabilities, _CONDITION_CAPABILITIES)
        api.register_command(self._trigger_capabilities, _TRIGGER_CAPABILITIES)
        return True

    def async_get_device_automations(
        self,
        automation_type: core.DeviceAutomation.Type,
        device_ids: typing.Iterable[str] = None,
    ) -> collections.abc.Mapping[str, list[core.ConfigType]]:
        return _async_get_device_automations(self._shc, automation_type, device_ids)

    async def async_get_device_automation_platform(
        self,
        domain: str,
        automation_type: core.DeviceAutomation.Type,
    ) -> core.DeviceAutomation.PlatformType:
        """Load device automation platform for integration.

        Throws InvalidDeviceAutomationConfig if the integration is not found or
        does not support device automation.
        """
        return await _async_get_device_automation_platform(
            self.controller, domain, automation_type
        )

    @staticmethod
    async def _handle_device_errors(
        func: collections.abc.Callable[
            [core.WebSocket.Connection, dict],
            collections.abc.Awaitable[typing.Any],
        ],
        connection: core.WebSocket.Connection,
        msg: dict,
    ):
        """Handle device automation errors."""

        try:
            result = await func(connection, msg)
        except core.DeviceNotFound:
            connection.send_error(
                msg["id"], core.WebSocket.ERR_NOT_FOUND, "Device not found"
            )
        else:
            return result

    async def _list_actions(
        self,
        connection: core.WebSocket.Connection,
        msg: dict,
    ):
        await self._handle_device_errors(self._internal_list_actions, connection, msg)

    async def _internal_list_actions(
        self,
        connection: core.WebSocket.Connection,
        msg: dict,
    ):
        """Handle request for device actions."""
        device_id = msg["device_id"]
        actions = (
            await self.async_get_device_automations(
                core.DeviceAutomation.Type.ACTION, [device_id]
            )
        ).get(device_id)
        connection.send_result(msg["id"], actions)

    async def _list_conditions(
        self,
        connection: core.WebSocket.Connection,
        msg: dict,
    ):
        await self._handle_device_errors(
            self._internal_list_conditions, connection, msg
        )

    async def _internal_list_conditions(
        self,
        connection: core.WebSocket.Connection,
        msg: dict,
    ):
        """Handle request for device conditions."""
        device_id = msg["device_id"]
        conditions = (
            await self.async_get_device_automations(
                core.DeviceAutomation.Type.CONDITION, [device_id]
            )
        ).get(device_id)
        connection.send_result(msg["id"], conditions)

    async def _list_triggers(
        self,
        connection: core.WebSocket.Connection,
        msg: dict,
    ):
        await self._handle_device_errors(self._internal_list_triggers, connection, msg)

    async def _internal_list_triggers(
        self,
        connection: core.WebSocket.Connection,
        msg: dict,
    ):
        """Handle request for device triggers."""
        device_id = msg["device_id"]
        triggers = (
            await self.async_get_device_automations(
                core.DeviceAutomation.Type.TRIGGER, [device_id]
            )
        ).get(device_id)
        connection.send_result(msg["id"], triggers)

    async def _action_capabilities(
        self,
        connection: core.WebSocket.Connection,
        msg: dict,
    ):
        await self._handle_device_errors(
            self._internal_action_capabilities, connection, msg
        )

    async def _internal_action_capabilities(
        self,
        connection: core.WebSocket.Connection,
        msg: dict,
    ):
        """Handle request for device action capabilities."""
        shc = connection.owner.controller
        action = msg["action"]
        capabilities = await _async_get_device_automation_capabilities(
            shc, core.Platform.ACTION, action
        )
        connection.send_result(msg["id"], capabilities)

    async def _condition_capabilities(
        self,
        connection: core.WebSocket.Connection,
        msg: dict,
    ):
        await self._handle_device_errors(
            self._internal_condition_capabilities, connection, msg
        )

    async def _internal_condition_capabilities(
        self,
        connection: core.WebSocket.Connection,
        msg: dict,
    ):
        """Handle request for device condition capabilities."""
        shc = connection.owner.controller
        condition = msg["condition"]
        capabilities = await _async_get_device_automation_capabilities(
            shc, core.Platform.CONDITION, condition
        )
        connection.send_result(msg["id"], capabilities)

    async def _trigger_capabilities(
        self,
        connection: core.WebSocket.Connection,
        msg: dict,
    ):
        await self._handle_device_errors(
            self._internal_trigger_capabilities, connection, msg
        )

    async def _internal_trigger_capabilities(
        self,
        connection: core.WebSocket.Connection,
        msg: dict,
    ):
        """Handle request for device trigger capabilities."""
        shc = connection.owner.controller
        trigger = msg["trigger"]
        capabilities = await _async_get_device_automation_capabilities(
            shc, core.Platform.TRIGGER, trigger
        )
        connection.send_result(msg["id"], capabilities)


_VALID_AUTOMATION_PLATFORMS: typing.Final = [
    core.DeviceAutomation.Type.ACTION,
    core.DeviceAutomation.Type.CONDITION,
    core.DeviceAutomation.Type.TRIGGER,
]


async def _async_get_device_automation_platform(
    shc: core.SmartHomeController,
    domain: str,
    automation_type: core.DeviceAutomation.Type,
) -> core.DeviceAutomation.PlatformType:
    """Load device automation platform for integration.

    Throws InvalidDeviceAutomationConfig if the integration is not found or
    does not support device automation.
    """
    if automation_type not in _VALID_AUTOMATION_PLATFORMS:
        raise core.InvalidDeviceAutomationConfig(
            f"Platform '{automation_type.name.lower()}' is not supported in device automation."
        )

    try:
        integration = await shc.setup.async_get_integration_with_requirements(domain)
        # import implementation, if not already done
        integration.get_component()
        shc_comp = core.SmartHomeControllerComponent.get_component(domain)
        platform: core.Platform = automation_type.value.platform

        if shc_comp is not None:
            impl = shc_comp.get_platform(platform)
            if platform == core.Platform.ACTION and not isinstance(
                impl, core.ActionPlatform
            ):
                impl = None
            elif platform == core.Platform.CONDITION and not isinstance(
                impl, core.ActionConditionPlatform
            ):
                impl = None
            elif platform == core.Platform.TRIGGER and not isinstance(
                impl, core.TriggerPlatform
            ):
                impl = None
            if impl is None:
                raise core.InvalidDeviceAutomationConfig(
                    f"Integration '{domain}' does not support device automation "
                    f"{platform.value}s"
                )
        else:
            legacy_platforms = {
                core.DeviceAutomation.Type.ACTION: "device_action",
                core.DeviceAutomation.Type.CONDITION: "device_condition",
                core.DeviceAutomation.Type.TRIGGER: "device_trigger",
            }
            platform_name = legacy_platforms[automation_type]
            impl = integration.get_platform(platform_name)
    except core.IntegrationNotFound as err:
        raise core.InvalidDeviceAutomationConfig(
            f"Integration '{domain}' not found"
        ) from err
    except ImportError as err:
        raise core.InvalidDeviceAutomationConfig(
            f"Integration '{domain}' does not support device automation "
            f"{platform.value}s"
        ) from err

    return impl


async def _async_get_device_automations_from_domain(
    shc: core.SmartHomeController,
    domain: str,
    automation_type: core.DeviceAutomation.Type,
    device_ids,
    return_exceptions,
):
    """List device automations."""
    try:
        impl = await _async_get_device_automation_platform(shc, domain, automation_type)
    except core.InvalidDeviceAutomationConfig:
        return {}

    if isinstance(impl, core.ActionPlatform):
        return await asyncio.gather(
            *(impl.async_get_actions(device_id) for device_id in device_ids),
            return_exceptions=return_exceptions,
        )

    if isinstance(impl, core.ActionConditionPlatform):
        return await asyncio.gather(
            *(impl.async_get_conditions(device_id) for device_id in device_ids),
            return_exceptions=return_exceptions,
        )

    if isinstance(impl, core.TriggerPlatform):
        return await asyncio.gather(
            *(impl.async_get_triggers(device_id) for device_id in device_ids),
            return_exceptions=return_exceptions,
        )

    # Legacy implementation. Will be removed
    function_name = automation_type.value.get_automations_func

    return await asyncio.gather(
        *(getattr(impl, function_name)(shc, device_id) for device_id in device_ids),
        return_exceptions=return_exceptions,
    )


@core.callback
def _async_set_entity_device_automation_metadata(
    shc: core.SmartHomeController, automation: core.ConfigType
) -> None:
    """Set device automation metadata based on entity registry entry data."""
    if "metadata" not in automation:
        automation["metadata"] = {}
    if (
        core.Const.ATTR_ENTITY_ID not in automation
        or "secondary" in automation["metadata"]
    ):
        return

    entity_registry = shc.entity_registry
    # Guard against the entry being removed before this is called
    if not (entry := entity_registry.async_get(automation[core.Const.ATTR_ENTITY_ID])):
        return

    automation["metadata"]["secondary"] = bool(entry.entity_category or entry.hidden_by)


async def _async_get_device_automations(
    shc: core.SmartHomeController,
    automation_type: core.DeviceAutomation.Type,
    device_ids: typing.Iterable[str] = None,
) -> collections.abc.Mapping[str, list[core.ConfigType]]:
    """List device automations."""
    device_registry = shc.device_registry
    entity_registry = shc.entity_registry
    domain_devices: dict[str, set[str]] = {}
    device_entities_domains: dict[str, set[str]] = {}
    match_device_ids = set(device_ids or device_registry.devices)
    combined_results: dict[str, list[core.ConfigType]] = {}

    for entry in entity_registry.entities.values():
        if not entry.disabled_by and entry.device_id in match_device_ids:
            device_entities_domains.setdefault(entry.device_id, set()).add(entry.domain)

    for device_id in match_device_ids:
        combined_results[device_id] = []
        if (device := device_registry.async_get(device_id)) is None:
            raise core.DeviceNotFound
        for entry_id in device.config_entries:
            if config_entry := shc.config_entries.async_get_entry(entry_id):
                domain_devices.setdefault(config_entry.domain, set()).add(device_id)
        for domain in device_entities_domains.get(device_id, []):
            domain_devices.setdefault(domain, set()).add(device_id)

    # If specific device ids were requested, we allow
    # InvalidDeviceAutomationConfig to be thrown, otherwise we skip
    # devices that do not have valid triggers
    return_exceptions = not bool(device_ids)

    for domain_results in await asyncio.gather(
        *(
            _async_get_device_automations_from_domain(
                shc, domain, automation_type, domain_device_ids, return_exceptions
            )
            for domain, domain_device_ids in domain_devices.items()
        )
    ):
        for device_results in domain_results:
            if device_results is None or isinstance(
                device_results, core.InvalidDeviceAutomationConfig
            ):
                continue
            if isinstance(device_results, Exception):
                _LOGGER.error(
                    f"Unexpected error fetching device {automation_type.name.lower()}s",
                    exc_info=device_results,
                )
                continue
            for automation in device_results:
                _async_set_entity_device_automation_metadata(shc, automation)
                combined_results[automation["device_id"]].append(automation)

    return combined_results


async def _async_get_device_automation_capabilities(
    shc: core.SmartHomeController,
    automation_type: core.DeviceAutomation.Type,
    automation: collections.abc.Mapping[str, typing.Any],
) -> core.ConfigType:
    """List device automations."""
    try:
        impl = await _async_get_device_automation_platform(
            shc, automation[core.Const.CONF_DOMAIN], automation_type
        )
    except core.InvalidDeviceAutomationConfig:
        return {}

    capabilities = None
    handled = False
    if isinstance(impl, core.ActionPlatform):
        capabilities = impl.async_get_action_capabilities(automation)
        handled = True
    elif isinstance(impl, core.ActionConditionPlatform):
        capabilities = impl.async_get_condition_capabilities(automation)
        handled = True
    elif isinstance(impl, core.TriggerPlatform):
        capabilities = impl.async_get_trigger_capabilities(automation)
        handled = True

    if not handled:
        # Legacy implementation, will be removed
        function_name: str = automation_type.value.get_capabilities_func

        if not hasattr(impl, function_name):
            # The device automation has no capabilities
            return {}

        try:
            capabilities = await getattr(impl, function_name)(shc, automation)
        except core.InvalidDeviceAutomationConfig:
            return {}

    if capabilities is None:
        # The device automation has no capabilities
        return {}

    capabilities = capabilities.copy()

    if (extra_fields := capabilities.get("extra_fields")) is None:
        capabilities["extra_fields"] = []
    else:
        capabilities["extra_fields"] = voluptuous_serialize.convert(
            extra_fields, custom_serializer=_cv.custom_serializer
        )

    return capabilities
