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

from ... import core


# pylint: disable=unused-variable
class APIEventView(core.SmartHomeControllerView):
    """View to handle Event requests."""

    def __init__(self):
        url = "/api/events/{event_type}"
        name = "api:event"
        super().__init__(url, name)

    async def post(self, request, event_type):
        """Fire events."""
        if not request[core.Const.KEY_SHC_USER].is_admin:
            raise core.Unauthorized()
        body = await request.text()
        try:
            event_data = json.loads(body) if body else None
        except ValueError:
            return self.json_message(
                "Event data should be valid JSON.", http.HTTPStatus.BAD_REQUEST
            )

        if event_data is not None and not isinstance(event_data, dict):
            return self.json_message(
                "Event data should be a JSON object", http.HTTPStatus.BAD_REQUEST
            )

        # Special case handling for event STATE_CHANGED
        # We will try to convert state dicts back to State objects
        if event_type == core.Const.EVENT_STATE_CHANGED and event_data:
            for key in ("old_state", "new_state"):
                state = core.State.from_dict(event_data.get(key))

                if state:
                    event_data[key] = state

        request.app[core.Const.KEY_SHC].bus.async_fire(
            event_type, event_data, core.EventOrigin.REMOTE, self.context(request)
        )

        return self.json_message(f"Event {event_type} fired.")
