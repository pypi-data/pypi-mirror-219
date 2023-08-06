"""
PyScript Component for Smart Home - The Next Generation.

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


This component is based on the custom_component

Pyscript: Python Scripting for Home Assistant, Copyright (c) 2020-2022 Craig Barrat,
which may be freely used and copied according tho the terms of the Apache 2.0 License.

Original source code and documentation can be found under:
https://github.com/custom-components/pyscript
"""

import asyncio
import glob
import json
import logging
import os
import time
import traceback
import typing
from importlib.metadata import PackageNotFoundError
from importlib.metadata import version as installed_version

import voluptuous as vol
import watchdog.events
import watchdog.observers
from pkg_resources import Requirement

from ... import core
from .const import Const
from .events import Events
from .functions import Functions
from .global_context_mgr import GlobalContextMgr
from .jupyter_kernel import JupyterKernel
from .mqtt import MQTT
from .pyscript_config_flow import PyscriptConfigFlow
from .pyscript_options_config_flow import PyscriptOptionsConfigFlow
from .state_val import StateVal
from .states import States
from .trig_time import TrigTime
from .watchdog_handler import WatchdogHandler

_const: typing.TypeAlias = core.Const
_cv: typing.TypeAlias = core.ConfigValidation
_LOGGER: typing.Final = logging.getLogger(__name__)
_PYSCRIPT_SCHEMA: typing.Final = vol.Schema(
    {
        vol.Optional(Const.CONF_ALLOW_ALL_IMPORTS, default=False): _cv.boolean,
        vol.Optional(Const.CONF_SHC_IS_GLOBAL, default=False): _cv.boolean,
    },
    extra=vol.ALLOW_EXTRA,
)


