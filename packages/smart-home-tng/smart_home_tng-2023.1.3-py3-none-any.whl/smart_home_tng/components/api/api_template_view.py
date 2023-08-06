"""
Rest API for Smart Home - The Next Generation.

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

from ... import core


# pylint: disable=unused-variable
class APITemplateView(core.SmartHomeControllerView):
    """View to handle Template requests."""

    def __init__(self):
        super().__init__(core.Const.URL_API_TEMPLATE, "api:template")

    async def post(self, request):
        """Render a template."""
        if not request[core.Const.KEY_SHC_USER].is_admin:
            raise core.Unauthorized()
        try:
            data = await request.json()
            tpl = core.Template(data["template"], request.app[core.Const.KEY_SHC])
            return tpl.async_render(variables=data.get("variables"), parse_result=False)
        except (ValueError, core.TemplateError) as ex:
            return self.json_message(
                f"Error rendering template: {ex}", http.HTTPStatus.BAD_REQUEST
            )
