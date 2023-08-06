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

import inspect
import typing

from .config_entry import ConfigEntry
from .device import Device
from .platform_implementation import PlatformImplementation


# pylint: disable=unused-variable
class DiagnosticsPlatform(PlatformImplementation):
    """Define the format that diagnostics platforms can have."""

    @property
    def supports_config_entry_diagnostics(self) -> bool:
        """Returns if config entry diagnostic supported"""
        current_impl = self.async_get_config_entry_diagnostics
        default_impl = DiagnosticsPlatform.async_get_config_entry_diagnostics
        return inspect.getfile(current_impl) != inspect.getfile(default_impl)

    @property
    def support_device_diagnostic(self) -> bool:
        """Returns if device diagnostic is supported"""
        current_impl = self.async_get_device_diagnostics
        default_impl = DiagnosticsPlatform.async_get_device_diagnostics
        return inspect.getfile(current_impl) != inspect.getfile(default_impl)

    # pylint: disable=unused-argument
    async def async_get_config_entry_diagnostics(
        self, config_entry: ConfigEntry
    ) -> typing.Any:
        """Return diagnostics for a config entry."""
        return

    # pylint: disable=unused-argument
    async def async_get_device_diagnostics(
        self, config_entry: ConfigEntry, device: Device
    ) -> typing.Any:
        """Return diagnostics for a device."""
        return
