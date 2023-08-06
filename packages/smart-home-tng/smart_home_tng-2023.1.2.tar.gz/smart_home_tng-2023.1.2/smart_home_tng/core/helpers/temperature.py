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

import numbers
import typing

from ..const import Const

if not typing.TYPE_CHECKING:

    class SmartHomeController:
        pass


if typing.TYPE_CHECKING:
    from ..smart_home_controller import SmartHomeController


# pylint: disable=unused-variable
def display_temp(
    shc: SmartHomeController, temperature: float, unit: str, precision: float
) -> float:
    """Convert temperature into preferred units/precision for display."""
    temperature_unit = unit

    if temperature is None:
        return temperature

    # If the temperature is not a number this can cause issues
    # with Polymer components, so bail early there.
    if not isinstance(temperature, numbers.Number):
        raise TypeError(f"Temperature is not a number: {temperature}")

    temperature = shc.config.units.temperature(temperature, temperature_unit)

    # Round in the units appropriate
    if precision == Const.PRECISION_HALVES:
        temperature = round(temperature * 2) / 2.0
    elif precision == Const.PRECISION_TENTHS:
        temperature = round(temperature, 1)
    # Integer as a fall back (PRECISION_WHOLE)
    else:
        temperature = round(temperature)

    return temperature
