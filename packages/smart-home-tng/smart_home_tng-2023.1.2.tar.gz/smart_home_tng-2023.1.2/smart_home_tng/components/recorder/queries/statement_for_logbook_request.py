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

from ..filters import Filters
from .all import all_stmt
from .devices import devices_stmt
from .entities import entities_stmt
from .entities_and_devices import entities_devices_stmt


# pylint: disable=unused-variable
def statement_for_logbook_request(
    start_day: dt.datetime,
    end_day: dt.datetime,
    event_types: tuple[str, ...],
    entity_ids: list[str] = None,
    device_ids: list[str] = None,
    filters: Filters = None,
    context_id: str = None,
) -> sql.sql.StatementLambdaElement:
    """Generate the logbook statement for a logbook request."""

    # No entities: logbook sends everything for the timeframe
    # limited by the context_id and the yaml configured filter
    if not entity_ids and not device_ids:
        states_entity_filter = filters.states_entity_filter() if filters else None
        events_entity_filter = filters.events_entity_filter() if filters else None
        return all_stmt(
            start_day,
            end_day,
            event_types,
            states_entity_filter,
            events_entity_filter,
            context_id,
        )

    # sqlalchemy caches object quoting, the
    # json quotable ones must be a different
    # object from the non-json ones to prevent
    # sqlalchemy from quoting them incorrectly

    # entities and devices: logbook sends everything for the timeframe for the entities and devices
    if entity_ids and device_ids:
        json_quotable_entity_ids = list(entity_ids)
        json_quotable_device_ids = list(device_ids)
        return entities_devices_stmt(
            start_day,
            end_day,
            event_types,
            entity_ids,
            json_quotable_entity_ids,
            json_quotable_device_ids,
        )

    # entities: logbook sends everything for the timeframe for the entities
    if entity_ids:
        json_quotable_entity_ids = list(entity_ids)
        return entities_stmt(
            start_day,
            end_day,
            event_types,
            entity_ids,
            json_quotable_entity_ids,
        )

    # devices: logbook sends everything for the timeframe for the devices
    assert device_ids is not None
    json_quotable_device_ids = list(device_ids)
    return devices_stmt(
        start_day,
        end_day,
        event_types,
        json_quotable_device_ids,
    )
