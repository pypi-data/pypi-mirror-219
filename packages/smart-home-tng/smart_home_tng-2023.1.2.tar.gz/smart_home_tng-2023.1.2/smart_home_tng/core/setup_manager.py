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
import collections
import collections.abc
import contextlib
import datetime
import importlib
import logging
import os
import pathlib
import queue
import re
import shutil
import subprocess  # nosec
import sys
import threading
import time
import timeit
import types
import typing
from importlib import metadata

import awesomeversion as asv
import pkg_resources
import voluptuous as vol
import voluptuous.humanize as vh
from urllib3.util import url

from ..auth.auth_manager import AuthManager
from ..auth.mfa_modules import MultiFactorAuthModule
from ..auth.providers import AuthProvider
from . import generated, helpers
from .callback import callback
from .callback_type import CallbackType
from .circular_dependency import CircularDependency
from .config_entries import ConfigEntries
from .config_errors import ConfigErrors
from .config_source import ConfigSource
from .config_type import ConfigType
from .config_validation import ConfigValidation as cv
from .const import Const
from .dependency_error import DependencyError
from .dhcp_matcher import DHCPMatcher
from .discovery_dict import DiscoveryDict
from .discovery_info_type import DiscoveryInfoType
from .entity_component import EntityComponent
from .entity_platform import EntityPlatform
from .entity_values import EntityValues
from .event import Event
from .integration import Integration
from .integration_not_found import IntegrationNotFound
from .integration_platform import IntegrationPlatform
from .manifest import Manifest
from .persistent_notification_component import PersistentNotificationComponent
from .platform import Platform
from .platform_implementation import PlatformImplementation
from .queue_logging_handler import QueueLoggingHandler
from .requirements_not_found import RequirementsNotFound
from .secrets import Secrets
from .smart_home_controller_component import SmartHomeControllerComponent
from .smart_home_controller_error import SmartHomeControllerError
from .smart_home_controller_job import SmartHomeControllerJob
from .unit_system import UnitSystem
from .yaml_loader import YamlLoader

if not typing.TYPE_CHECKING:

    class SmartHomeController:
        ...


if typing.TYPE_CHECKING:
    from .smart_home_controller import SmartHomeController


_UNDEF: typing.Final = object()
_LOGGER: typing.Final = logging.getLogger(__name__)
_BASE_PLATFORMS: typing.Final = {str(platform) for platform in Platform}

_MOVED_ZEROCONF_PROPS: typing.Final = ("macaddress", "model", "manufacturer")

_DATA_PERSISTENT_ERRORS: typing.Final = "setup.persistent_errors"
_YAML_CONFIG_FILE: typing.Final = "configuration.yaml"
_VERSION_FILE: typing.Final = ".SHC_VERSION"
_CONFIG_DIR_NAME: typing.Final = ".config/shc"
_DATA_CUSTOMIZE: typing.Final = "setup.shc_customize"
# The default is too low when the internet connection is satellite or high latency
_PIP_TIMEOUT: typing.Final = 60
_MAX_INSTALL_FAILURES: typing.Final = 3
_DATA_PIP_LOCK: typing.Final = "setup.pip_lock"
_DATA_INTEGRATIONS_WITH_REQS: typing.Final = "setup.integrations_with_reqs"
_DATA_INSTALL_FAILURE_HISTORY: typing.Final = "setup.install_failure_history"
_DATA_AUTH_REQS: typing.Final = "setup.auth_prov_reqs_processed"
_DATA_MFA_REQS: typing.Final = "setup.mfa_auth_module_reqs_processed"
# hass.data key for logging information.
_DATA_SETUP_TIME: typing.Final = "setup.time"

_LOG_SLOW_STARTUP_INTERVAL: typing.Final = 60
_SLOW_STARTUP_CHECK_INTERVAL: typing.Final = 1
_STAGE_1_TIMEOUT = 120
_STAGE_2_TIMEOUT = 300
_WRAP_UP_TIMEOUT = 300
_COOLDOWN_TIME = 60


_CORE_INTEGRATIONS: typing.Final = {
    Const.CORE_COMPONENT_NAME,
    Const.PERSISTENT_NOTIFICATION_COMPONENT_NAME,
}
_DEBUGGER_INTEGRATIONS: typing.Final = {"debugpy"}
_LOGGING_INTEGRATIONS = {
    # Set log levels
    "logger",
    # Error logging
    "system_log",
    "sentry",
    # To record data
    "recorder",
}
_STARTUP_DISCOVERY_INTEGRATIONS: typing.Final = ("dhcp", "ssdp", "usb", "zeroconf")
_STAGE_1_INTEGRATIONS = {
    # We need to make sure discovery integrations
    # update their deps before stage 2 integrations
    # load them inadvertently before their deps have
    # been updated which leads to using an old version
    # of the dep, or worse (import errors).
    "discovery",
    *_STARTUP_DISCOVERY_INTEGRATIONS,
    # To make sure we forward data to other instances
    "mqtt_eventstream",
    # To provide account link implementations
    # "cloud",
    # Ensure supervisor is available
    # "hassio",
    # Get the frontend up and running as soon
    # as possible so problem integrations can
    # be removed
    "frontend",
}

_CONSTRAINT_FILE: typing.Final = "package_constraints.txt"
_DISCOVERY_INTEGRATIONS: typing.Final[dict[str, collections.abc.Iterable[str]]] = {
    "dhcp": ("dhcp",),
    "mqtt": ("mqtt",),
    "ssdp": ("ssdp",),
    "zeroconf": ("zeroconf", "homekit"),
}

_AUTOMATION_CONFIG_PATH: typing.Final = "automations.yaml"
_SCRIPT_CONFIG_PATH: typing.Final = "scripts.yaml"
_SCENE_CONFIG_PATH: typing.Final = "scenes.yaml"
_INVALID_CONFIG_NOTIFICATION_ID: typing.Final = "invalid_config"

_LOAD_EXCEPTIONS: typing.Final = (ImportError, FileNotFoundError)
_INTEGRATION_LOAD_EXCEPTIONS: typing.Final = (
    IntegrationNotFound,
    RequirementsNotFound,
    *_LOAD_EXCEPTIONS,
)

_DEFAULT_CONFIG: typing.Final = f"""
# Loads default set of integrations. Do not remove.
default_config:

automation: !include {_AUTOMATION_CONFIG_PATH}
script: !include {_SCRIPT_CONFIG_PATH}
scene: !include {_SCENE_CONFIG_PATH}
"""
_DEFAULT_SECRETS: typing.Final = """
# Use this file to store secrets like usernames and passwords.
# Learn more at https://www.home-assistant.io/docs/configuration/secrets/
some_password: welcome
"""
_TTS_PRE_92: typing.Final = """
tts:
- platform: google
"""
_TTS_92: typing.Final = """
tts:
- platform: google_translate
  service_name: google_say
"""

_DATA_SETUP_DONE: typing.Final = "setup.done"
_DATA_SETUP_STARTED: typing.Final = "setup.started"
_DATA_SETUP: typing.Final = "setup.tasks"

_DATA_DEPS_REQS: typing.Final = "setup.deps_reqs_processed"

_DATA_COMPONENTS: typing.Final = "setup.components"
_DATA_INTEGRATIONS: typing.Final = "setup.integrations"
_DATA_CUSTOM_COMPONENTS: typing.Final = "setup.custom_components"

_SLOW_SETUP_WARNING: typing.Final = 15
_SLOW_SETUP_MAX_WAIT: typing.Final = 300
_PACKAGE_CUSTOM_COMPONENTS: typing.Final = "custom_components"
_PACKAGE_BUILTIN: typing.Final = "smart_home_tng.components"
_ERROR_LOG_FILENAME: typing.Final = "smart_home_tng.log"

_SIGNAL_PLATFORM_DISCOVERED: typing.Final = "discovery.platform_discovered.{}"
_EVENT_LOAD_PLATFORM: typing.Final = "load_platform.{}"
_ATTR_PLATFORM: typing.Final = "platform"
_ATTR_DISCOVERED: typing.Final = "discovered"


def _log_pkg_error(package: str, component: str, config: dict, message: str) -> None:
    """Log an error while merging packages."""
    message = f"Package {package} setup failed. Integration {component} {message}"

    pack_config = config[Const.CORE_COMPONENT_NAME][Const.CONF_PACKAGES].get(
        package, config
    )
    message += (
        f" (See {getattr(pack_config, '__config_file__', '?')}:"
        f"{getattr(pack_config, '__line__', '?')}). "
    )

    _LOGGER.error(message)


