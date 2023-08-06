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
import typing

import sqlalchemy as sql
import sqlalchemy.exc as sql_exc
import sqlalchemy.orm as sql_orm

from . import model, statistics, util
from .const import Const
from .model import _SCHEMA_VERSION, _TABLE_STATES


if not typing.TYPE_CHECKING:

    class RecorderComponent:
        ...


if typing.TYPE_CHECKING:
    from .recorder_component import RecorderComponent


_LOGGER: typing.Final = logging.getLogger(__name__)
SessionMaker: typing.TypeAlias = collections.abc.Callable[[], sql_orm.Session]


def raise_if_exception_missing_str(
    ex: Exception, match_substrs: collections.abc.Iterable[str]
) -> None:
    """Raise an exception if the exception and cause do not contain the match substrs."""
    lower_ex_strs = [str(ex).lower(), str(ex.__cause__).lower()]
    for str_sub in match_substrs:
        for exc_str in lower_ex_strs:
            if exc_str and str_sub in exc_str:
                return

    raise ex


def get_schema_version(session_maker: SessionMaker) -> int:
    """Get the schema version."""
    with util.session_scope(session=session_maker()) as session:
        res = (
            session.query(model.SchemaChanges)
            .order_by(model.SchemaChanges.change_id.desc())
            .first()
        )
        current_version = getattr(res, "schema_version", None)

        if current_version is None:
            current_version = _inspect_schema_version(session)
            _LOGGER.debug(
                f"No schema version found. Inspected version: {current_version}"
            )

        return typing.cast(int, current_version)


def schema_is_current(current_version: int) -> bool:
    """Check if the schema is current."""
    return current_version == _SCHEMA_VERSION


def migrate_schema(
    rec_comp: RecorderComponent,
    engine: sql.engine.Engine,
    session_maker: SessionMaker,
    current_version: int,
) -> None:
    """Check if the schema needs to be upgraded."""
    _LOGGER.warning(f"Database is about to upgrade. Schema version: {current_version}")
    for version in range(current_version, _SCHEMA_VERSION):
        new_version = version + 1
        _LOGGER.info(f"Upgrading recorder db schema to version {new_version}")
        _apply_update(rec_comp, engine, session_maker, new_version, current_version)
        with util.session_scope(session=session_maker()) as session:
            session.add(model.SchemaChanges(schema_version=new_version))

        _LOGGER.info(f"Upgrade to version {new_version} done")


def _create_index(
    session_maker: SessionMaker, table_name: str, index_name: str
) -> None:
    """Create an index for the specified table.

    The index name should match the name given for the index
    within the table definition described in the models
    """
    table = sql.Table(table_name, model.Base.metadata)
    _LOGGER.debug(f"Looking up index {index_name} for table {table_name}")
    # Look up the index object by name from the table is the models
    index_list = [idx for idx in table.indexes if idx.name == index_name]
    if not index_list:
        _LOGGER.debug(f"The index {index_name} no longer exists")
        return
    index = index_list[0]
    _LOGGER.debug(f"Creating {index_name} index")
    _LOGGER.warning(
        f"Adding index `{index_name}` to database. Note: this can take several "
        + "minutes on large databases and slow computers. Please "
        + "be patient!",
    )
    with util.session_scope(session=session_maker()) as session:
        try:
            connection = session.connection()
            index.create(connection)
        except (
            sql_exc.InternalError,
            sql_exc.OperationalError,
            sql_exc.ProgrammingError,
        ) as err:
            raise_if_exception_missing_str(err, ["already exists", "duplicate"])
            _LOGGER.warning(
                f"Index {index_name} already exists on {table_name}, continuing"
            )

    _LOGGER.debug(f"Finished creating {index_name}", index_name)


