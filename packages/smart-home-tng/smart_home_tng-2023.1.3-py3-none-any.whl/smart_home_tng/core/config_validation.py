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

# pylint: disable=unused-variable

import collections.abc
import contextlib
import datetime as sys_dt
import enum as enum_types
import inspect
import logging
import os
import re
import socket
import typing
import uuid

import voluptuous as vol
import voluptuous_serialize as vs
import yarl
from urllib3.util import url as util_url

from ..backports import strenum
from . import helpers
from .binary_sensor import BinarySensor
from .const import Const
from .entity_category import EntityCategory
from .script_variables import ScriptVariables
from .selector import Selector
from .template import Template
from .template_error import TemplateError

# typing typevar
_T = typing.TypeVar("_T")


class _ScriptAction(strenum.LowercaseStrEnum):
    DELAY = enum_types.auto()
    WAIT_TEMPLATE = enum_types.auto()
    CONDITION = enum_types.auto()
    EVENT = enum_types.auto()
    CALL_SERVICE = enum_types.auto()
    DEVICE = enum_types.auto()
    SCENE = enum_types.auto()
    REPEAT = enum_types.auto()
    CHOOSE = enum_types.auto()
    WAIT_FOR_TRIGGER = enum_types.auto()
    VARIABLES = enum_types.auto()
    STOP = enum_types.auto()
    IF = enum_types.auto()
    PARALLEL = enum_types.auto()


def _entities_domain(
    domain: str | list[str],
) -> collections.abc.Callable[[str | list], list[str]]:
    """Validate that entities belong to domain."""
    if isinstance(domain, str):

        def check_invalid(val: str) -> bool:
            return val != domain

    else:

        def check_invalid(val: str) -> bool:
            return val not in domain

    def validate(values: str | list) -> list[str]:
        """Test if entity domain is domain."""
        values = ConfigValidation.entity_ids(values)
        for ent_id in values:
            if check_invalid(helpers.split_entity_id(ent_id)[0]):
                raise vol.Invalid(
                    f"Entity ID '{ent_id}' does not belong to domain '{domain}'"
                )
        return values

    return validate


def _deprecated_tts_platform(value):
    """Validate if platform is deprecated."""
    if value == "google":
        raise vol.Invalid(
            "google tts service has been renamed to google_translate,"
            + " please update your configuration."
        )
    return value


def _valid_tts_base_url(value: str) -> str:
    """Validate base url, return value."""
    url = yarl.URL(ConfigValidation.url(value))

    if url.path != "/":
        raise vol.Invalid("Path should be empty")

    return helpers.normalize_url(value)


