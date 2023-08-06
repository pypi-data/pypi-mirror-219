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

import datetime as dt
import logging
import typing

from ... import core
from .avm_wrapper import AvmWrapper
from .fritz_data import FritzData
from .fritz_device import FritzDevice
from .fritz_device_base import FritzDeviceBase

if not typing.TYPE_CHECKING:

    class FritzboxToolsIntegration:
        pass


if typing.TYPE_CHECKING:
    from .fritzbox_tools_integration import FritzboxToolsIntegration


_LOGGER: typing.Final = logging.getLogger(__name__)


class FritzboxTracker(FritzDeviceBase, core.ScannerEntity):
    """This class queries a FRITZ!Box device."""

    def __init__(self, avm_wrapper: AvmWrapper, device: FritzDevice) -> None:
        """Initialize a FRITZ!Box device."""
        super().__init__(avm_wrapper, device)
        self._last_activity: dt.datetime = device.last_activity

    @property
    def is_connected(self) -> bool:
        """Return device status."""
        return self._avm_wrapper.devices[self._mac].is_connected

    @property
    def unique_id(self) -> str:
        """Return device unique id."""
        return f"{self._mac}_tracker"

    @property
    def mac_address(self) -> str:
        """Return mac_address."""
        return self._mac

    @property
    def icon(self) -> str:
        """Return device icon."""
        if self.is_connected:
            return "mdi:lan-connect"
        return "mdi:lan-disconnect"

    @property
    def extra_state_attributes(self) -> dict[str, str]:
        """Return the attributes."""
        attrs: dict[str, str] = {}
        device = self._avm_wrapper.devices[self._mac]
        self._last_activity = device.last_activity
        if self._last_activity is not None:
            attrs["last_time_reachable"] = self._last_activity.isoformat(
                timespec="seconds"
            )
        if device.connected_to:
            attrs["connected_to"] = device.connected_to
        if device.connection_type:
            attrs["connection_type"] = device.connection_type
        if device.ssid:
            attrs["ssid"] = device.ssid
        return attrs

    @property
    def source_type(self) -> core.DeviceTracker.SourceType:
        """Return tracker source type."""
        return core.DeviceTracker.SourceType.ROUTER


def _async_add_entities(
    avm_wrapper: AvmWrapper,
    async_add_entities: core.AddEntitiesCallback,
    data_fritz: FritzData,
) -> None:
    """Add new tracker entities from the AVM device."""

    new_tracked = []
    if avm_wrapper.unique_id not in data_fritz.tracked:
        data_fritz.tracked[avm_wrapper.unique_id] = set()

    for mac, device in avm_wrapper.devices.items():
        if _device_filter_out_from_trackers(mac, device, data_fritz.tracked.values()):
            continue

        new_tracked.append(FritzboxTracker(avm_wrapper, device))
        data_fritz.tracked[avm_wrapper.unique_id].add(mac)

    if new_tracked:
        async_add_entities(new_tracked)


def _device_filter_out_from_trackers(
    mac: str,
    device: FritzDevice,
    current_devices: typing.ValuesView,
) -> bool:
    """Check if device should be filtered out from trackers."""
    reason: str = None
    if device.ip_address == "":
        reason = "Missing IP"
    elif _is_tracked(mac, current_devices):
        reason = "Already tracked"

    if reason:
        _LOGGER.debug(f"Skip adding device {device.hostname} [{mac}], reason: {reason}")
    return bool(reason)


def _is_tracked(mac: str, current_devices: typing.ValuesView) -> bool:
    """Check if device is already tracked."""
    for tracked in current_devices:
        if mac in tracked:
            return True
    return False


# pylint: disable=unused-variable
async def async_setup_device_trackers(
    owner: FritzboxToolsIntegration,
    entry: core.ConfigEntry,
    async_add_entities: core.AddEntitiesCallback,
) -> None:
    """Set up device tracker for FRITZ!Box component."""
    _LOGGER.debug("Starting FRITZ!Box device tracker")
    avm_wrapper = owner.wrappers[entry.entry_id]
    data_fritz = owner.data

    @core.callback
    def update_avm_device() -> None:
        """Update the values of AVM device."""
        _async_add_entities(avm_wrapper, async_add_entities, data_fritz)

    entry.async_on_unload(
        owner.controller.dispatcher.async_connect(
            avm_wrapper.signal_device_new, update_avm_device
        )
    )

    update_avm_device()
