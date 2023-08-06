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

import collections
import collections.abc
import datetime
import itertools as it
import logging
import time
import typing

import sqlalchemy as sql
import sqlalchemy.engine as sql_engine
import sqlalchemy.orm as sql_orm

from ... import core
from . import model, util
from .filters import Filters

if not typing.TYPE_CHECKING:

    class RecorderComponent:
        ...


if typing.TYPE_CHECKING:
    from .recorder_component import RecorderComponent

_LOGGER: typing.Final = logging.getLogger(__name__)
_STATE_KEY: typing.Final = "state"
_LAST_CHANGED_KEY = "last_changed"

_SIGNIFICANT_DOMAINS: typing.Final = {
    "climate",
    "device_tracker",
    "humidifier",
    "thermostat",
    "water_heater",
}
_SIGNIFICANT_DOMAINS_ENTITY_ID_LIKE: typing.Final = [
    f"{domain}.%" for domain in _SIGNIFICANT_DOMAINS
]
_IGNORE_DOMAINS: typing.Final = {"zone", "scene"}
_IGNORE_DOMAINS_ENTITY_ID_LIKE: typing.Final = [
    f"{domain}.%" for domain in _IGNORE_DOMAINS
]
_NEED_ATTRIBUTE_DOMAINS: typing.Final = {
    "climate",
    "humidifier",
    "input_datetime",
    "thermostat",
    "water_heater",
}

_BASE_STATES: typing.Final = [
    model.States.entity_id,
    model.States.state,
    model.States.last_changed,
    model.States.last_updated,
]
_BASE_STATES_NO_LAST_CHANGED: typing.Final = [
    model.States.entity_id,
    model.States.state,
    sql.literal(value=None, type_=sql.Text).label("last_changed"),
    model.States.last_updated,
]
_QUERY_STATE_NO_ATTR: typing.Final = [
    *_BASE_STATES,
    sql.literal(value=None, type_=sql.Text).label("attributes"),
    sql.literal(value=None, type_=sql.Text).label("shared_attrs"),
]
_QUERY_STATE_NO_ATTR_NO_LAST_CHANGED: typing.Final = [
    *_BASE_STATES_NO_LAST_CHANGED,
    sql.literal(value=None, type_=sql.Text).label("attributes"),
    sql.literal(value=None, type_=sql.Text).label("shared_attrs"),
]
# Remove QUERY_STATES_PRE_SCHEMA_25
# and the migration_in_progress check
# once schema 26 is created
_QUERY_STATES_PRE_SCHEMA_25: typing.Final = [
    *_BASE_STATES,
    model.States.attributes,
    sql.literal(value=None, type_=sql.Text).label("shared_attrs"),
]
_QUERY_STATES_PRE_SCHEMA_25_NO_LAST_CHANGED: typing.Final = [
    *_BASE_STATES_NO_LAST_CHANGED,
    model.States.attributes,
    sql.literal(value=None, type_=sql.Text).label("shared_attrs"),
]
_QUERY_STATES: typing.Final = [
    *_BASE_STATES,
    # Remove States.attributes once all attributes are in StateAttributes.shared_attrs
    model.States.attributes,
    model.StateAttributes.shared_attrs,
]
_QUERY_STATES_NO_LAST_CHANGED: typing.Final = [
    *_BASE_STATES_NO_LAST_CHANGED,
    # Remove States.attributes once all attributes are in StateAttributes.shared_attrs
    model.States.attributes,
    model.StateAttributes.shared_attrs,
]

# pylint: disable=unused-variable


def _schema_version(rec_comp: RecorderComponent) -> int:
    return rec_comp.recorder.schema_version


