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

import datetime
import typing

from .add_entities_callback import AddEntitiesCallback
from .config_type import ConfigType
from .discovery_info_type import DiscoveryInfoType
from .protocol import Protocol


if not typing.TYPE_CHECKING:

    class ConfigEntry:
        ...


if typing.TYPE_CHECKING:
    from .config_entry import ConfigEntry


# pylint: disable=unused-variable
class PlatformImplementation(Protocol):
    """Base Class for all platforms."""

    # pylint: disable=unused-argument
    async def async_setup_platform(
        self,
        platform_config: ConfigType,
        add_entities: AddEntitiesCallback,
        discovery_info: DiscoveryInfoType,
    ):
        """Setup the Platform."""
        return

    # pylint: disable=unused-argument
    async def async_setup_platform_devices(
        self, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
    ) -> None:
        """Set up platform devices."""
        return

    @property
    def platform_config_schema(self) -> typing.Callable[[ConfigType], ConfigType]:
        return None

    @property
    def parallel_updates(self) -> int:
        return 1

    @property
    def scan_interval(self) -> datetime.timedelta:
        return None
