"""
Bosch SHC Integration for Smart Home - The Next Generation.

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
import boschshcpy as bosch

from ... import core
from .bosch_entity import BoschEntity

if not typing.TYPE_CHECKING:

    class BoschShcIntegration:
        pass


if typing.TYPE_CHECKING:
    from .bosch_shc_integration import BoschShcIntegration

_switch: typing.TypeAlias = core.Switch


@dataclasses.dataclass
class RequiredKeysMixin:
    """Mixin for SHC switch required keys."""

    on_key: str
    on_value: core.StateType
    should_poll: bool


@dataclasses.dataclass
class _EntityDescription(
    _switch.EntityDescription,
    RequiredKeysMixin,
):
    """Class describing SHC switch entities."""


_SWITCH_TYPES: typing.Final[dict[str, _EntityDescription]] = {
    "smartplug": _EntityDescription(
        key="smartplug",
        device_class=_switch.DeviceClass.OUTLET,
        on_key="state",
        on_value=bosch.SHCSmartPlug.PowerSwitchService.State.ON,
        should_poll=False,
    ),
    "smartplugcompact": _EntityDescription(
        key="smartplugcompact",
        device_class=_switch.DeviceClass.OUTLET,
        on_key="state",
        on_value=bosch.SHCSmartPlugCompact.PowerSwitchService.State.ON,
        should_poll=False,
    ),
    "lightswitch": _EntityDescription(
        key="lightswitch",
        device_class=_switch.DeviceClass.SWITCH,
        on_key="state",
        on_value=bosch.SHCLightSwitch.PowerSwitchService.State.ON,
        should_poll=False,
    ),
    "cameraeyes": _EntityDescription(
        key="cameraeyes",
        device_class=_switch.DeviceClass.SWITCH,
        on_key="cameralight",
        on_value=bosch.SHCCameraEyes.CameraLightService.State.ON,
        should_poll=True,
    ),
    "camera360": _EntityDescription(
        key="camera360",
        device_class=_switch.DeviceClass.SWITCH,
        on_key="privacymode",
        on_value=bosch.SHCCamera360.PrivacyModeService.State.DISABLED,
        should_poll=True,
    ),
}


class _Entity(BoschEntity, _switch.Entity):
    """Representation of a SHC switch."""

    _entity_description: _EntityDescription

    def __init__(
        self,
        owner: BoschShcIntegration,
        device: bosch.SHCDevice,
        parent_id: str,
        entry_id: str,
        description: _EntityDescription,
    ) -> None:
        """Initialize a SHC switch."""
        super().__init__(owner, device, parent_id, entry_id)
        self._entity_description = description

    @property
    def entity_description(self) -> _EntityDescription:
        return super().entity_description

    @property
    def is_on(self) -> bool:
        """Return the state of the switch."""
        return (
            getattr(self._device, self.entity_description.on_key)
            == self.entity_description.on_value
        )

    def turn_on(self, **kwargs) -> None:
        """Turn the switch on."""
        setattr(self._device, self.entity_description.on_key, True)

    def turn_off(self, **kwargs) -> None:
        """Turn the switch off."""
        setattr(self._device, self.entity_description.on_key, False)

    @property
    def should_poll(self) -> bool:
        """Switch needs polling."""
        return self.entity_description.should_poll

    def update(self) -> None:
        """Trigger an update of the device."""
        self._device.update()


class _RoutingEntity(BoschEntity, _switch.Entity):
    """Representation of a SHC routing switch."""

    _attr_icon = "mdi:wifi"
    _attr_entity_category = core.EntityCategory.CONFIG

    def __init__(
        self,
        owner: BoschShcIntegration,
        device: bosch.SHCDevice,
        parent_id: str,
        entry_id: str,
    ) -> None:
        """Initialize an SHC communication quality reporting sensor."""
        super().__init__(owner, device, parent_id, entry_id)
        self._attr_name = f"{device.name} Routing"
        self._attr_unique_id = f"{device.serial}_routing"

    @property
    def is_on(self) -> bool:
        """Return the state of the switch."""
        return self._device.routing.name == "ENABLED"

    def turn_on(self, **kwargs) -> None:
        """Turn the switch on."""
        self._device.routing = True

    def turn_off(self, **kwargs) -> None:
        """Turn the switch off."""
        self._device.routing = False


# pylint: disable=invalid-name
class BoschSwitch:
    """BoschSwitch namespace."""

    Entity: typing.TypeAlias = _Entity
    EntityDescription: typing.TypeAlias = _EntityDescription

    RoutingEntity: typing.TypeAlias = _RoutingEntity


# pylint: disable=unused-variable
async def _async_setup_switches(
    owner: BoschShcIntegration,
    session: bosch.SHCSession,
    config_entry: core.ConfigEntry,
) -> typing.Iterable[core.Entity]:
    """Set up the SHC switch platform."""
    entities: list[_switch.Entity] = []

    for switch in session.device_helper.smart_plugs:
        entities.append(
            BoschSwitch.Entity(
                owner,
                device=switch,
                parent_id=session.information.unique_id,
                entry_id=config_entry.entry_id,
                description=_SWITCH_TYPES["smartplug"],
            )
        )
        entities.append(
            BoschSwitch.RoutingEntity(
                owner,
                device=switch,
                parent_id=session.information.unique_id,
                entry_id=config_entry.entry_id,
            )
        )

    for switch in session.device_helper.light_switches_bsm:
        entities.append(
            BoschSwitch.Entity(
                owner,
                device=switch,
                parent_id=session.information.unique_id,
                entry_id=config_entry.entry_id,
                description=_SWITCH_TYPES["lightswitch"],
            )
        )

    for switch in session.device_helper.smart_plugs_compact:
        entities.append(
            BoschSwitch.Entity(
                owner,
                device=switch,
                parent_id=session.information.unique_id,
                entry_id=config_entry.entry_id,
                description=_SWITCH_TYPES["smartplugcompact"],
            )
        )

    for switch in session.device_helper.camera_eyes:
        entities.append(
            BoschSwitch.Entity(
                owner,
                device=switch,
                parent_id=session.information.unique_id,
                entry_id=config_entry.entry_id,
                description=_SWITCH_TYPES["cameraeyes"],
            )
        )

    for switch in session.device_helper.camera_360:
        entities.append(
            BoschSwitch.Entity(
                owner,
                device=switch,
                parent_id=session.information.unique_id,
                entry_id=config_entry.entry_id,
                description=_SWITCH_TYPES["camera360"],
            )
        )
    return entities
