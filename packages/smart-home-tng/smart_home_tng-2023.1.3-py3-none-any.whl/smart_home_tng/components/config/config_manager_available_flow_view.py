"""
Configuration API for Smart Home - The Next Generation.

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

from ... import core


# pylint: disable=unused-variable
class ConfigManagerAvailableFlowView(core.SmartHomeControllerView):
    """View to query available flows."""

    def __init__(self):
        url = "/api/config/config_entries/flow_handlers"
        name = "api:config:config_entries:flow_handlers"
        super().__init__(url, name)

    async def get(self, request):
        """List available flow handlers."""
        shc: core.SmartHomeController = request.app[core.Const.KEY_SHC]
        kwargs = {}
        if "type" in request.query:
            kwargs["type_filter"] = request.query["type"]
        return self.json(await shc.setup.async_get_config_flows(**kwargs))
