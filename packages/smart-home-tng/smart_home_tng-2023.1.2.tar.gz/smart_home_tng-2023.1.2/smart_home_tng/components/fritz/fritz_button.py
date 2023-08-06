"""
AVM FRITZ!Box Tools Integration for Smart Home - The Next Generation.

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

import logging
import dataclasses
import typing

from ... import core
from .avm_wrapper import AvmWrapper

if not typing.TYPE_CHECKING:

    class FritzboxToolsIntegration:
        pass


if typing.TYPE_CHECKING:
    from .fritzbox_tools_integration import FritzboxToolsIntegration

_LOGGER: typing.Final = logging.getLogger(__name__)


@dataclasses.dataclass
class FritzButtonDescriptionMixin:
    """Mixin to describe a Button entity."""

    press_action: typing.Callable


@dataclasses.dataclass
class FritzButtonDescription(
    core.Button.EntityDescription, FritzButtonDescriptionMixin
):
    """Class to describe a Button entity."""


_BUTTONS: typing.Final = [
    FritzButtonDescription(
        key="firmware_update",
        name="Firmware Update",
        device_class=core.Button.DeviceClass.UPDATE,
        entity_category=core.EntityCategory.CONFIG,
        press_action=lambda avm_wrapper: avm_wrapper.async_trigger_firmware_update(),
    ),
    FritzButtonDescription(
        key="reboot",
        name="Reboot",
        device_class=core.Button.DeviceClass.RESTART,
        entity_category=core.EntityCategory.CONFIG,
        press_action=lambda avm_wrapper: avm_wrapper.async_trigger_reboot(),
    ),
    FritzButtonDescription(
        key="reconnect",
        name="Reconnect",
        device_class=core.Button.DeviceClass.RESTART,
        entity_category=core.EntityCategory.CONFIG,
        press_action=lambda avm_wrapper: avm_wrapper.async_trigger_reconnect(),
    ),
    FritzButtonDescription(
        key="cleanup",
        name="Cleanup",
        icon="mdi:broom",
        entity_category=core.EntityCategory.CONFIG,
        press_action=lambda avm_wrapper: avm_wrapper.async_trigger_cleanup(),
    ),
]


class FritzButton(core.Button.Entity):
    """Defines a Fritz!Box base button."""

    entity_description: FritzButtonDescription

    def __init__(
        self,
        avm_wrapper: AvmWrapper,
        device_friendly_name: str,
        description: FritzButtonDescription,
    ) -> None:
        """Initialize Fritz!Box button."""
        self._entity_description = description
        self._avm_wrapper = avm_wrapper

        self._attr_name = f"{device_friendly_name} {description.name}"
        self._attr_unique_id = f"{avm_wrapper.unique_id}-{description.key}"

        self._attr_device_info = core.DeviceInfo(
            connections={(core.DeviceRegistry.ConnectionType.MAC, avm_wrapper.mac)}
        )

    async def async_press(self) -> None:
        """Triggers Fritz!Box service."""
        await self.entity_description.press_action(self._avm_wrapper)


# pylint: disable=unused-variable
async def async_setup_buttons(
    owner: FritzboxToolsIntegration,
    entry: core.ConfigEntry,
    async_add_entities: core.AddEntitiesCallback,
) -> None:
    """Set buttons for device."""
    _LOGGER.debug("Setting up buttons")
    avm_wrapper: AvmWrapper = owner.wrappers[entry.entry_id]

    async_add_entities(
        [FritzButton(avm_wrapper, entry.title, button) for button in _BUTTONS]
    )
