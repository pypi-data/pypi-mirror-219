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

from .platform_implementation import PlatformImplementation


# pylint: disable=unused-variable
class ScenePlatform(PlatformImplementation):
    """Required base class for Scene Platform implementations."""

    @abc.abstractmethod
    def scenes_with_entity(self, entity_id: str) -> list[str]:
        """Return all scenes that reference the entity."""

    @abc.abstractmethod
    def entities_in_scene(self, scene_entity_id: str) -> list[str]:
        """Return all entities in a scene."""
