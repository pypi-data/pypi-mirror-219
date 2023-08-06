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

from ... import auth, core


# pylint: disable=unused-variable
class APIEntityStateView(core.SmartHomeControllerView):
    """View to handle EntityState requests."""

    def __init__(self):
        url = "/api/states/{entity_id}"
        super().__init__(url, "api:entity-state")

    @core.callback
    def get(self, request, entity_id):
        """Retrieve state of entity."""
        user = request[core.Const.KEY_SHC_USER]
        if not user.permissions.check_entity(
            entity_id, auth.permissions.Const.POLICY_READ
        ):
            raise core.Unauthorized(entity_id=entity_id)

        if state := request.app[core.Const.KEY_SHC].states.get(entity_id):
            return self.json(state)
        return self.json_message("Entity not found.", http.HTTPStatus.NOT_FOUND)

    async def post(self, request, entity_id):
        """Update state of entity."""
        if not request[core.Const.KEY_SHC_USER].is_admin:
            raise core.Unauthorized(entity_id=entity_id)
        shc = request.app[core.Const.KEY_SHC]
        try:
            data = await request.json()
        except ValueError:
            return self.json_message(
                "Invalid JSON specified.", http.HTTPStatus.BAD_REQUEST
            )

        if (new_state := data.get("state")) is None:
            return self.json_message("No state specified.", http.HTTPStatus.BAD_REQUEST)

        attributes = data.get("attributes")
        force_update = data.get("force_update", False)

        is_new_state = shc.states.get(entity_id) is None

        # Write state
        shc.states.async_set(
            entity_id, new_state, attributes, force_update, self.context(request)
        )

        # Read the state back for our response
        status_code = http.HTTPStatus.CREATED if is_new_state else http.HTTPStatus.OK
        resp = self.json(shc.states.get(entity_id), status_code)

        loc = core.Const.URL_API_STATES_ENTITY.format(entity_id)
        resp.headers.add("Location", loc)

        return resp

    @core.callback
    def delete(self, request, entity_id):
        """Remove entity."""
        if not request[core.Const.KEY_SHC_USER].is_admin:
            raise core.Unauthorized(entity_id=entity_id)
        if request.app[core.Const.KEY_SHC].states.async_remove(entity_id):
            return self.json_message("Entity removed.")
        return self.json_message("Entity not found.", http.HTTPStatus.NOT_FOUND)
