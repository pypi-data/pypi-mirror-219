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

import asyncio
import base64
import collections.abc
import logging
import typing

import bcrypt
import voluptuous as vol

from ...core.callback import callback
from ...core.const import Const
from ...core.flow_result import FlowResult
from ...core.smart_home_controller_error import SmartHomeControllerError
from ...core.store import Store
from ..credentials import Credentials
from ..invalid_auth_error import InvalidAuthError
from ..user_meta import UserMeta
from .auth_provider import AuthProvider, _AUTH_PROVIDERS
from .login_flow import LoginFlow

_STORAGE_VERSION: typing.Final = 1
_STORAGE_KEY: typing.Final = "auth_provider.internal"
_LOGGER: typing.Final = logging.getLogger(__name__)


if not typing.TYPE_CHECKING:

    class SmartHomeController:
        ...


if typing.TYPE_CHECKING:
    from ...core.smart_home_controller import SmartHomeController


def _disallow_id(conf: dict[str, typing.Any]) -> dict[str, typing.Any]:
    """Disallow ID in config."""
    if Const.CONF_ID in conf:
        raise vol.Invalid(
            "ID is not allowed for the Smart Home - "
            + "The Next Generation auth provider."
        )

    return conf


class InvalidUser(SmartHomeControllerError):
    """Raised when invalid user is specified.

    Will not be raised when validating authentication.
    """


class Data:
    """Hold the user data."""

    def __init__(self, shc: SmartHomeController) -> None:
        """Initialize the user data store."""
        self._shc = shc
        self._store = Store[dict[str, list[dict[str, str]]]](
            shc, _STORAGE_VERSION, _STORAGE_KEY, private=True, atomic_writes=True
        )
        self._data: dict[str, typing.Any] = None
        # Legacy mode will allow usernames to start/end with whitespace
        # and will compare usernames case-insensitive.
        # Remove in 2020 or when we launch 1.0.
        self.is_legacy = False

    @callback
    def normalize_username(self, username: str) -> str:
        """Normalize a username based on the mode."""
        if self.is_legacy:
            return username

        return username.strip().casefold()

    async def async_load(self) -> None:
        """Load stored data."""
        if (data := await self._store.async_load()) is None or not isinstance(
            data, dict
        ):
            data = {"users": []}

        seen: set[str] = set()

        for user in data["users"]:
            username = user["username"]

            # check if we have duplicates
            if (folded := username.casefold()) in seen:
                self.is_legacy = True

                _LOGGER.warning(
                    "Home Assistant auth provider is running in legacy mode "
                    + "because we detected usernames that are case-insensitive"
                    + f"equivalent. Please change the username: '{username}'."
                )

                break

            seen.add(folded)

            # check if we have unstripped usernames
            if username != username.strip():
                self.is_legacy = True

                _LOGGER.warning(
                    "Home Assistant auth provider is running in legacy mode "
                    + "because we detected usernames that start or end in a "
                    + f"space. Please change the username: '{username}'."
                )

                break

        self._data = data

    @property
    def users(self) -> list[dict[str, str]]:
        """Return users."""
        return self._data["users"]

    def validate_login(self, username: str, password: str) -> None:
        """Validate a username and password.

        Raises InvalidAuth if auth invalid.
        """
        username = self.normalize_username(username)
        dummy = b"$2b$12$CiuFGszHx9eNHxPuQcwBWez4CwDTOcLTX5CbOpV6gef2nYuXkY7BO"
        found = None

        # Compare all users to avoid timing attacks.
        for user in self.users:
            if self.normalize_username(user["username"]) == username:
                found = user

        if found is None:
            # check a hash to make timing the same as if user was found
            bcrypt.checkpw(b"foo", dummy)
            raise InvalidAuthError

        user_hash = base64.b64decode(found["password"])

        # bcrypt.checkpw is timing-safe
        if not bcrypt.checkpw(password.encode(), user_hash):
            raise InvalidAuthError

    def hash_password(self, password: str, for_storage: bool = False) -> bytes:
        """Encode a password."""
        hashed: bytes = bcrypt.hashpw(password.encode(), bcrypt.gensalt(rounds=12))

        if for_storage:
            hashed = base64.b64encode(hashed)
        return hashed

    def add_auth(self, username: str, password: str) -> None:
        """Add a new authenticated user/pass."""
        username = self.normalize_username(username)

        if any(
            self.normalize_username(user["username"]) == username for user in self.users
        ):
            raise InvalidUser

        self.users.append(
            {
                "username": username,
                "password": self.hash_password(password, True).decode(),
            }
        )

    @callback
    def async_remove_auth(self, username: str) -> None:
        """Remove authentication."""
        username = self.normalize_username(username)

        index = None
        for i, user in enumerate(self.users):
            if self.normalize_username(user["username"]) == username:
                index = i
                break

        if index is None:
            raise InvalidUser

        self.users.pop(index)

    def change_password(self, username: str, new_password: str) -> None:
        """Update the password.

        Raises InvalidUser if user cannot be found.
        """
        username = self.normalize_username(username)

        for user in self.users:
            if self.normalize_username(user["username"]) == username:
                user["password"] = self.hash_password(new_password, True).decode()
                break
        else:
            raise InvalidUser

    async def async_save(self) -> None:
        """Save data."""
        if self._data is not None:
            await self._store.async_save(self._data)


