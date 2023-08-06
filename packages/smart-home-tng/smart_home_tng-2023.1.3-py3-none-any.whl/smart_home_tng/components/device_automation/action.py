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

import types
import typing

import voluptuous as vol

from ... import core


if not typing.TYPE_CHECKING:

    class DeviceAutomation:
        ...


if typing.TYPE_CHECKING:
    from .device_automation import DeviceAutomation


# pylint: disable=unused-variable
class Action(core.ActionPlatform):
    """Implementation of the Action Platform."""

    def __init__(self, owner: DeviceAutomation):
        super().__init__()
        self._owner = owner

    async def async_validate_action_config(
        self, config: core.ConfigType
    ) -> core.ConfigType:
        """Validate config."""
        try:
            platform = await self._owner.async_get_device_automation_platform(
                config[core.Const.CONF_DOMAIN], core.DeviceAutomation.Type.ACTION
            )
            if isinstance(platform, types.ModuleType):
                # Legacy impl, will be removed
                if hasattr(platform, "async_validate_action_config"):
                    return await platform.async_validate_action_config(
                        self._owner.controller, config
                    )
                return typing.cast(core.ConfigType, platform.ACTION_SCHEMA(config))
            if isinstance(platform, core.ActionPlatform):
                return await platform.async_validate_action_config(config)
            raise vol.Invalid("Invalid action configuration")

        except core.InvalidDeviceAutomationConfig as err:
            raise vol.Invalid(str(err) or "Invalid action configuration") from err

    async def async_call_action_from_config(
        self,
        config: core.ConfigType,
        variables: dict[str, typing.Any],
        context: core.Context,
    ) -> None:
        """Execute a device action."""
        platform = await self._owner.async_get_device_automation_platform(
            config[core.Const.CONF_DOMAIN],
            core.DeviceAutomation.Type.ACTION,
        )
        if isinstance(platform, types.ModuleType) and hasattr(
            platform, "async_call_action_from_config"
        ):
            # Legacy impl, will be removed
            await platform.async_call_action_from_config(
                self._owner.controller, config, variables, context
            )
            return
        if isinstance(platform, core.ActionPlatform):
            await platform.async_call_action_from_config(config, variables, context)
            return
        raise vol.Invalid("Invalid action configuration")
