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
import datetime
import json
import logging
import typing

import ciso8601
import fnvhash
import frozenlist
import sqlalchemy as sql
import sqlalchemy.dialects.sqlite as dialect_sqlite
import sqlalchemy.dialects.postgresql as dialect_postgresql
import sqlalchemy.dialects.oracle as dialect_oracle
import sqlalchemy.dialects.mysql as dialect_mysql
import sqlalchemy.dialects as sql_dialects
import sqlalchemy.engine as sql_engine
import sqlalchemy.ext.declarative as sql_decl
import sqlalchemy.orm as sql_orm

from ... import core
from .const import Const

_statistic: typing.TypeAlias = core.Statistic

# SQLAlchemy Schema
# pylint: disable=invalid-name
Base: typing.TypeAlias = sql_orm.declarative_base()

_SCHEMA_VERSION: typing.Final = 29

_LOGGER: typing.Final = logging.getLogger(__name__)

_DB_TIMEZONE: typing.Final = "+00:00"

_TABLE_EVENTS: typing.Final = "events"
_TABLE_EVENT_DATA: typing.Final = "event_data"
_TABLE_STATES: typing.Final = "states"
_TABLE_STATE_ATTRIBUTES: typing.Final = "state_attributes"
_TABLE_RECORDER_RUNS: typing.Final = "recorder_runs"
_TABLE_SCHEMA_CHANGES: typing.Final = "schema_changes"
_TABLE_STATISTICS: typing.Final = "statistics"
_TABLE_STATISTICS_META: typing.Final = "statistics_meta"
_TABLE_STATISTICS_RUNS: typing.Final = "statistics_runs"
_TABLE_STATISTICS_SHORT_TERM: typing.Final = "statistics_short_term"

_ALL_TABLES: typing.Final = [
    _TABLE_STATES,
    _TABLE_STATE_ATTRIBUTES,
    _TABLE_EVENTS,
    _TABLE_EVENT_DATA,
    _TABLE_RECORDER_RUNS,
    _TABLE_SCHEMA_CHANGES,
    _TABLE_STATISTICS,
    _TABLE_STATISTICS_META,
    _TABLE_STATISTICS_RUNS,
    _TABLE_STATISTICS_SHORT_TERM,
]

_TABLES_TO_CHECK: typing.Final = frozenlist.FrozenList(
    [
        _TABLE_STATES,
        _TABLE_EVENTS,
        _TABLE_RECORDER_RUNS,
        _TABLE_SCHEMA_CHANGES,
    ]
)

_LAST_UPDATED_INDEX: typing.Final = "ix_states_last_updated"
_ENTITY_ID_LAST_UPDATED_INDEX: typing.Final = "ix_states_entity_id_last_updated"
_EVENTS_CONTEXT_ID_INDEX: typing.Final = "ix_events_context_id"
_STATES_CONTEXT_ID_INDEX: typing.Final = "ix_states_context_id"

_EMPTY_JSON_OBJECT: typing.Final = "{}"


class _FAST_PYSQLITE_DATETIME(dialect_sqlite.DATETIME):
    """Use ciso8601 to parse datetimes instead of sqlalchemy built-in regex."""

    def result_processor(self, dialect, coltype):
        """Offload the datetime parsing to ciso8601."""
        return lambda value: None if value is None else ciso8601.parse_datetime(value)


_JSON_VARIANT_CAST: typing.Final = sql.Text().with_variant(
    dialect_postgresql.JSON(none_as_null=True), "postgresql"
)
_JSONB_VARIANT_CAST: typing.Final = sql.Text().with_variant(
    dialect_postgresql.JSONB(none_as_null=True), "postgresql"
)
_DATETIME_TYPE: typing.Final = (
    sql.DateTime(timezone=True)
    .with_variant(dialect_mysql.DATETIME(timezone=True, fsp=6), "mysql")
    .with_variant(_FAST_PYSQLITE_DATETIME(), "sqlite")
)
_DOUBLE_TYPE: typing.Final = (
    sql.Float()
    .with_variant(dialect_mysql.DOUBLE(asdecimal=False), "mysql")
    .with_variant(dialect_oracle.DOUBLE_PRECISION(), "oracle")
    .with_variant(dialect_postgresql.DOUBLE_PRECISION(), "postgresql")
)


