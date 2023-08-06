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

import argparse
import pathlib
import sys
import time
import typing

from .application_credentials import ApplicationCredentialsGenerator
from .code_generator import CodeGenerator
from .codeowners import CodeOwnersGenerator
from .config import Config
from .config_flow import ConfigFlowGenerator
from .dependencies import DependencyValidator
from .dhcp import DhcpGenerator
from .integration import Integration
from .json import JsonValidator
from .manifest import ManifestValidator
from .metadata import MetaDataValidator
from .mqtt import MqttGenerator
from .mypy_config import MyPyGenerator
from .requirements import RequirementsValidator
from .services import ServiceValidator
from .ssdp import SsdpGenerator
from .supported_brands import SupportedBrandsGenerator
from .translations import TranslationValidator
from .usb import UsbGenerator
from .zeroconf import ZeroConfGenerator

_INTEGRATION_PLUGINS: typing.Final = [
    ApplicationCredentialsGenerator(),
    CodeOwnersGenerator(),
    ConfigFlowGenerator(),
    DependencyValidator(),
    DhcpGenerator(),
    JsonValidator(),
    ManifestValidator(),
    MqttGenerator(),
    RequirementsValidator(),
    ServiceValidator(),
    SsdpGenerator(),
    SupportedBrandsGenerator(),
    TranslationValidator(),
    UsbGenerator(),
    ZeroConfGenerator(),
]
_SHC_PLUGINS: typing.Final = [
    MyPyGenerator(),
    MetaDataValidator(),
]

_ALL_PLUGIN_NAMES: typing.Final = [
    plugin.name for plugin in (*_INTEGRATION_PLUGINS, *_SHC_PLUGINS)
]


def _valid_integration_path(integration_path):
    """Test if it's a valid integration."""
    path = pathlib.Path(integration_path)
    if not path.is_dir():
        raise argparse.ArgumentTypeError(f"{integration_path} is not a directory.")

    return path


def _validate_plugins(plugin_names: str) -> list[str]:
    """Split and validate plugin names."""
    all_plugin_names = set(_ALL_PLUGIN_NAMES)
    plugins = plugin_names.split(",")
    for plugin in plugins:
        if plugin not in all_plugin_names:
            raise argparse.ArgumentTypeError(f"{plugin} is not a valid plugin name")

    return plugins


def _get_config() -> Config:
    """Return config."""
    parser = argparse.ArgumentParser(
        description="Smart Home - The Next Generation helper generation from manifests."
    )
    parser.add_argument(
        "--action", type=str, choices=["validate", "generate"], default=None
    )
    parser.add_argument(
        "--integration-path",
        action="append",
        type=_valid_integration_path,
        help="Validate a single integration",
    )
    parser.add_argument(
        "--requirements",
        action="store_true",
        help="Validate requirements",
    )
    parser.add_argument(
        "-p",
        "--plugins",
        type=_validate_plugins,
        default=_ALL_PLUGIN_NAMES,
        help="Comma-separate list of plugins to run. Valid plugin names: %(default)s",
    )
    parsed = parser.parse_args()

    if parsed.action is None:
        parsed.action = "validate" if parsed.integration_path else "generate"

    if parsed.action == "generate" and parsed.integration_path:
        raise RuntimeError(
            "Generate is not allowed when limiting to specific integrations"
        )

    if (
        not parsed.integration_path
        and not pathlib.Path("requirements_all.txt").is_file()
        and not pathlib.Path("smart_home_tng/core").is_dir()
    ):
        raise RuntimeError("Run from Smart Home - The Next Generation root")

    return Config(
        root=pathlib.Path(".").absolute(),
        specific_integrations=parsed.integration_path,
        action=parsed.action,
        requirements=parsed.requirements,
        plugins=set(parsed.plugins),
    )


def _main():
    """Validate manifests."""
    try:
        config = _get_config()
    except RuntimeError as err:
        print(err)
        return 1

    plugins = [*_INTEGRATION_PLUGINS]

    if config.specific_integrations:
        integrations = {}

        for int_path in config.specific_integrations:
            integration = Integration(int_path)
            integration.load_manifest()
            integrations[integration.domain] = integration

    else:
        integrations = Integration.load_dir(pathlib.Path("smart_home_tng/components"))
        plugins += _SHC_PLUGINS

    for plugin in plugins:
        plugin_name = plugin.name
        if plugin_name not in config.plugins:
            continue
        try:
            start = time.monotonic()
            print(f"Validating {plugin_name}...", end="", flush=True)
            if (
                plugin.name == "requirements"
                and config.requirements
                and not config.specific_integrations
            ):
                print()
            plugin.validate(integrations, config)
            print(f" done in {time.monotonic() - start:.2f}s")
        except RuntimeError as err:
            print()
            print()
            print("Error!")
            print(err)
            return 1

    # When we generate, all errors that are fixable will be ignored,
    # as generating them will be fixed.
    if config.action == "generate":
        general_errors = [err for err in config.errors if not err.fixable]
        invalid_itg = [
            itg
            for itg in integrations.values()
            if any(not error.fixable for error in itg.errors)
        ]
    else:
        # action == validate
        general_errors = config.errors
        invalid_itg = [itg for itg in integrations.values() if itg.errors]

    warnings_itg = [itg for itg in integrations.values() if itg.warnings]

    print()
    print("Integrations:", len(integrations))
    print("Invalid integrations:", len(invalid_itg))
    print()

    if not invalid_itg and not general_errors:
        _print_integrations_status(config, warnings_itg, show_fixable_errors=False)

        if config.action == "generate":
            for plugin in plugins:
                plugin_name = plugin.name
                if plugin_name not in config.plugins:
                    continue
                if not isinstance(plugin, CodeGenerator):
                    continue
                plugin.generate(integrations, config)
        return 0

    if config.action == "generate":
        print("Found errors. Generating files canceled.")
        print()

    if general_errors:
        print("General errors:")
        for error in general_errors:
            print("*", error)
        print()

    invalid_itg.extend(itg for itg in warnings_itg if itg not in invalid_itg)

    _print_integrations_status(config, invalid_itg, show_fixable_errors=False)

    return 1


def _print_integrations_status(config, integrations, *, show_fixable_errors=True):
    """Print integration status."""
    for integration in sorted(integrations, key=lambda itg: itg.domain):
        extra = f" - {integration.path}" if config.specific_integrations else ""
        print(f"Integration {integration.domain}{extra}:")
        for error in integration.errors:
            if show_fixable_errors or not error.fixable:
                print("*", "[ERROR]", error)
        for warning in integration.warnings:
            print("*", "[WARNING]", warning)
        print()


if __name__ == "__main__":
    sys.exit(_main())
