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
import datetime as dt
import logging
import time
import typing
import urllib.error

import aiohttp
import requests

from . import helpers
from .callback import callback
from .callback_type import CallbackType
from .config_entry import _current_entry
from .config_entry_auth_failed import ConfigEntryAuthFailed
from .config_entry_not_ready import ConfigEntryNotReady
from .debouncer import Debouncer
from .smart_home_controller_job import SmartHomeControllerJob
from .update_failed import UpdateFailed


_T = typing.TypeVar("_T")


if not typing.TYPE_CHECKING:

    class SmartHomeController:
        pass


if typing.TYPE_CHECKING:
    from .smart_home_controller import SmartHomeController


_REQUEST_REFRESH_DEFAULT_COOLDOWN: typing.Final = 10
_REQUEST_REFRESH_DEFAULT_IMMEDIATE: typing.Final = True


# pylint: disable=unused-variable
class DataUpdateCoordinator(typing.Generic[_T]):
    """Class to manage fetching data from single endpoint."""

    def __init__(
        self,
        shc: SmartHomeController,
        logger: logging.Logger,
        *,
        name: str,
        update_interval: dt.timedelta = None,
        update_method: typing.Callable[[], typing.Awaitable[_T]] = None,
        request_refresh_debouncer: Debouncer[
            typing.Coroutine[typing.Any, typing.Any, None]
        ] = None,
    ) -> None:
        """Initialize global data updater."""
        self._shc = shc
        self._logger = logger
        self._name = name
        self._update_method = update_method
        self._update_interval = update_interval
        self._config_entry = _current_entry.get()

        # It's None before the first successful update.
        # Components should call async_config_entry_first_refresh
        # to make sure the first update was successful.
        # Set type to just T to remove annoying checks that data is not None
        # when it was already checked during setup.
        self._data: _T = None

        self._listeners: dict[CallbackType, tuple[CallbackType, object]] = {}
        self._job = SmartHomeControllerJob(self._handle_refresh_interval)
        self._unsub_refresh: CallbackType = None
        self._request_refresh_task: asyncio.TimerHandle = None
        self._last_update_success = True
        self._last_exception: Exception = None

        if request_refresh_debouncer is None:
            request_refresh_debouncer = Debouncer(
                shc,
                logger,
                cooldown=_REQUEST_REFRESH_DEFAULT_COOLDOWN,
                immediate=_REQUEST_REFRESH_DEFAULT_IMMEDIATE,
                function=self.async_refresh,
            )
        else:
            request_refresh_debouncer.function = self.async_refresh

        self._debounced_refresh = request_refresh_debouncer

    @property
    def name(self) -> str:
        return self._name

    @property
    def data(self) -> _T:
        return self._data

    @property
    def last_update_success(self) -> bool:
        return self._last_update_success

    @property
    def last_exception(self) -> Exception:
        return self._last_exception

    @property
    def update_interval(self):
        return self._update_interval

    @update_interval.setter
    def update_interval(self, value: dt.timedelta) -> None:
        self._update_interval = value

    @callback
    def async_add_listener(
        self, update_callback: CallbackType, context: typing.Any = None
    ) -> typing.Callable[[], None]:
        """Listen for data updates."""
        schedule_refresh = not self._listeners

        @callback
        def remove_listener() -> None:
            """Remove update listener."""
            self._listeners.pop(remove_listener)
            if not self._listeners:
                self._unschedule_refresh()

        self._listeners[remove_listener] = (update_callback, context)

        # This is the first listener, set up interval.
        if schedule_refresh:
            self._schedule_refresh()

        return remove_listener

    @callback
    def async_update_listeners(self) -> None:
        """Update all registered listeners."""
        for update_callback, _ in list(self._listeners.values()):
            update_callback()

    @callback
    def _unschedule_refresh(self) -> None:
        """Unschedule any pending refresh since there is no longer any listeners."""
        if self._unsub_refresh:
            self._unsub_refresh()
            self._unsub_refresh = None

    def async_contexts(self) -> typing.Generator[typing.Any, None, None]:
        """Return all registered contexts."""
        yield from (
            context for _, context in self._listeners.values() if context is not None
        )

    @callback
    def _schedule_refresh(self) -> None:
        """Schedule a refresh."""
        if self._update_interval is None:
            return

        if self._config_entry and self._config_entry.pref_disable_polling:
            return

        if self._unsub_refresh:
            self._unsub_refresh()
            self._unsub_refresh = None

        # We _floor_ utcnow to create a schedule on a rounded second,
        # minimizing the time between the point and the real activation.
        # That way we obtain a constant update frequency,
        # as long as the update process takes less than a second
        self._unsub_refresh = self._shc.tracker.async_track_point_in_utc_time(
            self._job,
            helpers.utcnow().replace(microsecond=0) + self._update_interval,
        )

    async def _handle_refresh_interval(self, _now: dt.datetime) -> None:
        """Handle a refresh interval occurrence."""
        self._unsub_refresh = None
        await self._async_refresh(log_failures=True, scheduled=True)

    async def async_request_refresh(self) -> None:
        """Request a refresh.

        Refresh will wait a bit to see if it can batch them.
        """
        await self._debounced_refresh.async_call()

    async def _async_update_data(self) -> _T:
        """Fetch the latest data from the source."""
        if self._update_method is None:
            raise NotImplementedError("Update method not implemented")
        return await self._update_method()

    async def async_config_entry_first_refresh(self) -> None:
        """Refresh data for the first time when a config entry is setup.

        Will automatically raise ConfigEntryNotReady if the refresh
        fails. Additionally logging is handled by config entry setup
        to ensure that multiple retries do not cause log spam.
        """
        await self._async_refresh(log_failures=False, raise_on_auth_failed=True)
        if self.last_update_success:
            return
        ex = ConfigEntryNotReady()
        ex.__cause__ = self.last_exception
        raise ex

    async def async_refresh(self) -> None:
        """Refresh data and log errors."""
        await self._async_refresh(log_failures=True)

    async def _async_refresh(  # noqa: C901
        self,
        log_failures: bool = True,
        raise_on_auth_failed: bool = False,
        scheduled: bool = False,
    ) -> None:
        """Refresh data."""
        if self._unsub_refresh:
            self._unsub_refresh()
            self._unsub_refresh = None

        self._debounced_refresh.async_cancel()

        if scheduled and self._shc.is_stopping:
            return

        if log_timing := self._logger.isEnabledFor(logging.DEBUG):
            start = time.monotonic()
        auth_failed = False

        try:
            self._data = await self._async_update_data()

        except (asyncio.TimeoutError, requests.exceptions.Timeout) as err:
            self._last_exception = err
            if self._last_update_success:
                if log_failures:
                    self._logger.error(f"Timeout fetching {self.name} data")
                self._last_update_success = False

        except (aiohttp.ClientError, requests.exceptions.RequestException) as err:
            self._last_exception = err
            if self._last_update_success:
                if log_failures:
                    self._logger.error(f"Error requesting {self.name} data: {err}")
                self._last_update_success = False

        except urllib.error.URLError as err:
            self._last_exception = err
            if self._last_update_success:
                if log_failures:
                    if err.reason == "timed out":
                        self._logger.error(f"Timeout fetching {self.name} data")
                    else:
                        self._logger.error(f"Error requesting {self.name} data: {err}")
                self._last_update_success = False

        except UpdateFailed as err:
            self._last_exception = err
            if self._last_update_success:
                if log_failures:
                    self._logger.error(f"Error fetching {self.name} data: {err}")
                self._last_update_success = False

        except ConfigEntryAuthFailed as err:
            auth_failed = True
            self._last_exception = err
            if self._last_update_success:
                if log_failures:
                    self._logger.error(
                        f"Authentication failed while fetching {self.name} data: {err}",
                    )
                self._last_update_success = False
            if raise_on_auth_failed:
                raise

            if self._config_entry:
                self._config_entry.async_start_reauth(self._shc)
        except NotImplementedError as err:
            self._last_exception = err
            raise err

        except Exception as err:  # pylint: disable=broad-except
            self._last_exception = err
            self._last_update_success = False
            self._logger.exception(f"Unexpected error fetching {self.name} data: {err}")

        else:
            if not self._last_update_success:
                self._last_update_success = True
                self._logger.info(f"Fetching {self.name} data recovered")

        finally:
            if log_timing:
                self._logger.debug(
                    f"Finished fetching {self.name} data in {time.monotonic() - start:.3f} "
                    + f"seconds (success: {self.last_update_success})",
                )
            if not auth_failed and self._listeners and not self._shc.is_stopping:
                self._schedule_refresh()

        self.async_update_listeners()

    @callback
    def async_set_update_error(self, err: Exception) -> None:
        """Manually set an error, log the message and notify listeners."""
        self._last_exception = err
        if self._last_update_success:
            self._logger.error(f"Error requesting {self.name} data: {err}")
            self._last_update_success = False
            self.async_update_listeners()

    @callback
    def async_set_updated_data(self, data: _T) -> None:
        """Manually update data, notify listeners and reset refresh interval."""
        if self._unsub_refresh:
            self._unsub_refresh()
            self._unsub_refresh = None

        self._debounced_refresh.async_cancel()

        self._data = data
        self._last_update_success = True
        self._logger.debug(
            f"Manually updated {self.name} data",
        )

        if self._listeners:
            self._schedule_refresh()

        self.async_update_listeners()
