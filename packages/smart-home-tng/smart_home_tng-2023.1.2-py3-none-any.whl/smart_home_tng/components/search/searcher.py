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

import collections
import logging
import typing

from ... import core

if not typing.TYPE_CHECKING:

    class SearchComponent:
        ...


if typing.TYPE_CHECKING:
    from .search_component import SearchComponent

_LOGGER: typing.Final = logging.getLogger(__name__)

# These types won't be further explored. Config entries + Output types.
_DONT_RESOLVE: typing.Final = {
    "scene",
    "automation",
    "script",
    "group",
    "config_entry",
    "area",
}
# These types exist as an entity and so need cleanup in results
_EXIST_AS_ENTITY: typing.Final = {"script", "scene", "automation", "group"}


# pylint: disable=unused-variable
class Searcher:
    """Find related things.

    Few rules:
    Scenes, scripts, automations and config entries will only be expanded if they are
    the entry point. They won't be expanded if we process them. This is because they
    turn the results into garbage.
    """

    def __init__(
        self,
        owner: SearchComponent,
    ) -> None:
        """Search results."""
        self._shc = owner.controller
        self._results: collections.defaultdict[str, set[str]] = collections.defaultdict(
            set
        )
        self._to_resolve: collections.deque[tuple[str, str]] = collections.deque()
        self._automation = owner.automation
        self._group = owner.group
        self._scene = owner.scene
        self._script = owner.script

    @core.callback
    def async_search(self, item_type, item_id):
        """Find results."""
        _LOGGER.debug(f"Searching for {item_type}/{item_id}", item_type, item_id)
        self._results[item_type].add(item_id)
        self._to_resolve.append((item_type, item_id))

        while self._to_resolve:
            search_type, search_id = self._to_resolve.popleft()
            getattr(self, f"_resolve_{search_type}")(search_id)

        # Clean up entity_id items, from the general "entity" type result,
        # that are also found in the specific entity domain type.
        for result_type in _EXIST_AS_ENTITY:
            self._results["entity"] -= self._results[result_type]

        # Remove entry into graph from search results.
        to_remove_item_type = item_type
        if item_type == "entity":
            domain = core.helpers.split_entity_id(item_id)[0]

            if domain in _EXIST_AS_ENTITY:
                to_remove_item_type = domain

        self._results[to_remove_item_type].remove(item_id)

        # Filter out empty sets.
        return {key: val for key, val in self._results.items() if val}

    @core.callback
    def _add_or_resolve(self, item_type, item_id):
        """Add an item to explore."""
        if item_id in self._results[item_type]:
            return

        self._results[item_type].add(item_id)

        if item_type not in _DONT_RESOLVE:
            self._to_resolve.append((item_type, item_id))

    @core.callback
    def _resolve_area(self, area_id) -> None:
        """Resolve an area."""
        dr = self._shc.device_registry
        er = self._shc.entity_registry

        for device in dr.async_entries_for_area(area_id):
            self._add_or_resolve("device", device.id)
        for entity_entry in er.async_entries_for_area(area_id):
            self._add_or_resolve("entity", entity_entry.entity_id)

        if self._script is not None:
            for entity_id in self._script.scripts_with_area(area_id):
                self._add_or_resolve("entity", entity_id)

        if self._automation is not None:
            for entity_id in self._automation.automations_with_area(area_id):
                self._add_or_resolve("entity", entity_id)

    @core.callback
    def _resolve_device(self, device_id) -> None:
        """Resolve a device."""
        device_entry = self._shc.device_registry.async_get(device_id)
        # Unlikely entry doesn't exist, but let's guard for bad data.
        if device_entry is not None:
            if device_entry.area_id:
                self._add_or_resolve("area", device_entry.area_id)

            for config_entry_id in device_entry.config_entries:
                self._add_or_resolve("config_entry", config_entry_id)

            # We do not resolve device_entry.via_device_id because that
            # device is not related data-wise inside HA.

        er = self._shc.entity_registry
        for entity_entry in er.async_entries_for_device(device_id):
            self._add_or_resolve("entity", entity_entry.entity_id)

        if self._script is not None:
            for entity_id in self._script.scripts_with_device(device_id):
                self._add_or_resolve("entity", entity_id)

        if self._automation is not None:
            for entity_id in self._automation.automations_with_device(device_id):
                self._add_or_resolve("entity", entity_id)

    @core.callback
    def _resolve_entity(self, entity_id) -> None:
        """Resolve an entity."""
        # Extra: Find automations and scripts that reference this entity.

        if self._scene is not None:
            for entity in self._scene.scenes_with_entity(entity_id):
                self._add_or_resolve("entity", entity)

        if self._group is not None:
            for entity in self._group.groups_with_entity(entity_id):
                self._add_or_resolve("entity", entity)

        if self._automation is not None:
            for entity in self._automation.automations_with_entity(entity_id):
                self._add_or_resolve("entity", entity)

        if self._script is not None:
            for entity in self._script.scripts_with_entity(entity_id):
                self._add_or_resolve("entity", entity)

        # Find devices
        er = self._shc.entity_registry
        entity_entry = er.async_get(entity_id)
        if entity_entry is not None:
            if entity_entry.device_id:
                self._add_or_resolve("device", entity_entry.device_id)

            if entity_entry.config_entry_id is not None:
                self._add_or_resolve("config_entry", entity_entry.config_entry_id)
        else:
            source = self._shc.entity_sources.get(entity_id)
            if source is not None and "config_entry" in source:
                self._add_or_resolve("config_entry", source["config_entry"])

        domain = core.helpers.split_entity_id(entity_id)[0]

        if domain in _EXIST_AS_ENTITY:
            self._add_or_resolve(domain, entity_id)

    @core.callback
    def _resolve_automation(self, automation_entity_id) -> None:
        """Resolve an automation.

        Will only be called if automation is an entry point.
        """
        if self._automation is not None:
            for entity in self._automation.entities_in_automation(automation_entity_id):
                self._add_or_resolve("entity", entity)

            for device in self._automation.devices_in_automation(automation_entity_id):
                self._add_or_resolve("device", device)

            for area in self._automation.areas_in_automation(automation_entity_id):
                self._add_or_resolve("area", area)

    @core.callback
    def _resolve_script(self, script_entity_id) -> None:
        """Resolve a script.

        Will only be called if script is an entry point.
        """
        if self._script is not None:
            for entity in self._script.entities_in_script(script_entity_id):
                self._add_or_resolve("entity", entity)

            for device in self._script.devices_in_script(script_entity_id):
                self._add_or_resolve("device", device)

            for area in self._script.areas_in_script(script_entity_id):
                self._add_or_resolve("area", area)

    @core.callback
    def _resolve_group(self, group_entity_id) -> None:
        """Resolve a group.

        Will only be called if group is an entry point.
        """
        if self._group is not None:
            for entity_id in self._group.get_entity_ids(group_entity_id):
                self._add_or_resolve("entity", entity_id)

    @core.callback
    def _resolve_scene(self, scene_entity_id) -> None:
        """Resolve a scene.

        Will only be called if scene is an entry point.
        """
        if self._scene is not None:
            for entity in self._scene.entities_in_scene(scene_entity_id):
                self._add_or_resolve("entity", entity)

    @core.callback
    def _resolve_config_entry(self, config_entry_id) -> None:
        """Resolve a config entry.

        Will only be called if config entry is an entry point.
        """
        dr = self._shc.device_registry
        er = self._shc.entity_registry
        for device_entry in dr.async_entries_for_config_entry(config_entry_id):
            self._add_or_resolve("device", device_entry.id)

        for entity_entry in er.async_entries_for_config_entry(config_entry_id):
            self._add_or_resolve("entity", entity_entry.entity_id)
