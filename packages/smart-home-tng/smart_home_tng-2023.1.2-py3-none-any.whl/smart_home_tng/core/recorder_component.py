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
import asyncio
import collections.abc
import datetime as dt
import typing

import sqlalchemy as sql

from .callback import callback
from .config_type import ConfigType
from .recorder_filters_base import RecorderFiltersBase
from .recorder_history_base import RecorderHistoryBase
from .recorder_statistics_base import RecorderStatisticsBase
from .smart_home_controller_component import SmartHomeControllerComponent
from .sql_session import SqlSession
from .state import State
from .statistic_business_model import Statistic as _statistic

_T = typing.TypeVar("_T")


# pylint: disable=unused-variable
class RecorderComponent(SmartHomeControllerComponent):
    """Required base class for Recorder Component."""

    @abc.abstractmethod
    def is_entity_recorded(self, entity_id: str) -> bool:
        """Returns if entity is recorded."""

    @property
    @abc.abstractmethod
    def statistics(self) -> RecorderStatisticsBase:
        """Return the RecorderStatistics implementation."""

    @property
    @abc.abstractmethod
    def history(self) -> RecorderHistoryBase:
        """Return the History implementation."""

    @callback
    @abc.abstractmethod
    def async_add_executor_job(
        self, target: collections.abc.Callable[..., _T], *args: typing.Any
    ) -> asyncio.Future[_T]:
        """Add an executor job from within the event loop."""

    @abc.abstractmethod
    def session_scope(
        self,
        *,
        session: SqlSession = None,
        exception_filter: collections.abc.Callable[[Exception], bool] = None,
    ) -> collections.abc.Generator[SqlSession, None, None]:
        """Provide a transactional scope around a series of operations."""

    @abc.abstractmethod
    def sqlalchemy_filter_from_include_exclude_conf(
        self,
        conf: ConfigType,
    ) -> RecorderFiltersBase:
        """Build a sql filter from config."""

    @abc.abstractmethod
    def extract_include_exclude_filter_conf(
        self, conf: ConfigType
    ) -> dict[str, typing.Any]:
        """Extract an include exclude filter from configuration.

        This makes a copy so we do not alter the original data.
        """

    @abc.abstractmethod
    def merge_include_exclude_filters(
        self, base_filter: dict[str, typing.Any], add_filter: dict[str, typing.Any]
    ) -> dict[str, typing.Any]:
        """Merge two filters.

        This makes a copy so we do not alter the original data.
        """

    @abc.abstractmethod
    def statement_for_logbook_request(
        self,
        start_day: dt.datetime,
        end_day: dt.datetime,
        event_types: tuple[str, ...],
        entity_ids: list[str] = None,
        device_ids: list[str] = None,
        filters: RecorderFiltersBase = None,
        context_id: str = None,
    ) -> sql.sql.StatementLambdaElement:
        """Generate the logbook statement for a logbook request."""

    @property
    @abc.abstractmethod
    def pseudo_event_state_changed(self) -> object:
        """Get pseudo event for STATE_CHANGED events."""

    @abc.abstractmethod
    def process_timestamp_to_utc_isoformat(self, timestamp: dt.datetime) -> str:
        """Process a timestamp into UTC isotime."""

    @abc.abstractmethod
    def process_datetime_to_timestamp(self, timestamp: dt.datetime) -> float:
        """Process a datebase datetime to epoch.

        Mirrors the behavior of process_timestamp_to_utc_isoformat
        except it returns the epoch time.
        """

    @abc.abstractmethod
    async def async_block_till_done(self) -> None:
        """Async version of block_till_done."""

    @abc.abstractmethod
    def get_metadata_with_session(
        self,
        session: SqlSession,
        *,
        statistic_ids: list[str] | tuple[str] = None,
        statistic_type: typing.Literal["mean"] | typing.Literal["sum"] = None,
        statistic_source: str = None,
    ) -> dict[str, tuple[int, _statistic.MetaData]]:
        """Fetch meta data.

        Returns a dict of (metadata_id, StatisticMetaData) tuples indexed by statistic_id.

        If statistic_ids is given, fetch metadata only for the listed statistics_ids.
        If statistic_type is given, fetch metadata only for statistic_ids supporting it.
        """

    @abc.abstractmethod
    def get_full_significant_states_with_session(
        self,
        session: SqlSession,
        start_time: dt.datetime,
        end_time: dt.datetime = None,
        entity_ids: list[str] = None,
        filters: RecorderFiltersBase = None,
        include_start_time_state: bool = True,
        significant_changes_only: bool = True,
        no_attributes: bool = False,
    ) -> collections.abc.MutableMapping[str, list[State]]:
        """Variant of get_significant_states_with_session that does not return minimal responses."""

    @abc.abstractmethod
    def get_latest_short_term_statistics(
        self,
        statistic_ids: list[str],
        types: set[typing.Literal["last_reset", "max", "mean", "min", "state", "sum"]],
        metadata: dict[str, tuple[int, _statistic.MetaData]] = None,
    ) -> dict[str, list[dict]]:
        """Return the latest short term statistics for a list of statistic_ids."""
