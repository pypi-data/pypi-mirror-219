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


This module includes all classes that are required to support
platform compiled statistics for the recorder component.
"""

# pylint: disable=unused-variable

import dataclasses
import datetime as dt
import typing

from .unit_conversion import (
    BaseUnitConverter,
    DistanceConverter,
    EnergyConverter,
    MassConverter,
    PowerConverter,
    PressureConverter,
    SpeedConverter,
    TemperatureConverter,
    VolumeConverter,
)


class Statistic:
    """Statistic namespace."""

    class MetaData(typing.TypedDict):
        """Statistic meta data class."""

        has_mean: bool
        has_sum: bool
        name: str
        source: str
        statistic_id: str
        unit_of_measurement: str

    class DataBase(typing.TypedDict):
        """Mandatory fields for statistic data class."""

        start: dt.datetime

    class Data(DataBase, total=False):
        """Statistic data class."""

        mean: float
        min: float
        max: float
        last_reset: dt.datetime
        state: float
        sum: float

    class Result(typing.TypedDict):
        """Statistic result data class.

        Allows multiple datapoints for the same statistic_id.
        """

        meta: "Statistic.MetaData"
        stat: "Statistic.Data"

    @dataclasses.dataclass()
    class PlatformCompiledStatistics:
        """Compiled Statistics from a platform."""

        platform_stats: list["Statistic.Result"]
        current_metadata: dict[str, tuple[int, "Statistic.MetaData"]]

    STATISTIC_UNIT_TO_UNIT_CONVERTER: typing.Final[
        dict[str, type[BaseUnitConverter]]
    ] = {
        **{unit: DistanceConverter for unit in DistanceConverter.VALID_UNITS},
        **{unit: EnergyConverter for unit in EnergyConverter.VALID_UNITS},
        **{unit: MassConverter for unit in MassConverter.VALID_UNITS},
        **{unit: PowerConverter for unit in PowerConverter.VALID_UNITS},
        **{unit: PressureConverter for unit in PressureConverter.VALID_UNITS},
        **{unit: SpeedConverter for unit in SpeedConverter.VALID_UNITS},
        **{unit: TemperatureConverter for unit in TemperatureConverter.VALID_UNITS},
        **{unit: VolumeConverter for unit in VolumeConverter.VALID_UNITS},
    }