def lambda_stmt_and_join_attributes(
    schema_version: int, no_attributes: bool, include_last_changed: bool = True
) -> tuple[sql.sql.StatementLambdaElement, bool]:
    """Return the lambda_stmt and if StateAttributes should be joined.

    Because these are lambda_stmt the values inside the lambdas need
    to be explicitly written out to avoid caching the wrong values.
    """
    # If no_attributes was requested we do the query
    # without the attributes fields and do not join the
    # state_attributes table
    if no_attributes:
        if include_last_changed:
            return sql.lambda_stmt(lambda: sql.select(*_QUERY_STATE_NO_ATTR)), False
        return (
            sql.lambda_stmt(lambda: sql.select(*_QUERY_STATE_NO_ATTR_NO_LAST_CHANGED)),
            False,
        )
    # If we in the process of migrating schema we do
    # not want to join the state_attributes table as we
    # do not know if it will be there yet
    if schema_version < 25:
        if include_last_changed:
            return (
                sql.lambda_stmt(lambda: sql.select(*_QUERY_STATES_PRE_SCHEMA_25)),
                False,
            )
        return (
            sql.lambda_stmt(
                lambda: sql.select(*_QUERY_STATES_PRE_SCHEMA_25_NO_LAST_CHANGED)
            ),
            False,
        )
    # Finally if no migration is in progress and no_attributes
    # was not requested, we query both attributes columns and
    # join state_attributes
    if include_last_changed:
        return sql.lambda_stmt(lambda: sql.select(*_QUERY_STATES)), True
    return sql.lambda_stmt(lambda: sql.select(*_QUERY_STATES_NO_LAST_CHANGED)), True


def get_significant_states(
    rec_comp: RecorderComponent,
    start_time: datetime.datetime,
    end_time: datetime.datetime = None,
    entity_ids: list[str] = None,
    filters: Filters = None,
    include_start_time_state: bool = True,
    significant_changes_only: bool = True,
    minimal_response: bool = False,
    no_attributes: bool = False,
    compressed_state_format: bool = False,
) -> collections.abc.MutableMapping[str, list[core.State | dict[str, typing.Any]]]:
    """Wrap get_significant_states_with_session with an sql session."""
    with util.session_scope(rc=rec_comp) as session:
        return get_significant_states_with_session(
            rec_comp,
            session,
            start_time,
            end_time,
            entity_ids,
            filters,
            include_start_time_state,
            significant_changes_only,
            minimal_response,
            no_attributes,
            compressed_state_format,
        )


def _ignore_domains_filter(query: sql_orm.Query) -> sql_orm.Query:
    """Add a filter to ignore domains we do not fetch history for."""
    return query.filter(
        sql.and_(
            *[
                ~model.States.entity_id.like(entity_domain)
                for entity_domain in _IGNORE_DOMAINS_ENTITY_ID_LIKE
            ]
        )
    )


def _significant_states_stmt(
    schema_version: int,
    start_time: datetime.datetime,
    end_time: datetime.datetime,
    entity_ids: list[str],
    filters: Filters,
    significant_changes_only: bool,
    no_attributes: bool,
) -> sql.sql.StatementLambdaElement:
    """Query the database for significant state changes."""
    stmt, join_attributes = lambda_stmt_and_join_attributes(
        schema_version, no_attributes, include_last_changed=not significant_changes_only
    )
    if (
        entity_ids
        and len(entity_ids) == 1
        and significant_changes_only
        and core.helpers.split_entity_id(entity_ids[0])[0] not in _SIGNIFICANT_DOMAINS
    ):
        stmt += lambda q: q.filter(
            (model.States.last_changed == model.States.last_updated)
            | model.States.last_changed.is_(None)
        )
    elif significant_changes_only:
        stmt += lambda q: q.filter(
            sql.or_(
                *[
                    model.States.entity_id.like(entity_domain)
                    for entity_domain in _SIGNIFICANT_DOMAINS_ENTITY_ID_LIKE
                ],
                (
                    (model.States.last_changed == model.States.last_updated)
                    | model.States.last_changed.is_(None)
                ),
            )
        )

    if entity_ids:
        stmt += lambda q: q.filter(model.States.entity_id.in_(entity_ids))
    else:
        stmt += _ignore_domains_filter
        if filters and filters.has_config:
            entity_filter = filters.states_entity_filter()
            stmt = stmt.add_criteria(
                lambda q: q.filter(entity_filter), track_on=[filters]
            )

    stmt += lambda q: q.filter(model.States.last_updated > start_time)
    if end_time:
        stmt += lambda q: q.filter(model.States.last_updated < end_time)

    if join_attributes:
        stmt += lambda q: q.outerjoin(
            model.StateAttributes,
            model.States.attributes_id == model.StateAttributes.attributes_id,
        )
    stmt += lambda q: q.order_by(model.States.entity_id, model.States.last_updated)
    return stmt


