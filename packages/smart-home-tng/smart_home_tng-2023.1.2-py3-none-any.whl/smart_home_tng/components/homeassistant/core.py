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

import asyncio
import itertools as it
import logging
import typing

import voluptuous as vol

from ... import core
from ...auth.permissions import Const as perm_const
from .core_trigger import CoreTrigger
from .event_trigger import EventTrigger
from .numeric_state_trigger import NumericStateTrigger
from .scene import Scene
from .scene_config import SceneConfig
from .state_trigger import StateTrigger
from .time_pattern_trigger import TimePatternTrigger
from .time_trigger import TimeTrigger


_cv: typing.TypeAlias = core.ConfigValidation
_LOGGER: typing.Final = logging.getLogger(__name__)


def _convert_states(states):
    """Convert state definitions to State objects."""
    result = {}

    for entity_id, info in states.items():
        entity_id = _cv.entity_id(entity_id)

        if isinstance(info, dict):
            entity_attrs = info.copy()
            state = entity_attrs.pop(core.Const.ATTR_STATE, None)
            attributes = entity_attrs
        else:
            state = info
            attributes = {}

        # YAML translates 'on' to a boolean
        # http://yaml.org/type/bool.html
        if isinstance(state, bool):
            state = core.Const.STATE_ON if state else core.Const.STATE_OFF
        elif not isinstance(state, str):
            raise vol.Invalid(f"State for {entity_id} should be a string")

        result[entity_id] = core.State(entity_id, state, attributes)

    return result


def _ensure_no_intersection(value):
    """Validate that entities and snapshot_entities do not overlap."""
    if (
        _CONF_SNAPSHOT not in value
        or core.Const.CONF_ENTITIES not in value
        or all(
            entity_id not in value[_CONF_SNAPSHOT]
            for entity_id in value[core.Const.CONF_ENTITIES]
        )
    ):
        return value

    raise vol.Invalid("entities and snapshot_entities must not overlap")


_CONF_SCENE_ID: typing.Final = "scene_id"
_CONF_SNAPSHOT: typing.Final = "snapshot_entities"

_SHUTDOWN_SERVICES: typing.Final = (
    core.Const.SERVICE_SHC_STOP,
    core.Const.SERVICE_SHC_RESTART,
)
_ATTR_ENTRY_ID: typing.Final = "entry_id"

_EVENT_SCENE_RELOADED: typing.Final = "scene.reloaded"

_SERVICE_RELOAD_CORE_CONFIG: typing.Final = "reload_core_config"
_SERVICE_RELOAD_CONFIG_ENTRY: typing.Final = "reload_config_entry"
_SERVICE_CHECK_CONFIG: typing.Final = "check_config"
_SERVICE_UPDATE_ENTITY: typing.Final = "update_entity"
_SERVICE_SET_LOCATION: typing.Final = "set_location"
_SERVICE_APPLY: typing.Final = "apply"
_SERVICE_CREATE: typing.Final = "create"

_SCHEMA_UPDATE_ENTITY: typing.Final = vol.Schema(
    {core.Const.ATTR_ENTITY_ID: _cv.entity_ids}
)
_SCHEMA_RELOAD_CONFIG_ENTRY: typing.Final = vol.All(
    vol.Schema(
        {
            vol.Optional(_ATTR_ENTRY_ID): str,
            **_cv.ENTITY_SERVICE_FIELDS,
        },
    ),
    _cv.has_at_least_one_key(_ATTR_ENTRY_ID, *_cv.ENTITY_SERVICE_FIELDS),
)
_STATES_SCHEMA: typing.Final = vol.All(dict, _convert_states)
_CREATE_SCENE_SCHEMA = vol.All(
    _cv.has_at_least_one_key(core.Const.CONF_ENTITIES, _CONF_SNAPSHOT),
    _ensure_no_intersection,
    vol.Schema(
        {
            vol.Required(_CONF_SCENE_ID): _cv.slug,
            vol.Optional(core.Const.CONF_ENTITIES, default={}): _STATES_SCHEMA,
            vol.Optional(_CONF_SNAPSHOT, default=[]): _cv.entity_ids,
        }
    ),
)