class ConfigValidation:
    """Implements the Config Validation using voluptuous"""

    _TIME_PERIOD_ERROR: typing.Final = (
        "offset {} should be format 'HH:MM', 'HH:MM:SS' or 'HH:MM:SS.F'"
    )

    # Smart Home - The Next Generation types
    byte = vol.All(vol.Coerce(int), vol.Range(min=0, max=255))
    small_float = vol.All(vol.Coerce(float), vol.Range(min=0, max=1))
    positive_int = helpers.positive_int
    positive_float = vol.All(vol.Coerce(float), vol.Range(min=0))
    latitude = vol.All(
        vol.Coerce(float), vol.Range(min=-90, max=90), msg="invalid latitude"
    )
    longitude = vol.All(
        vol.Coerce(float), vol.Range(min=-180, max=180), msg="invalid longitude"
    )
    gps = vol.ExactSequence([latitude, longitude])
    sun_event = vol.All(
        vol.Lower, vol.Any(Const.SUN_EVENT_SUNSET, Const.SUN_EVENT_SUNRISE)
    )
    port = vol.All(vol.Coerce(int), vol.Range(min=1, max=65535))

    SCRIPT_ACTION_DELAY: typing.Final = _ScriptAction.DELAY
    SCRIPT_ACTION_WAIT_TEMPLATE: typing.Final = _ScriptAction.WAIT_TEMPLATE
    SCRIPT_ACTION_CHECK_CONDITION: typing.Final = _ScriptAction.CONDITION
    SCRIPT_ACTION_FIRE_EVENT: typing.Final = _ScriptAction.EVENT
    SCRIPT_ACTION_CALL_SERVICE: typing.Final = _ScriptAction.CALL_SERVICE
    SCRIPT_ACTION_DEVICE_AUTOMATION: typing.Final = _ScriptAction.DEVICE
    SCRIPT_ACTION_ACTIVATE_SCENE: typing.Final = _ScriptAction.SCENE
    SCRIPT_ACTION_REPEAT: typing.Final = _ScriptAction.REPEAT
    SCRIPT_ACTION_CHOOSE: typing.Final = _ScriptAction.CHOOSE
    SCRIPT_ACTION_WAIT_FOR_TRIGGER: typing.Final = _ScriptAction.WAIT_FOR_TRIGGER
    SCRIPT_ACTION_VARIABLES: typing.Final = _ScriptAction.VARIABLES
    SCRIPT_ACTION_STOP: typing.Final = _ScriptAction.STOP
    SCRIPT_ACTION_IF: typing.Final = _ScriptAction.IF
    SCRIPT_ACTION_PARALLEL: typing.Final = _ScriptAction.PARALLEL

    @staticmethod
    def path(value: typing.Any) -> str:
        """Validate it's a safe path."""
        if not isinstance(value, str):
            raise vol.Invalid("Expected a string")

        try:
            helpers.raise_if_invalid_path(value)
        except ValueError as err:
            raise vol.Invalid("Invalid path") from err

        return value

    # Adapted from:
    # https://github.com/alecthomas/voluptuous/issues/115#issuecomment-144464666
    @staticmethod
    def has_at_least_one_key(
        *keys: typing.Any,
    ) -> collections.abc.Callable[[dict], dict]:
        """Validate that at least one key exists."""

        def validate(obj: dict) -> dict:
            """Test keys exist in dict."""
            if not isinstance(obj, dict):
                raise vol.Invalid("expected dictionary")

            for k in obj:
                if k in keys:
                    return obj
            expected = ", ".join(str(k) for k in keys)
            raise vol.Invalid(f"must contain at least one of {expected}.")

        return validate

    @staticmethod
    def has_at_most_one_key(
        *keys: typing.Any,
    ) -> collections.abc.Callable[[dict], dict]:
        """Validate that zero keys exist or one key exists."""

        def validate(obj: dict) -> dict:
            """Test zero keys exist or one key exists in dict."""
            if not isinstance(obj, dict):
                raise vol.Invalid("expected dictionary")

            if len(set(keys) & set(obj)) > 1:
                expected = ", ".join(str(k) for k in keys)
                raise vol.Invalid(f"must contain at most one of {expected}.")
            return obj

        return validate

    _WS: typing.Final = re.compile("\\s*")

    @staticmethod
    def whitespace(value: typing.Any) -> str:
        """Validate result contains only whitespace."""
        if isinstance(value, str) and ConfigValidation._WS.fullmatch(value):
            return value

        raise vol.Invalid(f"contains non-whitespace: {value}")

    @staticmethod
    def isdevice(value: typing.Any) -> str:
        """Validate that value is a real device."""
        try:
            os.stat(value)
            return str(value)
        except OSError as err:
            raise vol.Invalid(f"No device at {value} found") from err

    @staticmethod
    def matches_regex(regex: str) -> collections.abc.Callable[[typing.Any], str]:
        """Validate that the value is a string that matches a regex."""
        compiled = re.compile(regex)

        def validator(value: typing.Any) -> str:
            """Validate that value matches the given regex."""
            if not isinstance(value, str):
                raise vol.Invalid(f"not a string value: {value}")

            if not compiled.match(value):
                raise vol.Invalid(
                    f"value {value} does not match regular expression {compiled.pattern}"
                )

            return value

        return validator

    @staticmethod
    def is_regex(value: typing.Any) -> re.Pattern[typing.Any]:
        """Validate that a string is a valid regular expression."""
        try:
            r = re.compile(value)
            return r
        except TypeError as err:
            raise vol.Invalid(
                f"value {value} is of the wrong type for a regular expression"
            ) from err
        except re.error as err:
            raise vol.Invalid(
                f"value {value} is not a valid regular expression"
            ) from err

    @staticmethod
    def isfile(value: typing.Any) -> str:
        """Validate that the value is an existing file."""
        if value is None:
            raise vol.Invalid("None is not file")
        file_in = os.path.expanduser(str(value))

        if not os.path.isfile(file_in):
            raise vol.Invalid("not a file")
        if not os.access(file_in, os.R_OK):
            raise vol.Invalid("file not readable")
        return file_in

    @staticmethod
    def isdir(value: typing.Any) -> str:
        """Validate that the value is an existing dir."""
        if value is None:
            raise vol.Invalid("not a directory")
        dir_in = os.path.expanduser(str(value))

        if not os.path.isdir(dir_in):
            raise vol.Invalid("not a directory")
        if not os.access(dir_in, os.R_OK):
            raise vol.Invalid("directory not readable")
        return dir_in

    @staticmethod
    def ensure_list(value: _T) -> list[_T] | list[typing.Any]:
        """Wrap value in list if it is not one."""
        if value is None:
            return []
        return typing.cast("list[_T]", value) if isinstance(value, list) else [value]

    @staticmethod
    def entity_id(value: typing.Any) -> str:
        """Validate Entity ID."""
        str_value = ConfigValidation.string(value).lower()
        if helpers.valid_entity_id(str_value):
            return str_value

        raise vol.Invalid(f"Entity ID {value} is an invalid entity ID")

    @staticmethod
    def entity_id_or_uuid(value: typing.Any) -> str:
        """Validate Entity specified by entity_id or uuid."""
        with contextlib.suppress(vol.Invalid):
            return ConfigValidation.entity_id(value)
        with contextlib.suppress(vol.Invalid):
            return ConfigValidation.fake_uuid4_hex(value)
        raise vol.Invalid(
            f"Entity {value} is neither a valid entity ID nor a valid UUID"
        )

    @staticmethod
    def _entity_ids(value: str | list, allow_uuid: bool) -> list[str]:
        """Help validate entity IDs or UUIDs."""
        if value is None:
            raise vol.Invalid("Entity IDs can not be None")
        if isinstance(value, str):
            value = [ent_id.strip() for ent_id in value.split(",")]

        validator = (
            ConfigValidation.entity_id_or_uuid
            if allow_uuid
            else ConfigValidation.entity_id
        )
        return [validator(ent_id) for ent_id in value]

    @staticmethod
    def entity_ids(value: str | list) -> list[str]:
        """Validate Entity IDs."""
        return ConfigValidation._entity_ids(value, False)

    @staticmethod
    def entity_ids_or_uuids(value: str | list) -> list[str]:
        """Validate entities specified by entity IDs or UUIDs."""
        return ConfigValidation._entity_ids(value, True)

    comp_entity_ids = vol.Any(
        vol.All(vol.Lower, vol.Any(Const.ENTITY_MATCH_ALL, Const.ENTITY_MATCH_NONE)),
        entity_ids,
    )

    comp_entity_ids_or_uuids = vol.Any(
        vol.All(vol.Lower, vol.Any(Const.ENTITY_MATCH_ALL, Const.ENTITY_MATCH_NONE)),
        entity_ids_or_uuids,
    )

    @staticmethod
    def entity_domain(
        domain: str | list[str],
    ) -> collections.abc.Callable[[typing.Any], str]:
        """Validate that entity belong to domain."""
        ent_domain = _entities_domain(domain)

        def validate(value: str) -> str:
            """Test if entity domain is domain."""
            validated = ent_domain(value)
            if len(validated) != 1:
                raise vol.Invalid(f"Expected exactly 1 entity, got {len(validated)}")
            return validated[0]

        return validate

    @staticmethod
    def entities_domain(
        domain: str | list[str],
    ) -> collections.abc.Callable[[str | list], list[str]]:
        """Validate that entities belong to domain."""
        return _entities_domain(domain)

    @staticmethod
    def enum(enum_class: type[enum_types.Enum]) -> vol.All:
        """Create validator for specified enum."""
        return vol.All(vol.In(enum_class.__members__), enum_class.__getitem__)

    @staticmethod
    def icon(value: typing.Any) -> str:
        """Validate icon."""
        str_value = str(value)

        if ":" in str_value:
            return str_value

        raise vol.Invalid('Icons should be specified in the form "prefix:name"')

    time_period_dict = vol.All(
        dict,
        vol.Schema(
            {
                "days": vol.Coerce(float),
                "hours": vol.Coerce(float),
                "minutes": vol.Coerce(float),
                "seconds": vol.Coerce(float),
                "milliseconds": vol.Coerce(float),
            }
        ),
        has_at_least_one_key("days", "hours", "minutes", "seconds", "milliseconds"),
        lambda value: sys_dt.timedelta(**value),
    )

    @staticmethod
    def time(value: typing.Any) -> sys_dt.time:
        """Validate and transform a time."""
        if isinstance(value, sys_dt.time):
            return value

        try:
            time_val = helpers.parse_time(value)
        except TypeError as err:
            raise vol.Invalid("Not a parseable type") from err

        if time_val is None:
            raise vol.Invalid(f"Invalid time specified: {value}")

        return time_val

    @staticmethod
    def date(value: typing.Any) -> sys_dt.date:
        """Validate and transform a date."""
        if isinstance(value, sys_dt.date):
            return value

        try:
            date_val = helpers.parse_date(value)
        except TypeError as err:
            raise vol.Invalid("Not a parseable type") from err

        if date_val is None:
            raise vol.Invalid("Could not parse date")

        return date_val

    @staticmethod
    def time_period_str(value: str) -> sys_dt.timedelta:
        """Validate and transform time offset."""
        if isinstance(value, int):  # type: ignore[unreachable]
            raise vol.Invalid("Make sure you wrap time values in quotes")
        if not isinstance(value, str):
            raise vol.Invalid(ConfigValidation._TIME_PERIOD_ERROR.format(value))

        negative_offset = False
        if value.startswith("-"):
            negative_offset = True
            value = value[1:]
        elif value.startswith("+"):
            value = value[1:]

        parsed = value.split(":")
        if len(parsed) not in (2, 3):
            raise vol.Invalid(ConfigValidation._TIME_PERIOD_ERROR.format(value))
        try:
            hour = int(parsed[0])
            minute = int(parsed[1])
            try:
                second = float(parsed[2])
            except IndexError:
                second = 0
        except ValueError as err:
            raise vol.Invalid(
                ConfigValidation._TIME_PERIOD_ERROR.format(value)
            ) from err

        offset = sys_dt.timedelta(hours=hour, minutes=minute, seconds=second)

        if negative_offset:
            offset *= -1

        return offset

    @staticmethod
    def time_period_seconds(value: float | str) -> sys_dt.timedelta:
        """Validate and transform seconds to a time offset."""
        try:
            return sys_dt.timedelta(seconds=float(value))
        except (ValueError, TypeError) as err:
            raise vol.Invalid(f"Expected seconds, got {value}") from err

    time_period = vol.Any(
        time_period_str, time_period_seconds, sys_dt.timedelta, time_period_dict
    )

    @staticmethod
    def match_all(value: _T) -> _T:
        """Validate that matches all values."""
        return value

    @staticmethod
    def positive_timedelta(value: sys_dt.timedelta) -> sys_dt.timedelta:
        """Validate timedelta is positive."""
        if value < sys_dt.timedelta(0):
            raise vol.Invalid("Time period should be positive")
        return value

    positive_time_period_dict = vol.All(time_period_dict, positive_timedelta)
    positive_time_period = vol.All(time_period, positive_timedelta)

    @staticmethod
    def remove_falsy(value: list[_T]) -> list[_T]:
        """Remove falsy values from a list."""
        return [v for v in value if v]

    @staticmethod
    def service(value: typing.Any) -> str:
        """Validate service."""
        # Services use same format as entities so we can use same helper.
        str_value = ConfigValidation.string(value).lower()
        if helpers.valid_entity_id(str_value):
            return str_value

        raise vol.Invalid(f"Service {value} does not match format <domain>.<name>")

    @staticmethod
    def slug(value: typing.Any) -> str:
        """Validate value is a valid slug."""
        if value is None:
            raise vol.Invalid("Slug should not be None")
        str_value = str(value)
        slg = helpers.slugify(str_value)
        if str_value == slg:
            return str_value
        raise vol.Invalid(f"invalid slug {value} (try {slg})")

    @staticmethod
    def schema_with_slug_keys(
        value_schema: _T | collections.abc.Callable,
        *,
        slug_validator: collections.abc.Callable[[typing.Any], str] = slug,
    ) -> collections.abc.Callable:
        """Ensure dicts have slugs as keys.

        Replacement of vol.Schema({cv.slug: value_schema}) to prevent misleading
        "Extra keys" errors from voluptuous.
        """
        schema = vol.Schema({str: value_schema})

        def verify(value: dict) -> dict:
            """Validate all keys are slugs and then the value_schema."""
            if not isinstance(value, dict):
                raise vol.Invalid("expected dictionary")

            for key in value.keys():
                slug_validator(key)

            return typing.cast(dict, schema(value))

        return verify

    @staticmethod
    def slugify(value: typing.Any) -> str:
        """Coerce a value to a slug."""
        if value is None:
            raise vol.Invalid("Slug should not be None")
        slg = helpers.slugify(str(value))
        if slg:
            return slg
        raise vol.Invalid(f"Unable to slugify {value}")

    string = helpers.string

    @staticmethod
    def string_with_no_html(value: typing.Any) -> str:
        """Validate that the value is a string without HTML."""
        value = ConfigValidation.string(value)
        regex = re.compile(r"<[a-z][\s\S]*>")
        if regex.search(value):
            raise vol.Invalid("the string should not contain HTML")
        return str(value)

    @staticmethod
    def temperature_unit(value: typing.Any) -> str:
        """Validate and transform temperature unit."""
        value = str(value).upper()
        if value == "C":
            return Const.TEMP_CELSIUS
        if value == "F":
            return Const.TEMP_FAHRENHEIT
        raise vol.Invalid("invalid temperature unit (expected C or F)")

    unit_system = vol.All(
        vol.Lower,
        vol.Any(Const.CONF_UNIT_SYSTEM_METRIC, Const.CONF_UNIT_SYSTEM_IMPERIAL),
    )

    @staticmethod
    def template(value: typing.Any) -> Template:
        """Validate a jinja2 template."""
        if value is None:
            raise vol.Invalid("template value is None")
        if isinstance(value, (list, dict, Template)):
            raise vol.Invalid("template value should be a string")

        template_value = Template(str(value))  # type: ignore[no-untyped-call]

        try:
            template_value.ensure_valid()
            return template_value
        except TemplateError as ex:
            raise vol.Invalid(f"invalid template ({ex})") from ex

    @staticmethod
    def dynamic_template(value: typing.Any) -> Template:
        """Validate a dynamic (non static) jinja2 template."""
        if value is None:
            raise vol.Invalid("template value is None")
        if isinstance(value, (list, dict, Template)):
            raise vol.Invalid("template value should be a string")
        if not Template.is_template_string(str(value)):
            raise vol.Invalid("template value does not contain a dynamic template")

        template_value = Template(str(value))  # type: ignore[no-untyped-call]
        try:
            template_value.ensure_valid()
            return template_value
        except TemplateError as ex:
            raise vol.Invalid(f"invalid template ({ex})") from ex

    @staticmethod
    def template_complex(value: typing.Any) -> typing.Any:
        """Validate a complex jinja2 template."""
        if isinstance(value, list):
            return_list = value.copy()
            for idx, element in enumerate(return_list):
                return_list[idx] = ConfigValidation.template_complex(element)
            return return_list
        if isinstance(value, dict):
            return {
                ConfigValidation.template_complex(
                    key
                ): ConfigValidation.template_complex(element)
                for key, element in value.items()
            }
        if isinstance(value, str) and Template.is_template_string(value):
            return ConfigValidation.template(value)

        return value

    positive_time_period_template = vol.Any(
        positive_time_period, template, template_complex
    )

    @staticmethod
    def datetime(value: typing.Any) -> sys_dt.datetime:
        """Validate datetime."""
        if isinstance(value, sys_dt.datetime):
            return value

        try:
            date_val = helpers.parse_datetime(value)
        except TypeError:
            date_val = None

        if date_val is None:
            raise vol.Invalid(f"Invalid datetime specified: {value}")

        return date_val

    @staticmethod
    def time_zone(value: str) -> str:
        """Validate timezone."""
        if helpers.get_time_zone(value) is not None:
            return value
        raise vol.Invalid(
            "Invalid time zone passed in. Valid options can be found here: "
            + "http://en.wikipedia.org/wiki/List_of_tz_database_time_zones"
        )

    weekdays = vol.All(ensure_list, [vol.In(Const.WEEKDAYS)])

    @staticmethod
    def socket_timeout(value: typing.Any) -> object:
        """Validate timeout float > 0.0.

        None coerced to socket._GLOBAL_DEFAULT_TIMEOUT bare object.
        """
        if value is None:
            return socket._GLOBAL_DEFAULT_TIMEOUT  # pylint: disable=protected-access
        try:
            float_value = float(value)
            if float_value > 0.0:
                return float_value
            raise vol.Invalid("Invalid socket timeout value. float > 0.0 required.")
        except Exception as err:
            raise vol.Invalid(f"Invalid socket timeout: {err}")

    # pylint: disable=no-value-for-parameter
    @staticmethod
    def url(value: typing.Any) -> str:
        """Validate an URL."""
        url_in = str(value)

        if util_url.parse_url(url_in).scheme in ["http", "https"]:
            return typing.cast(str, vol.Schema(vol.Url())(url_in))

        raise vol.Invalid("invalid url")

    @staticmethod
    def url_no_path(value: typing.Any) -> str:
        """Validate a url without a path."""
        url_in = ConfigValidation.url(value)

        if util_url.parse_url(url_in).path not in ("", "/"):
            raise vol.Invalid("url it not allowed to have a path component")

        return url_in

    _X10: typing.Final = re.compile(r"([A-Pa-p]{1})(?:[2-9]|1[0-6]?)$")

    @staticmethod
    def x10_address(value: str) -> str:
        """Validate an x10 address."""
        if not ConfigValidation._X10.match(value):
            raise vol.Invalid("Invalid X10 Address")
        return str(value).lower()

    @staticmethod
    def uuid4_hex(value: typing.Any) -> str:
        """Validate a v4 UUID in hex format."""
        try:
            result = uuid.UUID(value, version=4)
        except (ValueError, AttributeError, TypeError) as error:
            raise vol.Invalid("Invalid Version4 UUID", error_message=str(error))

        if result.hex != value.lower():
            # UUID() will create a uuid4 if input is invalid
            raise vol.Invalid("Invalid Version4 UUID")

        return result.hex

    _FAKE_UUID_4_HEX: typing.Final = re.compile(r"^[0-9a-f]{32}$")

    @staticmethod
    def fake_uuid4_hex(value: typing.Any) -> str:
        """Validate a fake v4 UUID generated by random_uuid_hex."""
        try:
            if not ConfigValidation._FAKE_UUID_4_HEX.match(value):
                raise vol.Invalid("Invalid UUID")
        except TypeError as exc:
            raise vol.Invalid("Invalid UUID") from exc
        return typing.cast(str, value)  # Pattern.match throws if input is not a string

    @staticmethod
    def ensure_list_csv(value: typing.Any) -> list:
        """Ensure that input is a list or make one from comma-separated string."""
        if isinstance(value, str):
            return [member.strip() for member in value.split(",")]
        return ConfigValidation.ensure_list(value)

    class MultiSelect:
        """Multi select validator returning list of selected values."""

        def __init__(self, options: dict) -> None:
            """Initialize multi select."""
            self.options = options

        def __call__(self, selected: list) -> list:
            """Validate input."""
            if not isinstance(selected, list):
                raise vol.Invalid("Not a list")

            for value in selected:
                if value not in self.options:
                    raise vol.Invalid(f"{value} is not a valid option")

            return selected

    multi_select = MultiSelect

    @staticmethod
    def _deprecated_or_removed(
        key: str,
        replacement_key: str,
        default: typing.Any,
        raise_if_present: bool,
        option_removed: bool,
    ) -> collections.abc.Callable[[dict], dict]:
        """
        Log key as deprecated and provide a replacement (if exists) or fail.

        Expected behavior:
            - Outputs or throws the appropriate deprecation warning if key is detected
            - Outputs or throws the appropriate error if key is detected and removed from support
            - Processes schema moving the value from key to replacement_key
            - Processes schema changing nothing if only replacement_key provided
            - No warning if only replacement_key provided
            - No warning if neither key nor replacement_key are provided
                - Adds replacement_key with default value in this case
        """
        module = inspect.getmodule(inspect.stack(context=0)[2].frame)
        if module is not None:
            module_name = module.__name__
        else:
            # If Python is unable to access the sources files, the call stack frame
            # will be missing information, so let's guard.
            # https://github.com/home-assistant/core/issues/24982
            module_name = __name__
        if option_removed:
            logger_func = logging.getLogger(module_name).error
            option_status = "has been removed"
        else:
            logger_func = logging.getLogger(module_name).warning
            option_status = "is deprecated"

        def validator(config: dict) -> dict:
            """Check if key is in config and log warning or error."""
            if key in config:
                try:
                    near = f"near {config.__config_file__}:{config.__line__} "
                except AttributeError:
                    near = ""
                arguments: tuple[str, ...]
                if replacement_key:
                    warning = "The '%s' option %s%s, please replace it with '%s'"
                    arguments = (key, near, option_status, replacement_key)
                else:
                    warning = (
                        "The '%s' option %s%s, please remove it from your configuration"
                    )
                    arguments = (key, near, option_status)

                if raise_if_present:
                    raise vol.Invalid(warning % arguments)

                logger_func(warning, *arguments)
                value = config[key]
                if replacement_key:
                    config.pop(key)
            else:
                value = default

            keys = [key]
            if replacement_key:
                keys.append(replacement_key)
                if value is not None and (
                    replacement_key not in config
                    or default == config.get(replacement_key)
                ):
                    config[replacement_key] = value

            return ConfigValidation.has_at_most_one_key(*keys)(config)

        return validator

    @staticmethod
    def deprecated(
        key: str,
        replacement_key: str = None,
        default: typing.Any = None,
        raise_if_present: bool = False,
    ) -> collections.abc.Callable[[dict], dict]:
        """
        Log key as deprecated and provide a replacement (if exists).

        Expected behavior:
            - Outputs the appropriate deprecation warning if key is detected or raises an exception
            - Processes schema moving the value from key to replacement_key
            - Processes schema changing nothing if only replacement_key provided
            - No warning if only replacement_key provided
            - No warning if neither key nor replacement_key are provided
                - Adds replacement_key with default value in this case
        """
        return ConfigValidation._deprecated_or_removed(
            key,
            replacement_key=replacement_key,
            default=default,
            raise_if_present=raise_if_present or False,
            option_removed=False,
        )

    @staticmethod
    def removed(
        key: str,
        default: typing.Any = None,
        raise_if_present: bool = True,
    ) -> collections.abc.Callable[[dict], dict]:
        """
        Log key as deprecated and fail the config validation.

        Expected behavior:
            - Outputs the appropriate error if key is detected and removed from
            support or raises an exception
        """
        return ConfigValidation._deprecated_or_removed(
            key,
            replacement_key=None,
            default=default,
            raise_if_present=raise_if_present or False,
            option_removed=True,
        )

    @staticmethod
    def key_value_schemas(
        key: str,
        value_schemas: dict[collections.abc.Hashable, vol.Schema],
        default_schema: vol.Schema = None,
        default_description: str = None,
    ) -> collections.abc.Callable[
        [typing.Any], dict[collections.abc.Hashable, typing.Any]
    ]:
        """Create a validator that validates based on a value for specific key.

        This gives better error messages.
        """

        def key_value_validator(
            value: typing.Any,
        ) -> dict[collections.abc.Hashable, typing.Any]:
            if not isinstance(value, dict):
                raise vol.Invalid("Expected a dictionary")

            key_value = value.get(key)

            if (
                isinstance(key_value, collections.abc.Hashable)
                and key_value in value_schemas
            ):
                return typing.cast(
                    dict[collections.abc.Hashable, typing.Any],
                    value_schemas[key_value](value),
                )

            if default_schema:
                with contextlib.suppress(vol.Invalid):
                    return typing.cast(
                        dict[collections.abc.Hashable, typing.Any],
                        default_schema(value),
                    )

            alternatives = ", ".join(str(key) for key in value_schemas)
            if default_description:
                alternatives += ", " + default_description
            raise vol.Invalid(
                f"Unexpected value for {key}: '{key_value}'. Expected {alternatives}"
            )

        return key_value_validator

    # Validator helpers

    @staticmethod
    def key_dependency(
        key: collections.abc.Hashable, dependency: collections.abc.Hashable
    ) -> collections.abc.Callable[
        [dict[collections.abc.Hashable, typing.Any]],
        dict[collections.abc.Hashable, typing.Any],
    ]:
        """Validate that all dependencies exist for key."""

        def validator(
            value: dict[typing.Hashable, typing.Any]
        ) -> dict[collections.abc.Hashable, typing.Any]:
            """Test dependencies."""
            if not isinstance(value, dict):
                raise vol.Invalid("key dependencies require a dict")
            if key in value and dependency not in value:
                raise vol.Invalid(
                    f'dependency violation - key "{key}" requires '
                    f'key "{dependency}" to exist'
                )

            return value

        return validator

    @staticmethod
    def custom_serializer(schema: typing.Any) -> typing.Any:
        """Serialize additional types for voluptuous_serialize."""

        if schema is ConfigValidation.positive_time_period_dict:
            return {"type": "positive_time_period_dict"}

        if schema is ConfigValidation.string:
            return {"type": "string"}

        if schema is ConfigValidation.boolean:
            return {"type": "boolean"}

        if isinstance(schema, ConfigValidation.MultiSelect):
            return {"type": "multi_select", "options": schema.options}

        if isinstance(schema, Selector):
            return schema.serialize()

        return vs.UNSUPPORTED

    @staticmethod
    def expand_condition_shorthand(value: typing.Any) -> typing.Any:
        """Expand boolean condition shorthand notations."""

        if not isinstance(value, dict) or Const.CONF_CONDITIONS in value:
            return value

        for key, schema in (
            ("and", ConfigValidation.AND_CONDITION_SHORTHAND_SCHEMA),
            ("or", ConfigValidation.OR_CONDITION_SHORTHAND_SCHEMA),
            ("not", ConfigValidation.NOT_CONDITION_SHORTHAND_SCHEMA),
        ):
            try:
                schema(value)
                return {
                    Const.CONF_CONDITION: key,
                    Const.CONF_CONDITIONS: value[key],
                    **{k: value[k] for k in value if k != key},
                }
            except vol.MultipleInvalid:
                pass

        if isinstance(value.get(Const.CONF_CONDITION), list):
            try:
                ConfigValidation.CONDITION_SHORTHAND_SCHEMA(value)
                return {
                    Const.CONF_CONDITION: "and",
                    Const.CONF_CONDITIONS: value[Const.CONF_CONDITION],
                    **{k: value[k] for k in value if k != Const.CONF_CONDITION},
                }
            except vol.MultipleInvalid:
                pass

        return value

    split_entity_id = helpers.split_entity_id
    valid_entity_id = helpers.valid_entity_id
    boolean = helpers.boolean

    # Schemas
    PLATFORM_SCHEMA: typing.Final = vol.Schema(
        {
            vol.Required(Const.CONF_PLATFORM): string,
            vol.Optional(Const.CONF_ENTITY_NAMESPACE): string,
            vol.Optional(Const.CONF_SCAN_INTERVAL): time_period,
        }
    )

    PLATFORM_SCHEMA_BASE: typing.Final = PLATFORM_SCHEMA.extend(
        {}, extra=vol.ALLOW_EXTRA
    )

    ENTITY_SERVICE_FIELDS: typing.Final = {
        # Either accept static entity IDs, a single dynamic template or a mixed list
        # of static and dynamic templates. While this could be solved with a single
        # complex template, handling it like this, keeps config validation useful.
        vol.Optional(Const.ATTR_ENTITY_ID): vol.Any(
            comp_entity_ids, dynamic_template, vol.All(list, template_complex)
        ),
        vol.Optional(Const.ATTR_DEVICE_ID): vol.Any(
            Const.ENTITY_MATCH_NONE,
            vol.All(ensure_list, [vol.Any(dynamic_template, str)]),
        ),
        vol.Optional(Const.ATTR_AREA_ID): vol.Any(
            Const.ENTITY_MATCH_NONE,
            vol.All(ensure_list, [vol.Any(dynamic_template, str)]),
        ),
    }

    TARGET_SERVICE_FIELDS: typing.Final = {
        # Same as ENTITY_SERVICE_FIELDS but supports specifying entity by entity registry
        # ID.
        # Either accept static entity IDs, a single dynamic template or a mixed list
        # of static and dynamic templates. While this could be solved with a single
        # complex template, handling it like this, keeps config validation useful.
        vol.Optional(Const.ATTR_ENTITY_ID): vol.Any(
            comp_entity_ids_or_uuids, dynamic_template, vol.All(list, template_complex)
        ),
        vol.Optional(Const.ATTR_DEVICE_ID): vol.Any(
            Const.ENTITY_MATCH_NONE,
            vol.All(ensure_list, [vol.Any(dynamic_template, str)]),
        ),
        vol.Optional(Const.ATTR_AREA_ID): vol.Any(
            Const.ENTITY_MATCH_NONE,
            vol.All(ensure_list, [vol.Any(dynamic_template, str)]),
        ),
    }

    @staticmethod
    def make_entity_service_schema(
        schema: dict, *, extra: int = vol.PREVENT_EXTRA
    ) -> vol.Schema:
        """Create an entity service schema."""
        return vol.Schema(
            vol.All(
                vol.Schema(
                    {
                        # The frontend stores data here. Don't use in core.
                        vol.Remove("metadata"): dict,
                        **schema,
                        **ConfigValidation.ENTITY_SERVICE_FIELDS,
                    },
                    extra=extra,
                ),
                ConfigValidation.has_at_least_one_key(
                    *ConfigValidation.ENTITY_SERVICE_FIELDS
                ),
            )
        )

    SCRIPT_VARIABLES_SCHEMA: typing.Final = vol.All(
        vol.Schema({str: template_complex}),
        # pylint: disable=unnecessary-lambda
        lambda val: ScriptVariables(val),
    )

    @staticmethod
    def script_action(value: typing.Any) -> dict:
        """Validate a script action."""
        if not isinstance(value, dict):
            raise vol.Invalid("expected dictionary")

        try:
            action = ConfigValidation.determine_script_action(value)
        except ValueError as err:
            raise vol.Invalid(str(err))

        return ConfigValidation.ACTION_TYPE_SCHEMAS[action](value)

    SCRIPT_SCHEMA: typing.Final = vol.All(ensure_list, [script_action])

    SCRIPT_ACTION_BASE_SCHEMA: typing.Final = {
        vol.Optional(Const.CONF_ALIAS): string,
        vol.Optional(Const.CONF_CONTINUE_ON_ERROR): boolean,
        vol.Optional(Const.CONF_ENABLED): boolean,
    }

    EVENT_SCHEMA: typing.Final = vol.Schema(
        {
            **SCRIPT_ACTION_BASE_SCHEMA,
            vol.Required(Const.CONF_EVENT): string,
            vol.Optional(Const.CONF_EVENT_DATA): vol.All(dict, template_complex),
            vol.Optional(Const.CONF_EVENT_DATA_TEMPLATE): vol.All(
                dict, template_complex
            ),
        }
    )

    SERVICE_SCHEMA: typing.Final = vol.All(
        vol.Schema(
            {
                **SCRIPT_ACTION_BASE_SCHEMA,
                vol.Exclusive(Const.CONF_SERVICE, "service name"): vol.Any(
                    service, dynamic_template
                ),
                vol.Exclusive(Const.CONF_SERVICE_TEMPLATE, "service name"): vol.Any(
                    service, dynamic_template
                ),
                vol.Optional("data"): vol.Any(
                    template, vol.All(dict, template_complex)
                ),
                vol.Optional("data_template"): vol.Any(
                    template, vol.All(dict, template_complex)
                ),
                vol.Optional(Const.CONF_ENTITY_ID): comp_entity_ids,
                vol.Optional(Const.CONF_TARGET): vol.Any(
                    TARGET_SERVICE_FIELDS, dynamic_template
                ),
                # The frontend stores data here. Don't use in core.
                vol.Remove("metadata"): dict,
            }
        ),
        has_at_least_one_key(Const.CONF_SERVICE, Const.CONF_SERVICE_TEMPLATE),
    )

    NUMERIC_STATE_THRESHOLD_SCHEMA: typing.Final = vol.Any(
        vol.Coerce(float),
        vol.All(str, entity_domain(["input_number", "number", "sensor"])),
    )

    CONDITION_BASE_SCHEMA: typing.Final = {
        vol.Optional(Const.CONF_ALIAS): string,
        vol.Optional(Const.CONF_ENABLED): boolean,
    }

    NUMERIC_STATE_CONDITION_SCHEMA: typing.Final = vol.All(
        vol.Schema(
            {
                **CONDITION_BASE_SCHEMA,
                vol.Required(Const.CONF_CONDITION): "numeric_state",
                vol.Required(Const.CONF_ENTITY_ID): entity_ids_or_uuids,
                vol.Optional(Const.CONF_ATTRIBUTE): str,
                Const.CONF_BELOW: NUMERIC_STATE_THRESHOLD_SCHEMA,
                Const.CONF_ABOVE: NUMERIC_STATE_THRESHOLD_SCHEMA,
                vol.Optional(Const.CONF_VALUE_TEMPLATE): template,
            }
        ),
        has_at_least_one_key(Const.CONF_BELOW, Const.CONF_ABOVE),
    )

    STATE_CONDITION_BASE_SCHEMA: typing.Final = {
        **CONDITION_BASE_SCHEMA,
        vol.Required(Const.CONF_CONDITION): "state",
        vol.Required(Const.CONF_ENTITY_ID): entity_ids_or_uuids,
        vol.Optional(Const.CONF_MATCH, default=Const.ENTITY_MATCH_ALL): vol.All(
            vol.Lower, vol.Any(Const.ENTITY_MATCH_ALL, Const.ENTITY_MATCH_ANY)
        ),
        vol.Optional(Const.CONF_ATTRIBUTE): str,
        vol.Optional(Const.CONF_FOR): positive_time_period,
        # To support use_trigger_value in automation
        # Deprecated 2016/04/25
        vol.Optional("from"): str,
    }

    STATE_CONDITION_STATE_SCHEMA: typing.Final = vol.Schema(
        {
            **STATE_CONDITION_BASE_SCHEMA,
            vol.Required(Const.CONF_STATE): vol.Any(str, [str]),
        }
    )

    STATE_CONDITION_ATTRIBUTE_SCHEMA: typing.Final = vol.Schema(
        {
            **STATE_CONDITION_BASE_SCHEMA,
            vol.Required(Const.CONF_STATE): match_all,
        }
    )

    @staticmethod
    def state_condition_schema(value: typing.Any) -> dict:
        """Validate a state condition."""
        if not isinstance(value, dict):
            raise vol.Invalid("Expected a dictionary")

        if Const.CONF_ATTRIBUTE in value:
            validated: dict = ConfigValidation.STATE_CONDITION_ATTRIBUTE_SCHEMA(value)
        else:
            validated = ConfigValidation.STATE_CONDITION_STATE_SCHEMA(value)

        return ConfigValidation.key_dependency("for", "state")(validated)

    SUN_CONDITION_SCHEMA: typing.Final = vol.All(
        vol.Schema(
            {
                **CONDITION_BASE_SCHEMA,
                vol.Required(Const.CONF_CONDITION): "sun",
                vol.Optional("before"): sun_event,
                vol.Optional("before_offset"): time_period,
                vol.Optional("after"): vol.All(
                    vol.Lower, vol.Any(Const.SUN_EVENT_SUNSET, Const.SUN_EVENT_SUNRISE)
                ),
                vol.Optional("after_offset"): time_period,
            }
        ),
        has_at_least_one_key("before", "after"),
    )

    TEMPLATE_CONDITION_SCHEMA: typing.Final = vol.Schema(
        {
            **CONDITION_BASE_SCHEMA,
            vol.Required(Const.CONF_CONDITION): "template",
            vol.Required(Const.CONF_VALUE_TEMPLATE): template,
        }
    )

    TIME_CONDITION_SCHEMA: typing.Final = vol.All(
        vol.Schema(
            {
                **CONDITION_BASE_SCHEMA,
                vol.Required(Const.CONF_CONDITION): "time",
                vol.Optional("before"): vol.Any(
                    time, vol.All(str, entity_domain(["input_datetime", "sensor"]))
                ),
                vol.Optional("after"): vol.Any(
                    time, vol.All(str, entity_domain(["input_datetime", "sensor"]))
                ),
                vol.Optional("weekday"): weekdays,
            }
        ),
        has_at_least_one_key("before", "after", "weekday"),
    )

    TRIGGER_CONDITION_SCHEMA: typing.Final = vol.Schema(
        {
            **CONDITION_BASE_SCHEMA,
            vol.Required(Const.CONF_CONDITION): "trigger",
            vol.Required(Const.CONF_ID): vol.All(ensure_list, [string]),
        }
    )

    ZONE_CONDITION_SCHEMA: typing.Final = vol.Schema(
        {
            **CONDITION_BASE_SCHEMA,
            vol.Required(Const.CONF_CONDITION): "zone",
            vol.Required(Const.CONF_ENTITY_ID): entity_ids,
            vol.Required("zone"): entity_ids,
            # To support use_trigger_value in automation
            # Deprecated 2016/04/25
            vol.Optional("event"): vol.Any("enter", "leave"),
        }
    )

    AND_CONDITION_SCHEMA: typing.Final = vol.Schema(
        {
            **CONDITION_BASE_SCHEMA,
            vol.Required(Const.CONF_CONDITION): "and",
            vol.Required(Const.CONF_CONDITIONS): vol.All(
                ensure_list,
                # pylint: disable=unnecessary-lambda
                [lambda value: ConfigValidation.CONDITION_SCHEMA(value)],
            ),
        }
    )

    AND_CONDITION_SHORTHAND_SCHEMA: typing.Final = vol.Schema(
        {
            **CONDITION_BASE_SCHEMA,
            vol.Required("and"): vol.All(
                ensure_list,
                # pylint: disable=unnecessary-lambda
                [lambda value: ConfigValidation.CONDITION_SCHEMA(value)],
            ),
        }
    )

    OR_CONDITION_SCHEMA: typing.Final = vol.Schema(
        {
            **CONDITION_BASE_SCHEMA,
            vol.Required(Const.CONF_CONDITION): "or",
            vol.Required(Const.CONF_CONDITIONS): vol.All(
                ensure_list,
                # pylint: disable=unnecessary-lambda
                [lambda value: ConfigValidation.CONDITION_SCHEMA(value)],
            ),
        }
    )

    OR_CONDITION_SHORTHAND_SCHEMA: typing.Final = vol.Schema(
        {
            **CONDITION_BASE_SCHEMA,
            vol.Required("or"): vol.All(
                ensure_list,
                # pylint: disable=unnecessary-lambda
                [lambda value: ConfigValidation.CONDITION_SCHEMA(value)],
            ),
        }
    )

    NOT_CONDITION_SCHEMA: typing.Final = vol.Schema(
        {
            **CONDITION_BASE_SCHEMA,
            vol.Required(Const.CONF_CONDITION): "not",
            vol.Required(Const.CONF_CONDITIONS): vol.All(
                ensure_list,
                # pylint: disable=unnecessary-lambda
                [lambda value: ConfigValidation.CONDITION_SCHEMA(value)],
            ),
        }
    )

    NOT_CONDITION_SHORTHAND_SCHEMA: typing.Final = vol.Schema(
        {
            **CONDITION_BASE_SCHEMA,
            vol.Required("not"): vol.All(
                ensure_list,
                # pylint: disable=unnecessary-lambda
                [lambda value: ConfigValidation.CONDITION_SCHEMA(value)],
            ),
        }
    )

    DEVICE_CONDITION_BASE_SCHEMA: typing.Final = vol.Schema(
        {
            **CONDITION_BASE_SCHEMA,
            vol.Required(Const.CONF_CONDITION): "device",
            vol.Required(Const.CONF_DEVICE_ID): str,
            vol.Required(Const.CONF_DOMAIN): str,
            vol.Remove("metadata"): dict,
        }
    )

    DEVICE_CONDITION_SCHEMA: typing.Final = DEVICE_CONDITION_BASE_SCHEMA.extend(
        {}, extra=vol.ALLOW_EXTRA
    )

    dynamic_template_condition_action = vol.All(
        # Wrap a shorthand template condition in a template condition
        dynamic_template,
        lambda config: {
            Const.CONF_VALUE_TEMPLATE: config,
            Const.CONF_CONDITION: "template",
        },
    )

    CONDITION_SHORTHAND_SCHEMA: typing.Final = vol.Schema(
        {
            **CONDITION_BASE_SCHEMA,
            vol.Required(Const.CONF_CONDITION): vol.All(
                ensure_list,
                # pylint: disable=unnecessary-lambda
                [lambda value: ConfigValidation.CONDITION_SCHEMA(value)],
            ),
        }
    )

    CONDITION_SCHEMA: typing.Final = vol.Schema(
        vol.Any(
            vol.All(
                expand_condition_shorthand,
                key_value_schemas(
                    Const.CONF_CONDITION,
                    {
                        "and": AND_CONDITION_SCHEMA,
                        "device": DEVICE_CONDITION_SCHEMA,
                        "not": NOT_CONDITION_SCHEMA,
                        "numeric_state": NUMERIC_STATE_CONDITION_SCHEMA,
                        "or": OR_CONDITION_SCHEMA,
                        "state": state_condition_schema,
                        "sun": SUN_CONDITION_SCHEMA,
                        "template": TEMPLATE_CONDITION_SCHEMA,
                        "time": TIME_CONDITION_SCHEMA,
                        "trigger": TRIGGER_CONDITION_SCHEMA,
                        "zone": ZONE_CONDITION_SCHEMA,
                    },
                ),
            ),
            dynamic_template_condition_action,
        )
    )

    TRACE_CONFIG_SCHEMA: typing.Final = {
        vol.Optional(
            Const.CONF_STORED_TRACES, default=Const.DEFAULT_STORED_TRACES
        ): positive_int
    }

    dynamic_template_condition_action = vol.All(
        # Wrap a shorthand template condition action in a template condition
        vol.Schema(
            {
                **CONDITION_BASE_SCHEMA,
                vol.Required(Const.CONF_CONDITION): dynamic_template,
            }
        ),
        lambda config: {
            **config,
            Const.CONF_VALUE_TEMPLATE: config[Const.CONF_CONDITION],
            Const.CONF_CONDITION: "template",
        },
    )

    CONDITION_ACTION_SCHEMA: typing.Final = vol.Schema(
        vol.All(
            expand_condition_shorthand,
            key_value_schemas(
                Const.CONF_CONDITION,
                {
                    "and": AND_CONDITION_SCHEMA,
                    "device": DEVICE_CONDITION_SCHEMA,
                    "not": NOT_CONDITION_SCHEMA,
                    "numeric_state": NUMERIC_STATE_CONDITION_SCHEMA,
                    "or": OR_CONDITION_SCHEMA,
                    "state": state_condition_schema,
                    "sun": SUN_CONDITION_SCHEMA,
                    "template": TEMPLATE_CONDITION_SCHEMA,
                    "time": TIME_CONDITION_SCHEMA,
                    "trigger": TRIGGER_CONDITION_SCHEMA,
                    "zone": ZONE_CONDITION_SCHEMA,
                },
                dynamic_template_condition_action,
                "a list of conditions or a valid template",
            ),
        )
    )

    TRIGGER_BASE_SCHEMA: typing.Final = vol.Schema(
        {
            vol.Required(Const.CONF_PLATFORM): str,
            vol.Optional(Const.CONF_ID): str,
            vol.Optional(Const.CONF_VARIABLES): SCRIPT_VARIABLES_SCHEMA,
            vol.Optional(Const.CONF_ENABLED): boolean,
        }
    )

    _base_trigger_validator_schema = TRIGGER_BASE_SCHEMA.extend(
        {}, extra=vol.ALLOW_EXTRA
    )

    # This is first round of validation, we don't want to process the config here already,
    # just ensure basics as platform and ID are there.
    @staticmethod
    def _base_trigger_validator(value: typing.Any) -> typing.Any:
        ConfigValidation._base_trigger_validator_schema(value)
        return value

    TRIGGER_SCHEMA: typing.Final = vol.All(ensure_list, [_base_trigger_validator])

    _SCRIPT_DELAY_SCHEMA: typing.Final = vol.Schema(
        {
            **SCRIPT_ACTION_BASE_SCHEMA,
            vol.Required(Const.CONF_DELAY): positive_time_period_template,
        }
    )

    _SCRIPT_WAIT_TEMPLATE_SCHEMA: typing.Final = vol.Schema(
        {
            **SCRIPT_ACTION_BASE_SCHEMA,
            vol.Required(Const.CONF_WAIT_TEMPLATE): template,
            vol.Optional(Const.CONF_TIMEOUT): positive_time_period_template,
            vol.Optional(Const.CONF_CONTINUE_ON_TIMEOUT): boolean,
        }
    )

    DEVICE_ACTION_BASE_SCHEMA: typing.Final = vol.Schema(
        {
            **SCRIPT_ACTION_BASE_SCHEMA,
            vol.Required(Const.CONF_DEVICE_ID): string,
            vol.Required(Const.CONF_DOMAIN): str,
            vol.Remove("metadata"): dict,
        }
    )

    DEVICE_ACTION_SCHEMA: typing.Final = DEVICE_ACTION_BASE_SCHEMA.extend(
        {}, extra=vol.ALLOW_EXTRA
    )

    DEVICE_CLASSES_SCHEMA: typing.Final = vol.All(
        vol.Lower, vol.Coerce(BinarySensor.DeviceClass)
    )

    _SCRIPT_SCENE_SCHEMA: typing.Final = vol.Schema(
        {
            **SCRIPT_ACTION_BASE_SCHEMA,
            vol.Required(Const.CONF_SCENE): entity_domain("scene"),
        }
    )

    _SCRIPT_REPEAT_SCHEMA: typing.Final = vol.Schema(
        {
            **SCRIPT_ACTION_BASE_SCHEMA,
            vol.Required(Const.CONF_REPEAT): vol.All(
                {
                    vol.Exclusive(Const.CONF_COUNT, "repeat"): vol.Any(
                        vol.Coerce(int), template
                    ),
                    vol.Exclusive(Const.CONF_FOR_EACH, "repeat"): vol.Any(
                        dynamic_template, vol.All(list, template_complex)
                    ),
                    vol.Exclusive(Const.CONF_WHILE, "repeat"): vol.All(
                        ensure_list, [CONDITION_SCHEMA]
                    ),
                    vol.Exclusive(Const.CONF_UNTIL, "repeat"): vol.All(
                        ensure_list, [CONDITION_SCHEMA]
                    ),
                    vol.Required(Const.CONF_SEQUENCE): SCRIPT_SCHEMA,
                },
                has_at_least_one_key(
                    Const.CONF_COUNT,
                    Const.CONF_FOR_EACH,
                    Const.CONF_WHILE,
                    Const.CONF_UNTIL,
                ),
            ),
        }
    )

    _SCRIPT_CHOOSE_SCHEMA: typing.Final = vol.Schema(
        {
            **SCRIPT_ACTION_BASE_SCHEMA,
            vol.Required(Const.CONF_CHOOSE): vol.All(
                ensure_list,
                [
                    {
                        vol.Optional(Const.CONF_ALIAS): string,
                        vol.Required(Const.CONF_CONDITIONS): vol.All(
                            ensure_list, [CONDITION_SCHEMA]
                        ),
                        vol.Required(Const.CONF_SEQUENCE): SCRIPT_SCHEMA,
                    }
                ],
            ),
            vol.Optional(Const.CONF_DEFAULT): SCRIPT_SCHEMA,
        }
    )

    _SCRIPT_WAIT_FOR_TRIGGER_SCHEMA: typing.Final = vol.Schema(
        {
            **SCRIPT_ACTION_BASE_SCHEMA,
            vol.Required(Const.CONF_WAIT_FOR_TRIGGER): TRIGGER_SCHEMA,
            vol.Optional(Const.CONF_TIMEOUT): positive_time_period_template,
            vol.Optional(Const.CONF_CONTINUE_ON_TIMEOUT): boolean,
        }
    )

    _SCRIPT_IF_SCHEMA: typing.Final = vol.Schema(
        {
            **SCRIPT_ACTION_BASE_SCHEMA,
            vol.Required(Const.CONF_IF): vol.All(ensure_list, [CONDITION_SCHEMA]),
            vol.Required(Const.CONF_THEN): SCRIPT_SCHEMA,
            vol.Optional(Const.CONF_ELSE): SCRIPT_SCHEMA,
        }
    )

    _SCRIPT_SET_SCHEMA: typing.Final = vol.Schema(
        {
            **SCRIPT_ACTION_BASE_SCHEMA,
            vol.Required(Const.CONF_VARIABLES): SCRIPT_VARIABLES_SCHEMA,
        }
    )

    _SCRIPT_STOP_SCHEMA: typing.Final = vol.Schema(
        {
            **SCRIPT_ACTION_BASE_SCHEMA,
            vol.Required(Const.CONF_STOP): vol.Any(None, string),
            vol.Optional(Const.CONF_ERROR, default=False): boolean,
        }
    )

    _SCRIPT_PARALLEL_SEQUENCE: typing.Final = vol.Schema(
        {
            **SCRIPT_ACTION_BASE_SCHEMA,
            vol.Required(Const.CONF_SEQUENCE): SCRIPT_SCHEMA,
        }
    )

    _parallel_sequence_action = vol.All(
        # Wrap a shorthand sequences in a parallel action
        SCRIPT_SCHEMA,
        lambda config: {
            Const.CONF_SEQUENCE: config,
        },
    )

    _SCRIPT_PARALLEL_SCHEMA: typing.Final = vol.Schema(
        {
            **SCRIPT_ACTION_BASE_SCHEMA,
            vol.Required(Const.CONF_PARALLEL): vol.All(
                ensure_list,
                [vol.Any(_SCRIPT_PARALLEL_SEQUENCE, _parallel_sequence_action)],
            ),
        }
    )

    @staticmethod
    def determine_script_action(action: dict[str, typing.Any]) -> _ScriptAction:
        """Determine action type."""
        result: _ScriptAction = None

        if Const.CONF_DELAY in action:
            result = _ScriptAction.DELAY
        elif Const.CONF_WAIT_TEMPLATE in action:
            result = _ScriptAction.WAIT_TEMPLATE
        elif any(key in action for key in (Const.CONF_CONDITION, "and", "or", "not")):
            result = _ScriptAction.CONDITION
        elif Const.CONF_EVENT in action:
            result = _ScriptAction.EVENT
        if Const.CONF_DEVICE_ID in action:
            result = _ScriptAction.DEVICE
        elif Const.CONF_SCENE in action:
            result = _ScriptAction.SCENE
        elif Const.CONF_REPEAT in action:
            result = _ScriptAction.REPEAT
        elif Const.CONF_CHOOSE in action:
            result = _ScriptAction.CHOOSE
        elif Const.CONF_WAIT_FOR_TRIGGER in action:
            result = _ScriptAction.WAIT_FOR_TRIGGER
        elif Const.CONF_VARIABLES in action:
            result = _ScriptAction.VARIABLES
        elif Const.CONF_IF in action:
            result = _ScriptAction.IF
        elif Const.CONF_SERVICE in action or Const.CONF_SERVICE_TEMPLATE in action:
            result = _ScriptAction.CALL_SERVICE
        elif Const.CONF_STOP in action:
            result = _ScriptAction.STOP
        elif Const.CONF_PARALLEL in action:
            result = _ScriptAction.PARALLEL

        if result is not None:
            return result
        raise ValueError("Unable to determine action")

    ACTION_TYPE_SCHEMAS: typing.Final = {
        _ScriptAction.CALL_SERVICE: SERVICE_SCHEMA,
        _ScriptAction.DELAY: _SCRIPT_DELAY_SCHEMA,
        _ScriptAction.WAIT_TEMPLATE: _SCRIPT_WAIT_TEMPLATE_SCHEMA,
        _ScriptAction.EVENT: EVENT_SCHEMA,
        _ScriptAction.CONDITION: CONDITION_ACTION_SCHEMA,
        _ScriptAction.DEVICE: DEVICE_ACTION_SCHEMA,
        _ScriptAction.SCENE: _SCRIPT_SCENE_SCHEMA,
        _ScriptAction.REPEAT: _SCRIPT_REPEAT_SCHEMA,
        _ScriptAction.CHOOSE: _SCRIPT_CHOOSE_SCHEMA,
        _ScriptAction.WAIT_FOR_TRIGGER: _SCRIPT_WAIT_FOR_TRIGGER_SCHEMA,
        _ScriptAction.VARIABLES: _SCRIPT_SET_SCHEMA,
        _ScriptAction.STOP: _SCRIPT_STOP_SCHEMA,
        _ScriptAction.IF: _SCRIPT_IF_SCHEMA,
        _ScriptAction.PARALLEL: _SCRIPT_PARALLEL_SCHEMA,
    }

    DEVICE_TRIGGER_BASE_SCHEMA: typing.Final = TRIGGER_BASE_SCHEMA.extend(
        {
            vol.Required(Const.CONF_PLATFORM): "device",
            vol.Required(Const.CONF_DOMAIN): str,
            vol.Required(Const.CONF_DEVICE_ID): str,
            vol.Remove("metadata"): dict,
        }
    )

    NOTIFY_SERVICE_SCHEMA: typing.Final = vol.Schema(
        {
            vol.Required(Const.ATTR_MESSAGE): template,
            vol.Optional(Const.ATTR_TITLE): template,
            vol.Optional(Const.ATTR_TARGET): vol.All(ensure_list, [string]),
            vol.Optional(Const.ATTR_DATA): dict,
        }
    )

    NOTIFY_PLATFORM_SCHEMA: typing.Final = vol.Schema(
        {
            vol.Required(Const.CONF_PLATFORM): string,
            vol.Optional(Const.CONF_NAME): string,
        },
        extra=vol.ALLOW_EXTRA,
    )

    ENTITY_CATEGORIES_SCHEMA: typing.Final = vol.Coerce(EntityCategory)

    # Validate currencies adopted by countries
    currency = vol.In(
        {
            "AED",
            "AFN",
            "ALL",
            "AMD",
            "ANG",
            "AOA",
            "ARS",
            "AUD",
            "AWG",
            "AZN",
            "BAM",
            "BBD",
            "BDT",
            "BGN",
            "BHD",
            "BIF",
            "BMD",
            "BND",
            "BOB",
            "BRL",
            "BSD",
            "BTN",
            "BWP",
            "BYN",
            "BYR",
            "BZD",
            "CAD",
            "CDF",
            "CHF",
            "CLP",
            "CNY",
            "COP",
            "CRC",
            "CUP",
            "CVE",
            "CZK",
            "DJF",
            "DKK",
            "DOP",
            "DZD",
            "EGP",
            "ERN",
            "ETB",
            "EUR",
            "FJD",
            "FKP",
            "GBP",
            "GEL",
            "GHS",
            "GIP",
            "GMD",
            "GNF",
            "GTQ",
            "GYD",
            "HKD",
            "HNL",
            "HRK",
            "HTG",
            "HUF",
            "IDR",
            "ILS",
            "INR",
            "IQD",
            "IRR",
            "ISK",
            "JMD",
            "JOD",
            "JPY",
            "KES",
            "KGS",
            "KHR",
            "KMF",
            "KPW",
            "KRW",
            "KWD",
            "KYD",
            "KZT",
            "LAK",
            "LBP",
            "LKR",
            "LRD",
            "LSL",
            "LTL",
            "LYD",
            "MAD",
            "MDL",
            "MGA",
            "MKD",
            "MMK",
            "MNT",
            "MOP",
            "MRO",
            "MUR",
            "MVR",
            "MWK",
            "MXN",
            "MYR",
            "MZN",
            "NAD",
            "NGN",
            "NIO",
            "NOK",
            "NPR",
            "NZD",
            "OMR",
            "PAB",
            "PEN",
            "PGK",
            "PHP",
            "PKR",
            "PLN",
            "PYG",
            "QAR",
            "RON",
            "RSD",
            "RUB",
            "RWF",
            "SAR",
            "SBD",
            "SCR",
            "SDG",
            "SEK",
            "SGD",
            "SHP",
            "SLL",
            "SOS",
            "SRD",
            "SSP",
            "STD",
            "SYP",
            "SZL",
            "THB",
            "TJS",
            "TMT",
            "TND",
            "TOP",
            "TRY",
            "TTD",
            "TWD",
            "TZS",
            "UAH",
            "UGX",
            "USD",
            "UYU",
            "UZS",
            "VEF",
            "VND",
            "VUV",
            "WST",
            "XAF",
            "XCD",
            "XOF",
            "XPF",
            "YER",
            "ZAR",
            "ZMK",
            "ZMW",
            "ZWL",
        },
        msg="invalid ISO 4217 formatted currency",
    )
