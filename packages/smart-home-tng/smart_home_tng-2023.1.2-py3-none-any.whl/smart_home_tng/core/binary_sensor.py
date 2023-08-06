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
import typing

from ..backports import strenum
from .const import Const
from .entity import Entity
from .entity_description import EntityDescription


class _DeviceClass(strenum.LowercaseStrEnum):
    """Device class for binary sensors."""

    # On means low, Off means normal
    BATTERY = enum.auto()

    # On means charging, Off means not charging
    BATTERY_CHARGING = enum.auto()

    # On means carbon monoxide detected, Off means no carbon monoxide (clear)
    CO = enum.auto()

    # On means cold, Off means normal
    COLD = enum.auto()

    # On means connected, Off means disconnected
    CONNECTIVITY = enum.auto()

    # On means open, Off means closed
    DOOR = enum.auto()

    # On means open, Off means closed
    GARAGE_DOOR = enum.auto()

    # On means gas detected, Off means no gas (clear)
    GAS = enum.auto()

    # On means hot, Off means normal
    HEAT = enum.auto()

    # On means light detected, Off means no light
    LIGHT = enum.auto()

    # On means open (unlocked), Off means closed (locked)
    LOCK = enum.auto()

    # On means wet, Off means dry
    MOISTURE = enum.auto()

    # On means motion detected, Off means no motion (clear)
    MOTION = enum.auto()

    # On means moving, Off means not moving (stopped)
    MOVING = enum.auto()

    # On means occupied, Off means not occupied (clear)
    OCCUPANCY = enum.auto()

    # On means open, Off means closed
    OPENING = enum.auto()

    # On means plugged in, Off means unplugged
    PLUG = enum.auto()

    # On means power detected, Off means no power
    POWER = enum.auto()

    # On means home, Off means away
    PRESENCE = enum.auto()

    # On means problem detected, Off means no problem (OK)
    PROBLEM = enum.auto()

    # On means running, Off means not running
    RUNNING = enum.auto()

    # On means unsafe, Off means safe
    SAFETY = enum.auto()

    # On means smoke detected, Off means no smoke (clear)
    SMOKE = enum.auto()

    # On means sound detected, Off means no sound (clear)
    SOUND = enum.auto()

    # On means tampering detected, Off means no tampering (clear)
    TAMPER = enum.auto()

    # On means update available, Off means up-to-date
    UPDATE = enum.auto()

    # On means vibration detected, Off means no vibration
    VIBRATION = enum.auto()

    # On means open, Off means closed
    WINDOW = enum.auto()


@dataclasses.dataclass
class _EntityDescription(EntityDescription):
    """A class that describes binary sensor entities."""

    device_class: _DeviceClass | str = None


class _Entity(Entity):
    """Represent a binary sensor."""

    _entity_description: _EntityDescription
    _attr_device_class: _DeviceClass | str
    _attr_is_on: bool = None
    _attr_state: None = None

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

    @property
    def is_on(self) -> bool:
        """Return true if the binary sensor is on."""
        return self._attr_is_on

    @typing.final
    @property
    def state(self) -> typing.Literal["on", "off"]:
        """Return the state of the binary sensor."""
        if (is_on := self.is_on) is None:
            return None
        return Const.STATE_ON if is_on else Const.STATE_OFF


# pylint: disable=unused-variable, invalid-name
class BinarySensor:
    """Binary Sensor namespace."""

    DeviceClass: typing.TypeAlias = _DeviceClass
    Entity: typing.TypeAlias = _Entity
    EntityDescription: typing.TypeAlias = _EntityDescription
