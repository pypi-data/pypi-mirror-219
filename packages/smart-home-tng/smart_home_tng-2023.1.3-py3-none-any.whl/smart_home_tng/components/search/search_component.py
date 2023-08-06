"""
Search Component for Smart Home - The Next Generation.

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

import voluptuous as vol

from ... import core
from .searcher import Searcher

_SEARCH_RELATED: typing.Final = {
    vol.Required("type"): "search/related",
    vol.Required("item_type"): vol.In(
        (
            "area",
            "automation",
            "config_entry",
            "device",
            "entity",
            "group",
            "scene",
            "script",
        )
    ),
    vol.Required("item_id"): str,
}


# pylint: disable=unused-variable
class SearchComponent(core.SmartHomeControllerComponent):
    """The Search integration."""

    def __init__(self, path: typing.Iterable[str]):
        super().__init__(path)
        self._automation: core.AutomationComponent = None
        self._group: core.GroupComponent = None
        self._scene: core.ScenePlatform = None
        self._script: core.ScriptComponent = None

    @property
    def automation(self) -> core.AutomationComponent:
        return self._automation

    @property
    def group(self) -> core.GroupComponent:
        return self._group

    @property
    def scene(self) -> core.ScenePlatform:
        return self._scene

    @property
    def script(self) -> core.ScriptComponent:
        return self._script

    async def async_setup(self, config: core.ConfigType) -> bool:
        """Set up the Search component."""
        if not await super().async_setup(config):
            return False

        # Resolve needed components in setup, so we do not
        # need to resolve them in every call

        api = self.controller.components.websocket_api
        if not isinstance(api, core.WebSocket.Component):
            return False

        comp = self.controller.components.automation
        if isinstance(comp, core.AutomationComponent):
            self._automation = comp

        comp = self.controller.components.group
        if isinstance(comp, core.GroupComponent):
            self._group = comp

        comp = self.controller.components.homeassistant
        if comp is not None:
            self._scene = comp.get_platform(core.Platform.SCENE)

        comp = self.controller.components.script
        if isinstance(comp, core.ScriptComponent):
            self._script = comp

        api.register_command(self._search_related, _SEARCH_RELATED)
        return True

    @core.callback
    def _search_related(
        self,
        connection: core.WebSocket.Connection,
        msg: dict,
    ):
        """Handle search."""
        searcher = Searcher(self)
        connection.send_result(
            msg["id"], searcher.async_search(msg["item_type"], msg["item_id"])
        )