# pylint: disable=unused-variable
class PyscriptComponent(
    core.SmartHomeControllerComponent, core.ConfigFlowPlatform, core.LogbookPlatform
):
    """Component to allow running Python scripts."""

    def __init__(self, path: typing.Iterable[str]):
        super().__init__(path)
        self._config_entry: core.ConfigEntry = None
        self._unsub_listeners: list[core.CallbackType] = []
        self._pyscript_folder: str = None
        self._old_config_data: dict = None
        self._global_context_mgr: GlobalContextMgr = None
        self._watchdog_observer: watchdog.observers.Observer = None
        self._watchdog_task: asyncio.Task = None
        self._events = Events(self)
        self._functions = Functions(self)
        self._mqtt = MQTT(self)
        self._states = States(self)
        self._time_triggers = TrigTime(self)
        self._supported_platforms = frozenset(
            [core.Platform.CONFIG_FLOW, core.Platform.LOGBOOK]
        )

    @property
    def config_data(self) -> typing.Mapping[str, typing.Any]:
        if not self._config_entry:
            return None
        return self._config_entry.data

    @property
    def config_schema(self) -> typing.Callable[[core.ConfigType], core.ConfigType]:
        return vol.Schema({self.domain: _PYSCRIPT_SCHEMA}, extra=vol.ALLOW_EXTRA)

    @property
    def events(self) -> Events:
        return self._events

    @property
    def functions(self) -> Functions:
        return self._functions

    @property
    def mqtt(self) -> MQTT:
        return self._mqtt

    @property
    def pyscript_folder(self) -> str:
        return self._pyscript_folder

    @property
    def states(self) -> States:
        return self._states

    @property
    def time_triggers(self):
        return self._time_triggers

    async def async_setup(self, config: core.ConfigType) -> bool:
        """Component setup, run import config flow for each entry in config."""
        if not await super().async_setup(config):
            return False

        await self._restore_state()
        if self._config:
            self.controller.async_create_task(
                self.controller.config_entries.flow.async_init(
                    self.domain,
                    context={"source": core.ConfigEntrySource.IMPORT},
                    data=self._config,
                )
            )

        return True

    async def async_setup_entry(self, entry: core.ConfigEntry) -> bool:
        """Initialize the pyscript config entry."""
        self._config_entry = entry
        controller = self.controller
        global_ctx_only = None
        doing_reload = False
        shc_is_global: bool = entry.data.get(Const.CONF_SHC_IS_GLOBAL, False)
        if self._global_context_mgr:
            #
            # reload yaml if this isn't the first time (ie, on reload)
            #
            doing_reload = True
            if await self._update_yaml_config():
                global_ctx_only = "*"
            # pylint: disable=protected-access
            self._global_context_mgr._shc_is_global = shc_is_global
        else:
            self._global_context_mgr = GlobalContextMgr(self, shc_is_global)

        self.states.register_functions()

        pyscript_folder = self._pyscript_folder = controller.config.path(Const.FOLDER)
        if not await controller.async_add_executor_job(os.path.isdir, pyscript_folder):
            _LOGGER.debug(
                f"Folder {Const.FOLDER} not found in configuration folder, creating it"
            )
            await controller.async_add_executor_job(os.makedirs, pyscript_folder)

        await self._install_requirements()
        await self._global_context_mgr.load_scripts(global_ctx_only=global_ctx_only)

        controller.services.async_register(
            self.domain, _const.SERVICE_RELOAD, self._reload_scripts_handler
        )

        controller.services.async_register(
            self.domain, Const.SERVICE_JUPYTER_KERNEL_START, self._jupyter_kernel_start
        )

        # Store callbacks to event listeners so we can unsubscribe on unload
        self._unsub_listeners.append(
            controller.bus.async_listen(
                _const.EVENT_SHC_STARTED, self._controller_started
            )
        )
        self._unsub_listeners.append(
            controller.bus.async_listen_once(
                _const.EVENT_SHC_STOP, self._controller_stopped
            )
        )

        await self._watchdog_start()

        if doing_reload:
            self._global_context_mgr.start_global_contexts(global_ctx_only="*")

        return True

    async def async_unload_entry(self, entry: core.ConfigEntry) -> bool:
        """Unload a config entry."""

        if entry != self._config_entry:
            return False

        _LOGGER.info("Unloading all scripts")
        await self._global_context_mgr.unload_scripts()

        for unsub_listener in self._unsub_listeners:
            unsub_listener()
        self._unsub_listeners = []

        return True

    async def _restore_state(self) -> None:
        """Restores the persisted pyscript state."""
        restore_data = await core.RestoreStateData.async_get_instance(self.controller)
        for entity_id, value in restore_data.last_states.items():
            if entity_id.startswith(f"{self.domain}."):
                last_state = value.state
                self.controller.states.async_set(
                    entity_id, last_state.state, last_state.attributes
                )

    async def _reload_scripts_handler(self, call: core.ServiceCall = None) -> None:
        """Handle reload service calls."""
        _LOGGER.debug("reload: yaml, reloading scripts, and restarting")

        global_ctx_only = call.data.get("global_ctx", None) if call else None

        if await self._update_yaml_config():
            global_ctx_only = "*"

        await self.states.get_service_params()

        await self._install_requirements()
        await self._global_context_mgr.load_scripts(global_ctx_only=global_ctx_only)

        self._global_context_mgr.start_global_contexts(global_ctx_only=global_ctx_only)

    async def _jupyter_kernel_start(self, call: core.ServiceCall) -> None:
        """Handle Jupyter kernel start call."""
        _LOGGER.debug(f"service call to jupyter_kernel_start: {call.data}")

        controller = self.controller
        global_ctx = self._global_context_mgr.create_context(
            "jupyter_", generate_unique_name=True, autostart=True
        )

        ast_ctx = global_ctx.create_ast_context()
        kernel = JupyterKernel(self, call.data, ast_ctx)
        await kernel.session_start()
        controller.states.async_set(
            call.data["state_var"], json.dumps(kernel.get_ports())
        )

        def state_var_remove():
            controller.states.async_remove(call.data["state_var"])

        kernel.set_session_cleanup_callback(state_var_remove)

    async def _state_changed(self, event: core.Event) -> None:
        var_name = event.data["entity_id"]
        if event.data.get("new_state", None):
            new_val = StateVal(event.data["new_state"])
        else:
            # state variable has been deleted
            new_val = None

        if event.data.get("old_state", None):
            old_val = StateVal(event.data["old_state"])
        else:
            # no previous state
            old_val = None

        new_vars = {var_name: new_val, f"{var_name}.old": old_val}
        func_args = {
            "trigger_type": "state",
            "var_name": var_name,
            "value": new_val,
            "old_value": old_val,
            "context": event.context,
        }
        await self.states.update(new_vars, func_args)

    async def _controller_started(self, _event: core.Event) -> None:
        _LOGGER.debug("adding state changed listener and starting global contexts")
        controller = self.controller
        await self.states.get_service_params()
        self._unsub_listeners.append(
            controller.bus.async_listen(_const.EVENT_STATE_CHANGED, self._state_changed)
        )
        self._global_context_mgr.start_global_contexts()
        if self._watchdog_observer:
            observer = self._watchdog_observer
            observer.start()

    async def _controller_stopped(self, _event: core.Event) -> None:
        if self._watchdog_observer:
            observer = self._watchdog_observer
            observer.stop()
            observer.join()
            self._watchdog_observer = None
            self.functions.reaper_cancel(self._watchdog_task)
            self._watchdog_task = None

        _LOGGER.debug("stopping global contexts")
        await self._global_context_mgr.unload_scripts(unload_all=True)
        # sync with waiter, and then tell waiter and reaper tasks to exit
        await self.functions.waiter_sync()
        await self.functions.waiter_stop()
        await self.functions.reaper_stop()

    async def _update_yaml_config(
        self,
    ) -> bool:
        """Update the yaml config."""
        try:
            conf = await self.controller.setup.async_shc_config_yaml()
        except core.SmartHomeControllerError as err:
            _LOGGER.error(err)
            return

        config = _PYSCRIPT_SCHEMA(conf.get(self.domain, {}))

        #
        # If data in config doesn't match config entry, trigger a config import
        # so that the config entry can get updated
        #
        if config != self._config_entry.data:
            await self.controller.config_entries.flow.async_init(
                self.domain,
                context={"source": core.ConfigEntrySource.IMPORT},
                data=config,
            )

        #
        # if hass_is_global or allow_all_imports have changed, we need to reload all scripts
        # since they affect all scripts
        #
        config_save = {
            param: self._config_entry.data.get(param, False)
            for param in Const.CONF_BOOL_ALL
        }
        if self._old_config_data:
            old_config = self._old_config_data
            self._old_config_data = config_save
            for param in Const.CONF_BOOL_ALL:
                if old_config.get(param, False) != self._config_entry.data.get(
                    param, False
                ):
                    return True
        self._old_config_data = config_save
        return False

    async def _watchdog_start(
        self,
    ) -> None:
        """Start watchdog thread to look for changed files in pyscript_folder."""
        if self._watchdog_observer:
            return

        watchdog_q = asyncio.Queue(0)
        observer = self._watchdog_observer = watchdog.observers.Observer()
        if observer is not None:
            # don't run watchdog when we are testing (Observer() patches to None)
            self._watchdog_observer = observer
            self._watchdog_task = self.functions.create_task(
                self._watchdog_loop(watchdog_q)
            )

            observer.schedule(
                WatchdogHandler(self.controller, watchdog_q),
                self._pyscript_folder,
                recursive=True,
            )

    async def _watchdog_loop(
        self,
        watchdog_q: asyncio.Queue,
    ) -> None:
        while True:
            try:
                #
                # since some file/dir changes create multiple events, we consume all
                # events in a small window; first # wait indefinitely for next event
                #
                do_reload = self._check_watchdog_event(await watchdog_q.get(), False)
                #
                # now consume all additional events with 50ms timeout or 500ms elapsed
                #
                t_start = time.monotonic()
                while time.monotonic() - t_start < 0.5:
                    try:
                        do_reload = self._check_watchdog_event(
                            await asyncio.wait_for(watchdog_q.get(), timeout=0.05),
                            do_reload,
                        )
                    except asyncio.TimeoutError:
                        break
                if do_reload:
                    await self._reload_scripts_handler()

            # pylint: disable=try-except-raise
            except asyncio.CancelledError:
                raise
            except Exception:  # pylint: disable=broad-except
                _LOGGER.error(
                    f"task_watchdog: got exception {traceback.format_exc(-1)}"
                )

    @staticmethod
    def _check_watchdog_event(
        event: watchdog.events.FileSystemEvent, do_reload: bool
    ) -> bool:
        """Check if event should trigger a reload."""
        if event.is_directory:
            # don't reload if it's just a directory modified
            if isinstance(event, watchdog.events.DirModifiedEvent):
                return do_reload
            return True
        # only reload if it's a script, yaml, or requirements.txt file
        for valid_suffix in [".py", ".yaml", "/" + Const.REQUIREMENTS_FILE]:
            if event.src_path.endswith(valid_suffix):
                return True
        return do_reload

    async def _install_requirements(self):
        """Install missing requirements from requirements.txt."""

        pyscript_installed_packages: dict = self._config_entry.data.get(
            Const.CONF_INSTALLED_PACKAGES, {}
        ).copy()

        # Import packaging inside install_requirements so that we can use Home Assistant
        # to install it if it can't been found
        # pylint: disable=import-outside-toplevel
        try:
            from packaging.version import Version
        except ModuleNotFoundError:
            await self.controller.setup.async_process_requirements(
                self.domain, ["packaging"]
            )
            from packaging.version import Version

        all_requirements = await self.controller.async_add_executor_job(
            self._process_all_requirements
        )

        requirements_to_install = {}

        if all_requirements and not self._config_entry.data.get(
            Const.CONF_ALLOW_ALL_IMPORTS, False
        ):
            _LOGGER.error(
                "Requirements detected but 'allow_all_imports' is set to False, set "
                + "'allow_all_imports' to True if you want packages to be installed"
            )
            return

        for package in all_requirements:
            pkg_installed_version = all_requirements[package].get(
                Const.ATTR_INSTALLED_VERSION
            )
            version_to_install = all_requirements[package][Const.ATTR_VERSION]
            sources = all_requirements[package][Const.ATTR_SOURCES]
            # If package is already installed, we need to run some checks
            if pkg_installed_version:
                # If the version to install is unpinned and there is already something installed,
                # defer to what is installed
                if version_to_install == Const.UNPINNED_VERSION:
                    _LOGGER.debug(
                        f"Skipping unpinned version of package '{package}' because version "
                        + f"'{pkg_installed_version}' is already installed"
                    )
                    # If installed package is not the same version as the one we last installed,
                    # that means that the package is externally managed now so we shouldn't touch it
                    # and should remove it from our internal tracker
                    if (
                        package in pyscript_installed_packages
                        and pyscript_installed_packages[package]
                        != pkg_installed_version
                    ):
                        pyscript_installed_packages.pop(package)
                    continue

                # If installed package is not the same version as the one we last installed,
                # that means that the package is externally managed now so we shouldn't touch it
                # and should remove it from our internal tracker
                if package in pyscript_installed_packages and Version(
                    pyscript_installed_packages[package]
                ) != Version(pkg_installed_version):
                    _LOGGER.warning(
                        f"Version '{version_to_install}' for package '{package}' detected in "
                        + f"'{str(sources)}' will be ignored in favor of "
                        + f"the version '{pkg_installed_version}' which was installed outside "
                        + "of pyscript"
                    )
                    pyscript_installed_packages.pop(package)
                # If there is a version mismatch between what we want and what is installed, we
                # can overwrite it since we know it was last installed by us
                elif package in pyscript_installed_packages and Version(
                    version_to_install
                ) != Version(pkg_installed_version):
                    requirements_to_install[package] = all_requirements[package]
                # If there is an installed version that we have not previously installed, we
                # should not install it
                else:
                    _LOGGER.debug(
                        f"Version '{version_to_install}' for package '{package}' detected in "
                        + f"'{str(sources)}' will be ignored because it  is already installed"
                    )
            # Anything not already installed in the environment can be installed
            else:
                requirements_to_install[package] = all_requirements[package]

        if requirements_to_install:
            _LOGGER.info(
                f"Installing the following packages: {str(requirements_to_install)}",
            )
            await self.controller.setup.async_process_requirements(
                self.domain,
                [
                    f"{package}=={requirements_to_install[package][Const.ATTR_VERSION]}"
                    if requirements_to_install[package][Const.ATTR_VERSION]
                    != Const.UNPINNED_VERSION
                    else package
                    for package in requirements_to_install.items()
                ],
            )
        else:
            _LOGGER.debug("No new packages to install")

        # Update package tracker in config entry for next time
        pyscript_installed_packages.update(
            {
                package: requirements_to_install[package][Const.ATTR_VERSION]
                for package in requirements_to_install.items()
            }
        )

        # If any requirements were unpinned, get their version now so they can be pinned later
        if any(
            version == Const.UNPINNED_VERSION
            for version in pyscript_installed_packages.values()
        ):
            pyscript_installed_packages = await self.controller.async_add_executor_job(
                _update_unpinned_versions, pyscript_installed_packages
            )
        if pyscript_installed_packages != self._config_entry.data.get(
            Const.CONF_INSTALLED_PACKAGES, {}
        ):
            new_data = self._config_entry.data.copy()
            new_data[Const.CONF_INSTALLED_PACKAGES] = pyscript_installed_packages
            self.controller.config_entries.async_update_entry(
                entry=self._config_entry, data=new_data
            )

    def _process_all_requirements(self):
        """
        Load all lines from requirements_file located in requirements_paths.

        Returns files and a list of packages, if any, that need to be installed.
        """

        # Re-import Version to avoid dealing with multiple flake and pylint errors
        from packaging.version import Version  # pylint: disable=import-outside-toplevel

        requirements_paths = Const.REQUIREMENTS_PATHS
        requirements_file = Const.REQUIREMENTS_FILE
        all_requirements_to_process = {}
        for root in requirements_paths:
            for requirements_path in glob.glob(
                os.path.join(self._pyscript_folder, root, requirements_file)
            ):
                with open(requirements_path, encoding="utf-8") as requirements_fp:
                    all_requirements_to_process[
                        requirements_path
                    ] = requirements_fp.readlines()

        all_requirements_to_install = {}
        for requirements_path, pkg_lines in all_requirements_to_process.items():
            for pkg in pkg_lines:
                # Remove inline comments which are accepted by pip but not by Home
                # Assistant's installation method.
                # https://rosettacode.org/wiki/Strip_comments_from_a_string#Python
                i = pkg.find("#")
                if i >= 0:
                    pkg = pkg[:i]
                pkg = pkg.strip()

                if not pkg:
                    continue

                try:
                    # Attempt to get version of package. Do nothing if it's found since
                    # we want to use the version that's already installed to be safe
                    requirement = Requirement.parse(pkg)
                    pkg_name = requirement.project_name

                    # Requirements must be pinned and will be skipped if they aren't
                    if len(requirement.specs) == 1 and (
                        len(requirement.specs[0]) != 2
                        or requirement.specs[0][0] != "=="
                    ):
                        _LOGGER.error(
                            f"Ignoring invalid requirement '{requirements_path}' specified in "
                            + f"'{pkg}'; if a specific version is required, the requirement "
                            + "must use the format 'pkg==version'"
                        )
                        continue

                    if not requirement.specs:
                        new_version = Const.UNPINNED_VERSION
                    else:
                        new_version = requirement.specs[0][1]
                    current_pinned_version = all_requirements_to_install.get(
                        pkg_name, {}
                    ).get(Const.ATTR_VERSION)
                    current_sources = all_requirements_to_install.get(pkg_name, {}).get(
                        Const.ATTR_SOURCES, []
                    )
                    # If a version hasn't already been recorded, record this one
                    if not current_pinned_version:
                        all_requirements_to_install[pkg_name] = {
                            Const.ATTR_VERSION: new_version,
                            Const.ATTR_SOURCES: [requirements_path],
                            Const.ATTR_INSTALLED_VERSION: _get_installed_version(
                                pkg_name
                            ),
                        }

                    # If the new version is unpinned and there is an existing pinned version,
                    # use existing pinned version
                    elif (
                        new_version == Const.UNPINNED_VERSION
                        and current_pinned_version != Const.UNPINNED_VERSION
                    ):
                        _LOGGER.warning(
                            f"Unpinned requirement for package '{pkg_name}' detected in "
                            + f"'{requirements_path}' will be ignored in favor of the "
                            + f"pinned version '{current_pinned_version}' detected in "
                            + f"'{str(current_sources)}'"
                        )
                    # If the new version is pinned and the existing version is unpinned,
                    # use the new pinned version
                    elif (
                        new_version != Const.UNPINNED_VERSION
                        and current_pinned_version == Const.UNPINNED_VERSION
                    ):
                        _LOGGER.warning(
                            f"Unpinned requirement for package '{pkg_name}' detected in "
                            + f"'{str(current_sources)} will be ignored in favor of the "
                            + f"pinned version '{new_version}' detected in '{requirements_path}'"
                        )
                        all_requirements_to_install[pkg_name] = {
                            Const.ATTR_VERSION: new_version,
                            Const.ATTR_SOURCES: [requirements_path],
                            Const.ATTR_INSTALLED_VERSION: _get_installed_version(
                                pkg_name
                            ),
                        }
                    # If the already recorded version is the same as the new version,
                    # append the current path so we can show sources
                    elif (
                        new_version == Const.UNPINNED_VERSION
                        and current_pinned_version == Const.UNPINNED_VERSION
                    ) or Version(current_pinned_version) == Version(new_version):
                        all_requirements_to_install[pkg_name][
                            Const.ATTR_SOURCES
                        ].append(requirements_path)
                    # If the already recorded version is lower than the new version, use the new one
                    elif Version(current_pinned_version) < Version(new_version):
                        _LOGGER.warning(
                            f"Version '{current_pinned_version}' for package '{pkg_name}' "
                            + f"detected in '{str(current_sources)}' will be ignored in "
                            + f"favor of the higher version '{new_version}' detected in "
                            + f"'{requirements_path}'"
                        )
                        all_requirements_to_install[pkg_name].update(
                            {
                                Const.ATTR_VERSION: new_version,
                                Const.ATTR_SOURCES: [requirements_path],
                            }
                        )
                    # If the already recorded version is higher than the new version,
                    # ignore the new one
                    elif Version(current_pinned_version) > Version(new_version):
                        _LOGGER.warning(
                            f"Version '{new_version}' for package '{pkg_name}' detected in "
                            + f"'{requirements_path}' will be ignored in favor of the higher "
                            + f"version '{current_pinned_version}' detected in "
                            + f"'{str(current_sources)}'"
                        )
                except ValueError:
                    # Not valid requirements line so it can be skipped
                    _LOGGER.debug(f"Ignoring '{pkg}' because it is not a valid package")

        return all_requirements_to_install

    # ---------------------- ConfigFlow Platform ----------------------

    def create_config_flow(
        self, context: dict, init_data: typing.Any
    ) -> core.ConfigFlow:
        return PyscriptConfigFlow(self, context, init_data)

    async def async_get_options_flow(
        self, entry: core.ConfigEntry, context: dict, init_data: typing.Any
    ) -> core.OptionsFlow:
        return PyscriptOptionsConfigFlow(self, entry)

    # ----------------------- Logbook Platform ---------------------------

    def async_describe_events(self, async_describe_event: core.LogbookCallback) -> None:
        async_describe_event(Const.EVENT_PYSCRIPT_RUNNING)

    def async_describe_event(self, event: core.LazyPartialState) -> dict[str, str]:
        """Describe a logbook event."""
        data = event.data
        func_args = data.get("func_args", {})
        ev_name = data.get("name", "unknown")
        ev_entity_id = data.get("entity_id", "pyscript.unknown")

        ev_trigger_type = func_args.get("trigger_type", "unknown")
        if ev_trigger_type == "event":
            ev_source = f"event {func_args.get('event_type', 'unknown event')}"
        elif ev_trigger_type == "state":
            ev_source = (
                f"state change {func_args.get('var_name', 'unknown entity')} "
                + f"== {func_args.get('value', 'unknown value')}"
            )
        elif ev_trigger_type == "time":
            ev_trigger_time = func_args.get("trigger_time", "unknown")
            if ev_trigger_time is None:
                ev_trigger_time = "startup"
            ev_source = f"time {ev_trigger_time}"
        else:
            ev_source = ev_trigger_type

        message = f"has been triggered by {ev_source}"

        return {
            core.Const.LOGBOOK_ENTRY_NAME: ev_name,
            core.Const.LOGBOOK_ENTRY_MESSAGE: message,
            core.Const.LOGBOOK_ENTRY_SOURCE: ev_source,
            core.Const.LOGBOOK_ENTRY_ENTITY_ID: ev_entity_id,
        }


def _get_installed_version(pkg_name: str):
    """Get installed version of package. Returns None if not found."""
    try:
        return installed_version(pkg_name)
    except PackageNotFoundError:
        return None


def _update_unpinned_versions(package_dict):
    """Check for current installed version of each unpinned package."""
    requirements_to_pop = []
    for package in package_dict:
        if package_dict[package] != Const.UNPINNED_VERSION:
            continue

        package_dict[package] = _get_installed_version(package)
        if not package_dict[package]:
            _LOGGER.error(f"{package} wasn't able to be installed")
            requirements_to_pop.append(package)

    for package in requirements_to_pop:
        package_dict.pop(package)

    return package_dict
