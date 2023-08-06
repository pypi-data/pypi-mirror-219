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

import json
import typing

from .code_validator import CodeValidator
from .config import Config
from .integration import Integration

_NAME: typing.Final = "json"


def _validate_json_files(integration: Integration):
    """Validate JSON files for integration."""
    for json_file in integration.path.glob("**/*.json"):
        if not json_file.is_file():
            continue

        try:
            json.loads(json_file.read_text())
        except json.JSONDecodeError:
            relative_path = json_file.relative_to(integration.path)
            integration.add_error("json", f"Invalid JSON file {relative_path}")


# pylint: disable=unused-variable
class JsonValidator(CodeValidator):
    """Validate integration JSON files."""

    def __init__(self):
        super().__init__(_NAME)

    def validate(self, integrations: dict[str, Integration], config: Config):
        """Handle JSON files inside integrations."""
        if not config.specific_integrations:
            return

        for integration in integrations.values():
            if not integration.manifest:
                continue

            _validate_json_files(integration)
