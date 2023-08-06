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

from ... import core


# pylint: disable=unused-variable
class ConfigManagerEntryResourceReloadView(core.SmartHomeControllerView):
    """View to reload a config entry."""

    def __init__(self):
        super().__init__(
            "/api/config/config_entries/entry/{entry_id}/reload",
            "api:config:config_entries:entry:resource:reload",
        )

    async def post(self, request, entry_id):
        """Reload a config entry."""
        if not request[core.Const.KEY_SHC_USER].is_admin:
            raise core.Unauthorized(config_entry_id=entry_id, permission="remove")

        shc = request.app[core.Const.KEY_SHC]
        entry = shc.config_entries.async_get_entry(entry_id)
        if not entry:
            return self.json_message(
                "Invalid entry specified", http.HTTPStatus.NOT_FOUND
            )
        assert isinstance(entry, core.ConfigEntry)

        try:
            await shc.config_entries.async_reload(entry_id)
        except core.OperationNotAllowed:
            return self.json_message(
                "Entry cannot be reloaded", http.HTTPStatus.FORBIDDEN
            )

        return self.json({"require_restart": not entry.state.recoverable})
