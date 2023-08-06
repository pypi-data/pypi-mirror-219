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

import collections.abc

import attr

from . import helpers


# pylint: disable=unused-variable
@attr.s(slots=True, frozen=True)
class Area:
    """Area Registry Entry."""

    name: str = attr.ib()
    normalized_name: str = attr.ib()
    picture: str = attr.ib(default=None)
    id: str = attr.ib(default=None)

    def generate_id(self, existing_ids: collections.abc.Container[str]) -> None:
        """Initialize ID."""
        suggestion = suggestion_base = helpers.slugify(self.name)
        tries = 1
        while suggestion in existing_ids:
            suggestion = f"{suggestion_base}_{tries}"
            tries += 1
        object.__setattr__(self, "id", suggestion)
