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

import abc
import datetime
import typing

from .protocol import Protocol
from .statistic_business_model import Statistic as _statistic


# pylint: disable=unused-variable
class RecorderStatisticsBase(Protocol):
    """
    Required base class for the statistics implementation of the recorder component.
    """

    @abc.abstractmethod
    def get_metadata(
        self,
        statistic_ids: list[str] | tuple[str] = None,
        statistic_type: typing.Literal["mean"] | typing.Literal["sum"] = None,
        statistic_source: str = None,
    ) -> dict[str, tuple[int, _statistic.MetaData]]:
        """Return metadata for statistic_ids."""

    @abc.abstractmethod
    def statistics_during_period(
        self,
        start_time: datetime.datetime,
        end_time: datetime.datetime,
        statistic_ids: list[str],
        period: typing.Literal["5minute", "day", "hour", "month"],
        units: dict[str, str],
        types: set[
            typing.Literal["change", "last_reset", "max", "mean", "min", "state", "sum"]
        ],
    ) -> dict[str, list[dict[str, typing.Any]]]:
        """Return statistics during UTC period start_time - end_time for the statistic_ids.

        If end_time is omitted, returns statistics newer than or equal to start_time.
        If statistic_ids is omitted, returns statistics for all statistics ids.
        """

    @abc.abstractmethod
    def list_statistic_ids(
        self,
        statistic_ids: list[str] | tuple[str] = None,
        statistic_type: typing.Literal["mean"] | typing.Literal["sum"] = None,
    ) -> list[dict]:
        """Return all statistic_ids (or filtered one) and unit of measurement.

        Queries the database for existing statistic_ids, as well as integrations with
        a recorder platform for statistic_ids which will be added in the next statistics
        period.
        """
