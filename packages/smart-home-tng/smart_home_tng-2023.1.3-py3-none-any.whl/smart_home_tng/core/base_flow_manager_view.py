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

import voluptuous_serialize

from .config_validation import ConfigValidation as cv
from .flow_manager import FlowManager
from .flow_result import FlowResult
from .flow_result_type import FlowResultType
from .smart_home_controller_view import SmartHomeControllerView


# pylint: disable=unused-variable
class _BaseFlowManagerView(SmartHomeControllerView):
    """Foundation for flow manager views."""

    def __init__(
        self,
        flow_mgr: FlowManager,
        url: str = None,
        name: str = None,
        extra_urls: list[str] = None,
        requires_auth=True,
        cors_allowed=False,
    ) -> None:
        """Initialize the flow manager index view."""
        super().__init__(url, name, extra_urls, requires_auth, cors_allowed)
        self._flow_mgr = flow_mgr

    def _prepare_result_json(self, result: FlowResult) -> FlowResult:
        """Convert result to JSON."""
        if result["type"] == FlowResultType.CREATE_ENTRY:
            data = result.copy()
            data.pop("result")
            data.pop("data")
            return data

        if "data_schema" not in result:
            return result

        data = result.copy()

        if (schema := data["data_schema"]) is None:
            data["data_schema"] = []
        else:
            data["data_schema"] = voluptuous_serialize.convert(
                schema, custom_serializer=cv.custom_serializer
            )

        return data
