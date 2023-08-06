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

import datetime
import typing
import uuid

import voluptuous as vol

from ... import auth, core
from .auth_provider_view import AuthProvidersView
from .link_user_view import LinkUserView
from .login_flow_index_view import LoginFlowIndexView
from .login_flow_resource_view import LoginFlowResourceView
from .mfa_flow_manager import MfaFlowManager
from .revoke_token_view import RevokeTokenView
from .token_view import TokenView

_WS_TYPE_CURRENT_USER: typing.Final = "auth/current_user"
_WS_CURRENT_USER: typing.Final = {vol.Required("type"): _WS_TYPE_CURRENT_USER}
_WS_TYPE_LONG_LIVED_ACCESS_TOKEN: typing.Final = "auth/long_lived_access_token"
_WS_LONG_LIVED_ACCESS_TOKEN: typing.Final = {
    vol.Required("type"): _WS_TYPE_LONG_LIVED_ACCESS_TOKEN,
    vol.Required("lifespan"): int,  # days
    vol.Required("client_name"): str,
    vol.Optional("client_icon"): str,
}
_WS_TYPE_REFRESH_TOKENS: typing.Final = "auth/refresh_tokens"
_WS_REFRESH_TOKENS: typing.Final = {vol.Required("type"): _WS_TYPE_REFRESH_TOKENS}
_WS_TYPE_DELETE_REFRESH_TOKEN: typing.Final = "auth/delete_refresh_token"
_WS_DELETE_REFRESH_TOKEN = {
    vol.Required("type"): _WS_TYPE_DELETE_REFRESH_TOKEN,
    vol.Required("refresh_token_id"): str,
}
_WS_TYPE_SIGN_PATH: typing.Final = "auth/sign_path"
_WS_SIGN_PATH: typing.Final = {
    vol.Required("type"): _WS_TYPE_SIGN_PATH,
    vol.Required("path"): str,
    vol.Optional("expires", default=30): int,
}


# pylint: disable=unused-variable
class Auth(core.AuthComponent):
    """Component to allow users to login and get tokens.

    # POST /auth/token

    This is an OAuth2 endpoint for granting tokens. We currently support the grant
    types "authorization_code" and "refresh_token". Because we follow the OAuth2
    spec, data should be send in formatted as x-www-form-urlencoded. Examples will
    be in JSON as it's more readable.

    ## Grant type authorization_code

    Exchange the authorization code retrieved from the login flow for tokens.

    {
        "client_id": "https://hassbian.local:8123/",
        "grant_type": "authorization_code",
        "code": "411ee2f916e648d691e937ae9344681e"
    }

    Return value will be the access and refresh tokens. The access token will have
    a limited expiration. New access tokens can be requested using the refresh
    token. The value ha_auth_provider will contain the auth provider type that was
    used to authorize the refresh token.

    {
        "access_token": "ABCDEFGH",
        "expires_in": 1800,
        "refresh_token": "IJKLMNOPQRST",
        "token_type": "Bearer",
        "ha_auth_provider": "homeassistant"
    }

    ## Grant type refresh_token

    Request a new access token using a refresh token.

    {
        "client_id": "https://hassbian.local:8123/",
        "grant_type": "refresh_token",
        "refresh_token": "IJKLMNOPQRST"
    }

    Return value will be a new access token. The access token will have
    a limited expiration.

    {
        "access_token": "ABCDEFGH",
        "expires_in": 1800,
        "token_type": "Bearer"
    }

    ## Revoking a refresh token

    It is also possible to revoke a refresh token and all access tokens that have
    ever been granted by that refresh token. Response code will ALWAYS be 200.

    {
        "token": "IJKLMNOPQRST",
        "action": "revoke"
    }

    # Websocket API

    ## Get current user

    Send websocket command `auth/current_user` will return current user of the
    active websocket connection.

    {
        "id": 10,
        "type": "auth/current_user",
    }

    The result payload likes

    {
        "id": 10,
        "type": "result",
        "success": true,
        "result": {
            "id": "USER_ID",
            "name": "John Doe",
            "is_owner": true,
            "credentials": [{
                "auth_provider_type": "homeassistant",
                "auth_provider_id": null
            }],
            "mfa_modules": [{
                "id": "totp",
                "name": "TOTP",
                "enabled": true
            }]
        }
    }

    ## Create a long-lived access token

    Send websocket command `auth/long_lived_access_token` will create
    a long-lived access token for current user. Access token will not be saved in
    Home Assistant. User need to record the token in secure place.

    {
        "id": 11,
        "type": "auth/long_lived_access_token",
        "client_name": "GPS Logger",
        "lifespan": 365
    }

    Result will be a long-lived access token:

    {
        "id": 11,
        "type": "result",
        "success": true,
        "result": "ABCDEFGH"
    }


    # POST /auth/external/callback

    This is an endpoint for OAuth2 Authorization callbacks used by integrations
    that link accounts with other cloud providers using LocalOAuth2Implementation
    as part of a config flow.
    """

    def create_auth_code(self, client_id: str, credential: auth.Credentials) -> str:
        """Create an authorization code to fetch tokens."""
        if self._shc is None:
            return None
        return self._shc.data[self.domain](client_id, credential)

    async def async_setup(self, config: core.ConfigType) -> bool:
        """Component to allow users to login."""
        # pylint: disable=no-member
        result = await super().async_setup(config)
        api = self.controller.components.websocket_api
        if not isinstance(api, core.WebSocket.Component) or not result:
            return False
        store_result, retrieve_result = _create_auth_code_store()

        self._shc.data[self.domain] = store_result

        self._shc.register_view(TokenView(retrieve_result))
        self._shc.register_view(RevokeTokenView())
        self._shc.register_view(LinkUserView(retrieve_result))
        self._shc.register_view(core.OAuth2AuthorizeCallbackView())

        api.register_command(
            _WS_TYPE_CURRENT_USER,
            _WS_CURRENT_USER,
            _websocket_current_user,
        )
        api.register_command(
            _WS_TYPE_LONG_LIVED_ACCESS_TOKEN,
            _WS_LONG_LIVED_ACCESS_TOKEN,
            _websocket_create_long_lived_access_token,
        )
        api.register_command(
            _WS_TYPE_REFRESH_TOKENS,
            _WS_REFRESH_TOKENS,
            _websocket_refresh_tokens,
        )
        api.register_command(
            _WS_TYPE_DELETE_REFRESH_TOKEN,
            _WS_DELETE_REFRESH_TOKEN,
            _websocket_delete_refresh_token,
        )
        api.register_command(
            _WS_TYPE_SIGN_PATH,
            _WS_SIGN_PATH,
            _websocket_sign_path,
        )

        await _async_setup(self._shc, store_result)
        await MfaFlowManager.async_setup(api)

        return result


