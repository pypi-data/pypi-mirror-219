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

import collections
import collections.abc
import contextlib
import dataclasses
import datetime as dt
import functools as ft
import itertools as it
import json
import logging
import os
import re
import statistics
import typing

import sqlalchemy as sql
import sqlalchemy.exc as sql_exc
import sqlalchemy.orm as sql_orm
import voluptuous as vol

from ... import core
from . import model, util
from .const import Const

_statistic: typing.TypeAlias = core.Statistic

if not typing.TYPE_CHECKING:

    class RecorderComponent:
        ...

    class Recorder:
        ...


if typing.TYPE_CHECKING:
    from .recorder_component import RecorderComponent
    from .recorder import Recorder

_QUERY_STATISTICS: typing.Final = [
    model.Statistics.metadata_id,
    model.Statistics.start,
    model.Statistics.mean,
    model.Statistics.min,
    model.Statistics.max,
    model.Statistics.last_reset,
    model.Statistics.state,
    model.Statistics.sum,
]

_QUERY_STATISTICS_SHORT_TERM: typing.Final = [
    model.StatisticsShortTerm.metadata_id,
    model.StatisticsShortTerm.start,
    model.StatisticsShortTerm.mean,
    model.StatisticsShortTerm.min,
    model.StatisticsShortTerm.max,
    model.StatisticsShortTerm.last_reset,
    model.StatisticsShortTerm.state,
    model.StatisticsShortTerm.sum,
]

_QUERY_STATISTICS_SUMMARY_MEAN: typing.Final = [
    model.StatisticsShortTerm.metadata_id,
    sql.func.avg(model.StatisticsShortTerm.mean),
    sql.func.min(model.StatisticsShortTerm.min),
    sql.func.max(model.StatisticsShortTerm.max),
]

_QUERY_STATISTICS_SUMMARY_SUM: typing.Final = [
    model.StatisticsShortTerm.metadata_id,
    model.StatisticsShortTerm.start,
    model.StatisticsShortTerm.last_reset,
    model.StatisticsShortTerm.state,
    model.StatisticsShortTerm.sum,
    sql.func.row_number()
    .over(
        partition_by=model.StatisticsShortTerm.metadata_id,
        order_by=model.StatisticsShortTerm.start.desc(),
    )
    .label("rownum"),
]

_QUERY_STATISTICS_SUMMARY_SUM_LEGACY: typing.Final = [
    model.StatisticsShortTerm.metadata_id,
    model.StatisticsShortTerm.last_reset,
    model.StatisticsShortTerm.state,
    model.StatisticsShortTerm.sum,
]

_QUERY_STATISTIC_META: typing.Final = [
    model.StatisticsMeta.id,
    model.StatisticsMeta.statistic_id,
    model.StatisticsMeta.source,
    model.StatisticsMeta.unit_of_measurement,
    model.StatisticsMeta.has_mean,
    model.StatisticsMeta.has_sum,
    model.StatisticsMeta.name,
]

_QUERY_STATISTIC_META_ID = [
    model.StatisticsMeta.id,
    model.StatisticsMeta.statistic_id,
]


_LOGGER = logging.getLogger(__name__)
_UNDEFINED: typing.Final = object()


def _get_unit_class(unit: str) -> str:
    """Get corresponding unit class from from the statistics unit."""
    if converter := _statistic.STATISTIC_UNIT_TO_UNIT_CONVERTER.get(unit):
        return converter.UNIT_CLASS
    return None


def _get_statistic_to_display_unit_converter(
    statistic_unit: str,
    state_unit: str,
    requested_units: dict[str, str],
) -> typing.Callable[[float], float]:
    """Prepare a converter from the statistics unit to display unit."""

    def no_conversion(val: float) -> float:
        """Return val."""
        return val

    if statistic_unit is None:
        return no_conversion

    if (
        converter := _statistic.STATISTIC_UNIT_TO_UNIT_CONVERTER.get(statistic_unit)
    ) is None:
        return no_conversion

    display_unit: str
    unit_class = converter.UNIT_CLASS
    if requested_units and unit_class in requested_units:
        display_unit = requested_units[unit_class]
    else:
        display_unit = state_unit

    if display_unit not in converter.VALID_UNITS:
        # Guard against invalid state unit in the DB
        return no_conversion

    def from_normalized_unit(
        val: float, conv: type[core.BaseUnitConverter], from_unit: str, to_unit: str
    ) -> float | None:
        """Return val."""
        if val is None:
            return val
        return conv.convert(val, from_unit=from_unit, to_unit=to_unit)

    return ft.partial(
        from_normalized_unit,
        conv=converter,
        from_unit=statistic_unit,
        to_unit=display_unit,
    )


def _get_display_to_statistic_unit_converter(
    display_unit: str,
    statistic_unit: str,
) -> typing.Callable[[float], float]:
    """Prepare a converter from the display unit to the statistics unit."""

    def no_conversion(val: float) -> float:
        """Return val."""
        return val

    if statistic_unit is None:
        return no_conversion

    if (
        converter := _statistic.STATISTIC_UNIT_TO_UNIT_CONVERTER.get(statistic_unit)
    ) is None:
        return no_conversion

    return ft.partial(converter.convert, from_unit=display_unit, to_unit=statistic_unit)


def _get_unit_converter(
    from_unit: str, to_unit: str
) -> typing.Callable[[float], float]:
    """Prepare a converter from a unit to another unit."""

    def convert_units(
        val: float, conv: type[core.BaseUnitConverter], from_unit: str, to_unit: str
    ) -> float:
        """Return converted val."""
        if val is None:
            return val
        return conv.convert(val, from_unit=from_unit, to_unit=to_unit)

    for conv in _statistic.STATISTIC_UNIT_TO_UNIT_CONVERTER.values():
        if from_unit in conv.VALID_UNITS and to_unit in conv.VALID_UNITS:
            return ft.partial(
                convert_units, conv=conv, from_unit=from_unit, to_unit=to_unit
            )
    raise core.SmartHomeControllerError


def can_convert_units(from_unit: str | None, to_unit: str | None) -> bool:
    """Return True if it's possible to convert from from_unit to to_unit."""
    for converter in _statistic.STATISTIC_UNIT_TO_UNIT_CONVERTER.values():
        if from_unit in converter.VALID_UNITS and to_unit in converter.VALID_UNITS:
            return True
    return False


def split_statistic_id(entity_id: str) -> list[str]:
    """Split a state entity ID into domain and object ID."""
    return entity_id.split(":", 1)


_VALID_STATISTIC_ID: typing.Final = re.compile(
    r"^(?!.+__)(?!_)[\da-z_]+(?<!_):(?!_)[\da-z_]+(?<!_)$"
)


def valid_statistic_id(statistic_id: str) -> bool:
    """Test if a statistic ID is a valid format.

    Format: <domain>:<statistic> where both are slugs.
    """
    return _VALID_STATISTIC_ID.match(statistic_id) is not None


def validate_statistic_id(value: str) -> str:
    """Validate statistic ID."""
    if valid_statistic_id(value):
        return value

    raise vol.Invalid(f"Statistics ID {value} is an invalid statistic ID")