def get_significant_states_with_session(
    rec_comp: RecorderComponent,
    session: sql_orm.Session,
    start_time: datetime.datetime,
    end_time: datetime.datetime = None,
    entity_ids: list[str] = None,
    filters: Filters = None,
    include_start_time_state: bool = True,
    significant_changes_only: bool = True,
    minimal_response: bool = False,
    no_attributes: bool = False,
    compressed_state_format: bool = False,
) -> collections.abc.MutableMapping[str, list[core.State | dict[str, typing.Any]]]:
    """
    Return states changes during UTC period start_time - end_time.

    entity_ids is an optional iterable of entities to include in the results.

    filters is an optional SQLAlchemy filter which will be applied to the database
    queries unless entity_ids is given, in which case its ignored.

    Significant states are all states where there is a state change,
    as well as all states from certain domains (for instance
    thermostat so that we get current temperature in our graphs).
    """
    stmt = _significant_states_stmt(
        _schema_version(rec_comp),
        start_time,
        end_time,
        entity_ids,
        filters,
        significant_changes_only,
        no_attributes,
    )
    states = util.execute_stmt_lambda_element(
        session, stmt, None if entity_ids else start_time, end_time
    )
    return _sorted_states_to_dict(
        rec_comp,
        session,
        states,
        start_time,
        entity_ids,
        filters,
        include_start_time_state,
        minimal_response,
        no_attributes,
        compressed_state_format,
    )


def get_full_significant_states_with_session(
    rec_comp: RecorderComponent,
    session: sql_orm.Session,
    start_time: datetime.datetime,
    end_time: datetime.datetime = None,
    entity_ids: list[str] = None,
    filters: Filters = None,
    include_start_time_state: bool = True,
    significant_changes_only: bool = True,
    no_attributes: bool = False,
) -> collections.abc.MutableMapping[str, list[core.State]]:
    """Variant of get_significant_states_with_session that does not return minimal responses."""
    return typing.cast(
        collections.abc.MutableMapping[str, list[core.State]],
        get_significant_states_with_session(
            rec_comp,
            session=session,
            start_time=start_time,
            end_time=end_time,
            entity_ids=entity_ids,
            filters=filters,
            include_start_time_state=include_start_time_state,
            significant_changes_only=significant_changes_only,
            minimal_response=False,
            no_attributes=no_attributes,
        ),
    )


def _state_changed_during_period_stmt(
    schema_version: int,
    start_time: datetime,
    end_time: datetime.datetime,
    entity_id: str,
    no_attributes: bool,
    descending: bool,
    limit: int,
) -> sql.sql.StatementLambdaElement:
    stmt, join_attributes = lambda_stmt_and_join_attributes(
        schema_version, no_attributes, include_last_changed=False
    )
    stmt += lambda q: q.filter(
        (
            (model.States.last_changed == model.States.last_updated)
            | model.States.last_changed.is_(None)
        )
        & (model.States.last_updated > start_time)
    )
    if end_time:
        stmt += lambda q: q.filter(model.States.last_updated < end_time)
    stmt += lambda q: q.filter(model.States.entity_id == entity_id)
    if join_attributes:
        stmt += lambda q: q.outerjoin(
            model.StateAttributes,
            model.States.attributes_id == model.StateAttributes.attributes_id,
        )
    if descending:
        stmt += lambda q: q.order_by(
            model.States.entity_id, model.States.last_updated.desc()
        )
    else:
        stmt += lambda q: q.order_by(model.States.entity_id, model.States.last_updated)
    if limit:
        stmt += lambda q: q.limit(limit)
    return stmt


