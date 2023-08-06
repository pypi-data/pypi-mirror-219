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

import collections
import json
import os
import re
import subprocess
import sys
import typing

import awesomeversion as asv
import tqdm

from smart_home_tng.core.const import Const as core
from smart_home_tng.core.the_next_generation import TheNextGeneration

from .code_validator import CodeValidator
from .config import Config
from .const import Const
from .integration import Integration

if sys.version_info < (3, 10):
    from stdlib_list import stdlib_list

_NAME: typing.Final = "requirements"
_IGNORE_PACKAGES: typing.Final = Const.COMMENT_REQUIREMENTS_NORMALIZED
_PACKAGE_REGEX: typing.Final = re.compile(
    r"^(?:--.+\s)?([-_,\.\w\d\[\]]+)(==|>=|<=|~=|!=|<|>|===)*(.*)$"
)
_PIP_REGEX: typing.Final = re.compile(
    r"^(--.+\s)?([-_\.\w\d]+.*(?:==|>=|<=|~=|!=|<|>|===)?.*$)"
)
_PIP_VERSION_RANGE_SEPARATOR: typing.Final = re.compile(
    r"^(==|>=|<=|~=|!=|<|>|===)?(.*)$"
)
_SUPPORTED_PYTHON_TUPLES: typing.Final = [
    core.REQUIRED_PYTHON_VER[:2],
]
if core.REQUIRED_PYTHON_VER[0] == core.REQUIRED_NEXT_PYTHON_VER[0]:
    for minor in range(
        core.REQUIRED_PYTHON_VER[1] + 1, core.REQUIRED_NEXT_PYTHON_VER[1] + 1
    ):
        _SUPPORTED_PYTHON_TUPLES.append((core.REQUIRED_PYTHON_VER[0], minor))
_SUPPORTED_PYTHON_VERSIONS: typing.Final = [
    ".".join(map(str, version_tuple)) for version_tuple in _SUPPORTED_PYTHON_TUPLES
]
if sys.version_info < (3, 10):
    _STD_LIBS: typing.Final = {
        version: set(stdlib_list(version)) for version in _SUPPORTED_PYTHON_VERSIONS
    }
else:
    _STD_LIBS: typing.Final = {}

_IGNORE_VIOLATIONS: typing.Final = {
    # Still has standard library requirements.
    "acmeda",
    "blink",
    "ezviz",
    "hdmi_cec",
    "juicenet",
    "lupusec",
    "rainbird",
    "slide",
    "suez_water",
}


def normalize_package_name(requirement: str) -> str:
    """Return a normalized package name from a requirement string."""
    # This function is also used in hassfest.
    match = Const.PACKAGE_REGEX.search(requirement)
    if not match:
        return ""

    # pipdeptree needs lowercase and dash instead of underscore as separator
    package = match.group(1).lower().replace("_", "-")

    return package


