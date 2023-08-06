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
import concurrent
import contextlib
import enum
import ipaddress
import logging
import os
import pathlib
import signal
import sys
import threading
import time
import typing
import uuid
import webbrowser

import yarl

from ..auth.auth_manager import AuthManager
from ..auth.providers.internal import InternalAuthProvider
from . import helpers
from .area_registry import AreaRegistry
from .callback import callback
from .components import Components
from .config import Config
from .config_entries import ConfigEntries
from .const import Const
from .core_state import CoreState
from .device_registry import DeviceRegistry
from .dispatcher import Dispatcher
from .entity_registry import EntityRegistry
from .event_bus import EventBus
from .event_tracker import EventTracker
from .flow_dispatcher import FlowDispatcher
from .intent_manager import IntentManager
from .no_url_available_error import NoURLAvailableError
from .runtime_config import RuntimeConfig
from .service_registry import ServiceRegistry
from .setup_manager import SetupManager
from .smart_home_controller import SmartHomeController
from .smart_home_controller_component import SmartHomeControllerComponent
from .smart_home_controller_error import SmartHomeControllerError
from .smart_home_controller_http import SmartHomeControllerHTTP
from .smart_home_controller_job import SmartHomeControllerJob
from .smart_home_controller_job_type import SmartHomeControllerJobType
from .smart_home_controller_view import SmartHomeControllerView
from .state_machine import StateMachine
from .store import Store
from .sun import Sun
from .timeout_manager import TimeoutManager
from .translations import Translations

_R = typing.TypeVar("_R")
_T = typing.TypeVar("_T")

_LOGGER: typing.Final = logging.getLogger(__name__)
# How long to wait to log tasks that are blocking
_BLOCK_LOG_TIMEOUT: typing.Final = 60
_STAGE_1_SHUTDOWN_TIMEOUT: typing.Final = 100
_STAGE_2_SHUTDOWN_TIMEOUT: typing.Final = 60
_STAGE_3_SHUTDOWN_TIMEOUT: typing.Final = 30
# How long to wait until things that run on startup have to finish.
_TIMEOUT_EVENT_START: typing.Final = 15


class _UrlType(enum.Enum):
    INTERNAL = enum.auto()
    EXTERNAL = enum.auto()
    SUPERVISOR = enum.auto()


