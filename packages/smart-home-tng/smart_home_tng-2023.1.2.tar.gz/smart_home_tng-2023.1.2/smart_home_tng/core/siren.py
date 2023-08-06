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

from .config_validation import ConfigValidation as _cv
from .toggle import Toggle

_ATTR_TONE: typing.Final = "tone"
_ATTR_AVAILABLE_TONES: typing.Final = "available_tones"
_ATTR_DURATION: typing.Final = "duration"
_ATTR_VOLUME_LEVEL: typing.Final = "volume_level"
_SCAN_INTERVAL: typing.Final = dt.timedelta(seconds=60)
_TURN_ON_SCHEMA: typing.Final = {
    vol.Optional(_ATTR_TONE): vol.Any(vol.Coerce(int), _cv.string),
    vol.Optional(_ATTR_DURATION): _cv.positive_int,
    vol.Optional(_ATTR_VOLUME_LEVEL): _cv.small_float,
}


class _EntityFeature(enum.IntEnum):
    """Supported features of the siren entity."""

    TURN_ON = 1
    TURN_OFF = 2
    TONES = 4
    VOLUME_SET = 8
    DURATION = 16


class _TurnOnServiceParameters(typing.TypedDict, total=False):
    """Represent possible parameters to siren.turn_on service data dict type."""

    tone: int | str
    duration: int
    volume_level: float


@dataclasses.dataclass
class _EntityDescription(Toggle.EntityDescription):
    """A class that describes siren entities."""

    available_tones: list[int | str] | dict[int, str] = None


class _Entity(Toggle.Entity):
    """Representation of a siren device."""

    _entity_description: _EntityDescription
    _attr_available_tones: list[int | str] | dict[int, str]

    @property
    def entity_description(self) -> _EntityDescription:
        return super().entity_description

    @typing.final
    @property
    def capability_attributes(self) -> dict[str, typing.Any]:
        """Return capability attributes."""
        supported_features = self.supported_features or 0

        if (
            supported_features & _EntityFeature.TONES
            and self.available_tones is not None
        ):
            return {_ATTR_AVAILABLE_TONES: self.available_tones}

        return None

    @property
    def available_tones(self) -> list[int | str] | dict[int, str]:
        """
        Return a list of available tones.

        Requires SirenEntityFeature.TONES.
        """
        if hasattr(self, "_attr_available_tones"):
            return self._attr_available_tones
        if hasattr(self, "_entity_description"):
            return self.entity_description.available_tones
        return None


# pylint: disable=invalid-name
class Siren:
    """Siren namespace."""

    ATTR_TONE: typing.Final = _ATTR_TONE
    ATTR_AVAILABLE_TONES: typing.Final = _ATTR_AVAILABLE_TONES
    ATTR_DURATION: typing.Final = _ATTR_DURATION
    ATTR_VOLUME_LEVEL: typing.Final = _ATTR_VOLUME_LEVEL
    SCAN_INTERVAL: typing.Final = _SCAN_INTERVAL
    TURN_ON_SCHEMA: typing.Final = _TURN_ON_SCHEMA

    Entity: typing.TypeAlias = _Entity
    EntityDescription: typing.TypeAlias = _EntityDescription
    EntityFeature: typing.TypeAlias = _EntityFeature
    TurnOnServiceParameters: typing.TypeAlias = _TurnOnServiceParameters
