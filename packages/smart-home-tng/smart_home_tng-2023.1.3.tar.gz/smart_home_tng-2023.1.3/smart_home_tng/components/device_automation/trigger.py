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
class Trigger(core.TriggerPlatform):
    """Offer device oriented automation."""

    def __init__(self, owner: DeviceAutomation) -> None:
        super().__init__()
        self._owner = owner

    async def async_validate_trigger_config(
        self, config: core.ConfigType
    ) -> core.ConfigType:
        """Validate config."""
        try:
            platform = await self._owner.async_get_device_automation_platform(
                config[core.Const.CONF_DOMAIN], core.DeviceAutomation.Type.TRIGGER
            )
            if isinstance(platform, types.ModuleType):
                # Legacy impl, will be removed
                if not hasattr(platform, "async_validate_trigger_config"):
                    return typing.cast(core.ConfigType, platform.TRIGGER_SCHEMA(config))
                return await platform.async_validate_trigger_config(
                    self._owner.controller, config
                )
            if isinstance(platform, core.TriggerPlatform):
                return await platform.async_validate_trigger_config(config)
            raise vol.Invalid("Invalid trigger configuration")
        except core.InvalidDeviceAutomationConfig as err:
            raise vol.Invalid(str(err) or "Invalid trigger configuration") from err

    async def async_attach_trigger(
        self,
        config: core.ConfigType,
        action: core.TriggerActionType,
        trigger_info: core.TriggerInfo,
    ) -> core.CallbackType:
        """Listen for trigger."""
        platform = await self._owner.async_get_device_automation_platform(
            config[core.Const.CONF_DOMAIN], core.DeviceAutomation.Type.TRIGGER
        )
        if isinstance(platform, types.ModuleType) and hasattr(
            platform, "async_attach_trigger"
        ):
            # Legacy impl, will be removed
            return await platform.async_attach_trigger(
                self._owner.controller, config, action, trigger_info
            )
        if isinstance(platform, core.TriggerPlatform):
            return await platform.async_attach_trigger(config, action, trigger_info)
        raise vol.Invalid("Invalid trigger configuration")
