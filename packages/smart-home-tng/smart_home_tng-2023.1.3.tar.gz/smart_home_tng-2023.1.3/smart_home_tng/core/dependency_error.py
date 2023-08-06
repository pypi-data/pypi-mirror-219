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

from .smart_home_controller_error import SmartHomeControllerError


# pylint: disable=unused-variable
class DependencyError(SmartHomeControllerError):
    """Raised when dependencies can not be setup."""

    def __init__(self, failed_dependencies: list[str]) -> None:
        """Initialize error."""
        super().__init__(
            self,
            f"Could not setup dependencies: {', '.join(failed_dependencies)}",
        )
        self.failed_dependencies = failed_dependencies
