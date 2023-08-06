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

import asyncio
import collections.abc
import datetime as dt
import logging
import typing

import voluptuous as vol

from ... import core
from . import model
from .const import Const
from .event_processor import EventProcessor
from .logbook_live_stream import LogbookLiveStream
from .logbook_view import LogbookView

_cv: typing.TypeAlias = core.ConfigValidation

_LOG_MESSAGE_SCHEMA: typing.Final = vol.Schema(
    {
        vol.Required(core.Const.ATTR_NAME): _cv.string,
        vol.Required(Const.ATTR_MESSAGE): _cv.template,
        vol.Optional(core.Const.ATTR_DOMAIN): _cv.slug,
        vol.Optional(core.Const.ATTR_ENTITY_ID): _cv.entity_id,
    }
)
_MAX_PENDING_LOGBOOK_EVENTS: typing.Final = 2048
_EVENT_COALESCE_TIME: typing.Final = 0.35
_MAX_RECORDER_WAIT: typing.Final = 10
# minimum size that we will split the query
_BIG_QUERY_HOURS: typing.Final = 25
# how many hours to deliver in the first chunk when we split the query
_BIG_QUERY_RECENT_HOURS: typing.Final = 24
_LOGGER: typing.Final = logging.getLogger(__name__)

_GET_EVENTS: typing.Final = {
    vol.Required("type"): "logbook/get_events",
    vol.Required("start_time"): str,
    vol.Optional("end_time"): str,
    vol.Optional("entity_ids"): [str],
    vol.Optional("device_ids"): [str],
    vol.Optional("context_id"): str,
}
_EVENT_STREAM: typing.Final = {
    vol.Required("type"): "logbook/event_stream",
    vol.Required("start_time"): str,
    vol.Optional("end_time"): str,
    vol.Optional("entity_ids"): [str],
    vol.Optional("device_ids"): [str],
}


