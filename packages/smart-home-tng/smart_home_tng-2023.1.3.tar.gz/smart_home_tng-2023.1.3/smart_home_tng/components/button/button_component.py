"""
Button Component for Smart Home - The Next Generation.

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

import datetime as dt
import logging
import typing

import voluptuous as vol

from ... import core

_cv: typing.TypeAlias = core.ConfigValidation
_LOGGER: typing.Final = logging.getLogger(__name__)
_ACTION_TYPES: typing.Final = {"press"}
_TRIGGER_TYPES = {"pressed"}
_TRIGGER_SCHEMA = _cv.DEVICE_TRIGGER_BASE_SCHEMA.extend(
    {
        vol.Required(core.Const.CONF_ENTITY_ID): _cv.entity_id,
        vol.Required(core.Const.CONF_TYPE): vol.In(_TRIGGER_TYPES),
    }
)


# pylint: disable=unused-variable
class ButtonComponent(
    core.SmartHomeControllerComponent, core.ActionPlatform, core.TriggerPlatform
):
    """Component to pressing a button as platforms."""

    def __init__(self, path: typing.Iterable[str]):
        super().__init__(path)
        self._entities: core.EntityComponent = None
        self._supported_platforms = frozenset(
            [core.Platform.ACTION, core.Platform.TRIGGER]
        )

    @property
    def entity_component(self) -> core.EntityComponent:
        return self._entities

    @property
    def scan_interval(self) -> dt.timedelta:
        return core.Button.SCAN_INTERVAL

    async def async_setup(self, config: core.ConfigType) -> bool:
        """Set up Button entities."""
        component = self._entities = core.EntityComponent(
            _LOGGER, self.domain, self.controller, self.scan_interval
        )
        await component.async_setup(config)

        component.async_register_entity_service(
            core.Button.SERVICE_PRESS,
            {},
            "_async_press_action",
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

    # --------------------- Action Platform -----------------------------------

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
        """List device actions for button devices."""
        registry = self.controller.entity_registry
        return [
            {
                core.Const.CONF_DEVICE_ID: device_id,
                core.Const.CONF_DOMAIN: self.domain,
                core.Const.CONF_ENTITY_ID: entry.entity_id,
                core.Const.CONF_TYPE: "press",
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
        await self._shc.services.async_call(
            self.domain,
            core.Button.SERVICE_PRESS,
            {
                core.Const.ATTR_ENTITY_ID: config[core.Const.CONF_ENTITY_ID],
            },
            blocking=True,
            context=context,
        )

    # ---------------------------- Trigger Platform ---------------------------

    @property
    def trigger_schema(self) -> typing.Callable[[core.ConfigType], core.ConfigType]:
        return _TRIGGER_SCHEMA

    async def async_get_triggers(self, device_id: str) -> list[dict[str, str]]:
        """List device triggers for button devices."""
        registry = self.controller.entity_registry
        return [
            {
                core.Const.CONF_PLATFORM: "device",
                core.Const.CONF_DEVICE_ID: device_id,
                core.Const.CONF_DOMAIN: self.domain,
                core.Const.CONF_ENTITY_ID: entry.entity_id,
                core.Const.CONF_TYPE: "pressed",
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
            core.Const.CONF_PLATFORM: "state",
            core.Const.CONF_ENTITY_ID: config[core.Const.CONF_ENTITY_ID],
        }

        state_config = await core.Trigger.async_validate_trigger_config(state_config)
        return await core.Trigger.async_attach_state_trigger(
            self.controller, state_config, action, trigger_info, platform_type="device"
        )
