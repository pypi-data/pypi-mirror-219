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

import collections.abc
import typing

import attr

from . import helpers
from .callback import callback
from .const import Const
from .entity_category import EntityCategory
from .entity_registry_entry_disabler import EntityRegistryEntryDisabler
from .entity_registry_entry_hider import EntityRegistryEntryHider


if not typing.TYPE_CHECKING:

    class SmartHomeController:
        ...


if typing.TYPE_CHECKING:
    from .smart_home_controller import SmartHomeController


# pylint: disable=unused-variable
@attr.s(slots=True, frozen=True)
class EntityRegistryEntry:
    """Entity Registry Entry."""

    entity_id: str = attr.ib()
    unique_id: str = attr.ib()
    platform: str = attr.ib()
    area_id: str = attr.ib(default=None)
    capabilities: collections.abc.Mapping[str, typing.Any] = attr.ib(default=None)
    config_entry_id: str = attr.ib(default=None)
    device_class: str = attr.ib(default=None)
    device_id: str = attr.ib(default=None)
    domain: str = attr.ib(init=False, repr=False)
    disabled_by: EntityRegistryEntryDisabler = attr.ib(default=None)
    entity_category: EntityCategory = attr.ib(default=None)
    hidden_by: EntityRegistryEntryHider = attr.ib(default=None)
    icon: str = attr.ib(default=None)
    id: str = attr.ib(factory=helpers.random_uuid_hex)
    has_entity_name: bool = attr.ib(default=False)
    name: str = attr.ib(default=None)
    options: collections.abc.Mapping[
        str, collections.abc.Mapping[str, typing.Any]
    ] = attr.ib(default=None, converter=attr.converters.default_if_none(factory=dict))
    # As set by integration
    original_device_class: str = attr.ib(default=None)
    original_icon: str = attr.ib(default=None)
    original_name: str = attr.ib(default=None)
    supported_features: int = attr.ib(default=0)
    unit_of_measurement: str = attr.ib(default=None)

    @domain.default
    def _domain_default(self) -> str:
        """Compute domain value."""
        return helpers.split_entity_id(self.entity_id)[0]

    @property
    def disabled(self) -> bool:
        """Return if entry is disabled."""
        return self.disabled_by is not None

    @property
    def hidden(self) -> bool:
        """Return if entry is hidden."""
        return self.hidden_by is not None

    @callback
    def write_unavailable_state(self, shc: SmartHomeController) -> None:
        """Write the unavailable state to the state machine."""
        attrs: dict[str, typing.Any] = {Const.ATTR_RESTORED: True}

        if self.capabilities is not None:
            attrs.update(self.capabilities)

        device_class = self.device_class or self.original_device_class
        if device_class is not None:
            attrs[Const.ATTR_DEVICE_CLASS] = device_class

        icon = self.icon or self.original_icon
        if icon is not None:
            attrs[Const.ATTR_ICON] = icon

        name = self.name or self.original_name
        if name is not None:
            attrs[Const.ATTR_FRIENDLY_NAME] = name

        if self.supported_features is not None:
            attrs[Const.ATTR_SUPPORTED_FEATURES] = self.supported_features

        if self.unit_of_measurement is not None:
            attrs[Const.ATTR_UNIT_OF_MEASUREMENT] = self.unit_of_measurement

        shc.states.async_set(self.entity_id, Const.STATE_UNAVAILABLE, attrs)