# pylint: disable=unused-variable
class LogbookComponent(core.LogbookComponent):
    """Event parser and human readable log generator."""

    def __init__(self, path: typing.Iterable[str]):
        super().__init__(path)

        # Format: event_name: (domain, LogbookPlatform Implementation)
        self._external_events: dict[str, tuple[str, core.LogbookPlatform]] = {}
        self._filters: core.RecorderFiltersBase = None
        self._entities_filter: core.EntityFilter = None
        self._recorder_component: core.RecorderComponent = None
        self._subscriptions: list[core.CallbackType] = []

    @property
    def filters(self) -> core.RecorderFiltersBase:
        return self._filters

    @property
    def entity_filters(self) -> core.EntityFilter:
        return self._entities_filter

    @property
    def recorder_component(self) -> core.RecorderComponent:
        return self._recorder_component

    @property
    def external_events(self) -> dict[str, tuple[str, core.LogbookPlatform]]:
        return self._external_events

    def log_entry(
        self,
        name: str,
        message: str,
        domain: str = None,
        entity_id: str = None,
        context: core.Context = None,
    ) -> None:
        """Add an entry to the logbook."""
        self._shc.add_job(
            self.async_log_entry, name, message, domain, entity_id, context
        )

    @core.callback
    def async_log_entry(
        self,
        name: str,
        message: str,
        domain: str = None,
        entity_id: str = None,
        context: core.Context = None,
    ) -> None:
        """Add an entry to the logbook."""
        data = {
            core.Const.LOGBOOK_ENTRY_NAME: name,
            core.Const.LOGBOOK_ENTRY_MESSAGE: message,
        }

        if domain is not None:
            data[Const.LOGBOOK_ENTRY_DOMAIN] = domain
        if entity_id is not None:
            data[core.Const.LOGBOOK_ENTRY_ENTITY_ID] = entity_id
        self._shc.bus.async_fire(core.Const.EVENT_LOGBOOK_ENTRY, data, context=context)

    @core.callback
    def _log_message(self, service: core.ServiceCall) -> None:
        """Handle sending notification message service calls."""
        message: core.Template = service.data[Const.ATTR_MESSAGE]
        name = service.data[Const.ATTR_NAME]
        domain = service.data.get(Const.ATTR_DOMAIN)
        entity_id = service.data.get(Const.ATTR_ENTITY_ID)

        if entity_id is None and domain is None:
            # If there is no entity_id or
            # domain, the event will get filtered
            # away so we use the "logbook" domain
            domain = self.domain

        # message wird durch MessageSchema zu Template
        message.controller = self._shc
        message = message.async_render(parse_result=False)

        self.async_log_entry(name, message, domain, entity_id, service.context)

    async def async_setup(self, config: core.ConfigType) -> bool:
        """Logbook setup."""
        if not await super().async_setup(config):
            return False

        api = self.controller.components.websocket_api
        if not isinstance(api, core.WebSocket.Component):
            return False

        comp = self.controller.components.frontend
        if isinstance(comp, core.FrontendComponent):
            comp.async_register_built_in_panel(
                self.domain, self.domain, "hass:format-list-bulleted-type"
            )

        comp = self.controller.components.recorder
        if isinstance(comp, core.RecorderComponent):
            self._recorder_component = comp

        recorder_conf = config.get(core.Const.RECORDER_COMPONENT_NAME, {})
        logbook_conf = config.get(self.domain, {})

        if self._recorder_component is not None:
            recorder_filter = comp.extract_include_exclude_filter_conf(recorder_conf)
            logbook_filter = comp.extract_include_exclude_filter_conf(logbook_conf)
            merged_filter = comp.merge_include_exclude_filters(
                recorder_filter, logbook_filter
            )

            possible_merged_entities_filter = (
                core.EntityFilter.convert_include_exclude_filter(merged_filter)
            )
            if not possible_merged_entities_filter.empty_filter:
                self._filters = comp.sqlalchemy_filter_from_include_exclude_conf(
                    merged_filter
                )
                self._entities_filter = possible_merged_entities_filter

        shc = self._shc

        # Set up the logbook websocket API.
        api.register_command(self._get_events, _GET_EVENTS)
        api.register_command(self._event_stream, _EVENT_STREAM)

        # Set up the logbook rest API.
        shc.register_view(LogbookView(self, config))

        shc.services.async_register(
            self.domain, "log", self._log_message, schema=_LOG_MESSAGE_SCHEMA
        )

        await shc.setup.async_process_integration_platforms(
            core.Platform.LOGBOOK, self._process_logbook_platform
        )

        return True

    async def _process_logbook_platform(
        self, domain: str, platform: core.PlatformImplementation
    ) -> None:
        """Process a logbook platform."""

        @core.callback
        def _async_describe_event(
            event_name: str,
        ) -> None:
            """Teach logbook how to describe a new event."""
            self._external_events[event_name] = (domain, platform)

        if isinstance(platform, core.LogbookPlatform):
            platform.async_describe_events(_async_describe_event)

    def async_determine_event_types(
        self, entity_ids: list[str], device_ids: list[str]
    ) -> tuple[str, ...]:
        """Reduce the event types based on the entity ids and device ids."""
        external_events = self._external_events

        if not entity_ids and not device_ids:
            return (*Const.ALL_EVENT_TYPES_EXCEPT_STATE_CHANGED, *external_events)

        config_entry_ids: set[str] = set()
        interested_event_types: set[str] = set()

        if entity_ids:
            #
            # Home Assistant doesn't allow firing events from
            # entities so we have a limited list to check
            #
            # automations and scripts can refer to entities
            # but they do not have a config entry so we need
            # to add them.
            #
            # We also allow entity_ids to be recorded via
            # manual logbook entries.
            #
            interested_event_types |= Const.ENTITY_EVENTS_WITHOUT_CONFIG_ENTRY

        if device_ids:
            dev_reg = self._shc.device_registry
            for device_id in device_ids:
                if (device := dev_reg.async_get(device_id)) and device.config_entries:
                    config_entry_ids |= device.config_entries
            interested_domains: set[str] = set()
            for entry_id in config_entry_ids:
                if entry := self._shc.config_entries.async_get_entry(entry_id):
                    interested_domains.add(entry.domain)
            for external_event, domain_call in external_events.items():
                if domain_call[0] in interested_domains:
                    interested_event_types.add(external_event)

        return tuple(
            event_type
            for event_type in (core.Const.EVENT_LOGBOOK_ENTRY, *external_events)
            if event_type in interested_event_types
        )

    def is_sensor_continuous(self, entity_id: str) -> bool:
        """Determine if a sensor is continuous by checking its state class.

        Sensors with a unit_of_measurement are also considered continuous, but are filtered
        already by the SQL query generated by _get_events
        """
        if not (entry := self._shc.entity_registry.async_get(entity_id)):
            # Entity not registered, so can't have a state class
            return False
        return (
            entry.capabilities is not None
            and entry.capabilities.get(core.Sensor.ATTR_STATE_CLASS) is not None
        )

    async def _event_stream(
        self,
        connection: core.WebSocket.Connection,
        msg: dict,
    ) -> None:
        """Handle logbook stream events websocket command."""
        start_time_str = msg["start_time"]
        msg_id: int = msg["id"]
        utc_now = core.helpers.utcnow()

        if start_time := core.helpers.parse_datetime(start_time_str):
            start_time = core.helpers.as_utc(start_time)

        if not start_time or start_time > utc_now:
            connection.send_error(msg_id, "invalid_start_time", "Invalid start_time")
            return

        end_time_str = msg.get("end_time")
        end_time: dt.datetime = None
        if end_time_str:
            if not (end_time := core.helpers.parse_datetime(end_time_str)):
                connection.send_error(msg_id, "invalid_end_time", "Invalid end_time")
                return
            end_time = core.helpers.as_utc(end_time)
            if end_time < start_time:
                connection.send_error(msg_id, "invalid_end_time", "Invalid end_time")
                return

        device_ids = msg.get("device_ids")
        entity_ids = msg.get("entity_ids")
        if entity_ids:
            entity_ids = self._async_filter_entities(entity_ids)
        event_types = self.async_determine_event_types(entity_ids, device_ids)
        event_processor = EventProcessor(
            self,
            event_types,
            entity_ids,
            device_ids,
            None,
            timestamp=True,
            include_entity_name=False,
        )

        if end_time and end_time <= utc_now:
            # Not live stream but we it might be a big query
            connection.subscriptions[msg_id] = core.callback(lambda: None)
            connection.send_result(msg_id)
            # Fetch everything from history
            await self._async_send_historical_events(
                connection,
                msg_id,
                start_time,
                end_time,
                connection.owner.event_message,
                event_processor,
                partial=False,
            )
            return

        subscriptions: list[core.CallbackType] = []
        stream_queue: asyncio.Queue[core.Event] = asyncio.Queue(
            _MAX_PENDING_LOGBOOK_EVENTS
        )
        live_stream = LogbookLiveStream(
            subscriptions=subscriptions, stream_queue=stream_queue
        )

        @core.callback
        def _unsub(*_time: typing.Any) -> None:
            """Unsubscribe from all events."""
            for subscription in subscriptions:
                subscription()
            subscriptions.clear()
            if live_stream.task:
                live_stream.task.cancel()
            if live_stream.end_time_unsub:
                live_stream.end_time_unsub()

        if end_time:
            live_stream.end_time_unsub = (
                self._shc.tracker.async_track_point_in_utc_time(_unsub, end_time)
            )

        @core.callback
        def _queue_or_cancel(event: core.Event) -> None:
            """Queue an event to be processed or cancel."""
            try:
                stream_queue.put_nowait(event)
            except asyncio.QueueFull:
                _LOGGER.debug(
                    "Client exceeded max pending messages of "
                    + f"{_MAX_PENDING_LOGBOOK_EVENTS}",
                )
                _unsub()

        self.async_subscribe_events(
            subscriptions, _queue_or_cancel, event_types, entity_ids, device_ids
        )
        subscriptions_setup_complete_time = core.helpers.utcnow()
        connection.subscriptions[msg_id] = _unsub
        connection.send_result(msg_id)
        # Fetch everything from history
        last_event_time = await self._async_send_historical_events(
            connection,
            msg_id,
            start_time,
            subscriptions_setup_complete_time,
            connection.owner.event_message,
            event_processor,
            partial=True,
        )

        await self._async_wait_for_recorder_sync()
        if msg_id not in connection.subscriptions:
            # Unsubscribe happened while waiting for recorder
            return

        #
        # Fetch any events from the database that have
        # not been committed since the original fetch
        # so we can switch over to using the subscriptions
        #
        # We only want events that happened after the last event
        # we had from the last database query or the maximum
        # time we allow the recorder to be behind
        #
        max_recorder_behind = subscriptions_setup_complete_time - dt.timedelta(
            seconds=_MAX_RECORDER_WAIT
        )
        second_fetch_start_time = max(
            last_event_time or max_recorder_behind, max_recorder_behind
        )
        await self._async_send_historical_events(
            connection,
            msg_id,
            second_fetch_start_time,
            subscriptions_setup_complete_time,
            connection.owner.event_message,
            event_processor,
            partial=False,
        )

        if not subscriptions:
            # Unsubscribe happened while waiting for formatted events
            # or there are no supported entities (all UOM or state class)
            # or devices
            return

        live_stream.task = asyncio.create_task(
            self._async_events_consumer(
                subscriptions_setup_complete_time,
                connection,
                msg_id,
                stream_queue,
                event_processor,
            )
        )

    async def _get_events(
        self,
        connection: core.WebSocket.Connection,
        msg: dict,
    ) -> None:
        """Handle logbook get events websocket command."""
        start_time_str = msg["start_time"]
        end_time_str = msg.get("end_time")
        utc_now = core.helpers.utcnow()

        if start_time := core.helpers.parse_datetime(start_time_str):
            start_time = core.helpers.as_utc(start_time)
        else:
            connection.send_error(msg["id"], "invalid_start_time", "Invalid start_time")
            return

        if not end_time_str:
            end_time = utc_now
        elif parsed_end_time := core.helpers.parse_datetime(end_time_str):
            end_time = core.helpers.as_utc(parsed_end_time)
        else:
            connection.send_error(msg["id"], "invalid_end_time", "Invalid end_time")
            return

        if start_time > utc_now:
            connection.send_result(msg["id"], [])
            return

        device_ids = msg.get("device_ids")
        entity_ids = msg.get("entity_ids")
        context_id = msg.get("context_id")
        if entity_ids:
            entity_ids = self._async_filter_entities(entity_ids)
            if not entity_ids and not device_ids:
                # Everything has been filtered away
                connection.send_result(msg["id"], [])
                return

        event_types = self.async_determine_event_types(entity_ids, device_ids)

        event_processor = EventProcessor(
            self,
            event_types,
            entity_ids,
            device_ids,
            context_id,
            timestamp=True,
            include_entity_name=False,
        )

        connection.send_message(
            await self._recorder_component.async_add_executor_job(
                _ws_formatted_get_events,
                connection.owner,
                msg["id"],
                start_time,
                end_time,
                event_processor,
            )
        )

    @core.callback
    def async_subscribe_events(
        self,
        subscriptions: list[core.CallbackType],
        target: collections.abc.Callable[[core.Event], None],
        event_types: tuple[str, ...],
        entity_ids: list[str],
        device_ids: list[str],
    ) -> None:
        """Subscribe to events for the entities and devices or all.

        These are the events we need to listen for to do
        the live logbook stream.
        """
        assert core.is_callback(target), "target must be a callback"
        event_forwarder = target

        if entity_ids or device_ids:
            entity_ids_set = set(entity_ids) if entity_ids else set()
            device_ids_set = set(device_ids) if device_ids else set()

            @core.callback
            def _forward_events_filtered(event: core.Event) -> None:
                event_data = event.data
                entity_included = False
                if entity_ids_set:
                    entity_ids = event_data.get(core.Const.ATTR_ENTITY_ID)
                    if isinstance(entity_ids, list):
                        for entry in entity_ids:
                            if entry in entity_ids_set:
                                entity_included = True
                                break
                    else:
                        entity_included = entity_ids in entity_ids_set
                if entity_included or (
                    device_ids_set
                    and event_data.get(core.Const.ATTR_DEVICE_ID) in device_ids_set
                ):
                    target(event)

            event_forwarder = _forward_events_filtered

        for event_type in event_types:
            subscriptions.append(
                self._shc.bus.async_listen(
                    event_type, event_forwarder, run_immediately=True
                )
            )

        @core.callback
        def _forward_state_events_filtered(event: core.Event) -> None:
            if (
                event.data.get("old_state") is None
                or event.data.get("new_state") is None
            ):
                return
            state: core.State = event.data["new_state"]
            if not self._is_state_filtered(state):
                target(event)

        if device_ids and not entity_ids:
            # No entities to subscribe to but we are filtering
            # on device ids so we do not want to get any state
            # changed events
            return

        if entity_ids:
            subscriptions.append(
                self._shc.tracker.async_track_state_change_event(
                    entity_ids, _forward_state_events_filtered
                )
            )
            return

        # We want the firehose
        subscriptions.append(
            self._shc.bus.async_listen(
                core.Const.EVENT_STATE_CHANGED,
                _forward_state_events_filtered,
                run_immediately=True,
            )
        )

    def _is_state_filtered(self, state: core.State) -> bool:
        """Check if the logbook should filter a state.

        Used when we are in live mode to ensure
        we only get significant changes (state.last_changed != state.last_updated)
        """
        return bool(
            state.last_changed != state.last_updated
            or core.Const.ATTR_UNIT_OF_MEASUREMENT in state.attributes
            or self.is_sensor_continuous(state.entity_id)
        )

    def _is_entity_id_filtered(self, entity_id: str) -> bool:
        """Check if the logbook should filter an entity.

        Used to setup listeners and which entities to select
        from the database when a list of entities is requested.
        """
        return bool(
            (state := self._shc.states.get(entity_id))
            and (core.Const.ATTR_UNIT_OF_MEASUREMENT in state.attributes)
            or self.is_sensor_continuous(entity_id)
        )

    def _async_filter_entities(self, entity_ids: list[str]) -> list[str]:
        """Filter out any entities that logbook will not produce results for."""
        return [
            entity_id
            for entity_id in entity_ids
            if not self._is_entity_id_filtered(entity_id)
        ]

    async def _async_send_historical_events(
        self,
        connection: core.WebSocket.Connection,
        msg_id: int,
        start_time: dt,
        end_time: dt,
        formatter: collections.abc.Callable[[int, typing.Any], dict[str, typing.Any]],
        event_processor: EventProcessor,
        partial: bool,
    ) -> dt.datetime:
        """Select historical data from the database and deliver it to the websocket.

        If the query is considered a big query we will split the request into
        two chunks so that they get the recent events first and the select
        that is expected to take a long time comes in after to ensure
        they are not stuck at a loading screen and can start looking at
        the data right away.

        This function returns the time of the most recent event we sent to the
        websocket.
        """
        is_big_query = (
            not event_processor.entity_ids
            and not event_processor.device_ids
            and ((end_time - start_time) > dt.timedelta(hours=_BIG_QUERY_HOURS))
        )

        if not is_big_query:
            message, last_event_time = await self._async_get_ws_stream_events(
                msg_id,
                start_time,
                end_time,
                formatter,
                event_processor,
                partial,
            )
            # If there is no last_event_time, there are no historical
            # results, but we still send an empty message
            # if its the last one (not partial) so
            # consumers of the api know their request was
            # answered but there were no results
            if last_event_time or not partial:
                connection.send_message(message)
            return last_event_time

        # This is a big query so we deliver
        # the first three hours and then
        # we fetch the old data
        recent_query_start = end_time - dt.timedelta(hours=_BIG_QUERY_RECENT_HOURS)
        (
            recent_message,
            recent_query_last_event_time,
        ) = await self._async_get_ws_stream_events(
            msg_id,
            recent_query_start,
            end_time,
            formatter,
            event_processor,
            partial=True,
        )
        if recent_query_last_event_time:
            connection.send_message(recent_message)

        (
            older_message,
            older_query_last_event_time,
        ) = await self._async_get_ws_stream_events(
            msg_id,
            start_time,
            recent_query_start,
            formatter,
            event_processor,
            partial,
        )
        # If there is no last_event_time, there are no historical
        # results, but we still send an empty message
        # if its the last one (not partial) so
        # consumers of the api know their request was
        # answered but there were no results
        if older_query_last_event_time or not partial:
            connection.send_message(older_message)

        # Returns the time of the newest event
        return recent_query_last_event_time or older_query_last_event_time

    async def _async_wait_for_recorder_sync(self) -> None:
        """Wait for the recorder to sync."""
        if not self._recorder_component:
            raise NotImplementedError()

        try:
            await asyncio.wait_for(
                self._recorder_component.async_block_till_done(), _MAX_RECORDER_WAIT
            )
        except asyncio.TimeoutError:
            _LOGGER.debug(
                f"Recorder is behind more than {_MAX_RECORDER_WAIT} seconds, "
                + "starting live stream; Some results may be missing"
            )

    async def _async_get_ws_stream_events(
        self,
        msg_id: int,
        start_time: dt.datetime,
        end_time: dt.datetime,
        formatter: collections.abc.Callable[[int, typing.Any], dict[str, typing.Any]],
        event_processor: EventProcessor,
        partial: bool,
    ) -> tuple[str, dt.datetime]:
        """Async wrapper around _ws_formatted_get_events."""
        if not self._recorder_component:
            raise NotImplementedError()

        return await self._recorder_component.async_add_executor_job(
            _ws_stream_get_events,
            msg_id,
            start_time,
            end_time,
            formatter,
            event_processor,
            partial,
        )

    async def _async_events_consumer(
        self,
        subscriptions_setup_complete_time: dt.datetime,
        connection: core.WebSocket.Connection,
        msg_id: int,
        stream_queue: asyncio.Queue[core.Event],
        event_processor: EventProcessor,
    ) -> None:
        """Stream events from the queue."""
        event_processor.switch_to_live()

        while True:
            events: list[core.Event] = [await stream_queue.get()]
            # If the event is older than the last db
            # event we already sent it so we skip it.
            if events[0].time_fired <= subscriptions_setup_complete_time:
                continue
            # We sleep for the EVENT_COALESCE_TIME so
            # we can group events together to minimize
            # the number of websocket messages when the
            # system is overloaded with an event storm
            await asyncio.sleep(_EVENT_COALESCE_TIME)
            while not stream_queue.empty():
                events.append(stream_queue.get_nowait())

            if logbook_events := event_processor.humanify(
                model.async_event_to_row(e, self._external_events) for e in events
            ):
                connection.send_message(
                    core.Const.JSON_DUMP(
                        connection.owner.event_message(
                            msg_id,
                            {"events": logbook_events},
                        )
                    )
                )


