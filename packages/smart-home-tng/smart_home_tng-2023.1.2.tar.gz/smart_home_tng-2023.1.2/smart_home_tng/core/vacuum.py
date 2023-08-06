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

from . import helpers
from .const import Const
from .entity import Entity
from .entity_description import EntityDescription
from .toggle import Toggle

_ATTR_BATTERY_ICON: typing.Final = "battery_icon"
_ATTR_CLEANED_AREA: typing.Final = "cleaned_area"
_ATTR_FAN_SPEED: typing.Final = "fan_speed"
_ATTR_FAN_SPEED_LIST: typing.Final = "fan_speed_list"
_ATTR_PARAMS: typing.Final = "params"
_ATTR_STATUS: typing.Final = "status"

_SERVICE_CLEAN_SPOT: typing.Final = "clean_spot"
_SERVICE_LOCATE: typing.Final = "locate"
_SERVICE_RETURN_TO_BASE: typing.Final = "return_to_base"
_SERVICE_SEND_COMMAND: typing.Final = "send_command"
_SERVICE_SET_FAN_SPEED: typing.Final = "set_fan_speed"
_SERVICE_START_PAUSE: typing.Final = "start_pause"
_SERVICE_START: typing.Final = "start"
_SERVICE_PAUSE: typing.Final = "pause"
_SERVICE_STOP: typing.Final = "stop"


_STATE_CLEANING: typing.Final = "cleaning"
_STATE_DOCKED: typing.Final = "docked"
_STATE_RETURNING: typing.Final = "returning"
_STATE_ERROR: typing.Final = "error"

_STATES: typing.Final = [_STATE_CLEANING, _STATE_DOCKED, _STATE_RETURNING, _STATE_ERROR]

_DEFAULT_NAME: typing.Final = "Vacuum cleaner robot"


class _EntityFeature(enum.IntEnum):
    """Supported features of the vacuum entity."""

    TURN_ON = 1
    TURN_OFF = 2
    PAUSE = 4
    STOP = 8
    RETURN_HOME = 16
    FAN_SPEED = 32
    BATTERY = 64
    STATUS = 128
    SEND_COMMAND = 256
    LOCATE = 512
    CLEAN_SPOT = 1024
    MAP = 2048
    STATE = 4096
    START = 8192


