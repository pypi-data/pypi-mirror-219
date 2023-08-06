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

import functools
import itertools
import json
import os
import pathlib
import re
import typing

import voluptuous as vol
import voluptuous.humanize as vh

from smart_home_tng.core import helpers
from smart_home_tng.core.config_validation import ConfigValidation as cv

from .code_validator import CodeValidator
from .config import Config
from .integration import Integration

_NAME = typing.Final = "translations"
_INTEGRATIONS_DIR: typing.Final = pathlib.Path("smart_home_tng/components")
_FILENAME_FORMAT: typing.Final = re.compile(r"strings\.(?P<suffix>\w+)\.json")

_UNDEFINED: typing.Final = 0
_REQUIRED: typing.Final = 1
_REMOVED: typing.Final = 2

_RE_REFERENCE: typing.Final = r"\[\%key:(.+)\%\]"

# Only allow translatino of integration names if they contain non-brand names
_ALLOW_NAME_TRANSLATION: typing.Final = {
    "cert_expiry",
    "cpuspeed",
    "emulated_roku",
    "faa_delays",
    "garages_amsterdam",
    "google_travel_time",
    "homekit_controller",
    "islamic_prayer_times",
    "local_ip",
    "nmap_tracker",
    "rpi_power",
    "waze_travel_time",
}

_REMOVED_TITLE_MSG: typing.Final = (
    "config.title key has been moved out of config and into the root of strings.json. "
    "Starting Home Assistant 0.109 you only need to define this key in the root "
    "if the title needs to be different than the name of your integration in the "
    "manifest."
)

_MOVED_TRANSLATIONS_DIRECTORY_MSG: typing.Final = (
    "The '.translations' directory has been moved, the new name is 'translations', "
    "starting with Home Assistant 0.112 your translations will no longer "
    "load if you do not move/rename this "
)


def _allow_name_translation(integration: Integration):
    """Validate that the translation name is not the same as the integration name."""
    # Only enforce for core because custom integrations can't be
    # added to allow list.
    return integration.core and (
        integration.domain in _ALLOW_NAME_TRANSLATION
        or integration.quality_scale == "internal"
    )


def _check_translations_directory_name(integration: Integration) -> None:
    """Check that the correct name is used for the translations directory."""
    legacy_translations = integration.path / ".translations"
    translations = integration.path / "translations"

    if translations.is_dir():
        # No action required
        return

    if legacy_translations.is_dir():
        integration.add_error("translations", _MOVED_TRANSLATIONS_DIRECTORY_MSG)


def _find_references(strings, prefix, found):
    """Find references."""
    for key, value in strings.items():
        if isinstance(value, dict):
            _find_references(value, f"{prefix}::{key}", found)
            continue

        match = re.match(_RE_REFERENCE, value)

        if match:
            found.append({"source": f"{prefix}::{key}", "ref": match.groups()[0]})


def _removed_title_validator(config, integration, value):
    """Mark removed title."""
    if not config.specific_integrations:
        raise vol.Invalid(_REMOVED_TITLE_MSG)

    # Don't mark it as an error yet for custom components to allow backwards compat.
    integration.add_warning("translations", _REMOVED_TITLE_MSG)
    return value


def _lowercase_validator(value):
    """Validate value is lowercase."""
    if value.lower() != value:
        raise vol.Invalid("Needs to be lowercase")

    return value


