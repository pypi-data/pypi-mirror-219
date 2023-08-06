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
import ipaddress
import typing

import voluptuous as vol

from ... import core
from ..credentials import Credentials
from ..invalid_auth_error import InvalidAuthError
from ..invalid_user_error import InvalidUserError
from ..refresh_token import RefreshToken
from ..user_meta import UserMeta
from .auth_provider import AuthProvider, _AUTH_PROVIDERS
from .login_flow import LoginFlow

IPAddress = typing.Union[ipaddress.IPv4Address, ipaddress.IPv6Address]
IPNetwork = typing.Union[ipaddress.IPv4Network, ipaddress.IPv6Network]

_CONF_TRUSTED_NETWORKS: typing.Final = "trusted_networks"
_CONF_TRUSTED_USERS: typing.Final = "trusted_users"
_CONF_GROUP: typing.Final = "group"
_CONF_ALLOW_BYPASS_LOGIN = "allow_bypass_login"

_DEFAULT_TITLE = "Trusted Networks"


@_AUTH_PROVIDERS.register("trusted_networks")
class TrustedNetworksAuthProvider(AuthProvider):
    """Trusted Networks auth provider.

    Allow passwordless access from trusted network.
    """

    @property
    def default_title(self) -> str:
        return _DEFAULT_TITLE

    @property
    def trusted_networks(self) -> list[IPNetwork]:
        """Return trusted networks."""
        return typing.cast(list[IPNetwork], self._config[_CONF_TRUSTED_NETWORKS])

    @property
    def trusted_users(self) -> dict[IPNetwork, typing.Any]:
        """Return trusted users per network."""
        return typing.cast(
            dict[IPNetwork, typing.Any], self._config[_CONF_TRUSTED_USERS]
        )

    @property
    def trusted_proxies(self) -> list[IPNetwork]:
        """Return trusted proxies in the system."""
        if not self._shc.http:
            return []

        return [
            ipaddress.ip_network(trusted_proxy)
            for trusted_proxy in self._shc.http.trusted_proxies
        ]

    @property
    def support_mfa(self) -> bool:
        """Trusted Networks auth provider does not support MFA."""
        return False

    async def async_login_flow(self, context: dict[str, typing.Any]) -> LoginFlow:
        """Return a flow to login."""
        assert context is not None
        ip_addr = typing.cast(IPAddress, context.get("ip_address"))
        users = await self._store.async_get_users()
        available_users = [
            user for user in users if not user.system_generated and user.is_active
        ]
        for ip_net, user_or_group_list in self.trusted_users.items():
            if ip_addr not in ip_net:
                continue

            user_list = [
                user_id for user_id in user_or_group_list if isinstance(user_id, str)
            ]
            group_list = [
                group[_CONF_GROUP]
                for group in user_or_group_list
                if isinstance(group, dict)
            ]
            flattened_group_list = [
                group for sublist in group_list for group in sublist
            ]
            available_users = [
                user
                for user in available_users
                if (
                    user.id in user_list
                    or any(group.id in flattened_group_list for group in user.groups)
                )
            ]
            break

        return TrustedNetworksLoginFlow(
            self,
            ip_addr,
            {user.id: user.name for user in available_users},
            self._config[_CONF_ALLOW_BYPASS_LOGIN],
        )

    async def async_get_or_create_credentials(
        self, flow_result: collections.abc.Mapping[str, str]
    ) -> Credentials:
        """Get credentials based on the flow result."""
        user_id = flow_result["user"]

        users = await self._store.async_get_users()
        for user in users:
            if user.id != user_id:
                continue

            if user.system_generated:
                continue

            if not user.is_active:
                continue

            for credential in await self.async_credentials():
                if credential.data["user_id"] == user_id:
                    return credential

            cred = self.async_create_credentials({"user_id": user_id})
            await self._store.async_link_user(user, cred)
            return cred

        # We only allow login as exist user
        raise InvalidUserError

    async def async_user_meta_for_credentials(
        self, _credentials: Credentials
    ) -> UserMeta:
        """Return extra user metadata for credentials.

        Trusted network auth provider should never create new user.
        """
        raise NotImplementedError()

    @core.callback
    def async_validate_access(self, ip_addr: IPAddress) -> None:
        """Make sure the access from trusted networks.

        Raise InvalidAuthError if not.
        Raise InvalidAuthError if trusted_networks is not configured.
        """
        if not self.trusted_networks:
            raise InvalidAuthError("trusted_networks is not configured")

        if not any(
            ip_addr in trusted_network for trusted_network in self.trusted_networks
        ):
            raise InvalidAuthError("Not in trusted_networks")

        if any(ip_addr in trusted_proxy for trusted_proxy in self.trusted_proxies):
            raise InvalidAuthError("Can't allow access from a proxy server")

    @core.callback
    def async_validate_refresh_token(
        self, _refresh_token: RefreshToken, remote_ip: str = None
    ) -> None:
        """Verify a refresh token is still valid."""
        if remote_ip is None:
            raise InvalidAuthError(
                "Unknown remote ip can't be used for trusted network provider."
            )
        self.async_validate_access(ipaddress.ip_address(remote_ip))


class TrustedNetworksLoginFlow(LoginFlow):
    """Handler for the login flow."""

    def __init__(
        self,
        auth_provider: TrustedNetworksAuthProvider,
        ip_addr: IPAddress,
        available_users: dict[str, str],
        allow_bypass_login: bool,
    ) -> None:
        """Initialize the login flow."""
        super().__init__(auth_provider)
        self._available_users = available_users
        self._ip_address = ip_addr
        self._allow_bypass_login = allow_bypass_login

    async def async_step_init(
        self, user_input: dict[str, str] = None
    ) -> core.FlowResult:
        """Handle the step of the form."""
        try:
            typing.cast(
                TrustedNetworksAuthProvider, self._auth_provider
            ).async_validate_access(self._ip_address)

        except InvalidAuthError:
            return self.async_abort(reason="not_allowed")

        if user_input is not None:
            return await self.async_finish(user_input)

        if self._allow_bypass_login and len(self._available_users) == 1:
            return await self.async_finish(
                {"user": next(iter(self._available_users.keys()))}
            )

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {vol.Required("user"): vol.In(self._available_users)}
            ),
        )


# pylint: disable=unused-variable
CONFIG_SCHEMA = AuthProvider.AUTH_PROVIDER_SCHEMA.extend(
    {
        vol.Required(_CONF_TRUSTED_NETWORKS): vol.All(
            core.ConfigValidation.ensure_list, [ipaddress.ip_network]
        ),
        vol.Optional(_CONF_TRUSTED_USERS, default={}): vol.Schema(
            # we only validate the format of user_id or group_id
            {
                ipaddress.ip_network: vol.All(
                    core.ConfigValidation.ensure_list,
                    [
                        vol.Or(
                            core.ConfigValidation.uuid4_hex,
                            vol.Schema(
                                {
                                    vol.Required(
                                        _CONF_GROUP
                                    ): core.ConfigValidation.uuid4_hex
                                }
                            ),
                        )
                    ],
                )
            }
        ),
        vol.Optional(
            _CONF_ALLOW_BYPASS_LOGIN, default=False
        ): core.ConfigValidation.boolean,
    },
    extra=vol.PREVENT_EXTRA,
)
