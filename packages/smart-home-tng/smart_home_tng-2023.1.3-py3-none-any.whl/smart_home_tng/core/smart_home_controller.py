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
import collections.abc
import concurrent.futures
import http
import ipaddress
import typing

import yarl
from aiohttp import web

from ..auth.auth_manager import AuthManager
from ..auth.providers.internal import InternalAuthProvider
from . import helpers
from .area_registry import AreaRegistry
from .callback import callback
from .callback_type import CallbackType
from .components import Components
from .config import Config
from .config_entries import ConfigEntries
from .const import Const
from .core_state import CoreState
from .current_controller import _current_controller
from .device_registry import DeviceRegistry
from .dispatcher import Dispatcher
from .entity_registry import EntityRegistry
from .event import Event
from .event_bus import EventBus
from .event_tracker import EventTracker
from .flow_dispatcher import FlowDispatcher
from .intent_manager import IntentManager
from .service_registry import ServiceRegistry
from .setup_manager import SetupManager
from .smart_home_controller_error import SmartHomeControllerError
from .smart_home_controller_http import SmartHomeControllerHTTP
from .smart_home_controller_job import SmartHomeControllerJob
from .smart_home_controller_view import SmartHomeControllerView
from .state_machine import StateMachine
from .store import Store
from .sun import Sun
from .timeout_manager import TimeoutManager
from .translations import Translations

_T = typing.TypeVar("_T")
_R = typing.TypeVar("_R")

_SmartHomeControllerT = typing.TypeVar(
    "_SmartHomeControllerT", bound="SmartHomeController"
)

# pylint: disable=unused-variable


