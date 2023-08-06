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

import typing

import boschshcpy as bosch

from ... import core

if not typing.TYPE_CHECKING:

    class BoschShcIntegration:
        pass


if typing.TYPE_CHECKING:
    from .bosch_shc_integration import BoschShcIntegration


# pylint: disable=unused-variable
class BoschEntity(core.Entity):
    """Representation of a SHC base entity."""

    def __init__(
        self,
        owner: BoschShcIntegration,
        device: bosch.SHCDevice,
        parent_id: str,
        entry_id: str,
    ) -> None:
        """Initialize the generic SHC device."""
        self._device = device
        self._parent_id = parent_id
        self._entry_id = entry_id
        self._attr_name = f"{device.name}"
        self._attr_unique_id = f"{device.serial}"
        self._owner = owner

    async def async_added_to_shc(self):
        """Subscribe to SHC events."""
        await super().async_added_to_shc()

        def on_state_changed():
            self.schedule_update_state()

        def update_entity_information():
            if self._device.deleted:
                self._shc.add_job(
                    self._owner.async_remove_devices(self, self._entry_id)
                )
            else:
                self.schedule_update_state()

        for service in self._device.device_services:
            service.subscribe_callback(self.entity_id, on_state_changed)
        self._device.subscribe_callback(self.entity_id, update_entity_information)

    async def async_will_remove_from_shc(self):
        """Unsubscribe from SHC events."""
        await super().async_will_remove_from_shc()
        for service in self._device.device_services:
            service.unsubscribe_callback(self.entity_id)
        self._device.unsubscribe_callback(self.entity_id)

    @property
    def device_name(self):
        """Name of the device."""
        return self._device.name

    @property
    def device_id(self):
        """Device id of the entity."""
        return self._device.id

    @property
    def device_info(self):
        """Return the device info."""
        return {
            "identifiers": {(self._owner.domain, self._device.id)},
            "name": self.device_name,
            "manufacturer": self._device.manufacturer,
            "model": self._device.device_model,
            "via_device": (
                self._owner.domain,
                self._device.parent_device_id
                if self._device.parent_device_id is not None
                else self._parent_id,
            ),
        }

    @property
    def available(self):
        """Return false if status is unavailable."""
        return self._device.status == "AVAILABLE"

    @property
    def should_poll(self):
        """Report polling mode. SHC Entity is communicating via long polling."""
        return False
