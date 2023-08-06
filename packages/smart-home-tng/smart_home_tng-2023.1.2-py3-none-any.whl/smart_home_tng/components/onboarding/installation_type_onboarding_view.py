"""
Onboarding Component for Smart Home - The Next Generation.

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

from aiohttp import web_exceptions as web_ex

from ... import core


# pylint: disable=unused-variable
class InstallationTypeOnboardingView(core.SmartHomeControllerView):
    """Return the installation type during onboarding."""

    def __init__(self, data):
        """Initialize the onboarding installation type view."""
        requires_auth = False
        url = "/api/onboarding/installation_type"
        name = "api:onboarding:installation_type"
        super().__init__(
            url,
            name,
            requires_auth=requires_auth,
        )
        self._data = data

    async def get(self, request):
        """Return the onboarding status."""
        if self._data["done"]:
            raise web_ex.HTTPUnauthorized()

        shc = request.app[core.Const.KEY_SHC]
        info = await core.helpers.async_get_system_info(shc)
        return self.json({"installation_type": info["installation_type"]})