def _drop_index(session_maker: SessionMaker, table_name: str, index_name: str) -> None:
    """Drop an index from a specified table.

    There is no universal way to do something like `DROP INDEX IF EXISTS`
    so we will simply execute the DROP command and ignore any exceptions

    WARNING: Due to some engines (MySQL at least) being unable to use bind
    parameters in a DROP INDEX statement (at least via SQLAlchemy), the query
    string here is generated from the method parameters without sanitizing.
    DO NOT USE THIS FUNCTION IN ANY OPERATION THAT TAKES USER INPUT.
    """
    _LOGGER.debug(f"Dropping index {index_name} from table {table_name}")
    success = False

    # Engines like DB2/Oracle
    with util.session_scope(session=session_maker()) as session:
        try:
            connection = session.connection()
            connection.execute(sql.text(f"DROP INDEX {index_name}"))
        except sql_exc.SQLAlchemyError:
            pass
        else:
            success = True

    # Engines like SQLite, SQL Server
    if not success:
        with util.session_scope(session=session_maker()) as session:
            try:
                connection = session.connection()
                connection.execute(sql.text(f"DROP INDEX {table_name}.{index_name}"))
            except sql_exc.SQLAlchemyError:
                pass
            else:
                success = True

    if not success:
        # Engines like MySQL, MS Access
        with util.session_scope(session=session_maker()) as session:
            try:
                connection = session.connection()
                connection.execute(sql.text(f"DROP INDEX {index_name} ON {table_name}"))
            except sql_exc.SQLAlchemyError:
                pass
            else:
                success = True

    if success:
        _LOGGER.debug(f"Finished dropping index {index_name} from table {table_name}")
    else:
        if index_name == "ix_states_context_parent_id":
            # Was only there on nightly so we do not want
            # to generate log noise or issues about it.
            return

        _LOGGER.warning(
            f"Failed to drop index {index_name} from table {table_name}. Schema "
            + "Migration will continue; this is not a "
            + "critical operation",
        )


def _add_columns(
    session_maker: SessionMaker, table_name: str, columns_def: list[str]
) -> None:
    """Add columns to a table."""
    cols = ", ".join(column.split(" ")[0] for column in columns_def)
    _LOGGER.warning(
        f"Adding columns {cols} to table {table_name}. Note: this can take several "
        + "minutes on large databases and slow computers. Please "
        + "be patient!",
    )

    columns_def = [f"ADD {col_def}" for col_def in columns_def]

    with util.session_scope(session=session_maker()) as session:
        try:
            cols = ", ".join(columns_def)
            connection = session.connection()
            connection.execute(sql.text(f"ALTER TABLE {table_name} {cols}"))
            return
        except (
            sql_exc.InternalError,
            sql_exc.OperationalError,
            sql_exc.ProgrammingError,
        ):
            # Some engines support adding all columns at once,
            # this error is when they don't
            _LOGGER.info("Unable to use quick column add. Adding 1 by 1")

    for col_def in columns_def:
        with util.session_scope(session=session_maker()) as session:
            try:
                connection = session.connection()
                connection.execute(sql.text(f"ALTER TABLE {table_name} {col_def}"))
            except (
                sql_exc.InternalError,
                sql_exc.OperationalError,
                sql_exc.ProgrammingError,
            ) as err:
                raise_if_exception_missing_str(err, ["already exists", "duplicate"])
                _LOGGER.warning(
                    f"Column {col_def.split(' ')[1]} already exists on {table_name}, continuing",
                )


def _modify_columns(
    session_maker: SessionMaker,
    engine: sql.engine.Engine,
    table_name: str,
    columns_def: list[str],
) -> None:
    """Modify columns in a table."""
    cols = ", ".join(column.split(" ")[0] for column in columns_def)
    if engine.dialect.name == Const.SupportedDialect.SQLITE:
        _LOGGER.debug(
            f"Skipping to modify columns {cols} in table {table_name}; "
            + "Modifying column length in SQLite is unnecessary, "
            + "it does not impose any length restrictions",
        )
        return

    _LOGGER.warning(
        f"Modifying columns {cols} in table {table_name}. Note: this can take several "
        "minutes on large databases and slow computers. Please "
        "be patient!",
    )

    if engine.dialect.name == Const.SupportedDialect.POSTGRESQL:
        # pylint: disable=consider-using-f-string
        columns_def = [
            "ALTER {column} TYPE {type}".format(
                **dict(zip(["column", "type"], col_def.split(" ", 1)))
            )
            for col_def in columns_def
        ]
    elif engine.dialect.name == "mssql":
        columns_def = [f"ALTER COLUMN {col_def}" for col_def in columns_def]
    else:
        columns_def = [f"MODIFY {col_def}" for col_def in columns_def]

    with util.session_scope(session=session_maker()) as session:
        try:
            cols = ", ".join(columns_def)
            connection = session.connection()
            connection.execute(sql.text(f"ALTER TABLE {table_name} {cols}"))
            return
        except (sql_exc.InternalError, sql_exc.OperationalError):
            _LOGGER.info("Unable to use quick column modify. Modifying 1 by 1")

    for col_def in columns_def:
        with util.session_scope(session=session_maker()) as session:
            try:
                connection = session.connection()
                connection.execute(sql.text(f"ALTER TABLE {table_name} {col_def}"))
            except (sql_exc.InternalError, sql_exc.OperationalError):
                _LOGGER.exception(
                    f"Could not modify column {col_def} in table {table_name}"
                )


