"""
Helpers for Components of Smart Home - The Next Generation.

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

import bisect
import contextlib
import datetime
import re
import typing
import zoneinfo

import ciso8601

_DATE_STR_FORMAT: typing.Final = "%Y-%m-%d"
_UTC: typing.Final = datetime.timezone.utc

# EPOCHORDINAL is not exposed as a constant
# https://github.com/python/cpython/blob/3.10/Lib/zoneinfo/_zoneinfo.py#L12
_EPOCHORDINAL = datetime.datetime(1970, 1, 1).toordinal()

# Copyright (c) Django Software Foundation and individual contributors.
# All rights reserved.
# https://github.com/django/django/blob/master/LICENSE
_DATETIME_RE: typing.Final = re.compile(
    r"(?P<year>\d{4})-(?P<month>\d{1,2})-(?P<day>\d{1,2})"
    + r"[T ](?P<hour>\d{1,2}):(?P<minute>\d{1,2})"
    + r"(?::(?P<second>\d{1,2})(?:\.(?P<microsecond>\d{1,6})\d{0,6})?)?"
    + r"(?P<tzinfo>Z|[+-]\d{2}(?::?\d{2})?)?$"
)

# Copyright (c) Django Software Foundation and individual contributors.
# All rights reserved.
# https://github.com/django/django/blob/master/LICENSE
_STANDARD_DURATION_RE: typing.Final = re.compile(
    r"^"
    + r"(?:(?P<days>-?\d+) (days?, )?)?"
    + r"(?P<sign>-?)"
    + r"((?:(?P<hours>\d+):)(?=\d+:\d+))?"
    + r"(?:(?P<minutes>\d+):)?"
    + r"(?P<seconds>\d+)"
    + r"(?:[\.,](?P<microseconds>\d{1,6})\d{0,6})?"
    + r"$"
)

# Copyright (c) Django Software Foundation and individual contributors.
# All rights reserved.
# https://github.com/django/django/blob/master/LICENSE
_ISO8601_DURATION_RE: typing.Final = re.compile(
    r"^(?P<sign>[-+]?)"
    + r"P"
    + r"(?:(?P<days>\d+([\.,]\d+)?)D)?"
    + r"(?:T"
    + r"(?:(?P<hours>\d+([\.,]\d+)?)H)?"
    + r"(?:(?P<minutes>\d+([\.,]\d+)?)M)?"
    + r"(?:(?P<seconds>\d+([\.,]\d+)?)S)?"
    + r")?"
    + r"$"
)

# Copyright (c) Django Software Foundation and individual contributors.
# All rights reserved.
# https://github.com/django/django/blob/master/LICENSE
_POSTGRES_INTERVAL_RE: typing.Final = re.compile(
    r"^"
    + r"(?:(?P<days>-?\d+) (days? ?))?"
    + r"(?:(?P<sign>[-+])?"
    + r"(?P<hours>\d+):"
    + r"(?P<minutes>\d\d):"
    + r"(?P<seconds>\d\d)"
    + r"(?:\.(?P<microseconds>\d{1,6}))?"
    + r")?$"
)

# pylint: disable=unused-variable


class _TimeZoneSettings:
    """Store the default time zone information."""

    default_time_zone = datetime.timezone.utc


def set_default_time_zone(time_zone: datetime.tzinfo) -> None:
    """Set a default time zone to be used when none is specified.

    Async friendly.
    """
    assert isinstance(time_zone, datetime.tzinfo)

    _TimeZoneSettings.default_time_zone = time_zone


def get_default_time_zone() -> datetime.timezone:
    return _TimeZoneSettings.default_time_zone


def get_time_zone(time_zone_str: str) -> datetime.tzinfo:
    """Get time zone from string. Return None if unable to determine.

    Async friendly.
    """
    try:
        return zoneinfo.ZoneInfo(time_zone_str)
    except zoneinfo.ZoneInfoNotFoundError:
        return None


def utcnow() -> datetime.datetime:
    """Get now in UTC time."""
    return datetime.datetime.now(_UTC)


def now(time_zone: datetime.tzinfo = None) -> datetime.datetime:
    """Get now in specified time zone."""
    return datetime.datetime.now(time_zone or _TimeZoneSettings.default_time_zone)


def as_utc(dattim: datetime.datetime) -> datetime.datetime:
    """Return a datetime as UTC time.

    Assumes datetime without tzinfo to be in the DEFAULT_TIME_ZONE.
    """
    if dattim.tzinfo == _UTC:
        return dattim
    if dattim.tzinfo is None:
        dattim = dattim.replace(tzinfo=_TimeZoneSettings.default_time_zone)

    return dattim.astimezone(_UTC)


def as_timestamp(dt_value: datetime.datetime | str) -> float:
    """Convert a date/time into a unix time (seconds since 1970)."""
    parsed_dt: datetime.datetime
    if isinstance(dt_value, datetime.datetime):
        parsed_dt = dt_value
    else:
        parsed_dt = parse_datetime(str(dt_value))
    if parsed_dt is None:
        raise ValueError("not a valid date/time.")
    return parsed_dt.timestamp()


def as_local(dattim: datetime.datetime) -> datetime.datetime:
    """Convert a UTC datetime object to local time zone."""
    if dattim.tzinfo == _TimeZoneSettings.default_time_zone:
        return dattim
    if dattim.tzinfo is None:
        dattim = dattim.replace(tzinfo=_TimeZoneSettings.default_time_zone)

    return dattim.astimezone(_TimeZoneSettings.default_time_zone)


def utc_from_timestamp(timestamp: float) -> datetime.datetime:
    """Return a UTC time from a timestamp."""
    return datetime.datetime.utcfromtimestamp(timestamp).replace(tzinfo=_UTC)


def utc_to_timestamp(utc_dt: datetime.datetime) -> float:
    """Fast conversion of a datetime in UTC to a timestamp."""
    # Taken from
    # https://github.com/python/cpython/blob/3.10/Lib/zoneinfo/_zoneinfo.py#L185
    return (
        (utc_dt.toordinal() - _EPOCHORDINAL) * 86400
        + utc_dt.hour * 3600
        + utc_dt.minute * 60
        + utc_dt.second
        + (utc_dt.microsecond / 1000000)
    )


def start_of_local_day(
    dt_or_d: datetime.date | datetime.datetime = None,
) -> datetime.datetime:
    """Return local datetime object of start of day from date or datetime."""
    if dt_or_d is None:
        date: datetime.date = now().date()
    elif isinstance(dt_or_d, datetime.datetime):
        date = dt_or_d.date()
    else:
        date = dt_or_d

    return datetime.datetime.combine(
        date, datetime.time(), tzinfo=_TimeZoneSettings.default_time_zone
    )


# Copyright (c) Django Software Foundation and individual contributors.
# All rights reserved.
# https://github.com/django/django/blob/master/LICENSE
def parse_datetime(dt_str: str) -> datetime.datetime:
    """Parse a string and return a datetime.datetime.

    This function supports time zone offsets. When the input contains one,
    the output uses a timezone with a fixed offset from UTC.
    Raises ValueError if the input is well formatted but not a valid datetime.
    Returns None if the input isn't well formatted.
    """
    with contextlib.suppress(ValueError, IndexError):
        return ciso8601.parse_datetime(dt_str)

    if not (match := _DATETIME_RE.match(dt_str)):
        return None
    kws: dict[str, typing.Any] = match.groupdict()
    if kws["microsecond"]:
        kws["microsecond"] = kws["microsecond"].ljust(6, "0")
    tzinfo_str = kws.pop("tzinfo")

    tzinfo: datetime.tzinfo = None
    if tzinfo_str == "Z":
        tzinfo = _UTC
    elif tzinfo_str is not None:
        offset_mins = int(tzinfo_str[-2:]) if len(tzinfo_str) > 3 else 0
        offset_hours = int(tzinfo_str[1:3])
        offset = datetime.timedelta(hours=offset_hours, minutes=offset_mins)
        if tzinfo_str[0] == "-":
            offset = -offset
        tzinfo = datetime.timezone(offset)
    kws = {k: int(v) for k, v in kws.items() if v is not None}
    kws["tzinfo"] = tzinfo
    return datetime.datetime(**kws)


def parse_date(dt_str: str) -> datetime.date:
    """Convert a date string to a date object."""
    try:
        return datetime.datetime.strptime(dt_str, _DATE_STR_FORMAT).date()
    except ValueError:  # If dt_str did not match our format
        return None


# Copyright (c) Django Software Foundation and individual contributors.
# All rights reserved.
# https://github.com/django/django/blob/master/LICENSE
def parse_duration(value: str) -> datetime.timedelta:
    """Parse a duration string and return a datetime.timedelta.

    Also supports ISO 8601 representation and PostgreSQL's day-time interval
    format.
    """
    match = (
        _STANDARD_DURATION_RE.match(value)
        or _ISO8601_DURATION_RE.match(value)
        or _POSTGRES_INTERVAL_RE.match(value)
    )
    if match:
        kws = match.groupdict()
        sign = -1 if kws.pop("sign", "+") == "-" else 1
        if kws.get("microseconds"):
            kws["microseconds"] = kws["microseconds"].ljust(6, "0")
        time_delta_args: dict[str, float] = {
            k: float(v.replace(",", ".")) for k, v in kws.items() if v is not None
        }
        days = datetime.timedelta(float(time_delta_args.pop("days", 0.0) or 0.0))
        if match.re == _ISO8601_DURATION_RE:
            days *= sign
        return days + sign * datetime.timedelta(**time_delta_args)
    return None


def parse_time(time_str: str) -> datetime.time:
    """Parse a time string (00:20:00) into Time object.

    Return None if invalid.
    """
    parts = str(time_str).split(":")
    if len(parts) < 2:
        return None
    try:
        hour = int(parts[0])
        minute = int(parts[1])
        second = int(parts[2]) if len(parts) > 2 else 0
        return datetime.time(hour, minute, second)
    except ValueError:
        # ValueError if value cannot be converted to an int or not in range
        return None


def get_age(date: datetime.datetime) -> str:
    """
    Take a datetime and return its "age" as a string.

    The age can be in second, minute, hour, day, month or year. Only the
    biggest unit is considered, e.g. if it's 2 days and 3 hours, "2 days" will
    be returned.
    Make sure date is not in the future, or else it won't work.
    """

    def formatn(number: int, unit: str) -> str:
        """Add "unit" if it's plural."""
        if number == 1:
            return f"1 {unit}"
        return f"{number:d} {unit}s"

    delta = (now() - date).total_seconds()
    rounded_delta = round(delta)

    units = ["second", "minute", "hour", "day", "month"]
    factors = [60, 60, 24, 30, 12]
    selected_unit = "year"

    for i, next_factor in enumerate(factors):
        if rounded_delta < next_factor:
            selected_unit = units[i]
            break
        delta /= next_factor
        rounded_delta = round(delta)

    return formatn(rounded_delta, selected_unit)