# pylint: disable=unused-variable
class CoreIntegration(
    core.SmartHomeControllerComponent,
    core.LogbookPlatform,
    core.ScenePlatform,
    core.TriggerPlatform,
    core.SystemHealthPlatform,
):
    """Integration providing core pieces of infrastructure."""

    def __init__(self, path: typing.Iterable[str]):
        super().__init__(path)
        self._scene_platform: core.EntityPlatform = None
        self._scene_config: core.ConfigType = None
        self._add_scene_entities: core.AddEntitiesCallback = None
        self._trigger_platforms: dict[str, core.TriggerPlatform] = None
        self._supported_platforms = frozenset(
            [
                core.Platform.LOGBOOK,
                core.Platform.SCENE,
                core.Platform.TRIGGER,
                core.Platform.SYSTEM_HEALTH,
            ]
        )

    def async_describe_event(self, event: core.LazyPartialState) -> dict[str, str]:
        result: dict[str, str] = {}
        result[self.LOGBOOK_ENTRY_NAME] = "Smart Home - The Next Generation"
        result[self.LOGBOOK_ENTRY_ICON] = "mdi:home-assistant"
        result[self.LOGBOOK_ENTRY_MESSAGE] = (
            "started" if event.event_type == core.Const.EVENT_SHC_START else "stopped"
        )
        return result

    def async_describe_events(self, async_describe_event: core.LogbookCallback) -> None:
        async_describe_event(core.Const.EVENT_SHC_STOP)
        async_describe_event(core.Const.EVENT_SHC_START)

    async def async_can_shutdown(self, service: str) -> str:
        result = None
        if service == core.Const.SERVICE_SHC_RESTART:
            errors = await self._shc.setup.async_check_shc_config_file()

            if errors:
                result = (
                    f"The system cannot {service} because the "
                    + f"configuration is not valid: {errors}"
                )
                self.controller.persistent_notification.async_create(
                    "Config error. See [the logs](/config/logs) for details.",
                    "Config validation",
                    f"{self.domain}.check_config",
                )
        return result

    async def _async_save_persistent_states(self, _service: core.ServiceCall) -> None:
        """Handle calls to homeassistant.save_persistent_states."""
        await core.RestoreStateData.async_save_persistent_states(self._shc)

    async def _async_handle_turn_service(self, service: core.ServiceCall) -> None:
        """Handle calls to homeassistant.turn_on/off."""
        referenced = core.Service.async_extract_referenced_entity_ids(
            self._shc, service
        )
        all_referenced = referenced.referenced | referenced.indirectly_referenced

        # Generic turn on/off method requires entity id
        if not all_referenced:
            _LOGGER.error(
                f"The service smart_home_tng.{service.service} "
                + "cannot be called without a target",
            )
            return

        # Group entity_ids by domain. groupby requires sorted data.
        by_domain = it.groupby(
            sorted(all_referenced),
            lambda item: core.helpers.split_entity_id(item)[0],
        )

        tasks = []
        unsupported_entities = set()

        for domain, ent_ids in by_domain:
            # This leads to endless loop.
            if domain == self.domain:
                _LOGGER.warning(
                    f"Called service smart_home_tng.{service.service} with "
                    + f"invalid entities {', '.join(ent_ids)}",
                )
                continue

            if not self._shc.services.has_service(domain, service.service):
                unsupported_entities.update(set(ent_ids) & referenced.referenced)
                continue

            # Create a new dict for this call
            data = dict(service.data)

            # ent_ids is a generator, convert it to a list.
            data[core.Const.ATTR_ENTITY_ID] = list(ent_ids)

            tasks.append(
                self._shc.services.async_call(
                    domain,
                    service.service,
                    data,
                    blocking=True,
                    context=service.context,
                )
            )

        if unsupported_entities:
            _LOGGER.warning(
                f"The service smart_home_tng.{service.service} does not "
                + f"support entities {', '.join(sorted(unsupported_entities))}"
            )

        if tasks:
            await asyncio.gather(*tasks)

    async def _async_handle_core_service(self, call: core.ServiceCall) -> None:
        """Service handler for handling core services."""
        if call.service in _SHUTDOWN_SERVICES:
            for component in self._components().values():
                error = await component.async_can_shutdown(call.service)
                if error is not None and error != "":
                    _LOGGER.error(error)
                    raise core.SmartHomeControllerError(error)

        if call.service == core.Const.SERVICE_SHC_STOP:
            asyncio.create_task(self._shc.async_stop())
            return

        if call.service == core.Const.SERVICE_SHC_RESTART:
            asyncio.create_task(self._shc.async_stop(core.Const.RESTART_EXIT_CODE))

    async def _async_handle_update_service(self, call: core.ServiceCall) -> None:
        """Service handler for updating an entity."""
        if call.context.user_id:
            user = await self._shc.auth.async_get_user(call.context.user_id)

            if user is None:
                raise core.UnknownUser(
                    context=call.context,
                    permission=perm_const.POLICY_CONTROL,
                    user_id=call.context.user_id,
                )

            for entity in call.data[core.Const.ATTR_ENTITY_ID]:
                if not user.permissions.check_entity(entity, perm_const.POLICY_CONTROL):
                    raise core.Unauthorized(
                        context=call.context,
                        permission=perm_const.POLICY_CONTROL,
                        user_id=call.context.user_id,
                        perm_category=perm_const.CAT_ENTITIES,
                    )

        tasks = [
            self._shc.entity_registry.async_update_entity(entity)
            for entity in call.data[core.Const.ATTR_ENTITY_ID]
        ]

        if tasks:
            await asyncio.wait(tasks)

    async def _async_handle_reload_config(self, _call: core.ServiceCall) -> None:
        """Service handler for reloading core config."""
        try:
            conf = await self._shc.setup.async_shc_config_yaml()
        except core.SmartHomeControllerError as err:
            _LOGGER.error(err)
            return

        # auth only processed during startup
        await self._shc.setup.async_process_shc_core_config(conf.get(self.domain) or {})

    async def _async_set_location(self, call: core.ServiceCall) -> None:
        """Service handler to set location."""
        await self._shc.config.async_update(
            latitude=call.data[core.Const.ATTR_LATITUDE],
            longitude=call.data[core.Const.ATTR_LONGITUDE],
        )

    async def _async_handle_reload_config_entry(self, call: core.ServiceCall) -> None:
        """Service handler for reloading a config entry."""
        reload_entries = set()
        if _ATTR_ENTRY_ID in call.data:
            reload_entries.add(call.data[_ATTR_ENTRY_ID])
        reload_entries.update(
            await core.Service.async_extract_config_entry_ids(self._shc, call)
        )
        if not reload_entries:
            raise ValueError("There were no matching config entries to reload")
        await asyncio.gather(
            *(
                self._shc.config_entries.async_reload(config_entry_id)
                for config_entry_id in reload_entries
            )
        )

    async def async_setup(self, config: core.ConfigType) -> bool:
        # pylint: disable=no-member
        if not await super().async_setup(config):
            return False

        self._shc.services.async_register(
            self.domain,
            core.Const.SERVICE_SAVE_PERSISTENT_STATES,
            self._async_save_persistent_states,
        )

        service_schema = vol.Schema(
            {core.Const.ATTR_ENTITY_ID: _cv.entity_ids}, extra=vol.ALLOW_EXTRA
        )

        self._shc.services.async_register(
            self.domain,
            core.Const.SERVICE_TURN_OFF,
            self._async_handle_turn_service,
            schema=service_schema,
        )
        self._shc.services.async_register(
            self.domain,
            core.Const.SERVICE_TURN_ON,
            self._async_handle_turn_service,
            schema=service_schema,
        )
        self._shc.services.async_register(
            self.domain,
            core.Const.SERVICE_TOGGLE,
            self._async_handle_turn_service,
            schema=service_schema,
        )

        core.Service.async_register_admin_service(
            self._shc,
            self.domain,
            core.Const.SERVICE_SHC_STOP,
            self._async_handle_core_service,
        )
        core.Service.async_register_admin_service(
            self._shc,
            self.domain,
            core.Const.SERVICE_SHC_RESTART,
            self._async_handle_core_service,
        )

        core.Service.async_register_admin_service(
            self._shc,
            self.domain,
            _SERVICE_CHECK_CONFIG,
            self._async_handle_core_service,
        )

        self._shc.services.async_register(
            self.domain,
            _SERVICE_UPDATE_ENTITY,
            self._async_handle_update_service,
            schema=_SCHEMA_UPDATE_ENTITY,
        )

        core.Service.async_register_admin_service(
            self._shc,
            self.domain,
            _SERVICE_RELOAD_CORE_CONFIG,
            self._async_handle_reload_config,
        )

        core.Service.async_register_admin_service(
            self._shc,
            self.domain,
            _SERVICE_SET_LOCATION,
            self._async_set_location,
            vol.Schema(
                {
                    core.Const.ATTR_LATITUDE: _cv.latitude,
                    core.Const.ATTR_LONGITUDE: _cv.longitude,
                }
            ),
        )

        core.Service.async_register_admin_service(
            self._shc,
            self.domain,
            _SERVICE_RELOAD_CONFIG_ENTRY,
            self._async_handle_reload_config_entry,
            schema=_SCHEMA_RELOAD_CONFIG_ENTRY,
        )

        return True

    def scenes_with_entity(self, entity_id: str) -> list[str]:
        """Return all scenes that reference the entity."""
        if self._scene_platform is None:
            return []

        platform = self._scene_platform

        return [
            scene_entity.entity_id
            for scene_entity in platform.entities.values()
            if entity_id in scene_entity.scene_config.states
        ]

    def entities_in_scene(self, scene_entity_id: str) -> list[str]:
        """Return all entities in a scene."""
        if self._scene_platform is None:
            return []

        platform = self._scene_platform

        if (entity := platform.entities.get(scene_entity_id)) is None:
            return []
        if not isinstance(entity, Scene):
            return []

        return list(entity.scene_config.states)

    async def async_setup_platform(
        self,
        platform_config: core.ConfigType,
        add_entities: core.AddEntitiesCallback,
        discovery_info: core.DiscoveryInfoType,
    ):
        platform = core.EntityPlatform.async_get_current_platform()
        if platform and platform.domain == core.Platform.SCENE:
            await self._async_setup_scene_platform(
                platform, platform_config, add_entities, discovery_info
            )

    async def _async_setup_scene_platform(
        self,
        platform: core.EntityPlatform,
        config: core.ConfigType,
        add_entities: core.AddEntitiesCallback,
        _discovery_info: core.DiscoveryInfoType,
    ):
        """Set up Smart Home TNG scene entries."""
        _process_scenes_config(self._shc, add_entities, config)

        # This platform can be loaded multiple times. Only first time register the service.
        if self._shc.services.has_service(
            core.Const.SCENE_COMPONENT_NAME, core.Const.SERVICE_RELOAD
        ):
            return

        # Store platform for later.
        self._scene_platform = platform
        self._scene_config = config
        self._add_scene_entities = add_entities

        core.Service.async_register_admin_service(
            self._shc,
            core.Const.SCENE_COMPONENT_NAME,
            core.Const.SERVICE_RELOAD,
            self._reload_scene_config,
        )

        self._shc.services.async_register(
            core.Const.SCENE_COMPONENT_NAME,
            _SERVICE_APPLY,
            self._apply_scene_service,
            vol.Schema(
                {
                    vol.Optional(core.Const.ATTR_TRANSITION): vol.All(
                        vol.Coerce(float), vol.Clamp(min=0, max=6553)
                    ),
                    vol.Required(core.Const.CONF_ENTITIES): _STATES_SCHEMA,
                }
            ),
        )

        self._shc.services.async_register(
            core.Const.SCENE_COMPONENT_NAME,
            _SERVICE_CREATE,
            self._create_scene_service,
            _CREATE_SCENE_SCHEMA,
        )

    async def _apply_scene_service(self, call: core.ServiceCall) -> None:
        """Apply a scene."""
        reproduce_options = {}

        if core.Const.ATTR_TRANSITION in call.data:
            reproduce_options[core.Const.ATTR_TRANSITION] = call.data.get(
                core.Const.ATTR_TRANSITION
            )

        await core.helpers.async_reproduce_states(
            self._shc,
            call.data[core.Const.CONF_ENTITIES].values(),
            context=call.context,
            reproduce_options=reproduce_options,
        )

    async def _create_scene_service(self, call: core.ServiceCall) -> None:
        """Create a scene."""
        snapshot = call.data[_CONF_SNAPSHOT]
        entities = call.data[core.Const.CONF_ENTITIES]

        for entity_id in snapshot:
            if (state := self._shc.states.get(entity_id)) is None:
                _LOGGER.warning(
                    f"Entity {entity_id} does not exist and therefore "
                    + "cannot be snapshotted",
                )
                continue
            entities[entity_id] = core.State(entity_id, state.state, state.attributes)

        if not entities:
            _LOGGER.warning("Empty scenes are not allowed")
            return

        scene_config = SceneConfig(None, call.data[_CONF_SCENE_ID], None, entities)
        entity_id = f"{core.Const.SCENE_COMPONENT_NAME}.{scene_config.name}"
        if (old := self._scene_platform.entities.get(entity_id)) is not None:
            if not isinstance(old, Scene) or not old.from_service:
                _LOGGER.warning(f"The scene {entity_id} already exists")
                return
            await self._scene_platform.async_remove_entity(entity_id)
        self._add_scene_entities([Scene(self._shc, scene_config, from_service=True)])

    async def _reload_scene_config(self, call: core.ServiceCall) -> None:
        """Reload the scene config."""
        try:
            config = await self._shc.setup.async_shc_config_yaml()
        except core.SmartHomeControllerError as err:
            _LOGGER.error(err)
            return

        integration = await self._shc.setup.async_get_integration(
            core.Const.SCENE_COMPONENT_NAME
        )

        conf = await self._shc.setup.async_process_component_config(config, integration)

        if not (conf and self._scene_platform):
            return

        await self._scene_platform.async_reset()

        # Extract only the config for the Home Assistant platform, ignore the rest.
        for p_type, p_config in self._shc.setup.config_per_platform(
            conf, core.Const.SCENE_COMPONENT_NAME
        ):
            if p_type != self.domain:
                continue

            _process_scenes_config(self._shc, self._add_scene_entities, p_config)

        self._shc.bus.async_fire(_EVENT_SCENE_RELOADED, context=call.context)

    async def async_validate_trigger_config(
        self, config: core.ConfigType
    ) -> core.ConfigType:
        """Validate config."""
        platform = self._get_trigger_platform(config)
        if platform is not None:
            return await platform.async_validate_trigger_config(config)
        return config

    def _get_trigger_platform(self, config: core.ConfigType) -> core.TriggerPlatform:
        platform_name = config[core.Const.CONF_PLATFORM]
        if platform_name not in self._trigger_platforms:
            if platform_name == "event":
                self._trigger_platforms["event"] = EventTrigger(self._shc)
            elif platform_name == core.Const.CORE_COMPONENT_NAME:
                self._trigger_platforms[core.Const.CORE_COMPONENT_NAME] = CoreTrigger(
                    self._shc
                )
            elif platform_name == "numeric_state":
                self._trigger_platforms["numeric_state"] = NumericStateTrigger(
                    self._shc
                )
            elif platform_name == "state":
                self._trigger_platforms["state"] = StateTrigger(self._shc)
            elif platform_name == "time":
                self._trigger_platforms["time"] = TimeTrigger(self._shc)
            elif platform_name == "time_pattern":
                self._trigger_platforms["time_pattern"] = TimePatternTrigger(self._shc)

        return self._trigger_platforms.get(platform_name, None)

    async def async_attach_trigger(
        self,
        config: core.ConfigType,
        action: core.TriggerActionType,
        trigger_info: core.TriggerInfo,
    ) -> core.CallbackType:
        """Attach trigger of specified platform."""
        platform = self._get_trigger_platform(config)
        if platform is not None:
            return await platform.async_attach_trigger(config, action, trigger_info)

    def register_system_health_info(self, info: core.SystemHealthRegistration) -> None:
        info.async_register_info(self._system_health_info)

    async def _system_health_info(self):
        """Get info for the info page."""
        info = await core.helpers.async_get_system_info(self._shc)

        return {
            "version": f"core-{info.get('version')}",
            "installation_type": info.get("installation_type"),
            "dev": info.get("dev"),
            "docker": info.get("docker"),
            "user": info.get("user"),
            "virtualenv": info.get("virtualenv"),
            "python_version": info.get("python_version"),
            "os_name": info.get("os_name"),
            "os_version": info.get("os_version"),
            "arch": info.get("arch"),
            "timezone": info.get("timezone"),
        }


def _process_scenes_config(shc: core.SmartHomeController, async_add_entities, config):
    """Process multiple scenes and add them."""
    # Check empty list
    if not (scene_config := config[core.Const.CONF_STATES]):
        return

    async_add_entities(
        Scene(
            shc,
            SceneConfig(
                scene.get(core.Const.CONF_ID),
                scene[core.Const.CONF_NAME],
                scene.get(core.Const.CONF_ICON),
                scene[core.Const.CONF_ENTITIES],
            ),
        )
        for scene in scene_config
    )
