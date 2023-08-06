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
import math
import typing

from . import helpers
from .toggle import Toggle

_SCAN_INTERVAL: typing.Final = dt.timedelta(seconds=30)


class _EntityFeature(enum.IntEnum):
    """Supported features of the fan entity."""

    SET_SPEED = 1
    OSCILLATE = 2
    DIRECTION = 4
    PRESET_MODE = 8


_SERVICE_INCREASE_SPEED: typing.Final = "increase_speed"
_SERVICE_DECREASE_SPEED: typing.Final = "decrease_speed"
_SERVICE_OSCILLATE: typing.Final = "oscillate"
_SERVICE_SET_DIRECTION: typing.Final = "set_direction"
_SERVICE_SET_PERCENTAGE: typing.Final = "set_percentage"
_SERVICE_SET_PRESET_MODE: typing.Final = "set_preset_mode"

_DIRECTION_FORWARD: typing.Final = "forward"
_DIRECTION_REVERSE: typing.Final = "reverse"

_ATTR_PERCENTAGE: typing.Final = "percentage"
_ATTR_PERCENTAGE_STEP: typing.Final = "percentage_step"
_ATTR_OSCILLATING: typing.Final = "oscillating"
_ATTR_DIRECTION: typing.Final = "direction"
_ATTR_PRESET_MODE: typing.Final = "preset_mode"
_ATTR_PRESET_MODES: typing.Final = "preset_modes"


class _NotValidPresetModeError(ValueError):
    """Exception class when the preset_mode in not in the preset_modes list."""


@dataclasses.dataclass
class _EntityDescription(Toggle.EntityDescription):
    """A class that describes fan entities."""


class _Entity(Toggle.Entity):
    """Base class for fan entities."""

    _entity_description: _EntityDescription
    _attr_current_direction: str | None = None
    _attr_oscillating: bool | None = None
    _attr_percentage: int | None
    _attr_preset_mode: str | None
    _attr_preset_modes: list[str] | None
    _attr_speed_count: int
    _attr_supported_features: int = 0

    @property
    def entity_description(self) -> _EntityDescription:
        return super().entity_description

    def set_percentage(self, percentage: int) -> None:
        """Set the speed of the fan, as a percentage."""
        raise NotImplementedError()

    async def async_set_percentage(self, percentage: int) -> None:
        """Set the speed of the fan, as a percentage."""
        if percentage == 0:
            await self.async_turn_off()
        await self._shc.async_add_executor_job(self.set_percentage, percentage)

    async def async_increase_speed(self, percentage_step: int = None) -> None:
        """Increase the speed of the fan."""
        await self._async_adjust_speed(1, percentage_step)

    async def async_decrease_speed(self, percentage_step: int = None) -> None:
        """Decrease the speed of the fan."""
        await self._async_adjust_speed(-1, percentage_step)

    async def _async_adjust_speed(self, modifier: int, percentage_step: int) -> None:
        """Increase or decrease the speed of the fan."""
        current_percentage = self.percentage or 0

        if percentage_step is not None:
            new_percentage = current_percentage + (percentage_step * modifier)
        else:
            speed_range = (1, self.speed_count)
            speed_index = math.ceil(
                helpers.percentage_to_ranged_value(speed_range, current_percentage)
            )
            new_percentage = helpers.ranged_value_to_percentage(
                speed_range, speed_index + modifier
            )

        new_percentage = max(0, min(100, new_percentage))

        await self.async_set_percentage(new_percentage)

    def set_preset_mode(self, preset_mode: str) -> None:
        """Set new preset mode."""
        raise NotImplementedError()

    async def async_set_preset_mode(self, preset_mode: str) -> None:
        """Set new preset mode."""
        await self._shc.async_add_executor_job(self.set_preset_mode, preset_mode)

    def _valid_preset_mode_or_raise(self, preset_mode: str) -> None:
        """Raise NotValidPresetModeError on invalid preset_mode."""
        preset_modes = self.preset_modes
        if not preset_modes or preset_mode not in preset_modes:
            raise _NotValidPresetModeError(
                f"The preset_mode {preset_mode} is not a valid preset_mode: {preset_modes}"
            )

    def set_direction(self, direction: str) -> None:
        """Set the direction of the fan."""
        raise NotImplementedError()

    async def async_set_direction(self, direction: str) -> None:
        """Set the direction of the fan."""
        await self._shc.async_add_executor_job(self.set_direction, direction)

    def turn_on(
        self,
        percentage: int = None,
        preset_mode: str = None,
        **kwargs: typing.Any,
    ) -> None:
        """Turn on the fan."""
        raise NotImplementedError()

    async def async_turn_on(
        self,
        percentage: int = None,
        preset_mode: str = None,
        **kwargs: typing.Any,
    ) -> None:
        """Turn on the fan."""
        await self._shc.async_add_executor_job(
            ft.partial(
                self.turn_on,
                percentage=percentage,
                preset_mode=preset_mode,
                **kwargs,
            )
        )

    def oscillate(self, oscillating: bool) -> None:
        """Oscillate the fan."""
        raise NotImplementedError()

    async def async_oscillate(self, oscillating: bool) -> None:
        """Oscillate the fan."""
        await self._shc.async_add_executor_job(self.oscillate, oscillating)

    @property
    def is_on(self) -> bool:
        """Return true if the entity is on."""
        return (
            self.percentage is not None and self.percentage > 0
        ) or self.preset_mode is not None

    @property
    def percentage(self) -> int:
        """Return the current speed as a percentage."""
        if hasattr(self, "_attr_percentage"):
            return self._attr_percentage
        return 0

    @property
    def speed_count(self) -> int:
        """Return the number of speeds the fan supports."""
        if hasattr(self, "_attr_speed_count"):
            return self._attr_speed_count
        return 100

    @property
    def percentage_step(self) -> float:
        """Return the step size for percentage."""
        return 100 / self.speed_count

    @property
    def current_direction(self) -> str:
        """Return the current direction of the fan."""
        return self._attr_current_direction

    @property
    def oscillating(self) -> bool:
        """Return whether or not the fan is currently oscillating."""
        return self._attr_oscillating

    @property
    def capability_attributes(self) -> dict[str, list[str]]:
        """Return capability attributes."""
        attrs = {}

        if (
            self.supported_features & _EntityFeature.SET_SPEED
            or self.supported_features & _EntityFeature.PRESET_MODE
        ):
            attrs[_ATTR_PRESET_MODES] = self.preset_modes

        return attrs

    @typing.final
    @property
    def state_attributes(self) -> dict[str, float | str]:
        """Return optional state attributes."""
        data: dict[str, float | str] = {}
        supported_features = self.supported_features

        if supported_features & _EntityFeature.DIRECTION:
            data[_ATTR_DIRECTION] = self.current_direction

        if supported_features & _EntityFeature.OSCILLATE:
            data[_ATTR_OSCILLATING] = self.oscillating

        if supported_features & _EntityFeature.SET_SPEED:
            data[_ATTR_PERCENTAGE] = self.percentage
            data[_ATTR_PERCENTAGE_STEP] = self.percentage_step

        if (
            supported_features & _EntityFeature.PRESET_MODE
            or supported_features & _EntityFeature.SET_SPEED
        ):
            data[_ATTR_PRESET_MODE] = self.preset_mode

        return data

    @property
    def supported_features(self) -> int:
        """Flag supported features."""
        return self._attr_supported_features

    @property
    def preset_mode(self) -> str:
        """Return the current preset mode, e.g., auto, smart, interval, favorite.

        Requires FanEntityFeature.SET_SPEED.
        """
        if hasattr(self, "_attr_preset_mode"):
            return self._attr_preset_mode
        return None

    @property
    def preset_modes(self) -> list[str]:
        """Return a list of available preset modes.

        Requires FanEntityFeature.SET_SPEED.
        """
        if hasattr(self, "_attr_preset_modes"):
            return self._attr_preset_modes
        return None


