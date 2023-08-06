"""
Authentication Provider Layer for Smart Home - The Next Generation.

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

import collections.abc
import hmac
import typing
import voluptuous as vol

from ... import core
from ..credentials import Credentials
from ..invalid_auth_error import InvalidAuthError
from ..user_meta import UserMeta
from .auth_provider import AuthProvider, _AUTH_PROVIDERS
from .login_flow import LoginFlow


# pylint: disable=unused-variable
@_AUTH_PROVIDERS.register("insecure_example")
class ExampleAuthProvider(AuthProvider):
    """Example auth provider based on hardcoded usernames and passwords."""

    async def async_login_flow(self, _context: dict[str, typing.Any]) -> LoginFlow:
        """Return a flow to login."""
        return ExampleLoginFlow(self)

    @core.callback
    def async_validate_login(self, username: str, password: str) -> None:
        """Validate a username and password."""
        user = None

        # Compare all users to avoid timing attacks.
        for usr in self._config["users"]:
            if hmac.compare_digest(
                username.encode("utf-8"), usr["username"].encode("utf-8")
            ):
                user = usr

        if user is None:
            # Do one more compare to make timing the same as if user was found.
            hmac.compare_digest(password.encode("utf-8"), password.encode("utf-8"))
            raise InvalidAuthError

        if not hmac.compare_digest(
            user["password"].encode("utf-8"), password.encode("utf-8")
        ):
            raise InvalidAuthError

    async def async_get_or_create_credentials(
        self, flow_result: collections.abc.Mapping[str, str]
    ) -> Credentials:
        """Get credentials based on the flow result."""
        username = flow_result["username"]

        for credential in await self.async_credentials():
            if credential.data["username"] == username:
                return credential

        # Create new credentials.
        return self.async_create_credentials({"username": username})

    async def async_user_meta_for_credentials(
        self, credentials: Credentials
    ) -> UserMeta:
        """Return extra user metadata for credentials.

        Will be used to populate info when creating a new user.
        """
        username = credentials.data["username"]
        name = None

        for user in self._config["users"]:
            if user["username"] == username:
                name = user.get("name")
                break

        return UserMeta(name=name, is_active=True)


class ExampleLoginFlow(LoginFlow):
    """Handler for the login flow."""

    async def async_step_init(
        self, user_input: dict[str, str] = None
    ) -> core.FlowResult:
        """Handle the step of the form."""
        errors = None

        if user_input is not None:
            try:
                typing.cast(
                    ExampleAuthProvider, self._auth_provider
                ).async_validate_login(user_input["username"], user_input["password"])
            except InvalidAuthError:
                errors = {"base": "invalid_auth"}

            if not errors:
                user_input.pop("password")
                return await self.async_finish(user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Required("username"): str,
                    vol.Required("password"): str,
                }
            ),
            errors=errors,
        )


# pylint: disable=unused-variable
USER_SCHEMA = vol.Schema(
    {
        vol.Required("username"): str,
        vol.Required("password"): str,
        vol.Optional("name"): str,
    }
)

# pylint: disable=unused-variable
CONFIG_SCHEMA = AuthProvider.AUTH_PROVIDER_SCHEMA.extend(
    {vol.Required("users"): [USER_SCHEMA]}, extra=vol.PREVENT_EXTRA
)
