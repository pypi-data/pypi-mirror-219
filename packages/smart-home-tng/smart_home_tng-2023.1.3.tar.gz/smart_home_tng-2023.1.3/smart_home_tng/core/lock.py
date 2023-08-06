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

# pylint: disable=unused-variable

import dataclasses
import datetime as dt
import enum
import functools as ft
import typing

import voluptuous as vol

from .config_validation import ConfigValidation as _cv
from .const import Const
from .entity import Entity
from .entity_description import EntityDescription
from .state_type import StateType

_ATTR_CHANGED_BY: typing.Final = "changed_by"
_PROP_TO_ATTR: typing.Final = {
    "changed_by": _ATTR_CHANGED_BY,
    "code_format": Const.ATTR_CODE_FORMAT,
}
_SCAN_INTERVAL: typing.Final = dt.timedelta(seconds=30)
_MIN_TIME_BETWEEN_SCANS: typing.Final = dt.timedelta(seconds=10)


class _EntityFeature(enum.IntEnum):
    """Supported features of the lock entity."""

    OPEN = 1


@dataclasses.dataclass
class _EntityDescription(EntityDescription):
    """A class that describes lock entities."""


class _Entity(Entity):
    """Base class for lock entities."""

    _entity_description: _EntityDescription
    _attr_changed_by: str = None
    _attr_code_format: str = None
    _attr_is_locked: bool = None
    _attr_is_locking: bool = None
    _attr_is_unlocking: bool = None
    _attr_is_jammed: bool = None
    _attr_state: None = None

    @property
    def changed_by(self) -> str:
        """Last change triggered by."""
        return self._attr_changed_by

    @property
    def code_format(self) -> str:
        """Regex for code format or None if no code is required."""
        return self._attr_code_format

    @property
    def is_locked(self) -> bool:
        """Return true if the lock is locked."""
        return self._attr_is_locked

    @property
    def is_locking(self) -> bool:
        """Return true if the lock is locking."""
        return self._attr_is_locking

    @property
    def is_unlocking(self) -> bool:
        """Return true if the lock is unlocking."""
        return self._attr_is_unlocking

    @property
    def is_jammed(self) -> bool:
        """Return true if the lock is jammed (incomplete locking)."""
        return self._attr_is_jammed

    def lock(self, **kwargs: typing.Any) -> None:
        """Lock the lock."""
        raise NotImplementedError()

    async def async_lock(self, **kwargs: typing.Any) -> None:
        """Lock the lock."""
        await self._shc.async_add_executor_job(ft.partial(self.lock, **kwargs))

    def unlock(self, **kwargs: typing.Any) -> None:
        """Unlock the lock."""
        raise NotImplementedError()

    async def async_unlock(self, **kwargs: typing.Any) -> None:
        """Unlock the lock."""
        await self._shc.async_add_executor_job(ft.partial(self.unlock, **kwargs))

    def open(self, **kwargs: typing.Any) -> None:
        """Open the door latch."""
        raise NotImplementedError()

    async def async_open(self, **kwargs: typing.Any) -> None:
        """Open the door latch."""
        await self._shc.async_add_executor_job(ft.partial(self.open, **kwargs))

    @typing.final
    @property
    def state_attributes(self) -> dict[str, StateType]:
        """Return the state attributes."""
        state_attr = {}
        for prop, attr in _PROP_TO_ATTR.items():
            if (value := getattr(self, prop)) is not None:
                state_attr[attr] = value
        return state_attr

    @typing.final
    @property
    def state(self) -> str:
        """Return the state."""
        if self.is_jammed:
            return Const.STATE_JAMMED
        if self.is_locking:
            return Const.STATE_LOCKING
        if self.is_unlocking:
            return Const.STATE_UNLOCKING
        if (locked := self.is_locked) is None:
            return None
        return Const.STATE_LOCKED if locked else Const.STATE_UNLOCKED


# pylint: disable=invalid-name
class Lock:
    """Lock namespace."""

    PLATFORM_SCHEMA: typing.Final = (_cv.PLATFORM_SCHEMA,)
    PLATFORM_SCHEMA_BASE: typing.Final = (_cv.PLATFORM_SCHEMA_BASE,)

    ATTR_CHANGED_BY: typing.Final = _ATTR_CHANGED_BY

    SCAN_INTERVAL: typing.Final = _SCAN_INTERVAL

    MIN_TIME_BETWEEN_SCANS: typing.Final = _MIN_TIME_BETWEEN_SCANS

    LOCK_SERVICE_SCHEMA = _cv.make_entity_service_schema(
        {vol.Optional(Const.ATTR_CODE): _cv.string}
    )

    Entity: typing.TypeAlias = _Entity
    EntityDescription: typing.TypeAlias = _EntityDescription
    EntityFeature: typing.TypeAlias = _EntityFeature
