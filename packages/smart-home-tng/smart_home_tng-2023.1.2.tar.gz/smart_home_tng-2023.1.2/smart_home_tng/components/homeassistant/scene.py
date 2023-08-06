"""
Core pieces for Smart Home - The Next Generation.

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
from ... import core
from .scene_config import SceneConfig


# pylint: disable=unused-variable
class Scene(core.Scene):
    """A scene is a group of entities and the states we want them to be."""

    def __init__(
        self,
        shc: core.SmartHomeController,
        scene_config: SceneConfig,
        from_service=False,
    ):
        """Initialize the scene."""
        self._shc = shc
        self._scene_config = scene_config
        self._from_service = from_service

    @property
    def scene_config(self) -> SceneConfig:
        return self._scene_config

    @property
    def from_service(self) -> bool:
        return self._from_service

    @property
    def name(self):
        """Return the name of the scene."""
        return self._scene_config.name

    @property
    def icon(self):
        """Return the icon of the scene."""
        return self._scene_config.icon

    @property
    def unique_id(self):
        """Return unique ID."""
        return self._scene_config.id

    @property
    def extra_state_attributes(self):
        """Return the scene state attributes."""
        attributes = {core.Const.ATTR_ENTITY_ID: list(self._scene_config.states)}
        if (unique_id := self.unique_id) is not None:
            attributes[core.Const.CONF_ID] = unique_id
        return attributes

    async def async_activate(self, **kwargs: typing.Any) -> None:
        """Activate scene. Try to get entities into requested state."""
        await core.helpers.async_reproduce_states(
            self._shc,
            self._scene_config.states.values(),
            context=self._context,
            reproduce_options=kwargs,
        )
