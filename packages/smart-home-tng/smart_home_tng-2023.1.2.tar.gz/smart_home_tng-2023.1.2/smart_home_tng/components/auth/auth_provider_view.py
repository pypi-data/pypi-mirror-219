"""
Auth Component for Smart Home - The Next Generation.

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
class AuthProvidersView(core.SmartHomeControllerView):
    """View to get available auth providers."""

    def __init__(self):
        super().__init__("/auth/providers", "api:auth:providers", requires_auth=False)

    async def get(self, request):
        """Get available auth providers."""
        shc = request.app[core.Const.KEY_SHC]
        comp = core.SmartHomeControllerComponent.get_component("onboarding")
        if (
            not isinstance(comp, core.OnboardingComponent)
            or not comp.async_is_user_onboarded()
        ):
            return self.json_message(
                message="Onboarding not finished",
                status_code=http.HTTPStatus.BAD_REQUEST,
                message_code="onboarding_required",
            )

        return self.json(
            [
                {"name": provider.name, "id": provider.id, "type": provider.type}
                for provider in shc.auth.auth_providers
            ]
        )
