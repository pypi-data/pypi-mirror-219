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
import typing

import awesomeversion as asv
import voluptuous as vol
import voluptuous.humanize as vh
from urllib3.util import url

from smart_home_tng.core.config_validation import ConfigValidation as cv
from smart_home_tng.core.platform import Platform

from .code_validator import CodeValidator
from .config import Config
from .integration import Integration

_NAME: typing.Final = "manifest"
_DOCUMENTATION_URL_SCHEMA: typing.Final = "https"
_DOCUMENTATION_URL_HOST: typing.Final = "www.home-assistant.io"
_DOCUMENTATION_URL_PATH_PREFIX: typing.Final = "/integrations/"
_DOCUMENTATION_URL_EXCEPTIONS: typing.Final = {"https://www.home-assistant.io/hassio"}

_SUPPORTED_QUALITY_SCALES: typing.Final = ["gold", "internal", "platinum", "silver"]
_SUPPORTED_IOT_CLASSES: typing.Final = [
    "assumed_state",
    "calculated",
    "cloud_polling",
    "cloud_push",
    "local_polling",
    "local_push",
]

# List of integrations that are supposed to have no IoT class
_NO_IOT_CLASS: typing.Final = [
    *{str(platform) for platform in Platform},
    "api",
    "application_credentials",
    "auth",
    "automation",
    "blueprint",
    "color_extractor",
    "config",
    "configurator",
    "counter",
    "default_config",
    "device_automation",
    "device_tracker",
    "diagnostics",
    "discovery",
    "downloader",
    "ffmpeg",
    "frontend",
    "hardkernel",
    "hardware",
    "history",
    "homeassistant",
    "homeassistant_alerts",
    "homeassistant_yellow",
    "image",
    "input_boolean",
    "input_button",
    "input_datetime",
    "input_number",
    "input_select",
    "input_text",
    "intent_script",
    "intent",
    "logbook",
    "logger",
    "lovelace",
    "map",
    "media_source",
    "my",
    "onboarding",
    "panel_custom",
    "panel_iframe",
    "plant",
    "profiler",
    "proxy",
    "python_script",
    "raspberry_pi",
    "repairs",
    "safe_mode",
    "script",
    "search",
    "system_health",
    "system_log",
    "tag",
    "timer",
    "trace",
    "webhook",
    "websocket_api",
    "zone",
]


def _documentation_url(value: str) -> str:
    """Validate that a documentation url has the correct path and domain."""
    if value in _DOCUMENTATION_URL_EXCEPTIONS:
        return value

    parsed_url = url.parse_url(value)
    if parsed_url.scheme != _DOCUMENTATION_URL_SCHEMA:
        raise vol.Invalid("Documentation url is not prefixed with https")
    if parsed_url.netloc == _DOCUMENTATION_URL_HOST and not parsed_url.path.startswith(
        _DOCUMENTATION_URL_PATH_PREFIX
    ):
        raise vol.Invalid(
            "Documentation url does not begin with www.home-assistant.io/integrations"
        )

    return value


def _verify_lowercase(value: str):
    """Verify a value is lowercase."""
    if value.lower() != value:
        raise vol.Invalid("Value needs to be lowercase")

    return value


def _verify_uppercase(value: str):
    """Verify a value is uppercase."""
    if value.upper() != value:
        raise vol.Invalid("Value needs to be uppercase")

    return value


def _verify_version(value: str):
    """Verify the version."""
    try:
        asv.AwesomeVersion(
            value,
            [
                asv.AwesomeVersionStrategy.CALVER,
                asv.AwesomeVersionStrategy.SEMVER,
                asv.AwesomeVersionStrategy.SIMPLEVER,
                asv.AwesomeVersionStrategy.BUILDVER,
                asv.AwesomeVersionStrategy.PEP440,
            ],
        )
    except asv.AwesomeVersionException as err:
        raise vol.Invalid(f"'{value}' is not a valid version.") from err
    return value


def _verify_wildcard(value: str):
    """Verify the matcher contains a wildcard."""
    if "*" not in value:
        raise vol.Invalid(f"'{value}' needs to contain a wildcard matcher")
    return value