class _JSONLiteral(sql.JSON):
    """Teach SA how to literalize json."""

    def literal_processor(
        self, dialect: str
    ) -> collections.abc.Callable[[typing.Any], str]:
        """Processor to convert a value to JSON."""

        def process(value: typing.Any) -> str:
            """Dump json."""
            return json.dumps(value)

        return process


_EVENT_ORIGIN_ORDER = [core.EventOrigin.LOCAL, core.EventOrigin.REMOTE]
_EVENT_ORIGIN_TO_IDX = {origin: idx for idx, origin in enumerate(_EVENT_ORIGIN_ORDER)}


class UnsupportedDialect(Exception):
    """The dialect or its version is not supported."""


class Events(Base):
    """Event history data."""

    __table_args__ = (
        # Used for fetching events at a specific time
        # see logbook
        sql.Index("ix_events_event_type_time_fired", "event_type", "time_fired"),
        {"mysql_default_charset": "utf8mb4", "mysql_collate": "utf8mb4_unicode_ci"},
    )
    __tablename__ = _TABLE_EVENTS
    event_id = sql.Column(sql.Integer, sql.Identity(), primary_key=True)
    event_type = sql.Column(sql.String(core.Const.MAX_LENGTH_EVENT_EVENT_TYPE))
    event_data = sql.Column(
        sql.Text().with_variant(sql_dialects.mysql.LONGTEXT, "mysql")
    )
    origin = sql.Column(
        sql.String(core.Const.MAX_LENGTH_EVENT_ORIGIN)
    )  # no longer used for new rows
    origin_idx = sql.Column(sql.SmallInteger)
    time_fired = sql.Column(_DATETIME_TYPE, index=True)
    context_id = sql.Column(
        sql.String(core.Const.MAX_LENGTH_EVENT_CONTEXT_ID), index=True
    )
    context_user_id = sql.Column(sql.String(core.Const.MAX_LENGTH_EVENT_CONTEXT_ID))
    context_parent_id = sql.Column(sql.String(core.Const.MAX_LENGTH_EVENT_CONTEXT_ID))
    data_id = sql.Column(sql.Integer, sql.ForeignKey("event_data.data_id"), index=True)
    event_data_rel = sql_orm.relationship("EventData")

    def __repr__(self) -> str:
        """Return string representation of instance for debugging."""
        return (
            f"<recorder.Events("
            f"id={self.event_id}, type='{self.event_type}', "
            f"origin_idx='{self.origin_idx}', time_fired='{self.time_fired}'"
            f", data_id={self.data_id})>"
        )

    @staticmethod
    def from_event(event: core.Event):
        """Create an event database object from a native event."""
        return Events(
            event_type=event.event_type,
            event_data=None,
            origin_idx=_EVENT_ORIGIN_TO_IDX.get(event.origin),
            time_fired=event.time_fired,
            context_id=event.context.context_id,
            context_user_id=event.context.user_id,
            context_parent_id=event.context.parent_id,
        )

    def to_native(self, _validate_entity_id: bool = True) -> core.Event:
        """Convert to a native HA Event."""
        context = core.Context(
            context_id=self.context_id,
            user_id=self.context_user_id,
            parent_id=self.context_parent_id,
        )
        try:
            return core.Event(
                self.event_type,
                json.loads(self.event_data) if self.event_data else {},
                core.EventOrigin(self.origin)
                if self.origin
                else _EVENT_ORIGIN_ORDER[self.origin_idx],
                process_timestamp(self.time_fired),
                context=context,
            )
        except ValueError:
            # When json.loads fails
            _LOGGER.exception(f"Error converting to event: {self}")
            return None


