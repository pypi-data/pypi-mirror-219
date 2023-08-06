"""
Core components of Smart Home - The Next Generation.

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


import abc
import asyncio
import collections.abc
import typing

from .abort_flow import AbortFlow
from .base_service_info import BaseServiceInfo
from .callback import callback
from .flow_handler import FlowHandler
from .flow_result import FlowResult
from .flow_result_type import FlowResultType
from .unknown_flow import UnknownFlow
from .unknown_step import UnknownStep


if not typing.TYPE_CHECKING:

    class SmartHomeController:
        ...


if typing.TYPE_CHECKING:
    from .smart_home_controller import SmartHomeController


# pylint: disable=unused-variable
class FlowManager(abc.ABC):
    """Manage all the flows that are in progress."""

    def __init__(
        self,
        shc: SmartHomeController,
    ) -> None:
        """Initialize the flow manager."""
        self._shc = shc
        self._initializing: dict[str, list[asyncio.Future]] = {}
        self._initialize_tasks: dict[str, list[asyncio.Task]] = {}
        self._progress: dict[str, FlowHandler] = {}
        self._handler_progress_index: dict[str, set[str]] = {}

    async def async_wait_init_flow_finish(self, handler: str) -> None:
        """Wait till all flows in progress are initialized."""
        if not (current := self._initializing.get(handler)):
            return

        await asyncio.wait(current)

    @abc.abstractmethod
    async def async_create_flow(
        self,
        handler_key: typing.Any,
        *,
        context: dict[str, typing.Any] = None,
        data: dict[str, typing.Any] = None,
    ) -> FlowHandler:
        """Create a flow for specified handler.

        Handler key is the domain of the component that we want to set up.
        """

    @abc.abstractmethod
    async def async_finish_flow(
        self, flow: FlowHandler, result: FlowResult
    ) -> FlowResult:
        """Finish a config flow and add an entry."""

    @abc.abstractmethod
    async def async_post_init(self, flow: FlowHandler, result: FlowResult) -> None:
        """Entry has finished executing its first step asynchronously."""

    @callback
    def async_has_matching_flow(
        self, handler: str, context: dict[str, typing.Any], data: typing.Any
    ) -> bool:
        """
        Check if an existing matching flow is in progress with the same handler,
        context, and data.
        """
        return any(
            flow
            for flow in self._async_progress_by_handler(handler)
            if flow.context["source"] == context["source"] and flow.init_data == data
        )

    @callback
    def async_get(self, flow_id: str) -> FlowResult:
        """Return a flow in progress as a partial FlowResult."""
        if (flow := self._progress.get(flow_id)) is None:
            raise UnknownFlow
        return self._async_flow_handler_to_flow_result([flow], False)[0]

    @callback
    @staticmethod
    def _async_flow_handler_to_flow_result(
        flows: collections.abc.Iterable[FlowHandler], include_uninitialized: bool
    ) -> list[FlowResult]:
        """Convert a list of FlowHandler to a partial FlowResult that can be serialized."""
        return [
            {
                "flow_id": flow.flow_id,
                "handler": flow.handler,
                "context": flow.context,
                "step_id": flow.cur_step["step_id"] if flow.cur_step else None,
            }
            for flow in flows
            if include_uninitialized or flow.cur_step is not None
        ]

    @callback
    def async_progress(self, include_uninitialized: bool = False) -> list[FlowResult]:
        """Return the flows in progress as a partial FlowResult."""
        return self._async_flow_handler_to_flow_result(
            self._progress.values(), include_uninitialized
        )

    @callback
    def async_progress_by_handler(
        self, handler: str, include_uninitialized: bool = False
    ) -> list[FlowResult]:
        """Return the flows in progress by handler as a partial FlowResult."""
        return self._async_flow_handler_to_flow_result(
            self._async_progress_by_handler(handler), include_uninitialized
        )

    @callback
    def _async_progress_by_handler(self, handler: str) -> list[FlowHandler]:
        """Return the flows in progress by handler."""
        return [
            self._progress[flow_id]
            for flow_id in self._handler_progress_index.get(handler, {})
        ]

    async def async_init(
        self,
        handler: str,
        *,
        context: dict[str, typing.Any] = None,
        data: typing.Any = None,
    ) -> FlowResult:
        """Start a configuration flow."""
        if context is None:
            context = {}

        init_done: asyncio.Future = asyncio.Future()
        self._initializing.setdefault(handler, []).append(init_done)

        task = asyncio.create_task(self._async_init(init_done, handler, context, data))
        self._initialize_tasks.setdefault(handler, []).append(task)

        try:
            flow, result = await task
        finally:
            self._initialize_tasks[handler].remove(task)
            self._initializing[handler].remove(init_done)

        if result["type"] != FlowResultType.ABORT:
            await self.async_post_init(flow, result)

        return result

    async def _async_init(
        self,
        init_done: asyncio.Future,
        handler: typing.Any,
        context: dict,
        data: typing.Any,
    ) -> tuple[FlowHandler, FlowResult]:
        """Run the init in a task to allow it to be canceled at shutdown."""
        flow = await self.async_create_flow(handler, context=context, data=data)
        if not flow:
            raise UnknownFlow("Flow was not created")
        self._async_add_flow_progress(flow)
        result = await self._async_handle_step(flow, flow.init_step, data, init_done)
        return flow, result

    async def async_shutdown(self) -> None:
        """Cancel any initializing flows."""
        for task_list in self._initialize_tasks.values():
            for task in task_list:
                task.cancel()

    async def async_configure(
        self, flow_id: str, user_input: dict = None
    ) -> FlowResult:
        """Continue a configuration flow."""
        if (flow := self._progress.get(flow_id)) is None:
            raise UnknownFlow

        cur_step = flow.cur_step
        assert cur_step is not None

        if cur_step.get("data_schema") is not None and user_input is not None:
            user_input = cur_step["data_schema"](user_input)

        # Handle a menu navigation choice
        if cur_step["type"] == FlowResultType.MENU and user_input:
            result = await self._async_handle_step(
                flow, user_input["next_step_id"], None
            )
        else:
            result = await self._async_handle_step(
                flow, cur_step["step_id"], user_input
            )

        if cur_step["type"] in (FlowResultType.EXTERNAL, FlowResultType.SHOW_PROGRESS):
            if cur_step["type"] == FlowResultType.EXTERNAL and result["type"] not in (
                FlowResultType.EXTERNAL,
                FlowResultType.EXTERNAL_DONE,
            ):
                raise ValueError(
                    "External step can only transition to "
                    + "external step or external step done."
                )
            if cur_step["type"] == FlowResultType.SHOW_PROGRESS and result[
                "type"
            ] not in (
                FlowResultType.SHOW_PROGRESS,
                FlowResultType.SHOW_PROGRESS_DONE,
            ):
                raise ValueError(
                    "Show progress can only transition to show progress or show progress done."
                )

            # If the result has changed from last result, fire event to update
            # the frontend.
            if (
                cur_step["step_id"] != result.get("step_id")
                or result["type"] == FlowResultType.SHOW_PROGRESS
            ):
                # Tell frontend to reload the flow state.
                self._shc.bus.async_fire(
                    FlowHandler.EVENT_DATA_ENTRY_FLOW_PROGRESSED,
                    {"handler": flow.handler, "flow_id": flow_id, "refresh": True},
                )

        return result

    @callback
    def async_abort(self, flow_id: str) -> None:
        """Abort a flow."""
        self._async_remove_flow_progress(flow_id)

    @callback
    def _async_add_flow_progress(self, flow: FlowHandler) -> None:
        """Add a flow to in progress."""
        self._progress[flow.flow_id] = flow
        self._handler_progress_index.setdefault(flow.handler, set()).add(flow.flow_id)

    @callback
    def _async_remove_flow_progress(self, flow_id: str) -> None:
        """Remove a flow from in progress."""
        if (flow := self._progress.pop(flow_id, None)) is None:
            raise UnknownFlow
        handler = flow.handler
        self._handler_progress_index[handler].remove(flow.flow_id)
        if not self._handler_progress_index[handler]:
            del self._handler_progress_index[handler]

    async def _async_handle_step(
        self,
        flow: FlowHandler,
        step_id: str,
        user_input: dict | BaseServiceInfo,
        step_done: asyncio.Future = None,
    ) -> FlowResult:
        """Handle a step of a flow."""
        method = f"async_step_{step_id}"

        if not hasattr(flow, method):
            self._async_remove_flow_progress(flow.flow_id)
            if step_done:
                step_done.set_result(None)
            raise UnknownStep(
                f"Handler {flow.__class__.__name__} doesn't support step {step_id}"
            )

        try:
            result: FlowResult = await getattr(flow, method)(user_input)
        except AbortFlow as err:
            result = flow.create_abort_data(err.reason, err.description_placeholders)

        # Mark the step as done.
        # We do this before calling async_finish_flow because config entries will hit a
        # circular dependency where async_finish_flow sets up new entry, which needs the
        # integration to be set up, which is waiting for init to be done.
        if step_done:
            step_done.set_result(None)

        if result["type"] not in (
            FlowResultType.FORM,
            FlowResultType.EXTERNAL,
            FlowResultType.CREATE_ENTRY,
            FlowResultType.ABORT,
            FlowResultType.EXTERNAL_DONE,
            FlowResultType.SHOW_PROGRESS,
            FlowResultType.SHOW_PROGRESS_DONE,
            FlowResultType.MENU,
        ):
            raise ValueError(f"Handler returned incorrect type: {result['type']}")

        if result["type"] in (
            FlowResultType.FORM,
            FlowResultType.EXTERNAL,
            FlowResultType.EXTERNAL_DONE,
            FlowResultType.SHOW_PROGRESS,
            FlowResultType.SHOW_PROGRESS_DONE,
            FlowResultType.MENU,
        ):
            flow.set_result(result)
            return result

        # We pass a copy of the result because we're mutating our version
        result = await self.async_finish_flow(flow, result.copy())

        # _async_finish_flow may change result type, check it again
        if result["type"] == FlowResultType.FORM:
            flow.set_result(result)
            return result

        # Abort and Success results both finish the flow
        self._async_remove_flow_progress(flow.flow_id)

        return result
