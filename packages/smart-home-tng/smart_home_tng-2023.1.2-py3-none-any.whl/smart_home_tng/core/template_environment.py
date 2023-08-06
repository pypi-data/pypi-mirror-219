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

import base64
import collections.abc
import datetime as dt
import functools
import json
import logging
import math
import random
import re
import statistics
import struct
import typing
import weakref
from urllib.parse import urlencode as urllib_urlencode

import jinja2
from jinja2 import sandbox

from . import helpers
from .all_states import AllStates
from .const import Const
from .domain_states import DomainStates
from .helpers.template import (
    _collect_state,
    get_template_state_if_valid,
    template_state_for_entity,
)
from .location_info import LocationInfo
from .logging_undefined import LoggingUndefined
from .render_info import RenderInfo as ri
from .state import State
from .template_context import template_context as context
from .template_environment_type import TemplateEnvironmentType
from .template_error import TemplateError
from .template_state import TemplateState

if not typing.TYPE_CHECKING:

    class SmartHomeController:
        ...

    class AreaRegistry:
        ...


if typing.TYPE_CHECKING:
    from .area_registry import AreaRegistry
    from .smart_home_controller import SmartHomeController


_LOGGER: typing.Final = logging.getLogger(__name__)
_SENTINEL: typing.Final = object()
_DATE_STR_FORMAT: typing.Final = "%Y-%m-%d %H:%M:%S"
_GROUP_DOMAIN_PREFIX: typing.Final = "group."
_ZONE_DOMAIN_PREFIX: typing.Final = "zone."


