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

import abc

from .smart_home_controller_component import SmartHomeControllerComponent


# pylint: disable=unused-variable
class UsbComponent(SmartHomeControllerComponent):
    """Required base class for the USB Component."""

    @abc.abstractmethod
    def get_serial_by_id(self, dev_path: str) -> str:
        """Return a /dev/serial/by-id match for given device if available."""

    @abc.abstractmethod
    def human_readable_device_name(
        device: str,
        serial_number: str,
        manufacturer: str,
        description: str,
        vid: str,
        pid: str,
    ) -> str:
        """Return a human readable name from USBDevice attributes."""
