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

import asyncio
import collections.abc
import functools
import logging
import typing

import voluptuous as vol

from ..auth.permissions.const import Const as perm_const
from . import helpers
from .callback import callback
from .config_type import ConfigType
from .config_validation import ConfigValidation as cv
from .const import Const
from .context import Context
from .entity import Entity
from .integration import Integration
from .json_type import JsonType
from .selected_entities import SelectedEntities
from .service_call import ServiceCall
from .service_params import ServiceParams
from .service_target_selector import ServiceTargetSelector
from .smart_home_controller_error import SmartHomeControllerError
from .template import Template
from .template_error import TemplateError
from .template_vars_type import TemplateVarsType
from .unauthorized import Unauthorized
from .unknown_user import UnknownUser
from .yaml_loader import YamlLoader

_LOGGER = logging.getLogger(__name__)
_SERVICE_DESCRIPTION_CACHE: typing.Final = "service_description_cache"


if not typing.TYPE_CHECKING:

    class SmartHomeController:
        pass

    class EntityPlatform:
        pass


if typing.TYPE_CHECKING:
    from .smart_home_controller import SmartHomeController
    from .entity_platform import EntityPlatform


# pylint: disable=unused-variable
class Service:
    """Handle Smart Home - The Next Generation services."""

    @staticmethod
    def call_from_config(
        shc: SmartHomeController,
        config: ConfigType,
        blocking: bool = False,
        variables: TemplateVarsType = None,
        validate_config: bool = True,
    ) -> None:
        """Call a service based on a config hash."""
        shc.run_coroutine_threadsafe(
            Service.async_call_from_config(
                shc, config, blocking, variables, validate_config
            )
        ).result()

    @staticmethod
    async def async_call_from_config(
        shc: SmartHomeController,
        config: ConfigType,
        blocking: bool = False,
        variables: TemplateVarsType = None,
        validate_config: bool = True,
        context: Context = None,
    ) -> None:
        """Call a service based on a config hash."""
        try:
            params = Service.async_prepare_call_from_config(
                shc, config, variables, validate_config
            )
        except SmartHomeControllerError as ex:
            if blocking:
                raise
            _LOGGER.error(ex)
        else:
            await shc.services.async_call(**params, blocking=blocking, context=context)

    @callback
    @staticmethod
    def async_prepare_call_from_config(
        shc: SmartHomeController,
        config: ConfigType,
        variables: TemplateVarsType = None,
        validate_config: bool = False,
    ) -> ServiceParams:
        """Prepare to call a service based on a config hash."""
        if validate_config:
            try:
                config = cv.SERVICE_SCHEMA(config)
            except vol.Invalid as ex:
                raise SmartHomeControllerError(
                    f"Invalid config for calling service: {ex}"
                ) from ex

        if Const.CONF_SERVICE in config:
            domain_service = config[Const.CONF_SERVICE]
        else:
            domain_service = config[Const.CONF_SERVICE_TEMPLATE]

        if isinstance(domain_service, Template):
            try:
                domain_service.controller = shc
                domain_service = domain_service.async_render(variables)
                domain_service = cv.service(domain_service)
            except TemplateError as ex:
                raise SmartHomeControllerError(
                    f"Error rendering service name template: {ex}"
                ) from ex
            except vol.Invalid as ex:
                raise SmartHomeControllerError(
                    f"Template rendered invalid service: {domain_service}"
                ) from ex

        domain, service = domain_service.split(".", 1)

        target = {}
        if Const.CONF_TARGET in config:
            conf = config[Const.CONF_TARGET]
            try:
                if isinstance(conf, Template):
                    conf.controller = shc
                    target.update(conf.async_render(variables))
                else:
                    Template.attach(shc, conf)
                    target.update(Template.render_complex(conf, variables))

                if Const.CONF_ENTITY_ID in target:
                    registry = shc.entity_registry
                    entity_ids = cv.comp_entity_ids_or_uuids(
                        target[Const.CONF_ENTITY_ID]
                    )
                    if entity_ids not in (
                        Const.ENTITY_MATCH_ALL,
                        Const.ENTITY_MATCH_NONE,
                    ):
                        entity_ids = registry.async_validate_entity_ids(entity_ids)
                    target[Const.CONF_ENTITY_ID] = entity_ids
            except TemplateError as ex:
                raise SmartHomeControllerError(
                    f"Error rendering service target template: {ex}"
                ) from ex
            except vol.Invalid as ex:
                raise SmartHomeControllerError(
                    f"Template rendered invalid entity IDs: {target[Const.CONF_ENTITY_ID]}"
                ) from ex

        service_data = {}

        for conf in (Const.CONF_SERVICE_DATA, Const.CONF_SERVICE_DATA_TEMPLATE):
            if conf not in config:
                continue
            try:
                Template.attach(shc, config[conf])
                render = Template.render_complex(config[conf], variables)
                if not isinstance(render, dict):
                    raise SmartHomeControllerError(
                        "Error rendering data template: Result is not a Dictionary"
                    )
                service_data.update(render)
            except TemplateError as ex:
                raise SmartHomeControllerError(
                    f"Error rendering data template: {ex}"
                ) from ex

        if Const.CONF_ENTITY_ID in config:
            if target:
                target[Const.ATTR_ENTITY_ID] = config[Const.CONF_ENTITY_ID]
            else:
                target = {Const.ATTR_ENTITY_ID: config[Const.CONF_ENTITY_ID]}

        return {
            "domain": domain,
            "service": service,
            "service_data": service_data,
            "target": target,
        }

    @staticmethod
    def extract_entity_ids(
        shc: SmartHomeController, service_call: ServiceCall, expand_group: bool = True
    ) -> set[str]:
        """Extract a list of entity ids from a service call.

        Will convert group entity ids to the entity ids it represents.
        """
        return shc.run_coroutine_threadsafe(
            Service.async_extract_entity_ids(shc, service_call, expand_group)
        ).result()

    @staticmethod
    async def async_extract_entities(
        shc: SmartHomeController,
        entities: collections.abc.Iterable[Entity],
        service_call: ServiceCall,
        expand_group: bool = True,
    ) -> list[Entity]:
        """Extract a list of entity objects from a service call.

        Will convert group entity ids to the entity ids it represents.
        """
        data_ent_id = service_call.data.get(Const.ATTR_ENTITY_ID)

        if data_ent_id == Const.ENTITY_MATCH_ALL:
            return [entity for entity in entities if entity.available]

        referenced = Service.async_extract_referenced_entity_ids(
            shc, service_call, expand_group
        )
        combined = referenced.referenced | referenced.indirectly_referenced

        found = []

        for entity in entities:
            if entity.entity_id not in combined:
                continue

            combined.remove(entity.entity_id)

            if not entity.available:
                continue

            found.append(entity)

        referenced.log_missing(referenced.referenced & combined)

        return found

    @staticmethod
    async def async_extract_entity_ids(
        shc: SmartHomeController, service_call: ServiceCall, expand_group: bool = True
    ) -> set[str]:
        """Extract a set of entity ids from a service call.

        Will convert group entity ids to the entity ids it represents.
        """
        referenced = Service.async_extract_referenced_entity_ids(
            shc, service_call, expand_group
        )
        return referenced.referenced | referenced.indirectly_referenced

    @staticmethod
    def async_extract_referenced_entity_ids(
        shc: SmartHomeController, service_call: ServiceCall, expand_group: bool = True
    ) -> SelectedEntities:
        """Extract referenced entity IDs from a service call."""
        selector = ServiceTargetSelector(service_call)
        selected = SelectedEntities()

        if not selector.has_any_selector:
            return selected

        entity_ids = selector.entity_ids
        if expand_group:
            entity_ids = shc.components.group.expand_entity_ids(entity_ids)
            # group = SmartHomeControllerComponent.get_component(Const.GROUP_COMPONENT_NAME)
            # if isinstance(group, GroupComponent):
            #    entity_ids = group.expand_entity_ids(entity_ids)

        selected.referenced.update(entity_ids)

        if not selector.device_ids and not selector.area_ids:
            return selected

        ent_reg = shc.entity_registry
        dev_reg = shc.device_registry
        area_reg = shc.area_registry

        for device_id in selector.device_ids:
            if device_id not in dev_reg.devices:
                selected.missing_devices.add(device_id)

        for area_id in selector.area_ids:
            if area_id not in area_reg.areas:
                selected.missing_areas.add(area_id)

        # Find devices for targeted areas
        selected.referenced_devices.update(selector.device_ids)
        for device_entry in dev_reg.devices.values():
            if device_entry.area_id in selector.area_ids:
                selected.referenced_devices.add(device_entry.id)

        if not selector.area_ids and not selected.referenced_devices:
            return selected

        for ent_entry in ent_reg.entities.values():
            # Do not add entities which are hidden or which are config or diagnostic entities
            if ent_entry.entity_category is not None or ent_entry.hidden_by is not None:
                continue

            if (
                # The entity's area matches a targeted area
                ent_entry.area_id in selector.area_ids
                # The entity's device matches a device referenced by an area and the entity
                # has no explicitly set area
                or (
                    not ent_entry.area_id
                    and ent_entry.device_id in selected.referenced_devices
                )
                # The entity's device matches a targeted device
                or ent_entry.device_id in selector.device_ids
            ):
                selected.indirectly_referenced.add(ent_entry.entity_id)

        return selected

    @staticmethod
    async def async_extract_config_entry_ids(
        shc: SmartHomeController, service_call: ServiceCall, expand_group: bool = True
    ) -> set:
        """Extract referenced config entry ids from a service call."""
        referenced = Service.async_extract_referenced_entity_ids(
            shc, service_call, expand_group
        )
        ent_reg = shc.entity_registry
        dev_reg = shc.device_registry
        config_entry_ids: set[str] = set()

        # Some devices may have no entities
        for device_id in referenced.referenced_devices:
            if (
                device_id in dev_reg.devices
                and (device := dev_reg.async_get(device_id)) is not None
            ):
                config_entry_ids.update(device.config_entries)

        for entity_id in referenced.referenced | referenced.indirectly_referenced:
            entry = ent_reg.async_get(entity_id)
            if entry is not None and entry.config_entry_id is not None:
                config_entry_ids.add(entry.config_entry_id)

        return config_entry_ids

    @staticmethod
    def _load_services_file(
        _shc: SmartHomeController, integration: Integration
    ) -> JsonType:
        """Load services file for an integration."""
        try:
            return YamlLoader.load_yaml(str(integration.file_path / "services.yaml"))
        except FileNotFoundError:
            _LOGGER.warning(
                f"Unable to find services.yaml for the {integration.domain} integration"
            )
            return {}
        except SmartHomeControllerError:
            _LOGGER.warning(
                f"Unable to parse services.yaml for the {integration.domain} integration"
            )
            return {}

    @staticmethod
    def _load_services_files(
        shc: SmartHomeController, integrations: collections.abc.Iterable[Integration]
    ) -> list[JsonType]:
        """Load service files for multiple intergrations."""
        return [
            Service._load_services_file(shc, integration)
            for integration in integrations
        ]

    @staticmethod
    async def async_get_all_descriptions(
        shc: SmartHomeController,
    ) -> dict[str, dict[str, typing.Any]]:
        """Return descriptions (i.e. user documentation) for all service calls."""
        descriptions_cache = shc.data.setdefault(_SERVICE_DESCRIPTION_CACHE, {})
        format_cache_key = "{}.{}".format
        services = shc.services.async_services()

        # See if there are new services not seen before.
        # Any service that we saw before already has an entry in description_cache.
        missing = set()
        for domain in services:
            for service in services[domain]:
                if format_cache_key(domain, service) not in descriptions_cache:
                    missing.add(domain)
                    break

        # Files we loaded for missing descriptions
        loaded = {}

        if missing:
            integrations = await helpers.gather_with_concurrency(
                Const.MAX_LOAD_CONCURRENTLY,
                *(shc.setup.async_get_integration(domain) for domain in missing),
            )

            contents = await shc.async_add_executor_job(
                Service._load_services_files, shc, integrations
            )

            for domain, content in zip(missing, contents):
                loaded[domain] = content

        # Build response
        descriptions: dict[str, dict[str, typing.Any]] = {}
        for domain in services:
            descriptions[domain] = {}

            for service in services[domain]:
                cache_key = format_cache_key(domain, service)
                description = descriptions_cache.get(cache_key)

                # Cache missing descriptions
                if description is None:
                    domain_yaml = loaded[domain]
                    yaml_description = domain_yaml.get(service, {})  # type: ignore[union-attr]

                    # Don't warn for missing services, because it triggers false
                    # positives for things like scripts, that register as a service

                    description = {
                        "name": yaml_description.get("name", ""),
                        "description": yaml_description.get("description", ""),
                        "fields": yaml_description.get("fields", {}),
                    }

                    if "target" in yaml_description:
                        description["target"] = yaml_description["target"]

                    descriptions_cache[cache_key] = description

                descriptions[domain][service] = description

        return descriptions

    @staticmethod
    @callback
    def async_set_service_schema(
        shc: SmartHomeController,
        domain: str,
        service: str,
        schema: dict[str, typing.Any],
    ) -> None:
        """Register a description for a service."""
        shc.data.setdefault(_SERVICE_DESCRIPTION_CACHE, {})

        description = {
            "name": schema.get("name", ""),
            "description": schema.get("description", ""),
            "fields": schema.get("fields", {}),
        }

        if "target" in schema:
            description["target"] = schema["target"]

        shc.data[_SERVICE_DESCRIPTION_CACHE][f"{domain}.{service}"] = description

    @staticmethod
    async def entity_service_call(
        shc: SmartHomeController,
        platforms: collections.abc.Iterable[EntityPlatform],
        func: str | collections.abc.Callable[..., typing.Any],
        call: ServiceCall,
        required_features: collections.abc.Iterable[int] = None,
    ) -> None:
        """Handle an entity service call.

        Calls all platforms simultaneously.
        """
        if call.context.user_id:
            user = await shc.auth.async_get_user(call.context.user_id)
            if user is None:
                raise UnknownUser(context=call.context)
            entity_perms: None | (
                collections.abc.Callable[[str, str], bool]
            ) = user.permissions.check_entity
        else:
            entity_perms = None

        target_all_entities = (
            call.data.get(Const.ATTR_ENTITY_ID) == Const.ENTITY_MATCH_ALL
        )

        if target_all_entities:
            referenced: SelectedEntities = None
            all_referenced: set[str] = None
        else:
            # A set of entities we're trying to target.
            referenced = Service.async_extract_referenced_entity_ids(shc, call, True)
            all_referenced = referenced.referenced | referenced.indirectly_referenced

        # If the service function is a string, we'll pass it the service call data
        if isinstance(func, str):
            data: dict | ServiceCall = {
                key: val
                for key, val in call.data.items()
                if key not in cv.ENTITY_SERVICE_FIELDS
            }
        # If the service function is not a string, we pass the service call
        else:
            data = call

        # Check the permissions

        # A list with entities to call the service on.
        entity_candidates: list[Entity] = []

        if entity_perms is None:
            for platform in platforms:
                if target_all_entities:
                    entity_candidates.extend(platform.entities.values())
                else:
                    assert all_referenced is not None
                    entity_candidates.extend(
                        [
                            entity
                            for entity in platform.entities.values()
                            if entity.entity_id in all_referenced
                        ]
                    )

        elif target_all_entities:
            # If we target all entities, we will select all entities the user
            # is allowed to control.
            for platform in platforms:
                entity_candidates.extend(
                    [
                        entity
                        for entity in platform.entities.values()
                        if entity_perms(entity.entity_id, perm_const.POLICY_CONTROL)
                    ]
                )

        else:
            assert all_referenced is not None

            for platform in platforms:
                platform_entities = []
                for entity in platform.entities.values():
                    if entity.entity_id not in all_referenced:
                        continue

                    if not entity_perms(entity.entity_id, perm_const.POLICY_CONTROL):
                        raise Unauthorized(
                            context=call.context,
                            entity_id=entity.entity_id,
                            permission=perm_const.POLICY_CONTROL,
                        )

                    platform_entities.append(entity)

                entity_candidates.extend(platform_entities)

        if not target_all_entities:
            assert referenced is not None

            # Only report on explicit referenced entities
            missing = set(referenced.referenced)

            for entity in entity_candidates:
                missing.discard(entity.entity_id)

            referenced.log_missing(missing)

        entities = []

        for entity in entity_candidates:
            if not entity.available:
                continue

            # Skip entities that don't have the required feature.
            if required_features is not None and (
                entity.supported_features is None
                or not any(
                    entity.supported_features & feature_set == feature_set
                    for feature_set in required_features
                )
            ):
                # If entity explicitly referenced, raise an error
                if referenced is not None and entity.entity_id in referenced.referenced:
                    raise SmartHomeControllerError(
                        f"Entity {entity.entity_id} does not support this service."
                    )

                continue

            entities.append(entity)

        if not entities:
            return

        done, pending = await asyncio.wait(
            [
                asyncio.create_task(
                    entity.async_request_call(
                        Service._handle_entity_call(
                            shc, entity, func, data, call.context
                        )
                    )
                )
                for entity in entities
            ]
        )
        assert not pending
        for future in done:
            future.result()  # pop exception if have

        tasks = []

        for entity in entities:
            if not entity.should_poll:
                continue

            # Context expires if the turn on commands took a long time.
            # Set context again so it's there when we update
            entity.async_set_context(call.context)
            tasks.append(asyncio.create_task(entity.async_update_state(True)))

        if tasks:
            done, pending = await asyncio.wait(tasks)
            assert not pending
            for future in done:
                future.result()  # pop exception if have

    @staticmethod
    async def _handle_entity_call(
        shc: SmartHomeController,
        entity: Entity,
        func: str | collections.abc.Callable[..., typing.Any],
        data: dict | ServiceCall,
        context: Context,
    ) -> None:
        """Handle calling service method."""
        entity.async_set_context(context)

        if isinstance(func, str):
            result = shc.async_run_job(functools.partial(getattr(entity, func), **data))
        else:
            result = shc.async_run_job(func, entity, data)

        # Guard because callback functions do not return a task when passed to async_run_job.
        if result is not None:
            await result

        if asyncio.iscoroutine(result):
            _LOGGER.error(
                f"Service {func} for {entity.entity_id} incorrectly returns a coroutine object. "
                + "Await result instead in service handler. Report bug to integration author",
            )
            await result

    @staticmethod
    @callback
    def async_register_admin_service(
        shc: SmartHomeController,
        domain: str,
        service: str,
        service_func: collections.abc.Callable[
            [ServiceCall], collections.abc.Awaitable[None]
        ],
        schema: vol.Schema = vol.Schema({}, extra=vol.PREVENT_EXTRA),
    ) -> None:
        """Register a service that requires admin access."""

        @functools.wraps(service_func)
        async def admin_handler(call: ServiceCall) -> None:
            if call.context.user_id:
                user = await shc.auth.async_get_user(call.context.user_id)
                if user is None:
                    raise UnknownUser(context=call.context)
                if not user.is_admin:
                    raise Unauthorized(context=call.context)

            result = shc.async_run_job(service_func, call)
            if result is not None:
                await result

        shc.services.async_register(domain, service, admin_handler, schema)

    @staticmethod
    @callback
    def verify_domain_control(
        shc: SmartHomeController, domain: str
    ) -> collections.abc.Callable[
        [collections.abc.Callable[[ServiceCall], typing.Any]],
        collections.abc.Callable[[ServiceCall], typing.Any],
    ]:
        """Ensure permission to access any entity under domain in service call."""

        def decorator(
            service_handler: collections.abc.Callable[[ServiceCall], typing.Any]
        ) -> collections.abc.Callable[[ServiceCall], typing.Any]:
            """Decorate."""
            if not asyncio.iscoroutinefunction(service_handler):
                raise SmartHomeControllerError("Can only decorate async functions.")

            async def check_permissions(call: ServiceCall) -> typing.Any:
                """Check user permission and raise before call if unauthorized."""
                if not call.context.user_id:
                    return await service_handler(call)

                user = await shc.auth.async_get_user(call.context.user_id)

                if user is None:
                    raise UnknownUser(
                        context=call.context,
                        permission=perm_const.POLICY_CONTROL,
                        user_id=call.context.user_id,
                    )

                reg = shc.entity_registry

                authorized = False

                for entity in reg.entities.values():
                    if entity.platform != domain:
                        continue

                    if user.permissions.check_entity(
                        entity.entity_id, perm_const.POLICY_CONTROL
                    ):
                        authorized = True
                        break

                if not authorized:
                    raise Unauthorized(
                        context=call.context,
                        permission=perm_const.POLICY_CONTROL,
                        user_id=call.context.user_id,
                        perm_category=perm_const.CAT_ENTITIES,
                    )

                return await service_handler(call)

            return check_permissions

        return decorator