class EventData(Base):
    """Event data history."""

    __table_args__ = (
        {"mysql_default_charset": "utf8mb4", "mysql_collate": "utf8mb4_unicode_ci"},
    )
    __tablename__ = _TABLE_EVENT_DATA
    data_id = sql.Column(sql.Integer, sql.Identity(), primary_key=True)
    hash = sql.Column(sql.BigInteger, index=True)
    # Note that this is not named attributes to avoid confusion with the states table
    shared_data = sql.Column(
        sql.Text().with_variant(sql_dialects.mysql.LONGTEXT, "mysql")
    )

    def __repr__(self) -> str:
        """Return string representation of instance for debugging."""
        return (
            f"<recorder.EventData("
            f"id={self.data_id}, hash='{self.hash}', data='{self.shared_data}'"
            f")>"
        )

    @staticmethod
    def from_event(event: core.Event):
        """Create object from an event."""
        shared_data = core.Const.JSON_DUMP(event.data)
        return EventData(
            shared_data=shared_data, hash=EventData.hash_shared_data(shared_data)
        )

    @staticmethod
    def shared_data_from_event(event: core.Event) -> str:
        """Create shared_attrs from an event."""
        return core.Const.JSON_DUMP(event.data)

    @staticmethod
    def hash_shared_data(shared_data: str) -> int:
        """Return the hash of json encoded shared data."""
        return typing.cast(int, fnvhash.fnv1a_32(shared_data.encode("utf-8")))

    def to_native(self) -> dict[str, typing.Any]:
        """Convert to an HA state object."""
        try:
            return typing.cast(dict[str, typing.Any], json.loads(self.shared_data))
        except ValueError:
            _LOGGER.exception(f"Error converting row to event data: {self}")
            return {}


class States(Base):
    """State change history."""

    __table_args__ = (
        # Used for fetching the state of entities at a specific time
        # (get_states in history.py)
        sql.Index(_ENTITY_ID_LAST_UPDATED_INDEX, "entity_id", "last_updated"),
        {"mysql_default_charset": "utf8mb4", "mysql_collate": "utf8mb4_unicode_ci"},
    )
    __tablename__ = _TABLE_STATES
    state_id = sql.Column(sql.Integer, sql.Identity(), primary_key=True)
    entity_id = sql.Column(sql.String(core.Const.MAX_LENGTH_STATE_ENTITY_ID))
    state = sql.Column(sql.String(core.Const.MAX_LENGTH_STATE_STATE))
    attributes = sql.Column(
        sql.Text().with_variant(sql_dialects.mysql.LONGTEXT, "mysql")
    )  # no longer used for new rows
    event_id = sql.Column(  # no longer used for new rows
        sql.Integer, sql.ForeignKey("events.event_id", ondelete="CASCADE"), index=True
    )
    last_changed = sql.Column(_DATETIME_TYPE)
    last_updated = sql.Column(_DATETIME_TYPE, default=core.helpers.utcnow, index=True)
    old_state_id = sql.Column(
        sql.Integer, sql.ForeignKey("states.state_id"), index=True
    )
    attributes_id = sql.Column(
        sql.Integer, sql.ForeignKey("state_attributes.attributes_id"), index=True
    )
    context_id = sql.Column(
        sql.String(core.Const.MAX_LENGTH_EVENT_CONTEXT_ID), index=True
    )
    context_user_id = sql.Column(sql.String(core.Const.MAX_LENGTH_EVENT_CONTEXT_ID))
    context_parent_id = sql.Column(sql.String(core.Const.MAX_LENGTH_EVENT_CONTEXT_ID))
    origin_idx = sql.Column(sql.SmallInteger)  # 0 is local, 1 is remote
    old_state = sql_orm.relationship("States", remote_side=[state_id])
    state_attributes = sql_orm.relationship("StateAttributes")

    def __repr__(self) -> str:
        """Return string representation of instance for debugging."""
        return (
            f"<recorder.States("
            f"id={self.state_id}, entity_id='{self.entity_id}', "
            f"state='{self.state}', event_id='{self.event_id}', "
            f"last_updated='{self.last_updated.isoformat(sep=' ', timespec='seconds')}', "
            f"old_state_id={self.old_state_id}, attributes_id={self.attributes_id}"
            f")>"
        )

    @staticmethod
    def from_event(event: core.Event):
        """Create object from a state_changed event."""
        entity_id = event.data["entity_id"]
        state: core.State = event.data.get("new_state")
        dbstate = States(
            entity_id=entity_id,
            attributes=None,
            context_id=event.context.context_id,
            context_user_id=event.context.user_id,
            context_parent_id=event.context.parent_id,
            origin_idx=_EVENT_ORIGIN_TO_IDX.get(event.origin),
        )

        # None state means the state was removed from the state machine
        if state is None:
            dbstate.state = ""
            dbstate.last_updated = event.time_fired
            dbstate.last_changed = None
            return dbstate

        dbstate.state = state.state
        dbstate.last_updated = state.last_updated
        if state.last_updated == state.last_changed:
            dbstate.last_changed = None
        else:
            dbstate.last_changed = state.last_changed

        return dbstate

    def to_native(self, validate_entity_id: bool = True) -> core.State:
        """Convert to an HA state object."""
        context = core.Context(
            context_id=self.context_id,
            user_id=self.context_user_id,
            parent_id=self.context_parent_id,
        )
        try:
            attrs = json.loads(self.attributes) if self.attributes else {}
        except ValueError:
            # When json.loads fails
            _LOGGER.exception(f"Error converting row to state: {self}")
            return None
        if self.last_changed is None or self.last_changed == self.last_updated:
            last_changed = last_updated = process_timestamp(self.last_updated)
        else:
            last_updated = process_timestamp(self.last_updated)
            last_changed = process_timestamp(self.last_changed)
        return core.State(
            self.entity_id,
            self.state,
            # Join the state_attributes table on attributes_id to get the attributes
            # for newer states
            attrs,
            last_changed,
            last_updated,
            context=context,
            validate_entity_id=validate_entity_id,
        )


