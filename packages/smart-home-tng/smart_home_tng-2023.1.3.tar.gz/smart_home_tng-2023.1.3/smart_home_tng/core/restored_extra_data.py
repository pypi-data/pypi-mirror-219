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

import typing

from .extra_stored_data import ExtraStoredData


# pylint: disable=unused-variable
class RestoredExtraData(ExtraStoredData):
    """Object to hold extra stored data loaded from storage."""

    def __init__(self, json_dict: dict[str, typing.Any]) -> None:
        """Object to hold extra stored data."""
        self._json_dict = json_dict

    def as_dict(self) -> dict[str, typing.Any]:
        """Return a dict representation of the extra data."""
        return self._json_dict