# pylint: disable=unused-variable
class TheNextGeneration(SmartHomeController):
    """Root object of the home automation."""

    def __init__(self) -> None:
        """
        Initialize new The Next Generation Smart Home Controller object.
        """
        super().__init__()

        self._auth: AuthManager = None
        self._http: SmartHomeControllerHTTP = None

        self._loop = asyncio.get_running_loop()
        self._pending_tasks: list[asyncio.Future[typing.Any]] = []
        self._track_task = True
        self._bus = EventBus(self, self._loop)
        self._services = ServiceRegistry(self)
        self._states = StateMachine(self._bus, self._loop)
        self._config = Config(self)
        self._components = Components(self)
        # This is a dictionary that any component can store any data on.
        self._data: dict[str, typing.Any] = {}
        self._state: CoreState = CoreState.NOT_RUNNING
        self._exit_code: int = 0
        # If not None, use to signal end-of-loop
        self._stopped: asyncio.Event = None
        # Timeout handler for Core/Helper namespace
        self._timeout: TimeoutManager = TimeoutManager()
        self._entity_info: dict[str, dict[str, str]] = {}
        self._area_registry: AreaRegistry = None
        self._entity_registry: EntityRegistry = None
        self._config_entries: ConfigEntries = None
        self._device_registry: DeviceRegistry = None
        self._dispatcher = Dispatcher(self)
        self._setup = SetupManager(self)
        self._sun = Sun(self)
        self._tracker = EventTracker(self)
        self._flow_dispatcher = FlowDispatcher(self)
        self._flow_dispatcher.async_setup()
        self._instance_id: str | asyncio.Event = None
        self._translations = Translations(self)
        self._pending_view_registrations = list[
            SmartHomeControllerView | type[SmartHomeControllerView]
        ]()
        self._loop.set_debug(False)
        self._intent_manager: IntentManager = None

    async def async_get_instance_id(self) -> str:
        if self._instance_id is None:
            self._instance_id = event = asyncio.Event()

            store = Store(self, 1, "core.uuid", True)

            data: dict[str, str] = await self.async_migrator(
                self.config.path(".uuid"),
                store,
            )

            if data is not None:
                self._instance_id = data["uuid"]
                event.set()
            else:
                self._instance_id = uuid.uuid4().hex
                data = {"uuid": self._instance_id}
                await store.async_save(data)
                event.set()

        else:
            id_or_event = self._instance_id
            if isinstance(id_or_event, asyncio.Event):
                await id_or_event.wait()
        return self._instance_id

    @property
    def translations(self) -> Translations:
        return self._translations

    @property
    def data(self) -> dict[str, typing.Any]:
        return self._data

    @property
    def area_registry(self) -> AreaRegistry:
        if self._area_registry is None:
            self._area_registry = AreaRegistry(self)
        return self._area_registry

    @property
    def auth(self) -> AuthManager:
        return self._auth

    @auth.setter
    def auth(self, auth: AuthManager) -> None:
        # only possible on startup!
        if self._auth is None:
            self._auth = auth

    @property
    def bus(self) -> EventBus:
        return self._bus

    @property
    def components(self) -> Components:
        return self._components

    @property
    def config(self) -> Config:
        return self._config

    @property
    def config_entries(self) -> ConfigEntries:
        return self._config_entries

    @config_entries.setter
    def config_entries(self, entries: ConfigEntries) -> None:
        if self._config_entries is None:
            self._config_entries = entries

    @property
    def device_registry(self) -> DeviceRegistry:
        if self._device_registry is None:
            self._device_registry = DeviceRegistry(self)
        return self._device_registry

    @property
    def dispatcher(self) -> Dispatcher:
        return self._dispatcher

    @property
    def entity_registry(self) -> EntityRegistry:
        if self._entity_registry is None:
            self._entity_registry = EntityRegistry(self)
        return self._entity_registry

    @property
    def entity_sources(self) -> dict[str, dict[str, str]]:
        return self._entity_info

    @property
    def flow_dispatcher(self) -> FlowDispatcher:
        return self._flow_dispatcher

    @property
    def http(self) -> SmartHomeControllerHTTP:
        return self._http

    @property
    def intents(self) -> IntentManager:
        if self._intent_manager is None:
            self._intent_manager = IntentManager(self)
        return self._intent_manager

    @property
    def services(self) -> ServiceRegistry:
        return self._services

    @property
    def setup(self) -> SetupManager:
        return self._setup

    @property
    def state(self) -> CoreState:
        return self._state

    @property
    def states(self) -> StateMachine:
        return self._states

    @property
    def sun(self) -> Sun:
        return self._sun

    @property
    def tracker(self) -> EventTracker:
        return self._tracker

    @property
    def in_safe_mode(self) -> bool:
        """Return if the Smart Home Controller running in safe mode."""
        return self._config.safe_mode

    @property
    def is_running(self) -> bool:
        """Return if the Smart Home Controller is running."""
        return self._state in (CoreState.STARTING, CoreState.RUNNING)

    @property
    def is_stopping(self) -> bool:
        """Return if the Smart Home Controller is stopping."""
        return self._state in (CoreState.STOPPING, CoreState.FINAL_WRITE)

    @property
    def timeout(self) -> TimeoutManager:
        return self._timeout

    @callback
    def async_get_shc_auth_provider(self) -> InternalAuthProvider:
        """Get the provider."""
        if self._auth is not None:
            for prv in self.auth.auth_providers:
                if prv.type == "internal":
                    return typing.cast(InternalAuthProvider, prv)
        raise RuntimeError("Provider not found")

    def call_later(self, delay: float, func: typing.Any, *args) -> asyncio.TimerHandle:
        return self._loop.call_later(delay, func, *args)

    def call_soon_threadsafe(self, func: typing.Any, *args) -> None:
        self._loop.call_soon_threadsafe(func, *args)

    def run_in_executor(self, executor, func, *args):
        return self._loop.run_in_executor(executor, func, *args)

    def start(self) -> int:
        """Start the Smart Home Controller.

        Note: This function is only used for testing.
        For regular use, use "await hass.run()".
        """
        # Register the async start
        helpers.fire_coroutine_threadsafe(self.async_start(), self._loop)

        # Run forever
        # Block until stopped
        _LOGGER.info("Starting Smart Home Controller core loop")
        self._loop.run_forever()
        return self._exit_code

    async def async_run(self, *, attach_signals: bool = True) -> int:
        """Smart Home - The Next Generation main entry point.

        Start the Smart Home Controller and block until stopped.

        This method is a coroutine.
        """
        if self.state != CoreState.NOT_RUNNING:
            raise RuntimeError("Smart Home - The Next Generation is already running")

        # _async_stop will set this instead of stopping the loop
        self._stopped = asyncio.Event()

        await self.async_start()
        if attach_signals:
            self.async_register_signal_handling()

        await self._stopped.wait()
        return self._exit_code

    @callback
    def async_register_signal_handling(self) -> None:
        """Register system signal handler for core."""

        @callback
        def async_signal_handle(exit_code: int) -> None:
            """Wrap signal handling.

            * queue call to shutdown task
            * re-instate default handler
            """
            self._loop.remove_signal_handler(signal.SIGTERM)
            self._loop.remove_signal_handler(signal.SIGINT)
            self.async_create_task(self.async_stop(exit_code))

        try:
            self._loop.add_signal_handler(signal.SIGTERM, async_signal_handle, 0)
        except ValueError:
            _LOGGER.warning("Could not bind to SIGTERM")

        try:
            self._loop.add_signal_handler(signal.SIGINT, async_signal_handle, 0)
        except ValueError:
            _LOGGER.warning("Could not bind to SIGINT")

        try:
            self._loop.add_signal_handler(
                signal.SIGHUP, async_signal_handle, Const.RESTART_EXIT_CODE
            )
        except ValueError:
            _LOGGER.warning("Could not bind to SIGHUP")

    async def async_start(self) -> None:
        """Finalize startup from inside the event loop.

        This method is a coroutine.
        """
        _LOGGER.info("Starting Smart Home - The Next Generation")
        setattr(self._loop, "_thread_ident", threading.get_ident())

        self._state = CoreState.STARTING
        self.bus.async_fire(Const.EVENT_CORE_CONFIG_UPDATE)
        self.bus.async_fire(Const.EVENT_SHC_START)

        try:
            # Only block for EVENT_ASSISTANT_START listener
            self.async_stop_track_tasks()
            async with self._timeout.async_timeout(_TIMEOUT_EVENT_START):
                await self.async_block_till_done()
        except asyncio.TimeoutError:
            _LOGGER.warning(
                "Something is blocking Smart Home - The Next Generation from wrapping up the "
                + "start up phase. We're going to continue anyway. Please report the following "
                + "info at https://github.com/nixe64/The-Next-Generation/issues: "
                + f"{', '.join(self._config.components)}"
            )

        # Allow automations to set up the start triggers before changing state
        await asyncio.sleep(0)

        if self.state != CoreState.STARTING:
            _LOGGER.warning(
                "Smart Home - The Next Generation startup has been interrupted. "
                + "Its state may be inconsistent"
            )
            return

        self._state = CoreState.RUNNING
        self.bus.async_fire(Const.EVENT_CORE_CONFIG_UPDATE)
        self.bus.async_fire(Const.EVENT_SHC_STARTED)

    def add_job(
        self,
        target: collections.abc.Callable[..., typing.Any]
        | collections.abc.Coroutine[typing.Any, typing.Any, typing.Any],
        *args: typing.Any,
    ) -> None:
        """Add a job to be executed by the event loop or by an executor.

        If the job is either a coroutine or decorated with @callback, it will be
        run by the event loop, if not it will be run by an executor.

        target: target to call.
        args: parameters for method to call.
        """
        if target is None:
            raise ValueError("Don't call add_job with None")
        self._loop.call_soon_threadsafe(self.async_add_job, target, *args)

    @callback
    def async_add_job(
        self,
        target: collections.abc.Callable[
            ..., collections.abc.Coroutine[typing.Any, typing.Any, _R] | _R
        ]
        | collections.abc.Coroutine[typing.Any, typing.Any, _R],
        *args: typing.Any,
    ) -> asyncio.Future[_R]:
        """Add a job to be executed by the event loop or by an executor.

        If the job is either a coroutine or decorated with @callback, it will be
        run by the event loop, if not it will be run by an executor.

        This method must be run in the event loop.

        target: target to call.
        args: parameters for method to call.
        """
        if target is None:
            raise ValueError("Don't call async_add_job with None")

        if asyncio.iscoroutine(target):
            return self.async_create_task(target)

        # This code path is performance sensitive and uses
        # if TYPE_CHECKING to avoid the overhead of constructing
        # the type used for the cast. For history see:
        # https://github.com/home-assistant/core/pull/71960
        if typing.TYPE_CHECKING:
            target = typing.cast(
                collections.abc.Callable[
                    ...,
                    typing.Union[
                        collections.abc.Coroutine[typing.Any, typing.Any, _R], _R
                    ],
                ],
                target,
            )
        return self.async_add_shc_job(SmartHomeControllerJob(target), *args)

    @callback
    def async_add_shc_job(
        self,
        job: SmartHomeControllerJob[
            collections.abc.Coroutine[typing.Any, typing.Any, _R] | _R
        ],
        *args: typing.Any,
    ) -> asyncio.Future[_R]:
        """Add a SmartHomeControllerJob from within the event loop.

        This method must be run in the event loop.
        job: SmartHomeControllerJob to call.
        args: parameters for method to call.
        """
        task: asyncio.Future[_R] = None
        # This code path is performance sensitive and uses
        # if TYPE_CHECKING to avoid the overhead of constructing
        # the type used for the cast. For history see:
        # https://github.com/home-assistant/core/pull/71960
        if job.job_type == SmartHomeControllerJobType.COROUTINE_FUNCTION:
            task = self._loop.create_task(job.target(*args))
        elif job.job_type == SmartHomeControllerJobType.CALLBACK:
            self._loop.call_soon(job.target, *args)
            return None
        else:
            task = self._loop.run_in_executor(None, job.target, *args)

        # If a task is scheduled
        if self._track_task:
            self._pending_tasks.append(task)
        return task

    def create_task(
        self, target: collections.abc.Coroutine[typing.Any, typing.Any, typing.Any]
    ):
        """Add task to the executor pool.

        target: target to call.
        """
        return self._loop.call_soon_threadsafe(self.async_create_task, target)

    @callback
    def async_create_task(
        self,
        target: collections.abc.Coroutine[typing.Any, typing.Any, _R],
        never_track: bool = False,
    ) -> asyncio.Task[_R]:
        """Create a task from within the eventloop.

        This method must be run in the event loop.

        target: target to call.
        """
        task = self._loop.create_task(target)

        if self._track_task and not never_track:
            self._pending_tasks.append(task)

        return task

    @callback
    def async_add_executor_job(
        self, target: collections.abc.Callable[..., _T], *args: typing.Any
    ) -> asyncio.Future[_T]:
        """Add an executor job from within the event loop."""
        task = self._loop.run_in_executor(None, target, *args)

        # If a task is scheduled
        if self._track_task:
            self._pending_tasks.append(task)

        return task

    @callback
    def async_track_tasks(self) -> None:
        """Track tasks so you can wait for all tasks to be done."""
        self._track_task = True

    @callback
    def async_stop_track_tasks(self) -> None:
        """Stop track tasks so you can't wait for all tasks to be done."""
        self._track_task = False

    @callback
    def async_run_shc_job(
        self,
        job: SmartHomeControllerJob[
            collections.abc.Coroutine[typing.Any, typing.Any, _R] | _R
        ],
        *args: typing.Any,
    ) -> asyncio.Future[_R]:
        """Run a HassJob from within the event loop.

        This method must be run in the event loop.

        hassjob: HassJob
        args: parameters for method to call.
        """
        # This code path is performance sensitive and uses
        # if TYPE_CHECKING to avoid the overhead of constructing
        # the type used for the cast. For history see:
        # https://github.com/home-assistant/core/pull/71960
        if job.job_type == SmartHomeControllerJobType.CALLBACK:
            job.target(*args)
            return None

        return self.async_add_shc_job(job, *args)

    @callback
    def async_run_job(
        self,
        target: collections.abc.Callable[
            ..., collections.abc.Coroutine[typing.Any, typing.Any, _R] | _R
        ]
        | collections.abc.Coroutine[typing.Any, typing.Any, _R],
        *args: typing.Any,
    ) -> asyncio.Future[_R]:
        """Run a job from within the event loop.

        This method must be run in the event loop.

        target: target to call.
        args: parameters for method to call.
        """
        if asyncio.iscoroutine(target):
            return self.async_create_task(target)

        # This code path is performance sensitive and uses
        # if TYPE_CHECKING to avoid the overhead of constructing
        # the type used for the cast. For history see:
        # https://github.com/home-assistant/core/pull/71960
        if typing.TYPE_CHECKING:
            target = typing.cast(
                collections.abc.Callable[
                    ...,
                    typing.Union[
                        collections.abc.Coroutine[typing.Any, typing.Any, _R], _R
                    ],
                ],
                target,
            )
        return self.async_run_shc_job(SmartHomeControllerJob(target), *args)

    def block_till_done(self) -> None:
        """Block until all pending work is done."""
        asyncio.run_coroutine_threadsafe(
            self.async_block_till_done(), self._loop
        ).result()

    @staticmethod
    async def _await_and_log_pending(
        pending: collections.abc.Iterable[collections.abc.Awaitable[typing.Any]],
    ) -> None:
        """Await and log tasks that take a long time."""
        wait_time = 0
        done = False
        while not done:
            done, still_pending = await asyncio.wait(
                pending, timeout=_BLOCK_LOG_TIMEOUT
            )
            if done:
                return
            wait_time += _BLOCK_LOG_TIMEOUT
            for task in still_pending:
                _LOGGER.debug(f"Waited {wait_time} seconds for task: {task}")

    async def async_block_till_done(self) -> None:
        """Block until all pending work is done."""
        # To flush out any call_soon_threadsafe
        await asyncio.sleep(0)
        start_time: float = None

        while self._pending_tasks:
            pending = [task for task in self._pending_tasks if not task.done()]
            self._pending_tasks.clear()
            if pending:
                await self._await_and_log_pending(pending)

                if start_time is None:
                    # Avoid calling monotonic() until we know
                    # we may need to start logging blocked tasks.
                    start_time = 0
                elif start_time == 0:
                    # If we have waited twice then we set the start
                    # time
                    start_time = time.monotonic()
                elif time.monotonic() - start_time > _BLOCK_LOG_TIMEOUT:
                    # We have waited at least three loops and new tasks
                    # continue to block. At this point we start
                    # logging all waiting tasks.
                    for task in pending:
                        _LOGGER.debug(f"Waiting for task: {task}")
            else:
                await asyncio.sleep(0)

    def stop(self) -> None:
        """Stop the Smart Home Controller and shuts down all threads."""
        if self._state == CoreState.NOT_RUNNING:  # just ignore
            return
        helpers.fire_coroutine_threadsafe(self.async_stop(), self._loop)

    async def async_stop(self, exit_code: int = 0, *, force: bool = False) -> None:
        """Stop the Smart Home Controller and shuts down all threads.

        The "force" flag commands async_stop to proceed regardless of
        the Smart Home Controller's current state. You should not set this
        flag unless you're testing.

        This method is a coroutine.
        """
        if not force:
            # Some tests require async_stop to run,
            # regardless of the state of the loop.
            if self._state == CoreState.NOT_RUNNING:  # just ignore
                return
            if self.is_stopping:
                _LOGGER.info("Additional call to async_stop was ignored")
                return
            if self._state == CoreState.STARTING:
                # This may not work
                _LOGGER.warning(
                    "Stopping Smart Home - The Next Generation before startup "
                    + "has completed may fail"
                )

        # stage 1
        self._state = CoreState.STOPPING
        self.async_track_tasks()
        self._bus.async_fire(Const.EVENT_SHC_STOP)
        try:
            async with self._timeout.async_timeout(_STAGE_1_SHUTDOWN_TIMEOUT):
                await self.async_block_till_done()
        except asyncio.TimeoutError:
            _LOGGER.warning(
                "Timed out waiting for shutdown stage 1 to complete, the shutdown will continue"
            )

        # stage 2
        self._state = CoreState.FINAL_WRITE
        self._bus.async_fire(Const.EVENT_SHC_FINAL_WRITE)
        try:
            async with self._timeout.async_timeout(_STAGE_2_SHUTDOWN_TIMEOUT):
                await self.async_block_till_done()
        except asyncio.TimeoutError:
            _LOGGER.warning(
                "Timed out waiting for shutdown stage 2 to complete, the shutdown will continue"
            )

        # stage 3
        self._state = CoreState.NOT_RUNNING
        self._bus.async_fire(Const.EVENT_SHC_CLOSE)

        # Prevent run_callback_threadsafe from scheduling any additional
        # callbacks in the event loop as callbacks created on the futures
        # it returns will never run after the final `self.async_block_till_done`
        # which will cause the futures to block forever when waiting for
        # the `result()` which will cause a deadlock when shutting down the executor.
        helpers.shutdown_run_callback_threadsafe(self._loop)

        try:
            async with self._timeout.async_timeout(_STAGE_3_SHUTDOWN_TIMEOUT):
                await self.async_block_till_done()
        except asyncio.TimeoutError:
            _LOGGER.warning(
                "Timed out waiting for shutdown stage 3 to complete, the shutdown will continue"
            )

        self._exit_code = exit_code
        self._state = CoreState.STOPPED

        if self._stopped is not None:
            self._stopped.set()

    async def async_migrator(
        self,
        old_path: str,
        store: Store,
        *,
        old_conf_load_func: collections.abc.Callable = None,
        old_conf_migrate_func: collections.abc.Callable = None,
    ) -> typing.Any:
        """Migrate old data to a store and then load data.

        async def old_conf_migrate_func(old_data)
        """
        # If we already have store data we have already migrated in the past.
        if (store_data := await store.async_load()) is not None:
            return store_data

        def load_old_config():
            """Load old config."""
            if not os.path.isfile(old_path):
                return None

            if old_conf_load_func is not None:
                return old_conf_load_func(old_path)

            return helpers.load_json(old_path)

        config = await self.async_add_executor_job(load_old_config)

        if config is None:
            return None

        if old_conf_migrate_func is not None:
            config = await old_conf_migrate_func(config)

        await store.async_save(config)
        await self.async_add_executor_job(os.remove, old_path)
        return config

    def is_virtual_env(self) -> bool:
        """Return if we run in a virtual environment."""
        # Check supports venv && virtualenv
        return getattr(sys, "base_prefix", sys.prefix) != sys.prefix or hasattr(
            sys, "real_prefix"
        )

    def is_docker_env(self) -> bool:
        """Return True if we run in a docker env."""
        return pathlib.Path("/.dockerenv").exists()

    @staticmethod
    async def async_from_config(
        runtime_config: RuntimeConfig,
    ) -> SmartHomeController:
        """Set up Smart Home - The Next Generation."""
        result = TheNextGeneration()
        result.config.config_dir = runtime_config.config_dir

        result.setup.async_enable_logging(
            runtime_config.verbose,
            runtime_config.log_rotate_days,
            runtime_config.log_file,
            runtime_config.log_no_color,
        )

        result.config.skip_pip = runtime_config.skip_pip
        if runtime_config.skip_pip:
            _LOGGER.warning(
                "Skipping pip installation of required modules. This may cause issues"
            )

        if not await result.setup.async_ensure_config_exists():
            _LOGGER.error("Error getting configuration path")
            return None

        _LOGGER.info(f"Config directory:{runtime_config.config_dir}")

        config_dict = None
        basic_setup_success = False

        if not (safe_mode := runtime_config.safe_mode):
            await result.async_add_executor_job(result.setup.process_shc_config_upgrade)

            try:
                config_dict = await result.setup.async_shc_config_yaml()
            except SmartHomeControllerError as err:
                _LOGGER.error(
                    f"Failed to parse configuration.yaml: {err}. Activating safe mode",
                    err,
                )
            else:
                if not result.is_virtual_env():
                    await result.setup.async_mount_local_lib_path()

                basic_setup_success = (
                    await result.setup.async_from_config_dict(config_dict) is not None
                )

        if config_dict is None:
            safe_mode = True

        elif not basic_setup_success:
            _LOGGER.warning("Unable to set up core integrations. Activating safe mode")
            safe_mode = True

        elif (
            "frontend" in result.data.get(SetupManager.DATA_SETUP, {})
            and "frontend" not in result.config.components
        ):
            _LOGGER.warning("Detected that frontend did not load. Activating safe mode")
            # Ask integrations to shut down. It's messy but we can't
            # do a clean stop without knowing what is broken
            with contextlib.suppress(asyncio.TimeoutError):
                async with result.timeout.async_timeout(10):
                    await result.async_stop()

            safe_mode = True
            old_config = result.config
            old_logging = old_config.error_log_path

            TheNextGeneration._the_instance = None
            result = TheNextGeneration()
            if old_logging:
                result.config.error_log_path = old_logging
            result.config.skip_pip = old_config.skip_pip
            result.config.internal_url = old_config.internal_url
            result.config.external_url = old_config.external_url
            result.config.config_dir = old_config.config_dir

        if safe_mode:
            _LOGGER.info("Starting in safe mode")
            result.config.safe_mode = True

            http_conf = (await result.async_get_last_http_config()) or {}

            result = await result.setup.async_from_config_dict(
                {"safe_mode": {}, "http": http_conf}
            )

        if result and runtime_config.open_ui:
            result.add_job(result.open_shc_ui)

        return result

    async def async_get_last_http_config(self) -> dict:
        """Return the last known working config."""
        component = SmartHomeControllerComponent.get_component("http")
        if component is None:
            return None

        store = Store(self, component.storage_version, component.storage_key)
        return typing.cast(typing.Optional[dict], await store.async_load())

    def open_shc_ui(self) -> None:
        """Open the UI."""
        if self._config.api is None or "frontend" not in self._config.components:
            _LOGGER.warning("Cannot launch the UI because frontend not loaded")
            return

        scheme = "https" if self._config.api.use_ssl else "http"
        uri = str(
            yarl.URL.build(scheme=scheme, host="127.0.0.1", port=self._config.api.port)
        )

        if not webbrowser.open(uri):
            _LOGGER.warning(
                f"Unable to open the UI in a browser. Open it yourself at {uri}"
            )

    async def async_get_user_site(self, deps_dir: str) -> str:
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

    async def start_http_server_and_save_config(
        self, conf: dict, server: SmartHomeControllerHTTP
    ) -> None:
        """Startup the http server and save the config."""
        assert self._http is None or self._http == server
        self._http = server
        await server.start()

        # If we are set up successful, we store the HTTP settings for safe mode.
        component = SmartHomeControllerComponent.get_component("http")
        if component is not None:
            store = Store(self, component.storage_version, component.storage_key)

            if Const.CONF_TRUSTED_PROXIES in conf:
                conf[Const.CONF_TRUSTED_PROXIES] = [
                    str(
                        typing.cast(
                            typing.Union[ipaddress.IPv4Network, ipaddress.IPv6Network],
                            ip,
                        ).network_address
                    )
                    for ip in conf[Const.CONF_TRUSTED_PROXIES]
                ]

            store.async_delay_save(lambda: conf, component.storage_save_delay)
        for view in self._pending_view_registrations:
            server.register_view(view)
        self._pending_view_registrations = []

    def _attach_server(self, server: SmartHomeControllerHTTP):
        if self._http is None:
            self._http = server

    def register_view(
        self, view: SmartHomeControllerView | type[SmartHomeControllerView]
    ) -> None:
        """Register a view with the WSGI server.

        The view argument must be a class that inherits from NextGenerationView.
        It is optional to instantiate it before registering; this method will
        handle it either way.
        """
        if self._http:
            self._http.register_view(view)
        else:
            self._pending_view_registrations.append(view)

    def get_url(
        self,
        *,
        require_current_request: bool = False,
        require_ssl: bool = False,
        require_standard_port: bool = False,
        allow_internal: bool = True,
        allow_external: bool = True,
        allow_ip: bool = None,
        prefer_external: bool = None,
    ) -> str:
        """Get a URL to this instance."""
        if require_current_request and self._http.current_request.get() is None:
            raise NoURLAvailableError

        if prefer_external is None:
            prefer_external = self._config.api is not None and self._config.api.use_ssl

        if allow_ip is None:
            allow_ip = self._config.api is None or not self._config.api.use_ssl

        order = [_UrlType.INTERNAL, _UrlType.EXTERNAL]
        if prefer_external:
            order.reverse()

        # Try finding an URL in the order specified
        for url_type in order:
            if allow_internal and url_type == _UrlType.INTERNAL:
                with contextlib.suppress(NoURLAvailableError):
                    return self._get_internal_url(
                        allow_ip=allow_ip,
                        require_current_request=require_current_request,
                        require_ssl=require_ssl,
                        require_standard_port=require_standard_port,
                    )

            if allow_external and url_type == _UrlType.EXTERNAL:
                with contextlib.suppress(NoURLAvailableError):
                    return self._get_external_url(
                        allow_ip=allow_ip,
                        require_current_request=require_current_request,
                        require_ssl=require_ssl,
                        require_standard_port=require_standard_port,
                    )

        # For current request, we accept loopback interfaces (e.g., 127.0.0.1),
        # the Supervisor hostname and localhost transparently
        request_host = self._get_request_host()
        if (
            require_current_request
            and request_host is not None
            and self._config.api is not None
        ):
            scheme = "https" if self._config.api.use_ssl else "http"
            current_url = yarl.URL.build(
                scheme=scheme, host=request_host, port=self._config.api.port
            )

            known_hostnames = ["localhost"]
            if self._components.hassio.is_hassio():
                host_info = self._components.hassio.get_host_info()
                known_hostnames.extend(
                    [host_info["hostname"], f"{host_info['hostname']}.local"]
                )

            if (
                (
                    (
                        allow_ip
                        and helpers.is_ip_address(request_host)
                        and helpers.is_loopback(ipaddress.ip_address(request_host))
                    )
                    or request_host in known_hostnames
                )
                and (not require_ssl or current_url.scheme == "https")
                and (not require_standard_port or current_url.is_default_port())
            ):
                return helpers.normalize_url(str(current_url))

        # We have to be honest now, we have no viable option available
        raise NoURLAvailableError

    def _get_internal_url(
        self,
        *,
        allow_ip: bool = True,
        require_current_request: bool = False,
        require_ssl: bool = False,
        require_standard_port: bool = False,
    ) -> str:
        """Get internal URL of this instance."""
        if self._config.internal_url:
            internal_url = yarl.URL(self._config.internal_url)
            if (
                (
                    not require_current_request
                    or internal_url.host == self._get_request_host()
                )
                and (not require_ssl or internal_url.scheme == "https")
                and (not require_standard_port or internal_url.is_default_port())
                and (allow_ip or not helpers.is_ip_address(str(internal_url.host)))
            ):
                return helpers.normalize_url(str(internal_url))

        # Fallback to detected local IP
        if allow_ip and not (
            require_ssl or self._config.api is None or self._config.api.use_ssl
        ):
            ip_url = yarl.URL.build(
                scheme="http",
                host=self._config.api.local_ip,
                port=self._config.api.port,
            )
            if (
                ip_url.host
                and not helpers.is_loopback(ipaddress.ip_address(ip_url.host))
                and (
                    not require_current_request
                    or ip_url.host == self._get_request_host()
                )
                and (not require_standard_port or ip_url.is_default_port())
            ):
                return helpers.normalize_url(str(ip_url))

        raise NoURLAvailableError

    def _get_external_url(
        self,
        *,
        allow_ip: bool = True,
        require_current_request: bool = False,
        require_ssl: bool = False,
        require_standard_port: bool = False,
    ) -> str:
        """Get external URL of this instance."""
        if self._config.external_url:
            external_url = yarl.URL(self._config.external_url)
            if (
                (allow_ip or not helpers.is_ip_address(str(external_url.host)))
                and (
                    not require_current_request
                    or external_url.host == self._get_request_host()
                )
                and (not require_standard_port or external_url.is_default_port())
                and (
                    not require_ssl
                    or (
                        external_url.scheme == "https"
                        and not helpers.is_ip_address(str(external_url.host))
                    )
                )
            ):
                return helpers.normalize_url(str(external_url))

        raise NoURLAvailableError

    def _get_request_host(self) -> str:
        """Get the host address of the current request."""
        if (request := self._http.current_request.get()) is None:
            raise NoURLAvailableError
        return yarl.URL(request.url).host

    def run_callback_threadsafe(
        self,
        callback_func: collections.abc.Callable[..., _T],
        *args: typing.Any,
    ) -> concurrent.futures.Future[_T]:
        """Submit a callback object to the main event loop.

        Return a concurrent.futures.Future to access the result.
        """
        return helpers.run_callback_threadsafe(self._loop, callback_func, *args)

    def run_coroutine_threadsafe(
        self, coro: collections.abc.Coroutine[typing.Any, typing.Any, typing.Any]
    ) -> concurrent.futures.Future[_T]:
        return asyncio.run_coroutine_threadsafe(coro, self._loop)


# pylint: disable=protected-access


@callback
def _ensure_auth_manager_loaded(auth_mgr: AuthManager):
    """Ensure an auth manager is considered loaded."""
    store = auth_mgr._store
    if store._users is None:
        store._set_defaults()