class _BaseVacuum(Entity):
    """Representation of a base vacuum.

    Contains common properties and functions for all vacuum devices.
    """

    _attr_battery_icon: str
    _attr_battery_level: int = None
    _attr_fan_speed: str = None
    _attr_fan_speed_list: list[str]
    _attr_supported_features: int

    @property
    def supported_features(self) -> int:
        """Flag vacuum cleaner features that are supported."""
        return self._attr_supported_features

    @property
    def battery_level(self) -> int:
        """Return the battery level of the vacuum cleaner."""
        return self._attr_battery_level

    @property
    def battery_icon(self) -> str:
        """Return the battery icon for the vacuum cleaner."""
        return self._attr_battery_icon

    @property
    def fan_speed(self) -> str:
        """Return the fan speed of the vacuum cleaner."""
        return self._attr_fan_speed

    @property
    def fan_speed_list(self) -> list[str]:
        """Get the list of available fan speed steps of the vacuum cleaner."""
        return self._attr_fan_speed_list

    @property
    def capability_attributes(self) -> typing.Mapping[str, typing.Any]:
        """Return capability attributes."""
        if self.supported_features & _EntityFeature.FAN_SPEED:
            return {_ATTR_FAN_SPEED_LIST: self.fan_speed_list}
        return None

    @property
    def state_attributes(self) -> dict[str, typing.Any]:
        """Return the state attributes of the vacuum cleaner."""
        data: dict[str, typing.Any] = {}

        if self.supported_features & _EntityFeature.BATTERY:
            data[Const.ATTR_BATTERY_LEVEL] = self.battery_level
            data[_ATTR_BATTERY_ICON] = self.battery_icon

        if self.supported_features & _EntityFeature.FAN_SPEED:
            data[_ATTR_FAN_SPEED] = self.fan_speed

        return data

    def stop(self, **kwargs: typing.Any) -> None:
        """Stop the vacuum cleaner."""
        raise NotImplementedError()

    async def async_stop(self, **kwargs: typing.Any) -> None:
        """Stop the vacuum cleaner.

        This method must be run in the event loop.
        """
        await self._shc.async_add_executor_job(ft.partial(self.stop, **kwargs))

    def return_to_base(self, **kwargs: typing.Any) -> None:
        """Set the vacuum cleaner to return to the dock."""
        raise NotImplementedError()

    async def async_return_to_base(self, **kwargs: typing.Any) -> None:
        """Set the vacuum cleaner to return to the dock.

        This method must be run in the event loop.
        """
        await self._shc.async_add_executor_job(
            ft.partial(self.return_to_base, **kwargs)
        )

    def clean_spot(self, **kwargs: typing.Any) -> None:
        """Perform a spot clean-up."""
        raise NotImplementedError()

    async def async_clean_spot(self, **kwargs: typing.Any) -> None:
        """Perform a spot clean-up.

        This method must be run in the event loop.
        """
        await self._shc.async_add_executor_job(ft.partial(self.clean_spot, **kwargs))

    def locate(self, **kwargs: typing.Any) -> None:
        """Locate the vacuum cleaner."""
        raise NotImplementedError()

    async def async_locate(self, **kwargs: typing.Any) -> None:
        """Locate the vacuum cleaner.

        This method must be run in the event loop.
        """
        await self._shc.async_add_executor_job(ft.partial(self.locate, **kwargs))

    def set_fan_speed(self, fan_speed: str, **kwargs: typing.Any) -> None:
        """Set fan speed."""
        raise NotImplementedError()

    async def async_set_fan_speed(self, fan_speed: str, **kwargs: typing.Any) -> None:
        """Set fan speed.

        This method must be run in the event loop.
        """
        await self._shc.async_add_executor_job(
            ft.partial(self.set_fan_speed, fan_speed, **kwargs)
        )

    def send_command(
        self,
        command: str,
        params: dict[str, typing.Any] | list[typing.Any] = None,
        **kwargs: typing.Any,
    ) -> None:
        """Send a command to a vacuum cleaner."""
        raise NotImplementedError()

    async def async_send_command(
        self,
        command: str,
        params: dict[str, typing.Any] | list[typing.Any] = None,
        **kwargs: typing.Any,
    ) -> None:
        """Send a command to a vacuum cleaner.

        This method must be run in the event loop.
        """
        await self._shc.async_add_executor_job(
            ft.partial(self.send_command, command, params=params, **kwargs)
        )


@dataclasses.dataclass
class _EntityDescription(Toggle.EntityDescription):
    """A class that describes vacuum entities."""


class _Entity(_BaseVacuum, Toggle.Entity):
    """Representation of a vacuum cleaner robot."""

    _entity_description: _EntityDescription

    @property
    def entity_description(self) -> _EntityDescription:
        return super().entity_description

    @property
    def status(self) -> str | None:
        """Return the status of the vacuum cleaner."""
        return None

    @property
    def battery_icon(self) -> str:
        """Return the battery icon for the vacuum cleaner."""
        charging = False
        if self.status is not None:
            charging = "charg" in self.status.lower()
        return helpers.icon_for_battery_level(
            battery_level=self.battery_level, charging=charging
        )

    @typing.final
    @property
    def state_attributes(self) -> dict[str, typing.Any]:
        """Return the state attributes of the vacuum cleaner."""
        data = super().state_attributes

        if self.supported_features & _EntityFeature.STATUS:
            data[_ATTR_STATUS] = self.status

        return data

    def turn_on(self, **kwargs: typing.Any) -> None:
        """Turn the vacuum on and start cleaning."""
        raise NotImplementedError()

    async def async_turn_on(self, **kwargs: typing.Any) -> None:
        """Turn the vacuum on and start cleaning.

        This method must be run in the event loop.
        """
        await self._shc.async_add_executor_job(ft.partial(self.turn_on, **kwargs))

    def turn_off(self, **kwargs: typing.Any) -> None:
        """Turn the vacuum off stopping the cleaning and returning home."""
        raise NotImplementedError()

    async def async_turn_off(self, **kwargs: typing.Any) -> None:
        """Turn the vacuum off stopping the cleaning and returning home.

        This method must be run in the event loop.
        """
        await self._shc.async_add_executor_job(ft.partial(self.turn_off, **kwargs))

    def start_pause(self, **kwargs: typing.Any) -> None:
        """Start, pause or resume the cleaning task."""
        raise NotImplementedError()

    async def async_start_pause(self, **kwargs: typing.Any) -> None:
        """Start, pause or resume the cleaning task.

        This method must be run in the event loop.
        """
        await self._shc.async_add_executor_job(ft.partial(self.start_pause, **kwargs))

    async def async_pause(self) -> None:
        """Not supported."""

    async def async_start(self) -> None:
        """Not supported."""


