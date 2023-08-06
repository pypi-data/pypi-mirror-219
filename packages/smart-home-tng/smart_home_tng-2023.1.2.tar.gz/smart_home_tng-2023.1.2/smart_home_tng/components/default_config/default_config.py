"""
Default Config Integration for Smart Home - The Next Generation.

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

from ... import core

try:
    import av
except ImportError:
    av = None


# pylint: disable=unused-variable
class DefaultConfig(core.SmartHomeControllerComponent):
    """Component providing default configuration for new users."""

    async def async_setup(self, config: core.ConfigType) -> bool:
        """Initialize default configuration."""
        if not await super().async_setup(config):
            return False

        result = await self._shc.setup.async_setup_component("backup", config)

        if av is None:
            return result

        return result or await self._shc.setup.async_setup_component("stream", config)
