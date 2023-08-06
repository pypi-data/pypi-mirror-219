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

import collections.abc
import typing

from . import helpers
from .callback import callback
from .const import Const
from .core_state import CoreState
from .event import Event
from .flow_result import FlowResult

_FLOW_INIT_LIMIT: typing.Final = 2

if not typing.TYPE_CHECKING:

    class SmartHomeController:
        ...


if typing.TYPE_CHECKING:
    from .smart_home_controller import SmartHomeController


# pylint: disable=unused-variable
class FlowDispatcher:
    """Dispatch discovery flows."""

    def __init__(self, shc: SmartHomeController) -> None:
        """Init the discovery dispatcher."""
        self._shc = shc
        self._pending_flows: list[tuple[str, dict[str, typing.Any], typing.Any]] = []

    @callback
    def async_setup(self) -> None:
        """Set up the flow disptcher."""
        if not self._shc.state == CoreState.RUNNING:
            self._shc.bus.async_listen_once(Const.EVENT_SHC_STARTED, self._async_start)

    @callback
    def _async_start(self, _event: Event) -> None:
        """Start processing pending flows."""
        self._shc.async_create_task(self._async_process_pending_flows())

    async def _async_process_pending_flows(self) -> None:
        """Process any pending discovery flows."""
        init_coros = [self._async_init_flow(*flow) for flow in self._pending_flows]
        await helpers.gather_with_concurrency(
            _FLOW_INIT_LIMIT,
            *[init_coro for init_coro in init_coros if init_coro is not None],
        )

    @callback
    def _async_create(
        self, domain: str, context: dict[str, typing.Any], data: typing.Any
    ) -> None:
        """Create and add or queue a flow."""
        self._pending_flows.append((domain, context, data))

    @callback
    def create_flow(
        self, domain: str, context: dict[str, typing.Any], data: typing.Any
    ) -> None:
        """Create a discovery flow."""
        if self._shc.state == CoreState.RUNNING:
            if init_coro := self._async_init_flow(domain, context, data):
                self._shc.async_create_task(init_coro)
            return None

        return self._async_create(domain, context, data)

    @callback
    def _async_init_flow(
        self, domain: str, context: dict[str, typing.Any], data: typing.Any
    ) -> collections.abc.Coroutine[None, None, FlowResult]:
        """Create a discovery flow."""
        # Avoid spawning flows that have the same initial discovery data
        # as ones in progress as it may cause additional device probing
        # which can overload devices since zeroconf/ssdp updates can happen
        # multiple times in the same minute
        if self._shc.config_entries.flow.async_has_matching_flow(domain, context, data):
            return None

        return self._shc.config_entries.flow.async_init(
            domain, context=context, data=data
        )
