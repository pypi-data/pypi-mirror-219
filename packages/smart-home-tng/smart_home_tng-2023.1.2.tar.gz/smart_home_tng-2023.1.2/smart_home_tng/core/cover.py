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
import enum
import functools as ft
import typing

import voluptuous as vol

from ..backports import strenum
from .config_validation import ConfigValidation as _cv
from .const import Const
from .entity import Entity
from .entity_description import EntityDescription

_P = typing.ParamSpec("_P")
_R = typing.TypeVar("_R")

if not typing.TYPE_CHECKING:

    class SmartHomeController:
        pass


if typing.TYPE_CHECKING:
    from .smart_home_controller import SmartHomeController


class _DeviceClass(strenum.LowercaseStrEnum):
    """Device class for cover."""

    # Refer to the cover dev docs for device class descriptions
    AWNING = enum.auto()
    BLIND = enum.auto()
    CURTAIN = enum.auto()
    DAMPER = enum.auto()
    DOOR = enum.auto()
    GARAGE = enum.auto()
    GATE = enum.auto()
    SHADE = enum.auto()
    SHUTTER = enum.auto()
    WINDOW = enum.auto()


_DEVICE_CLASSES_SCHEMA = vol.All(vol.Lower, vol.Coerce(_DeviceClass))


class _EntityFeature(enum.IntEnum):
    """Supported features of the cover entity."""

    OPEN = 1
    CLOSE = 2
    SET_POSITION = 4
    STOP = 8
    OPEN_TILT = 16
    CLOSE_TILT = 32
    STOP_TILT = 64
    SET_TILT_POSITION = 128


_ATTR_CURRENT_POSITION: typing.Final = "current_position"
_ATTR_CURRENT_TILT_POSITION: typing.Final = "current_tilt_position"
_ATTR_POSITION: typing.Final = "position"
_ATTR_TILT_POSITION: typing.Final = "tilt_position"


@dataclasses.dataclass
class _EntityDescription(EntityDescription):
    """A class that describes cover entities."""

    device_class: _DeviceClass | str = None


