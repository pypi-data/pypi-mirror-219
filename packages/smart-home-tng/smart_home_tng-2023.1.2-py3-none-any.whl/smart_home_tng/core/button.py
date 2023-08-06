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
from . import helpers
from .entity_description import EntityDescription
from .restore_entity import RestoreEntity

_SERVICE_PRESS: typing.Final = "press"
_SCAN_INTERVAL: typing.Final = dt.timedelta(seconds=30)
_MIN_TIME_BETWEEN_SCANS = dt.timedelta(seconds=10)


class _DeviceClass(strenum.LowercaseStrEnum):
    """Device class for buttons."""

    RESTART = enum.auto()
    UPDATE = enum.auto()


_DEVICE_CLASSES_SCHEMA: typing.Final = vol.All(vol.Lower, vol.Coerce(_DeviceClass))


@dataclasses.dataclass()
class _EntityDescription(EntityDescription):
    """A class that describes button entities."""

    device_class: _DeviceClass = None


class _Entity(RestoreEntity):
    """Representation of a Button entity."""

    _entity_description: _EntityDescription
    _attr_should_poll = False
    _attr_device_class: _DeviceClass
    _attr_state: None = None
    _last_pressed: dt.datetime = None

    @property
    def entity_description(self) -> _EntityDescription:
        return super().entity_description

    @property
    def device_class(self) -> str:
        """Return the class of this entity."""
        if hasattr(self, "_attr_device_class"):
            return str(self._attr_device_class)
        if hasattr(self, "_entity_description"):
            return str(self.entity_description.device_class)
        return None

    @property
    @typing.final
    def state(self) -> str:
        """Return the entity state."""
        if self._last_pressed is None:
            return None
        return self._last_pressed.isoformat()

    @typing.final
    async def _async_press_action(self) -> None:
        """Press the button (from e.g., service call).

        Should not be overridden, handle setting last press timestamp.
        """
        self._last_pressed = helpers.utcnow()
        self.async_write_state()
        await self.async_press()

    async def async_internal_added_to_shc(self) -> None:
        """Call when the button is added to hass."""
        await super().async_internal_added_to_shc()
        state = await self.async_get_last_state()
        if state is not None and state.state is not None:
            self._last_pressed = helpers.parse_datetime(state.state)

    def press(self) -> None:
        """Press the button."""
        raise NotImplementedError()

    async def async_press(self) -> None:
        """Press the button."""
        await self._shc.async_add_executor_job(self.press)


# pylint: disable=invalid-name
class Button:
    """Button namespace."""

    DeviceClass: typing.TypeAlias = _DeviceClass
    Entity: typing.TypeAlias = _Entity
    EntityDescription: typing.TypeAlias = _EntityDescription

    MIN_TIME_BETWEEN_SCANS: typing.Final = _MIN_TIME_BETWEEN_SCANS
    SCAN_INTERVAL: typing.Final = _SCAN_INTERVAL
    SERVICE_PRESS: typing.Final = _SERVICE_PRESS
    DEVICE_CLASSES_SCHEMA: typing.Final = _DEVICE_CLASSES_SCHEMA