class StateAttributes(Base):  # type: ignore[misc,valid-type]
    """State attribute change history."""

    __table_args__ = (
        {"mysql_default_charset": "utf8mb4", "mysql_collate": "utf8mb4_unicode_ci"},
    )
    __tablename__ = _TABLE_STATE_ATTRIBUTES
    attributes_id = sql.Column(sql.Integer, sql.Identity(), primary_key=True)
    hash = sql.Column(sql.BigInteger, index=True)
    # Note that this is not named attributes to avoid confusion with the states table
    shared_attrs = sql.Column(
        sql.Text().with_variant(sql_dialects.mysql.LONGTEXT, "mysql")
    )

    def __repr__(self) -> str:
        """Return string representation of instance for debugging."""
        return (
            f"<recorder.StateAttributes("
            f"id={self.attributes_id}, hash='{self.hash}', attributes='{self.shared_attrs}'"
            f")>"
        )

    @staticmethod
    def from_event(event: core.Event):
        """Create object from a state_changed event."""
        state: core.State = event.data.get("new_state")
        # None state means the state was removed from the state machine
        dbstate = StateAttributes(
            shared_attrs="{}"
            if state is None
            else core.Const.JSON_DUMP(state.attributes)
        )
        dbstate.hash = StateAttributes.hash_shared_attrs(dbstate.shared_attrs)
        return dbstate

    @staticmethod
    def shared_attrs_from_event(
        event: core.Event, exclude_attrs_by_domain: dict[str, set[str]]
    ) -> str:
        """Create shared_attrs from a state_changed event."""
        state: core.State = event.data.get("new_state")
        # None state means the state was removed from the state machine
        if state is None:
            return "{}"
        domain = core.helpers.split_entity_id(state.entity_id)[0]
        exclude_attrs = (
            exclude_attrs_by_domain.get(domain, set()) | Const.ALL_DOMAIN_EXCLUDE_ATTRS
        )
        return core.Const.JSON_DUMP(
            {k: v for k, v in state.attributes.items() if k not in exclude_attrs}
        )

    @staticmethod
    def hash_shared_attrs(shared_attrs: str) -> int:
        """Return the hash of json encoded shared attributes."""
        return typing.cast(int, fnvhash.fnv1a_32(shared_attrs.encode("utf-8")))

    def to_native(self) -> dict[str, typing.Any]:
        """Convert to an HA state object."""
        try:
            return typing.cast(dict[str, typing.Any], json.loads(self.shared_attrs))
        except ValueError:
            # When json.loads fails
            _LOGGER.exception(f"Error converting row to state attributes: {self}")
            return {}


class StatisticsBase:
    """Statistics base class."""

    id = sql.Column(sql.Integer, sql.Identity(), primary_key=True)
    created = sql.Column(_DATETIME_TYPE, default=core.helpers.utcnow)

    @sql_decl.declared_attr
    def metadata_id(self) -> sql.Column:
        """Define the metadata_id column for sub classes."""
        return sql.Column(
            sql.Integer,
            sql.ForeignKey(f"{_TABLE_STATISTICS_META}.id", ondelete="CASCADE"),
            index=True,
        )

    start = sql.Column(_DATETIME_TYPE, index=True)
    mean = sql.Column(_DOUBLE_TYPE)
    min = sql.Column(_DOUBLE_TYPE)
    max = sql.Column(_DOUBLE_TYPE)
    last_reset = sql.Column(_DATETIME_TYPE)
    state = sql.Column(_DOUBLE_TYPE)
    sum = sql.Column(_DOUBLE_TYPE)

    @classmethod
    def from_stats(cls, metadata_id: int, stats: _statistic.Data):
        """Create object from a statistics."""
        return cls(  # type: ignore[call-arg,misc]
            metadata_id=metadata_id,
            **stats,
        )


