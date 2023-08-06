"""
History Component for Smart Home - The Next Generation.

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
import http
import logging
import time
import typing

from aiohttp import web

from ... import core

_LOGGER: typing.Final = logging.getLogger(__name__)


# pylint: disable=unused-variable
class HistoryPeriodView(core.SmartHomeControllerView):
    """Handle history period requests."""

    def __init__(
        self,
        recorder: core.RecorderComponent,
        filters: core.RecorderFiltersBase,
        use_include_order: bool,
    ):
        super().__init__(
            "/api/history/period",
            "api:history:view-period",
            ["/api/history/period/{datetime}"],
        )
        self._recorder = recorder
        self._filters = filters
        self._use_include_order = use_include_order

    async def get(self, request: web.Request, datetime: str = None) -> web.Response:
        """Return history over a period of time."""
        datetime_ = None
        if datetime and (datetime_ := core.helpers.parse_datetime(datetime)) is None:
            return self.json_message("Invalid datetime", http.HTTPStatus.BAD_REQUEST)

        now = core.helpers.utcnow()

        one_day = dt.timedelta(days=1)
        if datetime_:
            start_time = core.helpers.as_utc(datetime_)
        else:
            start_time = now - one_day

        if start_time > now or self._recorder is None:
            return self.json([])

        if end_time_str := request.query.get("end_time"):
            if end_time := core.helpers.parse_datetime(end_time_str):
                end_time = core.helpers.as_utc(end_time)
            else:
                return self.json_message(
                    "Invalid end_time", http.HTTPStatus.BAD_REQUEST
                )
        else:
            end_time = start_time + one_day
        entity_ids_str = request.query.get("filter_entity_id")
        entity_ids = None
        if entity_ids_str:
            entity_ids = entity_ids_str.lower().split(",")
        include_start_time_state = "skip_initial_state" not in request.query
        significant_changes_only = (
            request.query.get("significant_changes_only", "1") != "0"
        )

        minimal_response = "minimal_response" in request.query
        no_attributes = "no_attributes" in request.query

        shc = request.app[core.Const.KEY_SHC]

        if (
            not include_start_time_state
            and entity_ids
            and not _entities_may_have_state_changes_after(shc, entity_ids, start_time)
        ):
            return self.json([])

        return typing.cast(
            web.Response,
            await self._recorder.async_add_executor_job(
                self._sorted_significant_states_json,
                start_time,
                end_time,
                entity_ids,
                include_start_time_state,
                significant_changes_only,
                minimal_response,
                no_attributes,
            ),
        )

    def _sorted_significant_states_json(
        self,
        start_time: dt.datetime,
        end_time: dt.datetime,
        entity_ids: list[str],
        include_start_time_state: bool,
        significant_changes_only: bool,
        minimal_response: bool,
        no_attributes: bool,
    ) -> web.Response:
        """Fetch significant stats from the database as json."""
        timer_start = time.perf_counter()

        states = None
        with self._recorder.session_scope() as session:
            states = self._recorder.history.get_significant_states_with_session(
                session,
                start_time,
                end_time,
                entity_ids,
                self._filters,
                include_start_time_state,
                significant_changes_only,
                minimal_response,
                no_attributes,
            )

        if states is None:
            return self.json("", http.HTTPStatus.NOT_FOUND)

        if _LOGGER.isEnabledFor(logging.DEBUG):
            elapsed = time.perf_counter() - timer_start
            _LOGGER.debug(
                f"Extracted {sum(map(len, states.values())):d} states in {elapsed:f}s"
            )

        # Optionally reorder the result to respect the ordering given
        # by any entities explicitly included in the configuration.
        if not self._filters or not self._use_include_order:
            return self.json(list(states.values()))

        sorted_result = [
            states.pop(order_entity)
            for order_entity in self._filters.included_entities
            if order_entity in states
        ]
        sorted_result.extend(list(states.values()))
        return self.json(sorted_result)


def _entities_may_have_state_changes_after(
    shc: core.SmartHomeController,
    entity_ids: collections.abc.Iterable[str],
    start_time: dt.datetime,
) -> bool:
    """Check the state machine to see if entities have changed since start time."""
    for entity_id in entity_ids:
        state = shc.states.get(entity_id)

        if state is None or state.last_changed > start_time:
            return True

    return False
