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

import typing

from .config_flow import _CONFIG_HANDLERS
from .config_flow_platform import ConfigFlowPlatform
from .flow_handler import FlowHandler
from .flow_manager import FlowManager
from .flow_result import FlowResult
from .flow_result_type import FlowResultType
from .options_flow import OptionsFlow
from .platform import Platform
from .smart_home_controller_component import SmartHomeControllerComponent
from .unknown_entry import UnknownEntry
from .unknown_handler import UnknownHandler


# pylint: disable=unused-variable
class OptionsFlowManager(FlowManager):
    """Flow to set options for a configuration entry."""

    async def async_create_flow(
        self,
        handler_key: typing.Any,
        *,
        context: dict[str, typing.Any] = None,
        data: dict[str, typing.Any] = None,
    ) -> FlowHandler:
        """Create an options flow for a config entry.

        Entry_id and flow.handler is the same thing to map entry with flow.
        """
        entry = self._shc.config_entries.async_get_entry(handler_key)
        if entry is None:
            raise UnknownEntry(handler_key)

        config_flow = None
        if entry.domain not in _CONFIG_HANDLERS:
            comp = SmartHomeControllerComponent.get_component(entry.domain)
            if isinstance(comp, SmartHomeControllerComponent):
                platform = comp.get_platform(Platform.CONFIG_FLOW)
                if isinstance(platform, ConfigFlowPlatform):
                    config_flow = platform
            if config_flow is None:
                raise UnknownHandler
        else:
            config_flow = _CONFIG_HANDLERS[entry.domain]

        return await config_flow.async_get_options_flow(entry, context, data)

    async def async_finish_flow(
        self, flow: FlowHandler, result: FlowResult
    ) -> FlowResult:
        """Finish an options flow and update options for configuration entry.

        Flow.handler and entry_id is the same thing to map flow with entry.
        """
        flow = typing.cast(OptionsFlow, flow)

        if result["type"] != FlowResultType.CREATE_ENTRY:
            return result

        entry = self._shc.config_entries.async_get_entry(flow.handler)
        if entry is None:
            raise UnknownEntry(flow.handler)
        if result["data"] is not None:
            self._shc.config_entries.async_update_entry(entry, options=result["data"])

        result["result"] = True
        return result

    async def async_post_init(self, flow: FlowHandler, result: FlowResult) -> None:
        return
