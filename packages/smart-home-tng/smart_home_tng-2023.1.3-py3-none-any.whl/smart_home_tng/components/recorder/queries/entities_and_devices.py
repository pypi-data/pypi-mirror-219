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
import sqlalchemy.sql.selectable as sql_selectable

from .. import model
from . import common, devices, entities

# pylint: disable=unused-variable


def _select_entities_device_id_context_ids_sub_query(
    start_day: dt,
    end_day: dt,
    event_types: tuple[str, ...],
    entity_ids: list[str],
    json_quotable_entity_ids: list[str],
    json_quotable_device_ids: list[str],
) -> sql.sql.CompoundSelect:
    """Generate a subquery to find context ids for multiple entities and multiple devices."""
    union = sql.union_all(
        common.select_events_context_id_subquery(start_day, end_day, event_types).where(
            _apply_event_entity_id_device_id_matchers(
                json_quotable_entity_ids, json_quotable_device_ids
            )
        ),
        entities.apply_entities_hints(sql.select(model.States.context_id))
        .filter(
            (model.States.last_updated > start_day)
            & (model.States.last_updated < end_day)
        )
        .where(model.States.entity_id.in_(entity_ids)),
    )
    return sql.select(union.c.context_id).group_by(union.c.context_id)


def _apply_entities_devices_context_union(
    query: sql_orm.Query,
    start_day: dt.datetime,
    end_day: dt.datetime,
    event_types: tuple[str, ...],
    entity_ids: list[str],
    json_quotable_entity_ids: list[str],
    json_quotable_device_ids: list[str],
) -> sql.sql.CompoundSelect:
    devices_entities_cte: sql_selectable.CTE = (
        _select_entities_device_id_context_ids_sub_query(
            start_day,
            end_day,
            event_types,
            entity_ids,
            json_quotable_entity_ids,
            json_quotable_device_ids,
        ).cte()
    )
    # We used to optimize this to exclude rows we already in the union with
    # a States.entity_id.not_in(entity_ids) but that made the
    # query much slower on MySQL, and since we already filter them away
    # in the python code anyways since they will have context_only
    # set on them the impact is minimal.
    return query.union_all(
        entities.states_query_for_entity_ids(start_day, end_day, entity_ids),
        common.apply_events_context_hints(
            common.select_events_context_only()
            .select_from(devices_entities_cte)
            .outerjoin(
                model.Events,
                devices_entities_cte.c.context_id == model.Events.context_id,
            )
        ).outerjoin(model.EventData, (model.Events.data_id == model.EventData.data_id)),
        common.apply_states_context_hints(
            common.select_states_context_only()
            .select_from(devices_entities_cte)
            .outerjoin(
                model.States,
                devices_entities_cte.c.context_id == model.States.context_id,
            )
        ),
    )


def entities_devices_stmt(
    start_day: dt.datetime,
    end_day: dt.datetime,
    event_types: tuple[str, ...],
    entity_ids: list[str],
    json_quotable_entity_ids: list[str],
    json_quotable_device_ids: list[str],
) -> sql.sql.StatementLambdaElement:
    """Generate a logbook query for multiple entities."""
    stmt = sql.lambda_stmt(
        lambda: _apply_entities_devices_context_union(
            common.select_events_without_states(start_day, end_day, event_types).where(
                _apply_event_entity_id_device_id_matchers(
                    json_quotable_entity_ids, json_quotable_device_ids
                )
            ),
            start_day,
            end_day,
            event_types,
            entity_ids,
            json_quotable_entity_ids,
            json_quotable_device_ids,
        ).order_by(model.Events.time_fired)
    )
    return stmt


def _apply_event_entity_id_device_id_matchers(
    json_quotable_entity_ids: collections.abc.Iterable[str],
    json_quotable_device_ids: collections.abc.Iterable[str],
) -> sql.or_:
    """Create matchers for the device_id and entity_id in the event_data."""
    return entities.apply_event_entity_id_matchers(
        json_quotable_entity_ids
    ) | devices.apply_event_device_id_matchers(json_quotable_device_ids)
