"""
Rest API for Smart Home - The Next Generation.

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


# pylint: disable=unused-variable
class Const:
    """Constansts for Rest API"""

    ATTR_BASE_URL: typing.Final = "base_url"
    ATTR_EXTERNAL_URL: typing.Final = "external_url"
    ATTR_INTERNAL_URL: typing.Final = "internal_url"
    ATTR_LOCATION_NAME: typing.Final = "location_name"
    ATTR_INSTALLATION_TYPE: typing.Final = "installation_type"
    ATTR_REQUIRES_API_PASSWORD: typing.Final = "requires_api_password"
    ATTR_UUID: typing.Final = "uuid"
    ATTR_VERSION: typing.Final = "version"

    STREAM_PING_PAYLOAD: typing.Final = "ping"
    STREAM_PING_INTERVAL: typing.Final = 50  # seconds
