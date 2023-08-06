"""
Blueprint Integration for Smart Home - The Next Generation.

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


def _version_validator(value):
    """Validate a Smart Home - The Next Generation version."""
    if not isinstance(value, str):
        raise vol.Invalid("Version needs to be a string")

    parts = value.split(".")

    if len(parts) != 3:
        raise vol.Invalid("Version needs to be formatted as {major}.{minor}.{patch}")

    try:
        parts = [int(p) for p in parts]
    except ValueError:
        raise vol.Invalid(
            "Major, minor and patch version needs to be an integer"
        ) from None

    return value


def _validate_yaml_suffix(value: str) -> str:
    """Validate value has a YAML suffix."""
    if not value.endswith(".yaml"):
        raise vol.Invalid("Path needs to end in .yaml")
    return value


# pylint: disable=unused-variable
class Const:
    """Constants for the blueprint integration."""

    BLUEPRINT_FOLDER: typing.Final = "blueprints"

    CONF_BLUEPRINT: typing.Final = "blueprint"
    CONF_USE_BLUEPRINT: typing.Final = "use_blueprint"
    CONF_INPUT: typing.Final = "input"
    CONF_SOURCE_URL: typing.Final = "source_url"
    CONF_MIN_VERSION: typing.Final = "min_version"
    CONF_SMART_HOME_CONTROLLER: typing.Final = "smart_home_tng"
    SHC_FOLDER: typing.Final = "smart_home_tng"
    BLUEPRINT_INPUT_SCHEMA: typing.Final = vol.Schema(
        {
            vol.Optional(core.Const.CONF_NAME): str,
            vol.Optional(core.Const.CONF_DESCRIPTION): str,
            vol.Optional(core.Const.CONF_DEFAULT): _cv.match_all,
            vol.Optional(core.Const.CONF_SELECTOR): core.Selector.validate_selector,
        }
    )
    BLUEPRINT_SCHEMA: typing.Final = vol.Schema(
        {
            vol.Required(CONF_BLUEPRINT): vol.Schema(
                {
                    vol.Required(core.Const.CONF_NAME): str,
                    vol.Optional(core.Const.CONF_DESCRIPTION): str,
                    vol.Required(core.Const.CONF_DOMAIN): str,
                    vol.Optional(CONF_SOURCE_URL): _cv.url,
                    vol.Optional(CONF_SMART_HOME_CONTROLLER): {
                        vol.Optional(CONF_MIN_VERSION): _version_validator
                    },
                    vol.Optional(CONF_INPUT, default=dict): {
                        str: vol.Any(
                            None,
                            BLUEPRINT_INPUT_SCHEMA,
                        )
                    },
                }
            ),
        },
        extra=vol.ALLOW_EXTRA,
    )
    BLUEPRINT_INSTANCE_FIELDS: typing.Final = vol.Schema(
        {
            vol.Required(CONF_USE_BLUEPRINT): vol.Schema(
                {
                    vol.Required(core.Const.CONF_PATH): vol.All(
                        _cv.path, _validate_yaml_suffix
                    ),
                    vol.Required(CONF_INPUT, default=dict): {str: _cv.match_all},
                }
            )
        },
        extra=vol.ALLOW_EXTRA,
    )