def parse_time_expression(
    parameter: typing.Any, min_value: int, max_value: int
) -> list[int]:
    """Parse the time expression part and return a list of times to match."""
    if parameter is None or parameter == "*":
        res = list(range(min_value, max_value + 1))
    elif isinstance(parameter, str):
        if parameter.startswith("/"):
            parameter = int(parameter[1:])
            res = [x for x in range(min_value, max_value + 1) if x % parameter == 0]
        else:
            res = [int(parameter)]

    elif not hasattr(parameter, "__iter__"):
        res = [int(parameter)]
    else:
        res = sorted(int(x) for x in parameter)

    for val in res:
        if val < min_value or val > max_value:
            raise ValueError(
                f"Time expression '{parameter}': parameter {val} out of range "
                f"({min_value} to {max_value})"
            )

    return res


def _dst_offset_diff(dattim: datetime.datetime) -> datetime.timedelta:
    """Return the offset when crossing the DST barrier."""
    delta = datetime.timedelta(hours=24)
    return (dattim + delta).utcoffset() - (dattim - delta).utcoffset()


def _lower_bound(arr: list[int], cmp: int) -> int:
    """Return the first value in arr greater or equal to cmp.

    Return None if no such value exists.
    """
    if (left := bisect.bisect_left(arr, cmp)) == len(arr):
        return None
    return arr[left]


