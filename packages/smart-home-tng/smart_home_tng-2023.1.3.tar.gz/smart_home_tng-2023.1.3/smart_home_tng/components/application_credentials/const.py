"""
Application Credentials Integration for Smart Home - The Next Generation.

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

_cv = core.ConfigValidation


# pylint: disable=unused-variable
class Const:
    """Constants for Application Credentials Integration."""

    CONF_AUTH_DOMAIN: typing.Final = "auth_domain"
    CREATE_FIELDS: typing.Final = {
        vol.Required(core.Const.CONF_DOMAIN): _cv.string,
        vol.Required(core.Const.CONF_CLIENT_ID): _cv.string,
        vol.Required(core.Const.CONF_CLIENT_SECRET): _cv.string,
        vol.Optional(CONF_AUTH_DOMAIN): _cv.string,
        vol.Optional(core.Const.CONF_NAME): _cv.string,
    }
    UPDATE_FIELDS: typing.Final = {}  # Not supported
    CREATE_SCHEMA: typing.Final = vol.Schema(CREATE_FIELDS)
    DEFAULT_IMPORT_NAME: typing.Final = "Import from configuration.yaml"