# pylint: disable=unused-variable
class SetupManager:
    """
    All methods needed to bootstrap a Smart Home Controller instance.

    Combines all functions from bootstrap, config, loader, runner, setup
    and requirements of Home Assistant.
    """

    AUTOMATION_CONFIG_PATH: typing.Final = _AUTOMATION_CONFIG_PATH
    SCENE_CONFIG_PATH: typing.Final = _SCENE_CONFIG_PATH
    SCRIPT_CONFIG_PATH: typing.Final = _SCRIPT_CONFIG_PATH

    DATA_CUSTOMIZE: typing.Final = _DATA_CUSTOMIZE
    DATA_COMPONENTS: typing.Final = _DATA_COMPONENTS
    DATA_SETUP: typing.Final = _DATA_SETUP
    DATA_SETUP_TIME: typing.Final = _DATA_SETUP_TIME
    DISCOVERY_INTEGRATIONS: typing.Final = _DISCOVERY_INTEGRATIONS
    PACKAGE_BUILTIN: typing.Final = _PACKAGE_BUILTIN

    def __init__(self, shc: SmartHomeController):
        self._shc = shc
        self._integration_platforms: list[IntegrationPlatform] = None
        self._reset_locks = dict[str, asyncio.Lock]()
        self._setup_locks = dict[str, asyncio.Lock]()

    @callback
    def async_set_domains_to_be_loaded(self, domains: set[str]) -> None:
        """Set domains that are going to be loaded from the config.

        This will allow us to properly handle after_dependencies.
        """
        self._shc.data[_DATA_SETUP_DONE] = {
            domain: asyncio.Event() for domain in domains
        }

    def setup_component(self, domain: str, config: ConfigType) -> bool:
        """Set up a component and all its dependencies."""
        return self._shc.run_coroutine_threadsafe(
            self.async_setup_component(domain, config)
        ).result()

    async def async_setup_component(self, domain: str, config: ConfigType) -> bool:
        """Set up a component and all its dependencies.

        This method is a coroutine.
        """
        lock = self._setup_locks.setdefault(domain, asyncio.Lock())
        async with lock:
            if domain in self._shc.config.components:
                return True

            task = self._shc.async_create_task(
                self._async_setup_component(domain, config)
            )

            try:
                return await task
            except IntegrationNotFound:
                pass
            finally:
                if domain in self._shc.data.get(_DATA_SETUP_DONE, {}):
                    self._shc.data[_DATA_SETUP_DONE].pop(domain).set()

    async def _async_process_dependencies(
        self, config: ConfigType, integration: Integration
    ) -> list[str]:
        """Ensure all dependencies are set up.

        Returns a list of dependencies which failed to set up.
        """
        dependencies_tasks = {
            dep: self.async_setup_component(dep, config)
            for dep in integration.dependencies
            if dep not in self._shc.config.components
        }

        after_dependencies_tasks = {}
        to_be_loaded = self._shc.data.get(_DATA_SETUP_DONE, {})
        for dep in integration.after_dependencies:
            if (
                dep not in dependencies_tasks
                and dep in to_be_loaded
                and dep not in self._shc.config.components
            ):
                after_dependencies_tasks[dep] = self._shc.async_create_task(
                    to_be_loaded[dep].wait()
                )

        if not dependencies_tasks and not after_dependencies_tasks:
            return []

        if dependencies_tasks:
            _LOGGER.debug(
                f"Dependency {integration.domain} will wait for dependencies "
                + f"{list(dependencies_tasks)}"
            )
        if after_dependencies_tasks:
            _LOGGER.debug(
                f"Dependency {integration.domain} will wait for after dependencies "
                + f"{list(after_dependencies_tasks)}"
            )

        async with self._shc.timeout.async_freeze(integration.domain):
            results = await asyncio.gather(
                *dependencies_tasks.values(), *after_dependencies_tasks.values()
            )

        failed = [
            domain for idx, domain in enumerate(dependencies_tasks) if not results[idx]
        ]

        if failed:
            _LOGGER.error(
                f"Unable to set up dependencies of {integration.domain}. "
                + f"Setup failed for dependencies: {', '.join(failed)}"
            )

        return failed

    async def _async_setup_component(self, domain: str, config: ConfigType) -> bool:
        """Set up a component for Smart Home - The Next Generation.

        This method is a coroutine.
        """
        integration: Integration = None

        def log_error(msg: str) -> None:
            """Log helper."""
            if integration is None:
                custom = ""
                link = None
            else:
                custom = "" if integration.is_built_in else "custom integration "
                link = integration.documentation
            _LOGGER.error(f"Setup failed for {custom}{domain}: {msg}")
            self.async_notify_setup_error(domain, link)

        try:
            integration = await self.async_get_integration(domain)
        except IntegrationNotFound:
            log_error("Integration not found.")
            return False

        if integration.disabled:
            log_error(f"Dependency is disabled - {integration.disabled}")
            return False

        # Validate all dependencies exist and there are no circular dependencies
        if not await integration.resolve_dependencies():
            return False

        # Process requirements as soon as possible, so we can import the component
        # without requiring imports to be in functions.
        try:
            await self.async_process_deps_reqs(config, integration)
        except SmartHomeControllerError as err:
            log_error(str(err))
            return False

        # Some integrations fail on import because they call functions incorrectly.
        # So we do it before validating config to catch these errors.
        try:
            component = integration.get_component()
        except ImportError as err:
            log_error(f"Unable to import component: {err}")
            return False

        processed_config = await self.async_process_component_config(
            config, integration
        )

        if processed_config is None:
            log_error("Invalid config.")
            return False

        start = timeit.default_timer()
        _LOGGER.info(f"Setting up {domain}")
        shc_component = SmartHomeControllerComponent.get_component(domain)
        with self.async_start_setup([domain]):
            if shc_component is not None:
                # Handle new class based implementation
                warn_task = shc_component.start_setup(self._shc)
                if warn_task is None:
                    warn_task = self._shc.call_later(
                        _SLOW_SETUP_WARNING,
                        _LOGGER.warning,
                        f"Setup of {domain} is taking over {_SLOW_SETUP_WARNING} seconds.",
                    )
            # Handle legacy module based implementation
            elif hasattr(component, "PLATFORM_SCHEMA"):
                # Entity components have their own warning
                warn_task = None
            else:
                warn_task = self._shc.call_later(
                    _SLOW_SETUP_WARNING,
                    _LOGGER.warning,
                    f"Setup of {domain} is taking over {_SLOW_SETUP_WARNING} seconds.",
                )

            task = None
            result: typing.Any | bool = True
            try:
                task = None
                if shc_component is not None:
                    # Handle new class based implementation
                    task = shc_component.get_setup_task(processed_config)
                    if isinstance(task, bool):
                        return task
                # Handle legacy module based implementation
                elif hasattr(component, "async_setup"):
                    task = component.async_setup(self._shc, processed_config)
                elif hasattr(component, "setup"):
                    # This should not be replaced with hass.async_add_executor_job because
                    # we don't want to track this task in case it blocks startup.
                    task = self._shc.run_in_executor(
                        None, component.setup, self._shc, processed_config
                    )
                elif not hasattr(component, "async_setup_entry"):
                    log_error("No setup or config entry setup function defined.")
                    return False

                if task:
                    async with self._shc.timeout.async_timeout(
                        _SLOW_SETUP_MAX_WAIT, domain
                    ):
                        result = await task
            except asyncio.TimeoutError:
                _LOGGER.error(
                    f"Setup of {domain} is taking longer than {_SLOW_SETUP_MAX_WAIT} seconds."
                    " Startup will proceed without waiting any longer"
                )
                return False
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception(f"Error during setup of component {domain}")
                self.async_notify_setup_error(domain, integration.documentation)
                return False
            finally:
                end = timeit.default_timer()
                if warn_task:
                    warn_task.cancel()
                if shc_component is not None:
                    shc_component.setup_finished()

            _LOGGER.info(f"Setup of domain {domain} took {end - start: .1f} seconds")

            if result is False:
                log_error("Integration failed to initialize.")
                return False
            if result is not True:
                log_error(
                    f"Integration {domain!r} did not return boolean if setup was "
                    "successful. Disabling component."
                )
                return False

            # Flush out async_setup calling create_task. Fragile but covered by test.
            await asyncio.sleep(0)
            await self._shc.config_entries.flow.async_wait_init_flow_finish(domain)

            await asyncio.gather(
                *(
                    entry.async_setup(self._shc, integration=integration)
                    for entry in self._shc.config_entries.async_entries(domain)
                )
            )

            self._shc.config.component_loaded(domain)

        self._shc.bus.async_fire(
            Const.EVENT_COMPONENT_LOADED, {Const.ATTR_COMPONENT: domain}
        )

        return True

    async def async_prepare_setup_platform(
        self, config: ConfigType, domain: Platform | str, platform: str
    ) -> PlatformImplementation:
        """Load a platform and makes sure dependencies are setup.

        This method is a coroutine.
        """
        platform_path = Const.PLATFORM_FORMAT.format(
            domain=platform, platform=str(domain)
        )

        def log_error(msg: str) -> None:
            """Log helper."""

            _LOGGER.error(
                f"Unable to prepare setup for platform {platform_path}: {msg}"
            )
            self.async_notify_setup_error(platform_path)

        try:
            integration = await self.async_get_integration(platform)
        except IntegrationNotFound:
            log_error("Integration not found")
            return None

        # Process deps and reqs as soon as possible, so that requirements are
        # available when we import the platform.
        try:
            await self.async_process_deps_reqs(config, integration)
        except SmartHomeControllerError as err:
            log_error(str(err))
            return None

        component = integration.get_component()
        shc_comp = SmartHomeControllerComponent.get_component(platform)
        if shc_comp is not None:
            platform = shc_comp.get_platform(domain)
            # Already loaded
            if platform_path in self._shc.config.components:
                return platform

        # Platforms cannot exist on their own, they are part of their integration.
        # If the integration is not set up yet, and can be set up, set it up.
        if integration.domain not in self._shc.config.components:
            try:
                component = integration.get_component()
            except ImportError as exc:
                log_error(f"Unable to import the component ({exc}).")
                return None

            if (
                SmartHomeControllerComponent.get_component(platform) is not None
                or hasattr(component, "setup")
                or hasattr(component, "async_setup")
            ) and not await self.async_setup_component(integration.domain, config):
                log_error("Unable to set up component.")
                return None

        if shc_comp is None:
            shc_comp = SmartHomeControllerComponent.get_component(platform)
        if shc_comp is not None:
            platform = shc_comp.get_platform(domain)
            if not isinstance(platform, PlatformImplementation):
                platform = None
        if platform is None:
            log_error(f"Platform not found:{platform_path}")
            return None
        return platform

    async def async_process_deps_reqs(
        self, config: ConfigType, integration: Integration
    ) -> None:
        """Process all dependencies and requirements for a module.

        Module is a Python module of either a component or platform.
        """
        if (processed := self._shc.data.get(_DATA_DEPS_REQS)) is None:
            processed = self._shc.data[_DATA_DEPS_REQS] = set()
        elif integration.domain in processed:
            return

        if failed_deps := await self._async_process_dependencies(config, integration):
            raise DependencyError(failed_deps)

        if not self._shc.config.skip_pip and integration.requirements:
            async with self._shc.timeout.async_freeze(integration.domain):
                await self.async_get_integration_with_requirements(integration.domain)

        processed.add(integration.domain)

    @callback
    def async_when_setup(
        self,
        component: str,
        when_setup_cb: collections.abc.Callable[
            [SmartHomeController, str], collections.abc.Awaitable[None]
        ],
    ) -> None:
        """Call a method when a component is setup."""
        self._async_when_setup(component, when_setup_cb, False)

    @callback
    def async_when_setup_or_start(
        self,
        component: str,
        when_setup_cb: collections.abc.Callable[
            [SmartHomeController, str], collections.abc.Awaitable[None]
        ],
    ) -> None:
        """Call a method when a component is setup or state is fired."""
        self._async_when_setup(component, when_setup_cb, True)

    @callback
    def _async_when_setup(
        self,
        component: str,
        when_setup_cb: collections.abc.Callable[
            [SmartHomeController, str], collections.abc.Awaitable[None]
        ],
        start_event: bool,
    ) -> None:
        """Call a method when a component is setup or the start event fires."""

        async def when_setup() -> None:
            """Call the callback."""
            try:
                await when_setup_cb(self._shc, component)
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception(f"Error handling when_setup callback for {component}")

        if component in self._shc.config.components:
            self._shc.async_create_task(when_setup())
            return

        listeners: list[CallbackType] = []

        async def _matched_event(_event: Event) -> None:
            """Call the callback when we matched an event."""
            for listener in listeners:
                listener()
            await when_setup()

        async def _loaded_event(event: Event) -> None:
            """Call the callback if we loaded the expected component."""
            if event.data[Const.ATTR_COMPONENT] == component:
                await _matched_event(event)

        listeners.append(
            self._shc.bus.async_listen(Const.EVENT_COMPONENT_LOADED, _loaded_event)
        )
        if start_event:
            listeners.append(
                self._shc.bus.async_listen(Const.EVENT_SHC_START, _matched_event)
            )

    @callback
    def async_get_loaded_integrations(self) -> set[str]:
        """Return the complete list of loaded integrations."""
        integrations = set()
        for component in self._shc.config.components:
            if "." not in component:
                integrations.add(component)
                continue
            domain, platform = component.split(".", 1)
            if domain in _BASE_PLATFORMS:
                integrations.add(platform)
        return integrations

    @contextlib.contextmanager
    def async_start_setup(
        self, components: collections.abc.Iterable[str]
    ) -> collections.abc.Generator[None, None, None]:
        """Keep track of when setup starts and finishes."""
        setup_started = self._shc.data.setdefault(_DATA_SETUP_STARTED, {})
        started = helpers.utcnow()
        unique_components: dict[str, str] = {}
        for domain in components:
            unique = helpers.ensure_unique_string(domain, setup_started)
            unique_components[unique] = domain
            setup_started[unique] = started

        yield

        setup_time: dict[str, datetime.timedelta] = self._shc.data.setdefault(
            _DATA_SETUP_TIME, {}
        )
        time_taken = helpers.utcnow() - started
        for unique, domain in unique_components.items():
            del setup_started[unique]
            if "." in domain:
                _, integration = domain.split(".", 1)
            else:
                integration = domain
            if integration in setup_time:
                setup_time[integration] += time_taken
            else:
                setup_time[integration] = time_taken

    @callback
    def async_notify_setup_error(
        self, component: str, display_link: str = None
    ) -> None:
        """Print a persistent notification.

        This method must be run in the event loop.
        """
        if (errors := self._shc.data.get(_DATA_PERSISTENT_ERRORS)) is None:
            errors = self._shc.data[_DATA_PERSISTENT_ERRORS] = {}

        errors[component] = errors.get(component) or display_link

        message = "The following integrations and platforms could not be set up:\n\n"

        for name, link in errors.items():
            show_logs = f"[Show logs](/config/logs?filter={name})"
            part = f"[{name}]({link})" if link else name
            message += f" - {part} ({show_logs})\n"

        message += "\nPlease check your config and [logs](/config/logs)."

        comp = SmartHomeControllerComponent.get_component(
            Const.PERSISTENT_NOTIFICATION_COMPONENT_NAME
        )
        if isinstance(comp, PersistentNotificationComponent):
            comp.async_create(
                message, "Invalid config", _INVALID_CONFIG_NOTIFICATION_ID
            )

    @staticmethod
    def get_default_config_dir() -> str:
        """Put together the default configuration directory based on the OS."""
        data_dir = os.path.expanduser("~")
        return os.path.join(data_dir, _CONFIG_DIR_NAME)

    async def async_ensure_config_exists(self) -> bool:
        """Ensure a configuration file exists in given configuration directory.

        Creating a default one if needed.
        Return boolean if configuration dir is ready to go.
        """
        config_path = self._shc.config.path(_YAML_CONFIG_FILE)

        if os.path.isfile(config_path):
            return True

        print(
            "Unable to find configuration. Creating default one in",
            self._shc.config.config_dir,
        )
        return await self.async_create_default_config()

    async def async_create_default_config(self) -> bool:
        """Create a default configuration file in given configuration directory.

        Return if creation was successful.
        """
        return await self._shc.async_add_executor_job(
            _write_default_config, self._shc.config.config_dir
        )

    async def async_shc_config_yaml(self) -> dict:
        """Load YAML from a Smart Home Controller configuration file.

        This function allow a component inside the asyncio loop to reload its
        configuration by itself. Include package merge.
        """
        if self._shc.config.config_dir is None:
            secrets = None
        else:
            secrets = Secrets(pathlib.Path(self._shc.config.config_dir))

        # Not using async_add_executor_job because this is an internal method.
        config = await self._shc.run_in_executor(
            None,
            self.load_yaml_config_file,
            secrets,
        )
        core_config = config.get(Const.CORE_COMPONENT_NAME, {})
        await self.merge_packages_config(
            config, core_config.get(Const.CONF_PACKAGES, {})
        )
        return config

    def load_yaml_config_file(
        self, secrets: Secrets = None
    ) -> dict[typing.Any, typing.Any]:
        """Parse a YAML configuration file.

        Raises FileNotFoundError or SmartHomeControllerError.

        This method needs to run in an executor.
        """
        config_path = self._shc.config.path(_YAML_CONFIG_FILE)
        conf_dict = YamlLoader.load_yaml(config_path, secrets)

        if not isinstance(conf_dict, dict):
            msg = (
                f"The configuration file {os.path.basename(config_path)} "
                + "does not contain a dictionary"
            )
            _LOGGER.error(msg)
            raise SmartHomeControllerError(msg)

        # Convert values to dictionaries if they are None
        for key, value in conf_dict.items():
            conf_dict[key] = value or {}
        return conf_dict

    def process_shc_config_upgrade(self) -> None:
        """Upgrade configuration if necessary.

        This method needs to run in an executor.
        """
        version_path = self._shc.config.path(_VERSION_FILE)

        try:
            with open(version_path, encoding="utf8") as inp:
                conf_version = inp.readline().strip()
        except FileNotFoundError:
            # Last version to not have this file
            conf_version = "0.1.0"

        if conf_version == Const.__version__:
            return

        _LOGGER.info(
            f"Upgrading configuration directory from {conf_version} to {Const.__version__}"
        )

        version_obj = asv.AwesomeVersion(conf_version)

        if version_obj < asv.AwesomeVersion("0.50"):
            # 0.50 introduced persistent deps dir.
            lib_path = self._shc.config.path("deps")
            if os.path.isdir(lib_path):
                shutil.rmtree(lib_path)

        if version_obj < asv.AwesomeVersion("0.92"):
            # 0.92 moved google/tts.py to google_translate/tts.py
            config_path = self._shc.config.path(_YAML_CONFIG_FILE)

            with open(config_path, encoding="utf-8") as config_file:
                config_raw = config_file.read()

            if _TTS_PRE_92 in config_raw:
                _LOGGER.info("Migrating google tts to google_translate tts")
                config_raw = config_raw.replace(_TTS_PRE_92, _TTS_92)
                try:
                    with open(config_path, "wt", encoding="utf-8") as config_file:
                        config_file.write(config_raw)
                except OSError:
                    _LOGGER.exception("Migrating to google_translate tts failed")

        if version_obj < asv.AwesomeVersion("0.94") and self._shc.is_docker_env():
            # In 0.94 we no longer install packages inside the deps folder when
            # running inside a Docker container.
            lib_path = self._shc.config.path("deps")
            if os.path.isdir(lib_path):
                shutil.rmtree(lib_path)

        with open(version_path, "wt", encoding="utf8") as outp:
            outp.write(Const.__version__)

    @callback
    def async_log_exception(
        self,
        ex: Exception,
        domain: str,
        config: dict,
        link: str = None,
    ) -> None:
        """Log an error for configuration validation.

        This method must be run in the event loop.
        """
        self.async_notify_setup_error(domain, link)
        message, is_friendly = _format_config_error(ex, domain, config, link)
        _LOGGER.error(message, exc_info=not is_friendly and ex)

    async def async_process_shc_core_config(self, config: dict) -> None:
        """Process the [smart_home_tng] section from the configuration.

        This method is a coroutine.
        """
        config = _CORE_CONFIG_SCHEMA(config)

        # Only load auth during startup.
        if self._shc.auth is None:
            if (auth_conf := config.get(Const.CONF_AUTH_PROVIDERS)) is None:
                auth_conf = [{"type": "internal"}]

            mfa_conf = config.get(
                Const.CONF_AUTH_MFA_MODULES,
                [{"type": "totp", "id": "totp", "name": "Authenticator-App"}],
            )

            self._shc.auth = await AuthManager.from_config(
                self._shc, auth_conf, mfa_conf
            )

        await self._shc.config.async_load()

        shc_config = self._shc.config

        if any(
            k in config
            for k in (
                Const.CONF_LATITUDE,
                Const.CONF_LONGITUDE,
                Const.CONF_NAME,
                Const.CONF_ELEVATION,
                Const.CONF_TIME_ZONE,
                Const.CONF_UNIT_SYSTEM,
                Const.CONF_EXTERNAL_URL,
                Const.CONF_INTERNAL_URL,
                Const.CONF_CURRENCY,
            )
        ):
            shc_config.config_source = ConfigSource.YAML

        for key, attr in (
            (Const.CONF_LATITUDE, "latitude"),
            (Const.CONF_LONGITUDE, "longitude"),
            (Const.CONF_NAME, "location_name"),
            (Const.CONF_ELEVATION, "elevation"),
            (Const.CONF_INTERNAL_URL, "internal_url"),
            (Const.CONF_EXTERNAL_URL, "external_url"),
            (Const.CONF_MEDIA_DIRS, "media_dirs"),
            (Const.CONF_LEGACY_TEMPLATES, "legacy_templates"),
            (Const.CONF_CURRENCY, "currency"),
        ):
            if key in config:
                setattr(shc_config, attr, config[key])

        if Const.CONF_TIME_ZONE in config:
            shc_config.set_time_zone(config[Const.CONF_TIME_ZONE])

        if Const.CONF_MEDIA_DIRS not in config:
            if self._shc.is_docker_env():
                shc_config.media_dirs = {"local": "/media"}
            else:
                shc_config.media_dirs = {"local": self._shc.config.path("media")}

        # Init whitelist external dir
        allowlist_external_dirs = {
            self._shc.config.path("www"),
            *shc_config.media_dirs.values(),
        }
        if Const.CONF_ALLOWLIST_EXTERNAL_DIRS in config:
            allowlist_external_dirs.update(
                set(config[Const.CONF_ALLOWLIST_EXTERNAL_DIRS])
            )

        elif Const.LEGACY_CONF_WHITELIST_EXTERNAL_DIRS in config:
            _LOGGER.warning(
                f"Key {Const.LEGACY_CONF_WHITELIST_EXTERNAL_DIRS} has been replaced with "
                + f"{Const.CONF_ALLOWLIST_EXTERNAL_DIRS}. Please update your config"
            )
            allowlist_external_dirs.update(
                set(config[Const.LEGACY_CONF_WHITELIST_EXTERNAL_DIRS])
            )
        shc_config.allowlist_external_dirs = allowlist_external_dirs

        # Init whitelist external URL list – make sure to add / to every URL that doesn't
        # already have it so that we can properly test "path ownership"
        if Const.CONF_ALLOWLIST_EXTERNAL_URLS in config:
            allowlist_external_urls = set()
            for value in config[Const.CONF_ALLOWLIST_EXTERNAL_URLS]:
                if value.endswith("/"):
                    allowlist_external_urls.add(value)
                else:
                    allowlist_external_urls.add(f"{value}/")
            shc_config.allowlist_external_urls = allowlist_external_urls

        # Customize
        cust_exact = dict(config[Const.CONF_CUSTOMIZE])
        cust_domain = dict(config[Const.CONF_CUSTOMIZE_DOMAIN])
        cust_glob = collections.OrderedDict(config[Const.CONF_CUSTOMIZE_GLOB])

        for name, pkg in config[Const.CONF_PACKAGES].items():
            if (pkg_cust := pkg.get(Const.CORE_COMPONENT_NAME)) is None:
                continue

            try:
                pkg_cust = _CUSTOMIZE_CONFIG_SCHEMA(pkg_cust)
            except vol.Invalid:
                _LOGGER.warning(f"Package {name} contains invalid customize")
                continue

            cust_exact.update(pkg_cust[Const.CONF_CUSTOMIZE])
            cust_domain.update(pkg_cust[Const.CONF_CUSTOMIZE_DOMAIN])
            cust_glob.update(pkg_cust[Const.CONF_CUSTOMIZE_GLOB])

        self._shc.data[_DATA_CUSTOMIZE] = EntityValues(
            cust_exact, cust_domain, cust_glob
        )

        if Const.CONF_UNIT_SYSTEM in config:
            if config[Const.CONF_UNIT_SYSTEM] == Const.CONF_UNIT_SYSTEM_IMPERIAL:
                shc_config.units = UnitSystem.IMPERIAL()
            else:
                shc_config.units = UnitSystem.METRIC()
        elif Const.CONF_TEMPERATURE_UNIT in config:
            unit = config[Const.CONF_TEMPERATURE_UNIT]
            shc_config.units = (
                UnitSystem.METRIC()
                if unit == Const.TEMP_CELSIUS
                else UnitSystem.IMPERIAL()
            )
            _LOGGER.warning(
                "Found deprecated temperature unit in core "
                + "configuration expected unit system. Replace "
                + f"'{Const.CONF_TEMPERATURE_UNIT}: {unit}' "
                + f"with '{Const.CONF_UNIT_SYSTEM}: {shc_config.units.name}'"
            )

    async def merge_packages_config(
        self,
        config: dict,
        packages: dict[str, typing.Any],
        _log_pkg_error: collections.abc.Callable = _log_pkg_error,
    ) -> dict:
        """Merge packages into the top-level configuration. Mutate config."""
        _PACKAGES_CONFIG_SCHEMA(packages)
        for pack_name, pack_conf in packages.items():
            for comp_name, comp_conf in pack_conf.items():
                if comp_name == Const.CORE_COMPONENT_NAME:
                    continue
                # If component name is given with a trailing description, remove it
                # when looking for component
                domain = comp_name.split(" ")[0]

                try:
                    integration = await self.async_get_integration_with_requirements(
                        domain
                    )
                    component = integration.get_component()
                except _INTEGRATION_LOAD_EXCEPTIONS as ex:
                    _log_pkg_error(pack_name, comp_name, config, str(ex))
                    continue

                shc_component = SmartHomeControllerComponent.get_component(domain)
                merge_list = False
                config_platform: types.ModuleType = None

                if shc_component is None:
                    # legacy module based config validation of home assistant
                    try:
                        config_platform = integration.get_platform("config")
                        # Test if config platform has a config validator
                        if not hasattr(config_platform, "async_validate_config"):
                            config_platform = None
                    except ImportError:
                        config_platform = None
                else:
                    # new class based config validation
                    merge_list = True

                # If integration has a custom config validator, it needs to provide a hint.
                if config_platform is not None:
                    merge_list = config_platform.PACKAGE_MERGE_HINT == "list"

                if not merge_list:
                    merge_list = hasattr(component, "PLATFORM_SCHEMA")

                if not merge_list and hasattr(component, "CONFIG_SCHEMA"):
                    merge_list = _identify_config_schema(component) == "list"

                if merge_list:
                    config[comp_name] = cv.remove_falsy(
                        cv.ensure_list(config.get(comp_name))
                        + cv.ensure_list(comp_conf)
                    )
                    continue

                if comp_conf is None:
                    comp_conf = collections.OrderedDict()

                if not isinstance(comp_conf, dict):
                    _log_pkg_error(
                        pack_name,
                        comp_name,
                        config,
                        "cannot be merged. Expected a dict.",
                    )
                    continue

                if comp_name not in config or config[comp_name] is None:
                    config[comp_name] = collections.OrderedDict()

                if not isinstance(config[comp_name], dict):
                    _log_pkg_error(
                        pack_name,
                        comp_name,
                        config,
                        "cannot be merged. Dict expected in main config.",
                    )
                    continue

                error = _recursive_merge(conf=config[comp_name], package=comp_conf)
                if error:
                    _log_pkg_error(
                        pack_name, comp_name, config, f"has duplicate key '{error}'"
                    )

        return config

    async def async_process_component_config(
        self, config: ConfigType, integration: Integration
    ) -> ConfigType:
        """Check component configuration and return processed configuration.

        Returns None on error.

        This method must be run in the event loop.
        """
        domain = integration.domain
        try:
            component = integration.get_component()
        except _LOAD_EXCEPTIONS as ex:
            _LOGGER.error(f"Unable to import {domain}: {ex}")
            return None

        shc_component = SmartHomeControllerComponent.get_component(domain)
        if shc_component is not None:
            try:
                return await shc_component.async_validate_config(config)
            except (vol.Invalid, SmartHomeControllerError) as ex:
                self.async_log_exception(ex, domain, config, integration.documentation)
                return None
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception(f"Unknown error calling {domain} config validator")
                return None

        # Check if the integration has a custom config validator
        config_validator = None
        try:
            config_validator = integration.get_platform("config")
        except ImportError as err:
            # Filter out import error of the config platform.
            # If the config platform contains bad imports, make sure
            # that still fails.
            if err.name != f"{integration.pkg_path}.config":
                _LOGGER.error(f"Error importing config platform {domain}: {err}")
                return None

        if config_validator is not None and hasattr(
            config_validator, "async_validate_config"
        ):
            try:
                return await config_validator.async_validate_config(self._shc, config)
            except (vol.Invalid, SmartHomeControllerError) as ex:
                self.async_log_exception(ex, domain, config, integration.documentation)
                return None
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception(f"Unknown error calling {domain} config validator")
                return None

        # No custom config validator, proceed with schema validation
        if hasattr(component, "CONFIG_SCHEMA"):
            try:
                return component.CONFIG_SCHEMA(config)
            except vol.Invalid as ex:
                self.async_log_exception(ex, domain, config, integration.documentation)
                return None
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception(f"Unknown error calling {domain} CONFIG_SCHEMA")
                return None

        component_platform_schema = getattr(
            component,
            "PLATFORM_SCHEMA_BASE",
            getattr(component, "PLATFORM_SCHEMA", None),
        )

        if component_platform_schema is None:
            return config

        platforms = []
        for p_name, p_config in self.config_per_platform(config, domain):
            # Validate component specific platform schema
            try:
                p_validated = component_platform_schema(p_config)
            except vol.Invalid as ex:
                self.async_log_exception(
                    ex, domain, p_config, integration.documentation
                )
                continue
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception(
                    f"Unknown error validating {p_name} platform config with "
                    + f"{domain} component platform schema",
                )
                continue

            # Not all platform components follow same pattern for platforms
            # So if p_name is None we are not going to validate platform
            # (the automation component is one of them)
            if p_name is None:
                platforms.append(p_validated)
                continue

            try:
                p_integration = await self.async_get_integration_with_requirements(
                    p_name
                )
            except (RequirementsNotFound, IntegrationNotFound) as ex:
                _LOGGER.error(f"Platform error: {domain} - {ex}")
                continue

            try:
                platform = p_integration.get_platform(domain)
            except _LOAD_EXCEPTIONS:
                _LOGGER.exception(f"Platform error: {domain}")
                continue

            # Validate platform specific schema
            if hasattr(platform, "PLATFORM_SCHEMA"):
                try:
                    p_validated = platform.PLATFORM_SCHEMA(p_config)
                except vol.Invalid as ex:
                    self.async_log_exception(
                        ex,
                        f"{domain}.{p_name}",
                        p_config,
                        p_integration.documentation,
                    )
                    continue
                except Exception:  # pylint: disable=broad-except
                    _LOGGER.exception(
                        f"Unknown error validating config for {p_name} platform for "
                        + f"{domain} component with PLATFORM_SCHEMA"
                    )
                    continue

            platforms.append(p_validated)

        # Create a copy of the configuration with all config for current
        # component removed and add validated config back in.
        config = self.config_without_domain(config, domain)
        config[domain] = platforms

        return config

    @callback
    def config_without_domain(self, config: ConfigType, domain: str) -> ConfigType:
        """Return a config with all configuration for a domain removed."""
        filter_keys = self.extract_domain_configs(config, domain)
        return {key: value for key, value in config.items() if key not in filter_keys}

    async def async_check_shc_config_file(self) -> str:
        """Check if Smart Home Controller configuration file is valid.

        This method is a coroutine.
        """

        res = await self._async_check_shc_config_file()

        if not res.errors:
            return None
        return res.error_str

    @staticmethod
    def config_per_platform(
        conf: ConfigType, domain: str
    ) -> collections.abc.Iterable[tuple[str, ConfigType]]:
        """Break a component config into different platforms.

        For example, will find 'switch', 'switch 2', 'switch 3', .. etc
        Async friendly.
        """
        for config_key in SetupManager.extract_domain_configs(conf, domain):
            if not (platform_config := conf[config_key]):
                continue

            if not isinstance(platform_config, list):
                platform_config = [platform_config]

            item: ConfigType
            platform: str
            for item in platform_config:
                try:
                    platform = item.get(Const.CONF_PLATFORM)
                except AttributeError:
                    platform = None

                yield platform, item

    @staticmethod
    def extract_domain_configs(
        conf: ConfigType, domain: str
    ) -> collections.abc.Sequence[str]:
        """Extract keys from config for given domain name.

        Async friendly.
        """
        pattern = re.compile(rf"^{domain}(| .+)$")
        return [key for key in conf.keys() if pattern.match(key)]

    async def _async_check_shc_config_file(self) -> ConfigErrors:
        """Load and check if the Smart Home Controller configuration file is valid.

        This method is a coroutine.
        """
        result = ConfigErrors()
        self.async_clear_install_history()

        def _pack_error(
            package: str, component: str, config: ConfigType, message: str
        ) -> None:
            """Handle errors from packages: _log_pkg_error."""
            message = f"Package {package} setup failed. Component {component} {message}"
            domain = f"smart-home-tng.packages.{package}.{component}"
            pack_config = core_config[Const.CONF_PACKAGES].get(package, config)
            result.add_error(message, domain, pack_config)

        def _comp_error(ex: Exception, domain: str, config: ConfigType) -> None:
            """Handle errors from components: async_log_exception."""
            result.add_error(
                _format_config_error(ex, domain, config)[0],
                domain,
                config,
            )

        # Load configuration.yaml
        config_path = self._shc.config.path(_YAML_CONFIG_FILE)
        try:
            if not await self._shc.async_add_executor_job(os.path.isfile, config_path):
                return result.add_error("File configuration.yaml not found.")

            assert self._shc.config.config_dir is not None

            config = await self._shc.async_add_executor_job(
                self.load_yaml_config_file,
                Secrets(pathlib.Path(self._shc.config.config_dir)),
            )
        except FileNotFoundError:
            return result.add_error(f"File not found: {config_path}")
        except SmartHomeControllerError as err:
            return result.add_error(f"Error loading {config_path}: {err}")

        # Extract and validate core [smart_home_tng] config
        try:
            core_domain = Const.CORE_COMPONENT_NAME
            core_config = config.pop(core_domain, {})
            core_config = _CORE_CONFIG_SCHEMA(core_config)
            result[core_domain] = core_config
        except vol.Invalid as err:
            result.add_error(err, core_domain, core_config)
            core_config = {}

        # Merge packages
        await self.merge_packages_config(
            config, core_config.get(Const.CONF_PACKAGES, {}), _pack_error
        )
        core_config.pop(Const.CONF_PACKAGES, None)

        # Filter out repeating config sections
        components = {key.split(" ")[0] for key in config.keys()}

        # Process and validate config
        for domain in components:
            try:
                integration = await self.async_get_integration_with_requirements(domain)
            except IntegrationNotFound as ex:
                if not self._shc.config.safe_mode:
                    result.add_error(f"Integration error: {domain} - {ex}")
                continue
            except RequirementsNotFound as ex:
                result.add_error(f"Integration error: {domain} - {ex}")
                continue

            try:
                component = integration.get_component()
            except ImportError as ex:
                result.add_error(f"Component error: {domain} - {ex}")
                continue

            shc_comp = SmartHomeControllerComponent.get_component(domain)
            if shc_comp is not None:
                try:
                    result[domain] = (await shc_comp.async_validate_config(config))[
                        domain
                    ]
                    continue
                except (vol.Invalid, SmartHomeControllerError) as ex:
                    _comp_error(ex, domain, config)
                    continue
                except Exception as err:  # pylint: disable=broad-except
                    _LOGGER.exception("Unexpected error validating config")
                    result.add_error(
                        f"Unexpected error calling config validator: {err}",
                        domain,
                        config.get(domain),
                    )
                    continue

            # Check if the integration has a custom config validator
            config_validator = None
            try:
                config_validator = integration.get_platform("config")
            except ImportError as err:
                # Filter out import error of the config platform.
                # If the config platform contains bad imports, make sure
                # that still fails.
                if err.name != f"{integration.pkg_path}.config":
                    result.add_error(f"Error importing config platform {domain}: {err}")
                    continue

            if config_validator is not None and hasattr(
                config_validator, "async_validate_config"
            ):
                try:
                    result[domain] = (
                        await config_validator.async_validate_config(self._shc, config)
                    )[domain]
                    continue
                except (vol.Invalid, SmartHomeControllerError) as ex:
                    _comp_error(ex, domain, config)
                    continue
                except Exception as err:  # pylint: disable=broad-except
                    _LOGGER.exception("Unexpected error validating config")
                    result.add_error(
                        f"Unexpected error calling config validator: {err}",
                        domain,
                        config.get(domain),
                    )
                    continue

            config_schema = getattr(component, "CONFIG_SCHEMA", None)
            if config_schema is not None:
                try:
                    config = config_schema(config)
                    result[domain] = config[domain]
                except vol.Invalid as ex:
                    _comp_error(ex, domain, config)
                    continue

            component_platform_schema = getattr(
                component,
                "PLATFORM_SCHEMA_BASE",
                getattr(component, "PLATFORM_SCHEMA", None),
            )

            if component_platform_schema is None:
                continue

            platforms = []
            for p_name, p_config in self.config_per_platform(config, domain):
                # Validate component specific platform schema
                try:
                    p_validated = component_platform_schema(p_config)
                except vol.Invalid as ex:
                    _comp_error(ex, domain, config)
                    continue

                # Not all platform components follow same pattern for platforms
                # So if p_name is None we are not going to validate platform
                # (the automation component is one of them)
                if p_name is None:
                    platforms.append(p_validated)
                    continue

                try:
                    p_integration = await self.async_get_integration_with_requirements(
                        p_name
                    )
                    platform = p_integration.get_platform(domain)
                except IntegrationNotFound as ex:
                    if not self._shc.config.safe_mode:
                        result.add_error(f"Platform error {domain}.{p_name} - {ex}")
                    continue
                except (
                    RequirementsNotFound,
                    ImportError,
                ) as ex:
                    result.add_error(f"Platform error {domain}.{p_name} - {ex}")
                    continue

                # Validate platform specific schema
                platform_schema = getattr(platform, "PLATFORM_SCHEMA", None)
                if platform_schema is not None:
                    try:
                        p_validated = platform_schema(p_validated)
                    except vol.Invalid as ex:
                        _comp_error(ex, f"{domain}.{p_name}", p_validated)
                        continue

                platforms.append(p_validated)

            # Remove config for current component and add validated config back in.
            for filter_comp in SetupManager.extract_domain_configs(config, domain):
                del config[filter_comp]
            result[domain] = platforms

        return result

    @callback
    def async_clear_install_history(self) -> None:
        """Forget the install history."""
        if install_failure_history := self._shc.data.get(_DATA_INSTALL_FAILURE_HISTORY):
            install_failure_history.clear()

    @staticmethod
    def manifest_from_legacy_module(domain: str, module: types.ModuleType) -> Manifest:
        """Generate a manifest from a legacy module."""
        return {
            "domain": domain,
            "name": domain,
            "requirements": getattr(module, "REQUIREMENTS", []),
            "dependencies": getattr(module, "DEPENDENCIES", []),
            "codeowners": [],
        }

    async def _async_get_custom_components(
        self,
    ) -> dict[str, Integration]:
        """Return list of custom integrations."""
        if self._shc.config.safe_mode:
            return {}

        if (
            self._shc.config.safe_mode
            or not pathlib.Path(self._shc.config.path("custom_components")).is_dir()
        ):
            return {}

        def get_sub_directories(paths: list[str]) -> list[pathlib.Path]:
            """Return all sub directories in a set of paths."""
            return [
                entry
                for path in paths
                for entry in pathlib.Path(path).iterdir()
                if entry.is_dir()
            ]

        custom_components = importlib.import_module(
            self._shc.config.path("custom_components")
        )
        dirs = await self._shc.async_add_executor_job(
            get_sub_directories, custom_components.__path__
        )

        integrations = await helpers.gather_with_concurrency(
            Const.MAX_LOAD_CONCURRENTLY,
            *(
                self._shc.async_add_executor_job(
                    Integration.resolve_from_root,
                    self._shc,
                    custom_components,
                    comp.name,
                )
                for comp in dirs
            ),
        )

        return {
            integration.domain: integration
            for integration in integrations
            if integration is not None
        }

    async def async_get_custom_components(
        self,
    ) -> dict[str, Integration]:
        """Return cached list of custom integrations."""
        if (reg_or_evt := self._shc.data.get(_DATA_CUSTOM_COMPONENTS)) is None:
            evt = self._shc.data[_DATA_CUSTOM_COMPONENTS] = asyncio.Event()

            reg = await self._async_get_custom_components()

            self._shc.data[_DATA_CUSTOM_COMPONENTS] = reg
            evt.set()
            return reg

        if isinstance(reg_or_evt, asyncio.Event):
            await reg_or_evt.wait()
            return typing.cast(
                dict[str, Integration], self._shc.data.get(_DATA_CUSTOM_COMPONENTS)
            )

        return typing.cast(dict[str, Integration], reg_or_evt)

    async def async_get_config_flows(
        self,
        type_filter: typing.Literal["helper", "integration"] = None,
    ) -> set[str]:
        """Return cached list of config flows."""

        integrations = await self.async_get_custom_components()
        flows: set[str] = set()

        if type_filter is not None:
            flows.update(generated.FLOWS[type_filter])
        else:
            for type_flows in generated.FLOWS.values():
                flows.update(type_flows)

        flows.update(
            [
                integration.domain
                for integration in integrations.values()
                if integration.config_flow
                and (type_filter is None or integration.integration_type == type_filter)
            ]
        )

        return flows

    async def async_get_application_credentials(self) -> list[str]:
        """Return cached list of application credentials."""
        integrations = await self.async_get_custom_components()

        return [
            *generated.APPLICATION_CREDENTIALS,
            *[
                integration.domain
                for integration in integrations.values()
                if Platform.APPLICATION_CREDENTIALS.value in integration.dependencies
            ],
        ]

    @staticmethod
    def async_process_zeroconf_match_dict(
        entry: dict[str, typing.Any]
    ) -> dict[str, typing.Any]:
        """Handle backwards compat with zeroconf matchers."""
        entry_without_type: dict[str, typing.Any] = entry.copy()
        del entry_without_type["type"]
        # These properties keys used to be at the top level, we relocate
        # them for backwards compat
        for moved_prop in _MOVED_ZEROCONF_PROPS:
            if value := entry_without_type.pop(moved_prop, None):
                _LOGGER.warning(
                    f'Matching the zeroconf property "{moved_prop}" at top-level is deprecated and '
                    + "should be moved into a properties dict; Check the developer documentation",
                )
                if "properties" not in entry_without_type:
                    prop_dict: dict[str, str] = {}
                    entry_without_type["properties"] = prop_dict
                else:
                    prop_dict = entry_without_type["properties"]
                prop_dict[moved_prop] = value.lower()
        return entry_without_type

    async def async_get_zeroconf(
        self,
    ) -> dict[str, list[dict[str, str | dict[str, str]]]]:
        """Return cached list of zeroconf types."""
        zeroconf: dict[
            str, list[dict[str, str | dict[str, str]]]
        ] = generated.ZEROCONF.copy()

        integrations = await self.async_get_custom_components()
        for integration in integrations.values():
            if not integration.zeroconf:
                continue
            for entry in integration.zeroconf:
                data: dict[str, str | dict[str, str]] = {"domain": integration.domain}
                if isinstance(entry, dict):
                    typ = entry["type"]
                    data.update(self.async_process_zeroconf_match_dict(entry))
                else:
                    typ = entry

                zeroconf.setdefault(typ, []).append(data)

        return zeroconf

    async def async_get_dhcp(self) -> list[DHCPMatcher]:
        """Return cached list of dhcp types."""
        dhcp = typing.cast(list[DHCPMatcher], generated.DHCP.copy())

        integrations = await self.async_get_custom_components()
        for integration in integrations.values():
            if not integration.dhcp:
                continue
            for entry in integration.dhcp:
                dhcp.append(
                    typing.cast(DHCPMatcher, {"domain": integration.domain, **entry})
                )

        return dhcp

    async def async_get_usb(self) -> list[dict[str, str]]:
        """Return cached list of usb types."""
        usb: list[dict[str, str]] = generated.USB.copy()

        integrations = await self.async_get_custom_components()
        for integration in integrations.values():
            if not integration.usb:
                continue
            for entry in integration.usb:
                usb.append(
                    {
                        "domain": integration.domain,
                        **{k: v for k, v in entry.items() if k != "known_devices"},
                    }
                )

        return usb

    async def async_get_homekit(self) -> dict[str, str]:
        """Return cached list of homekit models."""

        homekit: dict[str, str] = generated.HOMEKIT.copy()

        integrations = await self.async_get_custom_components()
        for integration in integrations.values():
            if (
                not integration.homekit
                or "models" not in integration.homekit
                or not integration.homekit["models"]
            ):
                continue
            for model in integration.homekit["models"]:
                homekit[model] = integration.domain

        return homekit

    async def async_get_ssdp(self) -> dict[str, list[dict[str, str]]]:
        """Return cached list of ssdp mappings."""

        ssdp: dict[str, list[dict[str, str]]] = generated.SSDP.copy()

        integrations = await self.async_get_custom_components()
        for integration in integrations.values():
            if not integration.ssdp:
                continue

            ssdp[integration.domain] = integration.ssdp

        return ssdp

    async def async_get_mqtt(self) -> dict[str, list[str]]:
        """Return cached list of MQTT mappings."""

        mqtt: dict[str, list[str]] = generated.MQTT.copy()

        integrations = await self.async_get_custom_components()
        for integration in integrations.values():
            if not integration.mqtt:
                continue

            mqtt[integration.domain] = integration.mqtt

        return mqtt

    async def async_get_integration(self, domain: str) -> Integration:
        """Get an integration."""
        if (cache := self._shc.data.get(_DATA_INTEGRATIONS)) is None:
            if not self._async_mount_config_dir():
                raise IntegrationNotFound(domain)
            cache = self._shc.data[_DATA_INTEGRATIONS] = {}

        int_or_evt: Integration | asyncio.Event = cache.get(domain, _UNDEF)

        if isinstance(int_or_evt, asyncio.Event):
            await int_or_evt.wait()

            # When we have waited and it's _UNDEF, it doesn't exist
            # We don't cache that it doesn't exist, or else people can't fix it
            # and then restart, because their config will never be valid.
            if (int_or_evt := cache.get(domain, _UNDEF)) is _UNDEF:
                raise IntegrationNotFound(domain)

        if int_or_evt is not _UNDEF:
            return typing.cast(Integration, int_or_evt)

        event = cache[domain] = asyncio.Event()

        try:
            integration = await self._async_get_integration(domain)
        except Exception:
            # Remove event from cache.
            cache.pop(domain)
            event.set()
            raise

        cache[domain] = integration
        event.set()
        return integration

    async def async_get_integrations(
        self, domains: typing.Iterable[str]
    ) -> dict[str, Integration | Exception]:
        """Get integrations."""
        if (cache := self._shc.data.get(_DATA_INTEGRATIONS)) is None:
            if not self._async_mount_config_dir():
                return {domain: IntegrationNotFound(domain) for domain in domains}
            cache = self._shc.data[_DATA_INTEGRATIONS] = {}

        results: dict[str, Integration | Exception] = {}
        needed: dict[str, asyncio.Event] = {}
        in_progress: dict[str, asyncio.Event] = {}
        for domain in domains:
            int_or_evt: Integration | asyncio.Event = cache.get(domain, _UNDEF)
            if isinstance(int_or_evt, asyncio.Event):
                in_progress[domain] = int_or_evt
            elif int_or_evt is not _UNDEF:
                results[domain] = int_or_evt
            elif "." in domain:
                results[domain] = ValueError(f"Invalid domain {domain}")
            else:
                needed[domain] = cache[domain] = asyncio.Event()

        if in_progress:
            await asyncio.gather(*[event.wait() for event in in_progress.values()])
            for domain in in_progress:
                # When we have waited and it's _UNDEF, it doesn't exist
                # We don't cache that it doesn't exist, or else people can't fix it
                # and then restart, because their config will never be valid.
                if (int_or_evt := cache.get(domain, _UNDEF)) is _UNDEF:
                    results[domain] = IntegrationNotFound(domain)
                else:
                    results[domain] = int_or_evt

        # First we look for custom components
        if needed:
            # Instead of using resolve_from_root we use the cache of custom
            # components to find the integration.
            custom = await self.async_get_custom_components()
            for domain, event in needed.items():
                if integration := custom.get(domain):
                    results[domain] = cache[domain] = integration
                    event.set()

            for domain in results:
                if domain in needed:
                    del needed[domain]

        # Now the rest use resolve_from_root
        if needed:
            components = importlib.import_module(".components", "smart_home_tng")
            integrations = await self._shc.async_add_executor_job(
                _resolve_integrations_from_root, self._shc, components, list(needed)
            )
            for domain, event in needed.items():
                int_or_exc = integrations.get(domain)
                if not int_or_exc:
                    cache.pop(domain)
                    results[domain] = IntegrationNotFound(domain)
                elif isinstance(int_or_exc, Exception):
                    cache.pop(domain)
                    exc = IntegrationNotFound(domain)
                    exc.__cause__ = int_or_exc
                    results[domain] = exc
                else:
                    results[domain] = cache[domain] = int_or_exc
                event.set()

        return results

    async def _async_get_integration(self, domain: str) -> Integration:
        if "." in domain:
            raise ValueError(f"Invalid domain {domain}")

        # Instead of using resolve_from_root we use the cache of custom
        # components to find the integration.
        if integration := (await self.async_get_custom_components()).get(domain):
            return integration

        components = importlib.import_module(".components", "smart_home_tng")

        if integration := await self._shc.async_add_executor_job(
            Integration.resolve_from_root, self._shc, components, domain
        ):
            return integration

        raise IntegrationNotFound(domain)

    async def async_component_dependencies(
        self,
        start_domain: str,
        integration: Integration,
        loaded: set[str],
        loading: set[str],
    ) -> set[str]:
        """Recursive function to get component dependencies.

        Async friendly.
        """
        domain = integration.domain
        loading.add(domain)

        for dependency_domain in integration.dependencies:
            # Check not already loaded
            if dependency_domain in loaded:
                continue

            # If we are already loading it, we have a circular dependency.
            if dependency_domain in loading:
                raise CircularDependency(domain, dependency_domain)

            loaded.add(dependency_domain)

            dep_integration = await self.async_get_integration(dependency_domain)

            if start_domain in dep_integration.after_dependencies:
                raise CircularDependency(start_domain, dependency_domain)

            if dep_integration.dependencies:
                dep_loaded = await self.async_component_dependencies(
                    start_domain, dep_integration, loaded, loading
                )

                loaded.update(dep_loaded)

        loaded.add(domain)
        loading.remove(domain)

        return loaded

    def _async_mount_config_dir(self) -> bool:
        """Mount config dir in order to load custom_component.

        Async friendly but not a coroutine.
        """
        if self._shc.config.config_dir is None:
            _LOGGER.error(
                "Can't load integrations - configuration directory is not set"
            )
            return False
        if self._shc.config.config_dir not in sys.path:
            sys.path.insert(0, self._shc.config.config_dir)
        return True

    def _lookup_path(self) -> list[str]:
        """Return the lookup paths for legacy lookups."""
        if self._shc.config.safe_mode:
            return [_PACKAGE_BUILTIN]
        return [_PACKAGE_CUSTOM_COMPONENTS, _PACKAGE_BUILTIN]

    async def async_get_integration_with_requirements(
        self, domain: str, done: set[str] = None
    ) -> Integration:
        """Get an integration with all requirements installed, including the dependencies.

        This can raise IntegrationNotFound if manifest or integration
        is invalid, RequirementNotFound if there was some type of
        failure to install requirements.
        """
        if done is None:
            done = {domain}
        else:
            done.add(domain)

        integration = await self.async_get_integration(domain)

        if self._shc.config.skip_pip:
            return integration

        if (cache := self._shc.data.get(_DATA_INTEGRATIONS_WITH_REQS)) is None:
            cache = self._shc.data[_DATA_INTEGRATIONS_WITH_REQS] = {}

        int_or_evt: Integration | asyncio.Event | object = cache.get(domain, _UNDEF)

        if isinstance(int_or_evt, asyncio.Event):
            await int_or_evt.wait()

            # When we have waited and it's UNDEFINED, it doesn't exist
            # We don't cache that it doesn't exist, or else people can't fix it
            # and then restart, because their config will never be valid.
            if (int_or_evt := cache.get(domain, _UNDEF)) is _UNDEF:
                raise IntegrationNotFound(domain)

        if int_or_evt is not _UNDEF:
            return typing.cast(Integration, int_or_evt)

        event = cache[domain] = asyncio.Event()

        try:
            await self._async_process_integration(integration, done)
        except Exception:
            del cache[domain]
            event.set()
            raise

        cache[domain] = integration
        event.set()
        return integration

    async def _async_process_integration(
        self, integration: Integration, done: set[str]
    ) -> None:
        """Process an integration and requirements."""
        if integration.requirements:
            await self.async_process_requirements(
                integration.domain, integration.requirements
            )

        deps_to_check = [
            dep
            for dep in integration.dependencies + integration.after_dependencies
            if dep not in done
        ]

        for check_domain, to_check in _DISCOVERY_INTEGRATIONS.items():
            if (
                check_domain not in done
                and check_domain not in deps_to_check
                and any(check in integration.manifest for check in to_check)
            ):
                deps_to_check.append(check_domain)

        if not deps_to_check:
            return

        results = await asyncio.gather(
            *(
                self.async_get_integration_with_requirements(dep, done)
                for dep in deps_to_check
            ),
            return_exceptions=True,
        )
        for result in results:
            if not isinstance(result, BaseException):
                continue
            if not isinstance(result, IntegrationNotFound) or not (
                not integration.is_built_in
                and result.domain in integration.after_dependencies
            ):
                raise result

    async def async_process_requirements(
        self, name: str, requirements: list[str]
    ) -> None:
        """Install the requirements for a component or platform.

        This method is a coroutine. It will raise RequirementsNotFound
        if an requirement can't be satisfied.
        """
        if (pip_lock := self._shc.data.get(_DATA_PIP_LOCK)) is None:
            pip_lock = self._shc.data[_DATA_PIP_LOCK] = asyncio.Lock()
        install_failure_history = self._shc.data.get(_DATA_INSTALL_FAILURE_HISTORY)
        if install_failure_history is None:
            install_failure_history = self._shc.data[
                _DATA_INSTALL_FAILURE_HISTORY
            ] = set()

        kwargs = self.pip_kwargs()

        async with pip_lock:
            for req in requirements:
                await self._async_process_requirements(
                    name, req, install_failure_history, kwargs
                )

    async def _async_process_requirements(
        self,
        name: str,
        req: str,
        install_failure_history: set[str],
        kwargs: typing.Any,
    ) -> None:
        """Install a requirement and save failures."""
        if req in install_failure_history:
            _LOGGER.info(
                f"Multiple attempts to install {req} failed, "
                + "install will be retried after next configuration check or restart",
            )
            raise RequirementsNotFound(name, [req])

        if self.is_installed(req):
            return

        def _install(req: str, kwargs: dict[str, typing.Any]) -> bool:
            """Install requirement."""
            return self.install_package(req, **kwargs)

        for _ in range(_MAX_INSTALL_FAILURES):
            if await self._shc.async_add_executor_job(_install, req, kwargs):
                return

        install_failure_history.add(req)
        raise RequirementsNotFound(name, [req])

    @staticmethod
    def is_installed(package: str) -> bool:
        """Check if a package is installed and will be loaded when we import it.

        Returns True when the requirement is met.
        Returns False when the package is not installed or doesn't meet req.
        """
        try:
            pkg_resources.get_distribution(package)
            return True
        except (pkg_resources.ResolutionError, pkg_resources.ExtractionError):
            req = pkg_resources.Requirement.parse(package)
        except ValueError:
            # This is a zip file. We no longer use this in Smart Home - TNG,
            # leaving it in for custom components.
            tmp = url.parse_url(package)
            if tmp is None:
                return False
            req = pkg_resources.Requirement.parse(tmp.fragment)

        try:
            installed_version = metadata.version(req.project_name)
            # This will happen when an install failed or
            # was aborted while in progress see
            # https://github.com/home-assistant/core/issues/47699
            if installed_version is None:
                _LOGGER.error(
                    f"Installed version for {req.project_name} resolved to None"
                )
                return False
            return installed_version in req
        except metadata.PackageNotFoundError:
            return False

    def pip_kwargs(self) -> dict[str, typing.Any]:
        """Return keyword arguments for PIP install."""
        config_dir = self._shc.config.config_dir
        is_docker = self._shc.is_docker_env()
        constraint_file = os.path.join(os.path.dirname(__file__), _CONSTRAINT_FILE)
        kwargs = {
            "no_cache_dir": is_docker,
            "timeout": _PIP_TIMEOUT,
        }
        if pathlib.Path(constraint_file).is_file():
            kwargs["constraints"] = constraint_file
        if "WHEELS_LINKS" in os.environ:
            kwargs["find_links"] = os.environ["WHEELS_LINKS"]
        if config_dir is not None and not self._shc.is_virtual_env() and not is_docker:
            kwargs["target"] = os.path.join(config_dir, "deps")
        return kwargs

    def install_package(
        self,
        package: str,
        upgrade: bool = True,
        target: str = None,
        constraints: str = None,
        find_links: str = None,
        timeout: int = None,
        no_cache_dir: bool = False,
    ) -> bool:
        """Install a package on PyPi. Accepts pip compatible package strings.

        Return boolean if install successful.
        """
        # Not using 'import pip; pip.main([])' because it breaks the logger
        _LOGGER.info(f"Attempting install of {package}")
        env = os.environ.copy()
        args = [sys.executable, "-m", "pip", "install", "--quiet", package]
        if timeout:
            args += ["--timeout", str(timeout)]
        if no_cache_dir:
            args.append("--no-cache-dir")
        if upgrade:
            args.append("--upgrade")
        if constraints is not None:
            args += ["--constraint", constraints]
        if find_links is not None:
            args += ["--find-links", find_links, "--prefer-binary"]
        if target:
            assert not self._shc.is_virtual_env()
            # This only works if not running in venv
            args += ["--user"]
            env["PYTHONUSERBASE"] = os.path.abspath(target)
            # Workaround for incompatible prefix setting
            # See http://stackoverflow.com/a/4495175
            args += ["--prefix="]
        _LOGGER.debug(f"Running pip command: args={args}")
        with subprocess.Popen(  # nosec
            args,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=env,
        ) as process:
            _, stderr = process.communicate()
            if process.returncode != 0:
                _LOGGER.error(
                    f"Unable to install package {package}: "
                    + f"{stderr.decode('utf-8').lstrip().strip()}"
                )
                return False

        return True

    async def async_from_config_dict(self, config: ConfigType) -> SmartHomeController:
        """Try to configure the Smart Home Controller from a configuration dictionary.

        Dynamically loads required components and its dependencies.
        This method is a coroutine.
        """
        start = time.monotonic()

        config_entries = ConfigEntries(self._shc, config)
        self._shc.config_entries = config_entries
        await config_entries.async_initialize()

        # Set up core.
        _LOGGER.debug(f"Setting up {_CORE_INTEGRATIONS}")

        if not all(
            await asyncio.gather(
                *(
                    self.async_setup_component(domain, config)
                    for domain in _CORE_INTEGRATIONS
                )
            )
        ):
            _LOGGER.error("Smart Home - The Next Generation core failed to initialize.")
            return None

        _LOGGER.debug("Smart Home - The Next Generation core initialized")

        core_config = config.get(Const.CORE_COMPONENT_NAME, {})

        try:
            await self.async_process_shc_core_config(core_config)
        except vol.Invalid as config_err:
            self.async_log_exception(config_err, Const.CORE_COMPONENT_NAME, core_config)
            return None
        except SmartHomeControllerError:
            _LOGGER.error(
                "Smart Home - The Next Generation core failed to initialize. "
                + "Further initialization aborted"
            )
            return None

        await self._async_set_up_integrations(config)

        stop = time.monotonic()
        _LOGGER.info(
            "Smart Home - The Next Generation initialized in " + f"{stop - start:.2f}s"
        )

        if (
            Const.REQUIRED_NEXT_PYTHON_SHC_RELEASE
            and sys.version_info[:3] < Const.REQUIRED_NEXT_PYTHON_VER
        ):
            msg = (
                "Support for the running Python version "
                f"{'.'.join(str(x) for x in sys.version_info[:3])} is deprecated and will "
                f"be removed in Home Assistant {Const.REQUIRED_NEXT_PYTHON_SHC_RELEASE}. "
                "Please upgrade Python to "
                f"{'.'.join(str(x) for x in Const.REQUIRED_NEXT_PYTHON_VER[:2])}."
            )
            _LOGGER.warning(msg)

            comp = SmartHomeControllerComponent.get_component(
                Const.PERSISTENT_NOTIFICATION_COMPONENT_NAME
            )
            if isinstance(comp, PersistentNotificationComponent):
                comp.async_create(msg, "Python Version", "python_version")

        return self._shc

    @callback
    def async_enable_logging(
        self,
        verbose: bool = False,
        log_rotate_days: int = None,
        log_file: str = None,
        log_no_color: bool = False,
    ) -> None:
        """Set up the logging.

        This method must be run in the event loop.
        """
        fmt = "%(asctime)s %(levelname)s (%(threadName)s) [%(name)s] %(message)s"
        datefmt = "%Y-%m-%d %H:%M:%S"

        if not log_no_color:
            try:
                # pylint: disable=import-outside-toplevel
                from colorlog import ColoredFormatter

                # basicConfig must be called after importing colorlog in order to
                # ensure that the handlers it sets up wraps the correct streams.
                logging.basicConfig(level=logging.INFO)

                colorfmt = f"%(log_color)s{fmt}%(reset)s"
                logging.getLogger().handlers[0].setFormatter(
                    ColoredFormatter(
                        colorfmt,
                        datefmt=datefmt,
                        reset=True,
                        log_colors={
                            "DEBUG": "cyan",
                            "INFO": "green",
                            "WARNING": "yellow",
                            "ERROR": "red",
                            "CRITICAL": "red",
                        },
                    )
                )
            except ImportError:
                pass

        # If the above initialization failed for any reason, setup the default
        # formatting.  If the above succeeds, this will result in a no-op.
        logging.basicConfig(format=fmt, datefmt=datefmt, level=logging.INFO)

        # Suppress overly verbose logs from libraries that aren't helpful
        logging.getLogger("requests").setLevel(logging.WARNING)
        logging.getLogger("urllib3").setLevel(logging.WARNING)
        logging.getLogger("aiohttp.access").setLevel(logging.WARNING)

        sys.excepthook = lambda *args: logging.getLogger(None).exception(
            "Uncaught exception", exc_info=args  # type: ignore[arg-type]
        )
        threading.excepthook = lambda args: logging.getLogger(None).exception(
            "Uncaught thread exception",
            exc_info=(args.exc_type, args.exc_value, args.exc_traceback),  # type: ignore[arg-type]
        )

        # Log errors to a file if we have write access to file or config dir
        if log_file is None:
            err_log_path = self._shc.config.path(_ERROR_LOG_FILENAME)
        else:
            err_log_path = os.path.abspath(log_file)

        err_path_exists = os.path.isfile(err_log_path)
        err_dir = os.path.dirname(err_log_path)

        # Check if we can write to the error log if it exists or that
        # we can create files in the containing directory if not.
        if (err_path_exists and os.access(err_log_path, os.W_OK)) or (
            not err_path_exists and os.access(err_dir, os.W_OK)
        ):
            # fmt: off

            err_handler: logging.handlers.RotatingFileHandler | \
                logging.handlers.TimedRotatingFileHandler

            # fmt: on

            if log_rotate_days:
                err_handler = logging.handlers.TimedRotatingFileHandler(
                    err_log_path, when="midnight", backupCount=log_rotate_days
                )
            else:
                err_handler = logging.handlers.RotatingFileHandler(
                    err_log_path, backupCount=1
                )

            try:
                err_handler.doRollover()
            except OSError as err:
                _LOGGER.error(f"Error rolling over log file: {err}")

            err_handler.setLevel(logging.INFO if verbose else logging.WARNING)
            err_handler.setFormatter(logging.Formatter(fmt, datefmt=datefmt))

            logger = logging.getLogger("")
            logger.addHandler(err_handler)
            logger.setLevel(logging.INFO if verbose else logging.WARNING)

            # Save the log file location for access by other components.
            self._shc.config.error_log_path = err_log_path
        else:
            _LOGGER.error(f"Unable to set up error log {err_log_path} (access denied)")

        self.async_activate_log_queue_handler()

    async def async_mount_local_lib_path(self) -> str:
        """Add local library to Python Path.

        This function is a coroutine.
        """
        config_dir = self._shc.config.config_dir
        deps_dir = os.path.join(config_dir, "deps")
        if (lib_dir := await self.async_get_user_site(deps_dir)) not in sys.path:
            sys.path.insert(0, lib_dir)
        return deps_dir

    @callback
    def _get_domains(self, config: dict[str, typing.Any]) -> set[str]:
        """Get domains of components to set up."""
        # Filter out the repeating and common config section [smart_home_tng]
        domains = {
            key.split(" ")[0] for key in config if key != Const.CORE_COMPONENT_NAME
        }

        # Add config entry domains
        if not self._shc.config.safe_mode:
            domains.update(self._shc.config_entries.async_domains())

        # Make sure the Hass.io component is loaded
        if "HASSIO" in os.environ:
            domains.add("hassio")

        return domains

    async def _async_watch_pending_setups(self) -> None:
        """Periodic log of setups that are pending for longer than LOG_SLOW_STARTUP_INTERVAL."""
        loop_count = 0
        setup_started: dict[str, datetime.datetime] = self._shc.data[
            _DATA_SETUP_STARTED
        ]
        previous_was_empty = True
        while True:
            now = helpers.utcnow()
            remaining_with_setup_started = {
                domain: (now - setup_started[domain]).total_seconds()
                for domain in setup_started
            }
            _LOGGER.debug(f"Integration remaining: {remaining_with_setup_started}")
            if remaining_with_setup_started or not previous_was_empty:
                self._shc.dispatcher.async_send(
                    Const.SIGNAL_BOOTSTRAP_INTEGRATONS, remaining_with_setup_started
                )
            previous_was_empty = not remaining_with_setup_started
            await asyncio.sleep(_SLOW_STARTUP_CHECK_INTERVAL)
            loop_count += _SLOW_STARTUP_CHECK_INTERVAL

            if loop_count >= _LOG_SLOW_STARTUP_INTERVAL and setup_started:
                _LOGGER.warning(
                    "Waiting on integrations to complete setup: "
                    + f"{', '.join(setup_started)}"
                )
                loop_count = 0
            _LOGGER.debug(f"Running timeout Zones: {self._shc.timeout.zones}")

    async def async_setup_multi_components(
        self,
        domains: set[str],
        config: dict[str, typing.Any],
    ) -> None:
        """Set up multiple domains. Log on failure."""
        futures = {
            domain: self._shc.async_create_task(
                self.async_setup_component(domain, config)
            )
            for domain in domains
        }
        await asyncio.wait(futures.values())
        errors = [domain for domain in domains if futures[domain].exception()]
        for domain in errors:
            exception = futures[domain].exception()
            assert exception is not None
            _LOGGER.error(
                f"Error setting up integration {domain} - received exception",
                exc_info=(type(exception), exception, exception.__traceback__),
            )

    async def _async_set_up_integrations(self, config: dict[str, typing.Any]) -> None:
        """Set up all the integrations."""
        self._shc.data[_DATA_SETUP_STARTED] = {}
        setup_time: dict[str, datetime.timedelta] = self._shc.data.setdefault(
            _DATA_SETUP_TIME, {}
        )

        watch_task = asyncio.create_task(self._async_watch_pending_setups())

        domains_to_setup = self._get_domains(config)

        # Resolve all dependencies so we know all integrations
        # that will have to be loaded and start rightaway
        integration_cache: dict[str, Integration] = {}
        to_resolve: set[str] = domains_to_setup
        while to_resolve:
            old_to_resolve: set[str] = to_resolve
            to_resolve = set()

            integrations_to_process = [
                int_or_exc
                for int_or_exc in await helpers.gather_with_concurrency(
                    Const.MAX_LOAD_CONCURRENTLY,
                    *(self.async_get_integration(domain) for domain in old_to_resolve),
                    return_exceptions=True,
                )
                if isinstance(int_or_exc, Integration)
            ]
            resolve_dependencies_tasks = [
                itg.resolve_dependencies()
                for itg in integrations_to_process
                if not itg.all_dependencies_resolved
            ]

            if resolve_dependencies_tasks:
                await asyncio.gather(*resolve_dependencies_tasks)

            for itg in integrations_to_process:
                integration_cache[itg.domain] = itg

                for dep in itg.all_dependencies:
                    if dep in domains_to_setup:
                        continue

                    domains_to_setup.add(dep)
                    to_resolve.add(dep)

        _LOGGER.info(f"Domains to be set up: {domains_to_setup}", domains_to_setup)

        # Load logging as soon as possible
        if logging_domains := domains_to_setup & _LOGGING_INTEGRATIONS:
            _LOGGER.info(f"Setting up logging: {logging_domains}")
            await self.async_setup_multi_components(logging_domains, config)

        # Start up debuggers. Start these first in case they want to wait.
        if debuggers := domains_to_setup & _DEBUGGER_INTEGRATIONS:
            _LOGGER.debug(f"Setting up debuggers: {debuggers}")
            await self.async_setup_multi_components(debuggers, config)

        # calculate what components to setup in what stage
        stage_1_domains: set[str] = set()

        # Find all dependencies of any dependency of any stage 1 integration that
        # we plan on loading and promote them to stage 1
        deps_promotion: set[str] = _STAGE_1_INTEGRATIONS
        while deps_promotion:
            old_deps_promotion = deps_promotion
            deps_promotion = set()

            for domain in old_deps_promotion:
                if domain not in domains_to_setup or domain in stage_1_domains:
                    continue

                stage_1_domains.add(domain)

                if (dep_itg := integration_cache.get(domain)) is None:
                    continue

                deps_promotion.update(dep_itg.all_dependencies)

        stage_2_domains = (
            domains_to_setup - logging_domains - debuggers - stage_1_domains
        )

        # Load the registries
        await asyncio.gather(
            self._shc.device_registry.async_load(),
            self._shc.entity_registry.async_load(),
            self._shc.area_registry.async_load(),
        )

        # Start setup
        if stage_1_domains:
            _LOGGER.info(f"Setting up stage 1: {stage_1_domains}")
            try:
                async with self._shc.timeout.async_timeout(
                    _STAGE_1_TIMEOUT, cool_down=_COOLDOWN_TIME
                ):
                    await self.async_setup_multi_components(stage_1_domains, config)
            except asyncio.TimeoutError:
                _LOGGER.warning("Setup timed out for stage 1 - moving forward")

        # Enables after dependencies
        self.async_set_domains_to_be_loaded(stage_2_domains)

        if stage_2_domains:
            _LOGGER.info(f"Setting up stage 2: {stage_2_domains}")
            try:
                async with self._shc.timeout.async_timeout(
                    _STAGE_2_TIMEOUT, cool_down=_COOLDOWN_TIME
                ):
                    await self.async_setup_multi_components(stage_2_domains, config)
            except asyncio.TimeoutError:
                _LOGGER.warning("Setup timed out for stage 2 - moving forward")

        # Wrap up startup
        _LOGGER.debug("Waiting for startup to wrap up")
        try:
            async with self._shc.timeout.async_timeout(
                _WRAP_UP_TIMEOUT, cool_down=_COOLDOWN_TIME
            ):
                await self._shc.async_block_till_done()
        except asyncio.TimeoutError:
            _LOGGER.warning("Setup timed out for bootstrap - moving forward")

        watch_task.cancel()
        self._shc.dispatcher.async_send(Const.SIGNAL_BOOTSTRAP_INTEGRATONS, {})

        setup_times = {
            integration: timedelta.total_seconds()
            for integration, timedelta in sorted(
                setup_time.items(), key=lambda item: item[1].total_seconds()
            )
        }
        _LOGGER.debug(f"Integration setup times: {setup_times}")

    @callback
    def async_activate_log_queue_handler(self) -> None:
        """
        Migrate the existing log handlers to use the queue.

        This allows us to avoid blocking I/O and formatting messages
        in the event loop as log messages are written in another thread.
        """
        simple_queue: queue.SimpleQueue[logging.Handler] = queue.SimpleQueue()
        queue_handler = QueueLoggingHandler(simple_queue)
        logging.root.addHandler(queue_handler)

        migrated_handlers: list[logging.Handler] = []
        for handler in logging.root.handlers[:]:
            if handler is queue_handler:
                continue
            logging.root.removeHandler(handler)
            migrated_handlers.append(handler)

        listener = logging.handlers.QueueListener(simple_queue, *migrated_handlers)

        listener.start()

        @callback
        def _async_stop_queue_handler(_: typing.Any) -> None:
            """Cleanup handler."""
            # Ensure any messages that happen after close still get logged
            for original_handler in migrated_handlers:
                logging.root.addHandler(original_handler)
            logging.root.removeHandler(queue_handler)
            listener.stop()

        self._shc.bus.async_listen_once(
            Const.EVENT_SHC_CLOSE, _async_stop_queue_handler
        )

    @staticmethod
    async def async_get_user_site(deps_dir: str) -> str:
        """Return user local library path.

        This function is a coroutine.
        """
        env = os.environ.copy()
        env["PYTHONUSERBASE"] = os.path.abspath(deps_dir)
        args = [sys.executable, "-m", "site", "--user-site"]
        process = await asyncio.create_subprocess_exec(
            *args,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.DEVNULL,
            env=env,
        )
        stdout, _ = await process.communicate()
        lib_dir = stdout.decode().strip()
        return lib_dir

    async def load_auth_provider_module(self, provider: str) -> types.ModuleType:
        """Load an auth provider."""
        try:
            module = importlib.import_module(
                f"smart_home_tng.auth.providers.{provider}"
            )
        except ImportError as err:
            _LOGGER.error(f"Unable to load auth provider {provider}: {err}")
            raise SmartHomeControllerError(
                f"Unable to load auth provider {provider}: {err}"
            ) from err

        if self._shc.config.skip_pip or not hasattr(module, "REQUIREMENTS"):
            return module

        if (processed := self._shc.data.get(_DATA_AUTH_REQS)) is None:
            processed = self._shc.data[_DATA_AUTH_REQS] = set()
        elif provider in processed:
            return module

        reqs = module.REQUIREMENTS
        await self.async_process_requirements(f"auth provider {provider}", reqs)

        processed.add(provider)
        return module

    async def load_mfa_module(self, module_name: str) -> types.ModuleType:
        """Load an mfa auth module."""
        module_path = f"smart_home_tng.auth.mfa_modules.{module_name}"

        try:
            module = importlib.import_module(module_path)
        except ImportError as err:
            _LOGGER.error(f"Unable to load mfa module {module_name}: {err}")
            raise SmartHomeControllerError(
                f"Unable to load mfa module {module_name}: {err}"
            ) from err

        if self._shc.config.skip_pip or not hasattr(module, "REQUIREMENTS"):
            return module

        processed = self._shc.data.get(_DATA_MFA_REQS)
        if processed and module_name in processed:
            return module

        processed = self._shc.data[_DATA_MFA_REQS] = set()

        await self.async_process_requirements(module_path, module.REQUIREMENTS)

        processed.add(module_name)
        return module

    def load_file(
        self, comp_or_platform: str, base_paths: list[str]
    ) -> types.ModuleType:
        """Try to load specified file.

        Looks in config dir first, then built-in components.
        Only returns it if also found to be valid.
        Async friendly.
        """
        with contextlib.suppress(KeyError):
            return self._shc.data[_DATA_COMPONENTS][comp_or_platform]

        if (cache := self._shc.data.get(_DATA_COMPONENTS)) is None:
            if not self._async_mount_config_dir():
                return None
            cache = self._shc.data[_DATA_COMPONENTS] = {}

        for path in (f"{base}.{comp_or_platform}" for base in base_paths):
            try:
                module = importlib.import_module(path)

                # In Python 3 you can import files from directories that do not
                # contain the file __init__.py. A directory is a valid module if
                # it contains a file with the .py extension. In this case Python
                # will succeed in importing the directory as a module and call it
                # a namespace. We do not care about namespaces.
                # This prevents that when only
                # custom_components/switch/some_platform.py exists,
                # the import custom_components.switch would succeed.
                # __file__ was unset for namespaces before Python 3.7
                if getattr(module, "__file__", None) is None:
                    continue

                cache[comp_or_platform] = module

                return module

            except ImportError as err:
                # This error happens if for example custom_components/switch
                # exists and we try to load switch.demo.
                # Ignore errors for custom_components, custom_components.switch
                # and custom_components.switch.demo.
                white_listed_errors = []
                parts = []
                for part in path.split("."):
                    parts.append(part)
                    white_listed_errors.append(f"No module named '{'.'.join(parts)}'")

                if str(err) not in white_listed_errors:
                    _LOGGER.exception(
                        f"Error loading {path}. Make sure all dependencies are installed."
                    )
        return None

    async def support_entry_unload(self, domain: str) -> bool:
        """Test if a domain supports entry unloading."""
        integration = await self.async_get_integration(domain)
        component = integration.get_component()
        shc_comp = SmartHomeControllerComponent.get_component(domain)
        if shc_comp is not None:
            return shc_comp.supports_entry_unload
        return hasattr(component, "async_unload_entry")

    async def support_remove_from_device(self, domain: str) -> bool:
        """Test if a domain supports being removed from a device."""
        integration = await self.async_get_integration(domain)
        component = integration.get_component()
        shc_comp = SmartHomeControllerComponent.get_component(domain)
        if shc_comp is not None:
            return shc_comp.supports_remove_from_device
        return hasattr(component, "async_remove_config_entry_device")

    async def _async_process_single_integration_platform_component(
        self, component_name: str, integration_platform: IntegrationPlatform
    ) -> None:
        """Process a single integration platform."""
        if component_name in integration_platform.seen_components:
            return
        integration_platform.seen_components.add(component_name)

        platform_name = integration_platform.platform_name

        comp = SmartHomeControllerComponent.get_component(component_name)
        if isinstance(comp, SmartHomeControllerComponent):
            platform = comp.get_platform(platform_name)
            if platform is None:
                return
        else:
            _LOGGER.exception(
                f"Unexpected error importing {component_name}/{platform_name}",
            )
            return

        try:
            await integration_platform.process_platform(component_name, platform)
        except Exception:  # pylint: disable=broad-except
            _LOGGER.exception(
                f"Error processing platform {component_name}.{platform_name}"
            )

    async def async_process_integration_platform_for_component(
        self, component_name: str
    ) -> None:
        """Process integration platforms on demand for a component.

        This function will load the integration platforms
        for an integration instead of waiting for the EVENT_COMPONENT_LOADED
        event to be fired for the integration.

        When the integration will create entities before
        it has finished setting up; call this function to ensure
        that the integration platforms are loaded before the entities
        are created.
        """
        if self._integration_platforms is None:
            # There are no integration platforms loaded yet
            return
        await asyncio.gather(
            *[
                self._async_process_single_integration_platform_component(
                    component_name, integration_platform
                )
                for integration_platform in self._integration_platforms
            ]
        )

    async def _async_component_loaded(self, event: Event) -> None:
        """Handle a new component loaded."""
        comp = event.data[Const.ATTR_COMPONENT]
        if "." not in comp:
            await self.async_process_integration_platform_for_component(comp)

    async def async_process_integration_platforms(
        self,
        platform_name: Platform | str,
        process_platform: typing.Callable[
            [str, PlatformImplementation], typing.Awaitable[None]
        ],
    ) -> None:
        """Process a specific platform for all current and future loaded integrations."""
        if self._integration_platforms is None:
            self._integration_platforms = []

            self._shc.bus.async_listen(
                Const.EVENT_COMPONENT_LOADED, self._async_component_loaded
            )

        integration_platform = IntegrationPlatform(
            platform_name, process_platform, set()
        )
        self._integration_platforms.append(integration_platform)
        if top_level_components := (
            comp for comp in self._shc.config.components if "." not in comp
        ):
            await asyncio.gather(
                *[
                    self._async_process_single_integration_platform_component(
                        comp, integration_platform
                    )
                    for comp in top_level_components
                ]
            )

    async def async_reload_integration_platforms(
        self, integration_name: str, integration_platforms: typing.Iterable[str]
    ) -> None:
        """Reload an integration's platforms.

        The platform must support being re-setup.

        This functionality is only intended to be used for integrations that process
        Home Assistant data and make this available to other integrations.

        Examples are template, stats, derivative, utility meter.
        """
        try:
            unprocessed_conf = await self.async_shc_config_yaml()
        except SmartHomeControllerError as err:
            _LOGGER.error(err)
            return

        tasks = [
            self._resetup_platform(
                integration_name, integration_platform, unprocessed_conf
            )
            for integration_platform in integration_platforms
        ]

        await asyncio.gather(*tasks)

    async def _resetup_platform(
        self,
        integration_name: str,
        integration_platform: str,
        unprocessed_conf: ConfigType,
    ) -> None:
        """Resetup a platform."""
        integration = await self.async_get_integration(integration_platform)

        conf = await self.async_process_component_config(unprocessed_conf, integration)

        if not conf:
            return

        root_config: dict[str, list[ConfigType]] = {integration_platform: []}
        # Extract only the config for template, ignore the rest.
        for p_type, p_config in self.config_per_platform(conf, integration_platform):
            if p_type != integration_name:
                continue

            root_config[integration_platform].append(p_config)

        component = integration.get_component()
        shc_comp = SmartHomeControllerComponent.get_component(integration_platform)
        if shc_comp is not None:
            platform_reset_supported = shc_comp.supports_platform_reset
        else:
            platform_reset_supported = hasattr(component, "async_reset_platform")
        if platform_reset_supported:
            # If the integration has its own way to reset
            # use this method.
            async with self._reset_locks.setdefault(
                integration_platform, asyncio.Lock()
            ):
                if shc_comp is not None:
                    await shc_comp.async_reset_platform(integration_name)
                    await shc_comp.async_setup(root_config)
                else:
                    await component.async_reset_platform(self._shc, integration_name)
                    await component.async_setup(self._shc, root_config)
            return

        # If it's an entity platform, we use the entity_platform
        # async_reset method
        platform = self._async_get_platform_without_config_entry(
            integration_name, integration_platform
        )
        if platform:
            await self._async_reconfig_platform(
                platform, root_config[integration_platform]
            )
            return

        if not root_config[integration_platform]:
            # No config for this platform
            # and it's not loaded. Nothing to do.
            return

        await self._async_setup_platform(
            integration_name, integration_platform, root_config[integration_platform]
        )

    @callback
    def _async_get_platform_without_config_entry(
        self, integration_name: str, integration_platform_name: str
    ) -> EntityPlatform:
        """Find an existing platform that is not a config entry."""
        for integration_platform in EntityPlatform.async_get_platforms(
            self._shc, integration_name
        ):
            if integration_platform.config_entry is not None:
                continue
            if integration_platform.domain == integration_platform_name:
                platform: EntityPlatform = integration_platform
                return platform
        return None

    async def _async_reconfig_platform(
        self, platform: EntityPlatform, platform_configs: list[dict[str, typing.Any]]
    ) -> None:
        """Reconfigure an already loaded platform."""
        await platform.async_reset()
        tasks = [platform.async_setup(p_config) for p_config in platform_configs]
        await asyncio.gather(*tasks)

    async def _async_setup_platform(
        self,
        integration_name: str,
        integration_platform: str,
        platform_configs: list[dict[str, typing.Any]],
    ) -> None:
        """Platform for the first time when new configuration is added."""
        shc_comp = SmartHomeControllerComponent.get_component(integration_platform)
        if shc_comp is None or shc_comp.entity_component is None:
            if integration_platform not in self._shc.data:
                await self.async_setup_component(
                    integration_platform, {integration_platform: platform_configs}
                )
                return

            entity_component: EntityComponent = self._shc.data.get(integration_platform)
        else:
            entity_component = shc_comp.entity_component

        if entity_component is not None:
            tasks = [
                entity_component.async_setup_platform(integration_name, p_config)
                for p_config in platform_configs
            ]
            await asyncio.gather(*tasks)

    @callback
    def async_listen(
        self,
        service: str,
        callback_func: collections.abc.Callable[
            [str, DiscoveryInfoType], collections.abc.Awaitable[None]
        ],
    ) -> None:
        """Set up listener for discovery of specific service.

        Service can be a string or a list/tuple.
        """
        job = SmartHomeControllerJob(callback_func)

        async def discovery_event_listener(discovered: DiscoveryDict) -> None:
            """Listen for discovery events."""
            task = self._shc.async_run_shc_job(
                job, discovered[Const.ATTR_SERVICE], discovered[_ATTR_DISCOVERED]
            )
            if task:
                await task

        self._shc.dispatcher.async_connect(
            _SIGNAL_PLATFORM_DISCOVERED.format(service), discovery_event_listener
        )

    def discover(
        self,
        service: str,
        discovered: DiscoveryInfoType,
        component: str,
        config: ConfigType,
    ) -> None:
        """Fire discovery event. Can ensure a component is loaded."""
        self._shc.add_job(self.async_discover(service, discovered, component, config))

    async def async_discover(
        self,
        service: str,
        discovered: DiscoveryInfoType,
        component: str,
        config: ConfigType,
    ) -> None:
        """Fire discovery event. Can ensure a component is loaded."""
        if component is not None and component not in self._shc.config.components:
            await self._shc.setup.async_setup_component(component, config)

        data: DiscoveryDict = {
            Const.ATTR_SERVICE: service,
            _ATTR_PLATFORM: None,
            _ATTR_DISCOVERED: discovered,
        }

        self._shc.dispatcher.async_send(
            _SIGNAL_PLATFORM_DISCOVERED.format(service), data
        )

    def async_listen_platform(
        self,
        component: str,
        callback_func: collections.abc.Callable[
            [str, dict[str, typing.Any]], typing.Any
        ],
    ) -> collections.abc.Callable[[], None]:
        """Register a platform loader listener.

        This method must be run in the event loop.
        """
        service = _EVENT_LOAD_PLATFORM.format(component)
        job = SmartHomeControllerJob(callback_func)

        async def discovery_platform_listener(discovered: DiscoveryDict) -> None:
            """Listen for platform discovery events."""
            if not (platform := discovered[_ATTR_PLATFORM]):
                return

            task = self._shc.async_run_shc_job(
                job, platform, discovered.get(_ATTR_DISCOVERED)
            )
            if task:
                await task

        return self._shc.dispatcher.async_connect(
            _SIGNAL_PLATFORM_DISCOVERED.format(service), discovery_platform_listener
        )

    def load_platform(
        self,
        component: Platform | str,
        platform: str,
        discovered: DiscoveryInfoType,
        config: ConfigType,
    ) -> None:
        """Load a component and platform dynamically."""
        self._shc.add_job(
            self.async_load_platform(component, platform, discovered, config)
        )

    async def async_load_platform(
        self,
        component: Platform | str,
        platform: str,
        discovered: DiscoveryInfoType,
        config: ConfigType,
    ) -> None:
        """Load a component and platform dynamically.

        Use `async_listen_platform` to register a callback for these events.

        Warning: Do not await this inside a setup method to avoid a dead lock.
        Use `hass.async_create_task(async_load_platform(..))` instead.
        """
        assert config is not None, "You need to pass in the real hass config"

        setup_success = True
        component = str(component)
        if component not in self._shc.config.components:
            setup_success = await self.async_setup_component(component, config)

        # No need to send signal if we could not set up component
        if not setup_success:
            return

        service = _EVENT_LOAD_PLATFORM.format(component)

        data: DiscoveryDict = {
            Const.ATTR_SERVICE: service,
            _ATTR_PLATFORM: platform,
            _ATTR_DISCOVERED: discovered,
        }

        self._shc.dispatcher.async_send(
            _SIGNAL_PLATFORM_DISCOVERED.format(service), data
        )


