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
import typing

from .entity import Entity
from .entity_description import EntityDescription

_ATTR_OPTIONS: typing.Final = "options"
_ATTR_OPTION: typing.Final = "option"

_CONF_OPTION: typing.Final = _ATTR_OPTION

_SERVICE_SELECT_OPTION: typing.Final = "select_option"


@dataclasses.dataclass()
class _EntityDescription(EntityDescription):
    """A class that describes select entities."""


class _Entity(Entity):
    """Representation of a Select entity."""

    _entity_description: _EntityDescription
    _attr_current_option: str
    _attr_options: list[str]
    _attr_state: None = None

    @property
    def entity_description(self) -> _EntityDescription:
        return super().entity_description

    @property
    def capability_attributes(self) -> dict[str, typing.Any]:
        """Return capability attributes."""
        return {
            _ATTR_OPTIONS: self.options,
        }

    @property
    @typing.final
    def state(self) -> str:
        """Return the entity state."""
        if self.current_option is None or self.current_option not in self.options:
            return None
        return self.current_option

    @property
    def options(self) -> list[str]:
        """Return a set of selectable options."""
        return self._attr_options

    @property
    def current_option(self) -> str:
        """Return the selected entity option to represent the entity state."""
        return self._attr_current_option

    # pylint: disable=unused-argument
    def select_option(self, option: str) -> None:
        """Change the selected option."""
        raise NotImplementedError()

    async def async_select_option(self, option: str) -> None:
        """Change the selected option."""
        await self._shc.async_add_executor_job(self.select_option, option)


# pylint: disable=invalid-name
class Select:
    """Select namespace."""

    ATTR_OPTIONS: typing.Final = _ATTR_OPTIONS
    ATTR_OPTION: typing.Final = _ATTR_OPTION

    CONF_OPTION: typing.Final = _CONF_OPTION

    SERVICE_SELECT_OPTION: typing.Final = _SERVICE_SELECT_OPTION

    Entity: typing.TypeAlias = _Entity
    EntityDescription: typing.Final = _EntityDescription
