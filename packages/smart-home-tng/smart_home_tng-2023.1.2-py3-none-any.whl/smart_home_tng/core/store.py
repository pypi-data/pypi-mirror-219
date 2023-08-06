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
import contextlib
import copy
import inspect
import json
import logging
import os
import typing

from . import helpers
from .callback import callback
from .callback_type import CallbackType
from .const import Const
from .core_state import CoreState
from .event import Event
from .serialization_error import SerializationError

_T = typing.TypeVar(
    "_T",
    bound=typing.Union[typing.Mapping[str, typing.Any], typing.Sequence[typing.Any]],
)

_STORAGE_SEMAPHORE: typing.Final = "store.semaphore"
_STORAGE_DIR: typing.Final = ".storage"

_LOGGER: typing.Final = logging.getLogger(__name__)


if not typing.TYPE_CHECKING:

    class SmartHomeController:
        ...


if typing.TYPE_CHECKING:
    from .smart_home_controller import SmartHomeController


# pylint: disable=unused-variable
class Store(typing.Generic[_T]):
    """Class to help storing data."""

    def __init__(
        self,
        shc: SmartHomeController,
        version: int,
        key: str,
        private: bool = False,
        *,
        atomic_writes: bool = False,
        encoder: type[json.JSONEncoder] = None,
        minor_version: int = 1,
    ) -> None:
        """Initialize storage class."""
        self._shc = shc
        self._version = version
        self._minor_version = minor_version
        self._key = key
        self._private = private
        self._data: dict[str, typing.Any] = None
        self._unsub_delay_listener: CallbackType = None
        self._unsub_final_write_listener: CallbackType = None
        self._write_lock = asyncio.Lock()
        self._load_task: asyncio.Future[_T] = None
        self._encoder = encoder
        self._atomic_writes = atomic_writes

    @property
    def path(self):
        """Return the config path."""
        return self._shc.config.path(_STORAGE_DIR, self._key)

    async def async_load(self) -> _T:
        """Load data.

        If the expected version and minor version do not match the given versions, the
        migrate function will be invoked with migrate_func(version, minor_version, config).

        Will ensure that when a call comes in while another one is in progress,
        the second call will wait and return the result of the first call.
        """
        if self._load_task is None:
            self._load_task = self._shc.async_create_task(self._async_load())

        return await self._load_task

    async def _async_load(self) -> _T:
        """Load the data and ensure the task is removed."""
        if _STORAGE_SEMAPHORE not in self._shc.data:
            self._shc.data[_STORAGE_SEMAPHORE] = asyncio.Semaphore(
                Const.MAX_LOAD_CONCURRENTLY
            )

        try:
            async with self._shc.data[_STORAGE_SEMAPHORE]:
                return await self._async_load_data()
        finally:
            self._load_task = None

    async def _async_load_data(self) -> _T:
        """Load the data."""
        # Check if we have a pending write
        if self._data is not None:
            data = self._data

            # If we didn't generate data yet, do it now.
            if "data_func" in data:
                data["data"] = data.pop("data_func")()

            # We make a copy because code might assume it's safe to mutate loaded data
            # and we don't want that to mess with what we're trying to store.
            data = copy.deepcopy(data)
        else:
            data = await self._shc.async_add_executor_job(helpers.load_json, self.path)

            if data == {}:
                return None

        # Add minor_version if not set
        if "minor_version" not in data:
            data["minor_version"] = 1

        if (
            data["version"] == self._version
            and data["minor_version"] == self._minor_version
        ):
            stored: _T = data["data"]
        else:
            _LOGGER.info(
                "Migrating %s storage from "
                + f"{self._key}.{data['version']}.{data['minor_version']} to "
                + f"{self._version}.{self._minor_version}"
            )
            if len(inspect.signature(self._async_migrate_func).parameters) == 2:
                # pylint: disable-next=no-value-for-parameter
                stored = await self._async_migrate_func(data["version"], data["data"])
            else:
                try:
                    stored: _T = await self._async_migrate_func(
                        data["version"], data["minor_version"], data["data"]
                    )
                except NotImplementedError:
                    if data["version"] != self._version:
                        raise
                    stored = data["data"]

        return stored

    async def async_save(self, data: _T) -> None:
        """Save data."""
        self._data = {
            "version": self._version,
            "minor_version": self._minor_version,
            "key": self._key,
            "data": data,
        }

        if self._shc.state == CoreState.STOPPING:
            self._async_ensure_final_write_listener()
            return

        await self._async_handle_write_data()

    @callback
    def async_delay_save(
        self,
        data_func: typing.Callable[[], _T],
        delay: float = 0,
    ) -> None:
        """Save data with an optional delay."""

        self._data = {
            "version": self._version,
            "minor_version": self._minor_version,
            "key": self._key,
            "data_func": data_func,
        }

        self._async_cleanup_delay_listener()
        self._async_ensure_final_write_listener()

        if self._shc.state == CoreState.STOPPING:
            return

        self._unsub_delay_listener = self._shc.tracker.async_call_later(
            delay, self._async_callback_delayed_write
        )

    @callback
    def _async_ensure_final_write_listener(self) -> None:
        """Ensure that we write if we quit before delay has passed."""
        if self._unsub_final_write_listener is None:
            self._unsub_final_write_listener = self._shc.bus.async_listen_once(
                Const.EVENT_SHC_FINAL_WRITE, self._async_callback_final_write
            )

    @callback
    def _async_cleanup_final_write_listener(self) -> None:
        """Clean up a stop listener."""
        if self._unsub_final_write_listener is not None:
            self._unsub_final_write_listener()
            self._unsub_final_write_listener = None

    @callback
    def _async_cleanup_delay_listener(self) -> None:
        """Clean up a delay listener."""
        if self._unsub_delay_listener is not None:
            self._unsub_delay_listener()
            self._unsub_delay_listener = None

    async def _async_callback_delayed_write(self, _now):
        """Handle a delayed write callback."""
        # catch the case where a call is scheduled and then we stop Home Assistant
        if self._shc.state == CoreState.STOPPING:
            self._async_ensure_final_write_listener()
            return
        await self._async_handle_write_data()

    async def _async_callback_final_write(self, _event: Event) -> None:
        """Handle a write because Home Assistant is in final write state."""
        self._unsub_final_write_listener = None
        await self._async_handle_write_data()

    async def _async_handle_write_data(self, *_args):
        """Handle writing the config."""
        async with self._write_lock:
            self._async_cleanup_delay_listener()
            self._async_cleanup_final_write_listener()

            if self._data is None:
                # Another write already consumed the data
                return

            data = self._data

            if "data_func" in data:
                data["data"] = data.pop("data_func")()

            self._data = None

            try:
                await self._shc.async_add_executor_job(
                    self._write_data, self.path, data
                )
            except SerializationError as err:
                _LOGGER.error(f"Error writing config for {self._key}: {err}")

    def _write_data(self, path: str, data: dict) -> None:
        """Write the data."""
        os.makedirs(os.path.dirname(path), exist_ok=True)

        _LOGGER.debug(f"Writing data for {self._key} to {path}")
        helpers.save_json(
            path,
            data,
            self._private,
            encoder=self._encoder,
            atomic_writes=self._atomic_writes,
        )

    async def _async_migrate_func(
        self, _old_major_version, _old_minor_version, _old_data
    ):
        """Migrate to the new version."""
        raise NotImplementedError()

    async def async_remove(self) -> None:
        """Remove all data."""
        self._async_cleanup_delay_listener()
        self._async_cleanup_final_write_listener()

        with contextlib.suppress(FileNotFoundError):
            await self._shc.async_add_executor_job(os.unlink, self.path)