def _ws_stream_get_events(
    msg_id: int,
    start_day: dt,
    end_day: dt,
    formatter: collections.abc.Callable[[int, typing.Any], dict[str, typing.Any]],
    event_processor: EventProcessor,
    partial: bool,
) -> tuple[str, dt.datetime]:
    """Fetch events and convert them to json in the executor."""
    events = event_processor.get_events(start_day, end_day)
    last_time = None
    if events:
        last_time = core.helpers.utc_from_timestamp(events[-1]["when"])
    message = {
        "events": events,
        "start_time": core.helpers.utc_to_timestamp(start_day),
        "end_time": core.helpers.utc_to_timestamp(end_day),
    }
    if partial:
        # This is a hint to consumers of the api that
        # we are about to send a another block of historical
        # data in case the UI needs to show that historical
        # data is still loading in the future
        message["partial"] = True
    return core.Const.JSON_DUMP(formatter(msg_id, message)), last_time


def _ws_formatted_get_events(
    comp: core.WebSocket.Component,
    msg_id: int,
    start_time: dt.datetime,
    end_time: dt.datetime,
    event_processor: EventProcessor,
) -> str:
    """Fetch events and convert them to json in the executor."""
    return core.Const.JSON_DUMP(
        comp.result_message(msg_id, event_processor.get_events(start_time, end_time))
    )
