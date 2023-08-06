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

import collections.abc
import datetime
import functools
import random
import re
import string
import typing

import slugify as unicode_slug

from ..callback import callback
from ..const import Const
from . import dt

_T = typing.TypeVar("_T")
_U = typing.TypeVar("_U")

_RE_SANITIZE_FILENAME: typing.Final = re.compile(r"(~|\.\.|/|\\)")
_RE_SANITIZE_PATH: typing.Final = re.compile(r"(~|\.(\.)+)")
_VALID_ENTITY_ID: typing.Final = re.compile(
    r"^(?!.+__)(?!_)[\da-z_]+(?<!_)\.(?!_)[\da-z_]+(?<!_)$"
)

if not typing.TYPE_CHECKING:

    class SmartHomeController:
        pass


if typing.TYPE_CHECKING:
    from ..smart_home_controller import SmartHomeController


# pylint: disable=unused-variable


def raise_if_invalid_filename(filename: str) -> None:
    """
    Check if a filename is valid.

    Raises a ValueError if the filename is invalid.
    """
    if _RE_SANITIZE_FILENAME.sub("", filename) != filename:
        raise ValueError(f"{filename} is not a safe filename")


def raise_if_invalid_path(path: str) -> None:
    """
    Check if a path is valid.

    Raises a ValueError if the path is invalid.
    """
    if _RE_SANITIZE_PATH.sub("", path) != path:
        raise ValueError(f"{path} is not a safe path")


def convert(value: _T, to_type: typing.Callable[[_T], _U], default: _U = None) -> _U:
    """Convert value to to_type, returns default if fails."""
    try:
        return default if value is None else to_type(value)
    except (ValueError, TypeError):
        # If value could not be converted
        return default


def slugify(text: str, *, separator: str = "_") -> str:
    """Slugify a given text."""
    if text == "" or text is None:
        return ""
    slug = unicode_slug.slugify(text, separator=separator)
    return "unknown" if slug == "" else slug


def repr_helper(inp: typing.Any) -> str:
    """Help creating a more readable string representation of objects."""
    if isinstance(inp, collections.abc.Mapping):
        return ", ".join(
            f"{repr_helper(key)}={repr_helper(item)}" for key, item in inp.items()
        )
    if isinstance(inp, datetime.datetime):
        return dt.as_local(inp).isoformat()

    return str(inp)


def ensure_unique_string(
    preferred_string: str,
    current_strings: collections.abc.Iterable[str] | collections.abc.KeysView[str],
) -> str:
    """Return a string that is not present in current_strings.

    If preferred string exists will append _2, _3, ..
    """
    test_string = preferred_string
    current_strings_set = set(current_strings)

    tries = 1

    while test_string in current_strings_set:
        tries += 1
        test_string = f"{preferred_string}_{tries}"

    return test_string


# Taken from http://stackoverflow.com/a/23728630
def get_random_string(length: int = 10) -> str:
    """Return a random string with letters and digits."""
    generator = random.SystemRandom()
    source_chars = string.ascii_letters + string.digits

    return "".join(generator.choice(source_chars) for _ in range(length))


@functools.lru_cache(Const.MAX_EXPECTED_ENTITY_IDS)
def split_entity_id(entity_id: str) -> tuple[str, str]:
    """Split a state entity ID into domain and object ID."""
    domain, _, object_id = entity_id.partition(".")
    if not domain or not object_id:
        raise ValueError(f"Invalid entity ID {entity_id}")
    return domain, object_id


def valid_entity_id(entity_id: str) -> bool:
    """Test if an entity ID is a valid format.

    Format: <domain>.<entity> where both are slugs.
    """
    return _VALID_ENTITY_ID.match(entity_id) is not None


@callback
def async_generate_entity_id(
    entity_id_format: str,
    name: str,
    current_ids: typing.Iterable[str] = None,
    shc: SmartHomeController = None,
) -> str:
    """Generate a unique entity ID based on given entity IDs or used IDs."""
    name = (name or Const.DEVICE_DEFAULT_NAME).lower()
    preferred_string = entity_id_format.format(slugify(name))

    if current_ids is not None:
        return ensure_unique_string(preferred_string, current_ids)

    if shc is None:
        raise ValueError("Missing required parameter current_ids or shc")

    test_string = preferred_string
    tries = 1
    while not shc.states.async_available(test_string):
        tries += 1
        test_string = f"{preferred_string}_{tries}"

    return test_string