@dataclasses.dataclass()
class ValidationIssue:
    """Error or warning message."""

    type: str
    data: dict[str, str] = None

    def as_dict(self) -> dict:
        """Return dictionary version."""
        return dataclasses.asdict(self)


def get_start_time() -> dt.datetime:
    """Return start time."""
    now = core.helpers.utcnow()
    current_period_minutes = now.minute - now.minute % 5
    current_period = now.replace(minute=current_period_minutes, second=0, microsecond=0)
    last_period = current_period - dt.timedelta(minutes=5)
    return last_period


def _update_or_add_metadata(
    session: sql_orm.Session,
    new_metadata: _statistic.MetaData,
    old_metadata_dict: dict[str, tuple[int, _statistic.MetaData]],
) -> int:
    """Get metadata_id for a statistic_id.

    If the statistic_id is previously unknown, add it. If it's already known, update
    metadata if needed.

    Updating metadata source is not possible.
    """
    statistic_id = new_metadata["statistic_id"]
    if statistic_id not in old_metadata_dict:
        meta = model.StatisticsMeta.from_meta(new_metadata)
        session.add(meta)
        session.flush()  # Flush to get the metadata id assigned
        _LOGGER.debug(
            f"Added new statistics metadata for {statistic_id}, new_metadata: {new_metadata}",
        )
        return meta.id

    metadata_id, old_metadata = old_metadata_dict[statistic_id]
    if (
        old_metadata["has_mean"] != new_metadata["has_mean"]
        or old_metadata["has_sum"] != new_metadata["has_sum"]
        or old_metadata["unit_of_measurement"] != new_metadata["unit_of_measurement"]
    ):
        session.query(model.StatisticsMeta).filter_by(statistic_id=statistic_id).update(
            {
                model.StatisticsMeta.has_mean: new_metadata["has_mean"],
                model.StatisticsMeta.has_sum: new_metadata["has_sum"],
                model.StatisticsMeta.unit_of_measurement: new_metadata[
                    "unit_of_measurement"
                ],
            },
            synchronize_session=False,
        )
        _LOGGER.debug(
            f"Updated statistics metadata for {statistic_id}, old_metadata: "
            + f"%{old_metadata}, new_metadata: {new_metadata}",
        )

    return metadata_id


def _find_duplicates(
    session: sql_orm.Session, table: type[model.Statistics | model.StatisticsShortTerm]
) -> tuple[list[int], list[dict]]:
    """Find duplicated statistics."""
    subquery = (
        session.query(
            table.start,
            table.metadata_id,
            sql.literal_column("1").label("is_duplicate"),
        )
        .group_by(table.metadata_id, table.start)
        .having(sql.func.count() > 1)
        .subquery()
    )
    query = (
        session.query(table)
        .outerjoin(
            subquery,
            (subquery.c.metadata_id == table.metadata_id)
            & (subquery.c.start == table.start),
        )
        .filter(subquery.c.is_duplicate == 1)
        .order_by(table.metadata_id, table.start, table.id.desc())
        .limit(1000 * Const.MAX_ROWS_TO_PURGE)
    )
    duplicates = util.execute(query)
    original_as_dict = {}
    start = None
    metadata_id = None
    duplicate_ids: list[int] = []
    non_identical_duplicates_as_dict: list[dict] = []

    if not duplicates:
        return (duplicate_ids, non_identical_duplicates_as_dict)

    def columns_to_dict(
        duplicate: type[model.Statistics | model.StatisticsShortTerm],
    ) -> dict:
        """Convert a SQLAlchemy row to dict."""
        dict_ = {}
        for key in duplicate.__mapper__.c.keys():
            dict_[key] = getattr(duplicate, key)
        return dict_

    def compare_statistic_rows(row1: dict, row2: dict) -> bool:
        """Compare two statistics rows, ignoring id and created."""
        ignore_keys = ["id", "created"]
        keys1 = set(row1).difference(ignore_keys)
        keys2 = set(row2).difference(ignore_keys)
        return keys1 == keys2 and all(row1[k] == row2[k] for k in keys1)

    for duplicate in duplicates:
        if start != duplicate.start or metadata_id != duplicate.metadata_id:
            original_as_dict = columns_to_dict(duplicate)
            start = duplicate.start
            metadata_id = duplicate.metadata_id
            continue
        duplicate_as_dict = columns_to_dict(duplicate)
        duplicate_ids.append(duplicate.id)
        if not compare_statistic_rows(original_as_dict, duplicate_as_dict):
            non_identical_duplicates_as_dict.append(
                {"duplicate": duplicate_as_dict, "original": original_as_dict}
            )

    return (duplicate_ids, non_identical_duplicates_as_dict)


def _delete_duplicates_from_table(
    session: sql_orm.Session, table: type[model.Statistics | model.StatisticsShortTerm]
) -> tuple[int, list[dict]]:
    """Identify and delete duplicated statistics from a specified table."""
    all_non_identical_duplicates: list[dict] = []
    total_deleted_rows = 0
    while True:
        duplicate_ids, non_identical_duplicates = _find_duplicates(session, table)
        if not duplicate_ids:
            break
        all_non_identical_duplicates.extend(non_identical_duplicates)
        for i in range(0, len(duplicate_ids), Const.MAX_ROWS_TO_PURGE):
            deleted_rows = (
                session.query(table)
                .filter(table.id.in_(duplicate_ids[i : i + Const.MAX_ROWS_TO_PURGE]))
                .delete(synchronize_session=False)
            )
            total_deleted_rows += deleted_rows
    return (total_deleted_rows, all_non_identical_duplicates)


def delete_statistics_duplicates(
    rec_comp: RecorderComponent, session: sql_orm.Session
) -> None:
    """Identify and delete duplicated statistics.

    A backup will be made of duplicated statistics before it is deleted.
    """
    deleted_statistics_rows, non_identical_duplicates = _delete_duplicates_from_table(
        session, model.Statistics
    )
    if deleted_statistics_rows:
        _LOGGER.info(f"Deleted {deleted_statistics_rows} duplicated statistics rows")

    if non_identical_duplicates:
        isotime = core.helpers.utcnow().isoformat()
        backup_file_name = f"deleted_statistics.{isotime}.json"
        backup_path = rec_comp.config.path(Const.BACKUP_DIR, backup_file_name)

        os.makedirs(os.path.dirname(backup_path), exist_ok=True)
        with open(backup_path, "w", encoding="utf8") as backup_file:
            json.dump(
                non_identical_duplicates,
                backup_file,
                indent=4,
                sort_keys=True,
                cls=core.JsonEncoder,
            )
        _LOGGER.warning(
            f"Deleted {len(non_identical_duplicates)} non identical duplicated "
            + f"{model.Statistics.__tablename__} rows, a backup of the deleted rows "
            + f"has been saved to {backup_path}",
        )

    deleted_short_term_statistics_rows, _ = _delete_duplicates_from_table(
        session, model.StatisticsShortTerm
    )
    if deleted_short_term_statistics_rows:
        rep_url = (
            "https://github.com/home-assistant/core/issues?q=is%3Aopen+is%3A"
            + "issue+label%3A%22integration%3A+recorder%22"
        )
        _LOGGER.warning(
            f"Deleted duplicated short term statistic rows, please report at {rep_url}",
        )


