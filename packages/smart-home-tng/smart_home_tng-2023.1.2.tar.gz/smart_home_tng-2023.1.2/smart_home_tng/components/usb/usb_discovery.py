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

# pylint: disable=unused-variable

import dataclasses
import fnmatch
import logging
import sys
import typing

import pyudev
from serial.tools import list_ports as serial_lp
from serial.tools import list_ports_common as serial_lpc

from ... import core
from .usb_device import USBDevice

_LOGGER: typing.Final = logging.getLogger(__name__)
_REQUEST_SCAN_COOLDOWN: typing.Final = 60  # 1 minute cooldown


# pylint: disable=unused-variable
class USBDiscovery:
    """Manage USB Discovery."""

    def __init__(
        self,
        shc: core.SmartHomeController,
        usb: list[dict[str, str]],
    ) -> None:
        """Init USB Discovery."""
        self._shc = shc
        self._usb = usb
        self._seen: set[tuple[str, ...]] = set()
        self._observer_active = False
        self._request_debouncer: core.Debouncer = None

    @property
    def observer_active(self) -> bool:
        return self._observer_active

    async def async_setup(self) -> None:
        """Set up USB Discovery."""
        await self._async_start_monitor()
        self._shc.bus.async_listen_once(core.Const.EVENT_SHC_STARTED, self._async_start)

    async def _async_start(self, _event: core.Event) -> None:
        """Start USB Discovery and run a manual scan."""
        await self._async_scan_serial()

    async def _async_start_monitor(self) -> None:
        """Start monitoring hardware with pyudev."""
        if not sys.platform.startswith("linux"):
            return
        info = await core.helpers.async_get_system_info(self._shc)
        if info.get("docker"):
            return

        try:
            context = pyudev.Context()
        except (ImportError, OSError):
            return

        monitor = pyudev.Monitor.from_netlink(context)
        try:
            monitor.filter_by(subsystem="tty")
        except ValueError as ex:  # this fails on WSL
            _LOGGER.debug(
                f"Unable to setup pyudev filtering; This is expected on WSL: {ex}"
            )
            return
        observer = pyudev.MonitorObserver(
            monitor, callback=self._device_discovered, name="usb-observer"
        )
        observer.start()

        def _stop_observer(_event: core.Event) -> None:
            observer.stop()

        self._shc.bus.async_listen_once(core.Const.EVENT_SHC_STOP, _stop_observer)
        self._observer_active = True

    def _device_discovered(self, device: pyudev.Device) -> None:
        """Call when the observer discovers a new usb tty device."""
        if device.action != "add":
            return
        _LOGGER.debug(
            f"Discovered Device at path: {device.device_path}, triggering scan serial",
        )
        self._scan_serial()

    @core.callback
    def _async_process_discovered_usb_device(self, device: USBDevice) -> None:
        """Process a USB discovery."""
        _LOGGER.debug(f"Discovered USB Device: {device}")
        device_tuple = dataclasses.astuple(device)
        if device_tuple in self._seen:
            return
        self._seen.add(device_tuple)
        matched = []
        for matcher in self._usb:
            if "vid" in matcher and device.vid != matcher["vid"]:
                continue
            if "pid" in matcher and device.pid != matcher["pid"]:
                continue
            if "serial_number" in matcher and not _fnmatch_lower(
                device.serial_number, matcher["serial_number"]
            ):
                continue
            if "manufacturer" in matcher and not _fnmatch_lower(
                device.manufacturer, matcher["manufacturer"]
            ):
                continue
            if "description" in matcher and not _fnmatch_lower(
                device.description, matcher["description"]
            ):
                continue
            matched.append(matcher)

        if not matched:
            return

        sorted_by_most_targeted = sorted(matched, key=lambda item: -len(item))
        most_matched_fields = len(sorted_by_most_targeted[0])

        for matcher in sorted_by_most_targeted:
            # If there is a less targeted match, we only
            # want the most targeted match
            if len(matcher) < most_matched_fields:
                break

            self._shc.flow_dispatcher.create_flow(
                matcher["domain"],
                {"source": core.ConfigEntrySource.USB},
                core.UsbServiceInfo(
                    device=device.device,
                    vid=device.vid,
                    pid=device.pid,
                    serial_number=device.serial_number,
                    manufacturer=device.manufacturer,
                    description=device.description,
                ),
            )

    @core.callback
    def _async_process_ports(self, ports: list[serial_lpc.ListPortInfo]) -> None:
        """Process each discovered port."""
        for port in ports:
            if port.vid is None and port.pid is None:
                continue
            self._async_process_discovered_usb_device(usb_device_from_port(port))

    def _scan_serial(self) -> None:
        """Scan serial ports."""
        self._shc.add_job(self._async_process_ports, serial_lp.comports())

    async def _async_scan_serial(self) -> None:
        """Scan serial ports."""
        self._async_process_ports(
            await self._shc.async_add_executor_job(serial_lp.comports)
        )

    async def async_request_scan_serial(self) -> None:
        """Request a serial scan."""
        if not self._request_debouncer:
            self._request_debouncer = core.Debouncer(
                self._shc,
                _LOGGER,
                cooldown=_REQUEST_SCAN_COOLDOWN,
                immediate=True,
                function=self._async_scan_serial,
            )
        await self._request_debouncer.async_call()


def _fnmatch_lower(name: str | None, pattern: str) -> bool:
    """Match a lowercase version of the name."""
    if name is None:
        return False
    return fnmatch.fnmatch(name.lower(), pattern)


def usb_device_from_port(port: serial_lpc.ListPortInfo) -> USBDevice:
    """Convert serial ListPortInfo to USBDevice."""
    return USBDevice(
        device=port.device,
        vid=f"{hex(port.vid)[2:]:0>4}".upper(),
        pid=f"{hex(port.pid)[2:]:0>4}".upper(),
        serial_number=port.serial_number,
        manufacturer=port.manufacturer,
        description=port.description,
    )
