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

import collections.abc
import contextlib
import datetime
import logging
import os
import sqlite3
import time
import typing

import awesomeversion as asv
import ciso8601
import sqlalchemy as sql
import sqlalchemy.exc as sql_exc
import sqlalchemy.orm as sql_orm

from ... import core
from . import model
from .const import Const
from .model import _TABLE_RECORDER_RUNS, _TABLE_SCHEMA_CHANGES, _TABLES_TO_CHECK

if not typing.TYPE_CHECKING:

    class Recorder:
        ...

    class RecorderComponent:
        ...


if typing.TYPE_CHECKING:
    from .recorder import Recorder
    from .recorder_component import RecorderComponent

_LOGGER: typing.Final = logging.getLogger(__name__)

_RETRIES: typing.Final = 3
_QUERY_RETRY_WAIT: typing.Final = 0.1
_SQLITE3_POSTFIXES: typing.Final = ["", "-wal", "-shm"]
_DEFAULT_YIELD_STATES_ROWS: typing.Final = 32768

_MIN_VERSION_MARIA_DB: typing.Final = asv.AwesomeVersion(
    "10.3.0", asv.AwesomeVersionStrategy.SIMPLEVER
)
_MIN_VERSION_MYSQL: typing.Final = asv.AwesomeVersion(
    "8.0.0", asv.AwesomeVersionStrategy.SIMPLEVER
)
_MIN_VERSION_PGSQL: typing.Final = asv.AwesomeVersion(
    "12.0", asv.AwesomeVersionStrategy.SIMPLEVER
)
_MIN_VERSION_SQLITE: typing.Final = asv.AwesomeVersion(
    "3.31.0", asv.AwesomeVersionStrategy.SIMPLEVER
)

# This is the maximum time after the recorder ends the session
# before we no longer consider startup to be a "restart" and we
# should do a check on the sqlite3 database.
_MAX_RESTART_TIME: typing.Final = datetime.timedelta(minutes=10)

# Retry when one of the following MySQL errors occurred:
_RETRYABLE_MYSQL_ERRORS: typing.Final = (1205, 1206, 1213)
# 1205: Lock wait timeout exceeded; try restarting transaction
# 1206: The total number of locks exceeds the lock table size
# 1213: Deadlock found when trying to get lock; try restarting transaction

_FIRST_POSSIBLE_SUNDAY: typing.Final = 8
_SUNDAY_WEEKDAY: typing.Final = 6
_DAYS_IN_WEEK: typing.Final = 7


@contextlib.contextmanager
def session_scope(
    *,
    rc: RecorderComponent = None,
    session: sql_orm.Session = None,
    exception_filter: collections.abc.Callable[[Exception], bool] = None,
) -> collections.abc.Generator[sql_orm.Session, None, None]:
    """Provide a transactional scope around a series of operations."""
    if session is None and rc is not None:
        session = rc.recorder.get_session()

    if session is None:
        raise RuntimeError("Session required")

    need_rollback = False
    try:
        yield session
        if session.get_transaction():
            need_rollback = True
            session.commit()
    except Exception as err:  # pylint: disable=broad-except
        _LOGGER.error(f"Error executing query: {err}")
        if need_rollback:
            session.rollback()
        if not exception_filter or not exception_filter(err):
            raise
    finally:
        session.close()


def commit(session: sql_orm.Session, work: typing.Any) -> bool:
    """Commit & retry work: Either a model or in a function."""
    for _ in range(0, _RETRIES):
        try:
            if callable(work):
                work(session)
            else:
                session.add(work)
            session.commit()
            return True
        except sql_exc.OperationalError as err:
            _LOGGER.error(f"Error executing query: {err}")
            session.rollback()
            time.sleep(_QUERY_RETRY_WAIT)
    return False


def execute(
    qry: sql_orm.Query, to_native: bool = False, validate_entity_ids: bool = True
) -> list[sql.engine.Row]:
    """Query the database and convert the objects to HA native form.

    This method also retries a few times in the case of stale connections.
    """
    for tryno in range(0, _RETRIES):
        try:
            timer_start = time.perf_counter()
            if to_native:
                result = [
                    row
                    for row in (
                        row.to_native(validate_entity_id=validate_entity_ids)
                        for row in qry
                    )
                    if row is not None
                ]
            else:
                result = qry.all()

            if _LOGGER.isEnabledFor(logging.DEBUG):
                elapsed = time.perf_counter() - timer_start
                if to_native:
                    _LOGGER.debug(
                        f"converting {len(result):d} rows to native objects took "
                        + f"{elapsed:f}s",
                    )
                else:
                    _LOGGER.debug(
                        f"querying {len(result):d} rows took {elapsed:f}s",
                    )

            return result
        except sql_exc.SQLAlchemyError as err:
            _LOGGER.error(f"Error executing query: {err}")

            if tryno == _RETRIES - 1:
                raise
            time.sleep(_QUERY_RETRY_WAIT)

    assert False  # unreachable # pragma: no cover


