"""
Philips Hue Integration for Smart Home - The Next Generation.

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
    """Constants for the Hue component."""

    CONF_API_VERSION: typing.Final = "api_version"
    CONF_IGNORE_AVAILABILITY: typing.Final = "ignore_availability"

    CONF_SUBTYPE: typing.Final = "subtype"

    ATTR_HUE_EVENT: typing.Final = "hue.event"
    SERVICE_HUE_ACTIVATE_SCENE: typing.Final = "hue.activate_scene"
    ATTR_GROUP_NAME: typing.Final = "group_name"
    ATTR_SCENE_NAME: typing.Final = "scene_name"
    ATTR_TRANSITION: typing.Final = "transition"
    ATTR_DYNAMIC: typing.Final = "dynamic"

    # V1 API SPECIFIC CONSTANTS ##################

    GROUP_TYPE_LIGHT_GROUP: typing.Final = "LightGroup"
    GROUP_TYPE_ROOM: typing.Final = "Room"
    GROUP_TYPE_LUMINAIRE: typing.Final = "Luminaire"
    GROUP_TYPE_LIGHT_SOURCE: typing.Final = "LightSource"
    GROUP_TYPE_ZONE: typing.Final = "Zone"
    GROUP_TYPE_ENTERTAINMENT: typing.Final = "Entertainment"

    CONF_ALLOW_HUE_GROUPS: typing.Final = "allow_hue_groups"
    DEFAULT_ALLOW_HUE_GROUPS: typing.Final = False

    CONF_ALLOW_UNREACHABLE: typing.Final = "allow_unreachable"
    DEFAULT_ALLOW_UNREACHABLE: typing.Final = False

    # How long to wait to actually do the refresh after requesting it.
    # We wait some time so if we control multiple lights, we batch requests.
    REQUEST_REFRESH_DELAY: typing.Final = 0.3
