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

import collections.abc
import contextlib
import datetime as dt
import typing

import sqlalchemy as sql
import sqlalchemy.orm as sql_orm

from ... import core
from . import model
from .const import Const
from .context_augmenter import ContextAugmenter
from .context_lookup import ContextLookup
from .entity_name_cache import EntityNameCache
from .event_cache import EventCache
from .logbook_run import LogbookRun

if not typing.TYPE_CHECKING:

    class LogbookComponent:
        ...


if typing.TYPE_CHECKING:
    from .logbook_component import LogbookComponent


# pylint: disable=unused-variable
class EventProcessor:
    """Stream into logbook format."""

    def __init__(
        self,
        owner: LogbookComponent,
        event_types: tuple[str, ...],
        entity_ids: list[str] = None,
        device_ids: list[str] = None,
        context_id: str = None,
        timestamp: bool = False,
        include_entity_name: bool = True,
    ) -> None:
        """Init the event stream."""
        assert not (
            context_id and (entity_ids or device_ids)
        ), "can't pass in both context_id and (entity_ids or device_ids)"
        self._owner = owner
        self._ent_reg = self._owner.controller.entity_registry
        self._event_types = event_types
        self._entity_ids = entity_ids
        self._device_ids = device_ids
        self._context_id = context_id
        self._filters = owner.filters
        if self.limited_select:
            self._entities_filter: core.EntityFilter | collections.abc.Callable[
                [str], bool
            ] = None
        else:
            self._entities_filter = owner.entity_filters

        format_time = (
            self._row_time_fired_timestamp
            if timestamp
            else self._row_time_fired_isoformat
        )
        external_events = self._owner.external_events

        self._logbook_run = LogbookRun(
            context_lookup=ContextLookup(),
            external_events=external_events,
            event_cache=EventCache({}),
            entity_name_cache=EntityNameCache(self._owner.controller),
            include_entity_name=include_entity_name,
            format_time=format_time,
        )
        self._context_augmenter = ContextAugmenter(self._logbook_run)

    @property
    def entity_ids(self) -> list[str]:
        return self._entity_ids

    @property
    def device_ids(self) -> list[str]:
        return self._device_ids

    @property
    def limited_select(self) -> bool:
        """Check if the stream is limited by entities context or device ids."""
        return bool(self._entity_ids or self._context_id or self._device_ids)

    def switch_to_live(self) -> None:
        """Switch to live stream.

        Clear caches so we can reduce memory pressure.
        """
        self._logbook_run.event_cache.clear()
        self._logbook_run.context_lookup.clear()

    def _row_time_fired_isoformat(self, row: sql.engine.Row | model.EventAsRow) -> str:
        """Convert the row timed_fired to isoformat."""
        if self._owner.recorder_component is not None:
            return self._owner.recorder_component.process_timestamp_to_utc_isoformat(
                row.time_fired or core.helpers.utcnow()
            )
        raise NotImplementedError()

    def _row_time_fired_timestamp(
        self, row: sql.engine.Row | model.EventAsRow
    ) -> float:
        """Convert the row timed_fired to timestamp."""
        if self._owner.recorder_component is not None:
            return self._owner.recorder_component.process_datetime_to_timestamp(
                row.time_fired or core.helpers.utcnow()
            )
        raise NotImplementedError()

    def get_events(
        self,
        start_day: dt.datetime,
        end_day: dt.datetime,
    ) -> list[dict[str, typing.Any]]:
        """Get events for a period of time."""

        def yield_rows(
            query: sql_orm.Query,
        ) -> collections.abc.Generator[sql.engine.Row, None, None]:
            """Yield rows from the database."""
            # end_day - start_day intentionally checks .days and not .total_seconds()
            # since we don't want to switch over to buffered if they go
            # over one day by a few hours since the UI makes it so easy to do that.
            if self.limited_select or (end_day - start_day).days <= 1:
                return query.all()
            # Only buffer rows to reduce memory pressure
            # if we expect the result set is going to be very large.
            # What is considered very large is going to differ
            # based on the hardware Home Assistant is running on.
            #
            # sqlalchemy suggests that is at least 10k, but for
            # even and RPi3 that number seems higher in testing
            # so we don't switch over until we request > 1 day+ of data.
            #
            return query.yield_per(1024)

        stmt = self._owner.recorder_component.statement_for_logbook_request(
            start_day,
            end_day,
            self._event_types,
            self._entity_ids,
            self._device_ids,
            self._filters,
            self._context_id,
        )
        with self._owner.recorder_component.session_scope() as session:
            return self.humanify(yield_rows(session.execute(stmt)))

    def humanify(
        self,
        row_generator: collections.abc.Generator[
            sql.engine.Row | model.EventAsRow, None, None
        ],
    ) -> list[dict[str, str]]:
        """Humanify rows."""
        return list(
            _humanify(
                self._owner,
                row_generator,
                self._entities_filter,
                self._logbook_run,
                self._context_augmenter,
            )
        )