def _no_duplicate_auth_provider(
    configs: collections.abc.Sequence[dict[str, typing.Any]]
) -> collections.abc.Sequence[dict[str, typing.Any]]:
    """No duplicate auth provider config allowed in a list.

    Each type of auth provider can only have one config without optional id.
    Unique id is required if same type of auth provider used multiple times.
    """
    config_keys: set[tuple[str, str]] = set()
    for config in configs:
        key = (config[Const.CONF_TYPE], config.get(Const.CONF_ID))
        if key in config_keys:
            raise vol.Invalid(
                f"Duplicate auth provider {config[Const.CONF_TYPE]} found. "
                + "Please add unique IDs "
                + "if you want to have the same auth provider twice"
            )
        config_keys.add(key)
    return configs


def _no_duplicate_auth_mfa_module(
    configs: collections.abc.Sequence[dict[str, typing.Any]]
) -> collections.abc.Sequence[dict[str, typing.Any]]:
    """No duplicate auth mfa module item allowed in a list.

    Each type of mfa module can only have one config without optional id.
    A global unique id is required if same type of mfa module used multiple
    times.
    Note: this is different than auth provider
    """
    config_keys: set[str] = set()
    for config in configs:
        key = config.get(Const.CONF_ID, config[Const.CONF_TYPE])
        if key in config_keys:
            raise vol.Invalid(
                f"Duplicate mfa module {config[Const.CONF_TYPE]} found. "
                + "Please add unique IDs "
                + "if you want to have the same mfa module twice"
            )
        config_keys.add(key)
    return configs