class Statistics(Base, StatisticsBase):
    """Long term statistics."""

    duration = datetime.timedelta(hours=1)

    __table_args__ = (
        # Used for fetching statistics for a certain entity at a specific time
        sql.Index(
            "ix_statistics_statistic_id_start", "metadata_id", "start", unique=True
        ),
    )
    __tablename__ = _TABLE_STATISTICS


class StatisticsShortTerm(Base, StatisticsBase):
    """Short term statistics."""

    duration = datetime.timedelta(minutes=5)

    __table_args__ = (
        # Used for fetching statistics for a certain entity at a specific time
        sql.Index(
            "ix_statistics_short_term_statistic_id_start",
            "metadata_id",
            "start",
            unique=True,
        ),
    )
    __tablename__ = _TABLE_STATISTICS_SHORT_TERM


class StatisticsMeta(Base):
    """Statistics meta data."""

    __table_args__ = (
        {"mysql_default_charset": "utf8mb4", "mysql_collate": "utf8mb4_unicode_ci"},
    )
    __tablename__ = _TABLE_STATISTICS_META
    id = sql.Column(sql.Integer, sql.Identity(), primary_key=True)
    statistic_id = sql.Column(sql.String(255), index=True, unique=True)
    source = sql.Column(sql.String(32))
    unit_of_measurement = sql.Column(sql.String(255))
    has_mean = sql.Column(sql.Boolean)
    has_sum = sql.Column(sql.Boolean)
    name = sql.Column(sql.String(255))

    @staticmethod
    def from_meta(meta: _statistic.MetaData):
        """Create object from meta data."""
        return StatisticsMeta(**meta)


class RecorderRuns(Base):
    """Representation of recorder run."""

    __table_args__ = (sql.Index("ix_recorder_runs_start_end", "start", "end"),)
    __tablename__ = _TABLE_RECORDER_RUNS
    run_id = sql.Column(sql.Integer, sql.Identity(), primary_key=True)
    start = sql.Column(sql.DateTime(timezone=True), default=core.helpers.utcnow)
    end = sql.Column(sql.DateTime(timezone=True))
    closed_incorrect = sql.Column(sql.Boolean, default=False)
    created = sql.Column(sql.DateTime(timezone=True), default=core.helpers.utcnow)

    def __repr__(self) -> str:
        """Return string representation of instance for debugging."""
        end = (
            f"'{self.end.isoformat(sep=' ', timespec='seconds')}'" if self.end else None
        )
        return (
            f"<recorder.RecorderRuns("
            f"id={self.run_id}, start='{self.start.isoformat(sep=' ', timespec='seconds')}', "
            f"end={end}, closed_incorrect={self.closed_incorrect}, "
            f"created='{self.created.isoformat(sep=' ', timespec='seconds')}'"
            f")>"
        )

    def entity_ids(self, point_in_time: datetime.datetime = None) -> list[str]:
        """Return the entity ids that existed in this run.

        Specify point_in_time if you want to know which existed at that point
        in time inside the run.
        """
        session = sql_orm.Session.object_session(self)

        assert session is not None, "RecorderRuns need to be persisted"

        query = session.query(sql.distinct(States.entity_id)).filter(
            States.last_updated >= self.start
        )

        if point_in_time is not None:
            query = query.filter(States.last_updated < point_in_time)
        elif self.end is not None:
            query = query.filter(States.last_updated < self.end)

        return [row[0] for row in query]

    def to_native(self, _validate_entity_id: bool = True):
        """Return self, native format is this model."""
        return self


class SchemaChanges(Base):
    """Representation of schema version changes."""

    __tablename__ = _TABLE_SCHEMA_CHANGES
    change_id = sql.Column(sql.Integer, sql.Identity(), primary_key=True)
    schema_version = sql.Column(sql.Integer)
    changed = sql.Column(sql.DateTime(timezone=True), default=core.helpers.utcnow)

    def __repr__(self) -> str:
        """Return string representation of instance for debugging."""
        return (
            f"<recorder.SchemaChanges("
            f"id={self.change_id}, schema_version={self.schema_version}, "
            f"changed='{self.changed.isoformat(sep=' ', timespec='seconds')}'"
            f")>"
        )