class SmartHomeController(abc.ABC):
    """
    The Base-Class for all Smart Home Controllers.

    Necessary to avoid circular imports.
    """

    CUSTOM_WARNING: typing.Final = (
        "We found a custom integration %s which has not "
        + "been tested by Smart Home - The Next Generation. This component might "
        + "cause stability problems, be sure to disable it if you "
        + "experience issues with Smart Home - The Next Generation"
    )

    def __init__(self):
        if _current_controller.get() is not None:
            raise SmartHomeControllerError("There can be only one!")
        _current_controller.set(self)

    @staticmethod
    def current():
        return _current_controller.get()

    @abc.abstractmethod
    async def async_get_instance_id(self) -> str:
        """Get unique ID for the Smart Home - The Next Generation instance."""

    @property
    @abc.abstractmethod
    def sun(self) -> Sun:
        """Returns a helper for Sun Events."""

    @property
    @abc.abstractmethod
    def translations(self) -> Translations:
        """Get the translation helper."""

    @property
    @abc.abstractmethod
    def area_registry(self) -> AreaRegistry:
        """Return the Area Registry for the Smart Home Controller."""

    @property
    @abc.abstractmethod
    def auth(self) -> AuthManager:
        """Return the Authorization Manager for the Smart Home Controller."""

    @auth.setter
    @abc.abstractmethod
    def auth(self, auth: AuthManager) -> None:
        """Set the Authorization Manager on startup."""

    @property
    @abc.abstractmethod
    def dispatcher(self) -> Dispatcher:
        """Return the Signal Handler for the Smart Home Controller."""

    @property
    @abc.abstractmethod
    def flow_dispatcher(self) -> FlowDispatcher:
        """Return the Flow Handler for the Smart Home Controller."""

    @abc.abstractmethod
    @callback
    def async_get_shc_auth_provider(self) -> InternalAuthProvider:
        """Get the internal auth provider."""

    @property
    @abc.abstractmethod
    def bus(self) -> EventBus:
        """Return the Event Bus."""

    @property
    @abc.abstractmethod
    def components(self) -> Components:
        """Return the Components of the Smart Home Controller."""

    @property
    @abc.abstractmethod
    def config(self) -> Config:
        """Return the Core Configuration of the Smart Home Controller."""

    @property
    @abc.abstractmethod
    def config_entries(self) -> ConfigEntries:
        """Return the Config Entries of the Smart Home Controller."""

    @config_entries.setter
    @abc.abstractmethod
    def config_entries(self, entries: ConfigEntries) -> None:
        """Set Config Entries during setup."""

    @property
    @abc.abstractmethod
    def data(self) -> dict[str, typing.Any]:
        """Return non-persistent data store for components."""

    @property
    @abc.abstractmethod
    def device_registry(self) -> DeviceRegistry:
        """Return the Device Registry of the Smart Home Controller."""

    @property
    @abc.abstractmethod
    def entity_registry(self) -> EntityRegistry:
        """Return the Entity Registry of the Smart Home Controller."""

    @property
    @abc.abstractmethod
    def entity_sources(self) -> dict[str, dict[str, str]]:
        """Get the Entity Sources / Entity Info."""

    @property
    @abc.abstractmethod
    def http(self) -> SmartHomeControllerHTTP:
        """Get the HTTP Server of the Smart Home Controller."""

    @property
    @abc.abstractmethod
    def services(self) -> ServiceRegistry:
        """Return the Service Registry of the Smart Home Controller."""

    @property
    @abc.abstractmethod
    def setup(self) -> SetupManager:
        """Return the Setup Manager of the Smart Home Controller."""

    @property
    @abc.abstractmethod
    def states(self) -> StateMachine:
        """Return the State Machine of the Smart Home Controller."""

    @property
    @abc.abstractmethod
    def timeout(self) -> TimeoutManager:
        """Return the Timeout Manager of the Smart Home Controller."""

    @property
    @abc.abstractmethod
    def tracker(self) -> EventTracker:
        """Get the Event Tracker Helpers of the Smart Home Controller."""

    @property
    @abc.abstractmethod
    def intents(self) -> IntentManager:
        """Get the Intent Manager of the Smart Home Controller."""

    @property
    @abc.abstractmethod
    def is_running(self) -> bool:
        """Return if Smart Home Controller is running."""

    # If Home Assistant is running in safe mode
    @property
    @abc.abstractmethod
    def in_safe_mode(self) -> bool:
        """Return if the Smart Home Controller running in safe mode."""

    @property
    @abc.abstractmethod
    def is_stopping(self) -> bool:
        """Return if Smart Home Controller is stopping."""

    @property
    @abc.abstractmethod
    def state(self) -> CoreState:
        """Returns the state of the Smart Home Controller."""

    @abc.abstractmethod
    def start(self) -> int:
        """Start the Smart Home Controller.

        Note: This function is only used for testing.
        For regular use, use "await hass.run()".
        """

    @abc.abstractmethod
    async def async_run(self, *, attach_signals: bool = True) -> int:
        """Smart Home Controller main entry point.

        Start the Smart Home Controller and block until stopped.

        This method is a coroutine.
        """

    @abc.abstractmethod
    @callback
    def async_register_signal_handling(self) -> None:
        """Register system signal handler for core."""

    @abc.abstractmethod
    async def async_start(self) -> None:
        """Finalize startup from inside the event loop.

        This method is a coroutine.
        """

    @abc.abstractmethod
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

    @typing.overload
    @callback
    def async_add_job(
        self,
        target: collections.abc.Callable[
            ..., collections.abc.Coroutine[typing.Any, typing.Any, _R]
        ],
        *args: typing.Any,
    ) -> asyncio.Future[_R]:
        ...

    @typing.overload
    @callback
    def async_add_job(
        self,
        target: collections.abc.Callable[
            ..., collections.abc.Coroutine[typing.Any, typing.Any, _R] | _R
        ],
        *args: typing.Any,
    ) -> asyncio.Future[_R]:
        ...

    @typing.overload
    @callback
    def async_add_job(
        self,
        target: collections.abc.Coroutine[typing.Any, typing.Any, _R],
        *args: typing.Any,
    ) -> asyncio.Future[_R]:
        ...

    @abc.abstractmethod
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

    @typing.overload
    @callback
    def async_add_shc_job(
        self,
        job: SmartHomeControllerJob[
            collections.abc.Coroutine[typing.Any, typing.Any, _R]
        ],
        *args: typing.Any,
    ) -> asyncio.Future[_R]:
        ...

    @typing.overload
    @callback
    def async_add_shc_job(
        self,
        job: SmartHomeControllerJob[
            collections.abc.Coroutine[typing.Any, typing.Any, _R] | _R
        ],
        *args: typing.Any,
    ) -> asyncio.Future[_R]:
        ...

    @abc.abstractmethod
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

    @abc.abstractmethod
    def create_task(
        self, target: collections.abc.Coroutine[typing.Any, typing.Any, typing.Any]
    ):
        """Add task to the executor pool.

        target: target to call.
        """

    @abc.abstractmethod
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

    @abc.abstractmethod
    def call_later(self, delay: float, func: typing.Any, *args) -> asyncio.TimerHandle:
        """Schedule task."""

    @abc.abstractmethod
    def call_soon_threadsafe(self, func: typing.Any, *args) -> None:
        """Schedule task for asap execution."""

    @abc.abstractmethod
    def run_in_executor(self, executor, func, *args):
        """Run a func in an executor pool."""

    @abc.abstractmethod
    @callback
    def async_add_executor_job(
        self, target: collections.abc.Callable[..., _T], *args: typing.Any
    ) -> asyncio.Future[_T]:
        """Add an executor job from within the event loop."""

    @abc.abstractmethod
    @callback
    def async_track_tasks(self) -> None:
        """Track tasks so you can wait for all tasks to be done."""

    @abc.abstractmethod
    @callback
    def async_stop_track_tasks(self) -> None:
        """Stop track tasks so you can't wait for all tasks to be done."""

    @abc.abstractmethod
    @callback
    def async_run_shc_job(
        self,
        job: SmartHomeControllerJob[
            collections.abc.Coroutine[typing.Any, typing.Any, _R] | _R
        ],
        *args: typing.Any,
    ) -> asyncio.Future[_R]:
        """Run a Smart Home Controller Job from within the event loop.

        This method must be run in the event loop.

        job: SmartHomeControllerJob
        args: parameters for method to call.
        """

    @typing.overload
    @callback
    def async_run_job(
        self,
        target: collections.abc.Callable[
            ..., collections.abc.Coroutine[typing.Any, typing.Any, _R]
        ],
        *args: typing.Any,
    ) -> asyncio.Future[_R]:
        ...

    @typing.overload
    @callback
    def async_run_job(
        self,
        target: collections.abc.Callable[
            ..., collections.abc.Coroutine[typing.Any, typing.Any, _R] | _R
        ],
        *args: typing.Any,
    ) -> asyncio.Future[_R]:
        ...

    @typing.overload
    @callback
    def async_run_job(
        self,
        target: collections.abc.Coroutine[typing.Any, typing.Any, _R],
        *args: typing.Any,
    ) -> asyncio.Future[_R]:
        ...

    @abc.abstractmethod
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

    @abc.abstractmethod
    def block_till_done(self) -> None:
        """Block until all pending work is done."""

    @abc.abstractmethod
    async def async_block_till_done(self) -> None:
        """Block until all pending work is done."""

    @abc.abstractmethod
    def stop(self) -> None:
        """Stop Home Assistant and shuts down all threads."""

    @abc.abstractmethod
    async def async_stop(self, exit_code: int = 0, *, force: bool = False) -> None:
        """Stop Home Assistant and shuts down all threads.

        The "force" flag commands async_stop to proceed regardless of
        Home Assistant's current state. You should not set this flag
        unless you're testing.

        This method is a coroutine.
        """

    @abc.abstractmethod
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

    @abc.abstractmethod
    def is_virtual_env(self) -> bool:
        """Return if we run in a virtual environment."""
        # Check supports venv && virtualenv

    @abc.abstractmethod
    def is_docker_env(self) -> bool:
        """Return True if we run in a docker env."""

    @abc.abstractmethod
    async def async_get_user_site(self, deps_dir: str) -> str:
        """Return user local library path.

        This function is a coroutine.
        """

    @abc.abstractmethod
    def run_callback_threadsafe(
        self,
        callback_func: collections.abc.Callable[..., _T],
        *args: typing.Any,
    ) -> concurrent.futures.Future[_T]:
        """Submit a callback object to the main event loop.

        Return a concurrent.futures.Future to access the result.
        """

    @abc.abstractmethod
    def run_coroutine_threadsafe(
        self, coro: collections.abc.Coroutine[typing.Any, typing.Any, typing.Any]
    ) -> concurrent.futures.Future[_T]:
        """Submit a coroutine object to a given event loop.

        Return a concurrent.futures.Future to access the result.
        """

    @abc.abstractmethod
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

    @abc.abstractmethod
    async def start_http_server_and_save_config(
        self, conf: dict, server: SmartHomeControllerHTTP
    ) -> None:
        """Startup the http server and save the config."""

    @abc.abstractmethod
    def _attach_server(self, server: SmartHomeControllerHTTP):
        """Prepare Server Startup."""

    @staticmethod
    def log_invalid_auth(
        func: collections.abc.Callable[
            ..., collections.abc.Awaitable[web.StreamResponse]
        ]
    ) -> collections.abc.Callable[..., collections.abc.Awaitable[web.StreamResponse]]:
        """Decorate function to handle invalid auth or failed login attempts."""

        async def handle_req(
            view: SmartHomeControllerView,
            request: web.Request,
            *args: typing.Any,
            **kwargs: typing.Any,
        ) -> web.StreamResponse:
            """Try to log failed login attempts if response status >= BAD_REQUEST."""
            resp = await func(view, request, *args, **kwargs)
            if resp.status >= http.HTTPStatus.BAD_REQUEST:
                shc = request.app[Const.KEY_SHC]
                if shc is not None:
                    await shc.http.process_wrong_login(request)
            return resp

        return handle_req

    @callback
    def async_at_start(
        self,
        at_start_cb: collections.abc.Callable[
            [_SmartHomeControllerT], collections.abc.Awaitable[None]
        ],
    ) -> CallbackType:
        """Execute something when Home Assistant is started.

        Will execute it now if Home Assistant is already started.
        """
        at_start_job = SmartHomeControllerJob(at_start_cb)
        if self.is_running:
            self.async_run_shc_job(at_start_job, self)
            return lambda: None

        unsub: CallbackType = None

        @callback
        def _matched_event(_event: Event) -> None:
            """Call the callback when Home Assistant started."""
            self.async_run_shc_job(at_start_job, self)
            nonlocal unsub
            unsub = None

        @callback
        def cancel() -> None:
            if unsub:
                unsub()

        unsub = self.bus.async_listen_once(Const.EVENT_SHC_START, _matched_event)
        return cancel

    @abc.abstractmethod
    def register_view(
        self, view: SmartHomeControllerView | type[SmartHomeControllerView]
    ) -> None:
        """Register a view with the WSGI server.

        The view argument must be a class that inherits from NextGenerationView.
        It is optional to instantiate it before registering; this method will
        handle it either way.
        """

    def is_shc_url(self, url: str) -> bool:
        """Return if the URL points at this Home Assistant instance."""
        parsed = yarl.URL(url)

        if not parsed.is_absolute():
            return False

        if parsed.is_default_port():
            parsed = parsed.with_port(None)

        def host_ip() -> str:
            if self.config.api is None or helpers.is_loopback(
                ipaddress.ip_address(self.config.api.local_ip)
            ):
                return None

            return str(
                yarl.URL.build(
                    scheme="http",
                    host=self.config.api.local_ip,
                    port=self.config.api.port,
                )
            )

        potential_base_factory: typing.Callable[[], str]
        for potential_base_factory in (
            lambda: self.config.internal_url,
            lambda: self.config.external_url,
            host_ip,
        ):
            potential_base = potential_base_factory()

            if potential_base is None:
                continue

            potential_parsed = yarl.URL(helpers.normalize_url(potential_base))

            if (
                parsed.scheme == potential_parsed.scheme
                and parsed.authority == potential_parsed.authority
            ):
                return True

        return False
