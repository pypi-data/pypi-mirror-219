"""
Core pieces for Smart Home - The Next Generation.

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

import voluptuous as vol


# pylint: disable=unused-variable
class TimePattern:
    """Validate a time pattern value.

    :raises Invalid: If the value has a wrong format or is outside the range.
    """

    def __init__(self, maximum):
        """Initialize time pattern."""
        self.maximum = maximum

    def __call__(self, value):
        """Validate input."""
        try:
            if value == "*":
                return value

            if isinstance(value, str) and value.startswith("/"):
                number = int(value[1:])
            else:
                value = number = int(value)

            if not 0 <= number <= self.maximum:
                raise vol.Invalid(f"must be a value between 0 and {self.maximum}")
        except ValueError as err:
            raise vol.Invalid("invalid time_pattern value") from err

        return value
