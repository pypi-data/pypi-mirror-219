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

import http

from aiohttp import web
from aiohttp import web_exceptions as web_exc

from ... import auth, core
from .config_manager_entry_index_view import _entry_json


# pylint: disable=unused-variable
class ConfigManagerFlowIndexView(core.FlowManagerIndexView):
    """View to create config flows."""

    def __init__(self, flow_mgr: core.FlowManager) -> None:
        url = "/api/config/config_entries/flow"
        name = "api:config:config_entries:flow"
        super().__init__(flow_mgr, url, name)

    async def get(self, request):
        """Not implemented."""
        raise web_exc.HTTPMethodNotAllowed("GET", ["POST"])

    async def post(self, request):
        """Handle a POST request."""
        if not request[core.Const.KEY_SHC_USER].is_admin:
            raise core.Unauthorized(
                perm_category=auth.permissions.Const.CAT_CONFIG_ENTRIES,
                permission="add",
            )

        try:
            return await super().post(request)
        except core.DependencyError as exc:
            return web.Response(
                text=f"Failed dependencies {', '.join(exc.failed_dependencies)}",
                status=http.HTTPStatus.BAD_REQUEST,
            )

    def _prepare_result_json(self, result):
        """Convert result to JSON."""
        return _prepare_config_flow_result_json(result, super()._prepare_result_json)


def _prepare_config_flow_result_json(result, prepare_result_json):
    """Convert result to JSON."""
    if result["type"] != core.FlowResultType.CREATE_ENTRY:
        return prepare_result_json(result)

    data = result.copy()
    data["result"] = _entry_json(result["result"])
    data.pop("data")
    return data