def _find_statistics_meta_duplicates(session: sql_orm.Session) -> list[int]:
    """Find duplicated statistics_meta."""
    subquery = (
        session.query(
            model.StatisticsMeta.statistic_id,
            sql.literal_column("1").label("is_duplicate"),
        )
        .group_by(model.StatisticsMeta.statistic_id)
        .having(sql.func.count() > 1)
        .subquery()
    )
    query = (
        session.query(model.StatisticsMeta)
        .outerjoin(
            subquery,
            (subquery.c.statistic_id == model.StatisticsMeta.statistic_id),
        )
        .filter(subquery.c.is_duplicate == 1)
        .order_by(model.StatisticsMeta.statistic_id, model.StatisticsMeta.id.desc())
        .limit(1000 * Const.MAX_ROWS_TO_PURGE)
    )
    duplicates = util.execute(query)
    statistic_id = None
    duplicate_ids: list[int] = []

    if not duplicates:
        return duplicate_ids

    for duplicate in duplicates:
        if statistic_id != duplicate.statistic_id:
            statistic_id = duplicate.statistic_id
            continue
        duplicate_ids.append(duplicate.id)

    return duplicate_ids


def _delete_statistics_meta_duplicates(session: sql_orm.Session) -> int:
    """Identify and delete duplicated statistics from a specified table."""
    total_deleted_rows = 0
    while True:
        duplicate_ids = _find_statistics_meta_duplicates(session)
        if not duplicate_ids:
            break
        for i in range(0, len(duplicate_ids), Const.MAX_ROWS_TO_PURGE):
            deleted_rows = (
                session.query(model.StatisticsMeta)
                .filter(
                    model.StatisticsMeta.id.in_(
                        duplicate_ids[i : i + Const.MAX_ROWS_TO_PURGE]
                    )
                )
                .delete(synchronize_session=False)
            )
            total_deleted_rows += deleted_rows
    return total_deleted_rows


def delete_statistics_meta_duplicates(session: sql_orm.Session) -> None:
    """Identify and delete duplicated statistics_meta."""
    deleted_statistics_rows = _delete_statistics_meta_duplicates(session)
    if deleted_statistics_rows:
        _LOGGER.info(
            f"Deleted {deleted_statistics_rows} duplicated statistics_meta rows"
        )


def _compile_hourly_statistics_summary_mean_stmt(
    start_time: dt.datetime, end_time: dt.datetime
) -> sql.sql.StatementLambdaElement:
    """Generate the summary mean statement for hourly statistics."""
    stmt = sql.lambda_stmt(lambda: sql.select(*_QUERY_STATISTICS_SUMMARY_MEAN))
    stmt += (
        lambda q: q.filter(model.StatisticsShortTerm.start >= start_time)
        .filter(model.StatisticsShortTerm.start < end_time)
        .group_by(model.StatisticsShortTerm.metadata_id)
        .order_by(model.StatisticsShortTerm.metadata_id)
    )
    return stmt


def compile_hourly_statistics(session: sql_orm.Session, start: dt.datetime) -> None:
    """Compile hourly statistics.

    This will summarize 5-minute statistics for one hour:
    - average, min max is computed by a database query
    - sum is taken from the last 5-minute entry during the hour
    """
    start_time = start.replace(minute=0)
    end_time = start_time + dt.timedelta(hours=1)

    # Compute last hour's average, min, max
    summary: dict[str, _statistic.Data] = {}
    stmt = _compile_hourly_statistics_summary_mean_stmt(start_time, end_time)
    stats = util.execute_stmt_lambda_element(session, stmt)

    if stats:
        for stat in stats:
            metadata_id, _mean, _min, _max = stat
            summary[metadata_id] = {
                "start": start_time,
                "mean": _mean,
                "min": _min,
                "max": _max,
            }

    # Get last hour's last sum
    subquery = (
        session.query(*_QUERY_STATISTICS_SUMMARY_SUM)
        .filter(model.StatisticsShortTerm.start >= sql.bindparam("start_time"))
        .filter(model.StatisticsShortTerm.start < sql.bindparam("end_time"))
        .subquery()
    )
    query = (
        session.query(subquery)
        .filter(subquery.c.rownum == 1)
        .order_by(subquery.c.metadata_id)
    )
    stats = util.execute(query.params(start_time=start_time, end_time=end_time))

    if stats:
        for stat in stats:
            metadata_id, start, last_reset, state, _sum, _ = stat
            if metadata_id in summary:
                summary[metadata_id].update(
                    {
                        "last_reset": model.process_timestamp(last_reset),
                        "state": state,
                        "sum": _sum,
                    }
                )
            else:
                summary[metadata_id] = {
                    "start": start_time,
                    "last_reset": model.process_timestamp(last_reset),
                    "state": state,
                    "sum": _sum,
                }

    # Insert compiled hourly statistics in the database
    for metadata_id, stat in summary.items():
        session.add(model.Statistics.from_stats(metadata_id, stat))


def compile_statistics(instance: Recorder, start: dt.datetime) -> bool:
    """Compile 5-minute statistics for all integrations with a recorder platform.

    The actual calculation is delegated to the platforms.
    """
    start = core.helpers.as_utc(start)
    end = start + dt.timedelta(minutes=5)

    # Return if we already have 5-minute statistics for the requested period
    with util.session_scope(session=instance.get_session()) as session:
        if session.query(model.StatisticsRuns).filter_by(start=start).first():
            _LOGGER.debug(f"Statistics already compiled for{start}-{end}", start, end)
            return True

    _LOGGER.debug(f"Compiling statistics for {start}-{end}")
    platform_stats: list[_statistic.Result] = []
    current_metadata: dict[str, tuple[int, _statistic.MetaData]] = {}
    # Collect statistics from all platforms implementing support
    for domain, platform in instance.owner.items():
        if not platform.supports_statistics or not platform.supports_compile_statistics:
            continue
        compiled: _statistic.PlatformCompiledStatistics = platform.compile_statistics(
            instance.owner, start, end
        )
        _LOGGER.debug(
            f"Statistics for {domain} during {start}-{end}: "
            + f"{compiled.platform_stats}",
        )
        platform_stats.extend(compiled.platform_stats)
        current_metadata.update(compiled.current_metadata)

    # Insert collected statistics in the database
    with util.session_scope(
        session=instance.get_session(),
        exception_filter=_filter_unique_constraint_integrity_error(instance),
    ) as session:
        for stats in platform_stats:
            metadata_id = _update_or_add_metadata(
                session, stats["meta"], current_metadata
            )
            _insert_statistics(
                session,
                model.StatisticsShortTerm,
                metadata_id,
                stats["stat"],
            )

        if start.minute == 55:
            # A full hour is ready, summarize it
            compile_hourly_statistics(session, start)

        session.add(model.StatisticsRuns(start=start))

    return True


def _adjust_sum_statistics(
    session: sql_orm.Session,
    table: type[model.Statistics | model.StatisticsShortTerm],
    metadata_id: int,
    start_time: dt.datetime,
    adj: float,
) -> None:
    """Adjust statistics in the database."""
    try:
        session.query(table).filter_by(metadata_id=metadata_id).filter(
            table.start >= start_time
        ).update(
            {
                table.sum: table.sum + adj,
            },
            synchronize_session=False,
        )
    except sql_exc.SQLAlchemyError:
        _LOGGER.exception(
            f"Unexpected exception when updating statistics {id}",
        )


