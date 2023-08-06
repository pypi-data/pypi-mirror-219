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

import collections.abc
import datetime as dt

import sqlalchemy as sql
import sqlalchemy.orm as sql_orm
import sqlalchemy.sql.elements as sql_elements
import sqlalchemy.sql.selectable as sql_selectable

from .. import model
from ..model import _DEVICE_ID_IN_EVENT
from . import common


def _select_device_id_context_ids_sub_query(
    start_day: dt.datetime,
    end_day: dt.datetime,
    event_types: tuple[str, ...],
    json_quotable_device_ids: list[str],
) -> sql.sql.CompoundSelect:
    """Generate a subquery to find context ids for multiple devices."""
    inner = common.select_events_context_id_subquery(
        start_day, end_day, event_types
    ).where(apply_event_device_id_matchers(json_quotable_device_ids))
    return sql.select(inner.c.context_id).group_by(inner.c.context_id)


def _apply_devices_context_union(
    query: sql_orm.Query,
    start_day: dt.datetime,
    end_day: dt.datetime,
    event_types: tuple[str, ...],
    json_quotable_device_ids: list[str],
) -> sql.sql.CompoundSelect:
    """Generate a CTE to find the device context ids and a query to find linked row."""
    devices_cte: sql_selectable.CTE = _select_device_id_context_ids_sub_query(
        start_day,
        end_day,
        event_types,
        json_quotable_device_ids,
    ).cte()
    return query.union_all(
        common.apply_events_context_hints(
            common.select_events_context_only()
            .select_from(devices_cte)
            .outerjoin(
                model.Events, devices_cte.c.context_id == model.Events.context_id
            )
        ).outerjoin(model.EventData, (model.Events.data_id == model.EventData.data_id)),
        common.apply_states_context_hints(
            common.select_states_context_only()
            .select_from(devices_cte)
            .outerjoin(
                model.States, devices_cte.c.context_id == model.States.context_id
            )
        ),
    )


# pylint: disable=unused-variable
def devices_stmt(
    start_day: dt.datetime,
    end_day: dt.datetime,
    event_types: tuple[str, ...],
    json_quotable_device_ids: list[str],
) -> sql.sql.StatementLambdaElement:
    """Generate a logbook query for multiple devices."""
    stmt = sql.lambda_stmt(
        lambda: _apply_devices_context_union(
            common.select_events_without_states(start_day, end_day, event_types).where(
                apply_event_device_id_matchers(json_quotable_device_ids)
            ),
            start_day,
            end_day,
            event_types,
            json_quotable_device_ids,
        ).order_by(model.Events.time_fired)
    )
    return stmt


def apply_event_device_id_matchers(
    json_quotable_device_ids: collections.abc.Iterable[str],
) -> sql_elements.ClauseList:
    """Create matchers for the device_ids in the event_data."""
    return _DEVICE_ID_IN_EVENT.in_(json_quotable_device_ids)