def execute_stmt_lambda_element(
    session: sql_orm.Session,
    stmt: sql.sql.StatementLambdaElement,
    start_time: datetime.datetime = None,
    end_time: datetime.datetime = None,
    yield_per: int = _DEFAULT_YIELD_STATES_ROWS,
) -> collections.abc.Iterable[sql.engine.Row]:
    """Execute a StatementLambdaElement.

    If the time window passed is greater than one day
    the execution method will switch to yield_per to
    reduce memory pressure.

    It is not recommended to pass a time window
    when selecting non-ranged rows (ie selecting
    specific entities) since they are usually faster
    with .all().
    """
    executed = session.execute(stmt)
    use_all = (
        not start_time or ((end_time or core.helpers.utcnow()) - start_time).days <= 1
    )
    for tryno in range(0, _RETRIES):
        try:
            return executed.all() if use_all else executed.yield_per(yield_per)
        except sql_exc.SQLAlchemyError as err:
            _LOGGER.error(f"Error executing query: {err}")
            if tryno == _RETRIES - 1:
                raise
            time.sleep(_QUERY_RETRY_WAIT)

    assert False  # unreachable # pragma: no cover


def validate_or_move_away_sqlite_database(dburl: str) -> bool:
    """Ensure that the database is valid or move it away."""
    dbpath = dburl_to_path(dburl)

    if not os.path.exists(dbpath):
        # Database does not exist yet, this is OK
        return True

    if not validate_sqlite_database(dbpath):
        move_away_broken_database(dbpath)
        return False

    return True


def dburl_to_path(dburl: str) -> str:
    """Convert the db url into a filesystem path."""
    return dburl[len(Const.SQLITE_URL_PREFIX) :]


def last_run_was_recently_clean(cursor: sql.engine.cursor.CursorFetchStrategy) -> bool:
    """Verify the last recorder run was recently clean."""

    cursor.execute("SELECT end FROM recorder_runs ORDER BY start DESC LIMIT 1;")
    end_time = cursor.fetchone()

    if not end_time or not end_time[0]:
        return False

    last_run_end_time = model.process_timestamp(
        core.helpers.parse_datetime(end_time[0])
    )
    assert last_run_end_time is not None
    now = core.helpers.utcnow()

    _LOGGER.debug(f"The last run ended at: {last_run_end_time} (now: {now})")

    if last_run_end_time + _MAX_RESTART_TIME < now:
        return False

    return True


def basic_sanity_check(cursor: sql.engine.cursor.CursorFetchStrategy) -> bool:
    """Check tables to make sure select does not fail."""

    for table in _TABLES_TO_CHECK:
        if table in (_TABLE_RECORDER_RUNS, _TABLE_SCHEMA_CHANGES):
            cursor.execute(f"SELECT * FROM {table};")  # nosec
        else:
            cursor.execute(f"SELECT * FROM {table} LIMIT 1;")  # nosec

    return True


def validate_sqlite_database(dbpath: str) -> bool:
    """Run a quick check on an sqlite database to see if it is corrupt."""

    try:
        conn = sqlite3.connect(dbpath)
        run_checks_on_open_db(dbpath, conn.cursor())
        conn.close()
    except sqlite3.DatabaseError:
        _LOGGER.exception(f"The database at {dbpath} is corrupt or malformed")
        return False

    return True


def run_checks_on_open_db(
    dbpath: str, cursor: sql.engine.cursor.CursorFetchStrategy
) -> None:
    """Run checks that will generate a sqlite3 exception if there is corruption."""
    sanity_check_passed = basic_sanity_check(cursor)
    last_run_was_clean = last_run_was_recently_clean(cursor)

    if sanity_check_passed and last_run_was_clean:
        _LOGGER.debug(
            "The system was restarted cleanly and passed the basic sanity check"
        )
        return

    if not sanity_check_passed:
        _LOGGER.warning(
            f"The database sanity check failed to validate the sqlite3 database at {dbpath}",
        )

    if not last_run_was_clean:
        _LOGGER.warning(
            f"The system could not validate that the sqlite3 database at {dbpath} "
            + "was shutdown cleanly",
        )