def _filter_bad_internal_external_urls(conf: dict) -> dict:
    """Filter internal/external URL with a path."""
    for key in Const.CONF_INTERNAL_URL, Const.CONF_EXTERNAL_URL:
        if key in conf and url.parse_url(conf[key]).path not in ("", "/"):
            # We warn but do not fix, because if this was incorrectly configured,
            # adjusting this value might impact security.
            _LOGGER.warning(
                f"Invalid {key} set. It's not allowed to have a path (/bla)"
            )

    return conf


_PACKAGES_CONFIG_SCHEMA: typing.Final = (
    cv.schema_with_slug_keys(  # Package names are slugs
        vol.Schema({cv.string: vol.Any(dict, list, None)})  # Component config
    )
)

_CUSTOMIZE_DICT_SCHEMA: typing.Final = vol.Schema(
    {
        vol.Optional(Const.ATTR_FRIENDLY_NAME): cv.string,
        vol.Optional(Const.ATTR_HIDDEN): cv.boolean,
        vol.Optional(Const.ATTR_ASSUMED_STATE): cv.boolean,
    },
    extra=vol.ALLOW_EXTRA,
)

_CUSTOMIZE_CONFIG_SCHEMA = vol.Schema(
    {
        vol.Optional(Const.CONF_CUSTOMIZE, default={}): vol.Schema(
            {cv.entity_id: _CUSTOMIZE_DICT_SCHEMA}
        ),
        vol.Optional(Const.CONF_CUSTOMIZE_DOMAIN, default={}): vol.Schema(
            {cv.string: _CUSTOMIZE_DICT_SCHEMA}
        ),
        vol.Optional(Const.CONF_CUSTOMIZE_GLOB, default={}): vol.Schema(
            {cv.string: _CUSTOMIZE_DICT_SCHEMA}
        ),
    }
)

