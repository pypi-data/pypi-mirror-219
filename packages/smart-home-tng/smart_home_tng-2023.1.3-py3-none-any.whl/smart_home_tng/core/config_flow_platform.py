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
import inspect
import typing

from .config_flow import _CONFIG_HANDLERS, ConfigFlow
from .options_flow import OptionsFlow
from .platform_implementation import PlatformImplementation
from .unknown_handler import UnknownHandler

if not typing.TYPE_CHECKING:

    class ConfigEntry:
        pass


if typing.TYPE_CHECKING:
    from .config_entry import ConfigEntry


# pylint: disable=unused-variable
class ConfigFlowPlatform(PlatformImplementation):
    """Base class for Config Flow Platform."""

    def _register_flow(self) -> None:
        if bool(self.domain):
            _CONFIG_HANDLERS[self.domain] = self

    @property
    @abc.abstractmethod
    def domain(self) -> str:
        """Return the domain of the ConfigFlow."""

    @property
    def version(self) -> int:
        return 1

    @abc.abstractmethod
    def create_config_flow(self, context: dict, init_data: typing.Any) -> ConfigFlow:
        """
        Create the Config Flow Implementation to avoid class registration
        in config flow registry.
        """

    def describe_config_flow(self) -> int:
        """Get infos about config flow without creating instance."""
        # For now, just return handler version
        return self.version

    # pylint: disable=unused-argument
    def supports_options_flow(self, entry: ConfigEntry):
        """Return options flow support for this handler."""
        current_impl = self.async_get_options_flow
        default_impl = ConfigFlowPlatform.async_get_options_flow
        return inspect.getfile(current_impl) != inspect.getfile(default_impl)

    # pylint: disable=unused-argument
    async def async_get_options_flow(
        self, entry: ConfigEntry, context: dict, init_data: typing.Any
    ) -> OptionsFlow:
        """Get the options flow for this handler."""
        raise UnknownHandler
