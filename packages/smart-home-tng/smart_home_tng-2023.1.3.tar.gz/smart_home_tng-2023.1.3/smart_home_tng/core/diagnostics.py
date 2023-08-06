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

import enum
import typing

from ..backports import strenum
from .callback import callback

_T = typing.TypeVar("_T")
_REDACTED: typing.Final = "**REDACTED**"


class _Type(strenum.LowercaseStrEnum):
    """Diagnostics types."""

    CONFIG_ENTRY = enum.auto()


class _SubType(strenum.LowercaseStrEnum):
    """Diagnostics sub types."""

    DEVICE = enum.auto()


# pylint: disable=unused-variable, invalid-name
class Diagnostics:
    """Diagnostics namespace."""

    SubType: typing.TypeAlias = _SubType
    Type: typing.TypeAlias = _Type

    REDACTED: typing.Final = _REDACTED

    @typing.overload
    @staticmethod
    def async_redact_data(
        data: typing.Mapping, to_redact: typing.Iterable[typing.Any]
    ) -> dict:
        ...

    @typing.overload
    @staticmethod
    def async_redact_data(data: _T, to_redact: typing.Iterable[typing.Any]) -> _T:
        ...

    @staticmethod
    @callback
    def async_redact_data(data: _T, to_redact: typing.Iterable[typing.Any]) -> _T:
        """Redact sensitive data in a dict."""
        if not isinstance(data, (typing.Mapping, list)):
            return data

        if isinstance(data, list):
            return typing.cast(
                _T, [Diagnostics.async_redact_data(val, to_redact) for val in data]
            )

        redacted = {**data}

        for key, value in redacted.items():
            if value is None:
                continue
            if isinstance(value, str) and not value:
                continue
            if key in to_redact:
                redacted[key] = _REDACTED
            elif isinstance(value, typing.Mapping):
                redacted[key] = Diagnostics.async_redact_data(value, to_redact)
            elif isinstance(value, list):
                redacted[key] = [
                    Diagnostics.async_redact_data(item, to_redact) for item in value
                ]

        return typing.cast(_T, redacted)