def _update_states_table_with_foreign_key_options(
    session_maker: SessionMaker, engine: sql.engine.Engine
) -> None:
    """Add the options to foreign key constraints."""
    inspector = sql.inspect(engine)
    alters = []
    for foreign_key in inspector.get_foreign_keys(_TABLE_STATES):
        if foreign_key["name"] and (
            # MySQL/MariaDB will have empty options
            not foreign_key.get("options")
            or
            # Postgres will have ondelete set to None
            foreign_key.get("options", {}).get("ondelete") is None
        ):
            alters.append(
                {
                    "old_fk": sql.schema.ForeignKeyConstraint(
                        (), (), name=foreign_key["name"]
                    ),
                    "columns": foreign_key["constrained_columns"],
                }
            )

    if not alters:
        return

    states_key_constraints = model.Base.metadata.tables[
        _TABLE_STATES
    ].foreign_key_constraints
    _old_states_table = sql.Table(  # noqa: F841
        _TABLE_STATES, sql.MetaData(), *(alter["old_fk"] for alter in alters)
    )

    for alter in alters:
        with util.session_scope(session=session_maker()) as session:
            try:
                connection = session.connection()
                connection.execute(sql.schema.DropConstraint(alter["old_fk"]))
                for fkc in states_key_constraints:
                    if fkc.column_keys == alter["columns"]:
                        connection.execute(sql.schema.AddConstraint(fkc))
            except (sql_exc.InternalError, sql_exc.OperationalError):
                _LOGGER.exception(
                    f"Could not update foreign options in {_TABLE_STATES} table"
                )


def _drop_foreign_key_constraints(
    session_maker: SessionMaker,
    engine: sql.engine.Engine,
    table: str,
    columns: list[str],
) -> None:
    """Drop foreign key constraints for a table on specific columns."""
    inspector = sql.inspect(engine)
    drops = []
    for foreign_key in inspector.get_foreign_keys(table):
        if (
            foreign_key["name"]
            and foreign_key.get("options", {}).get("ondelete")
            and foreign_key["constrained_columns"] == columns
        ):
            drops.append(
                sql.schema.ForeignKeyConstraint((), (), name=foreign_key["name"])
            )

    # Bind the ForeignKeyConstraints to the table
    _old_table = sql.Table(table, sql.MetaData(), *drops)  # noqa: F841

    for drop in drops:
        with util.session_scope(session=session_maker()) as session:
            try:
                connection = session.connection()
                connection.execute(sql.schema.DropConstraint(drop))
            except (sql_exc.InternalError, sql_exc.OperationalError):
                _LOGGER.exception(
                    f"Could not drop foreign constraints in {_TABLE_STATES} table on {columns}",
                )


