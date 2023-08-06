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

import asyncio
import logging
import typing

from .base_tracker_entity import BaseTrackerEntity
from .callback import callback
from .const import Const
from .device import Device
from .device_info import DeviceInfo
from .device_tracker_component import DeviceTrackerComponent
from .entity_platform import EntityPlatform
from .state_type import StateType

_LOGGER: typing.Final = logging.getLogger(__name__)

if not typing.TYPE_CHECKING:

    class SmartHomeController:
        ...


if typing.TYPE_CHECKING:
    from .smart_home_controller import SmartHomeController


# pylint: disable=unused-variable
class ScannerEntity(BaseTrackerEntity):
    """Base class for a tracked device that is on a scanned network."""

    @property
    def ip_address(self) -> str:
        """Return the primary ip address of the device."""
        return None

    @property
    def mac_address(self) -> str:
        """Return the mac address of the device."""
        return None

    @property
    def hostname(self) -> str:
        """Return hostname of the device."""
        return None

    @property
    def state(self) -> str:
        """Return the state of the device."""
        if self.is_connected:
            return Const.STATE_HOME
        return Const.STATE_NOT_HOME

    @property
    def is_connected(self) -> bool:
        """Return true if the device is connected to the network."""
        raise NotImplementedError()

    @property
    def unique_id(self) -> str:
        """Return unique ID of the entity."""
        return self.mac_address

    @typing.final
    @property
    def device_info(self) -> DeviceInfo:
        """Device tracker entities should not create device registry entries."""
        return None

    @property
    def entity_registry_enabled_default(self) -> bool:
        """Return if entity is enabled by default."""
        # If mac_address is None, we can never find a device entry.
        return (
            # Do not disable if we won't activate our attach to device logic
            self.mac_address is None
            or self.device_info is not None
            # Disable if we automatically attach but there is no device
            or self.find_device_entry() is not None
        )

    @callback
    def add_to_platform_start(
        self,
        shc: SmartHomeController,
        platform: EntityPlatform,
        parallel_updates: asyncio.Semaphore,
    ) -> None:
        """Start adding an entity to a platform."""
        super().add_to_platform_start(shc, platform, parallel_updates)
        if self.mac_address and self.unique_id:
            _async_register_mac(
                shc,
                platform.platform_name,
                self.mac_address,
                self.unique_id,
            )
            if self.is_connected:
                _async_connected_device_registered(
                    shc,
                    self.mac_address,
                    self.ip_address,
                    self.hostname,
                )

    @callback
    def find_device_entry(self) -> Device:
        """Return device entry."""
        assert self.mac_address is not None

        dr = self._shc.device_registry
        return dr.async_get_device(set(), {(dr.ConnectionType.MAC, self.mac_address)})

    async def async_internal_added_to_shc(self) -> None:
        """Handle added to Smart Home - The Next Generation."""
        # Entities without a unique ID don't have a device
        if (
            not self.registry_entry
            or not self.platform
            or not self.platform.config_entry
            or not self.mac_address
            or (device_entry := self.find_device_entry()) is None
            # Entities should not have a device info. We opt them out
            # of this logic if they do.
            or self.device_info
        ):
            if self.device_info:
                _LOGGER.debug(f"Entity {self.entity_id} unexpectedly has a device info")
            await super().async_internal_added_to_shc()
            return

        # Attach entry to device
        if self.registry_entry.device_id != device_entry.id:
            er = self._shc.entity_registry
            self._registry_entry = er.async_update_entity(
                self.entity_id, device_id=device_entry.id
            )

        # Attach device to config entry
        if self.platform.config_entry.entry_id not in device_entry.config_entries:
            dr = self._shc.device_registry
            dr.async_update_device(
                device_entry.id,
                add_config_entry_id=self.platform.config_entry.entry_id,
            )

        # Do this last or else the entity registry update listener has been installed
        await super().async_internal_added_to_shc()

    @typing.final
    @property
    def state_attributes(self) -> dict[str, StateType]:
        """Return the device state attributes."""
        attr: dict[str, StateType] = {}
        attr.update(super().state_attributes)
        if self.ip_address is not None:
            attr[Const.ATTR_IP] = self.ip_address
        if self.mac_address is not None:
            attr[Const.ATTR_MAC] = self.mac_address
        if self.hostname is not None:
            attr[Const.ATTR_HOST_NAME] = self.hostname

        return attr


@callback
def _async_register_mac(
    shc: SmartHomeController,
    domain: str,
    mac: str,
    unique_id: str,
) -> None:
    """Register a mac address with a unique ID."""
    device_tracker = shc.components.device_tracker
    if not isinstance(device_tracker, DeviceTrackerComponent):
        return

    device_tracker.register_mac(domain, mac, unique_id)


@callback
def _async_connected_device_registered(
    shc: SmartHomeController, mac: str, ip_address: str, hostname: str
) -> None:
    """Register a newly seen connected device.

    This is currently used by the dhcp integration
    to listen for newly registered connected devices
    for discovery.
    """
    device_tracker = shc.components.device_tracke
    if not isinstance(device_tracker, DeviceTrackerComponent):
        return

    device_tracker.connected_device_registered(mac, ip_address, hostname)
