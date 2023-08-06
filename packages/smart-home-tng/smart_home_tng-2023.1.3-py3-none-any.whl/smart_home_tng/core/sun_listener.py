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

import collections.abc
import datetime
import typing

import attr

from .callback import callback
from .callback_type import CallbackType
from .const import Const
from .smart_home_controller_job import SmartHomeControllerJob


if not typing.TYPE_CHECKING:

    class SmartHomeController:
        ...


if typing.TYPE_CHECKING:
    from .smart_home_controller import SmartHomeController


# pylint: disable=unused-variable
@attr.s
class SunListener:
    """Helper class to help listen to sun events."""

    def __init__(
        self,
        shc: SmartHomeController,
        job: SmartHomeControllerJob[collections.abc.Awaitable[None]],
        event: str,
        offset: datetime.timedelta = None,
    ):
        self._shc = shc
        self._job = job
        self._event = event
        self._offset = offset
        self._unsub_sun: CallbackType = None
        self._unsub_config: CallbackType = None

    @callback
    def async_attach(self) -> None:
        """Attach a sun listener."""
        assert self._unsub_config is None

        self._unsub_config = self._shc.bus.async_listen(
            Const.EVENT_CORE_CONFIG_UPDATE, self._handle_config_event
        )

        self._listen_next_sun_event()

    @callback
    def async_detach(self) -> None:
        """Detach the sun listener."""
        assert self._unsub_sun is not None
        assert self._unsub_config is not None

        self._unsub_sun()
        self._unsub_sun = None
        self._unsub_config()
        self._unsub_config = None

    @callback
    def _listen_next_sun_event(self) -> None:
        """Set up the sun event listener."""
        assert self._unsub_sun is None

        self._unsub_sun = self._shc.async_track_point_in_utc_time(
            self._handle_sun_event,
            self._shc.sun.get_astral_event_next(self._event, offset=self._offset),
        )

    @callback
    def _handle_sun_event(self, _now: typing.Any) -> None:
        """Handle solar event."""
        self._unsub_sun = None
        self._listen_next_sun_event()
        self._shc.async_run_shc_job(self._job)

    @callback
    def _handle_config_event(self, _event: typing.Any) -> None:
        """Handle core config update."""
        assert self._unsub_sun is not None
        self._unsub_sun()
        self._unsub_sun = None
        self._listen_next_sun_event()
