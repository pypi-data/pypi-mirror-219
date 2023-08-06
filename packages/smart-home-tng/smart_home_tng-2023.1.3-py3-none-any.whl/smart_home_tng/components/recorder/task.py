"""
Recorder Component for Smart Home - The Next Generation.

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

import abc
import asyncio
import collections.abc
import datetime
import threading
import typing
from dataclasses import dataclass

from ... import core
from . import purge, statistics, util

_statistic: typing.TypeAlias = core.Statistic

if not typing.TYPE_CHECKING:

    class Recorder:
        ...


if typing.TYPE_CHECKING:
    from .recorder import Recorder


class RecorderTask(abc.ABC):
    """ABC for recorder tasks."""

    commit_before = True

    @abc.abstractmethod
    def run(self, instance: Recorder) -> None:
        """Handle the task."""


@dataclass()
class ClearStatisticsTask(RecorderTask):
    """Object to store statistics_ids which for which to remove statistics."""

    statistic_ids: list[str]

    def run(self, instance: Recorder) -> None:
        """Handle the task."""
        statistics.clear_statistics(instance, self.statistic_ids)


@dataclass()
class UpdateStatisticsMetadataTask(RecorderTask):
    """Object to store statistics_id and unit for update of statistics metadata."""

    statistic_id: str
    new_statistic_id: str | object
    new_unit_of_measurement: str | object

    def run(self, instance: Recorder) -> None:
        """Handle the task."""
        statistics.update_statistics_metadata(
            instance,
            self.statistic_id,
            self.new_statistic_id,
            self.new_unit_of_measurement,
        )


@dataclass()
class PurgeTask(RecorderTask):
    """Object to store information about purge task."""

    purge_before: datetime
    repack: bool
    apply_filter: bool

    def run(self, instance: Recorder) -> None:
        """Purge the database."""
        if purge.purge_old_data(
            instance, self.purge_before, self.repack, self.apply_filter
        ):
            with instance.get_session() as session:
                instance.run_history.load_from_db(session)
            # We always need to do the db cleanups after a purge
            # is finished to ensure the WAL checkpoint and other
            # tasks happen after a vacuum.
            util.periodic_db_cleanups(instance)
            return
        # Schedule a new purge task if this one didn't finish
        instance.queue_task(
            PurgeTask(self.purge_before, self.repack, self.apply_filter)
        )


@dataclass()
class PurgeEntitiesTask(RecorderTask):
    """Object to store entity information about purge task."""

    entity_filter: collections.abc.Callable[[str], bool]

    def run(self, instance: Recorder) -> None:
        """Purge entities from the database."""
        if purge.purge_entity_data(instance, self.entity_filter):
            return
        # Schedule a new purge task if this one didn't finish
        instance.queue_task(PurgeEntitiesTask(self.entity_filter))


@dataclass()
class PeriodicCleanupTask(RecorderTask):
    """
    An object to insert into the recorder to trigger cleanup tasks
    when auto purge is disabled.
    """

    def run(self, instance: Recorder) -> None:
        """Handle the task."""
        util.periodic_db_cleanups(instance)


@dataclass()
class StatisticsTask(RecorderTask):
    """An object to insert into the recorder queue to run a statistics task."""

    start: datetime.datetime

    def run(self, instance: Recorder) -> None:
        """Run statistics task."""
        if statistics.compile_statistics(instance, self.start):
            return
        # Schedule a new statistics task if this one didn't finish
        instance.queue_task(StatisticsTask(self.start))


@dataclass()
class ExternalStatisticsTask(RecorderTask):
    """An object to insert into the recorder queue to run an external statistics task."""

    metadata: _statistic.MetaData
    statistics: collections.abc.Iterable[_statistic.Data]

    def run(self, instance: Recorder) -> None:
        """Run statistics task."""
        if statistics.add_external_statistics(instance, self.metadata, self.statistics):
            return
        # Schedule a new statistics task if this one didn't finish
        instance.queue_task(ExternalStatisticsTask(self.metadata, self.statistics))


@dataclass()
class AdjustStatisticsTask(RecorderTask):
    """An object to insert into the recorder queue to run an adjust statistics task."""

    statistic_id: str
    start_time: datetime
    sum_adjustment: float
    adjustment_unit: str

    def run(self, instance: Recorder) -> None:
        """Run statistics task."""
        if statistics.adjust_statistics(
            instance,
            self.statistic_id,
            self.start_time,
            self.sum_adjustment,
            self.adjustment_unit,
        ):
            return
        # Schedule a new adjust statistics task if this one didn't finish
        instance.queue_task(
            AdjustStatisticsTask(
                self.statistic_id,
                self.start_time,
                self.sum_adjustment,
                self.adjustment_unit,
            )
        )


@dataclass()
class WaitTask(RecorderTask):
    """An object to insert into the recorder queue to tell it set the _queue_watch event."""

    commit_before = False

    def run(self, instance: Recorder) -> None:
        """Handle the task."""
        instance._queue_watch.set()  # pylint: disable=[protected-access]


@dataclass()
class DatabaseLockTask(RecorderTask):
    """An object to insert into the recorder queue to prevent writes to the database."""

    database_locked: asyncio.Event
    database_unlock: threading.Event
    queue_overflow: bool

    def run(self, instance: Recorder) -> None:
        """Handle the task."""
        instance._lock_database(self)  # pylint: disable=[protected-access]


@dataclass()
class StopTask(RecorderTask):
    """An object to insert into the recorder queue to stop the event handler."""

    commit_before = False

    def run(self, instance: Recorder) -> None:
        """Handle the task."""
        # pylint: disable=protected-access
        instance._stop_requested = True


@dataclass()
class EventTask(RecorderTask):
    """An event to be processed."""

    event: core.Event
    commit_before = False

    def run(self, instance: Recorder) -> None:
        """Handle the task."""
        # pylint: disable-next=[protected-access]
        instance._process_one_event(self.event)


@dataclass()
class KeepAliveTask(RecorderTask):
    """A keep alive to be sent."""

    commit_before = False

    def run(self, instance: Recorder) -> None:
        """Handle the task."""
        # pylint: disable-next=[protected-access]
        instance._send_keep_alive()


@dataclass()
class CommitTask(RecorderTask):
    """Commit the event session."""

    commit_before = False

    def run(self, instance: Recorder) -> None:
        """Handle the task."""
        # pylint: disable-next=[protected-access]
        instance._commit_event_session_or_retry()


@dataclass()
class AddRecorderPlatformTask(RecorderTask):
    """Add a recorder platform."""

    domain: str
    platform: core.RecorderPlatform
    commit_before = False

    def run(self, instance: Recorder) -> None:
        """Handle the task."""
        owner = instance.owner
        domain = self.domain
        platform = self.platform

        owner.add_platform(domain, platform)


@dataclass()
class SynchronizeTask(RecorderTask):
    """Ensure all pending data has been committed."""

    # commit_before is the default
    event: asyncio.Event

    def run(self, instance: Recorder) -> None:
        """Handle the task."""
        # Does not use a tracked task to avoid
        # blocking shutdown if the recorder is broken
        instance.owner.controller.call_soon_threadsafe(self.event.set)
