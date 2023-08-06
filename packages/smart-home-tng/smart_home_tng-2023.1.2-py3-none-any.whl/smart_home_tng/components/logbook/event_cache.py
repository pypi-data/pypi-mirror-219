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

from . import model


# pylint: disable=unused-variable
class EventCache:
    """Cache LazyEventPartialState by row."""

    def __init__(self, event_data_cache: dict[str, dict[str, typing.Any]]) -> None:
        """Init the cache."""
        self._event_data_cache = event_data_cache
        self._event_cache: dict[
            sql.engine.Row | model.EventAsRow, model.LazyEventPartialState
        ] = {}

    def get(
        self, row: model.EventAsRow | sql.engine.Row
    ) -> model.LazyEventPartialState:
        """Get the event from the row."""
        if isinstance(row, model.EventAsRow):
            return model.LazyEventPartialState(row, self._event_data_cache)
        if event := self._event_cache.get(row):
            return event
        self._event_cache[row] = lazy_event = model.LazyEventPartialState(
            row, self._event_data_cache
        )
        return lazy_event

    def clear(self) -> None:
        """Clear the event cache."""
        self._event_data_cache = {}
        self._event_cache = {}
