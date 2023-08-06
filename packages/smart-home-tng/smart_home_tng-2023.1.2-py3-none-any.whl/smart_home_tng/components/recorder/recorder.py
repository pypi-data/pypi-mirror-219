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

import asyncio
import collections.abc
import contextlib
import datetime
import logging
import queue
import sqlite3
import threading
import time
import typing

import awesomeversion as asv
import lru
import sqlalchemy as sql
from sqlalchemy import engine as sql_engine
from sqlalchemy import event as sql_event
from sqlalchemy import exc as sql_exc
from sqlalchemy import orm as sql_orm

from ... import core
from . import executor, migration, model, pool, queries, statistics, task, util
from .const import Const
from .run_history import RunHistory

_statistic: typing.TypeAlias = core.Statistic

_T = typing.TypeVar("_T")
_LOGGER: typing.Final = logging.getLogger(__name__)

# Controls how often we clean up
# States and Events objects
_EXPIRE_AFTER_COMMITS: typing.Final = 120

# The number of attribute ids to cache in memory
#
# Based on:
# - The number of overlapping attributes
# - How frequently states with overlapping attributes will change
# - How much memory our low end hardware has
_STATE_ATTRIBUTES_ID_CACHE_SIZE: typing.Final = 2048
_EVENT_DATA_ID_CACHE_SIZE: typing.Final = 2048

_SHUTDOWN_TASK: typing.Final = object()

_COMMIT_TASK: typing.Final = task.CommitTask()
_KEEP_ALIVE_TASK: typing.Final = task.KeepAliveTask()
_WAIT_TASK: typing.Final = task.WaitTask()

_DB_LOCK_TIMEOUT: typing.Final = 30
_DB_LOCK_QUEUE_CHECK_TIMEOUT: typing.Final = 1


_INVALIDATED_ERR: typing.Final = "Database connection invalidated"
_CONNECTIVITY_ERR: typing.Final = "Error in database connectivity during commit"
_UNDEFINED: typing.Final = object()

# Pool size must accommodate Recorder thread + All db executors
_MAX_DB_EXECUTOR_WORKERS = Const.POOL_SIZE - 1


if not typing.TYPE_CHECKING:

    class RecorderComponent:
        ...


if typing.TYPE_CHECKING:
    from .recorder_component import RecorderComponent