def _humanify(
    owner: LogbookComponent,
    rows: collections.abc.Generator[sql.engine.Row | model.EventAsRow, None, None],
    entities_filter: core.EntityFilter | collections.abc.Callable[[str], bool],
    logbook_run: LogbookRun,
    context_augmenter: ContextAugmenter,
) -> collections.abc.Generator[dict[str, typing.Any], None, None]:
    """Generate a converted list of events into entries."""
    # Continuous sensors, will be excluded from the logbook
    continuous_sensors: dict[str, bool] = {}
    context_lookup = logbook_run.context_lookup
    external_events = logbook_run.external_events
    event_cache = logbook_run.event_cache
    entity_name_cache = logbook_run.entity_name_cache
    include_entity_name = logbook_run.include_entity_name
    format_time = logbook_run.format_time

    def _keep_row(row: model.EventAsRow) -> bool:
        """Check if the entity_filter rejects a row."""
        assert entities_filter is not None
        if entity_id := row.entity_id:
            return entities_filter(entity_id)
        if entity_id := row.data.get(core.Const.ATTR_ENTITY_ID):
            return entities_filter(entity_id)
        if domain := row.data.get(core.Const.ATTR_DOMAIN):
            return entities_filter(f"{domain}._")
        return True

    # Process rows
    for row in rows:
        context_id = context_lookup.memorize(row)
        if row.context_only:
            continue
        event_type = row.event_type
        if event_type == core.Const.EVENT_CALL_SERVICE or (
            entities_filter and isinstance(row, model.EventAsRow) and not _keep_row(row)
        ):
            continue
        if event_type is owner.recorder_component.pseudo_event_state_changed:
            entity_id = row.entity_id
            assert entity_id is not None
            # Skip continuous sensors
            if (
                is_continuous := continuous_sensors.get(entity_id)
            ) is None and core.helpers.split_entity_id(entity_id)[
                0
            ] == core.Const.SENSOR_COMPONENT_NAME:
                is_continuous = owner.is_sensor_continuous(entity_id)
                continuous_sensors[entity_id] = is_continuous
            if is_continuous:
                continue

            data = {
                Const.LOGBOOK_ENTRY_WHEN: format_time(row),
                Const.LOGBOOK_ENTRY_STATE: row.state,
                core.Const.LOGBOOK_ENTRY_ENTITY_ID: entity_id,
            }
            if include_entity_name:
                data[core.Const.LOGBOOK_ENTRY_NAME] = entity_name_cache.get(entity_id)
            if icon := row.icon or row.old_format_icon:
                data[core.Const.LOGBOOK_ENTRY_ICON] = icon

            context_augmenter.augment(data, row, context_id)
            yield data

        elif event_type in external_events:
            domain, platform = external_events[event_type]
            data = platform.async_describe_event(event_cache.get(row))
            data[Const.LOGBOOK_ENTRY_WHEN] = format_time(row)
            data[Const.LOGBOOK_ENTRY_DOMAIN] = domain
            context_augmenter.augment(data, row, context_id)
            yield data

        elif event_type == core.Const.EVENT_LOGBOOK_ENTRY:
            event = event_cache.get(row)
            if not (event_data := event.data):
                continue
            entry_domain = event_data.get(core.Const.ATTR_DOMAIN)
            entry_entity_id = event_data.get(core.Const.ATTR_ENTITY_ID)
            if entry_domain is None and entry_entity_id is not None:
                with contextlib.suppress(IndexError):
                    entry_domain = core.helpers.split_entity_id(str(entry_entity_id))[0]
            data = {
                Const.LOGBOOK_ENTRY_WHEN: format_time(row),
                core.Const.LOGBOOK_ENTRY_NAME: event_data.get(core.Const.ATTR_NAME),
                core.Const.LOGBOOK_ENTRY_MESSAGE: event_data.get(Const.ATTR_MESSAGE),
                Const.LOGBOOK_ENTRY_DOMAIN: entry_domain,
                core.Const.LOGBOOK_ENTRY_ENTITY_ID: entry_entity_id,
            }
            context_augmenter.augment(data, row, context_id)
            yield data