class _Entity(Entity):
    """Base class for cover entities."""

    _entity_description: _EntityDescription
    _attr_current_cover_position: int = None
    _attr_current_cover_tilt_position: int = None
    _attr_device_class: _DeviceClass | str
    _attr_is_closed: bool
    _attr_is_closing: bool = None
    _attr_is_opening: bool = None
    _attr_state: None = None

    _cover_is_last_toggle_direction_open = True

    @property
    def entity_description(self) -> _EntityDescription:
        return super().entity_description

    @property
    def current_cover_position(self) -> int:
        """Return current position of cover.

        None is unknown, 0 is closed, 100 is fully open.
        """
        return self._attr_current_cover_position

    @property
    def current_cover_tilt_position(self) -> int:
        """Return current position of cover tilt.

        None is unknown, 0 is closed, 100 is fully open.
        """
        return self._attr_current_cover_tilt_position

    @property
    def device_class(self) -> str:
        """Return the class of this entity."""
        if hasattr(self, "_attr_device_class"):
            return str(self._attr_device_class)
        if (description := self._entity_description) is not None:
            return str(description.device_class)
        return None

    @property
    @typing.final
    def state(self) -> str | None:
        """Return the state of the cover."""
        if self.is_opening:
            self._cover_is_last_toggle_direction_open = True
            return Cover.STATE_OPENING
        if self.is_closing:
            self._cover_is_last_toggle_direction_open = False
            return Cover.STATE_CLOSING

        if (closed := self.is_closed) is None:
            return None

        return Cover.STATE_CLOSED if closed else Cover.STATE_OPEN

    @typing.final
    @property
    def state_attributes(self) -> dict[str, typing.Any]:
        """Return the state attributes."""
        data = {}

        if (current := self.current_cover_position) is not None:
            data[_ATTR_CURRENT_POSITION] = current

        if (current_tilt := self.current_cover_tilt_position) is not None:
            data[_ATTR_CURRENT_TILT_POSITION] = current_tilt

        return data

    @property
    def supported_features(self) -> int:
        """Flag supported features."""
        if self._attr_supported_features is not None:
            return self._attr_supported_features

        supported_features = (
            _EntityFeature.OPEN | _EntityFeature.CLOSE | _EntityFeature.STOP
        )

        if self.current_cover_position is not None:
            supported_features |= _EntityFeature.SET_POSITION

        if self.current_cover_tilt_position is not None:
            supported_features |= (
                _EntityFeature.OPEN_TILT
                | _EntityFeature.CLOSE_TILT
                | _EntityFeature.STOP_TILT
                | _EntityFeature.SET_TILT_POSITION
            )

        return supported_features

    @property
    def is_opening(self) -> bool:
        """Return if the cover is opening or not."""
        return self._attr_is_opening

    @property
    def is_closing(self) -> bool:
        """Return if the cover is closing or not."""
        return self._attr_is_closing

    @property
    def is_closed(self) -> bool:
        """Return if the cover is closed or not."""
        return self._attr_is_closed

    def open_cover(self, **kwargs: typing.Any) -> None:
        """Open the cover."""
        raise NotImplementedError()

    async def async_open_cover(self, **kwargs: typing.Any) -> None:
        """Open the cover."""
        await self._shc.async_add_executor_job(ft.partial(self.open_cover, **kwargs))

    def close_cover(self, **kwargs: typing.Any) -> None:
        """Close cover."""
        raise NotImplementedError()

    async def async_close_cover(self, **kwargs: typing.Any) -> None:
        """Close cover."""
        await self._shc.async_add_executor_job(ft.partial(self.close_cover, **kwargs))

    def toggle(self, **kwargs: typing.Any) -> None:
        """Toggle the entity."""
        fns = {
            "open": self.open_cover,
            "close": self.close_cover,
            "stop": self.stop_cover,
        }
        function = self._get_toggle_function(fns)
        function(**kwargs)

    async def async_toggle(self, **kwargs: typing.Any) -> None:
        """Toggle the entity."""
        fns = {
            "open": self.async_open_cover,
            "close": self.async_close_cover,
            "stop": self.async_stop_cover,
        }
        function = self._get_toggle_function(fns)
        await function(**kwargs)

    def set_cover_position(self, **kwargs: typing.Any) -> None:
        """Move the cover to a specific position."""

    async def async_set_cover_position(self, **kwargs: typing.Any) -> None:
        """Move the cover to a specific position."""
        await self._shc.async_add_executor_job(
            ft.partial(self.set_cover_position, **kwargs)
        )

    def stop_cover(self, **kwargs: typing.Any) -> None:
        """Stop the cover."""

    async def async_stop_cover(self, **kwargs: typing.Any) -> None:
        """Stop the cover."""
        await self._shc.async_add_executor_job(ft.partial(self.stop_cover, **kwargs))

    def open_cover_tilt(self, **kwargs: typing.Any) -> None:
        """Open the cover tilt."""

    async def async_open_cover_tilt(self, **kwargs: typing.Any) -> None:
        """Open the cover tilt."""
        await self._shc.async_add_executor_job(
            ft.partial(self.open_cover_tilt, **kwargs)
        )

    def close_cover_tilt(self, **kwargs: typing.Any) -> None:
        """Close the cover tilt."""

    async def async_close_cover_tilt(self, **kwargs: typing.Any) -> None:
        """Close the cover tilt."""
        await self._shc.async_add_executor_job(
            ft.partial(self.close_cover_tilt, **kwargs)
        )

    def set_cover_tilt_position(self, **kwargs: typing.Any) -> None:
        """Move the cover tilt to a specific position."""

    async def async_set_cover_tilt_position(self, **kwargs: typing.Any) -> None:
        """Move the cover tilt to a specific position."""
        await self._shc.async_add_executor_job(
            ft.partial(self.set_cover_tilt_position, **kwargs)
        )

    def stop_cover_tilt(self, **kwargs: typing.Any) -> None:
        """Stop the cover."""

    async def async_stop_cover_tilt(self, **kwargs: typing.Any) -> None:
        """Stop the cover."""
        await self._shc.async_add_executor_job(
            ft.partial(self.stop_cover_tilt, **kwargs)
        )

    def toggle_tilt(self, **kwargs: typing.Any) -> None:
        """Toggle the entity."""
        if self.current_cover_tilt_position == 0:
            self.open_cover_tilt(**kwargs)
        else:
            self.close_cover_tilt(**kwargs)

    async def async_toggle_tilt(self, **kwargs: typing.Any) -> None:
        """Toggle the entity."""
        if self.current_cover_tilt_position == 0:
            await self.async_open_cover_tilt(**kwargs)
        else:
            await self.async_close_cover_tilt(**kwargs)

    def _get_toggle_function(
        self, fns: dict[str, typing.Callable[_P, _R]]
    ) -> typing.Callable[_P, _R]:
        if _EntityFeature.STOP | self.supported_features and (
            self.is_closing or self.is_opening
        ):
            return fns["stop"]
        if self.is_closed:
            return fns["open"]
        if self._cover_is_last_toggle_direction_open:
            return fns["close"]
        return fns["open"]


