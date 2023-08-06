"""
Code Generator for Smart Home - The Next Generation.

Generates helper code from component manifests.

Smart Home - TNG is a Home Automation framework for observing the state
of entities and react to changes. It is based on Home Assistant from
home-assistant.io and the Home Assistant Community.

Copyright (c) 2022, Andreas Nixdorf

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

import pathlib
import re
import typing

import voluptuous as vol
from voluptuous.humanize import humanize_error

from smart_home_tng.core.config_validation import ConfigValidation as cv
from smart_home_tng.core.const import Const
from smart_home_tng.core.selector import Selector
from smart_home_tng.core.smart_home_controller_error import SmartHomeControllerError
from smart_home_tng.core.target_selector import TargetSelector
from smart_home_tng.core.yaml_loader import YamlLoader

from .code_validator import CodeValidator
from .config import Config
from .integration import Integration

_NAME: typing.Final = "services"


def _exists(value):
    """Check if value exists."""
    if value is None:
        raise vol.Invalid("Value cannot be None")
    return value


_FIELD_SCHEMA: typing.Final = vol.Schema(
    {
        vol.Required("description"): str,
        vol.Optional("name"): str,
        vol.Optional("example"): _exists,
        vol.Optional("default"): _exists,
        vol.Optional("values"): _exists,
        vol.Optional("required"): bool,
        vol.Optional("advanced"): bool,
        vol.Optional(Const.CONF_SELECTOR): Selector.validate_selector,
    }
)

_SERVICE_SCHEMA: typing.Final = vol.Schema(
    {
        vol.Required("description"): str,
        vol.Optional("name"): str,
        vol.Optional("target"): vol.Any(TargetSelector.CONFIG_SCHEMA, None),
        vol.Optional("fields"): vol.Schema({str: _FIELD_SCHEMA}),
    }
)

_SERVICES_SCHEMA: typing.Final = vol.Schema({cv.slug: _SERVICE_SCHEMA})


def _grep_dir(path: pathlib.Path, glob_pattern: str, search_pattern: str) -> bool:
    """Recursively go through a dir and it's children and find the regex."""
    pattern = re.compile(search_pattern)

    for fil in path.glob(glob_pattern):
        if not fil.is_file():
            continue

        if pattern.search(fil.read_text()):
            return True

    return False


def _validate_services(integration: Integration):
    """Validate services."""
    try:
        data = YamlLoader.load_yaml(str(integration.path / "services.yaml"))
    except FileNotFoundError:
        # Find if integration uses services
        # pylint: disable=line-too-long
        has_services = _grep_dir(
            integration.path,
            "**/*.py",
            r"(shc\.services\.(register|async_register))|async_register_entity_service|async_register_admin_service",
        )

        if has_services:
            integration.add_error(
                "services", "Registers services but has no services.yaml"
            )
        return
    except SmartHomeControllerError:
        integration.add_error("services", "Unable to load services.yaml")
        return

    try:
        _SERVICES_SCHEMA(data)
    except vol.Invalid as err:
        integration.add_error(
            "services", f"Invalid services.yaml: {humanize_error(data, err)}"
        )


# pylint: disable=unused-variable
class ServiceValidator(CodeValidator):
    """Validate dependencies."""

    def __init__(self):
        super().__init__(_NAME)

    def validate(self, integrations: dict[str, Integration], config: Config):
        """Handle dependencies for integrations."""
        # check services.yaml is cool
        for integration in integrations.values():
            if not integration.manifest:
                continue

            _validate_services(integration)