class StatisticsRuns(Base):
    """Representation of statistics run."""

    __tablename__ = _TABLE_STATISTICS_RUNS
    run_id = sql.Column(sql.Integer, sql.Identity(), primary_key=True)
    start = sql.Column(sql.DateTime(timezone=True), index=True)

    def __repr__(self) -> str:
        """Return string representation of instance for debugging."""
        return (
            f"<recorder.StatisticsRuns("
            f"id={self.run_id}, start='{self.start.isoformat(sep=' ', timespec='seconds')}', "
            f")>"
        )


_EVENT_DATA_JSON: typing.Final = sql.type_coerce(
    EventData.shared_data.cast(_JSONB_VARIANT_CAST), _JSONLiteral(none_as_null=True)
)
_OLD_FORMAT_EVENT_DATA_JSON: typing.Final = sql.type_coerce(
    Events.event_data.cast(_JSONB_VARIANT_CAST), _JSONLiteral(none_as_null=True)
)

_SHARED_ATTRS_JSON: typing.Final = sql.type_coerce(
    StateAttributes.shared_attrs.cast(_JSON_VARIANT_CAST), sql.JSON(none_as_null=True)
)
_OLD_FORMAT_ATTRS_JSON: typing.Final = sql.type_coerce(
    States.attributes.cast(_JSON_VARIANT_CAST), sql.JSON(none_as_null=True)
)

_ENTITY_ID_IN_EVENT: typing.Final[sql.Column] = _EVENT_DATA_JSON["entity_id"]
_OLD_ENTITY_ID_IN_EVENT: typing.Final[sql.Column] = _OLD_FORMAT_EVENT_DATA_JSON[
    "entity_id"
]
_DEVICE_ID_IN_EVENT: typing.Final[sql.Column] = _EVENT_DATA_JSON["device_id"]
_OLD_STATE: typing.Final = sql_orm.aliased(States, name="old_state")


@typing.overload
def process_timestamp(ts: None) -> None:
    ...


@typing.overload
def process_timestamp(ts: datetime.datetime) -> datetime.time:
    ...


def process_timestamp(ts: datetime.datetime) -> datetime.datetime:
    """Process a timestamp into datetime object."""
    if ts is None:
        return None
    if ts.tzinfo is None:
        return ts.replace(tzinfo=datetime.timezone.utc)

    return core.helpers.as_utc(ts)


@typing.overload
def process_timestamp_to_utc_isoformat(ts: None) -> None:
    ...


@typing.overload
def process_timestamp_to_utc_isoformat(ts: datetime.datetime) -> str:
    ...


def process_timestamp_to_utc_isoformat(ts: datetime.datetime) -> str:
    """Process a timestamp into UTC isotime."""
    if ts is None:
        return None
    if ts.tzinfo == datetime.timezone.utc:
        return ts.isoformat()
    if ts.tzinfo is None:
        return f"{ts.isoformat()}{_DB_TIMEZONE}"
    return ts.astimezone(datetime.timezone.utc).isoformat()


def process_datetime_to_timestamp(ts: datetime.datetime) -> float:
    """Process a datebase datetime to epoch.

    Mirrors the behavior of process_timestamp_to_utc_isoformat
    except it returns the epoch time.
    """
    if ts.tzinfo is None or ts.tzinfo == datetime.timezone.utc:
        return core.helpers.utc_to_timestamp(ts)
    return ts.timestamp()