def _gen_data_entry_schema(
    *,
    config: Config,
    integration: Integration,
    flow_title: int,
    require_step_title: bool,
    mandatory_description: str = None,
):
    """Generate a data entry schema."""
    step_title_class = vol.Required if require_step_title else vol.Optional
    schema = {
        vol.Optional("flow_title"): cv.string_with_no_html,
        vol.Required("step"): {
            str: {
                step_title_class("title"): cv.string_with_no_html,
                vol.Optional("description"): cv.string_with_no_html,
                vol.Optional("data"): {str: cv.string_with_no_html},
                vol.Optional("data_description"): {str: cv.string_with_no_html},
                vol.Optional("menu_options"): {str: cv.string_with_no_html},
            }
        },
        vol.Optional("error"): {str: cv.string_with_no_html},
        vol.Optional("abort"): {str: cv.string_with_no_html},
        vol.Optional("progress"): {str: cv.string_with_no_html},
        vol.Optional("create_entry"): {str: cv.string_with_no_html},
    }
    if flow_title == _REQUIRED:
        schema[vol.Required("title")] = cv.string_with_no_html
    elif flow_title == _REMOVED:
        schema[vol.Optional("title", msg=_REMOVED_TITLE_MSG)] = functools.partial(
            _removed_title_validator, config, integration
        )

    def data_description_validator(value):
        """Validate data description."""
        for step_info in value["step"].values():
            if "data_description" not in step_info:
                continue

            for key in step_info["data_description"]:
                if key not in step_info["data"]:
                    raise vol.Invalid(f"data_description key {key} is not in data")

        return value

    validators = [vol.Schema(schema), data_description_validator]

    if mandatory_description is not None:

        def validate_description_set(value):
            """Validate description is set."""
            steps = value["step"]
            if mandatory_description not in steps:
                raise vol.Invalid(f"{mandatory_description} needs to be defined")

            if "description" not in steps[mandatory_description]:
                raise vol.Invalid(f"Step {mandatory_description} needs a description")

            return value

        validators.append(validate_description_set)

    if not _allow_name_translation(integration):

        def name_validator(value):
            """Validate name."""
            for step_id, info in value["step"].items():
                if info.get("title") == integration.name:
                    raise vol.Invalid(
                        f"Do not set title of step {step_id} if it's a brand name "
                        "or add exception to ALLOW_NAME_TRANSLATION"
                    )

            return value

        validators.append(name_validator)

    return vol.All(*validators)


def _gen_strings_schema(config: Config, integration: Integration):
    """Generate a strings schema."""
    return vol.Schema(
        {
            vol.Optional("title"): cv.string_with_no_html,
            vol.Optional("config"): _gen_data_entry_schema(
                config=config,
                integration=integration,
                flow_title=_REMOVED,
                require_step_title=False,
                mandatory_description=(
                    "user" if integration.integration_type == "helper" else None
                ),
            ),
            vol.Optional("options"): _gen_data_entry_schema(
                config=config,
                integration=integration,
                flow_title=_UNDEFINED,
                require_step_title=False,
            ),
            vol.Optional("device_automation"): {
                vol.Optional("action_type"): {str: cv.string_with_no_html},
                vol.Optional("condition_type"): {str: cv.string_with_no_html},
                vol.Optional("trigger_type"): {str: cv.string_with_no_html},
                vol.Optional("trigger_subtype"): {str: cv.string_with_no_html},
            },
            vol.Optional("state"): cv.schema_with_slug_keys(
                cv.schema_with_slug_keys(str, slug_validator=_lowercase_validator),
                slug_validator=vol.Any("_", cv.slug),
            ),
            vol.Optional("system_health"): {
                vol.Optional("info"): {str: cv.string_with_no_html}
            },
            vol.Optional("config_panel"): cv.schema_with_slug_keys(
                cv.schema_with_slug_keys(
                    cv.string_with_no_html, slug_validator=_lowercase_validator
                ),
                slug_validator=vol.Any("_", cv.slug),
            ),
        }
    )


def _gen_auth_schema(config: Config, integration: Integration):
    """Generate auth schema."""
    return vol.Schema(
        {
            vol.Optional("mfa_setup"): {
                str: _gen_data_entry_schema(
                    config=config,
                    integration=integration,
                    flow_title=_REQUIRED,
                    require_step_title=True,
                )
            }
        }
    )


def _gen_platform_strings_schema(_config: Config, integration: Integration):
    """Generate platform strings schema like strings.sensor.json.

    Example of valid data:
    {
        "state": {
            "moon__phase": {
                "full": "Full"
            }
        }
    }
    """

    def device_class_validator(value):
        """Key validator for platform states.

        Platform states are only allowed to provide states for device classes they prefix.
        """
        if not value.startswith(f"{integration.domain}__"):
            raise vol.Invalid(
                f"Device class need to start with '{integration.domain}__'. Key {value} "
                + "is invalid. See https://developers.home-assistant.io/docs/"
                + "internationalization/core#stringssensorjson"
            )

        slug_friendly = value.replace("__", "_", 1)
        slugged = helpers.slugify(slug_friendly)

        if slug_friendly != slugged:
            raise vol.Invalid(
                f"invalid device class {value}. After domain__, "
                + "needs to be all lowercase, no spaces."
            )

        return value

    return vol.Schema(
        {
            vol.Optional("state"): cv.schema_with_slug_keys(
                cv.schema_with_slug_keys(str, slug_validator=_lowercase_validator),
                slug_validator=device_class_validator,
            )
        }
    )