_CORE_CONFIG_SCHEMA: typing.Final = vol.All(
    _CUSTOMIZE_CONFIG_SCHEMA.extend(
        {
            Const.CONF_NAME: vol.Coerce(str),
            Const.CONF_LATITUDE: cv.latitude,
            Const.CONF_LONGITUDE: cv.longitude,
            Const.CONF_ELEVATION: vol.Coerce(int),
            vol.Optional(Const.CONF_TEMPERATURE_UNIT): cv.temperature_unit,
            Const.CONF_UNIT_SYSTEM: cv.unit_system,
            Const.CONF_TIME_ZONE: cv.time_zone,
            vol.Optional(Const.CONF_INTERNAL_URL): cv.url,
            vol.Optional(Const.CONF_EXTERNAL_URL): cv.url,
            vol.Optional(Const.CONF_ALLOWLIST_EXTERNAL_DIRS): vol.All(
                cv.ensure_list, [vol.IsDir()]  # pylint: disable=no-value-for-parameter
            ),
            vol.Optional(Const.LEGACY_CONF_WHITELIST_EXTERNAL_DIRS): vol.All(
                cv.ensure_list, [vol.IsDir()]  # pylint: disable=no-value-for-parameter
            ),
            vol.Optional(Const.CONF_ALLOWLIST_EXTERNAL_URLS): vol.All(
                cv.ensure_list, [cv.url]
            ),
            vol.Optional(Const.CONF_PACKAGES, default={}): _PACKAGES_CONFIG_SCHEMA,
            vol.Optional(Const.CONF_AUTH_PROVIDERS): vol.All(
                cv.ensure_list,
                [
                    AuthProvider.AUTH_PROVIDER_SCHEMA.extend(
                        {
                            Const.CONF_TYPE: vol.NotIn(
                                ["insecure_example"],
                                "The insecure_example auth provider"
                                + " is for testing only.",
                            )
                        }
                    )
                ],
                _no_duplicate_auth_provider,
            ),
            vol.Optional(Const.CONF_AUTH_MFA_MODULES): vol.All(
                cv.ensure_list,
                [
                    MultiFactorAuthModule.MODULE_SCHEMA.extend(
                        {
                            Const.CONF_TYPE: vol.NotIn(
                                ["insecure_example"],
                                "The insecure_example mfa module is for testing only.",
                            )
                        }
                    )
                ],
                _no_duplicate_auth_mfa_module,
            ),
            # pylint: disable=no-value-for-parameter
            vol.Optional(Const.CONF_MEDIA_DIRS): cv.schema_with_slug_keys(vol.IsDir()),
            vol.Optional(Const.CONF_LEGACY_TEMPLATES): cv.boolean,
            vol.Optional(Const.CONF_CURRENCY): cv.currency,
        }
    ),
    _filter_bad_internal_external_urls,
)


