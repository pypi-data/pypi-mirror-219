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

import typing

from .callback import callback
from .store import Store

if not typing.TYPE_CHECKING:

    class SmartHomeController:
        pass


if typing.TYPE_CHECKING:
    from .smart_home_controller import SmartHomeController


_STORE_AUTHORIZED: typing.Final = "authorized"


# pylint: disable=unused-variable
class AlexaConfigStore:
    """A configuration store for Alexa."""

    _STORAGE_VERSION: typing.Final = 1
    _STORAGE_KEY: typing.Final = "alexa"

    def __init__(self, shc: SmartHomeController):
        """Initialize a configuration store."""
        self._data = None
        self._shc = shc
        self._store = Store(shc, self._STORAGE_VERSION, self._STORAGE_KEY)

    @property
    def authorized(self):
        """Return authorization status."""
        return self._data[_STORE_AUTHORIZED]

    @callback
    def set_authorized(self, authorized):
        """Set authorization status."""
        if authorized != self._data[_STORE_AUTHORIZED]:
            self._data[_STORE_AUTHORIZED] = authorized
            self._store.async_delay_save(lambda: self._data, 1.0)

    async def async_load(self):
        """Load saved configuration from disk."""
        if data := await self._store.async_load():
            self._data = data
        else:
            self._data = {_STORE_AUTHORIZED: False}
