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
import contextvars
import datetime
import logging
import typing

import voluptuous as vol
from urllib3.util import parse_url

from . import helpers
from .callback import callback
from .callback_type import CallbackType
from .config_entry import ConfigEntry
from .config_type import ConfigType
from .config_validation import ConfigValidation as cv
from .const import Const
from .core_state import CoreState
from .device_registry import DeviceRegistry
from .discovery_info_type import DiscoveryInfoType
from .entity_registry import EntityRegistry
from .entity_registry_entry_disabler import EntityRegistryEntryDisabler
from .entity_registry_entry_hider import EntityRegistryEntryHider
from .platform import Platform
from .platform_implementation import PlatformImplementation
from .platform_not_ready import PlatformNotReady
from .required_parameter_missing import RequiredParameterMissing
from .service import Service
from .service_call import ServiceCall
from .smart_home_controller_error import SmartHomeControllerError

_DATA_ENTITY_PLATFORM: typing.Final = "entity_platform"
_SLOW_SETUP_WARNING: typing.Final = 15
_SLOW_SETUP_MAX_WAIT: typing.Final = 60
_SLOW_ADD_ENTITY_MAX_WAIT: typing.Final = 15  # Per Entity
_SLOW_ADD_MIN_TIMEOUT: typing.Final = 500

_PLATFORM_NOT_READY_BASE_WAIT_TIME: typing.Final = 30  # seconds


if not typing.TYPE_CHECKING:

    class SmartHomeController:
        pass

    class Entity:
        pass


if typing.TYPE_CHECKING:
    from .entity import Entity
    from .smart_home_controller import SmartHomeController