# pylint: disable=unused-variable
class RequirementsValidator(CodeValidator):
    """Validate requirements."""

    def __init__(self):
        super().__init__(_NAME)
        self._pip_deptree_cache = None

    def _ensure_cache(self):
        """Ensure we have a cache of pipdeptree.

        {
            "flake8-docstring": {
                "key": "flake8-docstrings",
                "package_name": "flake8-docstrings",
                "installed_version": "1.5.0"
                "dependencies": {"flake8"}
            }
        }
        """

        if self._pip_deptree_cache is not None:
            return

        cache = {}

        for item in json.loads(
            subprocess.run(
                ["pipdeptree", "-w", "silence", "--json"],
                check=True,
                capture_output=True,
                text=True,
            ).stdout
        ):
            cache[item["package"]["key"]] = {
                **item["package"],
                "dependencies": {dep["key"] for dep in item["dependencies"]},
            }

        self._pip_deptree_cache = cache

    def validate(self, integrations: dict[str, Integration], config: Config):
        """Handle requirements for integrations."""
        # Check if we are doing format-only validation.
        if not config.requirements:
            for integration in integrations.values():
                self._validate_requirements_format(integration)
            return

        self._ensure_cache()

        # check for incompatible requirements

        disable_tqdm = config.specific_integrations or os.environ.get("CI", False)

        for integration in tqdm.tqdm(integrations.values(), disable=disable_tqdm):
            if not integration.manifest:
                continue

            self._validate_requirements(integration)

    def _get_requirements(self, integration: Integration, packages: set[str]) -> set[str]:
        """Return all (recursively) requirements for an integration."""
        self._ensure_cache()

        all_requirements = set()

        to_check = collections.deque(packages)

        while to_check:
            package = to_check.popleft()

            if package in all_requirements:
                continue

            all_requirements.add(package)

            item = self._pip_deptree_cache.get(package)

            if item is None:
                # Only warn if direct dependencies could not be resolved
                if package in packages:
                    integration.add_error(
                        "requirements", f"Failed to resolve requirements for {package}"
                    )
                continue

            to_check.extend(item["dependencies"])

        return all_requirements

    async def _install_requirements(
        self, integration: Integration, requirements: set[str]
    ) -> bool:
        """Install integration requirements.

        Return True if successful.
        """
        self._ensure_cache()

        current_shc = TheNextGeneration.current()
        if current_shc is None:
            current_shc = TheNextGeneration()

        for req in requirements:
            match = _PIP_REGEX.search(req)

            if not match:
                integration.add_error(
                    "requirements",
                    f"Failed to parse requirement {req} before installation",
                )
                continue

            requirement_arg = match.group(2)

            is_installed = False

            normalized = normalize_package_name(requirement_arg)

            if normalized and "==" in requirement_arg:
                ver = requirement_arg.split("==")[-1]
                item = self._pip_deptree_cache.get(normalized)
                is_installed = item and item["installed_version"] == ver
            elif normalized and ">=" in requirement_arg:
                ver = requirement_arg.split(">=")[-1]
                item = self._pip_deptree_cache.get(normalized)
                is_installed = item and item["installed_version"] >= ver

            if not is_installed:
                try:
                    is_installed = current_shc.setup.is_installed(req)
                except ValueError:
                    is_installed = False

            if is_installed:
                continue

            await current_shc.setup.async_process_requirements(integration.domain, [req])
            if current_shc.setup.is_installed(req):
                # Clear the pipdeptree cache if something got installed
                self._pip_deptree_cache = None
            else:
                integration.add_error(
                    "requirements",
                    f"Requirement {req} failed to install",
                )

        if integration.errors:
            return False

        return True

    def _validate_requirements(self, integration: Integration):
        """Validate requirements."""
        if not self._validate_requirements_format(integration):
            return

        # Some integrations have not been fixed yet so are allowed to have violations.
        if integration.domain in _IGNORE_VIOLATIONS:
            return

        integration_requirements = set()
        integration_packages = set()
        for req in integration.requirements:
            package = normalize_package_name(req)
            if not package:
                integration.add_error(
                    "requirements",
                    f"Failed to normalize package name from requirement {req}",
                )
                return
            if package in _IGNORE_PACKAGES:
                continue
            integration_requirements.add(req)
            integration_packages.add(package)

        if integration.disabled:
            return

        install_ok = self._install_requirements(integration, integration_requirements)

        if not install_ok:
            return

        all_integration_requirements = self._get_requirements(integration, integration_packages)

        if integration_requirements and not all_integration_requirements:
            integration.add_error(
                "requirements",
                f"Failed to resolve requirements {integration_requirements}",
            )
            return

        # Check for requirements incompatible with standard library.
        for version, std_libs in _STD_LIBS.items():
            for req in all_integration_requirements:
                if req in std_libs:
                    integration.add_error(
                        "requirements",
                        f"Package {req} is not compatible with Python {version} standard library",
                    )

    @staticmethod
    def _validate_requirements_format(integration: Integration) -> bool:
        """Validate requirements format.

        Returns if valid.
        """
        start_errors = len(integration.errors)

        for req in integration.requirements:
            if " " in req:
                integration.add_error(
                    "requirements",
                    f'Requirement "{req}" contains a space',
                )
                continue

            pkg, sep, version = _PACKAGE_REGEX.match(req).groups()

            if integration.core and sep != "==" and sep != ">=":
                integration.add_error(
                    "requirements",
                    f'Requirement {req} need to be pinned "<pkg name>==<version>".',
                )
                continue

            if not version:
                continue

            for part in version.split(","):
                version_part = _PIP_VERSION_RANGE_SEPARATOR.match(part)
                if (
                    version_part
                    and asv.AwesomeVersion(version_part.group(2)).strategy
                    == asv.AwesomeVersionStrategy.UNKNOWN
                ):
                    integration.add_error(
                        "requirements",
                        f"Unable to parse package version ({version}) for {pkg}.",
                    )
                    continue

        return len(integration.errors) == start_errors
