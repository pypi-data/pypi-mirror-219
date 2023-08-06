"""
Tag Component for Smart Home - The Next Generation.

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

_ConfVal: typing.TypeAlias = core.ConfigValidation


# pylint: disable=unused-variable
class Const:
    """Constants for the Tag integration."""

    EVENT_TAG_SCANNED: typing.Final = "tag.scanned"
    TAG_ID: typing.Final = "tag_id"
    LAST_SCANNED: typing.Final = "last_scanned"
    CREATE_FIELDS: typing.Final = {
        vol.Optional(TAG_ID): _ConfVal.string,
        vol.Optional(core.Const.CONF_NAME): vol.All(str, vol.Length(min=1)),
        vol.Optional("description"): _ConfVal.string,
        vol.Optional(LAST_SCANNED): _ConfVal.datetime,
    }

    UPDATE_FIELDS: typing.Final = {
        vol.Optional(core.Const.CONF_NAME): vol.All(str, vol.Length(min=1)),
        vol.Optional("description"): _ConfVal.string,
        vol.Optional(LAST_SCANNED): _ConfVal.datetime,
    }