def _insert_statistics(
    session: sql_orm.Session,
    table: type[model.Statistics | model.StatisticsShortTerm],
    metadata_id: int,
    statistic: _statistic.Data,
) -> None:
    """Insert statistics in the database."""
    try:
        session.add(table.from_stats(metadata_id, statistic))
    except sql_exc.SQLAlchemyError:
        _LOGGER.exception(
            f"Unexpected exception when inserting statistics {metadata_id}:"
            + f"{statistic}",
        )


def _update_statistics(
    session: sql_orm.Session,
    table: type[model.Statistics | model.StatisticsShortTerm],
    stat_id: int,
    statistic: _statistic.Data,
) -> None:
    """Insert statistics in the database."""
    try:
        session.query(table).filter_by(id=stat_id).update(
            {
                table.mean: statistic.get("mean"),
                table.min: statistic.get("min"),
                table.max: statistic.get("max"),
                table.last_reset: statistic.get("last_reset"),
                table.state: statistic.get("state"),
                table.sum: statistic.get("sum"),
            },
            synchronize_session=False,
        )
    except sql_exc.SQLAlchemyError:
        _LOGGER.exception(
            f"Unexpected exception when updating statistics {stat_id}:{statistic}",
        )


def _generate_get_metadata_stmt(
    statistic_ids: list[str] | tuple[str] = None,
    statistic_type: typing.Literal["mean"] | typing.Literal["sum"] = None,
    statistic_source: str = None,
) -> sql.sql.StatementLambdaElement:
    """Generate a statement to fetch metadata."""
    stmt = sql.lambda_stmt(lambda: sql.select(*_QUERY_STATISTIC_META))
    if statistic_ids is not None:
        stmt += lambda q: q.where(model.StatisticsMeta.statistic_id.in_(statistic_ids))
    if statistic_source is not None:
        stmt += lambda q: q.where(model.StatisticsMeta.source == statistic_source)
    if statistic_type == "mean":
        stmt += lambda q: q.where(model.StatisticsMeta.has_mean == sql.true())
    elif statistic_type == "sum":
        stmt += lambda q: q.where(model.StatisticsMeta.has_sum == sql.true())
    return stmt


