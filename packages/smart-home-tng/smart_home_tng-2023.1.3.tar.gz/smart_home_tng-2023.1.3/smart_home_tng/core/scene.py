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

import functools
import typing

from . import helpers
from .const import Const
from .restore_entity import RestoreEntity


# pylint: disable=unused-variable
class Scene(RestoreEntity):
    """A scene is a group of entities and the states we want them to be."""

    _attr_should_poll = False
    __last_activated: str = None

    @property
    @typing.final
    def state(self) -> str:
        """Return the state of the scene."""
        if self.__last_activated is None:
            return None
        return self.__last_activated

    @typing.final
    async def _async_activate(self, **kwargs: typing.Any) -> None:
        """Activate scene.

        Should not be overridden, handle setting last press timestamp.
        """
        self.__last_activated = helpers.utcnow().isoformat()
        self.async_write_state()
        await self.async_activate(**kwargs)

    async def async_internal_added_to_shc(self) -> None:
        """Call when the scene is added to hass."""
        await super().async_internal_added_to_shc()
        state = await self.async_get_last_state()
        if (
            state is not None
            and state.state is not None
            and state.state != Const.STATE_UNAVAILABLE
        ):
            self.__last_activated = state.state

    def activate(self, **kwargs: typing.Any) -> None:
        """Activate scene. Try to get entities into requested state."""
        raise NotImplementedError()

    async def async_activate(self, **kwargs: typing.Any) -> None:
        """Activate scene. Try to get entities into requested state."""
        task = self._shc.async_add_job(functools.partial(self.activate, **kwargs))
        if task:
            await task
