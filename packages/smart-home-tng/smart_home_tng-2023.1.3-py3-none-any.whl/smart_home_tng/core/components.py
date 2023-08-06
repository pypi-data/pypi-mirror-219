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

import typing

from .integration import Integration
from .setup_manager import _DATA_INTEGRATIONS
from .smart_home_controller_component import SmartHomeControllerComponent

if not typing.TYPE_CHECKING:

    class SmartHomeController:
        ...


if typing.TYPE_CHECKING:
    from .smart_home_controller import SmartHomeController


# pylint: disable=unused-variable
class Components:
    """Helper to load components."""

    def __init__(self, shc: SmartHomeController) -> None:
        """Initialize the Components class."""
        self._shc = shc
        self._data: dict[str, typing.Any] = {}

    def __getattr__(self, comp_name: str) -> SmartHomeControllerComponent:
        """Fetch a component."""
        # Test integration cache
        integration = self._data.get(comp_name)
        if integration is None:
            cache = self._shc.data.get(_DATA_INTEGRATIONS)
            if cache is not None:
                integration = cache.get(comp_name)
            if isinstance(integration, Integration):
                self._data[comp_name] = integration

        result = None
        if isinstance(integration, Integration):
            # import implementation, if not already don
            integration.get_component()
            result = SmartHomeControllerComponent.get_component(comp_name)
            if isinstance(result, SmartHomeControllerComponent):
                self._data[comp_name] = result
        elif isinstance(integration, SmartHomeControllerComponent):
            # Fallback to importing old-school
            result = integration

        if result:
            setattr(self, comp_name, result)
        return result