def _apply_update(
    rec_comp: RecorderComponent,
    engine: sql.engine.Engine,
    session_maker: SessionMaker,
    new_version: int,
    old_version: int,
) -> None:
    """Perform operations to bring schema up to date."""
    dialect = engine.dialect.name
    big_int = "INTEGER(20)" if dialect == Const.SupportedDialect.MYSQL else "INTEGER"

    if new_version == 1:
        _create_index(session_maker, "events", "ix_events_time_fired")
    elif new_version == 2:
        # Create compound start/end index for recorder_runs
        _create_index(session_maker, "recorder_runs", "ix_recorder_runs_start_end")
        # Create indexes for states
        _create_index(session_maker, "states", "ix_states_last_updated")
    elif new_version == 3:
        # There used to be a new index here, but it was removed in version 4.
        pass
    elif new_version == 4:
        # Queries were rewritten in this schema release. Most indexes from
        # earlier versions of the schema are no longer needed.

        if old_version == 3:
            # Remove index that was added in version 3
            _drop_index(session_maker, "states", "ix_states_created_domain")
        if old_version == 2:
            # Remove index that was added in version 2
            _drop_index(session_maker, "states", "ix_states_entity_id_created")

        # Remove indexes that were added in version 0
        _drop_index(session_maker, "states", "states__state_changes")
        _drop_index(session_maker, "states", "states__significant_changes")
        _drop_index(session_maker, "states", "ix_states_entity_id_created")

        _create_index(session_maker, "states", "ix_states_entity_id_last_updated")
    elif new_version == 5:
        # Create supporting index for States.event_id foreign key
        _create_index(session_maker, "states", "ix_states_event_id")
    elif new_version == 6:
        _add_columns(
            session_maker,
            "events",
            ["context_id CHARACTER(36)", "context_user_id CHARACTER(36)"],
        )
        _create_index(session_maker, "events", "ix_events_context_id")
        _create_index(session_maker, "events", "ix_events_context_user_id")
        _add_columns(
            session_maker,
            "states",
            ["context_id CHARACTER(36)", "context_user_id CHARACTER(36)"],
        )
        _create_index(session_maker, "states", "ix_states_context_id")
        _create_index(session_maker, "states", "ix_states_context_user_id")
    elif new_version == 7:
        _create_index(session_maker, "states", "ix_states_entity_id")
    elif new_version == 8:
        _add_columns(session_maker, "events", ["context_parent_id CHARACTER(36)"])
        _add_columns(session_maker, "states", ["old_state_id INTEGER"])
        _create_index(session_maker, "events", "ix_events_context_parent_id")
    elif new_version == 9:
        # We now get the context from events with a join
        # since its always there on state_changed events
        #
        # Ideally we would drop the columns from the states
        # table as well but sqlite doesn't support that
        # and we would have to move to something like
        # sqlalchemy alembic to make that work
        #
        # no longer dropping ix_states_context_id since its recreated in 28
        _drop_index(session_maker, "states", "ix_states_context_user_id")
        # This index won't be there if they were not running
        # nightly but we don't treat that as a critical issue
        _drop_index(session_maker, "states", "ix_states_context_parent_id")
        # Redundant keys on composite index:
        # We already have ix_states_entity_id_last_updated
        _drop_index(session_maker, "states", "ix_states_entity_id")
        _create_index(session_maker, "events", "ix_events_event_type_time_fired")
        _drop_index(session_maker, "events", "ix_events_event_type")
    elif new_version == 10:
        # Now done in step 11
        pass
    elif new_version == 11:
        _create_index(session_maker, "states", "ix_states_old_state_id")
        _update_states_table_with_foreign_key_options(session_maker, engine)
    elif new_version == 12:
        if engine.dialect.name == Const.SupportedDialect.MYSQL:
            _modify_columns(session_maker, engine, "events", ["event_data LONGTEXT"])
            _modify_columns(session_maker, engine, "states", ["attributes LONGTEXT"])
    elif new_version == 13:
        if engine.dialect.name == Const.SupportedDialect.MYSQL:
            _modify_columns(
                session_maker,
                engine,
                "events",
                ["time_fired DATETIME(6)", "created DATETIME(6)"],
            )
            _modify_columns(
                session_maker,
                engine,
                "states",
                [
                    "last_changed DATETIME(6)",
                    "last_updated DATETIME(6)",
                    "created DATETIME(6)",
                ],
            )
    elif new_version == 14:
        _modify_columns(session_maker, engine, "events", ["event_type VARCHAR(64)"])
    elif new_version == 15:
        # This dropped the statistics table, done again in version 18.
        pass
    elif new_version == 16:
        _drop_foreign_key_constraints(
            session_maker, engine, _TABLE_STATES, ["old_state_id"]
        )
    elif new_version == 17:
        # This dropped the statistics table, done again in version 18.
        pass
    elif new_version == 18:
        # Recreate the statistics and statistics meta tables.
        #
        # Order matters! Statistics and StatisticsShortTerm have a relation with
        # StatisticsMeta, so statistics need to be deleted before meta (or in pair
        # depending on the SQL backend); and meta needs to be created before statistics.
        model.Base.metadata.drop_all(
            bind=engine,
            tables=[
                model.StatisticsShortTerm.__table__,
                model.Statistics.__table__,
                model.StatisticsMeta.__table__,  # pylint: disable=no-member
            ],
        )

        model.StatisticsMeta.__table__.create(engine)  # pylint: disable=no-member
        model.StatisticsShortTerm.__table__.create(engine)
        model.Statistics.__table__.create(engine)
    elif new_version == 19:
        # This adds the statistic runs table, insert a fake run to prevent duplicating
        # statistics.
        with util.session_scope(session=session_maker()) as session:
            session.add(model.StatisticsRuns(start=statistics.get_start_time()))
    elif new_version == 20:
        # This changed the precision of statistics from float to double
        if engine.dialect.name in [
            Const.SupportedDialect.MYSQL,
            Const.SupportedDialect.POSTGRESQL,
        ]:
            _modify_columns(
                session_maker,
                engine,
                "statistics",
                [
                    "mean DOUBLE PRECISION",
                    "min DOUBLE PRECISION",
                    "max DOUBLE PRECISION",
                    "state DOUBLE PRECISION",
                    "sum DOUBLE PRECISION",
                ],
            )
    elif new_version == 21:
        # Try to change the character set of the statistic_meta table
        if engine.dialect.name == Const.SupportedDialect.MYSQL:
            for table in ("events", "states", "statistics_meta"):
                _LOGGER.warning(
                    f"Updating character set and collation of table {table} to utf8mb4. "
                    + "Note: this can take several minutes on large databases and slow "
                    + "computers. Please be patient!",
                )
                with contextlib.suppress(sql_exc.SQLAlchemyError):
                    with util.session_scope(session=session_maker()) as session:
                        connection = session.connection()
                        connection.execute(
                            # Using LOCK=EXCLUSIVE to prevent the database from corrupting
                            # https://github.com/home-assistant/core/issues/56104
                            sql.text(
                                f"ALTER TABLE {table} CONVERT TO "
                                "CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci, LOCK=EXCLUSIVE"
                            )
                        )
    elif new_version == 22:
        # Recreate the all statistics tables for Oracle DB with Identity columns
        #
        # Order matters! Statistics has a relation with StatisticsMeta,
        # so statistics need to be deleted before meta (or in pair depending
        # on the SQL backend); and meta needs to be created before statistics.
        if engine.dialect.name == "oracle":
            model.Base.metadata.drop_all(
                bind=engine,
                tables=[
                    model.StatisticsShortTerm.__table__,
                    model.Statistics.__table__,
                    model.StatisticsMeta.__table__,  # pylint: disable=no-member
                    model.StatisticsRuns.__table__,
                ],
            )

            model.StatisticsRuns.__table__.create(engine)
            model.StatisticsMeta.__table__.create(engine)  # pylint: disable=no-member
            model.StatisticsShortTerm.__table__.create(engine)
            model.Statistics.__table__.create(engine)

        # Block 5-minute statistics for one hour from the last run, or it will overlap
        # with existing hourly statistics. Don't block on a database with no existing
        # statistics.
        with util.session_scope(session=session_maker()) as session:
            if session.query(model.Statistics.id).count() and (
                last_run_string := session.query(
                    sql.func.max(model.StatisticsRuns.start)
                ).scalar()
            ):
                last_run_start_time = model.process_timestamp(last_run_string)
                if last_run_start_time:
                    fake_start_time = last_run_start_time + datetime.timedelta(
                        minutes=5
                    )
                    while fake_start_time < last_run_start_time + datetime.timedelta(
                        hours=1
                    ):
                        session.add(model.StatisticsRuns(start=fake_start_time))
                        fake_start_time += datetime.timedelta(minutes=5)

        # When querying the database, be careful to only explicitly query for columns
        # which were present in schema version 21. If querying the table, SQLAlchemy
        # will refer to future columns.
        with util.session_scope(session=session_maker()) as session:
            for sum_statistic in session.query(model.StatisticsMeta.id).filter_by(
                has_sum=sql.sql.true()
            ):
                last_statistic = (
                    session.query(
                        model.Statistics.start,
                        model.Statistics.last_reset,
                        model.Statistics.state,
                        model.Statistics.sum,
                    )
                    .filter_by(metadata_id=sum_statistic.id)
                    .order_by(model.Statistics.start.desc())
                    .first()
                )
                if last_statistic:
                    session.add(
                        model.StatisticsShortTerm(
                            metadata_id=sum_statistic.id,
                            start=last_statistic.start,
                            last_reset=last_statistic.last_reset,
                            state=last_statistic.state,
                            sum=last_statistic.sum,
                        )
                    )
    elif new_version == 23:
        # Add name column to StatisticsMeta
        _add_columns(session_maker, "statistics_meta", ["name VARCHAR(255)"])
    elif new_version == 24:
        # Recreate statistics indices to block duplicated statistics
        _drop_index(session_maker, "statistics", "ix_statistics_statistic_id_start")
        _drop_index(
            session_maker,
            "statistics_short_term",
            "ix_statistics_short_term_statistic_id_start",
        )
        try:
            _create_index(
                session_maker, "statistics", "ix_statistics_statistic_id_start"
            )
            _create_index(
                session_maker,
                "statistics_short_term",
                "ix_statistics_short_term_statistic_id_start",
            )
        except sql_exc.DatabaseError:
            # There may be duplicated statistics entries, delete duplicated statistics
            # and try again
            with util.session_scope(session=session_maker()) as session:
                statistics.delete_statistics_duplicates(rec_comp, session)
            _create_index(
                session_maker, "statistics", "ix_statistics_statistic_id_start"
            )
            _create_index(
                session_maker,
                "statistics_short_term",
                "ix_statistics_short_term_statistic_id_start",
            )
    elif new_version == 25:
        _add_columns(session_maker, "states", [f"attributes_id {big_int}"])
        _create_index(session_maker, "states", "ix_states_attributes_id")
    elif new_version == 26:
        _create_index(session_maker, "statistics_runs", "ix_statistics_runs_start")
    elif new_version == 27:
        _add_columns(session_maker, "events", [f"data_id {big_int}"])
        _create_index(session_maker, "events", "ix_events_data_id")
    elif new_version == 28:
        _add_columns(session_maker, "events", ["origin_idx INTEGER"])
        # We never use the user_id or parent_id index
        _drop_index(session_maker, "events", "ix_events_context_user_id")
        _drop_index(session_maker, "events", "ix_events_context_parent_id")
        _add_columns(
            session_maker,
            "states",
            [
                "origin_idx INTEGER",
                "context_id VARCHAR(36)",
                "context_user_id VARCHAR(36)",
                "context_parent_id VARCHAR(36)",
            ],
        )
        _create_index(session_maker, "states", "ix_states_context_id")
        # Once there are no longer any state_changed events
        # in the events table we can drop the index on states.event_id
    elif new_version == 29:
        # Recreate statistics_meta index to block duplicated statistic_id
        _drop_index(session_maker, "statistics_meta", "ix_statistics_meta_statistic_id")
        if engine.dialect.name == Const.SupportedDialect.MYSQL:
            # Ensure the row format is dynamic or the index
            # unique will be too large
            with contextlib.suppress(sql_exc.SQLAlchemyError):
                with util.session_scope(session=session_maker()) as session:
                    connection = session.connection()
                    # This is safe to run multiple times and fast since the table is small
                    connection.execute(
                        sql.text("ALTER TABLE statistics_meta ROW_FORMAT=DYNAMIC")
                    )
        try:
            _create_index(
                session_maker, "statistics_meta", "ix_statistics_meta_statistic_id"
            )
        except sql_exc.DatabaseError:
            # There may be duplicated statistics_meta entries, delete duplicates
            # and try again
            with util.session_scope(session=session_maker()) as session:
                statistics.delete_statistics_meta_duplicates(session)
            _create_index(
                session_maker, "statistics_meta", "ix_statistics_meta_statistic_id"
            )
    else:
        raise ValueError(f"No schema migration defined for version {new_version}")


def _inspect_schema_version(session: sql_orm.Session) -> int:
    """Determine the schema version by inspecting the db structure.

    When the schema version is not present in the db, either db was just
    created with the correct schema, or this is a db created before schema
    versions were tracked. For now, we'll test if the changes for schema
    version 1 are present to make the determination. Eventually this logic
    can be removed and we can assume a new db is being created.
    """
    inspector = sql.inspect(session.connection())
    indexes = inspector.get_indexes("events")

    for index in indexes:
        if index["column_names"] == ["time_fired"]:
            # Schema addition from version 1 detected. New DB.
            session.add(model.StatisticsRuns(start=statistics.get_start_time()))
            session.add(model.SchemaChanges(schema_version=_SCHEMA_VERSION))
            return _SCHEMA_VERSION

    # Version 1 schema changes not found, this db needs to be migrated.
    current_version = model.SchemaChanges(schema_version=0)
    session.add(current_version)
    return typing.cast(int, current_version.schema_version)
