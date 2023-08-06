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
import logging
import typing

import voluptuous as vol
import voluptuous.humanize as vh

from ...core.callback import callback
from ...core.const import Const
from ...core.registry import Registry
from ..auth_store import AuthStore
from ..credentials import Credentials
from ..refresh_token import RefreshToken
from ..user_meta import UserMeta


_LOGGER: typing.Final = logging.getLogger(__name__)

_DEFAULT_TITLE: typing.Final = "Unnamed auth provider"


if not typing.TYPE_CHECKING:

    class LoginFlow:
        ...

    class SmartHomeController:
        ...


if typing.TYPE_CHECKING:
    from ...core.smart_home_controller import SmartHomeController
    from .login_flow import LoginFlow


_AUTH_PROVIDER_SCHEMA: typing.Final = vol.Schema(
    {
        vol.Required(Const.CONF_TYPE): str,
        vol.Optional(Const.CONF_NAME): str,
        # Specify ID if you have two auth providers for same type.
        vol.Optional(Const.CONF_ID): str,
    },
    extra=vol.ALLOW_EXTRA,
)


# pylint: disable=unused-variable
class AuthProvider:
    """Provider of user authentication."""

    def __init__(
        self,
        shc: SmartHomeController,
        store: AuthStore,
        config: dict[str, typing.Any],
    ) -> None:
        """Initialize an auth provider."""
        self._shc = shc
        self._store = store
        self._config = config

    AUTH_PROVIDER_SCHEMA: typing.Final = _AUTH_PROVIDER_SCHEMA

    @property
    def default_title(self) -> str:
        return _DEFAULT_TITLE

    @property
    def controller(self) -> SmartHomeController:
        return self._shc

    @property
    def id(self) -> str:
        """Return id of the auth provider.

        Optional, can be None.
        """
        return self._config.get(Const.CONF_ID)

    @property
    def type(self) -> str:
        """Return type of the provider."""
        return self._config[Const.CONF_TYPE]

    @property
    def name(self) -> str:
        """Return the name of the auth provider."""
        return self._config.get(Const.CONF_NAME, self.default_title)

    @property
    def support_mfa(self) -> bool:
        """Return whether multi-factor auth supported by the auth provider."""
        return True

    async def async_credentials(self) -> list[Credentials]:
        """Return all credentials of this provider."""
        users = await self._store.async_get_users()
        return [
            credentials
            for user in users
            for credentials in user.credentials
            if (
                credentials.auth_provider_type == self.type
                and credentials.auth_provider_id == self.id
            )
        ]

    @callback
    def async_create_credentials(self, data: dict[str, str]) -> Credentials:
        """Create credentials."""
        return Credentials(
            auth_provider_type=self.type, auth_provider_id=self.id, data=data
        )

    # Implement by extending class

    async def async_login_flow(self, _context: dict[str, typing.Any]) -> LoginFlow:
        """Return the data flow for logging in with auth provider.

        Auth provider should extend LoginFlow and return an instance.
        """
        raise NotImplementedError()

    async def async_get_or_create_credentials(
        self, _flow_result: collections.abc.Mapping[str, str]
    ) -> Credentials:
        """Get credentials based on the flow result."""
        raise NotImplementedError()

    async def async_user_meta_for_credentials(
        self, _credentials: Credentials
    ) -> UserMeta:
        """Return extra user metadata for credentials.

        Will be used to populate info when creating a new user.
        """
        raise NotImplementedError()

    async def async_initialize(self) -> None:
        """Initialize the auth provider."""

    @callback
    def async_validate_refresh_token(
        self, _refresh_token: RefreshToken, _remote_ip: str = None
    ) -> None:
        """Verify a refresh token is still valid.

        Optional hook for an auth provider to verify validity of a refresh token.
        Should raise InvalidAuthError on errors.
        """

    @staticmethod
    async def from_config(
        shc: SmartHomeController, store: AuthStore, config: dict[str, typing.Any]
    ):
        """Initialize an auth provider from a config."""
        provider_name: str = config[Const.CONF_TYPE]
        module = await shc.setup.load_auth_provider_module(provider_name)

        try:
            config = module.CONFIG_SCHEMA(config)
        except vol.Invalid as err:
            _LOGGER.error(
                f"Invalid configuration for auth provider {provider_name}: "
                + f"{vh.humanize_error(config, err)}"
            )
            raise

        return _AUTH_PROVIDERS[provider_name](shc, store, config)


_AUTH_PROVIDERS: typing.Final[Registry[str, type[AuthProvider]]] = Registry()
