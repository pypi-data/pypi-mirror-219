"""
USB Discovery Component for Smart Home - The Next Generation.

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

import os
import typing

import voluptuous as vol

from ... import core
from .usb_discovery import USBDiscovery

_USB_SCAN: typing.Final = {vol.Required("type"): "usb/scan"}


# pylint: disable=unused-variable
class UsbComponent(core.UsbComponent):
    """The USB Discovery integration."""

    def __init__(self, path: typing.Iterable[str]):
        super().__init__(path)
        self._usb_discovery: USBDiscovery = None

    async def async_setup(self, config: core.ConfigType) -> bool:
        """Set up the USB Discovery integration."""
        if not await super().async_setup(config):
            return False

        websocket_api = self.controller.components.websocket_api
        if not isinstance(websocket_api, core.WebSocket.Component):
            return False

        usb = await self._shc.setup.async_get_usb()
        usb_discovery = USBDiscovery(self._shc, usb)
        await usb_discovery.async_setup()
        self._usb_discovery = usb_discovery
        websocket_api.register_command(self._usb_scan, _USB_SCAN)

        return True

    async def _usb_scan(
        self,
        connection: core.WebSocket.Connection,
        msg: dict,
    ) -> None:
        """Scan for new usb devices."""
        connection.require_admin()

        usb_discovery = self._usb_discovery
        if not usb_discovery.observer_active:
            await usb_discovery.async_request_scan_serial()
        connection.send_result(msg["id"])

    def get_serial_by_id(self, dev_path: str) -> str:
        """Return a /dev/serial/by-id match for given device if available."""
        by_id = "/dev/serial/by-id"
        if not os.path.isdir(by_id):
            return dev_path

        for path in (entry.path for entry in os.scandir(by_id) if entry.is_symlink()):
            if os.path.realpath(path) == dev_path:
                return path
        return dev_path

    def human_readable_device_name(
        device: str,
        serial_number: str,
        manufacturer: str,
        description: str,
        vid: str,
        pid: str,
    ) -> str:
        """Return a human readable name from USBDevice attributes."""
        device_details = f"{device}, s/n: {serial_number or 'n/a'}"
        manufacturer_details = f" - {manufacturer}" if manufacturer else ""
        vendor_details = f" - {vid}:{pid}" if vid else ""
        full_details = f"{device_details}{manufacturer_details}{vendor_details}"

        if not description:
            return full_details
        return f"{description[:26]} - {full_details}"