_DEFAULT_TITLE: typing.Final = "Smart Home - The Next Generation"


@_AUTH_PROVIDERS.register("internal")
class InternalAuthProvider(AuthProvider):
    """
    Auth provider based on a local storage of users in
    Smart Home - The Next Generation config dir."""

    def __init__(self, *args: typing.Any, **kwargs: typing.Any) -> None:
        """Initialize an internal auth provider."""
        super().__init__(*args, **kwargs)
        self._data: Data = None
        self._init_lock = asyncio.Lock()

    @property
    def default_title(self) -> str:
        return _DEFAULT_TITLE

    @property
    def data(self) -> Data:
        return self._data

    async def async_initialize(self) -> None:
        """Initialize the auth provider."""
        async with self._init_lock:
            if self._data is not None:
                return

            data = Data(self._shc)
            await data.async_load()
            self._data = data

    async def async_login_flow(self, context: dict[str, typing.Any]) -> LoginFlow:
        """Return a flow to login."""
        return InternalLoginFlow(self, context)

    async def async_validate_login(self, username: str, password: str) -> None:
        """Validate a username and password."""
        if self._data is None:
            await self.async_initialize()
            assert self._data is not None

        await self._shc.async_add_executor_job(
            self._data.validate_login, username, password
        )

    async def async_add_auth(self, username: str, password: str) -> None:
        """Call add_auth on data."""
        if self._data is None:
            await self.async_initialize()
            assert self._data is not None

        await self._shc.async_add_executor_job(self._data.add_auth, username, password)
        await self._data.async_save()

    async def async_remove_auth(self, username: str) -> None:
        """Call remove_auth on data."""
        if self._data is None:
            await self.async_initialize()
            assert self._data is not None

        self._data.async_remove_auth(username)
        await self._data.async_save()

    async def async_change_password(self, username: str, new_password: str) -> None:
        """Call change_password on data."""
        if self._data is None:
            await self.async_initialize()
            assert self._data is not None

        await self._shc.async_add_executor_job(
            self._data.change_password, username, new_password
        )
        await self._data.async_save()

    async def async_get_or_create_credentials(
        self, flow_result: collections.abc.Mapping[str, str]
    ) -> Credentials:
        """Get credentials based on the flow result."""
        if self._data is None:
            await self.async_initialize()
            assert self._data is not None

        norm_username = self._data.normalize_username
        username = norm_username(flow_result["username"])

        for credential in await self.async_credentials():
            if norm_username(credential.data["username"]) == username:
                return credential

        # Create new credentials.
        return self.async_create_credentials({"username": username})

    async def async_user_meta_for_credentials(
        self, credentials: Credentials
    ) -> UserMeta:
        """Get extra info for this credential."""
        return UserMeta(name=credentials.data["username"], is_active=True)

    async def async_will_remove_credentials(self, credentials: Credentials) -> None:
        """When credentials get removed, also remove the auth."""
        if self._data is None:
            await self.async_initialize()
            assert self._data is not None

        try:
            self._data.async_remove_auth(credentials.data["username"])
            await self._data.async_save()
        except InvalidUser:
            # Can happen if somehow we didn't clean up a credential
            pass


class InternalLoginFlow(LoginFlow):
    """Handler for the login flow."""

    async def async_step_init(self, user_input: dict[str, str] = None) -> FlowResult:
        """Handle the step of the form."""
        errors = {}

        if user_input is not None:
            try:
                await typing.cast(
                    InternalAuthProvider, self._auth_provider
                ).async_validate_login(user_input["username"], user_input["password"])
            except InvalidAuthError:
                errors["base"] = "invalid_auth"

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
CONFIG_SCHEMA: typing.Final = vol.All(AuthProvider.AUTH_PROVIDER_SCHEMA, _disallow_id)