# pylint: disable=invalid-name
class Cover:
    """Cover namespace."""

    DeviceClass: typing.TypeAlias = _DeviceClass

    Entity: typing.TypeAlias = _Entity
    EntityDescription: typing.TypeAlias = _EntityDescription
    EntityFeature: typing.TypeAlias = _EntityFeature

    ATTR_CURRENT_POSITION: typing.Final = _ATTR_CURRENT_POSITION
    ATTR_CURRENT_TILT_POSITION: typing.Final = _ATTR_CURRENT_TILT_POSITION
    ATTR_POSITION: typing.Final = _ATTR_POSITION
    ATTR_TILT_POSITION: typing.Final = _ATTR_TILT_POSITION

    DEVICE_CLASSES_SCHEMA: typing.Final = _DEVICE_CLASSES_SCHEMA

    PLATFORM_SCHEMA: typing.Final = _cv.PLATFORM_SCHEMA
    PLATFORM_SCHEMA_BASE: typing.Final = _cv.PLATFORM_SCHEMA_BASE

    SERVICE_CLOSE: typing.Final = Const.SERVICE_CLOSE_COVER
    SERVICE_CLOSE_TILT: typing.Final = Const.SERVICE_CLOSE_COVER_TILT
    SERVICE_OPEN: typing.Final = Const.SERVICE_OPEN_COVER
    SERVICE_OPEN_TILT: typing.Final = Const.SERVICE_OPEN_COVER_TILT
    SERVICE_SET_POSITION: typing.Final = Const.SERVICE_SET_COVER_POSITION
    SERVICE_SET_TILT_POSITION: typing.Final = Const.SERVICE_SET_COVER_TILT_POSITION
    SERVICE_STOP: typing.Final = Const.SERVICE_STOP_COVER
    SERVICE_STOP_TILT: typing.Final = Const.SERVICE_STOP_COVER_TILT
    SERVICE_TOGGLE: typing.Final = Const.SERVICE_TOGGLE
    SERVICE_TOGGLE_TILT: typing.Final = Const.SERVICE_TOGGLE_COVER_TILT
    STATE_CLOSED: typing.Final = Const.STATE_CLOSED
    STATE_CLOSING: typing.Final = Const.STATE_CLOSING
    STATE_OPEN: typing.Final = Const.STATE_OPEN
    STATE_OPENING: typing.Final = Const.STATE_OPENING

    INTENT_OPEN_COVER: typing.Final = "ControllerOpenCover"
    INTENT_CLOSE_COVER: typing.Final = "ControllerCloseCover"

    @staticmethod
    def is_closed(shc: SmartHomeController, entity_id: str) -> bool:
        """Return if the cover is closed based on the statemachine."""
        return shc.states.is_state(entity_id, Cover.STATE_CLOSED)
