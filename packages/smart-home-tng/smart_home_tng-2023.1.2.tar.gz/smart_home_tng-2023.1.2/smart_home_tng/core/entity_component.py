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
import datetime
import itertools as it
import logging
import typing

import voluptuous as vol

from .callback import callback
from .config_entry import ConfigEntry
from .config_type import ConfigType
from .config_validation import ConfigValidation as cv
from .const import Const
from .discovery_info_type import DiscoveryInfoType
from .entity import Entity
from .entity_platform import EntityPlatform
from .event import Event
from .platform import Platform
from .platform_implementation import PlatformImplementation
from .registry import Registry
from .service import Service
from .service_call import ServiceCall
from .smart_home_controller_component import SmartHomeControllerComponent
from .smart_home_controller_error import SmartHomeControllerError

_DEFAULT_SCAN_INTERVAL = datetime.timedelta(seconds=15)


if not typing.TYPE_CHECKING:

    class SmartHomeController:
        ...


if typing.TYPE_CHECKING:
    from .smart_home_controller import SmartHomeController


# pylint: disable=unused-variable
class EntityComponent:
    """The EntityComponent manages platforms that manages entities.

    This class has the following responsibilities:
     - Process the configuration and set up a platform based component.
     - Manage the platforms and their entities.
     - Help extract the entities from a service call.
     - Listen for discovery events for platforms related to the domain.
    """

    def __init__(
        self,
        logger: logging.Logger,
        domain: str,
        shc: SmartHomeController,
        scan_interval: datetime.timedelta = _DEFAULT_SCAN_INTERVAL,
    ) -> None:
        """Initialize an entity component."""
        self._logger = logger
        self._shc = shc
        self._domain = domain
        self._scan_interval = scan_interval

        self._config: ConfigType = None

        self._platforms: dict[
            str | tuple[str, datetime.timedelta, str], EntityPlatform
        ] = {domain: self._async_init_entity_platform(domain, None)}
        self.async_add_entities = self._platforms[domain].async_add_entities
        self.add_entities = self._platforms[domain].add_entities

        _INSTANCES[domain] = self

    @property
    def entities(self) -> typing.Iterable[Entity]:
        """Return an iterable that returns all entities."""
        return it.chain.from_iterable(
            platform.entities.values() for platform in self._platforms.values()
        )

    def get_entity(self, entity_id: str) -> Entity:
        """Get an entity."""
        for platform in self._platforms.values():
            entity_obj = platform.entities.get(entity_id)
            if entity_obj is not None:
                return entity_obj
        return None

    def setup(self, config: ConfigType) -> None:
        """Set up a full entity component.

        This doesn't block the executor to protect from deadlocks.
        """
        self._shc.add_job(self.async_setup(config))

    async def async_setup(self, config: ConfigType) -> None:
        """Set up a full entity component.

        Loads the platforms from the config and will listen for supported
        discovered platforms.

        This method must be run in the event loop.
        """
        self._shc.bus.async_listen_once(Const.EVENT_SHC_STOP, self._async_shutdown)

        self._config = config

        # Look in config for Domain, Domain 2, Domain 3 etc and load them
        for p_type, p_config in self._shc.setup.config_per_platform(
            config, self._domain
        ):
            if p_type is not None:
                self._shc.async_create_task(self.async_setup_platform(p_type, p_config))

        # Generic discovery listener for loading platform dynamically
        # Refer to: homeassistant.helpers.discovery.async_load_platform()
        async def component_platform_discovered(
            platform: Platform, info: dict[str, typing.Any]
        ) -> None:
            """Handle the loading of a platform."""
            await self.async_setup_platform(platform, {}, info)

        self._shc.setup.async_listen_platform(
            self._domain, component_platform_discovered
        )

    async def async_setup_entry(self, config_entry: ConfigEntry) -> bool:
        """Set up a config entry."""
        platform_type = config_entry.domain
        platform = await self._shc.setup.async_prepare_setup_platform(
            self._config or {},
            self._domain,
            platform_type,
        )

        if platform is None:
            return False

        key = config_entry.entry_id

        if key in self._platforms:
            raise ValueError("Config entry has already been setup!")

        self._platforms[key] = self._async_init_entity_platform(
            platform_type,
            platform,
            scan_interval=platform.scan_interval,
        )

        return await self._platforms[key].async_setup_entry(config_entry)

    async def async_unload_entry(self, config_entry: ConfigEntry) -> bool:
        """Unload a config entry."""
        key = config_entry.entry_id

        if (platform := self._platforms.pop(key, None)) is None:
            raise ValueError("Config entry was never loaded!")

        await platform.async_reset()
        return True

    async def async_extract_from_service(
        self, service_call: ServiceCall, expand_group: bool = True
    ) -> list[Entity]:
        """Extract all known and available entities from a service call.

        Will return an empty list if entities specified but unknown.

        This method must be run in the event loop.
        """
        return await Service.async_extract_entities(
            self._shc, self.entities, service_call, expand_group
        )

    @callback
    def async_register_entity_service(
        self,
        name: str,
        schema: dict[str, typing.Any] | vol.Schema,
        func: str | collections.abc.Callable[..., typing.Any],
        required_features: list[int] = None,
    ) -> None:
        """Register an entity service."""
        if isinstance(schema, dict):
            schema = cv.make_entity_service_schema(schema)

        async def handle_service(call: ServiceCall) -> None:
            """Handle the service."""
            await Service.entity_service_call(
                self._shc, self._platforms.values(), func, call, required_features
            )

        self._shc.services.async_register(self._domain, name, handle_service, schema)

    async def async_setup_platform(
        self,
        platform_type: str,
        platform_config: ConfigType,
        discovery_info: DiscoveryInfoType = None,
    ) -> None:
        """Set up a platform for this component."""
        if self._config is None:
            raise RuntimeError("async_setup needs to be called first")

        platform = await self._shc.setup.async_prepare_setup_platform(
            self._config, self._domain, platform_type
        )

        if platform is None:
            return

        scan_interval = platform.scan_interval
        domain_scan_interval = None
        if scan_interval is None:
            comp = SmartHomeControllerComponent.get_component(self._domain)
            if comp is not None:
                domain_scan_interval = comp.scan_interval

        # Use config scan interval, fallback to platform if none set
        if scan_interval is None:
            scan_interval = platform_config.get(
                Const.CONF_SCAN_INTERVAL, domain_scan_interval
            )
        entity_namespace = platform_config.get(Const.CONF_ENTITY_NAMESPACE)

        key = (platform_type, scan_interval, entity_namespace)

        if key not in self._platforms:
            self._platforms[key] = self._async_init_entity_platform(
                platform_type, platform, scan_interval, entity_namespace
            )

        await self._platforms[key].async_setup(platform_config, discovery_info)

    async def _async_reset(self) -> None:
        """Remove entities and reset the entity component to initial values.

        This method must be run in the event loop.
        """
        tasks = []

        for key, platform in self._platforms.items():
            if key == self._domain:
                tasks.append(platform.async_reset())
            else:
                tasks.append(platform.async_destroy())

        if tasks:
            await asyncio.gather(*tasks)

        self._platforms = {self._domain: self._platforms[self._domain]}
        self._config = None

    async def async_remove_entity(self, entity_id: str) -> None:
        """Remove an entity managed by one of the platforms."""
        found = None

        for platform in self._platforms.values():
            if entity_id in platform.entities:
                found = platform
                break

        if found:
            await found.async_remove_entity(entity_id)

    async def async_prepare_reload(self, *, skip_reset: bool = False) -> ConfigType:
        """Prepare reloading this entity component.

        This method must be run in the event loop.
        """
        try:
            conf = await self._shc.setup.async_shc_config_yaml()
        except SmartHomeControllerError as err:
            self._logger.error(err)
            return None

        integration = await self._shc.setup.async_get_integration(self._domain)

        processed_conf = await self._shc.setup.async_process_component_config(
            conf, integration
        )

        if processed_conf is None:
            return None

        if not skip_reset:
            await self._async_reset()

        return processed_conf

    @callback
    def _async_init_entity_platform(
        self,
        platform_type: Platform | str,
        platform: PlatformImplementation,
        scan_interval: datetime.timedelta = None,
        entity_namespace: str = None,
    ) -> EntityPlatform:
        """Initialize an entity platform."""
        if scan_interval is None:
            scan_interval = self._scan_interval

        return EntityPlatform(
            shc=self._shc,
            logger=self._logger,
            domain=self._domain,
            platform_name=platform_type,
            platform=platform,
            scan_interval=scan_interval,
            entity_namespace=entity_namespace,
        )

    async def _async_shutdown(self, _event: Event) -> None:
        """Call when Home Assistant is stopping."""
        await asyncio.gather(
            *(
                platform.async_shutdown()
                for platform in it.chain(self._platforms.values())
            )
        )


_INSTANCES: typing.Final[Registry[str, EntityComponent]] = Registry()
