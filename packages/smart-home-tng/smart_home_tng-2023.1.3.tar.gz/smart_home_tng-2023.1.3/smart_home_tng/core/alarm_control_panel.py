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

_ATTR_CHANGED_BY: typing.Final = "changed_by"
_ATTR_CODE_ARM_REQUIRED: typing.Final = "code_arm_required"


class _CodeFormat(strenum.LowercaseStrEnum):
    """Code formats for the Alarm Control Panel."""

    TEXT = enum.auto()
    NUMBER = enum.auto()


class _EntityFeature(enum.IntEnum):
    """Supported features of the alarm control panel entity."""

    ARM_HOME = 1
    ARM_AWAY = 2
    ARM_NIGHT = 4
    TRIGGER = 8
    ARM_CUSTOM_BYPASS = 16
    ARM_VACATION = 32


@dataclasses.dataclass
class _EntityDescription(EntityDescription):
    """A class that describes alarm control panel entities."""


class _Entity(Entity):
    """An abstract class for alarm control entities."""

    _entity_description: _EntityDescription
    _attr_changed_by: str = None
    _attr_code_arm_required: bool = True
    _attr_code_format: _CodeFormat = None
    _attr_supported_features: int

    @property
    def entity_description(self) -> _EntityDescription:
        return super().entity_description

    @property
    def code_format(self) -> _CodeFormat:
        """Code format or None if no code is required."""
        return self._attr_code_format

    @property
    def changed_by(self) -> str:
        """Last change triggered by."""
        return self._attr_changed_by

    @property
    def code_arm_required(self) -> bool:
        """Whether the code is required for arm actions."""
        return self._attr_code_arm_required

    def alarm_disarm(self, code: str = None) -> None:
        """Send disarm command."""
        raise NotImplementedError()

    async def async_alarm_disarm(self, code: str = None) -> None:
        """Send disarm command."""
        await self._shc.async_add_executor_job(self.alarm_disarm, code)

    def alarm_arm_home(self, code: str = None) -> None:
        """Send arm home command."""
        raise NotImplementedError()

    async def async_alarm_arm_home(self, code: str = None) -> None:
        """Send arm home command."""
        await self._shc.async_add_executor_job(self.alarm_arm_home, code)

    def alarm_arm_away(self, code: str = None) -> None:
        """Send arm away command."""
        raise NotImplementedError()

    async def async_alarm_arm_away(self, code: str = None) -> None:
        """Send arm away command."""
        await self._shc.async_add_executor_job(self.alarm_arm_away, code)

    def alarm_arm_night(self, code: str = None) -> None:
        """Send arm night command."""
        raise NotImplementedError()

    async def async_alarm_arm_night(self, code: str = None) -> None:
        """Send arm night command."""
        await self._shc.async_add_executor_job(self.alarm_arm_night, code)

    def alarm_arm_vacation(self, code: str = None) -> None:
        """Send arm vacation command."""
        raise NotImplementedError()

    async def async_alarm_arm_vacation(self, code: str = None) -> None:
        """Send arm vacation command."""
        await self._shc.async_add_executor_job(self.alarm_arm_vacation, code)

    def alarm_trigger(self, code: str = None) -> None:
        """Send alarm trigger command."""
        raise NotImplementedError()

    async def async_alarm_trigger(self, code: str = None) -> None:
        """Send alarm trigger command."""
        await self._shc.async_add_executor_job(self.alarm_trigger, code)

    def alarm_arm_custom_bypass(self, code: str = None) -> None:
        """Send arm custom bypass command."""
        raise NotImplementedError()

    async def async_alarm_arm_custom_bypass(self, code: str = None) -> None:
        """Send arm custom bypass command."""
        await self._shc.async_add_executor_job(self.alarm_arm_custom_bypass, code)

    @property
    def supported_features(self) -> int:
        """Return the list of supported features."""
        return self._attr_supported_features

    @typing.final
    @property
    def state_attributes(self) -> dict[str, typing.Any]:
        """Return the state attributes."""
        return {
            Const.ATTR_CODE_FORMAT: self.code_format,
            _ATTR_CHANGED_BY: self.changed_by,
            _ATTR_CODE_ARM_REQUIRED: self.code_arm_required,
        }


# pylint: disable=invalid-name
class AlarmControlPanel:
    """Namespace for Alarm Control Panel objects."""

    ATTR_CHANGED_BY: typing.Final = _ATTR_CHANGED_BY
    ATTR_CODE_ARM_REQUIRED: typing.Final = _ATTR_CODE_ARM_REQUIRED

    CodeFormat: typing.TypeAlias = _CodeFormat
    Entity: typing.TypeAlias = _Entity
    EntityDescription: typing.TypeAlias = _EntityDescription
    EntityFeature: typing.TypeAlias = _EntityFeature
