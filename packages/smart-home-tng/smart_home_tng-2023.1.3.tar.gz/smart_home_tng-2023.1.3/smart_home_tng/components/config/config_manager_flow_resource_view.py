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

from ... import auth, core
from .config_manager_flow_index_view import _prepare_config_flow_result_json


# pylint: disable=unused-variable
class ConfigManagerFlowResourceView(core.FlowManagerResourceView):
    """View to interact with the flow manager."""

    def __init__(self, flow_mgr: core.FlowManager) -> None:
        url = "/api/config/config_entries/flow/{flow_id}"
        name = "api:config:config_entries:flow:resource"
        super().__init__(flow_mgr, url, name)

    async def get(self, request, flow_id):
        """Get the current state of a data_entry_flow."""
        if not request[core.Const.KEY_SHC_USER].is_admin:
            raise core.Unauthorized(
                perm_category=auth.permissions.Const.CAT_CONFIG_ENTRIES,
                permission="add",
            )

        return await super().get(request, flow_id)

    async def post(self, request, flow_id):
        """Handle a POST request."""
        if not request[core.Const.KEY_SHC_USER].is_admin:
            raise core.Unauthorized(
                perm_category=auth.permissions.Const.CAT_CONFIG_ENTRIES,
                permission="add",
            )

        return await super().post(request, flow_id)

    def _prepare_result_json(self, result):
        """Convert result to JSON."""
        return _prepare_config_flow_result_json(result, super()._prepare_result_json)
