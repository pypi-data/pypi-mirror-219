"""
Script Component for Smart Home - The Next Generation.

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
import contextlib
import logging
import typing

import voluptuous as vol
import voluptuous.humanize as vh

from ... import core
from .const import Const
from .script_config import ScriptConfig
from .script_entity import ScriptEntity

_cv: typing.TypeAlias = core.ConfigValidation
_LOGGER: typing.Final = logging.getLogger(__name__)


# pylint: disable=unused-variable
class ScriptComponent(
    core.ScriptComponent, core.LogbookPlatform, core.RecorderPlatform
):
    """Support for scripts."""

    def __init__(self, path: typing.Iterable[str]):
        super().__init__(path)
        self._component: core.EntityComponent = None
        self._blueprints: core.DomainBlueprintsBase = None
        self._supported_platforms = frozenset(
            [core.Platform.LOGBOOK, core.Platform.RECORDER]
        )
        blueprint = self.controller.components.blueprint
        if isinstance(blueprint, core.BlueprintComponent):
            self._blueprints = blueprint.create_domain_blueprints(
                self.domain, Const.LOGGER
            )

    @property
    def entity_component(self) -> core.EntityComponent:
        return self._component

    def _is_on(self, entity_id):
        """Return if the script is on based on the statemachine."""
        return self._shc.states.is_state(entity_id, core.Const.STATE_ON)

    async def async_setup(self, config: core.ConfigType) -> bool:
        """Load the scripts from the configuration."""
        if not await super().async_setup(config):
            return False

        shc = self._shc
        component = core.EntityComponent(Const.LOGGER, self.domain, shc)
        self._component = component

        # Process integration platforms right away since
        # we will create entities before firing EVENT_COMPONENT_LOADED
        await shc.setup.async_process_integration_platform_for_component(self.domain)

        if not await self._async_process_config(config):
            await self._blueprints.async_populate()

        shc.services.async_register(
            self.domain,
            core.Const.SERVICE_RELOAD,
            self._reload_service,
            schema=Const.RELOAD_SERVICE_SCHEMA,
        )
        shc.services.async_register(
            self.domain,
            core.Const.SERVICE_TURN_ON,
            self._turn_on_service,
            schema=Const.SCRIPT_TURN_ONOFF_SCHEMA,
        )
        shc.services.async_register(
            self.domain,
            core.Const.SERVICE_TURN_OFF,
            self._turn_off_service,
            schema=Const.SCRIPT_TURN_ONOFF_SCHEMA,
        )
        shc.services.async_register(
            self.domain,
            core.Const.SERVICE_TOGGLE,
            self._toggle_service,
            schema=Const.SCRIPT_TURN_ONOFF_SCHEMA,
        )

        return True

    async def async_validate_config(self, config: core.ConfigType) -> core.ConfigType:
        """Validate config."""
        scripts = {}
        for _, p_config in self.controller.setup.config_per_platform(
            config, self.domain
        ):
            for object_id, cfg in p_config.items():
                if object_id in scripts:
                    _LOGGER.warning(
                        f"Duplicate script detected with name: '{object_id}'"
                    )
                    continue
                cfg = await self._try_async_validate_config_item(object_id, cfg, config)
                if cfg is not None:
                    scripts[object_id] = cfg

        # Create a copy of the configuration with all config for current
        # component removed and add validated config back in.
        config = self.controller.setup.config_without_domain(config, self.domain)
        config[self.domain] = scripts

        return config

    async def _try_async_validate_config_item(
        self, object_id, config, full_config=None
    ):
        """Validate config item."""
        raw_config = None
        with contextlib.suppress(ValueError):  # Invalid config
            raw_config = dict(config)

        try:
            _cv.slug(object_id)
            config = await self.async_validate_config_item(config)
        except (vol.Invalid, core.SmartHomeControllerError) as ex:
            self.controller.setup.async_log_exception(
                ex, self.domain, full_config or config
            )
            return None

        if isinstance(config, core.BlueprintInputsBase):
            return config

        config = ScriptConfig(config)
        config.raw_config = raw_config
        return config

    async def async_validate_config_item(
        self, config: core.ConfigType
    ) -> core.ConfigType:
        """Validate config item."""
        blueprint = self.controller.components.blueprint
        if isinstance(
            blueprint, core.BlueprintComponent
        ) and blueprint.is_blueprint_instance_config(config):
            return await self._blueprints.async_inputs_from_config(config)

        config = Const.SCRIPT_ENTITY_SCHEMA(config)
        actions = core.Scripts.get_action_protocol(self._shc)
        config[core.Const.CONF_SEQUENCE] = await actions.async_validate_actions_config(
            config[core.Const.CONF_SEQUENCE]
        )

        return config

    async def _reload_service(self, _service: core.ServiceCall) -> None:
        """Call a service to reload scripts."""
        if (conf := await self._component.async_prepare_reload()) is None:
            return
        if self._blueprints:
            self._blueprints.reset_cache()
        await self._async_process_config(conf)

    async def _turn_on_service(self, service: core.ServiceCall) -> None:
        """Call a service to turn script on."""
        variables = service.data.get(Const.ATTR_VARIABLES)
        script_entities: list[ScriptEntity] = typing.cast(
            list[ScriptEntity],
            await self._component.async_extract_from_service(service),
        )
        for script_entity in script_entities:
            await script_entity.async_turn_on(
                variables=variables, context=service.context, wait=False
            )

    async def _turn_off_service(self, service: core.ServiceCall) -> None:
        """Cancel a script."""
        # Stopping a script is ok to be done in parallel
        script_entities: list[ScriptEntity] = typing.cast(
            list[ScriptEntity],
            await self._component.async_extract_from_service(service),
        )

        if not script_entities:
            return

        await asyncio.wait(
            [
                asyncio.create_task(script_entity.async_turn_off())
                for script_entity in script_entities
            ]
        )

    async def _toggle_service(self, service: core.ServiceCall) -> None:
        """Toggle a script."""
        script_entities: list[ScriptEntity] = typing.cast(
            list[ScriptEntity],
            await self._component.async_extract_from_service(service),
        )
        for script_entity in script_entities:
            await script_entity.async_toggle(context=service.context, wait=False)

    async def _entity_service_handler(self, service: core.ServiceCall) -> None:
        """Execute a service call to script.<script name>."""
        entity_id = f"{self.domain}.{service.service}"
        script_entity = self._component.get_entity(entity_id)
        await script_entity.async_turn_on(
            variables=service.data, context=service.context
        )

    async def _async_process_config(self, config: core.ConfigType) -> bool:
        """Process script configuration.

        Return true, if Blueprints were used.
        """
        shc = self._shc
        component = self._component
        entities: list[ScriptEntity] = []
        blueprints_used = False

        for config_key in shc.setup.extract_domain_configs(config, self.domain):
            conf: dict[str, dict[str, typing.Any] | core.BlueprintInputsBase] = config[
                config_key
            ]

            for object_id, config_block in conf.items():
                raw_blueprint_inputs = None
                raw_config = None

                if isinstance(config_block, core.BlueprintInputsBase):
                    blueprints_used = True
                    blueprint_inputs = config_block
                    raw_blueprint_inputs = blueprint_inputs.config_with_inputs

                    try:
                        raw_config = blueprint_inputs.async_substitute()
                        config_block = typing.cast(
                            dict[str, typing.Any],
                            await self.async_validate_config_item(raw_config),
                        )
                    except vol.Invalid as err:
                        Const.LOGGER.error(
                            f"Blueprint {blueprint_inputs.blueprint.name} generated "
                            + f"invalid script with input {blueprint_inputs.inputs}: "
                            + f"{vh.humanize_error(config_block, err)}",
                        )
                        continue
                else:
                    raw_config = typing.cast(ScriptConfig, config_block).raw_config

                entities.append(
                    ScriptEntity(
                        self, object_id, config_block, raw_config, raw_blueprint_inputs
                    )
                )

        await component.async_add_entities(entities)

        # Register services for all entities that were created successfully.
        for entity in entities:
            self._shc.services.async_register(
                self.domain,
                entity.object_id,
                self._entity_service_handler,
                schema=Const.SCRIPT_SERVICE_SCHEMA,
            )

            # Register the service description
            service_desc = {
                core.Const.CONF_NAME: entity.name,
                core.Const.CONF_DESCRIPTION: entity.description,
                Const.CONF_FIELDS: entity.fields,
            }
            core.Service.async_set_service_schema(
                self._shc, self.domain, entity.object_id, service_desc
            )
        return blueprints_used

    def scripts_with_entity(self, entity_id: str) -> list[str]:
        """Return all scripts that reference the entity."""

        component = self._component

        return [
            script_entity.entity_id
            for script_entity in component.entities
            if entity_id in script_entity.script.referenced_entities
        ]

    def entities_in_script(self, script_entity_id: str) -> list[str]:
        """Return all entities in script."""

        component = self._component

        if (script_entity := component.get_entity(script_entity_id)) is None:
            return []

        return list(script_entity.script.referenced_entities)

    def scripts_with_device(self, device_id: str) -> list[str]:
        """Return all scripts that reference the device."""

        component = self._component

        return [
            script_entity.entity_id
            for script_entity in component.entities
            if device_id in script_entity.script.referenced_devices
        ]

    def devices_in_script(self, script_entity_id: str) -> list[str]:
        """Return all devices in script."""

        component = self._component

        if (script_entity := component.get_entity(script_entity_id)) is None:
            return []

        return list(script_entity.script.referenced_devices)

    def scripts_with_area(self, area_id: str) -> list[str]:
        """Return all scripts that reference the area."""

        component = self._component

        return [
            script_entity.entity_id
            for script_entity in component.entities
            if area_id in script_entity.script.referenced_areas
        ]

    def areas_in_script(self, script_entity_id: str) -> list[str]:
        """Return all areas in a script."""

        component = self._component

        if (script_entity := component.get_entity(script_entity_id)) is None:
            return []

        return list(script_entity.script.referenced_areas)

    def async_describe_events(self, async_describe_event: core.LogbookCallback) -> None:
        async_describe_event(core.Const.EVENT_SCRIPT_STARTED)

    def async_describe_event(self, event: core.LazyPartialState) -> dict[str, str]:
        """Describe the logbook event."""
        data = event.data
        icon = None
        entity = self._component.get_entity(data.get(core.Const.ATTR_ENTITY_ID))
        if entity is not None:
            icon = entity.icon

        return {
            core.Const.LOGBOOK_ENTRY_NAME: data.get(core.Const.ATTR_NAME),
            core.Const.LOGBOOK_ENTRY_MESSAGE: "started",
            core.Const.LOGBOOK_ENTRY_ENTITY_ID: data.get(core.Const.ATTR_ENTITY_ID),
            core.Const.LOGBOOK_ENTRY_CONTEXT_ID: event.context_id,
            core.Const.LOGBOOK_ENTRY_ICON: icon,
        }

    def exclude_attributes(self) -> set[str]:
        """Exclude extra attributes from being recorded in the database."""
        return {
            Const.ATTR_LAST_TRIGGERED,
            core.Const.ATTR_MODE,
            core.Scripts.Const.ATTR_CUR,
            core.Scripts.Const.ATTR_MAX,
            Const.ATTR_LAST_ACTION,
        }
