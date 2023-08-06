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
import typing

import voluptuous as vol

from ..backports import strenum
from .const import Const
from .toggle import Toggle

_SCAN_INTERVAL: typing.Final = dt.timedelta(seconds=60)
_MODE_NORMAL: typing.Final = "normal"
_MODE_ECO: typing.Final = "eco"
_MODE_AWAY: typing.Final = "away"
_MODE_BOOST: typing.Final = "boost"
_MODE_COMFORT: typing.Final = "comfort"
_MODE_HOME: typing.Final = "home"
_MODE_SLEEP: typing.Final = "sleep"
_MODE_AUTO: typing.Final = "auto"
_MODE_BABY: typing.Final = "baby"

_ATTR_AVAILABLE_MODES: typing.Final = "available_modes"
_ATTR_HUMIDITY: typing.Final = "humidity"
_ATTR_MAX_HUMIDITY: typing.Final = "max_humidity"
_ATTR_MIN_HUMIDITY: typing.Final = "min_humidity"

_DEFAULT_MIN_HUMIDITY: typing.Final = 0
_DEFAULT_MAX_HUMIDITY: typing.Final = 100

_SERVICE_SET_MODE: typing.Final = "set_mode"
_SERVICE_SET_HUMIDITY: typing.Final = "set_humidity"


class _EntityFeature(enum.IntEnum):
    """Supported features of the alarm control panel entity."""

    MODES = 1


class _DeviceClass(strenum.LowercaseStrEnum):
    """Device class for humidifiers."""

    HUMIDIFIER = enum.auto()
    DEHUMIDIFIER = enum.auto()


_DEVICE_CLASSES_SCHEMA: typing.Final = vol.All(vol.Lower, vol.Coerce(_DeviceClass))


@dataclasses.dataclass
class _EntityDescription(Toggle.EntityDescription):
    """A class that describes humidifier entities."""

    device_class: _DeviceClass | str = None


class _Entity(Toggle.Entity):
    """Base class for humidifier entities."""

    _entity_description: _EntityDescription
    _attr_available_modes: list[str]
    _attr_device_class: _DeviceClass | str
    _attr_max_humidity: int = _DEFAULT_MAX_HUMIDITY
    _attr_min_humidity: int = _DEFAULT_MIN_HUMIDITY
    _attr_mode: str
    _attr_target_humidity: int = None

    @property
    def entity_description(self) -> _EntityDescription:
        return super().entity_description

    @property
    def capability_attributes(self) -> dict[str, typing.Any]:
        """Return capability attributes."""
        supported_features = self.supported_features or 0
        data: dict[str, int | list[str]] = {
            _ATTR_MIN_HUMIDITY: self.min_humidity,
            _ATTR_MAX_HUMIDITY: self.max_humidity,
        }

        if supported_features & _EntityFeature.MODES:
            data[_ATTR_AVAILABLE_MODES] = self.available_modes

        return data

    @property
    def device_class(self) -> str:
        """Return the class of this entity."""
        if hasattr(self, "_attr_device_class"):
            return str(self._attr_device_class)
        if hasattr(self, "_entity_description"):
            return str(self.entity_description.device_class)
        return None

    @typing.final
    @property
    def state_attributes(self) -> dict[str, typing.Any]:
        """Return the optional state attributes."""
        supported_features = self.supported_features or 0
        data: dict[str, int | str] = {}

        if self.target_humidity is not None:
            data[_ATTR_HUMIDITY] = self.target_humidity

        if supported_features & _EntityFeature.MODES:
            data[Const.ATTR_MODE] = self.mode

        return data

    @property
    def target_humidity(self) -> int | None:
        """Return the humidity we try to reach."""
        return self._attr_target_humidity

    @property
    def mode(self) -> str | None:
        """Return the current mode, e.g., home, auto, baby.

        Requires HumidifierEntityFeature.MODES.
        """
        return self._attr_mode

    @property
    def available_modes(self) -> list[str] | None:
        """Return a list of available modes.

        Requires HumidifierEntityFeature.MODES.
        """
        return self._attr_available_modes

    def set_humidity(self, humidity: int) -> None:
        """Set new target humidity."""
        raise NotImplementedError()

    async def async_set_humidity(self, humidity: int) -> None:
        """Set new target humidity."""
        await self._shc.async_add_executor_job(self.set_humidity, humidity)

    def set_mode(self, mode: str) -> None:
        """Set new mode."""
        raise NotImplementedError()

    async def async_set_mode(self, mode: str) -> None:
        """Set new mode."""
        await self._shc.async_add_executor_job(self.set_mode, mode)

    @property
    def min_humidity(self) -> int:
        """Return the minimum humidity."""
        return self._attr_min_humidity

    @property
    def max_humidity(self) -> int:
        """Return the maximum humidity."""
        return self._attr_max_humidity


# pylint: disable=invalid-name
class Humidifier:
    """Humidifier namespace."""

    SCAN_INTERVAL: typing.Final = _SCAN_INTERVAL
    MODE_NORMAL: typing.Final = _MODE_NORMAL
    MODE_ECO: typing.Final = _MODE_ECO
    MODE_AWAY: typing.Final = _MODE_AWAY
    MODE_BOOST: typing.Final = _MODE_BOOST
    MODE_COMFORT: typing.Final = _MODE_COMFORT
    MODE_HOME: typing.Final = _MODE_HOME
    MODE_SLEEP: typing.Final = _MODE_SLEEP
    MODE_AUTO: typing.Final = _MODE_AUTO
    MODE_BABY: typing.Final = _MODE_BABY

    ATTR_AVAILABLE_MODES: typing.Final = _ATTR_AVAILABLE_MODES
    ATTR_HUMIDITY: typing.Final = _ATTR_HUMIDITY
    ATTR_MAX_HUMIDITY: typing.Final = _ATTR_MAX_HUMIDITY
    ATTR_MIN_HUMIDITY: typing.Final = _ATTR_MIN_HUMIDITY

    DEFAULT_MIN_HUMIDITY: typing.Final = _DEFAULT_MIN_HUMIDITY
    DEFAULT_MAX_HUMIDITY: typing.Final = _DEFAULT_MAX_HUMIDITY

    SERVICE_SET_MODE: typing.Final = _SERVICE_SET_MODE
    SERVICE_SET_HUMIDITY: typing.Final = _SERVICE_SET_HUMIDITY

    DeviceClass: typing.TypeAlias = _DeviceClass

    Entity: typing.TypeAlias = _Entity
    EntityDescription: typing.TypeAlias = _EntityDescription
    EntityFeature: typing.TypeAlias = _EntityFeature