def state_changes_during_period(
    rec_comp: RecorderComponent,
    start_time: datetime.datetime,
    end_time: datetime.datetime = None,
    entity_id: str = None,
    no_attributes: bool = False,
    descending: bool = False,
    limit: int = None,
    include_start_time_state: bool = True,
) -> collections.abc.MutableMapping[str, list[core.State]]:
    """Return states changes during UTC period start_time - end_time."""
    entity_id = entity_id.lower() if entity_id is not None else None

    with util.session_scope(rc=rec_comp) as session:
        stmt = _state_changed_during_period_stmt(
            _schema_version(rec_comp),
            start_time,
            end_time,
            entity_id,
            no_attributes,
            descending,
            limit,
        )
        states = util.execute_stmt_lambda_element(
            session, stmt, None if entity_id else start_time, end_time
        )
        entity_ids = [entity_id] if entity_id is not None else None

        return typing.cast(
            collections.abc.MutableMapping[str, list[core.State]],
            _sorted_states_to_dict(
                rec_comp,
                session,
                states,
                start_time,
                entity_ids,
                include_start_time_state=include_start_time_state,
            ),
        )


def _get_last_state_changes_stmt(
    schema_version: int, number_of_states: int, entity_id: str
) -> sql.sql.StatementLambdaElement:
    stmt, join_attributes = lambda_stmt_and_join_attributes(
        schema_version, False, include_last_changed=False
    )
    stmt += lambda q: q.filter(
        (model.States.last_changed == model.States.last_updated)
        | model.States.last_changed.is_(None)
    ).filter(model.States.entity_id == entity_id)
    if join_attributes:
        stmt += lambda q: q.outerjoin(
            model.StateAttributes,
            model.States.attributes_id == model.StateAttributes.attributes_id,
        )
    stmt += lambda q: q.order_by(
        model.States.entity_id, model.States.last_updated.desc()
    ).limit(number_of_states)
    return stmt


def get_last_state_changes(
    rec_comp: RecorderComponent, number_of_states: int, entity_id: str
) -> collections.abc.MutableMapping[str, list[core.State]]:
    """Return the last number_of_states."""
    start_time = core.helpers.utcnow()
    entity_id = entity_id.lower() if entity_id is not None else None

    with util.session_scope(rc=rec_comp) as session:
        stmt = _get_last_state_changes_stmt(
            _schema_version(rec_comp), number_of_states, entity_id
        )
        states = list(util.execute_stmt_lambda_element(session, stmt))
        entity_ids = [entity_id] if entity_id is not None else None

        return typing.cast(
            collections.abc.MutableMapping[str, list[core.State]],
            _sorted_states_to_dict(
                rec_comp,
                session,
                reversed(states),
                start_time,
                entity_ids,
                include_start_time_state=False,
            ),
        )


def _get_states_for_entities_stmt(
    schema_version: int,
    run_start: datetime,
    utc_point_in_time: datetime,
    entity_ids: list[str],
    no_attributes: bool,
) -> sql.sql.StatementLambdaElement:
    """Baked query to get states for specific entities."""
    stmt, join_attributes = lambda_stmt_and_join_attributes(
        schema_version, no_attributes, include_last_changed=True
    )
    # We got an include-list of entities, accelerate the query by filtering already
    # in the inner query.
    stmt += lambda q: q.where(
        model.States.state_id
        == (
            sql.select(sql.func.max(model.States.state_id).label("max_state_id"))
            .filter(
                (model.States.last_updated >= run_start)
                & (model.States.last_updated < utc_point_in_time)
            )
            .filter(model.States.entity_id.in_(entity_ids))
            .group_by(model.States.entity_id)
            .subquery()
        ).c.max_state_id
    )
    if join_attributes:
        stmt += lambda q: q.outerjoin(
            model.StateAttributes,
            (model.States.attributes_id == model.StateAttributes.attributes_id),
        )
    return stmt


