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
import asyncio
import datetime as dt
import inspect
import json
import logging
import pathlib
import typing

import voluptuous as vol

from . import helpers
from .config_type import ConfigType
from .current_controller import _get_current_controller
from .device import Device
from .integration_not_found import IntegrationNotFound
from .platform import Platform
from .platform_implementation import PlatformImplementation
from .requirements_not_found import RequirementsNotFound

if not typing.TYPE_CHECKING:

    class ConfigEntry:
        ...

    class SmartHomeController:
        ...

    class GroupComponent:
        ...

    class EntityComponent:
        ...


if typing.TYPE_CHECKING:
    from .config_entry import ConfigEntry
    from .entity_component import EntityComponent
    from .group_component import GroupComponent
    from .smart_home_controller import SmartHomeController


_LOGGER: typing.Final = logging.getLogger(__name__)


# pylint: disable=unused-variable
class SmartHomeControllerComponent(abc.ABC):
    """
    Base class for all Smart Home Controller Components.

    Implements defaults Setup and Config where possible
    and defines abstract methods, that must be implemented
    in each new Smart Home Controller Component.
    """

    def __init__(self, path: typing.Iterable[str]):
        self._shc_: SmartHomeController = None
        self._manifest: dict = None
        self._config: ConfigType = None
        self._supported_platforms: set[Platform | str] = []
        self._current_platform: Platform | str = None

        for base in path:
            manifest_path = pathlib.Path(base) / "manifest.json"

            if not manifest_path.is_file() or self._manifest is not None:
                continue

            try:
                self._manifest: dict = json.loads(manifest_path.read_text())
            except ValueError as err:
                _LOGGER.error(
                    f"Error parsing manifest.json file at {manifest_path}: {err}"
                )
                continue
        if self.domain is not None:
            _COMPONENT_REGISTRY[self.domain] = self

    @property
    def controller(self) -> SmartHomeController:
        return self._shc

    @property
    def _shc(self) -> SmartHomeController:
        if self._shc_ is None:
            self._shc_ = _get_current_controller()
        return self._shc_

    @property
    def supports_async_setup(self) -> bool:
        current_impl = self.setup
        default_impl = SmartHomeControllerComponent.setup
        return inspect.getfile(current_impl) == inspect.getfile(default_impl)

    @property
    def supports_entry_unload(self) -> bool:
        current_impl = self.async_unload_entry
        default_impl = SmartHomeControllerComponent.async_unload_entry
        return inspect.getfile(current_impl) != inspect.getfile(default_impl)

    @property
    def supports_entry_remove(self) -> bool:
        current_impl = self.async_remove_entry
        default_impl = SmartHomeControllerComponent.async_remove_entry
        return inspect.getfile(current_impl) != inspect.getfile(default_impl)

    @property
    def supports_migrate_entry(self) -> bool:
        current_impl = self.async_migrate_entry
        default_impl = SmartHomeControllerComponent.async_migrate_entry
        return inspect.getfile(current_impl) != inspect.getfile(default_impl)

    @property
    def supports_remove_from_device(self) -> bool:
        current_impl = self.async_remove_config_entry_device
        default_impl = SmartHomeControllerComponent.async_remove_config_entry_device
        return inspect.getfile(current_impl) != inspect.getfile(default_impl)

    @property
    def supports_platform_reset(self) -> bool:
        current_impl = self.async_reset_platform
        default_impl = SmartHomeControllerComponent.async_reset_platform
        return inspect.getfile(current_impl) != inspect.getfile(default_impl)

    @property
    def domain(self) -> str:
        """Get the domain from the manifest."""
        return self._manifest["domain"] if self._manifest else None

    @property
    def documentation(self) -> str:
        """Return documentation."""
        return self._manifest.get("documentation") if self._manifest else None

    @property
    def scan_interval(self) -> dt.timedelta:
        """Default Scan Interval for Platform."""
        return None

    @property
    def storage_key(self) -> str:
        return self.domain

    @property
    def storage_version(self) -> int:
        return 1

    @property
    def storage_save_delay(self) -> int:
        return 10

    @property
    def supported_platforms(self) -> set[Platform | str]:
        return self._supported_platforms

    @staticmethod
    def get_component(domain: str):
        return _COMPONENT_REGISTRY.get(domain, None)

    @staticmethod
    def _components():
        return _COMPONENT_REGISTRY

    @property
    def config_schema(self) -> typing.Callable[[ConfigType], ConfigType]:
        return None

    @property
    def platform_schema(self) -> typing.Callable[[ConfigType], ConfigType]:
        return None

    @property
    def platform_schema_base(self) -> typing.Callable[[ConfigType], ConfigType]:
        return None

    # pylint: disable=unused-argument
    async def async_can_shutdown(self, service: str) -> str:
        """Return the error message, if shutdown is not possible."""
        return None

    async def async_validate_config(self, config: ConfigType) -> ConfigType:
        """Validates the configuration of the component."""
        # pylint: disable=not-callable
        config_validator = self.config_schema
        if config_validator is not None:
            return config_validator(config)

        config_validator = self.platform_schema_base
        if config_validator is None:
            config_validator = self.platform_schema
        if config_validator is None:
            return config

        platforms = []
        setup_mgr = self.controller.setup
        for p_name, p_config in setup_mgr.config_per_platform(config, self.domain):
            # Validate component specific platform schema
            try:
                p_validated = config_validator(p_config)
            except vol.Invalid as ex:
                self.controller.setup.async_log_exception(
                    ex, self.domain, p_config, self.documentation
                )
                continue
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception(
                    f"Unknown error validating {p_name} platform config with "
                    + f"{self.domain} component platform schema",
                )
                continue

            # Not all platform components follow same pattern for platforms
            # So if p_name is None we are not going to validate platform
            # (the automation component is one of them)
            if p_name is None:
                platforms.append(p_validated)
                continue

            try:
                p_integration = await setup_mgr.async_get_integration_with_requirements(
                    p_name
                )
                p_integration.get_component()
            except (RequirementsNotFound, IntegrationNotFound) as ex:
                _LOGGER.error(f"Platform error: {self.domain} - {ex}")
                continue

            shc_component = self.get_component(p_name)
            if shc_component is None:
                continue

            platform = shc_component.get_platform(self.domain)
            if platform is None:
                continue

            # Validate platform specific schema
            platform_schema = platform.platform_config_schema
            if platform_schema is not None:
                try:
                    p_validated = platform_schema(p_config)
                except vol.Invalid as ex:
                    self.controller.setup.async_log_exception(
                        ex,
                        f"{self.domain}.{p_name}",
                        p_config,
                        p_integration.documentation,
                    )
                    continue
                except Exception:  # pylint: disable=broad-except
                    _LOGGER.exception(
                        f"Unknown error validating config for {p_name} platform for "
                        + f"{self.domain} component with PLATFORM_SCHEMA"
                    )
                    continue

            platforms.append(p_validated)

        # Create a copy of the configuration with all config for current
        # component removed and add validated config back in.
        config = setup_mgr.config_without_domain(config, self.domain)
        config[self.domain] = platforms

        return config

    def get_setup_task(self, config: ConfigType):
        if self.supports_async_setup:
            return self.async_setup(config)

        return self._shc.run_in_executor(None, self.setup, config)

    def start_setup(self, shc: SmartHomeController) -> asyncio.TimerHandle:
        """Create Setup Watcher."""
        if self._shc_ is None:
            self._shc_ = shc
        # default: uses warning task of environment (Setup is taking over ...)

    def setup_finished(self):
        """clean up created setup resources, if neccesarry."""
        # default: nothing to do

    async def async_setup(self, config: ConfigType) -> bool:
        self._config = config.get(self.domain, None)
        return True

    def setup(self, config: ConfigType) -> bool:
        self._config = config.get(self.domain, None)
        return True

    def get_platform(self, platform: Platform | str) -> PlatformImplementation:
        """Get the requested platform implementation."""
        if platform in self.supported_platforms:
            self._current_platform = platform
            return self
        self._current_platform = None
        return None

    async def async_setup_entry(self, entry: ConfigEntry) -> bool:
        """
        Default implementation for components, that do not
        use Config Entries.
        """
        return False

    async def async_unload_entry(self, entry: ConfigEntry) -> bool:
        """
        Default implementation for components, that do not
        use Config Entries.
        """
        return True

    async def async_remove_entry(self, entry: ConfigEntry) -> None:
        """Remove a config entry"""
        return

    async def async_remove_config_entry_device(
        self, entry: ConfigEntry, device_entry: Device
    ) -> bool:
        """Remove lookin config entry from a device."""
        return False

    def _is_on(self, entity_id: str) -> bool:
        """
        Return True if the entity is on.

        The default implementation returns always 'False'.

        Must be overridden in Components that support on/off states.
        """
        return False

    @staticmethod
    def is_on(shc: SmartHomeController, entity_id: str = None) -> bool:
        """Load up the module to call the is_on method.

        If there is no entity id given we will check all.
        """
        if entity_id:
            group = shc.components.group
            if isinstance(group, GroupComponent):
                entity_ids = group.expand_entity_ids([entity_id])
            else:
                entity_ids = [entity_id]
        else:
            entity_ids = shc.states.entity_ids()

        for ent_id in entity_ids:
            domain = helpers.split_entity_id(ent_id)[0]

            component = getattr(shc.components, domain)
            if component is None:
                continue

            # Should not be called directly from other components
            # pylint: disable=protected-access
            if component._is_on(ent_id):
                return True

        return False

    # pylint: disable=unused-argument
    async def async_reset_platform(self, platform: Platform | str):
        """Reset the Platform Implementation."""
        return

    # pylint: disable=unused-argument
    async def async_migrate_entry(self, entry: ConfigEntry) -> bool:
        """Migrate old entry."""
        return False

    @property
    def entity_component(self) -> EntityComponent:
        """Return the Entity Component, if it is used."""
        return None


_COMPONENT_REGISTRY: typing.Final[dict[str, SmartHomeControllerComponent]] = {}
