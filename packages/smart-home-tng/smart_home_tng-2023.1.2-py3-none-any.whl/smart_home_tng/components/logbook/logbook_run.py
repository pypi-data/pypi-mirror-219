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

import collections.abc
import dataclasses
import typing

import sqlalchemy as sql

from ... import core
from .context_lookup import ContextLookup
from .event_cache import EventCache
from .entity_name_cache import EntityNameCache


@dataclasses.dataclass()
class LogbookRun:
    """A logbook run which may be a long running event stream or single request."""

    context_lookup: ContextLookup
    external_events: dict[
        str,
        tuple[str, core.LogbookPlatform],
    ]
    event_cache: EventCache
    entity_name_cache: EntityNameCache
    include_entity_name: bool
    format_time: collections.abc.Callable[[sql.engine.Row], typing.Any]
