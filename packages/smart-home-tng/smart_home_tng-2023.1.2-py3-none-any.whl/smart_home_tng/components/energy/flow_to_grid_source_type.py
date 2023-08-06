"""
Energy Component for Smart Home - The Next Generation.

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


# pylint: disable=unused-variable
class FlowToGridSourceType(typing.TypedDict):
    """Dictionary describing the 'to' stat for the grid source."""

    # kWh meter
    stat_energy_to: str

    # statistic_id of compensation ($) received for contributing back
    # If set to None and entity_energy_from and entity_energy_price are configured,
    # an EnergyCostSensor will be automatically created
    stat_compensation: str

    # Used to generate costs if stat_compensation is set to None
    entity_energy_from: str  # entity_id of an energy meter (kWh),
    # entity_id of the energy meter for stat_energy_from
    entity_energy_price: str  # entity_id of an entity providing price ($/kWh)
    number_energy_price: float  # Price for energy ($/kWh)
