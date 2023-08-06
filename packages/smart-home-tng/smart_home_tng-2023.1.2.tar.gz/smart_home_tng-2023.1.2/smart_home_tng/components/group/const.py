"""
Group Component for Smart Home - The Next Generation.

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

from ... import core

_cv: typing.TypeAlias = core.ConfigValidation


# pylint: disable=unused-variable
class Const:
    """Constants for the Group Component."""

    GROUP_ORDER: typing.Final = "group_order"
    CONF_ALL: typing.Final = "all"
    CONF_HIDE_MEMBERS: typing.Final = "hide_members"

    ATTR_ADD_ENTITIES: typing.Final = "add_entities"
    ATTR_AUTO: typing.Final = "auto"
    ATTR_ENTITIES: typing.Final = "entities"
    ATTR_OBJECT_ID: typing.Final = "object_id"
    ATTR_ORDER: typing.Final = "order"
    ATTR_ALL: typing.Final = "all"

    SERVICE_SET: typing.Final = "set"
    SERVICE_REMOVE: typing.Final = "remove"

    GROUP_SCHEMA: typing.Final = vol.All(
        vol.Schema(
            {
                vol.Optional(core.Const.CONF_ENTITIES): vol.Any(_cv.entity_ids, None),
                core.Const.CONF_NAME: _cv.string,
                core.Const.CONF_ICON: _cv.icon,
                CONF_ALL: _cv.boolean,
            }
        )
    )
