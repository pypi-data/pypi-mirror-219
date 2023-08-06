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

# pylint: disable=unused-variable
import dataclasses
import typing


# pylint: disable=unused-variable
@dataclasses.dataclass()
class SourceAdapter:
    """Adapter to allow sources and their flows to be used as sensors."""

    source_type: typing.Literal["grid", "gas", "water"]
    flow_type: typing.Literal["flow_from", "flow_to", None]
    stat_energy_key: typing.Literal["stat_energy_from", "stat_energy_to"]
    total_money_key: typing.Literal["stat_cost", "stat_compensation"]
    name_suffix: str
    entity_id_suffix: str