def _get_states_for_all_stmt(
    schema_version: int,
    run_start: datetime,
    utc_point_in_time: datetime,
    filters: Filters,
    no_attributes: bool,
) -> sql.sql.StatementLambdaElement:
    """Baked query to get states for all entities."""
    stmt, join_attributes = lambda_stmt_and_join_attributes(
        schema_version, no_attributes, include_last_changed=True
    )
    # We did not get an include-list of entities, query all states in the inner
    # query, then filter out unwanted domains as well as applying the custom filter.
    # This filtering can't be done in the inner query because the domain column is
    # not indexed and we can't control what's in the custom filter.
    most_recent_states_by_date = (
        sql.select(
            model.States.entity_id.label("max_entity_id"),
            sql.func.max(model.States.last_updated).label("max_last_updated"),
        )
        .filter(
            (model.States.last_updated >= run_start)
            & (model.States.last_updated < utc_point_in_time)
        )
        .group_by(model.States.entity_id)
        .subquery()
    )
    stmt += lambda q: q.where(
        model.States.state_id
        == (
            sql.select(sql.func.max(model.States.state_id).label("max_state_id"))
            .join(
                most_recent_states_by_date,
                sql.and_(
                    model.States.entity_id
                    == most_recent_states_by_date.c.max_entity_id,
                    model.States.last_updated
                    == most_recent_states_by_date.c.max_last_updated,
                ),
            )
            .group_by(model.States.entity_id)
            .subquery()
        ).c.max_state_id,
    )
    stmt += _ignore_domains_filter
    if filters and filters.has_config:
        entity_filter = filters.states_entity_filter()
        stmt = stmt.add_criteria(lambda q: q.filter(entity_filter), track_on=[filters])
    if join_attributes:
        stmt += lambda q: q.outerjoin(
            model.StateAttributes,
            (model.States.attributes_id == model.StateAttributes.attributes_id),
        )
    return stmt


def _get_rows_with_session(
    rec_comp: RecorderComponent,
    session: sql_orm.Session,
    utc_point_in_time: datetime,
    entity_ids: list[str] = None,
    run: model.RecorderRuns = None,
    filters: Filters = None,
    no_attributes: bool = False,
) -> collections.abc.Iterable[sql_engine.Row]:
    """Return the states at a specific point in time."""
    schema_version = _schema_version(rec_comp)
    if entity_ids and len(entity_ids) == 1:
        return util.execute_stmt_lambda_element(
            session,
            _get_single_entity_states_stmt(
                schema_version, utc_point_in_time, entity_ids[0], no_attributes
            ),
        )

    if run is None:
        run = rec_comp.recorder.run_history.get(utc_point_in_time)

    if run is None or model.process_timestamp(run.start) > utc_point_in_time:
        # History did not run before utc_point_in_time
        return []

    # We have more than one entity to look at so we need to do a query on states
    # since the last recorder run started.
    if entity_ids:
        stmt = _get_states_for_entities_stmt(
            schema_version, run.start, utc_point_in_time, entity_ids, no_attributes
        )
    else:
        stmt = _get_states_for_all_stmt(
            schema_version, run.start, utc_point_in_time, filters, no_attributes
        )

    return util.execute_stmt_lambda_element(session, stmt)


def _get_single_entity_states_stmt(
    schema_version: int,
    utc_point_in_time: datetime,
    entity_id: str,
    no_attributes: bool = False,
) -> sql.sql.StatementLambdaElement:
    # Use an entirely different (and extremely fast) query if we only
    # have a single entity id
    stmt, join_attributes = lambda_stmt_and_join_attributes(
        schema_version, no_attributes, include_last_changed=True
    )
    stmt += (
        lambda q: q.filter(
            model.States.last_updated < utc_point_in_time,
            model.States.entity_id == entity_id,
        )
        .order_by(model.States.last_updated.desc())
        .limit(1)
    )
    if join_attributes:
        stmt += lambda q: q.outerjoin(
            model.StateAttributes,
            model.States.attributes_id == model.StateAttributes.attributes_id,
        )
    return stmt


