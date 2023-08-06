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

import datetime as dt
import typing

import sqlalchemy as sql
import sqlalchemy.orm as sql_orm
import sqlalchemy.sql.elements as sql_elements

from .... import core
from .. import model
from ..model import (
    _EVENTS_CONTEXT_ID_INDEX,
    _OLD_FORMAT_ATTRS_JSON,
    _OLD_STATE,
    _SHARED_ATTRS_JSON,
    _STATES_CONTEXT_ID_INDEX,
)

_CONTINUOUS_DOMAINS: typing.Final = {
    core.Const.PROXIMITY_COMPONENT_NAME,
    core.Const.SENSOR_COMPONENT_NAME,
}
_CONTINUOUS_ENTITY_ID_LIKE: typing.Final = [
    f"{domain}.%" for domain in _CONTINUOUS_DOMAINS
]

_UNIT_OF_MEASUREMENT_JSON: typing.Final = '"unit_of_measurement":'
_UNIT_OF_MEASUREMENT_JSON_LIKE: typing.Final = f"%{_UNIT_OF_MEASUREMENT_JSON}%"


_PSEUDO_EVENT_STATE_CHANGED: typing.Final = None
# Since we don't store event_types and None
# and we don't store state_changed in events
# we use a NULL for state_changed events
# when we synthesize them from the states table
# since it avoids another column being sent
# in the payload

_EVENT_COLUMNS: typing.Final = (
    model.Events.event_id.label("event_id"),
    model.Events.event_type.label("event_type"),
    model.Events.event_data.label("event_data"),
    model.Events.time_fired.label("time_fired"),
    model.Events.context_id.label("context_id"),
    model.Events.context_user_id.label("context_user_id"),
    model.Events.context_parent_id.label("context_parent_id"),
)

_STATE_COLUMNS: typing.Final = (
    model.States.state_id.label("state_id"),
    model.States.state.label("state"),
    model.States.entity_id.label("entity_id"),
    _SHARED_ATTRS_JSON["icon"].as_string().label("icon"),
    _OLD_FORMAT_ATTRS_JSON["icon"].as_string().label("old_format_icon"),
)

_STATE_CONTEXT_ONLY_COLUMNS: typing.Final = (
    model.States.state_id.label("state_id"),
    model.States.state.label("state"),
    model.States.entity_id.label("entity_id"),
    sql.literal(value=None, type_=sql.String).label("icon"),
    sql.literal(value=None, type_=sql.String).label("old_format_icon"),
)

_EVENT_COLUMNS_FOR_STATE_SELECT: typing.Final = [
    sql.literal(value=None, type_=sql.Text).label("event_id"),
    # We use PSEUDO_EVENT_STATE_CHANGED aka None for
    # state_changed events since it takes up less
    # space in the response and every row has to be
    # marked with the event_type
    sql.literal(value=_PSEUDO_EVENT_STATE_CHANGED, type_=sql.String).label(
        "event_type"
    ),
    sql.literal(value=None, type_=sql.Text).label("event_data"),
    model.States.last_updated.label("time_fired"),
    model.States.context_id.label("context_id"),
    model.States.context_user_id.label("context_user_id"),
    model.States.context_parent_id.label("context_parent_id"),
    sql.literal(value=None, type_=sql.Text).label("shared_data"),
]

_EMPTY_STATE_COLUMNS: typing.Final = (
    sql.literal(value=None, type_=sql.String).label("state_id"),
    sql.literal(value=None, type_=sql.String).label("state"),
    sql.literal(value=None, type_=sql.String).label("entity_id"),
    sql.literal(value=None, type_=sql.String).label("icon"),
    sql.literal(value=None, type_=sql.String).label("old_format_icon"),
)


_EVENT_ROWS_NO_STATES: typing.Final = (
    *_EVENT_COLUMNS,
    model.EventData.shared_data.label("shared_data"),
    *_EMPTY_STATE_COLUMNS,
)

# Virtual column to tell logbook if it should avoid processing
# the event as its only used to link contexts
_CONTEXT_ONLY: typing.Final = sql.literal("1").label("context_only")
_NOT_CONTEXT_ONLY: typing.Final = sql.literal(None).label("context_only")


# pylint: disable=unused-variable


def select_events_context_id_subquery(
    start_day: dt.datetime,
    end_day: dt.datetime,
    event_types: tuple[str, ...],
) -> sql.sql.Select:
    """Generate the select for a context_id subquery."""
    return (
        sql.select(model.Events.context_id)
        .where(
            (model.Events.time_fired > start_day) & (model.Events.time_fired < end_day)
        )
        .where(model.Events.event_type.in_(event_types))
        .outerjoin(model.EventData, (model.Events.data_id == model.EventData.data_id))
    )


def select_events_context_only() -> sql.sql.Select:
    """Generate an events query that mark them as for context_only.

    By marking them as context_only we know they are only for
    linking context ids and we can avoid processing them.
    """
    return sql.select(*_EVENT_ROWS_NO_STATES, _CONTEXT_ONLY)


