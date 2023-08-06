"""
Authentication Layer for Smart Home - The Next Generation.

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
import collections
import datetime
import typing

import jwt

from ..core import helpers
from ..core.callback import callback
from ..core.callback_type import CallbackType
from .auth_manager_flow_manager import AuthManagerFlowManager
from .auth_store import AuthStore
from .const import Const
from .credentials import Credentials
from .group import Group
from .invalid_provider import InvalidProvider
from .mfa_modules import MultiFactorAuthModule
from .providers import AuthProvider
from .refresh_token import RefreshToken
from .token_type import TokenType
from .user import User

_MfaModuleDict = dict[str, MultiFactorAuthModule]
_ProviderKey = tuple[str, typing.Optional[str]]
_ProviderDict = dict[_ProviderKey, AuthProvider]

if not typing.TYPE_CHECKING:

    class SmartHomeController:
        pass


if typing.TYPE_CHECKING:
    from ..core.smart_home_controller import SmartHomeController


# pylint: disable=unused-variable
class AuthManager:
    """Manage the authentication for Smart Home - The Next Generation."""

    EVENT_USER_ADDED: typing.Final = "user.added"
    EVENT_USER_REMOVED: typing.Final = "user.removed"

    def __init__(
        self,
        shc: SmartHomeController,
        store: AuthStore,
        providers: _ProviderDict,
        mfa_modules: _MfaModuleDict,
    ) -> None:
        """Initialize the auth manager."""
        self._shc = shc
        self._store = store
        self._providers = providers
        self._mfa_modules = mfa_modules
        self._login_flow = AuthManagerFlowManager(shc, self)
        self._revoke_callbacks: dict[str, list[CallbackType]] = {}

    @property
    def login_flow(self) -> AuthManagerFlowManager:
        return self._login_flow

    @property
    def auth_providers(self) -> list[AuthProvider]:
        """Return a list of available auth providers."""
        return list(self._providers.values())

    @property
    def auth_mfa_modules(self) -> list[MultiFactorAuthModule]:
        """Return a list of available auth modules."""
        return list(self._mfa_modules.values())

    def get_auth_provider(self, provider_type: str, provider_id: str) -> AuthProvider:
        """Return an auth provider, None if not found."""
        return self._providers.get((provider_type, provider_id))

    def get_auth_providers(self, provider_type: str) -> list[AuthProvider]:
        """Return a List of auth provider of one type, Empty if not found."""
        return [
            provider
            for (p_type, _), provider in self._providers.items()
            if p_type == provider_type
        ]

    def get_auth_mfa_module(self, module_id: str) -> MultiFactorAuthModule:
        """Return a multi-factor auth module, None if not found."""
        return self._mfa_modules.get(module_id)

    async def async_get_users(self) -> list[User]:
        """Retrieve all users."""
        return await self._store.async_get_users()

    async def async_get_user(self, user_id: str) -> User:
        """Retrieve a user."""
        return await self._store.async_get_user(user_id)

    async def async_get_owner(self) -> User:
        """Retrieve the owner."""
        users = await self.async_get_users()
        return next((user for user in users if user.is_owner), None)

    async def async_get_group(self, group_id: str) -> Group:
        """Retrieve all groups."""
        return await self._store.async_get_group(group_id)

    async def async_get_user_by_credentials(self, credentials: Credentials) -> User:
        """Get a user by credential, return None if not found."""
        for user in await self.async_get_users():
            for creds in user.credentials:
                if creds.id == credentials.id:
                    return user

        return None

    async def async_create_system_user(
        self,
        name: str,
        *,
        group_ids: list[str] = None,
        local_only: bool = None,
    ) -> User:
        """Create a system user."""
        user = await self._store.async_create_user(
            name=name,
            system_generated=True,
            is_active=True,
            group_ids=group_ids or [],
            local_only=local_only,
        )

        self._shc.bus.async_fire(self.EVENT_USER_ADDED, {"user_id": user.id})

        return user

    async def async_create_user(
        self,
        name: str,
        *,
        group_ids: list[str] = None,
        local_only: bool = None,
    ) -> User:
        """Create a user."""
        kwargs: dict[str, typing.Any] = {
            "name": name,
            "is_active": True,
            "group_ids": group_ids or [],
            "local_only": local_only,
        }

        if await self._user_should_be_owner():
            kwargs["is_owner"] = True

        user = await self._store.async_create_user(**kwargs)

        self._shc.bus.async_fire(self.EVENT_USER_ADDED, {"user_id": user.id})

        return user

    async def async_get_or_create_user(self, credentials: Credentials) -> User:
        """Get or create a user."""
        if not credentials.is_new:
            user = await self.async_get_user_by_credentials(credentials)
            if user is None:
                raise ValueError("Unable to find the user.")
            return user

        auth_provider = self._async_get_auth_provider(credentials)

        if auth_provider is None:
            raise RuntimeError("Credential with unknown provider encountered")

        info = await auth_provider.async_user_meta_for_credentials(credentials)

        user = await self._store.async_create_user(
            credentials=credentials,
            name=info.name,
            is_active=info.is_active,
            group_ids=[Const.GROUP_ID_ADMIN],
        )

        self._shc.bus.async_fire(self.EVENT_USER_ADDED, {"user_id": user.id})

        return user

    async def async_link_user(self, user: User, credentials: Credentials) -> None:
        """Link credentials to an existing user."""
        linked_user = await self.async_get_user_by_credentials(credentials)
        if linked_user == user:
            return
        if linked_user is not None:
            raise ValueError("Credential is already linked to a user")

        await self._store.async_link_user(user, credentials)

    async def async_remove_user(self, user: User) -> None:
        """Remove a user."""
        tasks = [
            self.async_remove_credentials(credentials)
            for credentials in user.credentials
        ]

        if tasks:
            await asyncio.gather(*tasks)

        await self._store.async_remove_user(user)

        self._shc.bus.async_fire(self.EVENT_USER_REMOVED, {"user_id": user.id})

    async def async_update_user(
        self,
        user: User,
        name: str = None,
        is_active: bool = None,
        group_ids: list[str] = None,
        local_only: bool = None,
    ) -> None:
        """Update a user."""
        kwargs: dict[str, typing.Any] = {}

        for attr_name, value in (
            ("name", name),
            ("group_ids", group_ids),
            ("local_only", local_only),
        ):
            if value is not None:
                kwargs[attr_name] = value
        await self._store.async_update_user(user, **kwargs)

        if is_active is not None:
            if is_active is True:
                await self.async_activate_user(user)
            else:
                await self.async_deactivate_user(user)

    async def async_activate_user(self, user: User) -> None:
        """Activate a user."""
        await self._store.async_activate_user(user)

    async def async_deactivate_user(self, user: User) -> None:
        """Deactivate a user."""
        if user.is_owner:
            raise ValueError("Unable to deactivate the owner")
        await self._store.async_deactivate_user(user)

    async def async_remove_credentials(self, credentials: Credentials) -> None:
        """Remove credentials."""
        provider = self._async_get_auth_provider(credentials)

        if provider is not None and hasattr(provider, "async_will_remove_credentials"):
            await provider.async_will_remove_credentials(credentials)

        await self._store.async_remove_credentials(credentials)

    async def async_enable_user_mfa(
        self, user: User, mfa_module_id: str, data: typing.Any
    ) -> None:
        """Enable a multi-factor auth module for user."""
        if user.system_generated:
            raise ValueError(
                "System generated users cannot enable multi-factor auth module."
            )

        if (module := self.get_auth_mfa_module(mfa_module_id)) is None:
            raise ValueError(f"Unable find multi-factor auth module: {mfa_module_id}")

        await module.async_setup_user(user.id, data)

    async def async_disable_user_mfa(self, user: User, mfa_module_id: str) -> None:
        """Disable a multi-factor auth module for user."""
        if user.system_generated:
            raise ValueError(
                "System generated users cannot disable multi-factor auth module."
            )

        if (module := self.get_auth_mfa_module(mfa_module_id)) is None:
            raise ValueError(f"Unable find multi-factor auth module: {mfa_module_id}")

        await module.async_depose_user(user.id)

    async def async_get_enabled_mfa(self, user: User) -> dict[str, str]:
        """List enabled mfa modules for user."""
        modules: dict[str, str] = collections.OrderedDict()
        for module_id, module in self._mfa_modules.items():
            if await module.async_is_user_setup(user.id):
                modules[module_id] = module.name
        return modules

    async def async_create_refresh_token(
        self,
        user: User,
        client_id: str = None,
        client_name: str = None,
        client_icon: str = None,
        token_type: str = None,
        access_token_expiration: datetime.timedelta = Const.ACCESS_TOKEN_EXPIRATION,
        credential: Credentials = None,
    ) -> RefreshToken:
        """Create a new refresh token for a user."""
        if not user.is_active:
            raise ValueError("User is not active")

        if user.system_generated and client_id is not None:
            raise ValueError(
                "System generated users cannot have refresh tokens connected "
                + "to a client."
            )

        if token_type is None:
            if user.system_generated:
                token_type = TokenType.SYSTEM
            else:
                token_type = TokenType.NORMAL

        if user.system_generated != (token_type == TokenType.SYSTEM):
            raise ValueError(
                "System generated users can only have system type refresh tokens"
            )

        if token_type == TokenType.NORMAL and client_id is None:
            raise ValueError("Client is required to generate a refresh token.")

        if token_type == TokenType.LONG_LIVED_ACCESS_TOKEN and client_name is None:
            raise ValueError("Client_name is required for long-lived access token")

        if token_type == TokenType.LONG_LIVED_ACCESS_TOKEN:
            for token in user.refresh_tokens.values():
                if (
                    token.client_name == client_name
                    and token.token_type == TokenType.LONG_LIVED_ACCESS_TOKEN
                ):
                    # Each client_name can only have one
                    # long_lived_access_token type of refresh token
                    raise ValueError(f"{client_name} already exists")

        return await self._store.async_create_refresh_token(
            user,
            client_id,
            client_name,
            client_icon,
            token_type,
            access_token_expiration,
            credential,
        )

    async def async_get_refresh_token(self, token_id: str) -> RefreshToken:
        """Get refresh token by id."""
        return await self._store.async_get_refresh_token(token_id)

    async def async_get_refresh_token_by_token(self, token: str) -> RefreshToken:
        """Get refresh token by token."""
        return await self._store.async_get_refresh_token_by_token(token)

    async def async_remove_refresh_token(self, refresh_token: RefreshToken) -> None:
        """Delete a refresh token."""
        await self._store.async_remove_refresh_token(refresh_token)

        callbacks = self._revoke_callbacks.pop(refresh_token.id, [])
        for revoke_callback in callbacks:
            revoke_callback()

    @callback
    def async_register_revoke_token_callback(
        self, refresh_token_id: str, revoke_callback: CallbackType
    ) -> CallbackType:
        """Register a callback to be called when the refresh token id is revoked."""
        if refresh_token_id not in self._revoke_callbacks:
            self._revoke_callbacks[refresh_token_id] = []

        callbacks = self._revoke_callbacks[refresh_token_id]
        callbacks.append(revoke_callback)

        @callback
        def unregister() -> None:
            if revoke_callback in callbacks:
                callbacks.remove(revoke_callback)

        return unregister

    @callback
    def async_create_access_token(
        self, refresh_token: RefreshToken, remote_ip: str = None
    ) -> str:
        """Create a new access token."""
        self.async_validate_refresh_token(refresh_token, remote_ip)

        self._store.async_log_refresh_token_usage(refresh_token, remote_ip)

        now = helpers.utcnow()
        return jwt.encode(
            {
                "iss": refresh_token.id,
                "iat": now,
                "exp": now + refresh_token.access_token_expiration,
            },
            refresh_token.jwt_key,
            algorithm="HS256",
        )

    @callback
    def _async_resolve_provider(self, refresh_token: RefreshToken) -> AuthProvider:
        """Get the auth provider for the given refresh token.

        Raises an exception if the expected provider is no longer available or return
        None if no provider was expected for this refresh token.
        """
        if refresh_token.credential is None:
            return None

        provider = self.get_auth_provider(
            refresh_token.credential.auth_provider_type,
            refresh_token.credential.auth_provider_id,
        )
        if provider is None:
            raise InvalidProvider(
                f"Auth provider {refresh_token.credential.auth_provider_type}, "
                + f"{refresh_token.credential.auth_provider_id} not available"
            )
        return provider

    @callback
    def async_validate_refresh_token(
        self, refresh_token: RefreshToken, remote_ip: str = None
    ) -> None:
        """Validate that a refresh token is usable.

        Will raise InvalidAuthError on errors.
        """
        if provider := self._async_resolve_provider(refresh_token):
            provider.async_validate_refresh_token(refresh_token, remote_ip)

    async def async_validate_access_token(self, token: str) -> RefreshToken:
        """Return refresh token if an access token is valid."""
        try:
            unverif_claims = jwt.decode(
                token, algorithms=["HS256"], options={"verify_signature": False}
            )
        except jwt.InvalidTokenError:
            return None

        refresh_token = await self.async_get_refresh_token(
            typing.cast(str, unverif_claims.get("iss"))
        )

        if refresh_token is None:
            jwt_key = ""
            issuer = ""
        else:
            jwt_key = refresh_token.jwt_key
            issuer = refresh_token.id

        try:
            jwt.decode(token, jwt_key, leeway=10, issuer=issuer, algorithms=["HS256"])
        except jwt.InvalidTokenError:
            return None

        if refresh_token is None or not refresh_token.user.is_active:
            return None

        return refresh_token

    @callback
    def _async_get_auth_provider(self, credentials: Credentials) -> AuthProvider:
        """Get auth provider from a set of credentials."""
        auth_provider_key = (
            credentials.auth_provider_type,
            credentials.auth_provider_id,
        )
        return self._providers.get(auth_provider_key)

    async def _user_should_be_owner(self) -> bool:
        """Determine if user should be owner.

        A user should be an owner if it is the first non-system user that is
        being created.
        """
        for user in await self._store.async_get_users():
            if not user.system_generated:
                return False

        return True

    @staticmethod
    async def from_config(
        shc: SmartHomeController,
        provider_configs: list[dict[str, typing.Any]],
        module_configs: list[dict[str, typing.Any]],
    ):
        """Initialize an auth manager from config.

        CORE_CONFIG_SCHEMA will make sure do duplicated auth providers or
        mfa modules exist in configs.
        """
        store = AuthStore(shc)
        if provider_configs:
            providers = await asyncio.gather(
                *(
                    AuthProvider.from_config(shc, store, config)
                    for config in provider_configs
                )
            )
        else:
            providers = []
        # So returned auth providers are in same order as config
        provider_hash: _ProviderDict = collections.OrderedDict()
        for provider in providers:
            key = (provider.type, provider.id)
            provider_hash[key] = provider

        if module_configs:
            modules = await asyncio.gather(
                *(
                    MultiFactorAuthModule.from_config(shc, config)
                    for config in module_configs
                )
            )
        else:
            modules = []
        # So returned auth modules are in same order as config
        module_hash: _MfaModuleDict = collections.OrderedDict()
        for module in modules:
            module_hash[module.id] = module

        return AuthManager(shc, store, provider_hash, module_hash)
