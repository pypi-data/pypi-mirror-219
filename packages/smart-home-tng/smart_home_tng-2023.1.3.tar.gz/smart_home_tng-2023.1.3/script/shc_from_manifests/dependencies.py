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

import ast
import pathlib
import typing

from smart_home_tng.core.platform import Platform
from smart_home_tng.core.setup_manager import SetupManager

from .code_validator import CodeValidator
from .integration import Integration

_NAME: typing.Final = "dependencies"


class ImportCollector(ast.NodeVisitor):
    """Collect all integrations referenced."""

    def __init__(self, integration: Integration):
        """Initialize the import collector."""
        self._integration = integration
        self._referenced: dict[pathlib.Path, set[str]] = {}

        # Current file or dir we're inspecting
        self._cur_fil_dir = None

    @property
    def referenced(self) -> dict[pathlib.Path, set[str]]:
        return self._referenced.copy()

    def collect(self) -> None:
        """Collect imports from a source file."""
        for fil in self._integration.path.glob("**/*.py"):
            if not fil.is_file():
                continue

            self._cur_fil_dir = fil.relative_to(self._integration.path)
            self._referenced[self._cur_fil_dir] = set()
            self.visit(ast.parse(fil.read_text()))
            self._cur_fil_dir = None

    def _add_reference(self, reference_domain: str):
        """Add a reference."""
        self._referenced[self._cur_fil_dir].add(reference_domain)

    # pylint: disable=invalid-name
    def visit_ImportFrom(self, node):
        """Visit ImportFrom node."""
        if node.module is None:
            return

        # Exception: we will allow importing the sign path code.
        if (
            node.module == "smart_home_tng.components.http.auth"
            and len(node.names) == 1
            and node.names[0].name == "async_sign_path"
        ):
            return

        if node.module.startswith("smart_home_tng.components."):
            # from homeassistant.components.alexa.smart_home import EVENT_ALEXA_SMART_HOME
            # from homeassistant.components.logbook import bla
            self._add_reference(node.module.split(".")[2])

        elif node.module == "smart_home_tng.components":
            # from smart_home_tng.components import sun
            for name_node in node.names:
                self._add_reference(name_node.name)

    # pylint: disable=invalid-name
    def visit_Import(self, node):
        """Visit Import node."""
        # import homeassistant.components.hue as hue
        for name_node in node.names:
            if name_node.name.startswith("smart_home_tng.components."):
                self._add_reference(name_node.name.split(".")[2])

    # pylint: disable=invalid-name
    def visit_Attribute(self, node):
        """Visit Attribute node."""
        # hass.components.hue.async_create()
        # Name(id=hass)
        #   .Attribute(attr=hue)
        #   .Attribute(attr=async_create)

        # self.hass.components.hue.async_create()
        # Name(id=self)
        #   .Attribute(attr=hass) or .Attribute(attr=_hass)
        #   .Attribute(attr=hue)
        #   .Attribute(attr=async_create)
        if (
            isinstance(node.value, ast.Attribute)
            and node.value.attr == "components"
            and (
                (
                    isinstance(node.value.value, ast.Name)
                    and node.value.value.id == "shc"
                )
                or (
                    isinstance(node.value.value, ast.Attribute)
                    and node.value.value.attr in ("shc", "_shc")
                )
            )
        ):
            self._add_reference(node.attr)
        else:
            # Have it visit other kids
            self.generic_visit(node)


_ALLOWED_USED_COMPONENTS = {
    *{str(platform) for platform in Platform},
    # Internal integrations
    "alert",
    "automation",
    "conversation",
    "device_automation",
    "frontend",
    "group",
    "hassio",
    "homeassistant",
    "input_boolean",
    "input_button",
    "input_datetime",
    "input_number",
    "input_select",
    "input_text",
    "media_source",
    "onboarding",
    "persistent_notification",
    "person",
    "script",
    "shopping_list",
    "sun",
    "system_health",
    "system_log",
    "timer",
    "webhook",
    "websocket_api",
    "zone",
    # Other
    "mjpeg",  # base class, has no reqs or component to load.
    "stream",  # Stream cannot install on all systems, can be imported without reqs.
}