class TemplateEnvironment(sandbox.ImmutableSandboxedEnvironment):
    """The Smart Home Controller template environment."""

    SENTINEL: typing.Final = _SENTINEL

    def __init__(self, shc: SmartHomeController, limited=False, strict=False):
        """Initialise template environment."""
        if not strict:
            undefined = LoggingUndefined
        else:
            undefined = jinja2.StrictUndefined
        super().__init__(undefined=undefined)
        self._shc = shc
        self._template_cache = weakref.WeakValueDictionary()
        self.filters["round"] = TemplateEnvironment.forgiving_round
        self.filters["multiply"] = TemplateEnvironment.multiply
        self.filters["log"] = TemplateEnvironment.logarithm
        self.filters["sin"] = TemplateEnvironment.sine
        self.filters["cos"] = TemplateEnvironment.cosine
        self.filters["tan"] = TemplateEnvironment.tangent
        self.filters["asin"] = TemplateEnvironment.arc_sine
        self.filters["acos"] = TemplateEnvironment.arc_cosine
        self.filters["atan"] = TemplateEnvironment.arc_tangent
        self.filters["atan2"] = TemplateEnvironment.arc_tangent2
        self.filters["sqrt"] = TemplateEnvironment.square_root
        self.filters["as_datetime"] = TemplateEnvironment.as_datetime
        self.filters["as_timedelta"] = TemplateEnvironment.as_timedelta
        self.filters["as_timestamp"] = TemplateEnvironment.forgiving_as_timestamp
        self.filters["today_at"] = TemplateEnvironment.today_at
        self.filters["as_local"] = helpers.as_local
        self.filters["timestamp_custom"] = TemplateEnvironment.timestamp_custom
        self.filters["timestamp_local"] = TemplateEnvironment.timestamp_local
        self.filters["timestamp_utc"] = TemplateEnvironment.timestamp_utc
        self.filters["to_json"] = TemplateEnvironment.to_json
        self.filters["from_json"] = TemplateEnvironment.from_json
        self.filters["is_defined"] = TemplateEnvironment.fail_when_undefined
        self.filters["average"] = TemplateEnvironment.average
        self.filters["random"] = TemplateEnvironment.random_every_time
        self.filters["base64_encode"] = TemplateEnvironment.base64_encode
        self.filters["base64_decode"] = TemplateEnvironment.base64_decode
        self.filters["ordinal"] = TemplateEnvironment.ordinal
        self.filters["regex_match"] = TemplateEnvironment.regex_match
        self.filters["regex_replace"] = TemplateEnvironment.regex_replace
        self.filters["regex_search"] = TemplateEnvironment.regex_search
        self.filters["regex_findall"] = TemplateEnvironment.regex_findall
        self.filters["regex_findall_index"] = TemplateEnvironment.regex_findall_index
        self.filters["bitwise_and"] = TemplateEnvironment.bitwise_and
        self.filters["bitwise_or"] = TemplateEnvironment.bitwise_or
        self.filters["pack"] = TemplateEnvironment.struct_pack
        self.filters["unpack"] = TemplateEnvironment.struct_unpack
        self.filters["ord"] = ord
        self.filters["is_number"] = TemplateEnvironment.is_number
        self.filters["float"] = TemplateEnvironment.forgiving_float_filter
        self.filters["int"] = TemplateEnvironment.forgiving_int_filter
        self.filters["relative_time"] = TemplateEnvironment.relative_time
        self.filters["slugify"] = TemplateEnvironment.slugify
        self.filters["iif"] = TemplateEnvironment.iif
        self.globals["log"] = TemplateEnvironment.logarithm
        self.globals["sin"] = TemplateEnvironment.sine
        self.globals["cos"] = TemplateEnvironment.cosine
        self.globals["tan"] = TemplateEnvironment.tangent
        self.globals["sqrt"] = TemplateEnvironment.square_root
        self.globals["pi"] = math.pi
        self.globals["tau"] = math.pi * 2
        self.globals["e"] = math.e
        self.globals["asin"] = TemplateEnvironment.arc_sine
        self.globals["acos"] = TemplateEnvironment.arc_cosine
        self.globals["atan"] = TemplateEnvironment.arc_tangent
        self.globals["atan2"] = TemplateEnvironment.arc_tangent2
        self.globals["float"] = TemplateEnvironment.forgiving_float
        self.globals["as_datetime"] = TemplateEnvironment.as_datetime
        self.globals["as_local"] = helpers.as_local
        self.globals["as_timedelta"] = TemplateEnvironment.as_timedelta
        self.globals["as_timestamp"] = TemplateEnvironment.forgiving_as_timestamp
        self.globals["today_at"] = TemplateEnvironment.today_at
        self.globals["relative_time"] = TemplateEnvironment.relative_time
        self.globals["timedelta"] = dt.timedelta
        self.globals["strptime"] = TemplateEnvironment.strptime
        self.globals["urlencode"] = TemplateEnvironment.urlencode
        self.globals["average"] = TemplateEnvironment.average
        self.globals["max"] = TemplateEnvironment.min_max_from_filter(
            self.filters["max"], "max"
        )
        self.globals["min"] = TemplateEnvironment.min_max_from_filter(
            self.filters["min"], "min"
        )
        self.globals["is_number"] = TemplateEnvironment.is_number
        self.globals["int"] = TemplateEnvironment.forgiving_int
        self.globals["pack"] = TemplateEnvironment.struct_pack
        self.globals["unpack"] = TemplateEnvironment.struct_unpack
        self.globals["slugify"] = TemplateEnvironment.slugify
        self.globals["iif"] = TemplateEnvironment.iif
        self.tests["is_number"] = TemplateEnvironment.is_number
        self.tests["match"] = TemplateEnvironment.regex_match
        self.tests["search"] = TemplateEnvironment.regex_search

        if shc is None:
            return

        # We mark these as a context functions to ensure they get
        # evaluated fresh with every execution, rather than executed
        # at compile time and the value stored. The context itself
        # can be discarded, we only need to get at the hass object.
        def shc_function(func):
            """Wrap function that depend on hass."""

            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                return func(shc, *args[1:], **kwargs)

            return jinja2.pass_context(wrapper)

        self.globals["device_entities"] = shc_function(
            TemplateEnvironment.device_entities
        )
        self.filters["device_entities"] = jinja2.pass_context(
            self.globals["device_entities"]
        )

        self.globals["device_attr"] = shc_function(TemplateEnvironment.device_attr)
        self.globals["is_device_attr"] = shc_function(
            TemplateEnvironment.is_device_attr
        )

        self.globals["device_id"] = shc_function(TemplateEnvironment.device_id)
        self.filters["device_id"] = jinja2.pass_context(self.globals["device_id"])

        self.globals["area_id"] = shc_function(TemplateEnvironment.area_id)
        self.filters["area_id"] = jinja2.pass_context(self.globals["area_id"])

        self.globals["area_name"] = shc_function(TemplateEnvironment.area_name)
        self.filters["area_name"] = jinja2.pass_context(self.globals["area_name"])

        self.globals["area_entities"] = shc_function(TemplateEnvironment.area_entities)
        self.filters["area_entities"] = jinja2.pass_context(
            self.globals["area_entities"]
        )

        self.globals["area_devices"] = shc_function(TemplateEnvironment.area_devices)
        self.filters["area_devices"] = jinja2.pass_context(self.globals["area_devices"])

        self.globals["integration_entities"] = shc_function(
            TemplateEnvironment.integration_entities
        )
        self.filters["integration_entities"] = jinja2.pass_context(
            self.globals["integration_entities"]
        )

        if limited:
            # Only device_entities is available to limited templates, mark other
            # functions and filters as unsupported.
            def unsupported(name):
                def warn_unsupported(*args, **kwargs):
                    raise TemplateError(
                        f"Use of '{name}' is not supported in limited templates"
                    )

                return warn_unsupported

            shc_globals = [
                "closest",
                "distance",
                "expand",
                "is_state",
                "is_state_attr",
                "state_attr",
                "states",
                "utcnow",
                "now",
                "device_attr",
                "is_device_attr",
                "device_id",
                "area_id",
                "area_name",
            ]
            shc_filters = ["closest", "expand", "device_id", "area_id", "area_name"]
            for glob in shc_globals:
                self.globals[glob] = unsupported(glob)
            for filt in shc_filters:
                self.filters[filt] = unsupported(filt)
            return

        self.globals["expand"] = shc_function(TemplateEnvironment.expand)
        self.filters["expand"] = jinja2.pass_context(self.globals["expand"])
        self.globals["closest"] = shc_function(TemplateEnvironment.closest)
        self.filters["closest"] = jinja2.pass_context(
            shc_function(TemplateEnvironment.closest_filter)
        )
        self.globals["distance"] = shc_function(TemplateEnvironment.distance)
        self.globals["is_state"] = shc_function(TemplateEnvironment.is_state)
        self.globals["is_state_attr"] = shc_function(TemplateEnvironment.is_state_attr)
        self.globals["state_attr"] = shc_function(TemplateEnvironment.state_attr)
        self.globals["states"] = AllStates(shc)
        self.globals["utcnow"] = shc_function(TemplateEnvironment.utcnow)
        self.globals["now"] = shc_function(TemplateEnvironment.now)

    def is_different_controller(self, shc: SmartHomeController) -> bool:
        return self._shc != shc

    @staticmethod
    def get_env(wanted_env: TemplateEnvironmentType, shc: SmartHomeController = None):
        """Get the wanted Environment from the Cache, or create it."""
        if shc is None:
            wanted_env = TemplateEnvironmentType.NO_SHC
        elif wanted_env == TemplateEnvironmentType.NO_SHC:
            shc = None

        result = _cache.get(wanted_env)
        if result is not None:
            if result.is_different_controller(shc):
                raise TemplateError("Invalid Smart Home Controller.")
            return result

        if wanted_env == TemplateEnvironmentType.NO_SHC:
            result = TemplateEnvironment(None)
        elif wanted_env == TemplateEnvironmentType.NORMAL:
            result = TemplateEnvironment(shc)
        elif wanted_env == TemplateEnvironmentType.LIMITED:
            result = TemplateEnvironment(shc, limited=True)
        else:
            result = TemplateEnvironment(shc, strict=True)
        _cache[wanted_env] = result
        return result

    def is_safe_callable(self, obj):
        """Test if callback is safe."""
        return isinstance(obj, AllStates) or super().is_safe_callable(obj)

    def is_safe_attribute(self, obj, attr, value):
        """Test if attribute is safe."""
        if isinstance(obj, (AllStates, DomainStates, TemplateState)):
            return attr[0] != "_"

        if isinstance(obj, jinja2.utils.Namespace):
            return True

        return super().is_safe_attribute(obj, attr, value)

    def compile(self, source, name=None, filename=None, raw=False, defer_init=False):
        """Compile the template."""
        if (
            name is not None
            or filename is not None
            or raw is not False
            or defer_init is not False
        ):
            # If there are any non-default keywords args, we do
            # not cache.  In prodution we currently do not have
            # any instance of this.
            return super().compile(source, name, filename, raw, defer_init)

        if (cached := self._template_cache.get(source)) is None:
            cached = self._template_cache[source] = super().compile(source)

        return cached

    def raise_no_default(function, value):
        """Log warning if no default is specified."""
        template, action = context.get() or ("", "rendering or compiling")
        raise ValueError(
            f"Template error: {function} got invalid input '{value}' when {action} "
            + f"template '{template}' but no default was specified"
        )

    @staticmethod
    def forgiving_round(value, precision=0, method="common", default=_SENTINEL):
        """Filter to round a value."""
        try:
            # support rounding methods like jinja
            multiplier = float(10**precision)
            if method == "ceil":
                value = math.ceil(float(value) * multiplier) / multiplier
            elif method == "floor":
                value = math.floor(float(value) * multiplier) / multiplier
            elif method == "half":
                value = round(float(value) * 2) / 2
            else:
                # if method is common or something else, use common rounding
                value = round(float(value), precision)
            return int(value) if precision == 0 else value
        except (ValueError, TypeError):
            # If value can't be converted to float
            if default is _SENTINEL:
                TemplateEnvironment.raise_no_default("round", value)
            return default

    @staticmethod
    def multiply(value, amount, default=_SENTINEL):
        """Filter to convert value to float and multiply it."""
        try:
            return float(value) * amount
        except (ValueError, TypeError):
            # If value can't be converted to float
            if default is _SENTINEL:
                TemplateEnvironment.raise_no_default("multiply", value)
            return default

    @staticmethod
    def logarithm(value, base=math.e, default=_SENTINEL):
        """Filter and function to get logarithm of the value with a specific base."""
        try:
            base_float = float(base)
        except (ValueError, TypeError):
            if default is _SENTINEL:
                TemplateEnvironment.raise_no_default("log", base)
            return default
        try:
            value_float = float(value)
            return math.log(value_float, base_float)
        except (ValueError, TypeError):
            if default is _SENTINEL:
                TemplateEnvironment.raise_no_default("log", value)
            return default

    @staticmethod
    def sine(value, default=_SENTINEL):
        """Filter and function to get sine of the value."""
        try:
            return math.sin(float(value))
        except (ValueError, TypeError):
            if default is _SENTINEL:
                TemplateEnvironment.raise_no_default("sin", value)
            return default

    @staticmethod
    def cosine(value, default=_SENTINEL):
        """Filter and function to get cosine of the value."""
        try:
            return math.cos(float(value))
        except (ValueError, TypeError):
            if default is _SENTINEL:
                TemplateEnvironment.raise_no_default("cos", value)
            return default

    @staticmethod
    def tangent(value, default=_SENTINEL):
        """Filter and function to get tangent of the value."""
        try:
            return math.tan(float(value))
        except (ValueError, TypeError):
            if default is _SENTINEL:
                TemplateEnvironment.raise_no_default("tan", value)
            return default

    @staticmethod
    def arc_sine(value, default=_SENTINEL):
        """Filter and function to get arc sine of the value."""
        try:
            return math.asin(float(value))
        except (ValueError, TypeError):
            if default is _SENTINEL:
                TemplateEnvironment.raise_no_default("asin", value)
            return default

    @staticmethod
    def arc_cosine(value, default=_SENTINEL):
        """Filter and function to get arc cosine of the value."""
        try:
            return math.acos(float(value))
        except (ValueError, TypeError):
            if default is _SENTINEL:
                TemplateEnvironment.raise_no_default("acos", value)
            return default

    @staticmethod
    def arc_tangent(value, default=_SENTINEL):
        """Filter and function to get arc tangent of the value."""
        try:
            return math.atan(float(value))
        except (ValueError, TypeError):
            if default is _SENTINEL:
                TemplateEnvironment.raise_no_default("atan", value)
            return default

    @staticmethod
    def arc_tangent2(*args, default=_SENTINEL):
        """Filter and function to calculate four quadrant arc tangent of y / x.

        The parameters to atan2 may be passed either in an iterable or as separate arguments
        The default value may be passed either as a positional or in a keyword argument
        """
        try:
            if 1 <= len(args) <= 2 and isinstance(args[0], (list, tuple)):
                if len(args) == 2 and default is _SENTINEL:
                    # Default value passed as a positional argument
                    default = args[1]
                args = args[0]
            elif len(args) == 3 and default is _SENTINEL:
                # Default value passed as a positional argument
                default = args[2]

            return math.atan2(float(args[0]), float(args[1]))
        except (ValueError, TypeError):
            if default is _SENTINEL:
                TemplateEnvironment.raise_no_default("atan2", args)
            return default

    @staticmethod
    def square_root(value, default=_SENTINEL):
        """Filter and function to get square root of the value."""
        try:
            return math.sqrt(float(value))
        except (ValueError, TypeError):
            if default is _SENTINEL:
                TemplateEnvironment.raise_no_default("sqrt", value)
            return default

    @staticmethod
    def as_datetime(value):
        """Filter and to convert a time string or UNIX timestamp to datetime object."""
        try:
            # Check for a valid UNIX timestamp string, int or float
            timestamp = float(value)
            return helpers.utc_from_timestamp(timestamp)
        except ValueError:
            return helpers.parse_datetime(value)

    @staticmethod
    def as_timedelta(value: str) -> dt.timedelta:
        """Parse a ISO8601 duration like 'PT10M' to a timedelta."""
        return helpers.parse_duration(value)

    @staticmethod
    def forgiving_as_timestamp(value, default=_SENTINEL):
        """Filter and function which tries to convert value to timestamp."""
        try:
            return helpers.as_timestamp(value)
        except (ValueError, TypeError):
            if default is _SENTINEL:
                TemplateEnvironment.raise_no_default("as_timestamp", value)
            return default

    @staticmethod
    def today_at(time_str: str = "") -> dt.datetime:
        """Record fetching now where the time has been replaced with value."""
        today = helpers.start_of_local_day()
        if not time_str:
            return today

        if (time_today := helpers.parse_time(time_str)) is None:
            raise ValueError(
                f"could not convert {type(time_str).__name__} to datetime: '{time_str}'"
            )
        return dt.datetime.combine(today, time_today, today.tzinfo)

    @staticmethod
    def timestamp_custom(
        value, date_format=_DATE_STR_FORMAT, local=True, default=_SENTINEL
    ):
        """Filter to convert given timestamp to format."""
        try:
            date = helpers.utc_from_timestamp(value)

            if local:
                date = helpers.as_local(date)

            return date.strftime(date_format)
        except (ValueError, TypeError):
            # If timestamp can't be converted
            if default is _SENTINEL:
                TemplateEnvironment.raise_no_default("timestamp_custom", value)
            return default

    @staticmethod
    def timestamp_local(value, default=_SENTINEL):
        """Filter to convert given timestamp to local date/time."""
        try:
            return helpers.as_local(helpers.utc_from_timestamp(value)).isoformat()
        except (ValueError, TypeError):
            # If timestamp can't be converted
            if default is _SENTINEL:
                TemplateEnvironment.raise_no_default("timestamp_local", value)
            return default

    @staticmethod
    def timestamp_utc(value, default=_SENTINEL):
        """Filter to convert given timestamp to UTC date/time."""
        try:
            return helpers.utc_from_timestamp(value).isoformat()
        except (ValueError, TypeError):
            # If timestamp can't be converted
            if default is _SENTINEL:
                TemplateEnvironment.raise_no_default("timestamp_utc", value)
            return default

    @staticmethod
    def to_json(value, ensure_ascii=True):
        """Convert an object to a JSON string."""
        return json.dumps(value, ensure_ascii=ensure_ascii)

    @staticmethod
    def from_json(value):
        """Convert a JSON string to an object."""
        return json.loads(value)

    @staticmethod
    def fail_when_undefined(value):
        """Filter to force a failure when the value is undefined."""
        if isinstance(value, jinja2.Undefined):
            value()
        return value

    @staticmethod
    def average(*args: typing.Any) -> float:
        """
        Filter and function to calculate the arithmetic mean of an iterable or
        of two or more arguments.

        The parameters may be passed as an iterable or as separate arguments.
        """
        if len(args) == 0:
            raise TypeError("average expected at least 1 argument, got 0")

        if len(args) == 1:
            if isinstance(args[0], collections.abc.Iterable):
                return statistics.fmean(args[0])

            raise TypeError(f"'{type(args[0]).__name__}' object is not iterable")

        return statistics.fmean(args)

    @staticmethod
    @jinja2.pass_context
    def random_every_time(_context, values):
        """Choose a random value.

        Unlike Jinja's random filter,
        this is context-dependent to avoid caching the chosen value.
        """
        return random.choice(values)  # nosec

    @staticmethod
    def base64_encode(value):
        """Perform base64 encode."""
        return base64.b64encode(value.encode("utf-8")).decode("utf-8")

    @staticmethod
    def base64_decode(value):
        """Perform base64 denode."""
        return base64.b64decode(value).decode("utf-8")

    @staticmethod
    def ordinal(value):
        """Perform ordinal conversion."""
        return str(value) + (
            list(["th", "st", "nd", "rd"] + ["th"] * 6)[(int(str(value)[-1])) % 10]
            if int(str(value)[-2:]) % 100 not in range(11, 14)
            else "th"
        )

    @staticmethod
    def regex_match(value, find="", ignorecase=False):
        """Match value using regex."""
        if not isinstance(value, str):
            value = str(value)
        flags = re.I if ignorecase else 0
        return bool(re.match(find, value, flags))

    @staticmethod
    def regex_replace(value="", find="", replace="", ignorecase=False):
        """Replace using regex."""
        if not isinstance(value, str):
            value = str(value)
        flags = re.I if ignorecase else 0
        regex = re.compile(find, flags)
        return regex.sub(replace, value)

    @staticmethod
    def regex_search(value, find="", ignorecase=False):
        """Search using regex."""
        if not isinstance(value, str):
            value = str(value)
        flags = re.I if ignorecase else 0
        return bool(re.search(find, value, flags))

    @staticmethod
    def regex_findall_index(value, find="", index=0, ignorecase=False):
        """Find all matches using regex and then pick specific match index."""
        return TemplateEnvironment.regex_findall(value, find, ignorecase)[index]

    @staticmethod
    def regex_findall(value, find="", ignorecase=False):
        """Find all matches using regex."""
        if not isinstance(value, str):
            value = str(value)
        flags = re.I if ignorecase else 0
        return re.findall(find, value, flags)

    @staticmethod
    def bitwise_and(first_value, second_value):
        """Perform a bitwise and operation."""
        return first_value & second_value

    @staticmethod
    def bitwise_or(first_value, second_value):
        """Perform a bitwise or operation."""
        return first_value | second_value

    @staticmethod
    def struct_pack(value: typing.Any, format_string: str) -> bytes:
        """Pack an object into a bytes object."""
        try:
            return struct.pack(format_string, value)
        except struct.error:
            _LOGGER.warning(
                f"Template warning: 'pack' unable to pack object '{value}' with type "
                + f"'{type(value).__name__}' and format_string '{format_string}' "
                + "see https://docs.python.org/3/library/struct.html for more information"
            )
            return None

    @staticmethod
    def struct_unpack(value: bytes, format_string: str, offset: int = 0) -> typing.Any:
        """Unpack an object from bytes an return the first native object."""
        try:
            return struct.unpack_from(format_string, value, offset)[0]
        except struct.error:
            _LOGGER.warning(
                f"Template warning: 'unpack' unable to unpack object '{value}' with "
                + f"format_string '{format_string}' and offset {offset} see "
                + "https://docs.python.org/3/library/struct.html for more information"
            )
            return None

    @staticmethod
    def is_number(value):
        """Try to convert value to a float."""
        try:
            fvalue = float(value)
        except (ValueError, TypeError):
            return False
        if math.isnan(fvalue) or math.isinf(fvalue):
            return False
        return True

    @staticmethod
    def forgiving_float(value, default=_SENTINEL):
        """Try to convert value to a float."""
        try:
            return float(value)
        except (ValueError, TypeError):
            if default is _SENTINEL:
                TemplateEnvironment.raise_no_default("float", value)
            return default

    @staticmethod
    def forgiving_float_filter(value, default=_SENTINEL):
        """Try to convert value to a float."""
        try:
            return float(value)
        except (ValueError, TypeError):
            if default is _SENTINEL:
                TemplateEnvironment.raise_no_default("float", value)
            return default

    @staticmethod
    def forgiving_int(value, default=_SENTINEL, base=10):
        """Try to convert value to an int, and raise if it fails."""
        result = jinja2.filters.do_int(value, default=default, base=base)
        if result is _SENTINEL:
            TemplateEnvironment.raise_no_default("int", value)
        return result

    @staticmethod
    def forgiving_int_filter(value, default=_SENTINEL, base=10):
        """Try to convert value to an int, and raise if it fails."""
        result = jinja2.filters.do_int(value, default=default, base=base)
        if result is _SENTINEL:
            TemplateEnvironment.raise_no_default("int", value)
        return result

    @staticmethod
    def relative_time(value):
        """
        Take a datetime and return its "age" as a string.

        The age can be in second, minute, hour, day, month or year. Only the
        biggest unit is considered, e.g. if it's 2 days and 3 hours, "2 days" will
        be returned.
        Make sure date is not in the future, or else it will return None.

        If the input are not a datetime object the input will be returned unmodified.
        """
        if not isinstance(value, dt.datetime):
            return value
        if not value.tzinfo:
            value = helpers.as_local(value)
        if helpers.now() < value:
            return value
        return helpers.get_age(value)

    @staticmethod
    def urlencode(value):
        """Urlencode dictionary and return as UTF-8 string."""
        return urllib_urlencode(value).encode("utf-8")

    @staticmethod
    def slugify(value, separator="_"):
        """Convert a string into a slug, such as what is used for entity ids."""
        return helpers.slugify(value, separator=separator)

    @staticmethod
    def iif(
        value: typing.Any,
        if_true: typing.Any = True,
        if_false: typing.Any = False,
        if_none: typing.Any = _SENTINEL,
    ) -> typing.Any:
        """Immediate if function/filter that allow for common if/else constructs.

        https://en.wikipedia.org/wiki/IIf

        Examples:
            {{ is_state("device_tracker.frenck", "home") | iif("yes", "no") }}
            {{ iif(1==2, "yes", "no") }}
            {{ (1 == 1) | iif("yes", "no") }}
        """
        if value is None and if_none is not _SENTINEL:
            return if_none
        if bool(value):
            return if_true
        return if_false

    @staticmethod
    def strptime(string, fmt, default=_SENTINEL):
        """Parse a time string to datetime."""
        try:
            return dt.datetime.strptime(string, fmt)
        except (ValueError, AttributeError, TypeError):
            if default is _SENTINEL:
                TemplateEnvironment.raise_no_default("strptime", string)
            return default

    @staticmethod
    def min_max_from_filter(builtin_filter: typing.Any, name: str) -> typing.Any:
        """
        Convert a built-in min/max Jinja filter to a global function.

        The parameters may be passed as an iterable or as separate arguments.
        """

        @jinja2.pass_environment
        @functools.wraps(builtin_filter)
        def wrapper(
            environment: jinja2.Environment, *args: typing.Any, **kwargs: typing.Any
        ) -> typing.Any:
            if len(args) == 0:
                raise TypeError(f"{name} expected at least 1 argument, got 0")

            if len(args) == 1:
                if isinstance(args[0], collections.abc.Iterable):
                    return builtin_filter(environment, args[0], **kwargs)

                raise TypeError(f"'{type(args[0]).__name__}' object is not iterable")

            return builtin_filter(environment, args, **kwargs)

        return jinja2.pass_environment(wrapper)

    @staticmethod
    def device_entities(
        shc: SmartHomeController, device_id: str
    ) -> collections.abc.Iterable[str]:
        """Get entity ids for entities tied to a device."""
        entity_reg = shc.entity_registry
        entries = entity_reg.async_entries_for_device(device_id)
        return [entry.entity_id for entry in entries]

    @staticmethod
    def device_id(shc: SmartHomeController, entity_id_or_device_name: str) -> str:
        """Get a device ID from an entity ID or device name."""
        entity_reg = shc.entity_registry
        entity = entity_reg.async_get(entity_id_or_device_name)
        if entity is not None:
            return entity.device_id

        dev_reg = shc.device_registry
        return next(
            (
                id
                for id, device in dev_reg.devices.items()
                if (name := device.name_by_user or device.name)
                and (str(entity_id_or_device_name) == name)
            ),
            None,
        )

    @staticmethod
    def device_attr(
        shc: SmartHomeController, device_or_entity_id: str, attr_name: str
    ) -> typing.Any:
        """Get the device specific attribute."""
        device_reg = shc.device_registry
        if not isinstance(device_or_entity_id, str):
            raise TemplateError("Must provide a device or entity ID")
        device = None
        if (
            "." in device_or_entity_id
            and (_device_id := TemplateEnvironment.device_id(shc, device_or_entity_id))
            is not None
        ):
            device = device_reg.async_get(_device_id)
        elif "." not in device_or_entity_id:
            device = device_reg.async_get(device_or_entity_id)
        if device is None or not hasattr(device, attr_name):
            return None
        return getattr(device, attr_name)

    @staticmethod
    def is_device_attr(
        shc: SmartHomeController,
        device_or_entity_id: str,
        attr_name: str,
        attr_value: typing.Any,
    ) -> bool:
        """Test if a device's attribute is a specific value."""
        return bool(
            TemplateEnvironment.device_attr(shc, device_or_entity_id, attr_name)
            == attr_value
        )

    @staticmethod
    def area_id(shc: SmartHomeController, lookup_value: str) -> str:
        """Get the area ID from an area name, device id, or entity id."""
        area_reg = shc.area_registry
        if area := area_reg.async_get_area_by_name(str(lookup_value)):
            return area.id

        ent_reg = shc.entity_registry
        dev_reg = shc.device_registry
        # Import here, not at top-level to avoid circular import

        if not helpers.valid_entity_id(lookup_value.lower()):
            if entity := ent_reg.async_get(lookup_value):
                # If entity has an area ID, return that
                if entity.area_id:
                    return entity.area_id
                # If entity has a device ID, return the area ID for the device
                if entity.device_id and (device := dev_reg.async_get(entity.device_id)):
                    return device.area_id

        # Check if this could be a device ID
        if device := dev_reg.async_get(lookup_value):
            return device.area_id

        return None

    @staticmethod
    def _get_area_name(area_reg: AreaRegistry, valid_area_id: str) -> str:
        """Get area name from valid area ID."""
        area = area_reg.async_get_area(valid_area_id)
        assert area
        return area.name

    @staticmethod
    def area_name(shc: SmartHomeController, lookup_value: str) -> str:
        """Get the area name from an area id, device id, or entity id."""
        area_reg = shc.area_registry
        if area := area_reg.async_get_area(lookup_value):
            return area.name

        dev_reg = shc.device_registry
        ent_reg = shc.entity_registry
        if not helpers.valid_entity_id(lookup_value.lower()):
            if entity := ent_reg.async_get(lookup_value):
                # If entity has an area ID, get the area name for that
                if entity.area_id:
                    return TemplateEnvironment._get_area_name(area_reg, entity.area_id)
                # If entity has a device ID and the device exists with an area ID, get the
                # area name for that
                if (
                    entity.device_id
                    and (device := dev_reg.async_get(entity.device_id))
                    and device.area_id
                ):
                    return TemplateEnvironment._get_area_name(area_reg, device.area_id)

        if (device := dev_reg.async_get(lookup_value)) and device.area_id:
            return TemplateEnvironment._get_area_name(area_reg, device.area_id)

        return None

    @staticmethod
    def area_entities(
        shc: SmartHomeController, area_id_or_name: str
    ) -> collections.abc.Iterable[str]:
        """Return entities for a given area ID or name."""
        _area_id: str
        # if area_name returns a value, we know the input was an ID, otherwise we
        # assume it's a name, and if it's neither, we return early
        if TemplateEnvironment.area_name(shc, area_id_or_name) is None:
            _area_id = TemplateEnvironment.area_id(shc, area_id_or_name)
        else:
            _area_id = area_id_or_name
        if _area_id is None:
            return []
        ent_reg = shc.entity_registry
        entity_ids = [
            entry.entity_id
            for entry in ent_reg.async_entries_for_area(ent_reg, _area_id)
        ]
        dev_reg = shc.device_registry
        # We also need to add entities tied to a device in the area that don't themselves
        # have an area specified since they inherit the area from the device.
        entity_ids.extend(
            [
                entity.entity_id
                for device in dev_reg.async_entries_for_area(_area_id)
                for entity in ent_reg.async_entries_for_device(device.id)
                if entity.area_id is None
            ]
        )
        return entity_ids

    @staticmethod
    def area_devices(
        shc: SmartHomeController, area_id_or_name: str
    ) -> collections.abc.Iterable[str]:
        """Return device IDs for a given area ID or name."""
        _area_id: str
        # if area_name returns a value, we know the input was an ID, otherwise we
        # assume it's a name, and if it's neither, we return early
        if TemplateEnvironment.area_name(shc, area_id_or_name) is not None:
            _area_id = area_id_or_name
        else:
            _area_id = TemplateEnvironment.area_id(shc, area_id_or_name)
        if _area_id is None:
            return []
        dev_reg = shc.device_registry
        entries = dev_reg.async_entries_for_area(_area_id)
        return [entry.id for entry in entries]

    @staticmethod
    def integration_entities(
        shc: SmartHomeController, entry_name: str
    ) -> collections.abc.Iterable[str]:
        """
        Get entity ids for entities tied to an integration/domain.

        Provide entry_name as domain to get all entity id's for a integration/domain
        or provide a config entry title for filtering between instances of the same integration.
        """
        # first try if this is a config entry match
        conf_entry = next(
            (
                entry.entry_id
                for entry in shc.config_entries.async_entries()
                if entry.title == entry_name
            ),
            None,
        )
        if conf_entry is not None:
            ent_reg = shc.entity_registry
            entries = ent_reg.async_entries_for_config_entry(conf_entry)
            return [entry.entity_id for entry in entries]

        # fallback to just returning all entities for a domain
        return [
            entity_id
            for entity_id, info in shc.entity_sources.items()
            if info["domain"] == entry_name
        ]

    @staticmethod
    def get_state_if_valid(shc: SmartHomeController, entity_id: str) -> TemplateState:
        return get_template_state_if_valid(shc, entity_id)

    @staticmethod
    def get_state(shc: SmartHomeController, entity_id: str) -> TemplateState:
        return template_state_for_entity(shc, entity_id)

    @staticmethod
    def _resolve_state(
        shc: SmartHomeController, entity_id_or_state: typing.Any
    ) -> State | TemplateState:
        """Return state or entity_id if given."""
        if isinstance(entity_id_or_state, State):
            return entity_id_or_state
        if isinstance(entity_id_or_state, str):
            return TemplateEnvironment.get_state(shc, entity_id_or_state)
        return None

    @staticmethod
    def closest(shc: SmartHomeController, *args):
        """Find closest entity.

        Closest to home:
            closest(states)
            closest(states.device_tracker)
            closest('group.children')
            closest(states.group.children)

        Closest to a point:
            closest(23.456, 23.456, 'group.children')
            closest('zone.school', 'group.children')
            closest(states.zone.school, 'group.children')

        As a filter:
            states | closest
            states.device_tracker | closest
            ['group.children', states.device_tracker] | closest
            'group.children' | closest(23.456, 23.456)
            states.device_tracker | closest('zone.school')
            'group.children' | closest(states.zone.school)

        """
        if len(args) == 1:
            latitude = shc.config.latitude
            longitude = shc.config.longitude
            entities = args[0]

        elif len(args) == 2:
            point_state = TemplateEnvironment._resolve_state(shc, args[0])

            if point_state is None:
                _LOGGER.warning(f"Closest:Unable to find state {args[0]}")
                return None
            if not LocationInfo.has_location(point_state):
                _LOGGER.warning(
                    f"Closest:State does not contain valid location: [{point_state}]"
                )
                return None

            latitude = point_state.attributes.get(Const.ATTR_LATITUDE)
            longitude = point_state.attributes.get(Const.ATTR_LONGITUDE)

            entities = args[1]

        else:
            latitude = helpers.convert(args[0], float)
            longitude = helpers.convert(args[1], float)

            if latitude is None or longitude is None:
                _LOGGER.warning(
                    f"Closest:Received invalid coordinates: {args[0]}, {args[1]}"
                )
                return None

            entities = args[2]

        states = TemplateEnvironment.expand(shc, entities)

        # state will already be wrapped here
        return LocationInfo.closest(latitude, longitude, states)

    @staticmethod
    def closest_filter(shc: SmartHomeController, *args):
        """Call closest as a filter. Need to reorder arguments."""
        new_args = list(args[1:])
        new_args.append(args[0])
        return TemplateEnvironment.closest(shc, *new_args)

    @staticmethod
    def distance(shc: SmartHomeController, *args):
        """Calculate distance.

        Will calculate distance from home to a point or between points.
        Points can be passed in using state objects or lat/lng coordinates.
        """
        locations = []

        to_process = list(args)

        while to_process:
            value = to_process.pop(0)
            if isinstance(value, str) and not helpers.valid_entity_id(value):
                point_state = None
            else:
                point_state = TemplateEnvironment._resolve_state(shc, value)

            if point_state is None:
                # We expect this and next value to be lat&lng
                if not to_process:
                    _LOGGER.warning(
                        f"Distance:Expected latitude and longitude, got {value}"
                    )
                    return None

                value_2 = to_process.pop(0)
                latitude = helpers.convert(value, float)
                longitude = helpers.convert(value_2, float)

                if latitude is None or longitude is None:
                    _LOGGER.warning(
                        "Distance:Unable to process latitude and longitude: "
                        + f"{value}, {value_2}"
                    )
                    return None

            else:
                if not LocationInfo.has_location(point_state):
                    _LOGGER.warning(
                        f"Distance:State does not contain valid location: {point_state}"
                    )
                    return None

                latitude = point_state.attributes.get(Const.ATTR_LATITUDE)
                longitude = point_state.attributes.get(Const.ATTR_LONGITUDE)

            locations.append((latitude, longitude))

        if len(locations) == 1:
            return shc.config.distance(*locations[0])

        return shc.config.units.length(
            LocationInfo.distance(*locations[0] + locations[1]), Const.LENGTH_METERS
        )

    @staticmethod
    def is_state(shc: SmartHomeController, entity_id: str, state: State) -> bool:
        """Test if a state is a specific value."""
        state_obj = TemplateEnvironment.get_state(shc, entity_id)
        return state_obj is not None and state_obj.state == state

    @staticmethod
    def is_state_attr(
        shc: SmartHomeController, entity_id: str, name: str, value: typing.Any
    ) -> bool:
        """Test if a state's attribute is a specific value."""
        attr = TemplateEnvironment.state_attr(shc, entity_id, name)
        return attr is not None and attr == value

    @staticmethod
    def state_attr(shc: SmartHomeController, entity_id: str, name: str) -> typing.Any:
        """Get a specific attribute from a state."""
        if (state_obj := TemplateEnvironment.get_state(shc, entity_id)) is not None:
            return state_obj.attributes.get(name)
        return None

    @staticmethod
    def now() -> dt.datetime:
        """Record fetching now."""
        if (render_info := ri.current) is not None:
            render_info.has_time = True

        return helpers.now()

    @staticmethod
    def utcnow() -> dt.datetime:
        """Record fetching utcnow."""
        if (render_info := ri.current) is not None:
            render_info.has_time = True

        return helpers.utcnow()

    @staticmethod
    def expand(
        shc: SmartHomeController, *args: typing.Any
    ) -> collections.abc.Iterable[State]:
        """Expand out any groups and zones into entity states."""
        search = list(args)
        found = {}
        while search:
            entity = search.pop()
            if isinstance(entity, str):
                entity_id = entity
                if (entity := TemplateEnvironment.get_state(shc, entity)) is None:
                    continue
            elif isinstance(entity, State):
                entity_id = entity.entity_id
            elif isinstance(entity, collections.abc.Iterable):
                search += entity
                continue
            else:
                # ignore other types
                continue

            if entity_id.startswith(_GROUP_DOMAIN_PREFIX) or (
                (source := shc.entity_sources.get(entity_id))
                and source["domain"] == "group"
            ):
                # Collect state will be called in here since it's wrapped
                if group_entities := entity.attributes.get(Const.ATTR_ENTITY_ID):
                    search += group_entities
            elif entity_id.startswith(_ZONE_DOMAIN_PREFIX):
                if zone_entities := entity.attributes.get(Const.ATTR_PERSONS):
                    search += zone_entities
            else:
                _collect_state(entity_id)
                found[entity_id] = entity

        return sorted(found.values(), key=lambda a: a.entity_id)


_cache: dict[TemplateEnvironmentType, TemplateEnvironment] = {}