# pylint: disable=unused-variable
class EntityPlatform:
    """Manage the entities for a single platform."""

    def __init__(
        self,
        *,
        shc: SmartHomeController,
        logger: logging.Logger,
        domain: str,
        platform_name: Platform | str,
        platform: PlatformImplementation,
        scan_interval: datetime.timedelta,
        entity_namespace: str,
    ) -> None:
        """Initialize the entity platform."""
        self._shc = shc
        self._logger = logger
        self._domain = domain
        self._platform_name = platform_name
        self._platform = platform
        self._scan_interval = scan_interval
        self._entity_namespace = entity_namespace
        self._config_entry: ConfigEntry = None
        self._entities: dict[str, Entity] = {}
        self._tasks: list[asyncio.Future] = []
        # Stop tracking tasks after setup is completed
        self._setup_complete = False
        # Method to cancel the state change listener
        self._async_unsub_polling: CallbackType = None
        # Method to cancel the retry of setup
        self._async_cancel_retry_setup: CallbackType = None
        self._process_updates: asyncio.Lock = None

        self._parallel_updates: asyncio.Semaphore = None

        # Platform is None for the EntityComponent "catch-all" EntityPlatform
        # which powers entity_component.add_entities
        self._parallel_updates_created = platform is None

        shc.data.setdefault(_DATA_ENTITY_PLATFORM, {}).setdefault(
            self.platform_name, []
        ).append(self)

    @property
    def logger(self) -> logging.Logger:
        return self._logger

    @property
    def domain(self) -> str:
        return self._domain

    @property
    def platform_name(self) -> str:
        return str(self._platform_name)

    @property
    def platform(self) -> PlatformImplementation:
        return self._platform

    @property
    def scan_interval(self) -> datetime.timedelta:
        return self._scan_interval

    @property
    def entity_namespace(self) -> str:
        return self._entity_namespace

    @property
    def config_entry(self) -> ConfigEntry:
        return self._config_entry

    @property
    def entities(self) -> dict[str, Entity]:
        return self._entities

    @property
    def parallel_updates(self) -> asyncio.Semaphore:
        return self._parallel_updates

    @property
    def parallel_updates_created(self) -> bool:
        return self._parallel_updates_created

    def __repr__(self) -> str:
        """Represent an EntityPlatform."""
        return (
            f"<EntityPlatform domain={self._domain} platform_name="
            + f"{self.platform_name} config_entry={self._config_entry}>"
        )

    @callback
    def _get_parallel_updates_semaphore(
        self, entity_has_sync_update: bool
    ) -> asyncio.Semaphore:
        """Get or create a semaphore for parallel updates.

        Semaphore will be created on demand because we base it off if update
        method is async or not.

        If parallel updates is set to 0, we skip the semaphore.
        If parallel updates is set to a number, we initialize the semaphore to
        that number.
        The default value for parallel requests is decided based on the first
        entity that is added to the Smart Home Controller.
        It's 0 if the entity defines the async_update method, else it's 1.
        """
        if self.parallel_updates_created:
            return self.parallel_updates

        self._parallel_updates_created = True

        parallel_updates = self.platform.parallel_updates

        if parallel_updates is None and entity_has_sync_update:
            parallel_updates = 1

        if parallel_updates == 0:
            parallel_updates = None

        if parallel_updates is not None:
            self._parallel_updates = asyncio.Semaphore(parallel_updates)

        return self.parallel_updates

    async def async_setup(
        self,
        platform_config: ConfigType,
        discovery_info: DiscoveryInfoType = None,
    ) -> None:
        """Set up the platform from a config file."""
        platform = self.platform

        if platform is None:
            self.logger.error(
                f"The {self.platform_name} platform for the {self.domain} "
                + "integration does not support platform setup. Please remove "
                + "it from your config.",
            )
            return

        @callback
        def async_create_setup_task() -> collections.abc.Coroutine:
            """Get task to set up platform."""
            return platform.async_setup_platform(
                platform_config,
                self._async_schedule_add_entities,
                discovery_info,
            )

        await self._async_setup_platform(async_create_setup_task)

    async def async_shutdown(self) -> None:
        """Call when Home Assistant is stopping."""
        self.async_cancel_retry_setup()
        self.async_unsub_polling()

    @callback
    def async_cancel_retry_setup(self) -> None:
        """Cancel retry setup."""
        if self._async_cancel_retry_setup is not None:
            self._async_cancel_retry_setup()
            self._async_cancel_retry_setup = None

    async def async_setup_entry(self, config_entry: ConfigEntry) -> bool:
        """Set up the platform from a config entry."""
        # Store it so that we can save config entry ID in entity registry
        self._config_entry = config_entry
        platform = self.platform

        @callback
        def async_create_setup_task() -> collections.abc.Coroutine:
            """Get task to set up platform."""
            ConfigEntry.current_entry().set(config_entry)
            return platform.async_setup_platform_devices(
                config_entry, self._async_schedule_add_entities
            )

        return await self._async_setup_platform(async_create_setup_task)

    async def _async_setup_platform(
        self,
        async_create_setup_task: collections.abc.Callable[
            [], collections.abc.Coroutine
        ],
        tries: int = 0,
    ) -> bool:
        """Set up a platform via config file or config entry.

        async_create_setup_task creates a coroutine that sets up platform.
        """
        _current_platform.set(self)
        logger = self._logger
        shc = self._shc
        full_name = f"{self.domain}.{self.platform_name}"

        logger.info(f"Setting up {full_name}")
        warn_task = shc.call_later(
            _SLOW_SETUP_WARNING,
            logger.warning,
            f"Setup of {self.domain} platform {self.platform_name} is taking "
            + f"over {_SLOW_SETUP_WARNING} seconds.",
        )
        with shc.setup.async_start_setup([full_name]):
            try:
                task = async_create_setup_task()

                async with shc.timeout.async_timeout(_SLOW_SETUP_MAX_WAIT, self.domain):
                    await asyncio.shield(task)

                # Block till all entities are done
                while self._tasks:
                    pending = [task for task in self._tasks if not task.done()]
                    self._tasks.clear()

                    if pending:
                        await asyncio.gather(*pending)

                shc.config.component_loaded(full_name)
                self._setup_complete = True
                return True
            except PlatformNotReady as ex:
                tries += 1
                wait_time = min(tries, 6) * _PLATFORM_NOT_READY_BASE_WAIT_TIME
                message = str(ex)
                ready_message = f"ready yet: {message}" if message else "ready yet"
                if tries == 1:
                    logger.warning(
                        f"Platform {self.platform_name} not {ready_message}; "
                        + f"Retrying in background in {wait_time:d} seconds"
                    )
                else:
                    logger.debug(
                        f"Platform {self.platform_name} not {ready_message}; "
                        + f"Retrying in {wait_time:d} seconds"
                    )

                async def setup_again(*_args: typing.Any) -> None:
                    """Run setup again."""
                    self._async_cancel_retry_setup = None
                    await self._async_setup_platform(async_create_setup_task, tries)

                if shc.state == CoreState.RUNNING:
                    self._async_cancel_retry_setup = shc.tracker.async_call_later(
                        wait_time, setup_again
                    )
                else:
                    self._async_cancel_retry_setup = shc.bus.async_listen_once(
                        Const.EVENT_SHC_STARTED, setup_again
                    )
                return False
            except asyncio.TimeoutError:
                logger.error(
                    f"Setup of platform {self.platform_name} is taking longer than "
                    + f"{_SLOW_SETUP_MAX_WAIT} seconds. "
                    + " Startup will proceed without waiting any longer.",
                )
                return False
            except Exception:  # pylint: disable=broad-except
                logger.exception(
                    f"Error while setting up {self.platform_name} platform "
                    + f"for {self.domain}",
                )
                return False
            finally:
                warn_task.cancel()

    def _schedule_add_entities(
        self,
        new_entities: collections.abc.Iterable[Entity],
        update_before_add: bool = False,
    ) -> None:
        """Schedule adding entities for a single platform, synchronously."""
        self._shc.run_callback_threadsafe(
            self._async_schedule_add_entities,
            list(new_entities),
            update_before_add,
        ).result()

    @callback
    def _async_schedule_add_entities(
        self,
        new_entities: collections.abc.Iterable[Entity],
        update_before_add: bool = False,
    ) -> None:
        """Schedule adding entities for a single platform async."""
        task = self._shc.async_create_task(
            self.async_add_entities(new_entities, update_before_add=update_before_add),
        )

        if not self._setup_complete:
            self._tasks.append(task)

    def add_entities(
        self,
        new_entities: collections.abc.Iterable[Entity],
        update_before_add: bool = False,
    ) -> None:
        """Add entities for a single platform."""
        # That avoid deadlocks
        if update_before_add:
            self.logger.warning(
                "Call 'add_entities' with update_before_add=True "
                + "only inside tests or you can run into a deadlock!"
            )

        self._shc.run_coroutine_threadsafe(
            self.async_add_entities(list(new_entities), update_before_add),
        ).result()

    async def async_add_entities(
        self,
        new_entities: collections.abc.Iterable[Entity],
        update_before_add: bool = False,
    ) -> None:
        """Add entities for a single platform async.

        This method must be run in the event loop.
        """
        # handle empty list from component/platform
        if not new_entities:
            return

        shc = self._shc

        device_registry = shc.device_registry
        entity_registry = shc.entity_registry
        tasks = [
            self._async_add_entity(
                entity, update_before_add, entity_registry, device_registry
            )
            for entity in new_entities
        ]

        # No entities for processing
        if not tasks:
            return

        timeout = max(_SLOW_ADD_ENTITY_MAX_WAIT * len(tasks), _SLOW_ADD_MIN_TIMEOUT)
        try:
            async with shc.timeout.async_timeout(timeout, self.domain):
                await asyncio.gather(*tasks)
        except asyncio.TimeoutError:
            self.logger.warning(
                f"Timed out adding entities for domain {self.domain} with platform "
                + f"{self.platform_name} after {timeout:d}s",
            )
        except Exception:
            self.logger.exception(
                f"Error adding entities for domain {self.domain} with platform "
                + f"{self.platform_name}",
            )
            raise

        if (
            (self.config_entry and self.config_entry.pref_disable_polling)
            or self._async_unsub_polling is not None
            or not any(entity.should_poll for entity in self.entities.values())
        ):
            return

        self._async_unsub_polling = self._shc.tracker.async_track_time_interval(
            self._update_entity_states,
            self.scan_interval,
        )

    async def _async_add_entity(
        self,
        entity: Entity,
        update_before_add: bool,
        entity_registry: EntityRegistry,
        device_registry: DeviceRegistry,
    ) -> None:
        """Add an entity to the platform."""
        if entity is None:
            raise ValueError("Entity cannot be None")

        entity.add_to_platform_start(
            self._shc,
            self,
            self._get_parallel_updates_semaphore(hasattr(entity, "update")),
        )

        # Update properties before we generate the entity_id
        if update_before_add:
            try:
                await entity.async_device_update(warning=False)
            except Exception:  # pylint: disable=broad-except
                self.logger.exception(f"{self.platform_name}: Error on device update!")
                entity.add_to_platform_abort()
                return

        requested_entity_id = None
        suggested_object_id: str = None
        generate_new_entity_id = False

        # Get entity_id from unique ID registration
        if entity.unique_id is not None:
            if entity.entity_id is not None:
                requested_entity_id = entity.entity_id
                suggested_object_id = helpers.split_entity_id(entity.entity_id)[1]
            else:
                suggested_object_id = entity.name

            if self.entity_namespace is not None:
                suggested_object_id = f"{self.entity_namespace} {suggested_object_id}"

            if self.config_entry is not None:
                config_entry_id: str = self.config_entry.entry_id
            else:
                config_entry_id = None

            device_info = entity.device_info
            device_id = None
            device = None

            if device_info is not None:
                processed_dev_info: dict[str, str] = {}
                if config_entry_id is not None:
                    processed_dev_info["config_entry_id"] = config_entry_id
                for key in (
                    "connections",
                    "default_manufacturer",
                    "default_model",
                    "default_name",
                    "entry_type",
                    "identifiers",
                    "manufacturer",
                    "model",
                    "name",
                    "suggested_area",
                    "sw_version",
                    "hw_version",
                    "via_device",
                ):
                    if key in device_info:
                        processed_dev_info[key] = device_info[key]

                if "configuration_url" in device_info:
                    if device_info["configuration_url"] is None:
                        processed_dev_info["configuration_url"] = None
                    else:
                        configuration_url = str(device_info["configuration_url"])
                        if parse_url(configuration_url).scheme in [
                            "http",
                            "https",
                            "smart-home-controller",
                        ]:
                            processed_dev_info["configuration_url"] = configuration_url
                        else:
                            self.logger.warning(
                                "Ignoring invalid device configuration_url "
                                + f"'{configuration_url}'"
                            )

                try:
                    device = device_registry.async_get_or_create(**processed_dev_info)
                    device_id = device.id
                except RequiredParameterMissing:
                    pass

            if entity.entity_id is not None:
                requested_entity_id = entity.entity_id
                suggested_object_id = helpers.split_entity_id(entity.entity_id)[1]
            else:
                if device and entity.has_entity_name:  # type: ignore[unreachable]
                    device_name = device.name_by_user or device.name
                    if not entity.name:
                        suggested_object_id = device_name
                    else:
                        suggested_object_id = f"{device_name} {entity.name}"
                if not suggested_object_id:
                    suggested_object_id = entity.name

            if self.entity_namespace is not None:
                suggested_object_id = f"{self.entity_namespace} {suggested_object_id}"

            disabled_by: EntityRegistryEntryDisabler = None
            if not entity.entity_registry_enabled_default:
                disabled_by = EntityRegistryEntryDisabler.INTEGRATION

            hidden_by: EntityRegistryEntryHider = None
            if not entity.entity_registry_visible_default:
                hidden_by = EntityRegistryEntryHider.INTEGRATION

            entry = entity_registry.async_get_or_create(
                self.domain,
                self.platform_name,
                entity.unique_id,
                capabilities=entity.capability_attributes,
                config_entry=self.config_entry,
                device_id=device_id,
                disabled_by=disabled_by,
                entity_category=entity.entity_category,
                hidden_by=hidden_by,
                known_object_ids=self.entities.keys(),
                has_entity_name=entity.has_entity_name,
                original_device_class=entity.device_class,
                original_icon=entity.icon,
                original_name=entity.name,
                suggested_object_id=suggested_object_id,
                supported_features=entity.supported_features,
                unit_of_measurement=entity.unit_of_measurement,
            )

            if device and device.disabled and not entry.disabled:
                entry = entity_registry.async_update_entity(
                    entry.entity_id, disabled_by=EntityRegistryEntryDisabler.DEVICE
                )

            # pylint: disable=protected-access
            entity._registry_entry = entry
            entity._entity_id = entry.entity_id

            if entry.disabled:
                self.logger.debug(
                    "Not adding entity %s because it's disabled",
                    entry.name
                    or entity.name
                    or f'"{self.platform_name} {entity.unique_id}"',
                )
                entity.add_to_platform_abort()
                return

        # We won't generate an entity ID if the platform has already set one
        # We will however make sure that platform cannot pick a registered ID
        elif entity.entity_id is not None and entity_registry.async_is_registered(
            entity.entity_id
        ):
            # If entity already registered, convert entity id to suggestion
            suggested_object_id = helpers.split_entity_id(entity.entity_id)[1]
            generate_new_entity_id = True

        # Generate entity ID
        if entity.entity_id is None or generate_new_entity_id:
            suggested_object_id = (
                suggested_object_id or entity.name or Const.DEVICE_DEFAULT_NAME
            )

            if self.entity_namespace is not None:
                suggested_object_id = f"{self.entity_namespace}.{suggested_object_id}"
            entity.entity_id = entity_registry.async_generate_entity_id(
                self.domain, suggested_object_id, self.entities.keys()
            )

        # Make sure it is valid in case an entity set the value themselves
        if not helpers.valid_entity_id(entity.entity_id):
            entity.add_to_platform_abort()
            raise SmartHomeControllerError(f"Invalid entity ID: {entity.entity_id}")

        already_exists = entity.entity_id in self.entities
        restored = False

        if not already_exists and not self._shc.states.async_available(
            entity.entity_id
        ):
            existing = self._shc.states.get(entity.entity_id)
            if existing is not None and Const.ATTR_RESTORED in existing.attributes:
                restored = True
            else:
                already_exists = True

        if already_exists:
            if entity.unique_id is not None:
                msg = f"Platform {self.platform_name} does not generate unique IDs. "
                if requested_entity_id:
                    msg += (
                        f"ID {entity.unique_id} is already used by {entity.entity_id}"
                        + f" - ignoring {requested_entity_id}"
                    )
                else:
                    msg += (
                        f"ID {entity.unique_id} already exists - ignoring "
                        + f"{entity.entity_id}"
                    )
            else:
                msg = f"Entity id already exists - ignoring: {entity.entity_id}"
            self.logger.error(msg)
            entity.add_to_platform_abort()
            return

        entity_id = entity.entity_id
        self.entities[entity_id] = entity

        if not restored:
            # Reserve the state in the state machine
            # because as soon as we return control to the event
            # loop below, another entity could be added
            # with the same id before `entity.add_to_platform_finish()`
            # has a chance to finish.
            self._shc.states.async_reserve(entity.entity_id)

        def remove_entity_cb() -> None:
            """Remove entity from entities dict."""
            self.entities.pop(entity_id)

        entity.async_on_remove(remove_entity_cb)

        await entity.add_to_platform_finish()

    async def async_reset(self) -> None:
        """Remove all entities and reset data.

        This method must be run in the event loop.
        """
        self.async_cancel_retry_setup()

        if not self.entities:
            return

        tasks = [entity.async_remove() for entity in self.entities.values()]

        await asyncio.gather(*tasks)

        self.async_unsub_polling()
        self._setup_complete = False

    @callback
    def async_unsub_polling(self) -> None:
        """Stop polling."""
        if self._async_unsub_polling is not None:
            self._async_unsub_polling()
            self._async_unsub_polling = None

    async def async_destroy(self) -> None:
        """Destroy an entity platform.

        Call before discarding the object.
        """
        await self.async_reset()
        self._shc.data[_DATA_ENTITY_PLATFORM][self.platform_name].remove(self)

    async def async_remove_entity(self, entity_id: str) -> None:
        """Remove entity id from platform."""
        await self.entities[entity_id].async_remove()

        # Clean up polling job if no longer needed
        if self._async_unsub_polling is not None and not any(
            entity.should_poll for entity in self.entities.values()
        ):
            self._async_unsub_polling()
            self._async_unsub_polling = None

    async def async_extract_from_service(
        self, service_call: ServiceCall, expand_group: bool = True
    ) -> list[Entity]:
        """Extract all known and available entities from a service call.

        Will return an empty list if entities specified but unknown.

        This method must be run in the event loop.
        """
        return await Service.async_extract_entities(
            self._shc, self.entities.values(), service_call, expand_group
        )

    @callback
    def async_register_entity_service(
        self,
        name: str,
        schema: dict | vol.Schema,
        func: str | collections.abc.Callable[..., typing.Any],
        required_features: collections.abc.Iterable[int] = None,
    ) -> None:
        """Register an entity service.

        Services will automatically be shared by all platforms of the same domain.
        """
        if self._shc.services.has_service(self.platform_name, name):
            return

        if isinstance(schema, dict):
            schema = cv.make_entity_service_schema(schema)

        async def handle_service(call: ServiceCall) -> None:
            """Handle the service."""
            await Service.entity_service_call(
                self._shc,
                [
                    plf
                    for plf in self._shc.data[_DATA_ENTITY_PLATFORM][self.platform_name]
                    if plf.domain == self.domain
                ],
                func,
                call,
                required_features,
            )

        self._shc.services.async_register(
            self.platform_name, name, handle_service, schema
        )

    async def _update_entity_states(self, _now: datetime) -> None:
        """Update the states of all the polling entities.

        To protect from flooding the executor, we will update async entities
        in parallel and other entities sequential.

        This method must be run in the event loop.
        """
        if self._process_updates is None:
            self._process_updates = asyncio.Lock()
        if self._process_updates.locked():
            self.logger.warning(
                f"Updating {self.platform_name} {self.domain} took longer "
                + f"than the scheduled update interval {self.scan_interval}",
            )
            return

        async with self._process_updates:
            tasks = []
            for entity in self.entities.values():
                if not entity.should_poll:
                    continue
                tasks.append(entity.async_update_state(True))

            if tasks:
                await asyncio.gather(*tasks)

    @staticmethod
    @callback
    def async_get_current_platform():
        """Get the current platform from context."""
        if (platform := _current_platform.get()) is None:
            raise RuntimeError("Cannot get non-set current platform")
        return platform

    @staticmethod
    @callback
    def async_get_platforms(shc: SmartHomeController, integration_name: str):
        """Find existing platforms."""
        if (
            _DATA_ENTITY_PLATFORM not in shc.data
            or integration_name not in shc.data[_DATA_ENTITY_PLATFORM]
        ):
            return []

        platforms: list[EntityPlatform] = shc.data[_DATA_ENTITY_PLATFORM][
            integration_name
        ]

        return platforms


_current_platform: contextvars.ContextVar[EntityPlatform] = contextvars.ContextVar(
    "current_platform", default=None
)