_IGNORE_VIOLATIONS: typing.Final = {
    # Has same requirement, gets defaults.
    ("sql", "recorder"),
    # Sharing a base class
    ("openalpr_cloud", "openalpr_local"),
    ("lutron_caseta", "lutron"),
    ("ffmpeg_noise", "ffmpeg_motion"),
    # Demo
    ("demo", "manual"),
    ("demo", "openalpr_local"),
    # This would be a circular dep
    ("http", "network"),
    # This should become a helper method that integrations can submit data to
    ("websocket_api", "lovelace"),
    ("websocket_api", "shopping_list"),
    "logbook",
    # Migration wizard from zwave to zwave_js.
    "zwave_js",
}


def _calc_allowed_references(integration: Integration) -> set[str]:
    """Return a set of allowed references."""
    allowed_references = (
        _ALLOWED_USED_COMPONENTS
        | set(integration.manifest.get("dependencies", []))
        | set(integration.manifest.get("after_dependencies", []))
    )

    # Discovery requirements are ok if referenced in manifest
    for check_domain, to_check in SetupManager.DISCOVERY_INTEGRATIONS.items():
        if any(check in integration.manifest for check in to_check):
            allowed_references.add(check_domain)

    return allowed_references


def _find_non_referenced_integrations(
    integrations: dict[str, Integration],
    integration: Integration,
    references: dict[pathlib.Path, set[str]],
):
    """Find intergrations that are not allowed to be referenced."""
    allowed_references = _calc_allowed_references(integration)
    referenced = set()
    for path, refs in references.items():
        if len(path.parts) == 1:
            # climate.py is stored as climate
            cur_fil_dir = path.stem
        else:
            # climate/__init__.py is stored as climate
            cur_fil_dir = path.parts[0]

        is_platform_other_integration = cur_fil_dir in integrations

        for ref in refs:
            # We are always allowed to import from ourselves
            if ref == integration.domain:
                continue

            # These references are approved based on the manifest
            if ref in allowed_references:
                continue

            # Some violations are whitelisted
            if (integration.domain, ref) in _IGNORE_VIOLATIONS:
                continue

            # If it's a platform for another integration, the other integration is ok
            if is_platform_other_integration and cur_fil_dir == ref:
                continue

            # These have a platform specified in this integration
            if not is_platform_other_integration and (
                (integration.path / f"{ref}.py").is_file()
                # Platform dir
                or (integration.path / ref).is_dir()
            ):
                continue

            referenced.add(ref)

    return referenced


def _validate_dependencies(
    integrations: dict[str, Integration], integration: Integration
):
    """Validate all dependencies."""
    # Some integrations are allowed to have violations.
    if integration.domain in _IGNORE_VIOLATIONS:
        return

    # Find usage of hass.components
    collector = ImportCollector(integration)
    collector.collect()
    referenced = collector.referenced

    for domain in sorted(
        _find_non_referenced_integrations(
            integrations, integration, referenced
        )
    ):
        integration.add_error(
            "dependencies",
            f"Using component {domain} but it's not in 'dependencies' "
            "or 'after_dependencies'",
        )


# pylint: disable=unused-variable
class DependencyValidator(CodeValidator):
    """Validate dependencies."""

    def __init__(self):
        super().__init__(_NAME)

    def validate(self, integrations: dict[str, Integration], config):
        """Handle dependencies for integrations."""
        # check for non-existing dependencies
        for integration in integrations.values():
            if not integration.manifest:
                continue

            _validate_dependencies(integrations, integration)

            if config.specific_integrations:
                continue

            # check that all referenced dependencies exist
            after_deps = integration.manifest.get("after_dependencies", [])
            for dep in integration.manifest.get("dependencies", []):
                if dep in after_deps:
                    integration.add_error(
                        "dependencies",
                        f"Dependency {dep} is both in dependencies and after_dependencies",
                    )

                if dep not in integrations:
                    integration.add_error(
                        "dependencies", f"Dependency {dep} does not exist"
                    )
