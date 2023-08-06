"""
Script Component for Smart Home - The Next Generation.

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

import logging
import typing
import voluptuous as vol

from ... import core

_cv: typing.TypeAlias = core.ConfigValidation


# pylint: disable=unused-variable
class Const:
    """Constants for the script integration."""

    ATTR_LAST_ACTION: typing.Final = "last_action"
    ATTR_LAST_TRIGGERED: typing.Final = "last_triggered"
    ATTR_VARIABLES: typing.Final = "variables"

    CONF_ADVANCED: typing.Final = "advanced"
    CONF_EXAMPLE: typing.Final = "example"
    CONF_FIELDS: typing.Final = "fields"
    CONF_REQUIRED: typing.Final = "required"
    CONF_TRACE: typing.Final = "trace"

    LOGGER: typing.Final = logging.getLogger(__package__)

    SCRIPT_SERVICE_SCHEMA: typing.Final = vol.Schema(dict)
    SCRIPT_TURN_ONOFF_SCHEMA: typing.Final = _cv.make_entity_service_schema(
        {vol.Optional(ATTR_VARIABLES): {str: _cv.match_all}}
    )
    RELOAD_SERVICE_SCHEMA: typing.Final = vol.Schema({})

    SCRIPT_ENTITY_SCHEMA: typing.Final = core.Scripts.make_script_schema(
        {
            vol.Optional(core.Const.CONF_ALIAS): _cv.string,
            vol.Optional(CONF_TRACE, default={}): _cv.TRACE_CONFIG_SCHEMA,
            vol.Optional(core.Const.CONF_ICON): _cv.icon,
            vol.Required(core.Const.CONF_SEQUENCE): _cv.SCRIPT_SCHEMA,
            vol.Optional(core.Const.CONF_DESCRIPTION, default=""): _cv.string,
            vol.Optional(core.Const.CONF_VARIABLES): _cv.SCRIPT_VARIABLES_SCHEMA,
            vol.Optional(CONF_FIELDS, default={}): {
                _cv.string: {
                    vol.Optional(CONF_ADVANCED, default=False): _cv.boolean,
                    vol.Optional(core.Const.CONF_DEFAULT): _cv.match_all,
                    vol.Optional(core.Const.CONF_DESCRIPTION): _cv.string,
                    vol.Optional(CONF_EXAMPLE): _cv.string,
                    vol.Optional(core.Const.CONF_NAME): _cv.string,
                    vol.Optional(CONF_REQUIRED, default=False): _cv.boolean,
                    vol.Optional(
                        core.Const.CONF_SELECTOR
                    ): core.Selector.validate_selector,
                }
            },
        },
        core.Scripts.Const.SCRIPT_MODE_SINGLE,
    )
