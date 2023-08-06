"""
Trace Component for Smart Home - The Next Generation.

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

import json
import logging
import typing

import voluptuous as vol

from ... import core
from .limited_size_dict import LimitedSizeDict

_LOGGER: typing.Final = logging.getLogger(__name__)
_STORAGE_KEY: typing.Final = "saved_traces"
_TRACE_DOMAINS: typing.Final = (
    "automation",
    "script",
)

_TRACE_GET: typing.Final = {
    vol.Required("type"): "trace/get",
    vol.Required("domain"): vol.In(_TRACE_DOMAINS),
    vol.Required("item_id"): str,
    vol.Required("run_id"): str,
}
_TRACE_LIST: typing.Final = {
    vol.Required("type"): "trace/list",
    vol.Required("domain", "id"): vol.In(_TRACE_DOMAINS),
    vol.Optional("item_id", "id"): str,
}
_TRACE_CONTEXTS: typing.Final = {
    vol.Required("type"): "trace/contexts",
    vol.Inclusive("domain", "id"): vol.In(_TRACE_DOMAINS),
    vol.Inclusive("item_id", "id"): str,
}
_BREAKPOINT_CLEAR: typing.Final = {
    vol.Required("type"): "trace/debug/breakpoint/clear",
    vol.Required("domain"): vol.In(_TRACE_DOMAINS),
    vol.Required("item_id"): str,
    vol.Required("node"): str,
    vol.Optional("run_id"): str,
}
_BREAKPOINT_LIST: typing.Final = {vol.Required("type"): "trace/debug/breakpoint/list"}
_BREAKPOINT_SET: typing.Final = {
    vol.Required("type"): "trace/debug/breakpoint/set",
    vol.Required("domain"): vol.In(_TRACE_DOMAINS),
    vol.Required("item_id"): str,
    vol.Required("node"): str,
    vol.Optional("run_id"): str,
}
_DEBUG_CONTINUE: typing.Final = {
    vol.Required("type"): "trace/debug/continue",
    vol.Required("domain"): vol.In(_TRACE_DOMAINS),
    vol.Required("item_id"): str,
    vol.Required("run_id"): str,
}
_DEBUG_STEP: typing.Final = {
    vol.Required("type"): "trace/debug/step",
    vol.Required("domain"): vol.In(_TRACE_DOMAINS),
    vol.Required("item_id"): str,
    vol.Required("run_id"): str,
}
_DEBUG_STOP: typing.Final = {
    vol.Required("type"): "trace/debug/stop",
    vol.Required("domain"): vol.In(_TRACE_DOMAINS),
    vol.Required("item_id"): str,
    vol.Required("run_id"): str,
}
_DEBUG_SUBSCRIBE: typing.Final = {
    vol.Required("type"): "trace/debug/breakpoint/subscribe"
}


# pylint: disable=unused-variable
class Trace(core.TraceComponent):
    """Support for script and automation tracing and debugging."""

    def __init__(self, path: typing.Iterable[str]):
        super().__init__(path)
        self._store: core.Store = None
        self._trace_data: dict[str, dict[str, core.TraceBase]] = {}
        self._data_restored = False

    @property
    def storage_key(self) -> str:
        return self.domain + "." + _STORAGE_KEY

    def store_trace(self, trace: core.TraceBase, stored_traces: int):
        """Store the trace."""
        if key := trace.key:
            traces = self._trace_data
            if key not in traces:
                traces[key] = LimitedSizeDict(size_limit=stored_traces)
            traces[key][trace.run_id] = trace

    async def async_setup(self, config: core.ConfigType) -> bool:
        """Initialize the trace integration."""
        if not await super().async_setup(config):
            return False

        api = self.controller.components.websocket_api
        if not isinstance(api, core.WebSocket.Component):
            return False

        self._register_websocket_commands(api)
        self._store = core.Store[dict[str, list]](
            self._shc,
            self.storage_version,
            self.storage_key,
            encoder=core.ExtendedJsonEncoder,
        )

        # Store traces when stopping hass
        self._shc.bus.async_listen_once(
            core.Const.EVENT_SHC_STOP, self._async_store_traces_at_stop
        )

        return True

    async def _async_store_traces_at_stop(self, *_) -> None:
        """Save traces to storage."""
        _LOGGER.debug("Storing traces")
        try:
            await self._store.async_save(
                {key: list(traces.values()) for key, traces in self._trace_data.items()}
            )
        except core.SmartHomeControllerError as exc:
            _LOGGER.error("Error storing traces", exc_info=exc)

    def _register_websocket_commands(self, api: core.WebSocket.Component):
        """Set up the websocket API."""
        api.register_command(self._trace_get, _TRACE_GET)
        api.register_command(self._trace_list, _TRACE_LIST)
        api.register_command(self._trace_contexts, _TRACE_CONTEXTS)
        api.register_command(self._breakpoint_clear, _BREAKPOINT_CLEAR)
        api.register_command(self._breakpoint_list, _BREAKPOINT_LIST)
        api.register_command(self._breakpoint_set, _BREAKPOINT_SET)
        api.register_command(self._debug_continue, _DEBUG_CONTINUE)
        api.register_command(self._debug_step, _DEBUG_STEP)
        api.register_command(self._debug_stop, _DEBUG_STOP)
        api.register_command(self._subscribe_breakpoint_events, _DEBUG_SUBSCRIBE)

    async def _trace_get(
        self,
        connection: core.WebSocket.Connection,
        msg: dict,
    ):
        """Get a script or automation trace."""
        connection.require_admin()
        key = f"{msg['domain']}.{msg['item_id']}"
        run_id = msg["run_id"]

        try:
            requested_trace = await self.async_get_trace(key, run_id)
        except KeyError:
            connection.send_error(
                msg["id"],
                core.WebSocket.ERR_NOT_FOUND,
                "The trace could not be found",
            )
            return

        message = connection.owner.result_message(msg["id"], requested_trace)

        connection.send_message(
            json.dumps(message, cls=core.ExtendedJsonEncoder, allow_nan=False)
        )

    async def _trace_list(
        self,
        connection: core.WebSocket.Connection,
        msg: dict,
    ):
        """Summarize script and automation traces."""
        connection.require_admin()

        wanted_domain = msg["domain"]
        key = f"{msg['domain']}.{msg['item_id']}" if "item_id" in msg else None

        traces = await self.async_list_traces(wanted_domain, key)

        connection.send_result(msg["id"], traces)

    async def _trace_contexts(
        self,
        connection: core.WebSocket.Connection,
        msg: dict,
    ):
        """Retrieve contexts we have traces for."""
        connection.require_admin()

        key = f"{msg['domain']}.{msg['item_id']}" if "item_id" in msg else None

        contexts = await self.async_list_contexts(key)

        connection.send_result(msg["id"], contexts)

    @core.callback
    def _breakpoint_set(
        self,
        connection: core.WebSocket.Connection,
        msg: dict,
    ):
        """Set breakpoint."""
        connection.require_admin()

        shc = connection.owner.controller
        key = f"{msg['domain']}.{msg['item_id']}"
        node = msg["node"]
        run_id = msg.get("run_id")

        breakpoint_hit = core.Scripts.Const.SCRIPT_BREAKPOINT_HIT
        if not shc.dispatcher.has_signal_subscription(breakpoint_hit):
            raise core.SmartHomeControllerError("No breakpoint subscription")

        result = core.Scripts.breakpoint_set(key, run_id, node)
        connection.send_result(msg["id"], result)

    @core.callback
    def _breakpoint_clear(
        self,
        connection: core.WebSocket.Connection,
        msg: dict,
    ):
        """Clear breakpoint."""
        connection.require_admin()

        key = f"{msg['domain']}.{msg['item_id']}"
        node = msg["node"]
        run_id = msg.get("run_id")

        result = core.Scripts.breakpoint_clear(key, run_id, node)

        connection.send_result(msg["id"], result)

    def _breakpoint_list(
        self,
        connection: core.WebSocket.Connection,
        msg: dict,
    ):
        """List breakpoints."""
        connection.require_admin()

        breakpoints = core.Scripts.breakpoint_list()
        for _breakpoint in breakpoints:
            key = _breakpoint.pop("key")
            _breakpoint["domain"], _breakpoint["item_id"] = key.split(".", 1)

        connection.send_result(msg["id"], breakpoints)

    @core.callback
    def _subscribe_breakpoint_events(
        self,
        connection: core.WebSocket.Connection,
        msg: dict,
    ):
        """Subscribe to breakpoint events."""
        connection.require_admin()

        hit = core.Scripts.Const.SCRIPT_BREAKPOINT_HIT
        shc = connection.owner.controller

        @core.callback
        def breakpoint_hit(key, run_id, node):
            """Forward events to websocket."""
            domain, item_id = key.split(".", 1)
            connection.send_event_message(
                msg["id"],
                {
                    "domain": domain,
                    "item_id": item_id,
                    "run_id": run_id,
                    "node": node,
                },
            )

        remove_signal = shc.dispatcher.async_connect(hit, breakpoint_hit)

        @core.callback
        def unsub():
            """Unsubscribe from breakpoint events."""
            remove_signal()
            if not shc.dispatcher.has_signal_subscription(hit):
                core.Scripts.breakpoint_clear_all()
                shc.dispatcher.async_send(core.Scripts.Const.SCRIPT_DEBUG_CONTINUE_ALL)

        connection.subscriptions[msg["id"]] = unsub

        connection.send_result(msg["id"])

    @core.callback
    def _debug_continue(
        self,
        connection: core.WebSocket.Connection,
        msg: dict,
    ):
        """Resume execution of halted script or automation."""
        connection.require_admin()

        shc = connection.owner.controller
        key = f"{msg['domain']}.{msg['item_id']}"
        run_id = msg["run_id"]

        result = core.Scripts.debug_continue(shc, key, run_id)

        connection.send_result(msg["id"], result)

    @core.callback
    def _debug_step(
        self,
        connection: core.WebSocket.Connection,
        msg: dict,
    ):
        """Single step a halted script or automation."""
        connection.require_admin()

        shc = connection.owner.controller
        key = f"{msg['domain']}.{msg['item_id']}"
        run_id = msg["run_id"]

        result = core.Scripts.debug_step(shc, key, run_id)

        connection.send_result(msg["id"], result)

    @core.callback
    def _debug_stop(
        self,
        connection: core.WebSocket.Connection,
        msg: dict,
    ):
        """Stop a halted script or automation."""
        connection.require_admin()

        shc = connection.owner.controller
        key = f"{msg['domain']}.{msg['item_id']}"
        run_id = msg["run_id"]

        result = core.Scripts.debug_stop(shc, key, run_id)

        connection.send_result(msg["id"], result)

    async def async_get_trace(self, key, run_id):
        """Return the requested trace."""
        # Restore saved traces if not done
        await self.async_restore_traces()

        return self._trace_data[key][run_id].as_extended_dict()

    async def async_list_contexts(self, key):
        """List contexts for which we have traces."""
        # Restore saved traces if not done
        await self.async_restore_traces()

        if key is not None:
            values = self._trace_data.get(key, {})
        else:
            values = self._trace_data

        def _trace_id(run_id, key) -> dict:
            """Make trace_id for the response."""
            domain, item_id = key.split(".", 1)
            return {"run_id": run_id, "domain": domain, "item_id": item_id}

        return {
            trace.context.context_id: _trace_id(trace.run_id, key)
            for key, traces in values.items()
            for trace in traces.values()
        }

    def _get_debug_traces(self, key):
        """Return a serializable list of debug traces for a script or automation."""
        traces = []

        for trace in self._trace_data.get(key, {}).values():
            traces.append(trace.as_short_dict())

        return traces

    async def async_list_traces(self, wanted_domain, wanted_key):
        """List traces for a domain."""
        # Restore saved traces if not done already
        await self.async_restore_traces()

        if not wanted_key:
            traces = []
            for key in self._trace_data:
                domain = key.split(".", 1)[0]
                if domain == wanted_domain:
                    traces.extend(self._get_debug_traces(key))
        else:
            traces = self._get_debug_traces(wanted_key)

        return traces

    def async_store_trace(self, trace: core.TraceBase, stored_traces: int):
        """Store a trace if its key is valid."""
        if key := trace.key:
            traces = self._trace_data
            if key not in traces:
                traces[key] = LimitedSizeDict(size_limit=stored_traces)
            else:
                traces[key].size_limit = stored_traces
            traces[key][trace.run_id] = trace

    def _async_store_restored_trace(self, trace):
        """Store a restored trace and move it to the end of the LimitedSizeDict."""
        key = trace.key
        traces = self._trace_data
        if key not in traces:
            traces[key] = LimitedSizeDict()
        traces[key][trace.run_id] = trace
        traces[key].move_to_end(trace.run_id, last=False)

    async def async_restore_traces(self):
        """Restore saved traces."""
        if self._data_restored:
            return

        self._data_restored = True

        store = self._store
        try:
            restored_traces = await store.async_load() or {}
        except core.SmartHomeControllerError:
            _LOGGER.exception("Error loading traces")
            restored_traces = {}

        for key, traces in restored_traces.items():
            # Add stored traces in reversed order to priorize the newest traces
            for json_trace in reversed(traces):
                if (
                    (stored_traces := self._trace_data.get(key))
                    and stored_traces.size_limit is not None
                    and len(stored_traces) >= stored_traces.size_limit
                ):
                    break

                try:
                    trace = core.RestoredTrace(json_trace)
                # Catch any exception to not blow up if the stored trace is invalid
                except Exception:  # pylint: disable=broad-except
                    _LOGGER.exception("Failed to restore trace")
                    continue
                self._async_store_restored_trace(trace)
