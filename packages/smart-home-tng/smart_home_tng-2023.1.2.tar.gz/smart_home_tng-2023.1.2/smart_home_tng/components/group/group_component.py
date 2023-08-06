"""
Group Component for Smart Home - The Next Generation.

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

import asyncio
import logging
import typing

import voluptuous as vol

from ... import core
from .const import Const
from .group import Group
from .group_integration_registry import GroupIntegrationRegistry, _current_domain

_ConfVal: typing.TypeAlias = core.ConfigValidation

_LOGGER: typing.Final = logging.getLogger(__name__)
_PLATFORMS: typing.Final = [
    core.Platform.BINARY_SENSOR,
    core.Platform.COVER,
    core.Platform.FAN,
    core.Platform.LIGHT,
    core.Platform.LOCK,
    core.Platform.MEDIA_PLAYER,
    core.Platform.NOTIFY,
    core.Platform.SWITCH,
]


# pylint: disable=unused-variable
class GroupComponent(
    core.GroupComponent, core.RecorderPlatform, core.ReproduceStatePlatform
):
    """Provide the functionality to group entities."""

    def __init__(self, path: typing.Iterable[str]):
        super().__init__(path)
        self._group_order: int = 0
        self._component: core.EntityComponent = None
        self._registry: GroupIntegrationRegistry = GroupIntegrationRegistry()
        self._service_lock = asyncio.Lock()

        self._supported_platforms = frozenset(
            _PLATFORMS
            + [
                core.Platform.CONFIG_FLOW,
                core.Platform.RECORDER,
                core.Platform.REPRODUCE_STATE,
            ]
        )

    @property
    def entity_component(self) -> core.EntityComponent:
        return self._component

    async def async_validate_config(self, config: core.ConfigType) -> core.ConfigType:
        schema = vol.Schema(
            {
                self.domain: vol.Schema(
                    {_ConfVal.match_all: vol.All(_conf_preprocess, Const.GROUP_SCHEMA)}
                )
            },
            extra=vol.ALLOW_EXTRA,
        )
        return schema(config)

    def get_group_order(self) -> int:
        result = self._group_order
        self._group_order += 1
        return result

    @property
    def state_registry(self) -> GroupIntegrationRegistry:
        return self._registry

    async def async_add_entities(self, entities: typing.Iterable[Group]):
        if self._component is None:
            self._component = core.EntityComponent(_LOGGER, self.domain, self._shc)
        await self._component.async_add_entities(entities)

    def _is_on(self, entity_id: str) -> bool:
        """Test if the group state is in its ON-state."""
        if self._registry is None:
            # Integration not setup yet, it cannot be on
            return False

        if (state := self._shc.states.get(entity_id)) is not None:
            return state.state in self._registry.on_off_mapping

        return False

    def expand_entity_ids(self, entity_ids: typing.Iterable[typing.Any]) -> list[str]:
        """Return entity_ids with group entity ids replaced by their members.

        Async friendly.
        """
        found_ids: list[str] = []
        for entity_id in entity_ids:
            if not isinstance(entity_id, str) or entity_id in (
                core.Const.ENTITY_MATCH_NONE,
                core.Const.ENTITY_MATCH_ALL,
            ):
                continue

            entity_id = entity_id.lower()

            try:
                # If entity_id points at a group, expand it
                domain, _ = core.helpers.split_entity_id(entity_id)

                if domain == self.domain:
                    child_entities = self.get_entity_ids(entity_id)
                    if entity_id in child_entities:
                        child_entities = list(child_entities)
                        child_entities.remove(entity_id)
                    found_ids.extend(
                        ent_id
                        for ent_id in self.expand_entity_ids(child_entities)
                        if ent_id not in found_ids
                    )

                else:
                    if entity_id not in found_ids:
                        found_ids.append(entity_id)

            except AttributeError:
                # Raised by split_entity_id if entity_id is not a string
                pass

        return found_ids

    def get_entity_ids(
        self, group_entity_id: str, domain_filter: str = None
    ) -> list[str]:
        """Get members of this group.

        Async friendly.
        """
        group = self._shc.states.get(group_entity_id)

        if not group or core.Const.ATTR_ENTITY_ID not in group.attributes:
            return []

        entity_ids = group.attributes[core.Const.ATTR_ENTITY_ID]
        if not domain_filter:
            return typing.cast(list[str], entity_ids)

        domain_filter = f"{domain_filter.lower()}."

        return [ent_id for ent_id in entity_ids if ent_id.startswith(domain_filter)]

    def groups_with_entity(self, entity_id: str) -> list[str]:
        """Get all groups that contain this entity.

        Async friendly.
        """
        if self._component is None:
            return []

        groups = []

        for group in self._component.entities:
            if entity_id in group.tracking:
                groups.append(group.entity_id)
        return groups

    async def async_setup_entry(self, entry: core.ConfigEntry) -> bool:
        """Set up a config entry."""
        self._shc.config_entries.async_setup_platforms(
            entry, (entry.options["group_type"],)
        )
        entry.async_on_unload(
            entry.add_update_listener(self._config_entry_update_listener)
        )
        return True

    async def _config_entry_update_listener(
        self, shc: core.SmartHomeController, entry: core.ConfigEntry
    ) -> None:
        """Update listener, called when the config entry options are changed."""
        await shc.config_entries.async_reload(entry.entry_id)

    async def async_unload_entry(self, entry: core.ConfigEntry) -> bool:
        """Unload a config entry."""
        return await self._shc.config_entries.async_unload_platforms(
            entry, (entry.options["group_type"],)
        )

    async def async_remove_entry(self, entry: core.ConfigEntry) -> None:
        """Remove a config entry."""
        # Unhide the group members
        registry = self._shc.entity_registry

        if not entry.options[Const.CONF_HIDE_MEMBERS]:
            return

        for member in entry.options[core.Const.CONF_ENTITIES]:
            if not (entity_id := registry.async_resolve_entity_id(member)):
                continue
            if (entity_entry := registry.async_get(entity_id)) is None:
                continue
            if entity_entry.hidden_by != core.EntityRegistryEntryHider.INTEGRATION:
                continue

            registry.async_update_entity(entity_id, hidden_by=None)

    async def async_setup(self, config: core.ConfigType) -> bool:
        """Set up all groups found defined in the configuration."""
        if not await super().async_setup(config):
            return False

        shc = self._shc

        if self._component is None:
            self._component = core.EntityComponent(_LOGGER, self.domain, shc)

        await shc.setup.async_process_integration_platform_for_component(self.domain)

        await shc.setup.async_process_integration_platforms(
            self.domain, self._process_group_platform
        )

        await self._async_process_config(config)

        shc.services.async_register(
            self.domain,
            core.Const.SERVICE_RELOAD,
            self._reload_service_handler,
            schema=vol.Schema({}),
        )

        shc.services.async_register(
            self.domain,
            Const.SERVICE_SET,
            self._locked_service_handler,
            schema=vol.All(
                vol.Schema(
                    {
                        vol.Required(Const.ATTR_OBJECT_ID): _ConfVal.slug,
                        vol.Optional(core.Const.ATTR_NAME): _ConfVal.string,
                        vol.Optional(core.Const.ATTR_ICON): _ConfVal.string,
                        vol.Optional(Const.ATTR_ALL): _ConfVal.boolean,
                        vol.Exclusive(
                            Const.ATTR_ENTITIES, "entities"
                        ): _ConfVal.entity_ids,
                        vol.Exclusive(
                            Const.ATTR_ADD_ENTITIES, "entities"
                        ): _ConfVal.entity_ids,
                    }
                )
            ),
        )

        shc.services.async_register(
            self.domain,
            Const.SERVICE_REMOVE,
            self._groups_service_handler,
            schema=vol.Schema({vol.Required(Const.ATTR_OBJECT_ID): _ConfVal.slug}),
        )
        return True

    async def _groups_service_handler(self, service: core.ServiceCall) -> None:
        """Handle dynamic group service functions."""
        object_id = service.data[Const.ATTR_OBJECT_ID]
        entity_id = f"{self.domain}.{object_id}"
        group: Group = self._component.get_entity(entity_id)

        # new group
        if service.service == Const.SERVICE_SET and group is None:
            entity_ids = (
                service.data.get(Const.ATTR_ENTITIES)
                or service.data.get(Const.ATTR_ADD_ENTITIES)
                or None
            )

            extra_arg = {
                attr: service.data[attr]
                for attr in (core.Const.ATTR_ICON,)
                if service.data.get(attr) is not None
            }

            await Group.async_create_group(
                self,
                service.data.get(core.Const.ATTR_NAME, object_id),
                object_id=object_id,
                entity_ids=entity_ids,
                user_defined=False,
                mode=service.data.get(Const.ATTR_ALL),
                **extra_arg,
            )
            return

        if group is None:
            _LOGGER.warning(f"{service.service}:Group '{object_id}' doesn't exist!")
            return

        # update group
        if service.service == Const.SERVICE_SET:
            need_update = False

            if Const.ATTR_ADD_ENTITIES in service.data:
                delta = service.data[Const.ATTR_ADD_ENTITIES]
                entity_ids = set(group.tracking) | set(delta)
                await group.async_update_tracked_entity_ids(entity_ids)

            if Const.ATTR_ENTITIES in service.data:
                entity_ids = service.data[Const.ATTR_ENTITIES]
                await group.async_update_tracked_entity_ids(entity_ids)

            if core.Const.ATTR_NAME in service.data:
                group.name = service.data[core.Const.ATTR_NAME]
                need_update = True

            if core.Const.ATTR_ICON in service.data:
                group.icon = service.data[core.Const.ATTR_ICON]
                need_update = True

            if Const.ATTR_ALL in service.data:
                group.mode = service.data[Const.ATTR_ALL]
                need_update = True

            if need_update:
                group.async_write_state()

            return

        # remove group
        if service.service == Const.SERVICE_REMOVE:
            await self._component.async_remove_entity(entity_id)

    async def _locked_service_handler(self, service: core.ServiceCall) -> None:
        """Handle a service with an async lock."""
        async with self._service_lock:
            await self._groups_service_handler(service)

    async def _reload_service_handler(self, _service: core.ServiceCall) -> None:
        """Remove all user-defined groups and load new ones from config."""
        auto = [
            typing.cast(Group, e)
            for e in self._component.entities
            if not typing.cast(Group, e).user_defined
        ]

        if (conf := await self._component.async_prepare_reload()) is None:
            return
        await self._async_process_config(conf)

        await self._component.async_add_entities(auto)

        await self._shc.setup.async_reload_integration_platforms(
            self.domain, _PLATFORMS
        )

    async def _process_group_platform(
        self, domain: str, platform: core.PlatformImplementation
    ):
        """Process a group platform."""
        if isinstance(platform, core.GroupPlatform):
            _current_domain.set(domain)
            platform.async_describe_on_off_states(self._registry)

    async def _async_process_config(self, config):
        """Process group configuration."""
        tasks = []

        for object_id, conf in config.get(self.domain, {}).items():
            name = conf.get(core.Const.CONF_NAME, object_id)
            entity_ids = conf.get(core.Const.CONF_ENTITIES) or []
            icon = conf.get(core.Const.CONF_ICON)
            mode = conf.get(Const.CONF_ALL)

            # We keep track of the order when we are creating the tasks
            # in the same way that async_create_group does to make
            # sure we use the same ordering system.  This overcomes
            # the problem with concurrently creating the groups
            tasks.append(
                Group.async_create_group(
                    self,
                    name,
                    entity_ids,
                    icon=icon,
                    object_id=object_id,
                    mode=mode,
                    order=self.get_group_order(),
                )
            )
        await asyncio.gather(*tasks)

    def exclude_attributes(self) -> set[str]:
        """Exclude static attributes from being recorded in the database."""
        return {
            core.Const.ATTR_ENTITY_ID,
            Const.ATTR_ORDER,
            Const.ATTR_AUTO,
        }

    async def async_reproduce_states(
        self,
        states: list[core.State],
        *,
        context: core.Context = None,
        reproduce_options: dict[str, typing.Any] = None,
    ):
        """Reproduce component states."""
        states_copy = []
        for state in states:
            members = self.get_entity_ids(state.entity_id)
            for member in members:
                states_copy.append(
                    core.State(
                        member,
                        state.state,
                        state.attributes,
                        last_changed=state.last_changed,
                        last_updated=state.last_updated,
                        context=state.context,
                    )
                )
        await core.helpers.async_reproduce_state(
            self.controller,
            states_copy,
            context=context,
            reproduce_options=reproduce_options,
        )


def _conf_preprocess(value):
    """Preprocess alternative configuration formats."""
    if not isinstance(value, dict):
        value = {core.Const.CONF_ENTITIES: value}

    return value
