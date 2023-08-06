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

import abc
import typing

import voluptuous as vol

from .callback_type import CallbackType
from .config_type import ConfigType
from .platform_implementation import PlatformImplementation
from .trigger_action_type import TriggerActionType
from .trigger_info import TriggerInfo


# pylint: disable=unused-variable
class TriggerPlatform(PlatformImplementation):
    """Define the format of device_trigger modules.

    Each module must define either TRIGGER_SCHEMA or async_validate_trigger_config.
    """

    @property
    def trigger_schema(self) -> typing.Callable[[ConfigType], ConfigType]:
        """
        Return the trigger schema, or none if async_validate_trigger config should be used.
        """
        return None

    async def async_validate_trigger_config(self, config: ConfigType) -> ConfigType:
        """Validate config."""
        schema = self.trigger_schema
        if schema is not None:
            # pylint: disable=not-callable
            return schema(config)
        raise NotImplementedError()

    @abc.abstractmethod
    async def async_attach_trigger(
        self,
        config: ConfigType,
        action: TriggerActionType,
        trigger_info: TriggerInfo,
    ) -> CallbackType:
        """Attach a trigger."""

    # pylint: disable=unused-argument
    async def async_get_trigger_capabilities(
        self, config: ConfigType
    ) -> dict[str, vol.Schema]:
        """List trigger capabilities."""
        # default impl does nothing
        return None

    # pylint: disable=unused-argument
    async def async_get_triggers(self, device_id: str) -> list[dict[str, str]]:
        """List triggers."""
        return None
