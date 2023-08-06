"""
Amazon Alexa MediaPlayer Integration for Smart Home - The Next Generation.

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

This integration is based custom_component "alexa_media_player"
from the Home Assistant Community Store (HACS), which is distributed
under the Terms of the Apache License, Version 2.0

The original source code and license terms can be found under:
https://github.com/custom_components/alexa_media_player
"""

import typing


# pylint: disable=unused-variable
class AlexaDevice:
    """
    Typisch Script-Dummie. Kommt mit den selbst erzeugten Objekten
    nicht zurecht!

    Wrapper über das erzeugte dictionary von AlexaAPI.get_devices,
    um die verwendeten 'Properties' innerhalb von AlexaAPI auch
    bereitzustellen.

    Ohne diesen Wrapper wird ständig eine Exception
    "'dict' object has no attribute 'xxx' erzeugt.
    """

    def __init__(self, device: dict[str, typing.Any]):
        self._device = device

    def __getitem__(self, name: str):
        if name.startswith("_"):
            name = name[1:]
        return self._device[name]

    def __getattr__(self, attr: str):
        attrib = attr
        if attr.startswith("_"):
            attrib = attr[1:]
        if attrib == "device_serial_number":
            attrib = "serialNumber"
        elif attrib == "device_type":
            attrib = "deviceType"
        elif attrib == "device_family":
            attrib = "deviceFamily"
        result = self._device[attrib]
        setattr(self, attr, result)
        return result

    def get(self, name: str, default=None):
        return self._device.get(name, default)
