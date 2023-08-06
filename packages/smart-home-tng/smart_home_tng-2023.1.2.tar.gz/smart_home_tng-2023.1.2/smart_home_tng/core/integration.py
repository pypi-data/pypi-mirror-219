"""
Core components of Smart Home - The Next Generation.

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

import importlib
import json
import logging
import pathlib
import types
import typing

import awesomeversion as asv

from .circular_dependency import CircularDependency
from .integration_not_found import IntegrationNotFound
from .manifest import Manifest

_LOGGER: typing.Final = logging.getLogger(__name__)

if not typing.TYPE_CHECKING:

    class SmartHomeController:
        ...


if typing.TYPE_CHECKING:
    from .smart_home_controller import SmartHomeController


# pylint: disable=unused-variable
class Integration:
    """An integration in Smart Home - The Next Generation."""

    def __init__(
        self,
        shc: SmartHomeController,
        pkg_path: str,
        file_path: pathlib.Path,
        manifest: Manifest,
    ) -> None:
        """Initialize an integration."""
        self._shc = shc
        self._pkg_path = pkg_path
        self._file_path = file_path
        self._manifest = manifest
        manifest["is_built_in"] = self.is_built_in

        if self.dependencies:
            self._all_dependencies_resolved: bool = None
            self._all_dependencies: set[str] = None
        else:
            self._all_dependencies_resolved = True
            self._all_dependencies = set()

        _LOGGER.info(f"Loaded {self.domain} from {pkg_path}")

    @staticmethod
    def resolve_from_root(
        shc: SmartHomeController, root_module: types.ModuleType, domain: str
    ):
        """Resolve an integration from a root module."""
        for base in root_module.__path__:
            manifest_path = pathlib.Path(base) / domain / "manifest.json"

            if not manifest_path.is_file():
                continue

            try:
                manifest = json.loads(manifest_path.read_text())
            except ValueError as err:
                _LOGGER.error(
                    f"Error parsing manifest.json file at {manifest_path}: {err}"
                )
                continue

            integration = Integration(
                shc,
                f"{root_module.__name__}.{domain}",
                manifest_path.parent,
                manifest,
            )

            if integration.is_built_in:
                return integration

            _LOGGER.warning(shc.CUSTOM_WARNING, integration.domain)
            if integration.version is None:
                _LOGGER.error(
                    f"The custom integration '{integration.domain}' does not have a "
                    + "version key in the manifest file and was blocked from loading. "
                )
                return None
            try:
                asv.AwesomeVersion(
                    integration.version,
                    [
                        asv.AwesomeVersionStrategy.CALVER,
                        asv.AwesomeVersionStrategy.SEMVER,
                        asv.AwesomeVersionStrategy.SIMPLEVER,
                        asv.AwesomeVersionStrategy.BUILDVER,
                        asv.AwesomeVersionStrategy.PEP440,
                    ],
                )
            except asv.AwesomeVersionException:
                _LOGGER.error(
                    f"The custom integration '{integration.domain}' does not "
                    f"have a valid version key ({integration.version}) "
                    + "in the manifest file and was blocked from loading."
                )
                return None
            return integration

        return None

    @property
    def pkg_path(self) -> str:
        return self._pkg_path

    @property
    def file_path(self) -> pathlib.Path:
        return self._file_path

    @property
    def name(self) -> str:
        """Return name."""
        return self._manifest["name"]

    @property
    def disabled(self) -> str:
        """Return reason integration is disabled."""
        return self._manifest.get("disabled")

    @property
    def domain(self) -> str:
        """Return domain."""
        return self._manifest["domain"]

    @property
    def dependencies(self) -> list[str]:
        """Return dependencies."""
        return self._manifest.get("dependencies", [])

    @property
    def after_dependencies(self) -> list[str]:
        """Return after_dependencies."""
        return self._manifest.get("after_dependencies", [])

    @property
    def requirements(self) -> list[str]:
        """Return requirements."""
        return self._manifest.get("requirements", [])

    @property
    def config_flow(self) -> bool:
        """Return config_flow."""
        return self._manifest.get("config_flow") or False

    @property
    def documentation(self) -> str:
        """Return documentation."""
        return self._manifest.get("documentation")

    @property
    def issue_tracker(self) -> str:
        """Return issue tracker link."""
        return self._manifest.get("issue_tracker")

    @property
    def loggers(self) -> list[str]:
        """Return list of loggers used by the integration."""
        return self._manifest.get("loggers")

    @property
    def quality_scale(self) -> str:
        """Return Integration Quality Scale."""
        return self._manifest.get("quality_scale")

    @property
    def iot_class(self) -> str:
        """Return the integration IoT Class."""
        return self._manifest.get("iot_class")

    @property
    def integration_type(self) -> typing.Literal["integration", "helper"]:
        """Return the integration type."""
        return self._manifest.get("integration_type", "integration")

    @property
    def manifest(self) -> Manifest:
        return self._manifest.copy()

    @property
    def mqtt(self) -> list[str]:
        """Return Integration MQTT entries."""
        return self._manifest.get("mqtt")

    @property
    def ssdp(self) -> list[dict[str, str]]:
        """Return Integration SSDP entries."""
        return self._manifest.get("ssdp")

    @property
    def zeroconf(self) -> list[str | dict[str, str]]:
        """Return Integration zeroconf entries."""
        return self._manifest.get("zeroconf")

    @property
    def dhcp(self) -> list[dict[str, str | bool]]:
        """Return Integration dhcp entries."""
        return self._manifest.get("dhcp")

    @property
    def usb(self) -> list[dict[str, str]]:
        """Return Integration usb entries."""
        return self._manifest.get("usb")

    @property
    def homekit(self) -> dict[str, list[str]]:
        """Return Integration homekit entries."""
        return self._manifest.get("homekit")

    @property
    def is_built_in(self) -> bool:
        """Test if package is a built-in integration."""
        return self._pkg_path.startswith(self._shc.setup.PACKAGE_BUILTIN)

    @property
    def version(self) -> asv.AwesomeVersion:
        """Return the version of the integration."""
        if "version" not in self._manifest:
            return None
        return asv.AwesomeVersion(self._manifest["version"])

    @property
    def all_dependencies(self) -> set[str]:
        """Return all dependencies including sub-dependencies."""
        if self._all_dependencies is None:
            raise RuntimeError("Dependencies not resolved!")

        return self._all_dependencies

    @property
    def all_dependencies_resolved(self) -> bool:
        """Return if all dependencies have been resolved."""
        return self._all_dependencies_resolved is not None

    async def resolve_dependencies(self) -> bool:
        """Resolve all dependencies."""
        if self._all_dependencies_resolved is not None:
            return self._all_dependencies_resolved

        try:
            dependencies = await self._shc.setup.async_component_dependencies(
                self.domain, self, set(), set()
            )
            dependencies.discard(self.domain)
            self._all_dependencies = dependencies
            self._all_dependencies_resolved = True
        except IntegrationNotFound as err:
            _LOGGER.error(
                f"Unable to resolve dependencies for {self.domain}: "
                + f"we are unable to resolve (sub)dependency {err.domain}"
            )
            self._all_dependencies_resolved = False
        except CircularDependency as err:
            _LOGGER.error(
                f"Unable to resolve dependencies for {self.domain}: "
                + "it contains a circular dependency: "
                + f"{err.from_domain} -> {err.to_domain}"
            )
            self._all_dependencies_resolved = False

        return self._all_dependencies_resolved

    def get_component(self) -> types.ModuleType:
        """Return the component."""
        cache: dict[str, types.ModuleType] = self._shc.data.setdefault(
            self._shc.setup.DATA_COMPONENTS, {}
        )
        if self.domain in cache:
            return cache[self.domain]

        try:
            cache[self.domain] = importlib.import_module(self.pkg_path)
        except ImportError:
            raise
        except Exception as err:
            _LOGGER.exception(
                f"Unexpected exception importing component {self._pkg_path}"
            )
            raise ImportError(f"Exception importing {self._pkg_path}") from err

        return cache[self.domain]

    def get_platform(self, platform_name: str) -> types.ModuleType:
        """Return a platform for the integration."""
        cache: dict[str, types.ModuleType] = self._shc.data.setdefault(
            self._shc.setup.DATA_COMPONENTS, {}
        )
        full_name = f"{self.domain}.{platform_name}"
        if full_name in cache:
            return cache[full_name]

        try:
            cache[full_name] = self._import_platform(platform_name)
        except ImportError:
            raise
        except Exception as err:
            _LOGGER.exception(
                f"Unexpected exception importing platform {self._pkg_path}."
                + f"{platform_name}"
            )
            raise ImportError(
                f"Exception importing {self.pkg_path}.{platform_name}"
            ) from err

        return cache[full_name]

    def _import_platform(self, platform_name: str) -> types.ModuleType:
        """Import the platform."""
        return importlib.import_module(f"{self._pkg_path}.{platform_name}")

    def __repr__(self) -> str:
        """Text representation of class."""
        return f"<Integration {self.domain}: {self._pkg_path}>"
