"""
Network Component for Smart Home - The Next Generation.

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

import voluptuous as vol

from ...core import ConfigValidation as cv


# pylint: disable=unused-variable
class Const:
    """Constants for the Network Component."""

    STORAGE_KEY: typing.Final = "core.network"
    STORAGE_VERSION: typing.Final = 1

    ATTR_ADAPTERS: typing.Final = "adapters"
    ATTR_CONFIGURED_ADAPTERS: typing.Final = "configured_adapters"
    DEFAULT_CONFIGURED_ADAPTERS: typing.Final = list[str]()

    LOOPBACK_TARGET_IP: typing.Final = "127.0.0.1"
    PUBLIC_TARGET_IP: typing.Final = "8.8.8.8"
    IPV4_BROADCAST_ADDR: typing.Final = "255.255.255.255"

    NETWORK_CONFIG_SCHEMA: typing.Final = vol.Schema(
        {
            vol.Optional(
                ATTR_CONFIGURED_ADAPTERS, default=DEFAULT_CONFIGURED_ADAPTERS
            ): vol.Schema(vol.All(cv.ensure_list, [cv.string])),
        }
    )
