"""
Analytics Component for Smart Home - The Next Generation.

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

import datetime
import logging
import typing

import voluptuous as vol


# pylint: disable=unused-variable
class Const:
    """Constants for the analytics integration."""

    ANALYTICS_ENDPOINT_URL: typing.Final = "https://analytics-api.home-assistant.io/v1"
    ANALYTICS_ENDPOINT_URL_DEV: typing.Final = (
        "https://analytics-api-dev.home-assistant.io/v1"
    )
    INTERVAL: typing.Final = datetime.timedelta(days=1)

    LOGGER: typing.Final = logging.getLogger(__package__)

    ATTR_ADDON_COUNT: typing.Final = "addon_count"
    ATTR_ADDONS: typing.Final = "addons"
    ATTR_ARCH: typing.Final = "arch"
    ATTR_AUTO_UPDATE: typing.Final = "auto_update"
    ATTR_AUTOMATION_COUNT: typing.Final = "automation_count"
    ATTR_BASE: typing.Final = "base"
    ATTR_BOARD: typing.Final = "board"
    ATTR_CERTIFICATE: typing.Final = "certificate"
    ATTR_CONFIGURED: typing.Final = "configured"
    ATTR_CUSTOM_INTEGRATIONS: typing.Final = "custom_integrations"
    ATTR_DIAGNOSTICS: typing.Final = "diagnostics"
    ATTR_ENERGY: typing.Final = "energy"
    ATTR_HEALTHY: typing.Final = "healthy"
    ATTR_INSTALLATION_TYPE: typing.Final = "installation_type"
    ATTR_INTEGRATION_COUNT: typing.Final = "integration_count"
    ATTR_INTEGRATIONS: typing.Final = "integrations"
    ATTR_ONBOARDED: typing.Final = "onboarded"
    ATTR_OPERATING_SYSTEM: typing.Final = "operating_system"
    ATTR_PREFERENCES: typing.Final = "preferences"
    ATTR_PROTECTED: typing.Final = "protected"
    ATTR_SLUG: typing.Final = "slug"
    ATTR_STATE_COUNT: typing.Final = "state_count"
    ATTR_STATISTICS: typing.Final = "statistics"
    ATTR_SUPERVISOR: typing.Final = "supervisor"
    ATTR_SUPPORTED: typing.Final = "supported"
    ATTR_USAGE: typing.Final = "usage"
    ATTR_USER_COUNT: typing.Final = "user_count"
    ATTR_UUID: typing.Final = "uuid"
    ATTR_VERSION: typing.Final = "version"

    PREFERENCE_SCHEMA: typing.Final = vol.Schema(
        {
            vol.Optional(ATTR_BASE): bool,
            vol.Optional(ATTR_DIAGNOSTICS): bool,
            vol.Optional(ATTR_STATISTICS): bool,
            vol.Optional(ATTR_USAGE): bool,
        }
    )
