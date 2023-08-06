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

import datetime as dt
import http
import typing

import voluptuous as vol
from aiohttp import web

from ... import core
from .event_processor import EventProcessor

_cv: typing.TypeAlias = core.ConfigValidation

if not typing.TYPE_CHECKING:

    class LogbookComponent:
        ...


if typing.TYPE_CHECKING:
    from .logbook_component import LogbookComponent


# pylint: disable=unused-variable
class LogbookView(core.SmartHomeControllerView):
    """Handle logbook view requests."""

    def __init__(
        self,
        owner: LogbookComponent,
        config: dict[str, typing.Any],
    ) -> None:
        """Initialize the logbook view."""
        url = "/api/logbook"
        name = "api:logbook"
        extra_urls = ["/api/logbook/{datetime}"]
        super().__init__(url, name, extra_urls)
        self._config = config
        self._owner = owner

    async def get(self, request: web.Request, datetime: str = None) -> web.Response:
        """Retrieve logbook entries."""
        if self._owner.recorder_component is None:
            return self.json_message(
                "Recorder not configured", http.HTTPStatus.INTERNAL_SERVER_ERROR
            )

        if datetime:
            if (datetime_dt := core.helpers.parse_datetime(datetime)) is None:
                return self.json_message(
                    "Invalid datetime", http.HTTPStatus.BAD_REQUEST
                )
        else:
            datetime_dt = core.helpers.start_of_local_day()

        if (period_str := request.query.get("period")) is None:
            period: int = 1
        else:
            period = int(period_str)

        if entity_ids_str := request.query.get("entity"):
            try:
                entity_ids = _cv.entity_ids(entity_ids_str)
            except vol.Invalid:
                raise core.InvalidEntityFormatError(
                    f"Invalid entity id(s) encountered: {entity_ids_str}. "
                    "Format should be <domain>.<object_id>"
                ) from vol.Invalid
        else:
            entity_ids = None

        if (end_time_str := request.query.get("end_time")) is None:
            start_day = core.helpers.as_utc(datetime_dt) - dt.timedelta(days=period - 1)
            end_day = start_day + dt.timedelta(days=period)
        else:
            start_day = datetime_dt
            if (end_day_dt := core.helpers.parse_datetime(end_time_str)) is None:
                return self.json_message(
                    "Invalid end_time", http.HTTPStatus.BAD_REQUEST
                )
            end_day = end_day_dt

        context_id = request.query.get("context_id")

        if entity_ids and context_id:
            return self.json_message(
                "Can't combine entity with context_id", http.HTTPStatus.BAD_REQUEST
            )

        event_types = self._owner.async_determine_event_types(entity_ids, None)
        event_processor = EventProcessor(
            self._owner,
            event_types,
            entity_ids,
            None,
            context_id,
            timestamp=False,
            include_entity_name=True,
        )

        return typing.cast(
            web.Response,
            await self._owner.recorder_component.async_add_executor_job(
                self._json_events, event_processor, start_day, end_day
            ),
        )

    def _json_events(
        self,
        event_processor: EventProcessor,
        start_day: dt.datetime,
        end_day: dt.datetime,
    ) -> web.Response:
        """Fetch events and generate JSON."""
        return self.json(
            event_processor.get_events(
                start_day,
                end_day,
            )
        )
