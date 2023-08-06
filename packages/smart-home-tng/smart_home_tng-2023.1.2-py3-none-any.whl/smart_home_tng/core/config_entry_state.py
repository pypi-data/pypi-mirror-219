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


_T = typing.TypeVar("_T", bound="ConfigEntryState")


# pylint: disable=unused-variable
class ConfigEntryState(enum.Enum):
    """Config entry state."""

    LOADED = "loaded", True
    """The config entry has been set up successfully"""
    SETUP_ERROR = "setup_error", True
    """There was an error while trying to set up this config entry"""
    MIGRATION_ERROR = "migration_error", False
    """There was an error while trying to migrate the config entry to a new version"""
    SETUP_RETRY = "setup_retry", True
    """The config entry was not ready to be set up yet, but might be later"""
    NOT_LOADED = "not_loaded", True
    """The config entry has not been loaded"""
    FAILED_UNLOAD = "failed_unload", False
    """An error occurred when trying to unload the entry"""

    _recoverable: bool  # pylint: disable=invalid-name

    def __new__(cls: type[_T], value: str, recoverable: bool) -> _T:
        """Create new ConfigEntryState."""
        obj = object.__new__(cls)
        obj._value_ = value
        obj._recoverable = recoverable
        return obj

    @property
    def recoverable(self) -> bool:
        """Get if the state is recoverable."""
        return self._recoverable