def find_next_time_expression_time(
    dt_now: datetime.datetime,
    seconds: list[int],
    minutes: list[int],
    hours: list[int],
) -> datetime.datetime:
    """Find the next datetime from now for which the time expression matches.

    The algorithm looks at each time unit separately and tries to find the
    next one that matches for each. If any of them would roll over, all
    time units below that are reset to the first matching value.

    Timezones are also handled (the tzinfo of the now object is used),
    including daylight saving time.
    """
    if not seconds or not minutes or not hours:
        raise ValueError("Cannot find a next time: Time expression never matches!")

    while True:
        # Reset microseconds and fold; fold (for ambiguous DST times) will be handled later
        result = dt_now.replace(microsecond=0, fold=0)

        # Match next second
        if (next_second := _lower_bound(seconds, result.second)) is None:
            # No second to match in this minute. Roll-over to next minute.
            next_second = seconds[0]
            result += datetime.timedelta(minutes=1)

        result = result.replace(second=next_second)

        # Match next minute
        next_minute = _lower_bound(minutes, result.minute)
        if next_minute != result.minute:
            # We're in the next minute. Seconds needs to be reset.
            result = result.replace(second=seconds[0])

        if next_minute is None:
            # No minute to match in this hour. Roll-over to next hour.
            next_minute = minutes[0]
            result += datetime.timedelta(hours=1)

        result = result.replace(minute=next_minute)

        # Match next hour
        next_hour = _lower_bound(hours, result.hour)
        if next_hour != result.hour:
            # We're in the next hour. Seconds+minutes needs to be reset.
            result = result.replace(second=seconds[0], minute=minutes[0])

        if next_hour is None:
            # No minute to match in this day. Roll-over to next day.
            next_hour = hours[0]
            result += datetime.timedelta(days=1)

        result = result.replace(hour=next_hour)

        if result.tzinfo in (None, _UTC):
            # Using UTC, no DST checking needed
            return result

        if not _datetime_exists(result):
            # When entering DST and clocks are turned forward.
            # There are wall clock times that don't "exist" (an hour is skipped).

            # -> trigger on the next time that 1. matches the pattern and 2. does exist
            # for example:
            #   on 2021.03.28 02:00:00 in CET timezone clocks are turned forward an hour
            #   with pattern "02:30", don't run on 28 mar (such a wall time does not
            #   exist on this day instead run at 02:30 the next day

            # We solve this edge case by just iterating one second until the result exists
            # (max. 3600 operations, which should be fine for an edge case that happens once a year)
            dt_now += datetime.timedelta(seconds=1)
            continue

        if not _datetime_ambiguous(dt_now):
            return result

        # When leaving DST and clocks are turned backward.
        # Then there are wall clock times that are ambiguous i.e. exist with DST and without DST
        # The logic above does not take into account if a given pattern matches _twice_
        # in a day.
        # Example: on 2021.10.31 02:00:00 in CET timezone clocks are turned backward an hour

        if _datetime_ambiguous(result):
            # `now` and `result` are both ambiguous, so the next match happens
            # _within_ the current fold.

            # Examples:
            #  1. 2021.10.31 02:00:00+02:00 with pattern 02:30 -> 2021.10.31 02:30:00+02:00
            #  2. 2021.10.31 02:00:00+01:00 with pattern 02:30 -> 2021.10.31 02:30:00+01:00
            return result.replace(fold=dt_now.fold)

        if dt_now.fold == 0:
            # `now` is in the first fold, but result is not ambiguous (meaning it no longer matches
            # within the fold).
            # -> Check if result matches in the next fold. If so, emit that match

            # Turn back the time by the DST offset, effectively run the algorithm on the first fold
            # If it matches on the first fold, that means it will also match on the second one.

            # Example: 2021.10.31 02:45:00+02:00 with pattern 02:30 -> 2021.10.31 02:30:00+01:00

            check_result = find_next_time_expression_time(
                dt_now + _dst_offset_diff(dt_now), seconds, minutes, hours
            )
            if _datetime_ambiguous(check_result):
                return check_result.replace(fold=1)

        return result


def _datetime_exists(dattim: datetime.datetime) -> bool:
    """Check if a datetime exists."""
    assert dattim.tzinfo is not None
    original_tzinfo = dattim.tzinfo
    # Check if we can round trip to UTC
    return dattim == dattim.astimezone(_UTC).astimezone(original_tzinfo)


def _datetime_ambiguous(dattim: datetime.datetime) -> bool:
    """Check whether a datetime is ambiguous."""
    assert dattim.tzinfo is not None
    opposite_fold = dattim.replace(fold=not dattim.fold)
    return _datetime_exists(dattim) and dattim.utcoffset() != opposite_fold.utcoffset()