def get_metadata_with_session(
    session: sql_orm.Session,
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

    # Fetch metatadata from the database
    stmt = _generate_get_metadata_stmt(statistic_ids, statistic_type, statistic_source)
    result = util.execute_stmt_lambda_element(session, stmt)
    if not result:
        return {}

    return {
        meta["statistic_id"]: (
            meta["id"],
            {
                "source": meta["source"],
                "statistic_id": meta["statistic_id"],
                "unit_of_measurement": meta["unit_of_measurement"],
                "has_mean": meta["has_mean"],
                "has_sum": meta["has_sum"],
                "name": meta["name"],
            },
        )
        for meta in result
    }


def get_metadata(
    rec_comp: RecorderComponent,
    *,
    statistic_ids: list[str] | tuple[str] = None,
    statistic_type: typing.Literal["mean"] | typing.Literal["sum"] = None,
    statistic_source: str = None,
) -> dict[str, tuple[int, _statistic.MetaData]]:
    """Return metadata for statistic_ids."""
    with util.session_scope(rc=rec_comp) as session:
        return get_metadata_with_session(
            session,
            statistic_ids=statistic_ids,
            statistic_type=statistic_type,
            statistic_source=statistic_source,
        )


@typing.overload
def _configured_unit(unit: None, units: core.UnitSystem) -> None:
    ...


@typing.overload
def _configured_unit(unit: str, units: core.UnitSystem) -> str:
    ...


def _configured_unit(unit: str, units: core.UnitSystem) -> str:
    """Return the pressure and temperature units configured by the user."""
    if unit == core.Const.UnitOfPressure.PA:
        return units.pressure_unit
    if unit == core.Const.UnitOfTemperature.CELSIUS:
        return units.temperature_unit
    if unit == core.Const.UnitOfVolume.CUBIC_METERS:
        return units.volume_unit
    return unit


def clear_statistics(instance: Recorder, statistic_ids: list[str]) -> None:
    """Clear statistics for a list of statistic_ids."""
    with util.session_scope(session=instance.get_session()) as session:
        session.query(model.StatisticsMeta).filter(
            model.StatisticsMeta.statistic_id.in_(statistic_ids)
        ).delete(synchronize_session=False)


def update_statistics_metadata(
    instance: Recorder,
    statistic_id: str,
    new_statistic_id: str | object = _UNDEFINED,
    new_unit_of_measurement: str | object = _UNDEFINED,
) -> None:
    """Update statistics metadata for a statistic_id."""
    if new_unit_of_measurement is not _UNDEFINED:
        with util.session_scope(session=instance.get_session()) as session:
            session.query(model.StatisticsMeta).filter(
                model.StatisticsMeta.statistic_id == statistic_id
            ).update(
                {model.StatisticsMeta.unit_of_measurement: new_unit_of_measurement}
            )
    if new_statistic_id is not _UNDEFINED:
        with util.session_scope(
            session=instance.get_session(),
            exception_filter=_filter_unique_constraint_integrity_error(instance),
        ) as session:
            session.query(model.StatisticsMeta).filter(
                (model.StatisticsMeta.statistic_id == statistic_id)
                & (model.StatisticsMeta.source == instance.owner.domain)
            ).update({model.StatisticsMeta.statistic_id: new_statistic_id})


def list_statistic_ids(
    recorder: RecorderComponent,
    statistic_ids: list[str] | tuple[str] = None,
    statistic_type: typing.Literal["mean"] | typing.Literal["sum"] = None,
) -> list[dict]:
    """Return all statistic_ids (or filtered one) and unit of measurement.

    Queries the database for existing statistic_ids, as well as integrations with
    a recorder platform for statistic_ids which will be added in the next statistics
    period.
    """
    result = {}

    # Query the database
    with util.session_scope(rc=recorder) as session:
        metadata = get_metadata_with_session(
            session, statistic_type=statistic_type, statistic_ids=statistic_ids
        )

        result = {
            meta["statistic_id"]: {
                "has_mean": meta["has_mean"],
                "has_sum": meta["has_sum"],
                "name": meta["name"],
                "source": meta["source"],
                "unit_class": _get_unit_class(meta["unit_of_measurement"]),
                "unit_of_measurement": meta["unit_of_measurement"],
            }
            for _, meta in metadata.values()
        }

    # Query all integrations with a registered recorder platform
    for platform in recorder.platforms:
        if not platform.supports_statistics:
            continue
        platform_statistic_ids = platform.list_statistic_ids(
            recorder, statistic_ids=statistic_ids, statistic_type=statistic_type
        )

        for key, meta in platform_statistic_ids.items():
            if key in result:
                continue
            result[key] = {
                "has_mean": meta["has_mean"],
                "has_sum": meta["has_sum"],
                "name": meta["name"],
                "source": meta["source"],
                "unit_class": _get_unit_class(meta["unit_of_measurement"]),
                "unit_of_measurement": meta["unit_of_measurement"],
            }

    # Return a list of statistic_id + metadata
    return [
        {
            "statistic_id": _id,
            "has_mean": info["has_mean"],
            "has_sum": info["has_sum"],
            "name": info.get("name"),
            "source": info["source"],
            "statistics_unit_of_measurement": info["unit_of_measurement"],
            "unit_class": info["unit_class"],
        }
        for _id, info in result.items()
    ]


def _reduce_statistics(
    stats: dict[str, list[dict[str, typing.Any]]],
    same_period: collections.abc.Callable[[dt.datetime, dt.datetime], bool],
    period_start_end: collections.abc.Callable[
        [dt.datetime], tuple[dt.datetime, dt.datetime]
    ],
    period: dt.timedelta,
    types: set[typing.Literal["last_reset", "max", "mean", "min", "state", "sum"]],
) -> dict[str, list[dict[str, typing.Any]]]:
    """Reduce hourly statistics to daily or monthly statistics."""
    result: dict[str, list[dict[str, typing.Any]]] = collections.defaultdict(list)
    for statistic_id, stat_list in stats.items():
        max_values: list[float] = []
        mean_values: list[float] = []
        min_values: list[float] = []
        prev_stat: dict[str, typing.Any] = stat_list[0]

        # Loop over the hourly statistics + a fake entry to end the period
        for statistic in it.chain(
            stat_list, ({"start": stat_list[-1]["start"] + period},)
        ):
            if not same_period(prev_stat["start"], statistic["start"]):
                start, end = period_start_end(prev_stat["start"])
                # The previous statistic was the last entry of the period
                row = {
                    "start": start,
                    "end": end,
                }
                if "mean" in types:
                    row["mean"] = statistics.mean(mean_values) if mean_values else None
                if "min" in types:
                    row["min"] = min(min_values) if min_values else None
                if "max" in types:
                    row["max"] = max(max_values) if max_values else None
                if "last_reset" in types:
                    row["last_reset"] = prev_stat.get("last_reset")
                if "state" in types:
                    row["state"] = prev_stat.get("state")
                if "sum" in types:
                    row["sum"] = prev_stat["sum"]
                result[statistic_id].append(row)

                max_values = []
                mean_values = []
                min_values = []
            if statistic.get("max") is not None:
                max_values.append(statistic["max"])
            if statistic.get("mean") is not None:
                mean_values.append(statistic["mean"])
            if statistic.get("min") is not None:
                min_values.append(statistic["min"])
            prev_stat = statistic

    return result


def same_day(time1: dt.datetime, time2: dt.datetime) -> bool:
    """Return True if time1 and time2 are in the same date."""
    date1 = core.helpers.as_local(time1).date()
    date2 = core.helpers.as_local(time2).date()
    return date1 == date2


def day_start_end(
    time: dt.datetime,
) -> tuple[dt.datetime, dt.datetime]:
    """Return the start and end of the period (day) time is within."""
    start = core.helpers.as_utc(
        core.helpers.as_local(time).replace(hour=0, minute=0, second=0, microsecond=0)
    )
    end = start + dt.timedelta(days=1)
    return (start, end)


def _reduce_statistics_per_day(
    stats: dict[str, list[dict[str, typing.Any]]],
    types: set[typing.Literal["last_reset", "max", "mean", "min", "state", "sum"]],
) -> dict[str, list[dict[str, typing.Any]]]:
    """Reduce hourly statistics to daily statistics."""

    return _reduce_statistics(
        stats, same_day, day_start_end, dt.timedelta(days=1), types
    )


def reduce_week_factory() -> (
    tuple[
        typing.Callable[[dt.datetime, dt.datetime], bool],
        typing.Callable[[float], tuple[float, float]],
    ]
):
    """Return functions to match same week and week start end."""
    _boundaries: tuple[dt.datetime, dt.datetime] = (None, None)

    def _same_week(time1: dt.datetime, time2: dt.datetime) -> bool:
        """Return True if time1 and time2 are in the same year and week."""
        nonlocal _boundaries
        time1 = core.helpers.as_local(time1)
        time2 = core.helpers.as_local(time2)
        if (
            _boundaries[0] is None
            or _boundaries[1] is None
            or not _boundaries[0] <= time1 < _boundaries[1]
        ):
            _boundaries = _week_start_end_cached(time1)
        return _boundaries[0] <= time2 < _boundaries[1]

    def _week_start_end(time: dt.datetime) -> tuple[dt.datetime, dt.datetime]:
        """Return the start and end of the period (week) time is within."""
        nonlocal _boundaries
        time_local = core.helpers.as_local(time)
        start_local = time_local.replace(
            hour=0, minute=0, second=0, microsecond=0
        ) - dt.timedelta(days=time_local.weekday())
        return (
            start_local,
            (start_local + dt.timedelta(days=7)),
        )

    # We create _week_start_end_ts_cached in the closure in case the timezone changes
    _week_start_end_cached = ft.lru_cache(maxsize=6)(_week_start_end)

    return _same_week, _week_start_end_cached


def _reduce_statistics_per_week(
    stats: dict[str, list[dict[str, typing.Any]]],
    types: set[typing.Literal["last_reset", "max", "mean", "min", "state", "sum"]],
) -> dict[str, list[dict[str, typing.Any]]]:
    """Reduce hourly statistics to weekly statistics."""
    _same_week, _week_start_end = reduce_week_factory()
    return _reduce_statistics(
        stats, _same_week, _week_start_end, dt.timedelta(days=7), types
    )


def same_month(time1: dt.datetime, time2: dt.datetime) -> bool:
    """Return True if time1 and time2 are in the same year and month."""
    date1 = core.helpers.as_local(time1).date()
    date2 = core.helpers.as_local(time2).date()
    return (date1.year, date1.month) == (date2.year, date2.month)


def month_start_end(
    time: dt.datetime,
) -> tuple[dt.datetime, dt.datetime]:
    """Return the start and end of the period (month) time is within."""
    start_local = core.helpers.as_local(time).replace(
        day=1, hour=0, minute=0, second=0, microsecond=0
    )
    start = core.helpers.as_utc(start_local)
    end_local = (start_local + dt.timedelta(days=31)).replace(day=1)
    end = core.helpers.as_utc(end_local)
    return (start, end)


def _reduce_statistics_per_month(
    stats: dict[str, list[dict[str, typing.Any]]],
    types: set[typing.Literal["last_reset", "max", "mean", "min", "state", "sum"]],
) -> dict[str, list[dict[str, typing.Any]]]:
    """Reduce hourly statistics to monthly statistics."""

    return _reduce_statistics(
        stats, same_month, month_start_end, dt.timedelta(days=31), types
    )


_type_column_mapping: typing.Final = {
    "last_reset": "last_reset",
    "max": "max",
    "mean": "mean",
    "min": "min",
    "state": "state",
    "sum": "sum",
}


def _generate_select_columns_for_types_stmt(
    table: type[model.StatisticsBase],
    types: set[typing.Literal["last_reset", "max", "mean", "min", "state", "sum"]],
) -> sql.sql.StatementLambdaElement:
    columns = sql.select(table.metadata_id, table.start)
    track_on: list[str | None] = [
        table.__tablename__,  # type: ignore[attr-defined]
    ]
    for key, column in _type_column_mapping.items():
        if key in types:
            columns = columns.add_columns(getattr(table, column))
            track_on.append(column)
        else:
            track_on.append(None)
    return sql.lambda_stmt(lambda: columns, track_on=track_on)


def _statistics_during_period_stmt(
    start_time: dt.datetime,
    end_time: dt.datetime,
    metadata_ids: list[int],
    table: type[model.Statistics | model.StatisticsShortTerm],
    types: set[typing.Literal["last_reset", "max", "mean", "min", "state", "sum"]],
) -> sql.sql.StatementLambdaElement:
    """Prepare a database query for statistics during a given period.

    This prepares a lambda_stmt query, so we don't insert the parameters yet.
    """
    stmt = _generate_select_columns_for_types_stmt(table, types)
    stmt += lambda q: q.filter(table.start >= start_time)
    if end_time is not None:
        stmt += lambda q: q.filter(table.start < end_time)
    if metadata_ids:
        stmt += lambda q: q.filter(
            # https://github.com/python/mypy/issues/2608
            table.metadata_id.in_(metadata_ids)  # type:ignore[arg-type]
        )
    stmt += lambda q: q.order_by(table.metadata_id, table.start)
    return stmt


def _extract_metadata_and_discard_impossible_columns(
    metadata: dict[str, tuple[int, _statistic.MetaData]],
    types: set[typing.Literal["last_reset", "max", "mean", "min", "state", "sum"]],
) -> list[int]:
    """Extract metadata ids from metadata and discard impossible columns."""
    metadata_ids = []
    has_mean = False
    has_sum = False
    for metadata_id, stats_metadata in metadata.values():
        metadata_ids.append(metadata_id)
        has_mean |= stats_metadata["has_mean"]
        has_sum |= stats_metadata["has_sum"]
    if not has_mean:
        types.discard("mean")
        types.discard("min")
        types.discard("max")
    if not has_sum:
        types.discard("sum")
        types.discard("state")
    return metadata_ids


def _find_month_end_time(timestamp: dt.datetime) -> dt.datetime:
    """Return the end of the month (midnight at the first day of the next month)."""
    # We add 4 days to the end to make sure we are in the next month
    return (timestamp.replace(day=28) + dt.timedelta(days=4)).replace(
        day=1, hour=0, minute=0, second=0, microsecond=0
    )


def _augment_result_with_change(
    rec_comp: RecorderComponent,
    session: sql_orm.Session,
    start_time: dt.datetime,
    units: dict[str, str] | None,
    types: set[
        typing.Literal["change", "last_reset", "max", "mean", "min", "state", "sum"]
    ],
    table: type[model.Statistics | model.StatisticsShortTerm],
    metadata: dict[str, tuple[int, _statistic.MetaData]],
    result: dict[str, list[dict[str, typing.Any]]],
) -> None:
    """Add change to the result."""
    drop_sum = "sum" not in types
    prev_sums = {}
    if tmp := _statistics_at_time(
        session,
        {metadata[statistic_id][0] for statistic_id in result},
        table,
        start_time,
    ):
        _metadata = dict(metadata.values())
        for row in tmp:
            metadata_by_id = _metadata[row.metadata_id]
            statistic_id = metadata_by_id["statistic_id"]

            state_unit = unit = metadata_by_id["unit_of_measurement"]
            if state := rec_comp.controller.states.get(statistic_id):
                state_unit = state.attributes.get(core.Const.ATTR_UNIT_OF_MEASUREMENT)
            convert = _get_statistic_to_display_unit_converter(unit, state_unit, units)

            if convert is not None:
                prev_sums[statistic_id] = convert(row.sum)
            else:
                prev_sums[statistic_id] = row.sum

    for statistic_id, rows in result.items():
        prev_sum = prev_sums.get(statistic_id) or 0
        for statistics_row in rows:
            if "sum" not in statistics_row:
                continue
            if drop_sum:
                _sum = statistics_row.pop("sum")
            else:
                _sum = statistics_row["sum"]
            if _sum is None:
                statistics_row["change"] = None
                continue
            statistics_row["change"] = _sum - prev_sum
            prev_sum = _sum


def statistics_during_period(
    rec_comp: RecorderComponent,
    start_time: dt.datetime,
    end_time: dt.datetime,
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
    metadata = None
    with util.session_scope(rc=rec_comp) as session:
        # Fetch metadata for the given (or all) statistic_ids
        metadata = get_metadata_with_session(session, statistic_ids=statistic_ids)
        if not metadata:
            return {}

        _types: set[
            typing.Literal["last_reset", "max", "mean", "min", "state", "sum"]
        ] = set()
        for stat_type in types:
            if stat_type == "change":
                _types.add("sum")
                continue
            _types.add(stat_type)

        metadata_ids = None
        if statistic_ids is not None:
            metadata_ids = _extract_metadata_and_discard_impossible_columns(
                metadata, _types
            )

        # Align start_time and end_time with the period
        if period == "day":
            start_time = core.helpers.as_local(start_time).replace(
                hour=0, minute=0, second=0, microsecond=0
            )
            start_time = start_time.replace()
            if end_time is not None:
                end_local = core.helpers.as_local(end_time)
                end_time = end_local.replace(
                    hour=0, minute=0, second=0, microsecond=0
                ) + dt.timedelta(days=1)
        elif period == "week":
            start_local = core.helpers.as_local(start_time)
            start_time = start_local.replace(
                hour=0, minute=0, second=0, microsecond=0
            ) - dt.timedelta(days=start_local.weekday())
            if end_time is not None:
                end_local = core.helpers.as_local(end_time)
                end_time = (
                    end_local.replace(hour=0, minute=0, second=0, microsecond=0)
                    - dt.timedelta(days=end_local.weekday())
                    + dt.timedelta(days=7)
                )
        elif period == "month":
            start_time = core.helpers.as_local(start_time).replace(
                day=1, hour=0, minute=0, second=0, microsecond=0
            )
            if end_time is not None:
                end_time = _find_month_end_time(core.helpers.as_local(end_time))

        if period == "5minute":
            table = model.StatisticsShortTerm
        else:
            table = model.Statistics

        stmt = _statistics_during_period_stmt(
            start_time, end_time, metadata_ids, table, _types
        )
        stats = util.execute_stmt_lambda_element(session, stmt)

        if not stats:
            return {}

        result = _sorted_statistics_to_dict(
            rec_comp,
            session,
            stats,
            statistic_ids,
            metadata,
            True,
            table,
            start_time,
            units,
            _types,
        )

    if period == "day":
        result = _reduce_statistics_per_day(result, _types)

    elif period == "week":
        result = _reduce_statistics_per_week(result, _types)

    elif period == "month":
        result = _reduce_statistics_per_month(result, _types)

    if "change" in types:
        _augment_result_with_change(
            rec_comp, session, start_time, units, types, table, metadata, result
        )

    # Return statistics combined with metadata
    return result


def _get_last_statistics_stmt(
    metadata_id: int,
    number_of_stats: int,
) -> sql.sql.StatementLambdaElement:
    """Generate a statement for number_of_stats statistics for a given statistic_id."""
    return sql.lambda_stmt(
        lambda: sql.select(*_QUERY_STATISTICS)
        .filter_by(metadata_id=metadata_id)
        .order_by(model.Statistics.metadata_id, model.Statistics.start.desc())
        .limit(number_of_stats)
    )


def _get_last_statistics_short_term_stmt(
    metadata_id: int,
    number_of_stats: int,
) -> sql.sql.StatementLambdaElement:
    """Generate a statement for number_of_stats short term statistics for a given statistic_id."""
    return sql.lambda_stmt(
        lambda: sql.select(*_QUERY_STATISTICS_SHORT_TERM)
        .filter_by(metadata_id=metadata_id)
        .order_by(
            model.StatisticsShortTerm.metadata_id,
            model.StatisticsShortTerm.start.desc(),
        )
        .limit(number_of_stats)
    )


def _get_last_statistics(
    rec_comp: RecorderComponent,
    number_of_stats: int,
    statistic_id: str,
    convert_units: bool,
    table: type[model.Statistics | model.StatisticsShortTerm],
    types: set[typing.Literal["last_reset", "max", "mean", "min", "state", "sum"]],
) -> dict[str, list[dict]]:
    """Return the last number_of_stats statistics for a given statistic_id."""
    statistic_ids = [statistic_id]
    with util.session_scope(rc=rec_comp) as session:
        # Fetch metadata for the given statistic_id
        metadata = get_metadata_with_session(session, statistic_ids=statistic_ids)
        if not metadata:
            return {}
        metadata_id = metadata[statistic_id][0]
        if table == model.Statistics:
            stmt = _get_last_statistics_stmt(metadata_id, number_of_stats)
        else:
            stmt = _get_last_statistics_short_term_stmt(metadata_id, number_of_stats)
        stats = util.execute_stmt_lambda_element(session, stmt)

        if not stats:
            return {}

        # Return statistics combined with metadata
        return _sorted_statistics_to_dict(
            rec_comp,
            session,
            stats,
            statistic_ids,
            metadata,
            convert_units,
            table,
            None,
            None,
            types,
        )


def get_last_statistics(
    rec_comp: RecorderComponent,
    number_of_stats: int,
    statistic_id: str,
    convert_units: bool,
    types: set[typing.Literal["last_reset", "max", "mean", "min", "state", "sum"]],
) -> dict[str, list[dict]]:
    """Return the last number_of_stats statistics for a statistic_id."""
    return _get_last_statistics(
        rec_comp, number_of_stats, statistic_id, convert_units, model.Statistics, types
    )


def get_last_short_term_statistics(
    rec_comp: RecorderComponent,
    number_of_stats: int,
    statistic_id: str,
    convert_units: bool,
    types: set[typing.Literal["last_reset", "max", "mean", "min", "state", "sum"]],
) -> dict[str, list[dict]]:
    """Return the last number_of_stats short term statistics for a statistic_id."""
    return _get_last_statistics(
        rec_comp,
        number_of_stats,
        statistic_id,
        convert_units,
        model.StatisticsShortTerm,
        types,
    )


def _latest_short_term_statistics_stmt(
    metadata_ids: list[int],
) -> sql.sql.StatementLambdaElement:
    """Create the statement for finding the latest short term stat rows."""
    stmt = sql.lambda_stmt(lambda: sql.select(*_QUERY_STATISTICS_SHORT_TERM))
    most_recent_statistic_row = (
        sql.select(
            model.StatisticsShortTerm.metadata_id,
            sql.func.max(model.StatisticsShortTerm.start).label("start_max"),
        )
        .where(model.StatisticsShortTerm.metadata_id.in_(metadata_ids))
        .group_by(model.StatisticsShortTerm.metadata_id)
    ).subquery()
    stmt += lambda s: s.join(
        most_recent_statistic_row,
        (
            # pylint: disable=comparison-with-callable
            model.StatisticsShortTerm.metadata_id
            == most_recent_statistic_row.c.metadata_id
        )
        & (model.StatisticsShortTerm.start == most_recent_statistic_row.c.start_max),
    )
    return stmt


def get_latest_short_term_statistics(
    rec_comp: RecorderComponent,
    statistic_ids: list[str],
    types: set[typing.Literal["last_reset", "max", "mean", "min", "state", "sum"]],
    metadata: dict[str, tuple[int, _statistic.MetaData]] = None,
) -> dict[str, list[dict]]:
    """Return the latest short term statistics for a list of statistic_ids."""
    with util.session_scope(rc=rec_comp) as session:
        # Fetch metadata for the given statistic_ids
        if not metadata:
            metadata = get_metadata_with_session(session, statistic_ids=statistic_ids)
        if not metadata:
            return {}
        metadata_ids = [
            metadata[statistic_id][0]
            for statistic_id in statistic_ids
            if statistic_id in metadata
        ]
        stmt = _latest_short_term_statistics_stmt(metadata_ids)
        stats = util.execute_stmt_lambda_element(session, stmt)
        if not stats:
            return {}

        # Return statistics combined with metadata
        return _sorted_statistics_to_dict(
            rec_comp,
            session,
            stats,
            statistic_ids,
            metadata,
            False,
            model.StatisticsShortTerm,
            None,
            None,
            types,
        )


def _statistics_at_time(
    session: sql_orm.Session,
    metadata_ids: set[int],
    table: type[model.Statistics | model.StatisticsShortTerm],
    start_time: dt.datetime,
) -> list:
    """Return last known statistics, earlier than start_time, for the metadata_ids."""
    # Fetch metadata for the given (or all) statistic_ids
    if table == model.StatisticsShortTerm:
        base_query = _QUERY_STATISTICS_SHORT_TERM
    else:
        base_query = _QUERY_STATISTICS

    query = session.query(*base_query)

    most_recent_statistic_ids = (
        session.query(
            sql.func.max(table.id).label("max_id"),
        )
        .filter(table.start < start_time)
        .filter(table.metadata_id.in_(metadata_ids))
    )
    most_recent_statistic_ids = most_recent_statistic_ids.group_by(table.metadata_id)
    most_recent_statistic_ids = most_recent_statistic_ids.subquery()
    query = query.join(
        most_recent_statistic_ids,
        table.id == most_recent_statistic_ids.c.max_id,
    )

    return util.execute(query)


def _sorted_statistics_to_dict(
    rec_comp: RecorderComponent,
    session: sql_orm.Session,
    stats: collections.abc.Iterable[sql.engine.Row],
    statistic_ids: list[str],
    _metadata: dict[str, tuple[int, _statistic.MetaData]],
    convert_units: bool,
    table: type[model.Statistics | model.StatisticsShortTerm],
    start_time: dt.datetime,
    units: dict[str, str],
    types: set[typing.Literal["last_reset", "max", "mean", "min", "state", "sum"]],
) -> dict[str, list[dict]]:
    """Convert SQL results into JSON friendly data structure."""
    result: dict = collections.defaultdict(list)
    metadata = dict(_metadata.values())
    need_stat_at_start_time: set[int] = set()
    stats_at_start_time = {}

    def no_conversion(val: float) -> float:
        """Return x."""
        return val  # type: ignore[no-any-return]

    # Set all statistic IDs to empty lists in result set to maintain the order
    if statistic_ids is not None:
        for stat_id in statistic_ids:
            result[stat_id] = []

    # Identify metadata IDs for which no data was available at the requested start time
    for meta_id, group in it.groupby(stats, lambda stat: stat.metadata_id):
        first_start_time = model.process_timestamp(next(group).start)
        if start_time and first_start_time > start_time:
            need_stat_at_start_time.add(meta_id)

    # Fetch last known statistics for the needed metadata IDs
    if need_stat_at_start_time:
        assert start_time  # Can not be None if need_stat_at_start_time is not empty
        tmp = _statistics_at_time(session, need_stat_at_start_time, table, start_time)
        if tmp:
            for stat in tmp:
                stats_at_start_time[stat.metadata_id] = (stat,)

    # Append all statistic entries, and optionally do unit conversion
    for meta_id, group in it.groupby(stats, lambda stat: stat.metadata_id):
        state_unit = unit = metadata[meta_id]["unit_of_measurement"]
        statistic_id = metadata[meta_id]["statistic_id"]
        if state := rec_comp.controller.states.get(statistic_id):
            state_unit = state.attributes.get(core.Const.ATTR_UNIT_OF_MEASUREMENT)
        if unit is not None and convert_units:
            convert = _get_statistic_to_display_unit_converter(unit, state_unit, units)
        else:
            convert = no_conversion
        ent_results = result[meta_id]
        for db_state in it.chain(stats_at_start_time.get(meta_id, ()), group):
            start = model.process_timestamp(db_state.start)
            end = start + table.duration
            row = {
                "start": start,
                "end": end,
            }
            if "mean" in types:
                row["mean"] = convert(db_state.mean)
            if "min" in types:
                row["min"] = convert(db_state.min)
            if "max" in types:
                row["max"] = convert(db_state.max)
            if "last_reset" in types:
                row["last_reset"] = model.process_timestamp(db_state.last_reset)
            if "state" in types:
                row["state"] = convert(db_state.state)
            if "sum" in types:
                row["sum"] = convert(db_state.sum)

            ent_results.append(row)

    # Filter out the empty lists if some states had 0 results.
    return {metadata[key]["statistic_id"]: val for key, val in result.items() if val}


def validate_statistics(
    rec_comp: RecorderComponent,
) -> dict[str, list[ValidationIssue]]:
    """Validate statistics."""
    platform_validation: dict[str, list[ValidationIssue]] = {}
    for platform in rec_comp.platforms:
        if not platform.supports_validate_statistics:
            continue
        platform_validation.update(platform.validate_statistics(rec_comp))
    return platform_validation


def _statistics_exists(
    session: sql_orm.Session,
    table: type[model.Statistics | model.StatisticsShortTerm],
    metadata_id: int,
    start: dt.datetime,
) -> int:
    """Return id if a statistics entry already exists."""
    result = (
        session.query(table.id)
        .filter((table.metadata_id == metadata_id) & (table.start == start))
        .first()
    )
    return result["id"] if result else None


@core.callback
def async_add_external_statistics(
    rec_comp: RecorderComponent,
    metadata: _statistic.MetaData,
    stats: collections.abc.Iterable[_statistic.Data],
) -> None:
    """Add hourly statistics from an external source.

    This inserts an add_external_statistics job in the recorder's queue.
    """
    # The statistic_id has same limitations as an entity_id, but with a ':' as separator
    if not valid_statistic_id(metadata["statistic_id"]):
        raise core.SmartHomeControllerError("Invalid statistic_id")

    # The source must not be empty and must be aligned with the statistic_id
    domain, _object_id = split_statistic_id(metadata["statistic_id"])
    if not metadata["source"] or metadata["source"] != domain:
        raise core.SmartHomeControllerError("Invalid source")

    for statistic in stats:
        start = statistic["start"]
        if start.tzinfo is None or start.tzinfo.utcoffset(start) is None:
            raise core.SmartHomeControllerError("Naive timestamp")
        if start.minute != 0 or start.second != 0 or start.microsecond != 0:
            raise core.SmartHomeControllerError("Invalid timestamp")
        statistic["start"] = core.helpers.as_utc(start)

    # Insert job in recorder's queue
    rec_comp.recorder.async_external_statistics(metadata, statistics)


def _filter_unique_constraint_integrity_error(
    instance: Recorder,
) -> collections.abc.Callable[[Exception], bool]:
    def _filter_unique_constraint_integrity_error(err: Exception) -> bool:
        """Handle unique constraint integrity errors."""
        if not isinstance(err, sql_exc.StatementError):
            return False

        assert instance.engine is not None
        dialect_name = instance.engine.dialect.name

        ignore = False
        if (
            dialect_name == Const.SupportedDialect.SQLITE
            and "UNIQUE constraint failed" in str(err)
        ):
            ignore = True
        if (
            dialect_name == Const.SupportedDialect.POSTGRESQL
            and hasattr(err.orig, "pgcode")
            and err.orig.pgcode == "23505"
        ):
            ignore = True
        if dialect_name == "mysql" and hasattr(err.orig, "args"):
            with contextlib.suppress(TypeError):
                if err.orig.args[0] == 1062:
                    ignore = True

        if ignore:
            rep_url = (
                "https://github.com/home-assistant/core/issues?q=is%3Aopen+is%3A"
                + "issue+label%3A%22integration%3A+recorder%22"
            )
            _LOGGER.warning(
                f"Blocked attempt to insert duplicated statistic rows, please report at {rep_url}",
                exc_info=err,
            )

        return ignore

    return _filter_unique_constraint_integrity_error


def add_external_statistics(
    instance: Recorder,
    metadata: _statistic.MetaData,
    stats: collections.abc.Iterable[_statistic.Data],
) -> bool:
    """Process an add_external_statistics job."""

    with util.session_scope(
        session=instance.get_session(),
        exception_filter=_filter_unique_constraint_integrity_error(instance),
    ) as session:
        old_metadata_dict = get_metadata_with_session(
            session, statistic_ids=[metadata["statistic_id"]]
        )
        metadata_id = _update_or_add_metadata(session, metadata, old_metadata_dict)
        for stat in stats:
            if stat_id := _statistics_exists(
                session, model.Statistics, metadata_id, stat["start"]
            ):
                _update_statistics(session, model.Statistics, stat_id, stat)
            else:
                _insert_statistics(session, model.Statistics, metadata_id, stat)

    return True


def adjust_statistics(
    instance: Recorder,
    statistic_id: str,
    start_time: dt.datetime,
    sum_adjustment: float,
    adjustment_unit: str,
) -> bool:
    """Process an add_statistics job."""

    with util.session_scope(session=instance.get_session()) as session:
        metadata = get_metadata_with_session(session, statistic_ids=(statistic_id,))
        if statistic_id not in metadata:
            return True

        statistic_unit = metadata[statistic_id][1]["unit_of_measurement"]
        convert = _get_display_to_statistic_unit_converter(
            adjustment_unit, statistic_unit
        )
        sum_adjustment = convert(sum_adjustment)

        _adjust_sum_statistics(
            session,
            model.StatisticsShortTerm,
            metadata[statistic_id][0],
            start_time,
            sum_adjustment,
        )

        _adjust_sum_statistics(
            session,
            model.Statistics,
            metadata[statistic_id][0],
            start_time.replace(minute=0),
            sum_adjustment,
        )

    return True
