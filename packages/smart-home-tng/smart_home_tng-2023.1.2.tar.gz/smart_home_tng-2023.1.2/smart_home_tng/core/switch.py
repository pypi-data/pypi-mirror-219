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
from .toggle import Toggle

_MIN_TIME_BETWEEN_SCANS: typing.Final = dt.timedelta(seconds=10)


class _DeviceClass(strenum.LowercaseStrEnum):
    """Device class for switches."""

    OUTLET = enum.auto()
    SWITCH = enum.auto()


_DEVICE_CLASSES_SCHEMA: typing.Final = vol.All(vol.Lower, vol.Coerce(_DeviceClass))


@dataclasses.dataclass
class _EntityDescription(Toggle.EntityDescription):
    """A class that describes switch entities."""

    device_class: _DeviceClass | str = None


class _Entity(Toggle.Entity):
    """Base class for switch entities."""

    _entity_description: _EntityDescription
    _attr_device_class: _DeviceClass | str

    @property
    def entity_description(self) -> _EntityDescription:
        return super().entity_description

    @property
    def device_class(self) -> str:
        """Return the class of this entity."""
        if hasattr(self, "_attr_device_class"):
            return str(self._attr_device_class)
        if (description := self.entity_description) is not None:
            return str(description.device_class)
        return None


# pylint: disable=invalid-name
class Switch:
    """Switch namespace."""

    DeviceClass: typing.TypeAlias = _DeviceClass
    Entity: typing.TypeAlias = _Entity
    EntityDescription: typing.TypeAlias = _EntityDescription

    DEVICE_CLASSES_SCHEMA: typing.Final = _DEVICE_CLASSES_SCHEMA
    MIN_TIME_BETWEEN_SCANS: typing.Final = _MIN_TIME_BETWEEN_SCANS
