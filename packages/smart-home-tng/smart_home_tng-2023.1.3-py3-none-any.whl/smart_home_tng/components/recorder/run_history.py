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

import bisect
import datetime
from dataclasses import dataclass

import sqlalchemy.orm as sql_orm

from ... import core
from . import model


@dataclass(frozen=True)
class _RecorderRunsHistory:
    """Bisectable history of RecorderRuns."""

    run_timestamps: list[int]
    runs_by_timestamp: dict[int, model.RecorderRuns]


def _find_recorder_run_for_start_time(
    run_history: _RecorderRunsHistory, start: datetime
) -> model.RecorderRuns:
    """Find the recorder run for a start time in _RecorderRunsHistory."""
    run_timestamps = run_history.run_timestamps
    runs_by_timestamp = run_history.runs_by_timestamp

    # bisect_left tells us were we would insert
    # a value in the list of runs after the start timestamp.
    #
    # The run before that (idx-1) is when the run started
    #
    # If idx is 0, history never ran before the start timestamp
    #
    if idx := bisect.bisect_left(run_timestamps, start.timestamp()):
        return runs_by_timestamp[run_timestamps[idx - 1]]
    return None


class RunHistory:
    """Track recorder run history."""

    def __init__(self) -> None:
        """Track recorder run history."""
        self._recording_start = core.helpers.utcnow()
        self._current_run_info: model.RecorderRuns = None
        self._run_history = _RecorderRunsHistory([], {})

    @property
    def recording_start(self) -> datetime.datetime:
        """Return the time the recorder started recording states."""
        return self._recording_start

    @property
    def first(self) -> model.RecorderRuns:
        """Get the first run."""
        if runs_by_timestamp := self._run_history.runs_by_timestamp:
            return next(iter(runs_by_timestamp.values()))
        return self.current

    @property
    def current(self) -> model.RecorderRuns:
        """Get the current run."""
        assert self._current_run_info is not None
        return self._current_run_info

    def get(self, start: datetime.datetime) -> model.RecorderRuns:
        """Return the recorder run that started before or at start.

        If the first run started after the start, return None
        """
        if start >= self.recording_start:
            return self.current
        return _find_recorder_run_for_start_time(self._run_history, start)

    def start(self, session: sql_orm.Session) -> None:
        """Start a new run.

        Must run in the recorder thread.
        """
        self._current_run_info = model.RecorderRuns(
            start=self.recording_start, created=core.helpers.utcnow()
        )
        session.add(self._current_run_info)
        session.flush()
        session.expunge(self._current_run_info)
        self.load_from_db(session)

    def reset(self) -> None:
        """Reset the run when the database is changed or fails.

        Must run in the recorder thread.
        """
        self._recording_start = core.helpers.utcnow()
        self._current_run_info = None

    def end(self, session: sql_orm.Session) -> None:
        """End the current run.

        Must run in the recorder thread.
        """
        assert self._current_run_info is not None
        self._current_run_info.end = core.helpers.utcnow()
        session.add(self._current_run_info)

    def load_from_db(self, session: sql_orm.Session) -> None:
        """Update the run cache.

        Must run in the recorder thread.
        """
        run_timestamps: list[int] = []
        runs_by_timestamp: dict[int, model.RecorderRuns] = {}

        for run in (
            session.query(model.RecorderRuns)
            .order_by(model.RecorderRuns.start.asc())
            .all()
        ):
            session.expunge(run)
            if run_dt := model.process_timestamp(run.start):
                timestamp = run_dt.timestamp()
                run_timestamps.append(timestamp)
                runs_by_timestamp[timestamp] = run

        #
        # self._run_history is accessed in get()
        # which is allowed to be called from any thread
        #
        # We use a dataclass to ensure that when we update
        # run_timestamps and runs_by_timestamp
        # are never out of sync with each other.
        #
        self._run_history = _RecorderRunsHistory(run_timestamps, runs_by_timestamp)

    def clear(self) -> None:
        """Clear the current run after ending it.

        Must run in the recorder thread.
        """
        assert self._current_run_info is not None
        assert self._current_run_info.end is not None
        self._current_run_info = None
