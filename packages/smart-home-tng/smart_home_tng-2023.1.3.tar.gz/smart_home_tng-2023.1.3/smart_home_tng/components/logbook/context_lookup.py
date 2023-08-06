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

import sqlalchemy as sql

from . import model


# pylint: disable=unused-variable
class ContextLookup:
    """A lookup class for context origins."""

    def __init__(self) -> None:
        """Memorize context origin."""
        self._memorize_new = True
        self._lookup: dict[str, sql.engine.Row | model.EventAsRow] = {None: None}

    def memorize(self, row: sql.engine.Row) -> str:
        """Memorize a context from the database."""
        if self._memorize_new:
            context_id: str = row.context_id
            self._lookup.setdefault(context_id, row)
            return context_id
        return None

    def clear(self) -> None:
        """Clear the context origins and stop recording new ones."""
        self._lookup.clear()
        self._memorize_new = False

    def get(self, context_id: str) -> sql.engine.Row:
        """Get the context origin."""
        return self._lookup.get(context_id)