class LazyState(core.State):
    """A lazy version of core State."""

    __slots__ = [
        "_row",
        "_attr_cache",
    ]

    def __init__(  # pylint: disable=super-init-not-called
        self,
        row: sql_engine.Row,
        attr_cache: dict[str, dict[str, typing.Any]],
        start_time: datetime.datetime = None,
    ) -> None:
        """Init the lazy state."""
        self._row = row
        self._entity_id: str = self._row.entity_id
        self._state = self._row.state or ""
        self._attributes: dict[str, typing.Any] = None
        self._last_changed: datetime.datetime = start_time
        self._last_updated: datetime.datetime = start_time
        self._context: core.Context = None
        self._attr_cache = attr_cache

    @property
    def attr_cache(self) -> dict[str, dict[str, typing.Any]]:
        return self._attr_cache

    @property
    def attributes(self) -> dict[str, typing.Any]:
        """State attributes."""
        if self._attributes is None:
            self._attributes = decode_attributes_from_row(self._row, self.attr_cache)
        return self._attributes

    @attributes.setter
    def attributes(self, value: dict[str, typing.Any]) -> None:
        """Set attributes."""
        self._attributes = value

    @property
    def context(self) -> core.Context:
        """State context."""
        if self._context is None:
            self._context = core.Context(context_id=None)
        return self._context

    @context.setter
    def context(self, value: core.Context) -> None:
        """Set context."""
        self._context = value

    @property
    def last_changed(self) -> datetime.datetime:
        """Last changed datetime."""
        if self._last_changed is None:
            if (last_changed := self._row.last_changed) is not None:
                self._last_changed = process_timestamp(last_changed)
            else:
                self._last_changed = self.last_updated
        return self._last_changed

    @last_changed.setter
    def last_changed(self, value: datetime.datetime) -> None:
        """Set last changed datetime."""
        self._last_changed = value

    @property
    def last_updated(self) -> datetime.datetime:
        """Last updated datetime."""
        if self._last_updated is None:
            self._last_updated = process_timestamp(self._row.last_updated)
        return self._last_updated

    @last_updated.setter
    def last_updated(self, value: datetime.datetime) -> None:
        """Set last updated datetime."""
        self._last_updated = value

    def as_dict(self) -> dict[str, typing.Any]:
        """Return a dict representation of the LazyState.

        Async friendly.

        To be used for JSON serialization.
        """
        if self._last_changed is None and self._last_updated is None:
            last_updated_isoformat = process_timestamp_to_utc_isoformat(
                self._row.last_updated
            )
            if (
                self._row.last_changed is None
                or self._row.last_changed == self._row.last_updated
            ):
                last_changed_isoformat = last_updated_isoformat
            else:
                last_changed_isoformat = process_timestamp_to_utc_isoformat(
                    self._row.last_changed
                )
        else:
            last_updated_isoformat = self.last_updated.isoformat()
            if self.last_changed == self.last_updated:
                last_changed_isoformat = last_updated_isoformat
            else:
                last_changed_isoformat = self.last_changed.isoformat()
        return {
            "entity_id": self._entity_id,
            "state": self._state,
            "attributes": self._attributes or self.attributes,
            "last_changed": last_changed_isoformat,
            "last_updated": last_updated_isoformat,
        }

    def __eq__(self, other: typing.Any) -> bool:
        """Return the comparison."""
        return (
            other.__class__ in [self.__class__, core.State]
            and self._entity_id == other.entity_id
            and self.state == other.state
            and self.attributes == other.attributes
        )


def decode_attributes_from_row(
    row: sql_engine.Row, attr_cache: dict[str, dict[str, typing.Any]]
) -> dict[str, typing.Any]:
    """Decode attributes from a database row."""
    source: str = row.shared_attrs or row.attributes
    if (attributes := attr_cache.get(source)) is not None:
        return attributes
    if not source or source == _EMPTY_JSON_OBJECT:
        return {}
    try:
        attr_cache[source] = attributes = json.loads(source)
    except ValueError:
        _LOGGER.exception(f"Error converting row to state attributes: {source}")
        attr_cache[source] = attributes = {}
    return attributes


def row_to_compressed_state(
    row: sql_engine.Row,
    attr_cache: dict[str, dict[str, typing.Any]],
    start_time: datetime.datetime = None,
) -> dict[str, typing.Any]:
    """Convert a database row to a compressed state."""
    comp_state = {
        core.WebSocket.COMPRESSED_STATE_STATE: row.state,
        core.WebSocket.COMPRESSED_STATE_ATTRIBUTES: decode_attributes_from_row(
            row, attr_cache
        ),
    }
    if start_time:
        comp_state[
            core.WebSocket.COMPRESSED_STATE_LAST_UPDATED
        ] = start_time.timestamp()
    else:
        row_last_updated: datetime = row.last_updated
        comp_state[
            core.WebSocket.COMPRESSED_STATE_LAST_UPDATED
        ] = process_datetime_to_timestamp(row_last_updated)
        if (
            row_changed_changed := row.last_changed
        ) and row_last_updated != row_changed_changed:
            comp_state[
                core.WebSocket.COMPRESSED_STATE_LAST_CHANGED
            ] = process_datetime_to_timestamp(row_changed_changed)
    return comp_state
