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

from .config_type import ConfigType
from .context import Context
from .platform_implementation import PlatformImplementation


# pylint: disable=unused-variable
class ActionPlatform(PlatformImplementation):
    """Define the format of device_action modules.

    Each module must define either ACTION_SCHEMA or async_validate_action_config.
    """

    @property
    def action_schema(self) -> typing.Callable[[ConfigType], ConfigType]:
        """
        Return the ACTION_SCHEMA or None, if async_validate_action_config
        should be called.
        """
        return None

    async def async_validate_action_config(self, config: ConfigType) -> ConfigType:
        """Validate config."""
        schema = self.action_schema
        if schema is not None:
            return schema(config)  # pylint: disable=not-callable
        raise NotImplementedError

    @abc.abstractmethod
    async def async_call_action_from_config(
        self,
        config: ConfigType,
        variables: dict[str, typing.Any],
        context: Context,
    ) -> None:
        """Execute a device action."""

    # pylint: disable=unused-argument
    async def async_get_action_capabilities(
        self, config: ConfigType
    ) -> dict[str, vol.Schema]:
        """List action capabilities."""
        # default impl does nothing
        return None

    # pylint: disable=unused-argument
    async def async_get_actions(self, device_id: str) -> list[dict[str, str]]:
        """List actions."""
        return None
