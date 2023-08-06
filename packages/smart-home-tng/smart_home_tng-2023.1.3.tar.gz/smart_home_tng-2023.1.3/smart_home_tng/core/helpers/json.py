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
import json
import logging
import pathlib
import typing

from ..serialization_error import SerializationError
from ..smart_home_controller_error import SmartHomeControllerError
from .file import write_utf8_file, write_utf8_file_atomic

_LOGGER: typing.Final = logging.getLogger(__name__)


if not typing.TYPE_CHECKING:

    class Event:
        pass

    class State:
        pass


if typing.TYPE_CHECKING:
    from ..event import Event
    from ..state import State


# pylint: disable=unused-variable


def load_json(filename: str, default: list | dict = None) -> list | dict:
    """Load JSON data from a file and return as dict or list.

    Defaults to returning empty dict if file is not found.
    """
    if not pathlib.Path(filename).is_file():
        return {} if default is None else default

    try:
        with open(filename, encoding="utf-8") as fdesc:
            return json.loads(fdesc.read())
    except FileNotFoundError:
        # This is not a fatal error
        _LOGGER.debug(f"JSON file not found: {filename}")
    except ValueError as error:
        _LOGGER.exception(f"Could not parse JSON content: {filename}")
        raise SmartHomeControllerError(error) from error
    except OSError as error:
        _LOGGER.exception(f"JSON file reading failed: {filename}")
        raise SmartHomeControllerError(error) from error
    return {} if default is None else default


def save_json(
    filename: str,
    data: list | dict,
    private: bool = False,
    *,
    encoder: type[json.JSONEncoder] = None,
    atomic_writes: bool = False,
) -> None:
    """Save JSON data to a file.

    Returns True on success.
    """
    try:
        json_data = json.dumps(data, indent=4, cls=encoder)
    except TypeError as error:
        msg = (
            f"Failed to serialize to JSON: {filename}. Bad data at "
            + f"{format_unserializable_data(find_paths_unserializable_data(data))}"
        )
        _LOGGER.error(msg)
        raise SerializationError(msg) from error

    if atomic_writes:
        write_utf8_file_atomic(filename, json_data, private)
    else:
        write_utf8_file(filename, json_data, private)


def format_unserializable_data(data: dict[str, typing.Any]) -> str:
    """Format output of find_paths in a friendly way.

    Format is comma separated: <path>=<value>(<type>)
    """
    return ", ".join(f"{path}={value}({type(value)}" for path, value in data.items())


def find_paths_unserializable_data(
    bad_data: typing.Any, *, dump_func: typing.Callable[[typing.Any], str] = json.dumps
) -> dict[str, typing.Any]:
    """Find the paths to unserializable data.

    This method is slow! Only use for error handling.
    """
    to_process = collections.deque([(bad_data, "$")])
    invalid = {}

    while to_process:
        obj, obj_path = to_process.popleft()

        try:
            dump_func(obj)
            continue
        except (ValueError, TypeError):
            pass

        # We convert objects with as_dict to their dict values so we can find bad data inside it
        if hasattr(obj, "as_dict"):
            desc = obj.__class__.__name__
            if isinstance(obj, State):
                desc += f": {obj.entity_id}"
            elif isinstance(obj, Event):
                desc += f": {obj.event_type}"

            obj_path += f"({desc})"
            obj = obj.as_dict()

        if isinstance(obj, dict):
            for key, value in obj.items():
                try:
                    # Is key valid?
                    dump_func({key: None})
                except TypeError:
                    invalid[f"{obj_path}<key: {key}>"] = key
                else:
                    # Process value
                    to_process.append((value, f"{obj_path}.{key}"))
        elif isinstance(obj, list):
            for idx, value in enumerate(obj):
                to_process.append((value, f"{obj_path}[{idx}]"))
        else:
            invalid[obj_path] = obj

    return invalid


json_loads = json.loads
