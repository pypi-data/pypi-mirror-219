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

from . import helpers


# pylint: disable=unused-variable
class IDManager:
    """Keep track of IDs across different collections."""

    def __init__(self) -> None:
        """Initiate the ID manager."""
        self.collections: list[dict[str, typing.Any]] = []

    def add_collection(self, collection: dict[str, typing.Any]) -> None:
        """Add a collection to check for ID usage."""
        self.collections.append(collection)

    def has_id(self, item_id: str) -> bool:
        """Test if the ID exists."""
        return any(item_id in collection for collection in self.collections)

    def generate_id(self, suggestion: str) -> str:
        """Generate an ID."""
        base = helpers.slugify(suggestion)
        proposal = base
        attempt = 1

        while self.has_id(proposal):
            attempt += 1
            proposal = f"{base}_{attempt}"

        return proposal