def select_states_context_only() -> sql.sql.Select:
    """Generate an states query that mark them as for context_only.

    By marking them as context_only we know they are only for
    linking context ids and we can avoid processing them.
    """
    return sql.select(
        *_EVENT_COLUMNS_FOR_STATE_SELECT, *_STATE_CONTEXT_ONLY_COLUMNS, _CONTEXT_ONLY
    )


def select_events_without_states(
    start_day: dt.datetime, end_day: dt.datetime, event_types: tuple[str, ...]
) -> sql.sql.Select:
    """Generate an events select that does not join states."""
    return (
        sql.select(*_EVENT_ROWS_NO_STATES, _NOT_CONTEXT_ONLY)
        .where(
            (model.Events.time_fired > start_day) & (model.Events.time_fired < end_day)
        )
        .where(model.Events.event_type.in_(event_types))
        .outerjoin(model.EventData, (model.Events.data_id == model.EventData.data_id))
    )


def select_states() -> sql.sql.Select:
    """Generate a states select that formats the states table as event rows."""
    return sql.select(
        *_EVENT_COLUMNS_FOR_STATE_SELECT,
        *_STATE_COLUMNS,
        _NOT_CONTEXT_ONLY,
    )


def legacy_select_events_context_id(
    start_day: dt.datetime, end_day: dt.datetime, context_id: str
) -> sql.sql.Select:
    """Generate a legacy events context id select that also joins states."""
    # This can be removed once we no longer have event_ids in the states table
    return (
        sql.select(
            *_EVENT_COLUMNS,
            sql.literal(value=None, type_=sql.String).label("shared_data"),
            *_STATE_COLUMNS,
            _NOT_CONTEXT_ONLY,
        )
        .outerjoin(model.States, (model.Events.event_id == model.States.event_id))
        .where(
            (model.States.last_updated == model.States.last_changed)
            | model.States.last_changed.is_(None)
        )
        .where(_not_continuous_entity_matcher())
        .outerjoin(
            model.StateAttributes,
            (model.States.attributes_id == model.StateAttributes.attributes_id),
        )
        .where(
            (model.Events.time_fired > start_day) & (model.Events.time_fired < end_day)
        )
        .where(model.Events.context_id == context_id)
    )


def apply_states_filters(
    query: sql_orm.Query, start_day: dt.datetime, end_day: dt.datetime
) -> sql_orm.Query:
    """Filter states by time range.

    Filters states that do not have an old state or new state (added / removed)
    Filters states that are in a continuous domain with a UOM.
    Filters states that do not have matching last_updated and last_changed.
    """
    return (
        query.filter(
            (model.States.last_updated > start_day)
            & (model.States.last_updated < end_day)
        )
        .outerjoin(_OLD_STATE, (model.States.old_state_id == _OLD_STATE.state_id))
        .where(_missing_state_matcher())
        .where(_not_continuous_entity_matcher())
        .where(
            (model.States.last_updated == model.States.last_changed)
            | model.States.last_changed.is_(None)
        )
        .outerjoin(
            model.StateAttributes,
            (model.States.attributes_id == model.StateAttributes.attributes_id),
        )
    )


def _missing_state_matcher() -> sql.and_:
    # The below removes state change events that do not have
    # and old_state or the old_state is missing (newly added entities)
    # or the new_state is missing (removed entities)
    return sql.and_(
        _OLD_STATE.state_id.isnot(None),
        (model.States.state != _OLD_STATE.state),
        model.States.state.isnot(None),
    )


def _not_continuous_entity_matcher() -> sql.or_:
    """Match non continuous entities."""
    return sql.or_(
        _not_continuous_domain_matcher(),
        sql.and_(
            _continuous_domain_matcher, _not_uom_attributes_matcher()
        ).self_group(),
    )


def _not_continuous_domain_matcher() -> sql.and_:
    """Match not continuous domains."""
    return sql.and_(
        *[
            ~model.States.entity_id.like(entity_domain)
            for entity_domain in _CONTINUOUS_ENTITY_ID_LIKE
        ],
    ).self_group()


def _continuous_domain_matcher() -> sql.or_:
    """Match continuous domains."""
    return sql.or_(
        *[
            model.States.entity_id.like(entity_domain)
            for entity_domain in _CONTINUOUS_ENTITY_ID_LIKE
        ],
    ).self_group()


def _not_uom_attributes_matcher() -> sql_elements.ClauseList:
    """Prefilter ATTR_UNIT_OF_MEASUREMENT as its much faster in sql."""
    return ~model.StateAttributes.shared_attrs.like(
        _UNIT_OF_MEASUREMENT_JSON_LIKE
    ) | ~model.States.attributes.like(_UNIT_OF_MEASUREMENT_JSON_LIKE)


def apply_states_context_hints(query: sql_orm.Query) -> sql_orm.Query:
    """Force mysql to use the right index on large context_id selects."""
    return query.with_hint(
        model.States, f"FORCE INDEX ({_STATES_CONTEXT_ID_INDEX})", dialect_name="mysql"
    )


def apply_events_context_hints(query: sql_orm.Query) -> sql_orm.Query:
    """Force mysql to use the right index on large context_id selects."""
    return query.with_hint(
        model.Events, f"FORCE INDEX ({_EVENTS_CONTEXT_ID_INDEX})", dialect_name="mysql"
    )
