"""
Logbook Component for Smart Home - The Next Generation.

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

import typing

import sqlalchemy as sql

from ... import core
from . import model
from .const import Const
from .logbook_run import LogbookRun


# pylint: disable=unused-variable
class ContextAugmenter:
    """Augment data with context trace."""

    def __init__(self, logbook_run: LogbookRun) -> None:
        """Init the augmenter."""
        self._context_lookup = logbook_run.context_lookup
        self._entity_name_cache = logbook_run.entity_name_cache
        self._external_events = logbook_run.external_events
        self._event_cache = logbook_run.event_cache
        self._include_entity_name = logbook_run.include_entity_name

    def _get_context_row(
        self, context_id: str, row: sql.engine.Row | model.EventAsRow
    ) -> sql.engine.Row | model.EventAsRow:
        """Get the context row from the id or row context."""
        if context_id:
            return self._context_lookup.get(context_id)
        if (context := getattr(row, "context", None)) is not None and (
            origin_event := context.origin_event
        ) is not None:
            return model.async_event_to_row(origin_event, self._external_events)
        return None

    def augment(
        self,
        data: dict[str, typing.Any],
        row: sql.engine.Row | model.EventAsRow,
        context_id: str,
    ) -> None:
        """Augment data from the row and cache."""
        if context_user_id := row.context_user_id:
            data[Const.CONTEXT_USER_ID] = context_user_id

        if not (context_row := self._get_context_row(context_id, row)):
            return

        if _rows_match(row, context_row):
            # This is the first event with the given ID. Was it directly caused by
            # a parent event?
            if (
                not row.context_parent_id
                or (
                    context_row := self._get_context_row(
                        row.context_parent_id, context_row
                    )
                )
                is None
            ):
                return
            # Ensure the (parent) context_event exists and is not the root cause of
            # this log entry.
            if _rows_match(row, context_row):
                return
        event_type = context_row.event_type
        # State change
        if context_entity_id := context_row.entity_id:
            data[Const.CONTEXT_STATE] = context_row.state
            data[Const.CONTEXT_ENTITY_ID] = context_entity_id
            if self._include_entity_name:
                data[Const.CONTEXT_ENTITY_ID_NAME] = self._entity_name_cache.get(
                    context_entity_id
                )
            return

        # Call service
        if event_type == core.Const.EVENT_CALL_SERVICE:
            event = self._event_cache.get(context_row)
            event_data = event.data
            data[Const.CONTEXT_DOMAIN] = event_data.get(core.Const.ATTR_DOMAIN)
            data[Const.CONTEXT_SERVICE] = event_data.get(core.Const.ATTR_SERVICE)
            data[Const.CONTEXT_EVENT_TYPE] = event_type
            return

        if event_type not in self._external_events:
            return

        domain, platform = self._external_events[event_type]
        data[Const.CONTEXT_EVENT_TYPE] = event_type
        data[Const.CONTEXT_DOMAIN] = domain
        event = self._event_cache.get(context_row)
        described = platform.async_describe_event(event)
        if name := described.get(core.Const.LOGBOOK_ENTRY_NAME):
            data[Const.CONTEXT_NAME] = name
        if source := described.get(core.Const.LOGBOOK_ENTRY_SOURCE):
            data[Const.CONTEXT_SOURCE] = source
        else:
            if message := described.get(core.Const.LOGBOOK_ENTRY_MESSAGE):
                data[Const.CONTEXT_MESSAGE] = message
        if not (attr_entity_id := described.get(core.Const.LOGBOOK_ENTRY_ENTITY_ID)):
            return
        data[Const.CONTEXT_ENTITY_ID] = attr_entity_id
        if self._include_entity_name:
            data[Const.CONTEXT_ENTITY_ID_NAME] = self._entity_name_cache.get(
                attr_entity_id
            )


def _rows_match(
    row: sql.engine.Row | model.EventAsRow, other_row: sql.engine.Row | model.EventAsRow
) -> bool:
    """Check of rows match by using the same method as Events __hash__."""
    if (
        row is other_row
        or (state_id := row.state_id) is not None
        and state_id == other_row.state_id
        or (event_id := row.event_id) is not None
        and event_id == other_row.event_id
    ):
        return True
    return False