def move_away_broken_database(dbfile: str) -> None:
    """Move away a broken sqlite3 database."""

    isotime = core.helpers.utcnow().isoformat()
    corrupt_postfix = f".corrupt.{isotime}"

    _LOGGER.error(
        f"The system will rename the corrupt database file {dbfile} to "
        + f"{dbfile}{corrupt_postfix} in order to allow startup to proceed",
    )

    for postfix in _SQLITE3_POSTFIXES:
        path = f"{dbfile}{postfix}"
        if not os.path.exists(path):
            continue
        os.rename(path, f"{path}{corrupt_postfix}")


def execute_on_connection(dbapi_connection: typing.Any, statement: str) -> None:
    """Execute a single statement with a dbapi connection."""
    cursor = dbapi_connection.cursor()
    cursor.execute(statement)
    cursor.close()


def query_on_connection(dbapi_connection: typing.Any, statement: str) -> typing.Any:
    """Execute a single statement with a dbapi connection and return the result."""
    cursor = dbapi_connection.cursor()
    cursor.execute(statement)
    result = cursor.fetchall()
    cursor.close()
    return result


def _fail_unsupported_dialect(dialect_name: str) -> None:
    """Warn about unsupported database version."""
    supported = "MariaDB ≥ 10.3, MySQL ≥ 8.0, PostgreSQL ≥ 12, SQLite ≥ 3.31.0"
    _LOGGER.error(
        f"Database {dialect_name} is not supported; Smart Home - The Next Generation "
        + f"supports {supported}. "
        + "Starting with Home Assistant 2022.6 this prevents the recorder from "
        + "starting. Please migrate your database to a supported software",
    )
    raise model.UnsupportedDialect


def _fail_unsupported_version(
    server_version: str, dialect_name: str, minimum_version: str
) -> None:
    """Warn about unsupported database version."""
    _LOGGER.error(
        f"Version {server_version} of {dialect_name} is not supported; "
        + f"minimum supported version is {minimum_version}. "
        + "Starting with Smart Home - The Next Generation 2022.8 this "
        + "prevents the recorder from "
        + "starting. Please upgrade your database software",
    )
    raise model.UnsupportedDialect


def _extract_version_from_server_response(
    server_response: str,
) -> asv.AwesomeVersion:
    """Attempt to extract version from server response."""
    try:
        return asv.AwesomeVersion(
            server_response,
            ensure_strategy=asv.AwesomeVersionStrategy.SIMPLEVER,
            find_first_match=True,
        )
    except asv.AwesomeVersionException:
        return None


def _datetime_or_none(value: str) -> datetime.datetime:
    """Fast version of mysqldb DateTime_or_None.

    https://github.com/PyMySQL/mysqlclient/blob/v2.1.0/MySQLdb/times.py#L66
    """
    try:
        return ciso8601.parse_datetime(value)
    except ValueError:
        return None


def build_mysqldb_conv() -> dict:
    """Build a MySQLDB conv dict that uses cisco8601 to parse datetimes."""
    # Late imports since we only call this if they are using mysqldb
    # pylint: disable=import-outside-toplevel,import-error
    from MySQLdb.constants import FIELD_TYPE

    # pylint: disable=import-outside-toplevel,import-error
    from MySQLdb.converters import conversions

    return {**conversions, FIELD_TYPE.DATETIME: _datetime_or_none}


