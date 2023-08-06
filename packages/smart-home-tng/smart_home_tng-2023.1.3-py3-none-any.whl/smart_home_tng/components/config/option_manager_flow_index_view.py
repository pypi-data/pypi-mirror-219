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


# pylint: disable=unused-variable
class OptionManagerFlowIndexView(core.FlowManagerIndexView):
    """View to create option flows."""

    def __init__(self, flow_mgr: core.FlowManager) -> None:
        url = "/api/config/config_entries/options/flow"
        name = "api:config:config_entries:option:flow"
        super().__init__(flow_mgr, url, name)

    async def post(self, request):
        """Handle a POST request.

        handler in request is entry_id.
        """
        if not request[core.Const.KEY_SHC_USER].is_admin:
            raise core.Unauthorized(
                perm_category=auth.permissions.Const.CAT_CONFIG_ENTRIES,
                permission=auth.permissions.Const.POLICY_EDIT,
            )

        return await super().post(request)
