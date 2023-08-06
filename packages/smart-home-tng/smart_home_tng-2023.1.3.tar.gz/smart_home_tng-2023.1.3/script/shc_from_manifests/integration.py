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

import importlib
import json
import pathlib
import typing

import attr

from .error import Error


# pylint: disable=unused-variable
@attr.s
class Integration:
    """Represent an integration in our validator."""

    @classmethod
    def load_dir(cls, path: pathlib.Path):
        """Load all integrations in a directory."""
        assert path.is_dir()
        integrations = {}
        for fil in path.iterdir():
            if fil.is_file() or fil.name == "__pycache__":
                continue

            init = fil / "__init__.py"
            if not init.exists():
                print(
                    f"Warning: {init} missing, skipping directory. "
                    "If this is your development environment, "
                    "you can safely delete this folder."
                )
                continue

            integration = cls(fil)
            integration.load_manifest()
            integrations[integration.domain] = integration

        return integrations

    path: pathlib.Path = attr.ib()
    manifest: dict[str, typing.Any] = attr.ib(default=None)
    errors: list[Error] = attr.ib(factory=list)
    warnings: list[Error] = attr.ib(factory=list)

    @property
    def domain(self) -> str:
        """Integration domain."""
        return self.path.name

    @property
    def core(self) -> bool:
        """Core integration."""
        return self.path.as_posix().startswith("smart_home_tng/components")

    @property
    def disabled(self) -> str:
        """Return if integration is disabled."""
        if self.manifest is None:
            return None
        return self.manifest.get("disabled")

    @property
    def name(self) -> str:
        """Return name of the integration."""
        if self.manifest is None:
            return None
        return self.manifest["name"]

    @property
    def quality_scale(self) -> str:
        """Return quality scale of the integration."""
        if self.manifest is None:
            return None
        return self.manifest.get("quality_scale")

    @property
    def config_flow(self) -> bool:
        """Return if the integration has a config flow."""
        if self.manifest is None:
            return False
        return self.manifest.get("config_flow", False)

    @property
    def requirements(self) -> list[str]:
        """List of requirements."""
        if self.manifest is None:
            return []
        return self.manifest.get("requirements", [])

    @property
    def dependencies(self) -> list[str]:
        """List of dependencies."""
        if self.manifest is None:
            return []
        return self.manifest.get("dependencies", [])

    @property
    def supported_brands(self) -> dict[str]:
        """Return dict of supported brands."""
        return self.manifest.get("supported_brands", {})

    @property
    def integration_type(self) -> str:
        """Get integration_type."""
        if self.manifest is None:
            return "integration"
        return self.manifest.get("integration_type", "integration")

    def add_error(self, *args: typing.Any, **kwargs: typing.Any) -> None:
        """Add an error."""
        self.errors.append(Error(*args, **kwargs))

    def add_warning(self, *args: typing.Any, **kwargs: typing.Any) -> None:
        """Add an warning."""
        self.warnings.append(Error(*args, **kwargs))

    def load_manifest(self) -> None:
        """Load manifest."""
        manifest_path = self.path / "manifest.json"
        if not manifest_path.is_file():
            self.add_error("model", f"Manifest file {manifest_path} not found")
            return

        try:
            manifest = json.loads(manifest_path.read_text())
        except ValueError as err:
            self.add_error("model", f"Manifest contains invalid JSON: {err}")
            return

        self.manifest = manifest

    def import_pkg(self, platform=None):
        """Import the Python file."""
        pkg = f"smart_home_tng.components.{self.domain}"
        if platform is not None:
            pkg += f".{platform}"
        return importlib.import_module(pkg)