def _sorted_states_to_dict(
    rec_comp: RecorderComponent,
    session: sql_orm.Session,
    states: collections.abc.Iterable[sql_engine.Row],
    start_time: datetime.datetime,
    entity_ids: list[str],
    filters: Filters = None,
    include_start_time_state: bool = True,
    minimal_response: bool = False,
    no_attributes: bool = False,
    compressed_state_format: bool = False,
) -> collections.abc.MutableMapping[str, list[core.State | dict[str, typing.Any]]]:
    """Convert SQL results into JSON friendly data structure.

    This takes our state list and turns it into a JSON friendly data
    structure {'entity_id': [list of states], 'entity_id2': [list of states]}

    States must be sorted by entity_id and last_updated

    We also need to go back and create a synthetic zero data point for
    each list of states, otherwise our graphs won't start on the Y
    axis correctly.
    """
    if compressed_state_format:
        state_class = model.row_to_compressed_state
        _process_timestamp: collections.abc.Callable[
            [datetime.datetime], float | str
        ] = model.process_datetime_to_timestamp
        attr_time = core.WebSocket.COMPRESSED_STATE_LAST_UPDATED
        attr_state = core.WebSocket.COMPRESSED_STATE_STATE
    else:
        state_class = model.LazyState
        _process_timestamp = model.process_timestamp_to_utc_isoformat
        attr_time = _LAST_CHANGED_KEY
        attr_state = _STATE_KEY

    result: dict[
        str, list[core.State | dict[str, typing.Any]]
    ] = collections.defaultdict(list)
    # Set all entity IDs to empty lists in result set to maintain the order
    if entity_ids is not None:
        for ent_id in entity_ids:
            result[ent_id] = []

    # Get the states at the start time
    timer_start = time.perf_counter()
    initial_states: dict[str, sql_engine.Row] = {}
    if include_start_time_state:
        initial_states = {
            row.entity_id: row
            for row in _get_rows_with_session(
                rec_comp,
                session,
                start_time,
                entity_ids,
                filters=filters,
                no_attributes=no_attributes,
            )
        }

    if _LOGGER.isEnabledFor(logging.DEBUG):
        elapsed = time.perf_counter() - timer_start
        _LOGGER.debug(f"getting {len(result):d} first datapoints took {elapsed:f}s")

    if entity_ids and len(entity_ids) == 1:
        states_iter: collections.abc.Iterable[
            tuple[str | sql.Column, collections.abc.Iterator[model.States]]
        ] = ((entity_ids[0], iter(states)),)
    else:
        states_iter = it.groupby(states, lambda state: state.entity_id)

    # Append all changes to it
    for ent_id, group in states_iter:
        attr_cache: dict[str, dict[str, typing.Any]] = {}
        prev_state: sql.Column | str
        ent_results = result[ent_id]
        if row := initial_states.pop(ent_id, None):
            prev_state = row.state
            ent_results.append(state_class(row, attr_cache, start_time))

        if (
            not minimal_response
            or core.helpers.split_entity_id(ent_id)[0] in _NEED_ATTRIBUTE_DOMAINS
        ):
            ent_results.extend(state_class(db_state, attr_cache) for db_state in group)
            continue

        # With minimal response we only provide a native
        # State for the first and last response. All the states
        # in-between only provide the "state" and the
        # "last_changed".
        if not ent_results:
            if (first_state := next(group, None)) is None:
                continue
            prev_state = first_state.state
            ent_results.append(state_class(first_state, attr_cache))

        for row in group:
            # With minimal response we do not care about attribute
            # changes so we can filter out duplicate states
            if (state := row.state) == prev_state:
                continue

            ent_results.append(
                {
                    attr_state: state,
                    #
                    # minimal_response only makes sense with last_updated == last_updated
                    #
                    # We use last_updated for for last_changed since its the same
                    #
                    attr_time: _process_timestamp(row.last_updated),
                }
            )
            prev_state = state

    # If there are no states beyond the initial state,
    # the state a was never popped from initial_states
    for ent_id, row in initial_states.items():
        result[ent_id].append(state_class(row, {}, start_time))

    # Filter out the empty lists if some states had 0 results.
    return {key: val for key, val in result.items() if val}
