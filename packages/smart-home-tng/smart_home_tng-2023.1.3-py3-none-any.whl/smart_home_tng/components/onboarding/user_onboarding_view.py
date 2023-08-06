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

import voluptuous as vol

from ... import auth, core
from .base_onboarding_view import _BaseOnboardingView
from .const import Const
from .step import Step


if not typing.TYPE_CHECKING:

    class Onboarding:
        ...


if typing.TYPE_CHECKING:
    from .onboarding import Onboarding

_VALIDATOR: typing.Final = core.RequestDataValidator(
    vol.Schema(
        {
            vol.Required("name"): str,
            vol.Required("username"): str,
            vol.Required("password"): str,
            vol.Required("client_id"): str,
            vol.Required("language"): str,
        }
    )
)


# pylint: disable=unused-variable
class UserOnboardingView(_BaseOnboardingView):
    """View to handle create user onboarding step."""

    def __init__(self, owner: Onboarding, data, store):
        super().__init__(
            owner,
            "/api/onboarding/users",
            "api:onboarding:users",
            Step.USER,
            False,
            data,
            store,
        )

    async def post(self, request):
        """Handle user creation, area creation."""
        shc: core.SmartHomeController = request.app[core.Const.KEY_SHC]
        data, error = await _VALIDATOR.async_get_request_data(request)
        if error is not None:
            return error

        async with self._lock:
            if self._async_is_done():
                return self.json_message(
                    "User step already done", http.HTTPStatus.FORBIDDEN
                )

            provider = shc.async_get_shc_auth_provider()
            await provider.async_initialize()

            user = await shc.auth.async_create_user(
                data["name"], group_ids=[auth.Const.GROUP_ID_ADMIN]
            )
            await shc.async_add_executor_job(
                provider.data.add_auth, data["username"], data["password"]
            )
            credentials = await provider.async_get_or_create_credentials(
                {"username": data["username"]}
            )
            await provider.data.async_save()
            await shc.auth.async_link_user(user, credentials)

            comp = core.SmartHomeControllerComponent.get_component("person")
            if "person" in shc.config.components and comp is not None:
                await comp.async_create_person(data["name"], user_id=user.id)

            area_registry = shc.area_registry
            # Create default areas using the users supplied language.
            translations = await shc.translations.async_get_translations(
                data["language"], "area", [self._owner.domain]
            )

            # Create default areas using the users supplied language.
            for area in Const.DEFAULT_AREAS:
                area_registry.async_create(
                    translations[f"component.onboarding.area.{area}"]
                )

            await self._async_mark_done(shc)

            # Return authorization code for fetching tokens and connect
            # during onboarding.
            auth_code = ""
            comp = core.SmartHomeControllerComponent.get_component("auth")
            if isinstance(comp, core.AuthComponent):
                auth_code = comp.create_auth_code(data["client_id"], credentials)
            return self.json({"auth_code": auth_code})