def _write_default_config(config_dir: str) -> bool:
    """Write the default config."""
    config_path = os.path.join(config_dir, _YAML_CONFIG_FILE)
    secret_path = os.path.join(config_dir, Const.SECRET_YAML)
    version_path = os.path.join(config_dir, _VERSION_FILE)
    automation_yaml_path = os.path.join(config_dir, _AUTOMATION_CONFIG_PATH)
    script_yaml_path = os.path.join(config_dir, _SCRIPT_CONFIG_PATH)
    scene_yaml_path = os.path.join(config_dir, _SCENE_CONFIG_PATH)
    media_dir_path = os.path.join(config_dir, "media")

    # Writing files with YAML does not create the most human readable results
    # So we're hard coding a YAML template.
    try:
        with open(config_path, "wt", encoding="utf8") as config_file:
            config_file.write(_DEFAULT_CONFIG)

        if not os.path.isfile(secret_path):
            with open(secret_path, "wt", encoding="utf8") as secret_file:
                secret_file.write(_DEFAULT_SECRETS)

        with open(version_path, "wt", encoding="utf8") as version_file:
            version_file.write(Const.__version__)

        if not os.path.isfile(automation_yaml_path):
            with open(automation_yaml_path, "wt", encoding="utf8") as automation_file:
                automation_file.write("[]")

        if not os.path.isfile(script_yaml_path):
            with open(script_yaml_path, "wt", encoding="utf8"):
                pass

        if not os.path.isfile(scene_yaml_path):
            with open(scene_yaml_path, "wt", encoding="utf8"):
                pass

        if not os.path.isdir(media_dir_path):
            os.mkdir(media_dir_path)
        return True

    except OSError:
        print("Unable to create default configuration file", config_path)
        return False