_MANIFEST_SCHEMA: typing.Final = vol.Schema(
    {
        vol.Required("domain"): str,
        vol.Required("name"): str,
        vol.Optional("integration_type"): vol.In(["hardware", "helper"]),
        vol.Optional("config_flow"): bool,
        vol.Optional("mqtt"): [str],
        vol.Optional("zeroconf"): [
            vol.Any(
                str,
                vol.All(
                    cv.deprecated("macaddress"),
                    cv.deprecated("model"),
                    cv.deprecated("manufacturer"),
                    vol.Schema(
                        {
                            vol.Required("type"): str,
                            vol.Optional("macaddress"): vol.All(
                                str, _verify_uppercase, _verify_wildcard
                            ),
                            vol.Optional("manufacturer"): vol.All(
                                str, _verify_lowercase
                            ),
                            vol.Optional("model"): vol.All(str, _verify_lowercase),
                            vol.Optional("name"): vol.All(str, _verify_lowercase),
                            vol.Optional("properties"): vol.Schema(
                                {str: _verify_lowercase}
                            ),
                        }
                    ),
                ),
            )
        ],
        vol.Optional("ssdp"): vol.Schema(
            vol.All([vol.All(vol.Schema({}, extra=vol.ALLOW_EXTRA), vol.Length(min=1))])
        ),
        vol.Optional("homekit"): vol.Schema({vol.Optional("models"): [str]}),
        vol.Optional("dhcp"): [
            vol.Schema(
                {
                    vol.Optional("macaddress"): vol.All(
                        str, _verify_uppercase, _verify_wildcard
                    ),
                    vol.Optional("hostname"): vol.All(str, _verify_lowercase),
                    vol.Optional("registered_devices"): cv.boolean,
                }
            )
        ],
        vol.Optional("usb"): [
            vol.Schema(
                {
                    vol.Optional("vid"): vol.All(str, _verify_uppercase),
                    vol.Optional("pid"): vol.All(str, _verify_uppercase),
                    vol.Optional("serial_number"): vol.All(str, _verify_lowercase),
                    vol.Optional("manufacturer"): vol.All(str, _verify_lowercase),
                    vol.Optional("description"): vol.All(str, _verify_lowercase),
                    vol.Optional("known_devices"): [str],
                }
            )
        ],
        vol.Required("documentation"): vol.All(
            vol.Url(), _documentation_url  # pylint: disable=no-value-for-parameter
        ),
        vol.Optional(
            "issue_tracker"
        ): vol.Url(),  # pylint: disable=no-value-for-parameter
        vol.Optional("quality_scale"): vol.In(_SUPPORTED_QUALITY_SCALES),
        vol.Optional("requirements"): [str],
        vol.Optional("dependencies"): [str],
        vol.Optional("after_dependencies"): [str],
        vol.Required("codeowners"): [str],
        vol.Optional("loggers"): [str],
        vol.Optional("disabled"): str,
        vol.Optional("iot_class"): vol.In(_SUPPORTED_IOT_CLASSES),
        vol.Optional("supported_brands"): vol.Schema({str: str}),
    }
)

_CUSTOM_INTEGRATION_MANIFEST_SCHEMA: typing.Final = _MANIFEST_SCHEMA.extend(
    {
        vol.Optional("version"): vol.All(str, _verify_version),
        vol.Remove("supported_brands"): dict,
    }
)


def _validate_version(integration: Integration):
    """
    Validate the version of the integration.

    Will be removed when the version key is no longer optional for custom integrations.
    """
    if not integration.core and not integration.manifest.get("version"):
        integration.add_error("manifest", "No 'version' key in the manifest file.")
        return


def _validate_manifest(
    integration: Integration, core_components_dir: pathlib.Path
) -> None:
    """Validate manifest."""
    if not integration.manifest:
        return

    try:
        if integration.core:
            _MANIFEST_SCHEMA(integration.manifest)
        else:
            _CUSTOM_INTEGRATION_MANIFEST_SCHEMA(integration.manifest)
    except vol.Invalid as err:
        integration.add_error(
            "manifest",
            f"Invalid manifest: {vh.humanize_error(integration.manifest, err)}",
        )

    if integration.manifest["domain"] != integration.path.name:
        integration.add_error("manifest", "Domain does not match dir name")

    if (
        not integration.core
        and (core_components_dir / integration.manifest["domain"]).exists()
    ):
        integration.add_warning(
            "manifest", "Domain collides with built-in core integration"
        )

    if (
        integration.manifest["domain"] in _NO_IOT_CLASS
        and "iot_class" in integration.manifest
    ):
        integration.add_error("manifest", "Domain should not have an IoT Class")

    if (
        integration.manifest["domain"] not in _NO_IOT_CLASS
        and "iot_class" not in integration.manifest
    ):
        integration.add_error("manifest", "Domain is missing an IoT Class")

    for domain, _name in integration.manifest.get("supported_brands", {}).items():
        if (core_components_dir / domain).exists():
            integration.add_warning(
                "manifest",
                f"Supported brand domain {domain} collides with built-in core integration",
            )

    if not integration.core:
        _validate_version(integration)


# pylint: disable=unused-variable
class ManifestValidator(CodeValidator):
    """Manifest validation."""

    def __init__(self):
        super().__init__(_NAME)

    def validate(self, integrations: dict[str, Integration], config: Config) -> None:
        """Handle all integrations manifests."""
        core_components_dir = config.root / "smart_home_tng/components"
        for integration in integrations.values():
            _validate_manifest(integration, core_components_dir)