def setup_connection_for_dialect(
    instance: Recorder,
    dialect_name: str,
    dbapi_connection: typing.Any,
    first_connection: bool,
) -> asv.AwesomeVersion:
    """Execute statements needed for dialect connection."""
    version: asv.AwesomeVersion = None
    if dialect_name == Const.SupportedDialect.SQLITE:
        if first_connection:
            old_isolation = dbapi_connection.isolation_level
            dbapi_connection.isolation_level = None
            execute_on_connection(dbapi_connection, "PRAGMA journal_mode=WAL")
            dbapi_connection.isolation_level = old_isolation
            # WAL mode only needs to be setup once
            # instead of every time we open the sqlite connection
            # as its persistent and isn't free to call every time.
            result = query_on_connection(dbapi_connection, "SELECT sqlite_version()")
            version_string = result[0][0]
            version = _extract_version_from_server_response(version_string)

            if not version or version < _MIN_VERSION_SQLITE:
                _fail_unsupported_version(
                    version or version_string, "SQLite", _MIN_VERSION_SQLITE
                )

        # The upper bound on the cache size is approximately 16MiB of memory
        execute_on_connection(dbapi_connection, "PRAGMA cache_size = -16384")

        #
        # Enable FULL synchronous if they have a commit interval of 0
        # or NORMAL if they do not.
        #
        # https://sqlite.org/pragma.html#pragma_synchronous
        # The synchronous=NORMAL setting is a good choice for most applications running in WAL mode.
        #
        synchronous = "NORMAL" if instance.commit_interval else "FULL"
        execute_on_connection(dbapi_connection, f"PRAGMA synchronous={synchronous}")

        # enable support for foreign keys
        execute_on_connection(dbapi_connection, "PRAGMA foreign_keys=ON")

    elif dialect_name == Const.SupportedDialect.MYSQL:
        execute_on_connection(dbapi_connection, "SET session wait_timeout=28800")
        if first_connection:
            result = query_on_connection(dbapi_connection, "SELECT VERSION()")
            version_string = result[0][0]
            version = _extract_version_from_server_response(version_string)
            is_maria_db = "mariadb" in version_string.lower()

            if is_maria_db:
                if not version or version < _MIN_VERSION_MARIA_DB:
                    _fail_unsupported_version(
                        version or version_string, "MariaDB", _MIN_VERSION_MARIA_DB
                    )
            else:
                if not version or version < _MIN_VERSION_MYSQL:
                    _fail_unsupported_version(
                        version or version_string, "MySQL", _MIN_VERSION_MYSQL
                    )

    elif dialect_name == Const.SupportedDialect.POSTGRESQL:
        if first_connection:
            # server_version_num was added in 2006
            result = query_on_connection(dbapi_connection, "SHOW server_version")
            version_string = result[0][0]
            version = _extract_version_from_server_response(version_string)
            if not version or version < _MIN_VERSION_PGSQL:
                _fail_unsupported_version(
                    version or version_string, "PostgreSQL", _MIN_VERSION_PGSQL
                )

    else:
        _fail_unsupported_dialect(dialect_name)

    return version


def end_incomplete_runs(
    session: sql_orm.Session, start_time: datetime.datetime
) -> None:
    """End any incomplete recorder runs."""
    for run in session.query(model.RecorderRuns).filter_by(end=None):
        run.closed_incorrect = True
        run.end = start_time
        _LOGGER.warning(f"Ended unfinished session (id={run.run_id} from {run.start})")
        session.add(run)


def periodic_db_cleanups(instance: Recorder) -> None:
    """Run any database cleanups that need to happen periodically.

    These cleanups will happen nightly or after any purge.
    """
    assert instance.engine is not None
    if instance.engine.dialect.name == Const.SupportedDialect.SQLITE:
        # Execute sqlite to create a wal checkpoint and free up disk space
        _LOGGER.debug("WAL checkpoint")
        with instance.engine.connect() as connection:
            connection.execute(sql.text("PRAGMA wal_checkpoint(TRUNCATE);"))


@contextlib.contextmanager
def write_lock_db_sqlite(
    instance: Recorder,
) -> collections.abc.Generator[None, None, None]:
    """Lock database for writes."""
    assert instance.engine is not None
    with instance.engine.connect() as connection:
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


def async_migration_in_progress(rec_comp: RecorderComponent) -> bool:
    """Determine is a migration is in progress.

    This is a thin wrapper that allows us to change
    out the implementation later.
    """
    if rec_comp is None or rec_comp.recorder is None:
        return False
    return rec_comp.recorder.migration_in_progress


def second_sunday(year: int, month: int) -> datetime.date:
    """Return the datetime.date for the second sunday of a month."""
    second = datetime.date(year, month, _FIRST_POSSIBLE_SUNDAY)
    day_of_week = second.weekday()
    if day_of_week == _SUNDAY_WEEKDAY:
        return second
    return second.replace(
        day=(_FIRST_POSSIBLE_SUNDAY + (_SUNDAY_WEEKDAY - day_of_week) % _DAYS_IN_WEEK)
    )


def is_second_sunday(date_time: datetime.datetime) -> bool:
    """Check if a time is the second sunday of the month."""
    return bool(second_sunday(date_time.year, date_time.month).day == date_time.day)