@callback
def _format_config_error(
    ex: Exception, domain: str, config: dict, link: str = None
) -> tuple[str, bool]:
    """Generate log exception for configuration validation.

    This method must be run in the event loop.
    """
    is_friendly = False
    message = f"Invalid config for [{domain}]: "
    if isinstance(ex, vol.Invalid):
        if "extra keys not allowed" in ex.error_message:
            path = "->".join(str(m) for m in ex.path)
            message += (
                f"[{ex.path[-1]}] is an invalid option for [{domain}]. "
                f"Check: {domain}->{path}."
            )
        else:
            message += f"{vh.humanize_error(config, ex)}."
        is_friendly = True
    else:
        message += str(ex) or repr(ex)

    try:
        domain_config = config.get(domain, config)
    except AttributeError:
        domain_config = config

    message += (
        f" (See {getattr(domain_config, '__config_file__', '?')}, "
        f"line {getattr(domain_config, '__line__', '?')}). "
    )

    if domain != Const.CORE_COMPONENT_NAME and link:
        message += f"Please check the docs at {link}"

    return message, is_friendly


def _identify_config_schema(module: types.ModuleType) -> str:
    """Extract the schema and identify list or dict based."""
    if not isinstance(module.CONFIG_SCHEMA, vol.Schema):
        return None

    schema = module.CONFIG_SCHEMA.schema

    if isinstance(schema, vol.All):
        for subschema in schema.validators:
            if isinstance(subschema, dict):
                schema = subschema
                break
        else:
            return None

    try:
        key = next(k for k in schema if k == module.DOMAIN)
    except (TypeError, AttributeError, StopIteration):
        return None
    except Exception:  # pylint: disable=broad-except
        _LOGGER.exception("Unexpected error identifying config schema")
        return None

    if hasattr(key, "default") and not isinstance(
        key.default, vol.schema_builder.Undefined
    ):
        default_value = module.CONFIG_SCHEMA({module.DOMAIN: key.default()})[
            module.DOMAIN
        ]

        if isinstance(default_value, dict):
            return "dict"

        if isinstance(default_value, list):
            return "list"

        return None

    domain_schema = schema[key]

    t_schema = str(domain_schema)
    if t_schema.startswith("{") or "schema_with_slug_keys" in t_schema:
        return "dict"
    if t_schema.startswith(("[", "All(<function ensure_list")):
        return "list"
    return None


def _recursive_merge(
    conf: dict[str, typing.Any], package: dict[str, typing.Any]
) -> bool | str:
    """Merge package into conf, recursively."""
    error: bool | str = False
    for key, pack_conf in package.items():
        if isinstance(pack_conf, dict):
            if not pack_conf:
                continue
            conf[key] = conf.get(key, collections.OrderedDict())
            error = _recursive_merge(conf=conf[key], package=pack_conf)

        elif isinstance(pack_conf, list):
            conf[key] = cv.remove_falsy(
                cv.ensure_list(conf.get(key)) + cv.ensure_list(pack_conf)
            )

        else:
            if conf.get(key) is not None:
                return key
            conf[key] = pack_conf
    return error


def _resolve_integrations_from_root(
    shc: SmartHomeController, root_module: types.ModuleType, domains: list[str]
) -> dict[str, Integration]:
    """Resolve multiple integrations from root."""
    integrations: dict[str, Integration] = {}
    for domain in domains:
        try:
            integration = Integration.resolve_from_root(shc, root_module, domain)
        except Exception:  # pylint: disable=broad-except
            _LOGGER.exception(f"Error loading integration: {domain}")
        else:
            if integration:
                integrations[domain] = integration
    return integrations
