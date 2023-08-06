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

# pylint: disable=unused-variable

import dataclasses
import datetime as dt
import json
import typing

import sqlalchemy as sql

from ... import core


@dataclasses.dataclass(frozen=True)
@typing.final
class EventAsRow:
    """Convert an event to a row."""

    data: dict[str, typing.Any]
    context: core.Context
    context_id: str
    time_fired: dt.datetime
    state_id: int
    event_data: str = None
    old_format_icon = None
    event_id: None = None
    entity_id: str = None
    icon: str = None
    context_user_id: str = None
    context_parent_id: str = None
    event_type: str = None
    state: str = None
    shared_data: str = None
    context_only: None = None


class LazyEventPartialState(core.LazyPartialState):
    """A lazy version of core Event with limited State joined in."""

    __slots__ = [
        "_row",
        "_event_data",
        "_event_data_cache",
        "_event_type",
        "_entity_id",
        "_state",
        "_context_id",
        "_context_user_id",
        "_context_parent_id",
        "_data",
    ]

    def __init__(
        self,
        row: sql.engine.Row | EventAsRow,
        event_data_cache: dict[str, dict[str, typing.Any]],
    ) -> None:
        """Init the lazy event."""
        self._row = row
        self._event_data: dict[str, typing.Any] = None
        self._event_data_cache = event_data_cache
        self._event_type: str = row.event_type
        self._entity_id: str = row.entity_id
        self._state = row.state
        self._context_id: str = row.context_id
        self._context_user_id: str = row.context_user_id
        self._context_parent_id: str = row.context_parent_id
        if data := getattr(row, "data", None):
            # If its an EventAsRow we can avoid the whole
            # json decode process as we already have the data
            self._data = data
            return
        source = typing.cast(str, row.shared_data or row.event_data)
        if not source:
            self._data = {}
        elif event_data := self._event_data_cache.get(source):
            self._data = event_data
        else:
            self._data = self._event_data_cache[source] = typing.cast(
                dict[str, typing.Any], json.loads(source)
            )

    @property
    def data(self) -> dict:
        return self._data

    @property
    def context_id(self) -> str:
        return self._context_id

    @property
    def event_type(self) -> str:
        return self._event_type


class _DescribeEventDummy(core.LazyPartialState):
    """
    Helper, to simulate LazyPartialState.

    Needed, to support all LOGBOOK_ENTRY_xxx fields
    """

    def __init__(self, event: core.Event) -> None:
        super().__init__()
        self._data = event.data
        self._context_id: str = None
        self._event_type = event.event_type
        if event.context is not None:
            self._context_id = event.context.context_id

    @property
    def event_type(self) -> str:
        return self._event_type

    @property
    def data(self) -> dict:
        return self._data

    @property
    def context_id(self) -> str:
        return self._context_id


@core.callback
def async_event_to_row(
    event: core.Event, external_events: dict[str, tuple[str, core.LogbookPlatform]]
) -> EventAsRow:
    """Convert an event to a row."""

    if event.event_type != core.Const.EVENT_STATE_CHANGED:
        context = event.context
        context_id = context.context_id
        context_user_id = context.user_id
        context_parent_id = context.parent_id
        icon: str = None

        event_type = event.event_type
        if event_type in external_events:
            _domain, platform = external_events[event_type]
            describe_dummy = _DescribeEventDummy(event)
            described = platform.async_describe_event(describe_dummy)
            if core.Const.LOGBOOK_ENTRY_CONTEXT_ID in described:
                context = None
                context_parent_id = None
                context_id = described[core.Const.LOGBOOK_ENTRY_CONTEXT_ID]
            if core.Const.LOGBOOK_ENTRY_ICON in described:
                icon = described[core.Const.LOGBOOK_ENTRY_ICON]

        return EventAsRow(
            data=event.data,
            context=context,
            event_type=event_type,
            context_id=context_id,
            context_user_id=context_user_id,
            context_parent_id=context_parent_id,
            time_fired=event.time_fired,
            state_id=hash(event),
            icon=icon,
        )
    # States are prefiltered so we never get states
    # that are missing new_state or old_state
    # since the logbook does not show these
    new_state: core.State = event.data["new_state"]
    return EventAsRow(
        data=event.data,
        context=event.context,
        entity_id=new_state.entity_id,
        state=new_state.state,
        context_id=new_state.context.context_id,
        context_user_id=new_state.context.user_id,
        context_parent_id=new_state.context.parent_id,
        time_fired=new_state.last_updated,
        state_id=hash(event),
        icon=new_state.attributes.get(core.Const.ATTR_ICON),
    )