# pylint: disable=unused-variable
class Recorder(threading.Thread):
    """A threaded recorder class."""

    def __init__(
        self,
        owner: RecorderComponent,
        auto_purge: bool,
        auto_repack: bool,
        keep_days: int,
        commit_interval: int,
        uri: str,
        db_max_retries: int,
        db_retry_wait: int,
        entity_filter: collections.abc.Callable[[str], bool],
        exclude_t: list[str],
        exclude_attributes_by_domain: dict[str, set[str]],
    ) -> None:
        """Initialize the recorder."""
        super().__init__(name="Recorder")
        self._owner = owner
        self._stop_requested: bool = False
        self._auto_purge = auto_purge
        self._auto_repack = auto_repack
        self._keep_days = keep_days
        self._shc_started: asyncio.Future[object] = asyncio.Future()
        self._commit_interval = commit_interval
        self._queue: queue.SimpleQueue[task.RecorderTask] = queue.SimpleQueue()
        self._db_url = uri
        self._db_max_retries = db_max_retries
        self._db_retry_wait = db_retry_wait
        self._engine_version: asv.AwesomeVersion = None
        self._async_db_ready: asyncio.Future[bool] = asyncio.Future()
        self._async_recorder_ready_event = asyncio.Event()
        self._queue_watch = threading.Event()
        self._engine: sql_engine.Engine = None
        self._run_history = RunHistory()

        self._entity_filter = entity_filter
        self._exclude_t = exclude_t

        self._schema_version = 0
        self._commits_without_expire = 0
        self._old_states: dict[str, model.States] = {}
        self._state_attributes_ids: lru.LRU = lru.LRU(_STATE_ATTRIBUTES_ID_CACHE_SIZE)
        self._event_data_ids: lru.LRU = lru.LRU(_EVENT_DATA_ID_CACHE_SIZE)
        self._pending_state_attributes: dict[str, model.StateAttributes] = {}
        self._pending_event_data: dict[str, model.EventData] = {}
        self._pending_expunge: list[model.States] = []
        self._event_session: core.SqlSession = None
        self._get_session: collections.abc.Callable[[], core.SqlSession] = None
        self._completed_first_database_setup: bool = None
        self._async_migration_event = asyncio.Event()
        self._migration_in_progress = False
        self._database_lock_task: task.DatabaseLockTask = None
        self._db_executor: executor.DBInterruptibleThreadPoolExecutor = None
        self._exclude_attributes_by_domain = exclude_attributes_by_domain

        self._event_listener: core.CallbackType = None
        self._queue_watcher: core.CallbackType = None
        self._keep_alive_listener: core.CallbackType = None
        self._commit_listener: core.CallbackType = None
        self._periodic_listener: core.CallbackType = None
        self._nightly_listener: core.CallbackType = None
        self._enabled = True

    @property
    def enabled(self) -> bool:
        return self._enabled

    @property
    def owner(self) -> RecorderComponent:
        return self._owner

    @property
    def controller(self):
        return self._owner.controller

    @property
    def migration_in_progress(self) -> bool:
        return self._migration_in_progress

    @property
    def async_migration_event(self) -> asyncio.Event:
        return self._async_migration_event

    @property
    def event_session(self) -> core.SqlSession:
        return self._event_session

    @property
    def schema_version(self) -> int:
        return self._schema_version

    @property
    def exclude_t(self) -> collections.abc.Iterable[str]:
        return self._exclude_t

    @property
    def entity_filter(self) -> collections.abc.Callable[[str], bool]:
        return self._entity_filter

    @property
    def run_history(self) -> RunHistory:
        return self._run_history

    @property
    def engine(self) -> sql_engine.Engine:
        return self._engine

    @property
    def async_recorder_ready(self) -> asyncio.Event:
        return self._async_recorder_ready_event

    @property
    def async_db_ready(self) -> asyncio.Future[bool]:
        return self._async_db_ready

    @property
    def commit_interval(self) -> int:
        return self._commit_interval

    @property
    def db_retry_wait(self) -> int:
        return self._db_retry_wait

    @property
    def db_max_retries(self) -> int:
        return self._db_max_retries

    @property
    def db_url(self) -> str:
        return self._db_url

    @property
    def keep_days(self) -> int:
        return self._keep_days

    @property
    def engine_version(self) -> asv.AwesomeVersion:
        return self._engine_version

    @property
    def auto_repack(self) -> bool:
        return self._auto_repack

    @property
    def auto_purge(self) -> bool:
        return self._auto_purge

    @property
    def stop_requested(self) -> bool:
        return self._stop_requested

    @property
    def backlog(self) -> int:
        """Return the number of items in the recorder backlog."""
        return self._queue.qsize()

    @property
    def dialect_name(self) -> Const.SupportedDialect:
        """Return the dialect the recorder uses."""
        with contextlib.suppress(ValueError):
            return (
                Const.SupportedDialect(self.engine.dialect.name)
                if self.engine
                else None
            )
        return None

    @property
    def _using_file_sqlite(self) -> bool:
        """Short version to check if we are using sqlite3 as a file."""
        return self.db_url != Const.SQLITE_URL_PREFIX and self.db_url.startswith(
            Const.SQLITE_URL_PREFIX
        )

    @property
    def recording(self) -> bool:
        """Return if the recorder is recording."""
        return self._event_listener is not None

    def get_session(self) -> core.SqlSession:
        """Get a new sqlalchemy session."""
        if self._get_session is None:
            raise RuntimeError("The database connection has not been established")
        return self._get_session()

    def queue_task(self, tsk: task.RecorderTask) -> None:
        """Add a task to the recorder queue."""
        self._queue.put(tsk)

    def set_enable(self, enable: bool) -> None:
        """Enable or disable recording events and states."""
        self._enabled = enable

    @core.callback
    def async_start_executor(self) -> None:
        """Start the executor."""
        self._db_executor = executor.DBInterruptibleThreadPoolExecutor(
            thread_name_prefix=Const.DB_WORKER_PREFIX,
            max_workers=_MAX_DB_EXECUTOR_WORKERS,
            shutdown_hook=self._shutdown_pool,
        )

    def _shutdown_pool(self) -> None:
        """Close the dbpool connections in the current thread."""
        if self.engine and hasattr(self.engine.pool, "shutdown"):
            self.engine.pool.shutdown()

    @core.callback
    def async_initialize(self) -> None:
        """Initialize the recorder."""
        owner = self.owner
        self._event_listener = owner.bus.async_listen(
            core.Const.MATCH_ALL,
            self.event_listener,
            run_immediately=True,
        )
        self._queue_watcher = self.owner.tracker.async_track_time_interval(
            self._async_check_queue, datetime.timedelta(minutes=10)
        )

    @core.callback
    def _async_keep_alive(self, _now: datetime) -> None:
        """Queue a keep alive."""
        if self._event_listener:
            self.queue_task(_KEEP_ALIVE_TASK)

    @core.callback
    def _async_commit(self, _now: datetime) -> None:
        """Queue a commit."""
        if (
            self._event_listener
            and not self._database_lock_task
            and self._event_session_has_pending_writes()
        ):
            self.queue_task(_COMMIT_TASK)

    @core.callback
    def async_add_executor_job(
        self, target: collections.abc.Callable[..., _T], *args: typing.Any
    ) -> asyncio.Future[_T]:
        """Add an executor job from within the event loop."""
        return self.owner.controller.run_in_executor(self._db_executor, target, *args)

    def _stop_executor(self) -> None:
        """Stop the executor."""
        assert self._db_executor is not None
        self._db_executor.shutdown()
        self._db_executor = None

    @core.callback
    def _async_check_queue(self, *_: typing.Any) -> None:
        """Periodic check of the queue size to ensure we do not exaust memory.

        The queue grows during migraton or if something really goes wrong.
        """
        size = self.backlog
        _LOGGER.debug(f"Recorder queue size is: {size}")
        if size <= Const.MAX_QUEUE_BACKLOG:
            return
        _LOGGER.error(
            "The recorder backlog queue reached the maximum size of "
            + f"{Const.MAX_QUEUE_BACKLOG} events; "
            + "usually, the system is CPU bound, I/O bound, or the database "
            + "is corrupt due to a disk problem; The recorder will stop "
            + "recording events to avoid running out of memory",
        )
        self._async_stop_queue_watcher_and_event_listener()

    @core.callback
    def _async_stop_queue_watcher_and_event_listener(self) -> None:
        """Stop watching the queue and listening for events."""
        if self._queue_watcher:
            self._queue_watcher()
            self._queue_watcher = None
        if self._event_listener:
            self._event_listener()
            self._event_listener = None

    @core.callback
    def _async_stop_listeners(self) -> None:
        """Stop listeners."""
        self._async_stop_queue_watcher_and_event_listener()
        if self._keep_alive_listener:
            self._keep_alive_listener()
            self._keep_alive_listener = None
        if self._commit_listener:
            self._commit_listener()
            self._commit_listener = None
        if self._nightly_listener:
            self._nightly_listener()
            self._nightly_listener = None
        if self._periodic_listener:
            self._periodic_listener()
            self._periodic_listener = None

    @core.callback
    def _async_event_filter(self, event: core.Event) -> bool:
        """Filter events."""
        if event.event_type in self.exclude_t:
            return False

        if (entity_id := event.data.get(core.Const.ATTR_ENTITY_ID)) is None:
            return True

        if isinstance(entity_id, str):
            return self.entity_filter(entity_id)

        if isinstance(entity_id, list):
            for eid in entity_id:
                if self.entity_filter(eid):
                    return True
            return False

        # Unknown what it is.
        return True

    def do_adhoc_statistics(self, **kwargs: typing.Any) -> None:
        """Trigger an adhoc statistics run."""
        if not (start := kwargs.get("start")):
            start = statistics.get_start_time()
        self.queue_task(task.StatisticsTask(start))

    def _empty_queue(self, _event: core.Event) -> None:
        """Empty the queue if its still present at final write."""

        # If the queue is full of events to be processed because
        # the database is so broken that every event results in a retry
        # we will never be able to get though the events to shutdown in time.
        #
        # We drain all the events in the queue and then insert
        # an empty one to ensure the next thing the recorder sees
        # is a request to shutdown.
        while True:
            try:
                self._queue.get_nowait()
            except queue.Empty:
                break
        self.queue_task(task.StopTask())

    async def _async_shutdown(self, _event: core.Event) -> None:
        """Shut down the Recorder."""
        if not self._shc_started.done():
            self._shc_started.set_result(_SHUTDOWN_TASK)
        self.queue_task(task.StopTask())
        self._async_stop_listeners()
        await self.owner.controller.async_add_executor_job(self.join)

    @core.callback
    def _async_shc_started(self, _event: core.Event) -> None:
        """Notify that hass has started."""
        self._shc_started.set_result(None)

    @core.callback
    def async_register(self) -> None:
        """Post connection initialize."""
        bus = self.owner.bus
        bus.async_listen_once(core.Const.EVENT_SHC_FINAL_WRITE, self._empty_queue)
        bus.async_listen_once(core.Const.EVENT_SHC_STOP, self._async_shutdown)
        if self.owner.smart_home_controller_state == core.CoreState.RUNNING:
            self._shc_started.set_result(None)
            return
        bus.async_listen_once(core.Const.EVENT_SHC_STARTED, self._async_shc_started)

    @core.callback
    def async_connection_failed(self) -> None:
        """Connect failed tasks."""
        self.async_db_ready.set_result(False)
        comp = core.SmartHomeControllerComponent.get_component(
            core.Const.PERSISTENT_NOTIFICATION_COMPONENT_NAME
        )
        if isinstance(comp, core.PersistentNotificationComponent):
            comp.async_create(
                "The recorder could not start, check [the logs](/config/logs)",
                "Recorder",
                f"{self.owner.domain}.check_config",
            )
        self._async_stop_listeners()

    @core.callback
    def async_connection_success(self) -> None:
        """Connect success tasks."""
        self.async_db_ready.set_result(True)
        self.async_start_executor()

    @core.callback
    def _async_recorder_ready(self) -> None:
        """Finish start and mark recorder ready."""
        self._async_setup_periodic_tasks()
        self.async_recorder_ready.set()

    @core.callback
    def async_nightly_tasks(self, now: datetime) -> None:
        """Trigger the purge."""
        if self.auto_purge:
            # Purge will schedule the periodic cleanups
            # after it completes to ensure it does not happen
            # until after the database is vacuumed
            repack = self.auto_repack and util.is_second_sunday(now)
            purge_before = core.helpers.utcnow() - datetime.timedelta(
                days=self.keep_days
            )
            self.queue_task(
                task.PurgeTask(purge_before, repack=repack, apply_filter=False)
            )
        else:
            self.queue_task(task.PeriodicCleanupTask())

    @core.callback
    def async_periodic_statistics(self, _now: datetime) -> None:
        """Trigger the statistics run.

        Short term statistics run every 5 minutes
        """
        start = statistics.get_start_time()
        self.queue_task(task.StatisticsTask(start))

    @core.callback
    def async_adjust_statistics(
        self,
        statistic_id: str,
        start_time: datetime.datetime,
        sum_adjustment: float,
        adjustment_unit: str,
    ) -> None:
        """Adjust statistics."""
        self.queue_task(
            task.AdjustStatisticsTask(
                statistic_id, start_time, sum_adjustment, adjustment_unit
            )
        )

    @core.callback
    def async_clear_statistics(self, statistic_ids: list[str]) -> None:
        """Clear statistics for a list of statistic_ids."""
        self.queue_task(task.ClearStatisticsTask(statistic_ids))

    @core.callback
    def async_update_statistics_metadata(
        self,
        statistic_id: str,
        *,
        new_statistic_id: str = _UNDEFINED,
        new_unit_of_measurement: str = _UNDEFINED,
    ) -> None:
        """Update statistics metadata for a statistic_id."""
        self.queue_task(
            task.UpdateStatisticsMetadataTask(
                statistic_id, new_statistic_id, new_unit_of_measurement
            )
        )

    @core.callback
    def async_external_statistics(
        self,
        metadata: _statistic.MetaData,
        stats: collections.abc.Iterable[_statistic.Data],
    ) -> None:
        """Schedule external statistics."""
        self.queue_task(task.ExternalStatisticsTask(metadata, stats))

    @core.callback
    def _async_setup_periodic_tasks(self) -> None:
        """Prepare periodic tasks."""
        if self.owner.is_controller_stopping or not self._get_session:
            # Home Assistant is shutting down
            return

        # If the db is using a socket connection, we need to keep alive
        # to prevent errors from unexpected disconnects
        if self.dialect_name != Const.SupportedDialect.SQLITE:
            self._keep_alive_listener = self.owner.tracker.async_track_time_interval(
                self._async_keep_alive, datetime.timedelta(seconds=Const.KEEPALIVE_TIME)
            )

        # If the commit interval is not 0, we need to commit periodically
        if self.commit_interval:
            self._commit_listener = self.owner.tracker.async_track_time_interval(
                self._async_commit, datetime.timedelta(seconds=self.commit_interval)
            )

        # Run nightly tasks at 4:12am
        self._nightly_listener = self.owner.tracker.async_track_time_change(
            self.async_nightly_tasks, hour=4, minute=12, second=0
        )

        # Compile short term statistics every 5 minutes
        self._periodic_listener = self.owner.tracker.async_track_utc_time_change(
            self.async_periodic_statistics, minute=range(0, 60, 5), second=10
        )

    async def _async_wait_for_started(self) -> object:
        """Wait for the hass started future."""
        return await self._shc_started

    def _wait_startup_or_shutdown(self) -> object:
        """Wait for startup or shutdown before starting."""
        try:
            return self.owner.controller.run_coroutine_threadsafe(
                self._async_wait_for_started()
            ).result()
        except asyncio.CancelledError as ex:
            _LOGGER.warning(
                f"Recorder startup was externally canceled before it could complete: {ex}",
            )
            return _SHUTDOWN_TASK

    def run(self) -> None:
        """Start processing events to save."""
        current_version = self._setup_recorder()

        if current_version is None:
            self.owner.controller.add_job(self.async_connection_failed)
            return

        self._schema_version = current_version

        schema_is_current = migration.schema_is_current(current_version)
        if schema_is_current:
            self._setup_run()
        else:
            self._migration_in_progress = True

        self.owner.controller.add_job(self.async_connection_success)

        # If shutdown happened before Home Assistant finished starting
        if self._wait_startup_or_shutdown() is _SHUTDOWN_TASK:
            self._migration_in_progress = False
            # Make sure we cleanly close the run if
            # we restart before startup finishes
            self._shutdown()
            return

        # We wait to start the migration until startup has finished
        # since it can be cpu intensive and we do not want it to compete
        # with startup which is also cpu intensive
        if not schema_is_current:
            if self._migrate_schema_and_setup_run(current_version):
                self.schema_version = Const.SCHEMA_VERSION
                if not self._event_listener:
                    # If the schema migration takes so long that the end
                    # queue watcher safety kicks in because MAX_QUEUE_BACKLOG
                    # is reached, we need to reinitialize the listener.
                    self.owner.controller.add_job(self.async_initialize)
            else:
                comp = core.SmartHomeControllerComponent.get_component(
                    core.Const.PERSISTENT_NOTIFICATION_COMPONENT_NAME
                )
                if isinstance(comp, core.PersistentNotificationComponent):
                    comp.create(
                        "The database migration failed, check [the logs](/config/logs).",
                        "Database Migration Failed",
                        "recorder_database_migration",
                    )
                self._shutdown()
                return

        _LOGGER.debug("Recorder processing the queue")
        self.owner.controller.add_job(self._async_recorder_ready)
        self._run_event_loop()

    def _run_event_loop(self) -> None:
        """Run the event loop for the recorder."""
        # Use a session for the event read loop
        # with a commit every time the event time
        # has changed. This reduces the disk io.
        self._stop_requested = False
        while not self.stop_requested:
            tsk = self._queue.get()
            _LOGGER.debug(f"Processing task: {tsk}")
            try:
                self._process_one_task_or_recover(tsk)
            except Exception as err:  # pylint: disable=broad-except
                _LOGGER.exception(f"Error while processing event {tsk}: {err}")

        self._shutdown()

    def _process_one_task_or_recover(self, tsk: task.RecorderTask) -> None:
        """Process an event, reconnect, or recover a malformed database."""
        try:
            # If its not an event, commit everything
            # that is pending before running the task
            if tsk.commit_before:
                self._commit_event_session_or_retry()
            return tsk.run(self)
        except sql_exc.DatabaseError as err:
            if self._handle_database_error(err):
                return None
            _LOGGER.exception(
                f"Unhandled database error while processing task {tsk}: {err}"
            )
        except sql_exc.SQLAlchemyError as err:
            _LOGGER.exception(f"SQLAlchemyError error processing task {tsk}: {err}")

        # Reset the session if an SQLAlchemyError (including DatabaseError)
        # happens to rollback and recover
        self._reopen_event_session()
        return None

    def _setup_recorder(self) -> int:
        """Create connect to the database and get the schema version."""
        tries = 1

        while tries <= self.db_max_retries:
            try:
                self._setup_connection()
                return migration.get_schema_version(self.get_session)
            except model.UnsupportedDialect:
                break
            except Exception as err:  # pylint: disable=broad-except
                _LOGGER.exception(
                    f"Error during connection setup: {err} (retrying in "
                    + f"{self.db_retry_wait} seconds)",
                )
            tries += 1
            time.sleep(self.db_retry_wait)

        return None

    @core.callback
    def _async_migration_started(self) -> None:
        """Set the migration started event."""
        self.async_migration_event.set()

    def _migrate_schema_and_setup_run(self, current_version: int) -> bool:
        """Migrate schema to the latest version."""
        comp = core.SmartHomeControllerComponent.get_component(
            core.Const.PERSISTENT_NOTIFICATION_COMPONENT_NAME
        )
        if isinstance(comp, core.PersistentNotificationComponent):
            comp.create(
                "System performance will temporarily degrade during "
                + "the database upgrade. Do not power down or restart the system "
                + "until the upgrade completes. Integrations that read the "
                + "database, such as logbook and history, may return inconsistent "
                + "results until the upgrade completes.",
                "Database upgrade in progress",
                "recorder_database_migration",
            )
        else:
            comp = None

        self.owner.controller.add_job(self._async_migration_started)

        try:
            migration.migrate_schema(
                self.owner, self.engine, self.get_session, current_version
            )
        except sql_exc.DatabaseError as err:
            if self._handle_database_error(err):
                return True
            _LOGGER.exception("Database error during schema migration")
            return False
        except Exception:  # pylint: disable=broad-except
            _LOGGER.exception("Error during schema migration")
            return False
        else:
            self._setup_run()
            return True
        finally:
            self.migration_in_progress = False
            if comp is not None:
                comp.dismiss("recorder_database_migration")

    def _lock_database(self, tsk: task.DatabaseLockTask) -> None:
        @core.callback
        def _async_set_database_locked(tsk: task.DatabaseLockTask) -> None:
            tsk.database_locked.set()

        with self.write_lock_db_sqlite():
            # Notify that lock is being held, wait until database can be used again.
            self.owner.controller.add_job(_async_set_database_locked, tsk)
            while not tsk.database_unlock.wait(timeout=_DB_LOCK_QUEUE_CHECK_TIMEOUT):
                if self.backlog > Const.MAX_QUEUE_BACKLOG * 0.9:
                    _LOGGER.warning(
                        "Database queue backlog reached more than 90% of maximum queue "
                        + "length while waiting for backup to finish; recorder will now "
                        + "resume writing to database. The backup can not be trusted and "
                        + "must be restarted"
                    )
                    tsk.queue_overflow = True
                    break
        _LOGGER.info(
            f"Database queue backlog reached {self.backlog} entries during backup",
        )

    @contextlib.contextmanager
    def write_lock_db_sqlite(self) -> collections.abc.Generator[None, None, None]:
        """Lock database for writes."""
        assert self.engine is not None
        with self.engine.connect() as connection:
            # Execute sqlite to create a wal checkpoint
            # This is optional but makes sure the backup is going to be minimal
            connection.execute(sql.text("PRAGMA wal_checkpoint(TRUNCATE)"))
            # Create write lock
            _LOGGER.debug("Lock database")
            connection.execute(sql.text("BEGIN IMMEDIATE;"))
            try:
                yield
            finally:
                _LOGGER.debug("Unlock database")
                connection.execute(sql.text("END;"))

    def _process_one_event(self, event: core.Event) -> None:
        if not self.enabled:
            return
        if event.event_type == core.Const.EVENT_STATE_CHANGED:
            self._process_state_changed_event_into_session(event)
        else:
            self._process_non_state_changed_event_into_session(event)
        # Commit if the commit interval is zero
        if not self.commit_interval:
            self._commit_event_session_or_retry()

    def _find_shared_attr_in_db(self, attr_hash: int, shared_attrs: str) -> int:
        """Find shared attributes in the db from the hash and shared_attrs."""
        #
        # Avoid the event session being flushed since it will
        # commit all the pending events and states to the database.
        #
        # The lookup has already have checked to see if the data is cached
        # or going to be written in the next commit so there is no
        # need to flush before checking the database.
        #
        assert self.event_session is not None
        with self.event_session.no_autoflush:
            if attributes_id := self.event_session.execute(
                queries.find_shared_attributes_id(attr_hash, shared_attrs)
            ).first():
                return typing.cast(int, attributes_id[0])
        return None

    def _find_shared_data_in_db(self, data_hash: int, shared_data: str) -> int:
        """Find shared event data in the db from the hash and shared_attrs."""
        #
        # Avoid the event session being flushed since it will
        # commit all the pending events and states to the database.
        #
        # The lookup has already have checked to see if the data is cached
        # or going to be written in the next commit so there is no
        # need to flush before checking the database.
        #
        assert self.event_session is not None
        with self.event_session.no_autoflush:
            if data_id := self.event_session.execute(
                queries.find_shared_data_id(data_hash, shared_data)
            ).first():
                return typing.cast(int, data_id[0])
        return None

    def _process_non_state_changed_event_into_session(self, event: core.Event) -> None:
        """Process any event into the session except state changed."""
        assert self.event_session is not None
        dbevent = model.Events.from_event(event)
        if not event.data:
            self.event_session.add(dbevent)
            return

        try:
            shared_data = model.EventData.shared_data_from_event(event)
        except (TypeError, ValueError) as ex:
            _LOGGER.warning(f"Event is not JSON serializable: {event}: {ex}")
            return

        # Matching attributes found in the pending commit
        if pending_event_data := self._pending_event_data.get(shared_data):
            dbevent.event_data_rel = pending_event_data
        # Matching attributes id found in the cache
        elif data_id := self._event_data_ids.get(shared_data):
            dbevent.data_id = data_id
        else:
            data_hash = model.EventData.hash_shared_data(shared_data)
            # Matching attributes found in the database
            if data_id := self._find_shared_data_in_db(data_hash, shared_data):
                self._event_data_ids[shared_data] = dbevent.data_id = data_id
            # No matching attributes found, save them in the DB
            else:
                dbevent_data = model.EventData(shared_data=shared_data, hash=data_hash)
                dbevent.event_data_rel = self._pending_event_data[
                    shared_data
                ] = dbevent_data
                self.event_session.add(dbevent_data)

        self.event_session.add(dbevent)

    def _process_state_changed_event_into_session(self, event: core.Event) -> None:
        """Process a state_changed event into the session."""
        assert self.event_session is not None
        try:
            dbstate = model.States.from_event(event)
            shared_attrs = model.StateAttributes.shared_attrs_from_event(
                event, self._exclude_attributes_by_domain
            )
        except (TypeError, ValueError) as ex:
            _LOGGER.warning(
                f"State is not JSON serializable: {event.data.get('new_state')}: "
                + f"{ex}",
            )
            return

        dbstate.attributes = None
        # Matching attributes found in the pending commit
        if pending_attributes := self._pending_state_attributes.get(shared_attrs):
            dbstate.state_attributes = pending_attributes
        # Matching attributes id found in the cache
        elif attributes_id := self._state_attributes_ids.get(shared_attrs):
            dbstate.attributes_id = attributes_id
        else:
            attr_hash = model.StateAttributes.hash_shared_attrs(shared_attrs)
            # Matching attributes found in the database
            if attributes_id := self._find_shared_attr_in_db(attr_hash, shared_attrs):
                dbstate.attributes_id = attributes_id
                self._state_attributes_ids[shared_attrs] = attributes_id
            # No matching attributes found, save them in the DB
            else:
                dbstate_attributes = model.StateAttributes(
                    shared_attrs=shared_attrs, hash=attr_hash
                )
                dbstate.state_attributes = dbstate_attributes
                self._pending_state_attributes[shared_attrs] = dbstate_attributes
                self.event_session.add(dbstate_attributes)

        if old_state := self._old_states.pop(dbstate.entity_id, None):
            if old_state.state_id:
                dbstate.old_state_id = old_state.state_id
            else:
                dbstate.old_state = old_state
        if event.data.get("new_state"):
            self._old_states[dbstate.entity_id] = dbstate
            self._pending_expunge.append(dbstate)
        else:
            dbstate.state = None
        self.event_session.add(dbstate)

    def _handle_database_error(self, err: Exception) -> bool:
        """Handle a database error that may result in moving away the corrupt db."""
        if isinstance(err.__cause__, sqlite3.DatabaseError):
            _LOGGER.exception(
                f"Unrecoverable sqlite3 database corruption detected: {err}"
            )
            self._handle_sqlite_corruption()
            return True
        return False

    def _event_session_has_pending_writes(self) -> bool:
        return bool(
            self.event_session and (self.event_session.new or self.event_session.dirty)
        )

    def _commit_event_session_or_retry(self) -> None:
        """Commit the event session if there is work to do."""
        if not self._event_session_has_pending_writes():
            return
        tries = 1
        while tries <= self.db_max_retries:
            try:
                self._commit_event_session()
                return
            except (sql_exc.InternalError, sql_exc.OperationalError) as err:
                msg = (
                    _INVALIDATED_ERR
                    if err.connection_invalidated
                    else _CONNECTIVITY_ERR
                )
                _LOGGER.error(
                    f"{msg}: Error executing query: {err}. (retrying in "
                    + f"{self.db_retry_wait} seconds)",
                )
                if tries == self.db_max_retries:
                    raise

                tries += 1
                time.sleep(self.db_retry_wait)

    def _commit_event_session(self) -> None:
        assert self.event_session is not None
        self._commits_without_expire += 1

        self.event_session.commit()
        if self._pending_expunge:
            for dbstate in self._pending_expunge:
                # Expunge the state so its not expired
                # until we use it later for dbstate.old_state
                if dbstate in self.event_session:
                    self.event_session.expunge(dbstate)
            self._pending_expunge = []

        # We just committed the state attributes to the database
        # and we now know the attributes_ids.  We can save
        # many selects for matching attributes by loading them
        # into the LRU cache now.
        for state_attr in self._pending_state_attributes.values():
            self._state_attributes_ids[
                state_attr.shared_attrs
            ] = state_attr.attributes_id
        self._pending_state_attributes = {}
        for event_data in self._pending_event_data.values():
            self._event_data_ids[event_data.shared_data] = event_data.data_id
        self._pending_event_data = {}

        # Expire is an expensive operation (frequently more expensive
        # than the flush and commit itself) so we only
        # do it after EXPIRE_AFTER_COMMITS commits
        if self._commits_without_expire >= _EXPIRE_AFTER_COMMITS:
            self._commits_without_expire = 0
            self.event_session.expire_all()

    def _handle_sqlite_corruption(self) -> None:
        """Handle the sqlite3 database being corrupt."""
        self._close_event_session()
        self._close_connection()
        util.move_away_broken_database(util.dburl_to_path(self.db_url))
        self.run_history.reset()
        self._setup_recorder()
        self._setup_run()

    def _close_event_session(self) -> None:
        """Close the event session."""
        self._old_states = {}
        self._state_attributes_ids = {}
        self._event_data_ids = {}
        self._pending_state_attributes = {}
        self._pending_event_data = {}

        if not self.event_session:
            return

        try:
            self.event_session.rollback()
            self.event_session.close()
        except sql_exc.SQLAlchemyError as err:
            _LOGGER.exception(
                f"Error while rolling back and closing the event session: {err}"
            )

    def _reopen_event_session(self) -> None:
        """Rollback the event session and reopen it after a failure."""
        self._close_event_session()
        self._open_event_session()

    def _open_event_session(self) -> None:
        """Open the event session."""
        self._event_session = self.get_session()
        self.event_session.expire_on_commit = False

    def _send_keep_alive(self) -> None:
        """Send a keep alive to keep the db connection open."""
        assert self.event_session is not None
        _LOGGER.debug("Sending keepalive")
        self.event_session.connection().scalar(sql.select([1]))

    @core.callback
    def event_listener(self, event: core.Event) -> None:
        """Listen for new events and put them in the process queue."""
        if self._async_event_filter(event):
            self.queue_task(task.EventTask(event))

    async def async_block_till_done(self) -> None:
        """Async version of block_till_done."""
        event = asyncio.Event()
        self.queue_task(task.SynchronizeTask(event))
        await event.wait()

    def block_till_done(self) -> None:
        """Block till all events processed.

        This is only called in tests.

        This only blocks until the queue is empty
        which does not mean the recorder is done.

        Call tests.common's wait_recording_done
        after calling this to ensure the data
        is in the database.
        """
        self._queue_watch.clear()
        self.queue_task(_WAIT_TASK)
        self._queue_watch.wait()

    async def lock_database(self) -> bool:
        """Lock database so it can be backed up safely."""
        if self.dialect_name != Const.SupportedDialect.SQLITE:
            _LOGGER.debug(
                "Not a SQLite database or not connected, locking not necessary"
            )
            return True

        if self._database_lock_task:
            _LOGGER.warning("Database already locked")
            return False

        database_locked = asyncio.Event()
        tsk = task.DatabaseLockTask(database_locked, threading.Event(), False)
        self.queue_task(tsk)
        try:
            await asyncio.wait_for(database_locked.wait(), timeout=_DB_LOCK_TIMEOUT)
        except asyncio.TimeoutError as err:
            tsk.database_unlock.set()
            raise TimeoutError(
                f"Could not lock database within {_DB_LOCK_TIMEOUT} seconds."
            ) from err
        self._database_lock_task = tsk
        return True

    @core.callback
    def unlock_database(self) -> bool:
        """Unlock database.

        Returns true if database lock has been held throughout the process.
        """
        if self.dialect_name != Const.SupportedDialect.SQLITE:
            _LOGGER.debug(
                "Not a SQLite database or not connected, unlocking not necessary"
            )
            return True

        if not self._database_lock_task:
            _LOGGER.warning("Database currently not locked")
            return False

        self._database_lock_task.database_unlock.set()
        success = not self._database_lock_task.queue_overflow

        self._database_lock_task = None

        return success

    def _setup_connection(self) -> None:
        """Ensure database is ready to fly."""
        kwargs: dict[str, typing.Any] = {}
        self._completed_first_database_setup = False

        def setup_recorder_connection(
            dbapi_connection: typing.Any, _connection_record: typing.Any
        ) -> None:
            """Dbapi specific connection settings."""
            assert self.engine is not None
            if version := util.setup_connection_for_dialect(
                self,
                self.engine.dialect.name,
                dbapi_connection,
                not self._completed_first_database_setup,
            ):
                self._engine_version = version
            self._completed_first_database_setup = True

        if self.db_url == Const.SQLITE_URL_PREFIX or ":memory:" in self.db_url:
            kwargs["connect_args"] = {"check_same_thread": False}
            kwargs["poolclass"] = pool.MutexPool
            pool.MutexPool.pool_lock = threading.RLock()
            kwargs["pool_reset_on_return"] = None
        elif self.db_url.startswith(Const.SQLITE_URL_PREFIX):
            kwargs["poolclass"] = pool.RecorderPool
        elif self.db_url.startswith(Const.MYSQLDB_URL_PREFIX):
            # If they have configured MySQLDB but don't have
            # the MySQLDB module installed this will throw
            # an ImportError which we suppress here since
            # sqlalchemy will give them a better error when
            # it tried to import it below.
            with contextlib.suppress(ImportError):
                kwargs["connect_args"] = {"conv": util.build_mysqldb_conv()}
        else:
            kwargs["echo"] = False

        if self._using_file_sqlite:
            util.validate_or_move_away_sqlite_database(self.db_url)

        self._engine = sql.create_engine(self.db_url, **kwargs)

        sql_event.listen(self.engine, "connect", setup_recorder_connection)

        model.Base.metadata.create_all(self.engine)
        self._get_session = sql_orm.scoped_session(
            sql_orm.sessionmaker(bind=self.engine)
        )
        _LOGGER.debug("Connected to recorder database")

    def _close_connection(self) -> None:
        """Close the connection."""
        assert self.engine is not None
        self.engine.dispose()
        self._engine = None
        self._get_session = None

    def _setup_run(self) -> None:
        """Log the start of the current run and schedule any needed jobs."""
        with util.session_scope(session=self.get_session()) as session:
            util.end_incomplete_runs(session, self.run_history.recording_start)
            self.run_history.start(session)
            self._schedule_compile_missing_statistics(session)

        self._open_event_session()

    def _schedule_compile_missing_statistics(self, session: core.SqlSession) -> None:
        """Add tasks for missing statistics runs."""
        now = core.helpers.utcnow()
        last_period_minutes = now.minute - now.minute % 5
        last_period = now.replace(minute=last_period_minutes, second=0, microsecond=0)
        start = now - datetime.timedelta(days=self.keep_days)
        start = start.replace(minute=0, second=0, microsecond=0)

        # Find the newest statistics run, if any
        if last_run := session.query(sql.func.max(model.StatisticsRuns.start)).scalar():
            start = max(
                start, model.process_timestamp(last_run) + datetime.timedelta(minutes=5)
            )

        # Add tasks
        while start < last_period:
            end = start + datetime.timedelta(minutes=5)
            _LOGGER.debug(f"Compiling missing statistics for {start}-{end}")
            self.queue_task(task.StatisticsTask(start))
            start = end

    def _end_session(self) -> None:
        """End the recorder session."""
        if self.event_session is None:
            return
        try:
            self.run_history.end(self.event_session)
            self._commit_event_session_or_retry()
            self.event_session.close()
        except Exception as err:  # pylint: disable=broad-except
            _LOGGER.exception(f"Error saving the event session during shutdown: {err}")

        self.run_history.clear()

    def _shutdown(self) -> None:
        """Save end time for current run."""
        self.owner.controller.add_job(self._async_stop_listeners)
        self._stop_executor()
        self._end_session()
        self._close_connection()

    def is_entity_recorded(self, entity_id: str) -> bool:
        """Check if an entity is being recorded.

        Async friendly.
        """
        return self.entity_filter(entity_id)
