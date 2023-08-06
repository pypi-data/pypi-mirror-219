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
import dataclasses
import logging
import typing

_LOGGER: typing.Final = logging.getLogger(__name__)


# pylint: disable=unused-variable
@dataclasses.dataclass()
class SelectedEntities:
    """Class to hold the selected entities."""

    # Entities that were explicitly mentioned.
    referenced: set[str] = dataclasses.field(default_factory=set)

    # Entities that were referenced via device/area ID.
    # Should not trigger a warning when they don't exist.
    indirectly_referenced: set[str] = dataclasses.field(default_factory=set)

    # Referenced items that could not be found.
    missing_devices: set[str] = dataclasses.field(default_factory=set)
    missing_areas: set[str] = dataclasses.field(default_factory=set)

    # Referenced devices
    referenced_devices: set[str] = dataclasses.field(default_factory=set)

    def log_missing(self, missing_entities: set[str]) -> None:
        """Log about missing items."""
        parts = []
        for label, items in (
            ("areas", self.missing_areas),
            ("devices", self.missing_devices),
            ("entities", missing_entities),
        ):
            if items:
                parts.append(f"{label} {', '.join(sorted(items))}")

        if not parts:
            return

        _LOGGER.warning(
            f"Unable to find referenced '{', '.join(parts)}' or it is/they are currently "
            + "not available"
        )
