"""
Dashboards Component for Smart Home - The Next Generation.

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
    """Constants for Dashboards Component."""

    EVENT_LOVELACE_UPDATED: typing.Final = "lovelace.updated"

    DEFAULT_ICON: typing.Final = "mdi:view-dashboard"

    MODE_YAML: typing.Final = "yaml"
    MODE_STORAGE: typing.Final = "storage"
    MODE_AUTO: typing.Final = "auto-gen"

    LOVELACE_CONFIG_FILE: typing.Final = "ui-lovelace.yaml"
    CONF_URL_PATH: typing.Final = "url_path"
    CONF_RESOURCE_TYPE_WS: typing.Final = "res_type"

    RESOURCE_TYPES: typing.Final = frozenset(["js", "css", "module", "html"])

    RESOURCE_FIELDS: typing.Final = {
        core.Const.CONF_TYPE: vol.In(RESOURCE_TYPES),
        core.Const.CONF_URL: _cv.string,
    }

    RESOURCE_SCHEMA: typing.Final = vol.Schema(RESOURCE_FIELDS)

    RESOURCE_CREATE_FIELDS: typing.Final = {
        vol.Required(CONF_RESOURCE_TYPE_WS): vol.In(RESOURCE_TYPES),
        vol.Required(core.Const.CONF_URL): _cv.string,
    }

    RESOURCE_UPDATE_FIELDS: typing.Final = {
        vol.Optional(CONF_RESOURCE_TYPE_WS): vol.In(RESOURCE_TYPES),
        vol.Optional(core.Const.CONF_URL): _cv.string,
    }

    SERVICE_RELOAD_RESOURCES: typing.Final = "reload_resources"
    RESOURCE_RELOAD_SERVICE_SCHEMA: typing.Final = vol.Schema({})

    CONF_TITLE: typing.Final = "title"
    CONF_REQUIRE_ADMIN: typing.Final = "require_admin"
    CONF_SHOW_IN_SIDEBAR: typing.Final = "show_in_sidebar"

    DASHBOARD_BASE_CREATE_FIELDS: typing.Final = {
        vol.Optional(CONF_REQUIRE_ADMIN, default=False): _cv.boolean,
        vol.Optional(core.Const.CONF_ICON): _cv.icon,
        vol.Required(CONF_TITLE): _cv.string,
        vol.Optional(CONF_SHOW_IN_SIDEBAR, default=True): _cv.boolean,
    }

    DASHBOARD_BASE_UPDATE_FIELDS: typing.Final = {
        vol.Optional(CONF_REQUIRE_ADMIN): _cv.boolean,
        vol.Optional(core.Const.CONF_ICON): vol.Any(_cv.icon, None),
        vol.Optional(CONF_TITLE): _cv.string,
        vol.Optional(CONF_SHOW_IN_SIDEBAR): _cv.boolean,
    }

    STORAGE_DASHBOARD_CREATE_FIELDS: typing.Final = {
        **DASHBOARD_BASE_CREATE_FIELDS,
        vol.Required(CONF_URL_PATH): _cv.string,
        # For now we write "storage" as all modes.
        # In future we can adjust this to be other modes.
        vol.Optional(core.Const.CONF_MODE, default=MODE_STORAGE): MODE_STORAGE,
    }

    STORAGE_DASHBOARD_UPDATE_FIELDS: typing.Final = DASHBOARD_BASE_UPDATE_FIELDS

    DASHBOARDS_STORAGE_VERSION: typing.Final = 1
    RESOURCES_STORAGE_VERSION: typing.Final = 1