# pylint: disable=unused-variable, invalid-name
class Fan:
    """Fan namespace."""

    Entity: typing.TypeAlias = _Entity
    EntityDescription: typing.TypeAlias = _EntityDescription
    EntityFeature: typing.TypeAlias = _EntityFeature
    NotValidPresetModeError: typing.TypeAlias = _NotValidPresetModeError

    SERVICE_INCREASE_SPEED: typing.Final = _SERVICE_INCREASE_SPEED
    SERVICE_DECREASE_SPEED: typing.Final = _SERVICE_DECREASE_SPEED
    SERVICE_OSCILLATE: typing.Final = _SERVICE_OSCILLATE
    SERVICE_SET_DIRECTION: typing.Final = _SERVICE_SET_DIRECTION
    SERVICE_SET_PERCENTAGE: typing.Final = _SERVICE_SET_PERCENTAGE
    SERVICE_SET_PRESET_MODE: typing.Final = _SERVICE_SET_PRESET_MODE

    DIRECTION_FORWARD: typing.Final = _DIRECTION_FORWARD
    DIRECTION_REVERSE: typing.Final = _DIRECTION_REVERSE

    ATTR_PERCENTAGE: typing.Final = _ATTR_PERCENTAGE
    ATTR_PERCENTAGE_STEP: typing.Final = _ATTR_PERCENTAGE_STEP
    ATTR_OSCILLATING: typing.Final = _ATTR_OSCILLATING
    ATTR_DIRECTION: typing.Final = _ATTR_DIRECTION
    ATTR_PRESET_MODE: typing.Final = _ATTR_PRESET_MODE
    ATTR_PRESET_MODES: typing.Final = _ATTR_PRESET_MODES

    SCAN_INTERVAL: typing.Final = _SCAN_INTERVAL