async def _async_setup(shc: core.SmartHomeController, store_result):
    """Component to allow users to login."""
    shc.register_view(AuthProvidersView)
    shc.register_view(LoginFlowIndexView(shc.auth.login_flow, store_result))
    shc.register_view(LoginFlowResourceView(shc.auth.login_flow, store_result))


@core.callback
def _websocket_sign_path(connection: core.WebSocket.Connection, msg: dict):
    """Handle a sign path request."""
    if connection.check_user(msg["id"]):
        connection.send_result(
            msg["id"],
            {
                "path": connection.owner.controller.http.async_sign_path(
                    msg["path"],
                    datetime.timedelta(seconds=msg["expires"]),
                )
            },
        )


@core.callback
def _create_auth_code_store():
    """Create an in memory store."""
    temp_results = {}

    @core.callback
    def store_result(client_id, result):
        """Store flow result and return a code to retrieve it."""
        if not isinstance(result, auth.Credentials):
            raise ValueError("result has to be a Credentials instance")

        code = uuid.uuid4().hex
        temp_results[(client_id, code)] = (
            core.helpers.utcnow(),
            result,
        )
        return code

    @core.callback
    def retrieve_result(client_id, code):
        """Retrieve flow result."""
        key = (client_id, code)

        if key in temp_results:
            created, result = temp_results.pop(key)
        else:
            return None

        # OAuth 4.2.1
        # The authorization code MUST expire shortly after it is issued to
        # mitigate the risk of leaks.  A maximum authorization code lifetime of
        # 10 minutes is RECOMMENDED.
        if core.helpers.utcnow() - created < datetime.timedelta(minutes=10):
            return result

        return None

    return store_result, retrieve_result


async def _websocket_current_user(connection: core.WebSocket.Connection, msg: dict):
    """Return the current user."""
    if not connection.check_user(msg["id"]):
        return

    shc = connection.owner.controller
    user = connection.user
    enabled_modules = await shc.auth.async_get_enabled_mfa(user)

    connection.send_result(
        msg["id"],
        {
            "id": user.id,
            "name": user.name,
            "is_owner": user.is_owner,
            "is_admin": user.is_admin,
            "credentials": [
                {
                    "auth_provider_type": c.auth_provider_type,
                    "auth_provider_id": c.auth_provider_id,
                }
                for c in user.credentials
            ],
            "mfa_modules": [
                {
                    "id": module.id,
                    "name": module.name,
                    "enabled": module.id in enabled_modules,
                }
                for module in shc.auth.auth_mfa_modules
            ],
        },
    )


async def _websocket_create_long_lived_access_token(
    connection: core.WebSocket.Connection, msg: dict
):
    """Create or a long-lived access token."""
    if not connection.check_user(msg["id"]):
        return

    shc = connection.owner.controller
    refresh_token = await shc.auth.async_create_refresh_token(
        connection.user,
        client_name=msg["client_name"],
        client_icon=msg.get("client_icon"),
        token_type=auth.TokenType.LONG_LIVED_ACCESS_TOKEN,
        access_token_expiration=datetime.timedelta(days=msg["lifespan"]),
    )

    try:
        access_token = shc.auth.async_create_access_token(refresh_token)
    except auth.InvalidAuthError as exc:
        connection.send_error(msg["id"], core.WebSocket.ERR_UNAUTHORIZED, str(exc))
        return

    connection.send_result(msg["id"], access_token)


@core.callback
def _websocket_refresh_tokens(connection: core.WebSocket.Connection, msg: dict):
    """Return metadata of users refresh tokens."""
    if not connection.check_user(msg["id"]):
        return

    current_id = connection.refresh_token_id
    connection.send_result(
        msg["id"],
        [
            {
                "id": refresh.id,
                "client_id": refresh.client_id,
                "client_name": refresh.client_name,
                "client_icon": refresh.client_icon,
                "type": refresh.token_type,
                "created_at": refresh.created_at,
                "is_current": refresh.id == current_id,
                "last_used_at": refresh.last_used_at,
                "last_used_ip": refresh.last_used_ip,
            }
            for refresh in connection.user.refresh_tokens.values()
        ],
    )


async def _websocket_delete_refresh_token(
    connection: core.WebSocket.Connection, msg: dict
):
    """Handle a delete refresh token request."""
    if not connection.check_user(msg["id"]):
        return
    shc = connection.owner.controller
    refresh_token = connection.user.refresh_tokens.get(msg["refresh_token_id"])

    if refresh_token is None:
        return connection.send_error(
            msg["id"], "invalid_token_id", "Received invalid token"
        )

    await shc.auth.async_remove_refresh_token(refresh_token)

    connection.send_result(msg["id"], {})