_ONBOARDING_SCHEMA: typing.Final = vol.Schema(
    {vol.Required("area"): {str: cv.string_with_no_html}}
)


def _validate_translation_file(config: Config, integration: Integration, all_strings):
    """Validate translation files for integration."""
    if config.specific_integrations:
        _check_translations_directory_name(integration)

    strings_files = [integration.path / "strings.json"]

    # Also validate translations for custom integrations
    if config.specific_integrations:
        # Only English needs to be always complete
        strings_files.append(integration.path / "translations/en.json")

    references = []

    if integration.domain == "auth":
        strings_schema = _gen_auth_schema(config, integration)
    elif integration.domain == "onboarding":
        strings_schema = _ONBOARDING_SCHEMA
    elif integration.domain == "binary_sensor":
        strings_schema = _gen_strings_schema(config, integration).extend(
            {
                vol.Optional("device_class"): cv.schema_with_slug_keys(
                    cv.string_with_no_html, slug_validator=vol.Any("_", cv.slug)
                )
            }
        )
    else:
        strings_schema = _gen_strings_schema(config, integration)

    for strings_file in strings_files:
        if not strings_file.is_file():
            continue

        name = str(strings_file.relative_to(integration.path))

        try:
            strings = json.loads(strings_file.read_text())
        except ValueError as err:
            integration.add_error("translations", f"Invalid JSON in {name}: {err}")
            continue

        try:
            strings_schema(strings)
        except vol.Invalid as err:
            integration.add_error(
                "translations", f"Invalid {name}: {vh.humanize_error(strings, err)}"
            )
        else:
            if strings_file.name == "strings.json":
                _find_references(strings, name, references)

                if strings.get(
                    "title"
                ) == integration.name and not _allow_name_translation(integration):
                    integration.add_error(
                        "translations",
                        "Don't specify title in translation strings if it's a brand name "
                        + "or add exception to ALLOW_NAME_TRANSLATION",
                    )

    platform_string_schema = _gen_platform_strings_schema(config, integration)
    platform_strings = [integration.path.glob("strings.*.json")]

    if config.specific_integrations:
        platform_strings.append(integration.path.glob("translations/*.en.json"))

    for path in itertools.chain(*platform_strings):
        name = str(path.relative_to(integration.path))

        try:
            strings = json.loads(path.read_text())
        except ValueError as err:
            integration.add_error("translations", f"Invalid JSON in {name}: {err}")
            continue

        try:
            platform_string_schema(strings)
        except vol.Invalid as err:
            msg = f"Invalid {path.name}: {vh.humanize_error(strings, err)}"
            if config.specific_integrations:
                integration.add_warning("translations", msg)
            else:
                integration.add_error("translations", msg)
        else:
            _find_references(strings, path.name, references)

    if config.specific_integrations:
        return

    # Validate references
    for reference in references:
        parts = reference["ref"].split("::")
        search = all_strings
        key = parts.pop(0)
        while parts and key in search:
            search = search[key]
            key = parts.pop(0)

        if parts or key not in search:
            integration.add_error(
                "translations",
                f"{reference['source']} contains invalid reference {reference['ref']}: "
                + f"Could not find {key}",
            )


def _generate_upload_data():
    """Generate the data for uploading."""
    translations = {}
    translations_path = _INTEGRATIONS_DIR.parent / "strings.json"
    if translations_path.is_file():
        translations = json.loads(translations_path.read_text())
    translations["component"] = {}

    for path in _INTEGRATIONS_DIR.glob(f"*{os.sep}strings*.json"):
        component = path.parent.name
        match = _FILENAME_FORMAT.search(path.name)
        platform = match.group("suffix") if match else None

        parent = translations["component"].setdefault(component, {})

        if platform:
            platforms = parent.setdefault("platform", {})
            parent = platforms.setdefault(platform, {})

        parent.update(json.loads(path.read_text()))

    return translations


# pylint: disable=unused-variable
class TranslationValidator(CodeValidator):
    """Validate integration translation files."""

    def __init__(self):
        super().__init__(_NAME)

    def validate(self, integrations: dict[str, Integration], config: Config) -> None:
        """Handle JSON files inside integrations."""
        if config.specific_integrations:
            all_strings = None
        else:
            all_strings = _generate_upload_data()

        for integration in integrations.values():
            _validate_translation_file(config, integration, all_strings)
