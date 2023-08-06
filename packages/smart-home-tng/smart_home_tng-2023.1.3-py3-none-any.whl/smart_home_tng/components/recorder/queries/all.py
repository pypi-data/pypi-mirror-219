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

import sqlalchemy as sql
import sqlalchemy.orm as sql_orm
import sqlalchemy.sql.elements as sql_elements

from .. import model
from ..model import _LAST_UPDATED_INDEX
from . import common


# pylint: disable=unused-variable
def all_stmt(
    start_day: dt,
    end_day: dt,
    event_types: tuple[str, ...],
    states_entity_filter: sql_elements.ClauseList = None,
    events_entity_filter: sql_elements.ClauseList = None,
    context_id: str = None,
) -> sql.sql.StatementLambdaElement:
    """Generate a logbook query for all entities."""
    stmt = sql.lambda_stmt(
        lambda: common.select_events_without_states(start_day, end_day, event_types)
    )
    if context_id is not None:
        # Once all the old `state_changed` events
        # are gone from the database remove the
        # _legacy_select_events_context_id()
        stmt += lambda s: s.where(model.Events.context_id == context_id).union_all(
            _states_query_for_context_id(start_day, end_day, context_id),
            common.legacy_select_events_context_id(start_day, end_day, context_id),
        )
    else:
        if events_entity_filter is not None:
            stmt += lambda s: s.where(events_entity_filter)

        if states_entity_filter is not None:
            stmt += lambda s: s.union_all(
                _states_query_for_all(start_day, end_day).where(states_entity_filter)
            )
        else:
            stmt += lambda s: s.union_all(_states_query_for_all(start_day, end_day))

    stmt += lambda s: s.order_by(model.Events.time_fired)
    return stmt


def _states_query_for_all(start_day: dt, end_day: dt) -> sql_orm.Query:
    return common.apply_states_filters(
        _apply_all_hints(common.select_states()), start_day, end_day
    )


def _apply_all_hints(query: sql_orm.Query) -> sql_orm.Query:
    """Force mysql to use the right index on large selects."""
    return query.with_hint(
        model.States, f"FORCE INDEX ({_LAST_UPDATED_INDEX})", dialect_name="mysql"
    )


def _states_query_for_context_id(
    start_day: dt, end_day: dt, context_id: str
) -> sql_orm.Query:
    return common.apply_states_filters(
        common.select_states(), start_day, end_day
    ).where(model.States.context_id == context_id)