@dataclasses.dataclass
class _StateEntityDescription(EntityDescription):
    """A class that describes vacuum entities."""


class _StateEntity(_BaseVacuum):
    """Representation of a vacuum cleaner robot that supports states."""

    _entity_description: _StateEntityDescription

    @property
    def entity_description(self) -> _StateEntityDescription:
        return super().entity_description

    @property
    def state(self) -> str:
        """Return the state of the vacuum cleaner."""
        return None

    @property
    def battery_icon(self) -> str:
        """Return the battery icon for the vacuum cleaner."""
        charging = bool(self.state == _STATE_DOCKED)

        return helpers.icon_for_battery_level(
            battery_level=self.battery_level, charging=charging
        )

    def start(self) -> None:
        """Start or resume the cleaning task."""
        raise NotImplementedError()

    async def async_start(self) -> None:
        """Start or resume the cleaning task.

        This method must be run in the event loop.
        """
        await self._shc.async_add_executor_job(self.start)

    def pause(self) -> None:
        """Pause the cleaning task."""
        raise NotImplementedError()

    async def async_pause(self) -> None:
        """Pause the cleaning task.

        This method must be run in the event loop.
        """
        await self._shc.async_add_executor_job(self.pause)

    async def async_turn_on(self, **kwargs: typing.Any) -> None:
        """Not supported."""

    async def async_turn_off(self, **kwargs: typing.Any) -> None:
        """Not supported."""

    async def async_toggle(self, **kwargs: typing.Any) -> None:
        """Not supported."""


# pylint: disable=invalid-name
class Vacuum:
    """Vacuum namespace."""

    ATTR_BATTERY_ICON: typing.Final = _ATTR_BATTERY_ICON
    ATTR_CLEANED_AREA: typing.Final = _ATTR_CLEANED_AREA
    ATTR_FAN_SPEED: typing.Final = _ATTR_FAN_SPEED
    ATTR_FAN_SPEED_LIST: typing.Final = _ATTR_FAN_SPEED_LIST
    ATTR_PARAMS: typing.Final = _ATTR_PARAMS
    ATTR_STATUS: typing.Final = _ATTR_STATUS

    SERVICE_CLEAN_SPOT: typing.Final = _SERVICE_CLEAN_SPOT
    SERVICE_LOCATE: typing.Final = _SERVICE_LOCATE
    SERVICE_RETURN_TO_BASE: typing.Final = _SERVICE_RETURN_TO_BASE
    SERVICE_SEND_COMMAND: typing.Final = _SERVICE_SEND_COMMAND
    SERVICE_SET_FAN_SPEED: typing.Final = _SERVICE_SET_FAN_SPEED
    SERVICE_START_PAUSE: typing.Final = _SERVICE_START_PAUSE
    SERVICE_START: typing.Final = _SERVICE_START
    SERVICE_PAUSE: typing.Final = _SERVICE_PAUSE
    SERVICE_STOP: typing.Final = _SERVICE_STOP

    STATE_CLEANING: typing.Final = _STATE_CLEANING
    STATE_DOCKED: typing.Final = _STATE_DOCKED
    STATE_RETURNING: typing.Final = _STATE_RETURNING
    STATE_ERROR: typing.Final = _STATE_ERROR

    STATES: typing.Final = _STATES

    DEFAULT_NAME: typing.Final = _DEFAULT_NAME

    Entity: typing.TypeAlias = _Entity
    EntityDescription: typing.TypeAlias = _EntityDescription
    EntityFeature: typing.TypeAlias = _EntityFeature

    StateEntity: typing.TypeAlias = _StateEntity
    StateEntityDescription: typing.TypeAlias = _StateEntityDescription
