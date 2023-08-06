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
import json

import aiohttp.web_exceptions as http_exc
import voluptuous as vol

from ... import core


# pylint: disable=unused-variable
class APIDomainServicesView(core.SmartHomeControllerView):
    """View to handle DomainServices requests."""

    def __init__(self):
        url = "/api/services/{domain}/{service}"
        name = "api:domain-services"
        super().__init__(url, name)

    async def post(self, request, domain, service):
        """Call a service.

        Returns a list of changed states.
        """
        shc: core.SmartHomeController = request.app[core.Const.KEY_SHC]
        body = await request.text()
        try:
            data = json.loads(body) if body else None
        except ValueError:
            return self.json_message(
                "Data should be valid JSON.", http.HTTPStatus.BAD_REQUEST
            )

        context = self.context(request)

        try:
            await shc.services.async_call(
                domain, service, data, blocking=True, context=context
            )
        except (vol.Invalid, core.ServiceNotFound) as ex:
            raise http_exc.HTTPBadRequest() from ex

        changed_states = []

        for state in shc.states.async_all():
            if state.context is context:
                changed_states.append(state)

        return self.json(changed_states)
