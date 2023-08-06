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

import http
import typing

from ... import core
from .base_onboarding_view import _BaseOnboardingView
from .step import Step

if not typing.TYPE_CHECKING:

    class Onboarding:
        ...


if typing.TYPE_CHECKING:
    from .onboarding import Onboarding


# pylint: disable=unused-variable
class AnalyticsOnboardingView(_BaseOnboardingView):
    """View to finish analytics onboarding step."""

    def __init__(self, owner: Onboarding, data, store):
        url = "/api/onboarding/analytics"
        name = "api:onboarding:analytics"
        super().__init__(
            owner,
            url,
            name,
            step=Step.ANALYTICS,
            data=data,
            store=store,
        )

    async def post(self, request):
        """Handle finishing analytics step."""
        shc: core.SmartHomeController = request.app[core.Const.KEY_SHC]

        async with self._lock:
            if self._async_is_done():
                return self.json_message(
                    "Analytics config step already done", http.HTTPStatus.FORBIDDEN
                )

            await self._async_mark_done(shc)

            return self.json({})
