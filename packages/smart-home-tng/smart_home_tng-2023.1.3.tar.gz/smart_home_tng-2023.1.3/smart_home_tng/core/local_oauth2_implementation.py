"""
Core components of Smart Home - The Next Generation.

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

import logging
import secrets
import typing

import jwt
import yarl

from .abstract_oauth2_implementation import AbstractOAuth2Implementation
from .http_client import HttpClient
from .callback import callback

_LOGGER: typing.Final = logging.getLogger(__name__)

_DATA_JWT_SECRET: typing.Final = "oauth2.jwt_secret"
_AUTH_CALLBACK_PATH: typing.Final = "/auth/external/callback"
_HEADER_FRONTEND_BASE: typing.Final = "SHC-Frontend-Base"


if not typing.TYPE_CHECKING:

    class SmartHomeController:
        ...


if typing.TYPE_CHECKING:
    from .smart_home_controller import SmartHomeController


# pylint: disable=unused-variable
class LocalOAuth2Implementation(AbstractOAuth2Implementation):
    """Local OAuth2 implementation."""

    def __init__(
        self,
        shc: SmartHomeController,
        domain: str,
        client_id: str,
        client_secret: str,
        authorize_url: str,
        token_url: str,
    ) -> None:
        """Initialize local auth implementation."""
        self._shc = shc
        self._domain = domain
        self._client_id = client_id
        self._client_secret = client_secret
        self._authorize_url = authorize_url
        self._token_url = token_url

    @property
    def name(self) -> str:
        """Name of the implementation."""
        return "Configuration.yaml"

    @property
    def domain(self) -> str:
        """Domain providing the implementation."""
        return self._domain

    @property
    def redirect_uri(self) -> str:
        """Return the redirect uri."""
        if (req := self._shc.http.current_request.get()) is None:
            raise RuntimeError("No current request in context")

        if (shc_host := req.headers.get(_HEADER_FRONTEND_BASE)) is None:
            raise RuntimeError("No header in request")

        return f"{shc_host}{_AUTH_CALLBACK_PATH}"

    @property
    def extra_authorize_data(self) -> dict:
        """Extra data that needs to be appended to the authorize url."""
        return {}

    async def async_generate_authorize_url(self, flow_id: str) -> str:
        """Generate a url for the user to authorize."""
        redirect_uri = self.redirect_uri
        return str(
            yarl.URL(self._authorize_url)
            .with_query(
                {
                    "response_type": "code",
                    "client_id": self._client_id,
                    "redirect_uri": redirect_uri,
                    "state": _encode_jwt(
                        self._shc, {"flow_id": flow_id, "redirect_uri": redirect_uri}
                    ),
                }
            )
            .update_query(self.extra_authorize_data)
        )

    async def async_resolve_external_data(self, external_data: typing.Any) -> dict:
        """Resolve the authorization code to tokens."""
        return await self._token_request(
            {
                "grant_type": "authorization_code",
                "code": external_data["code"],
                "redirect_uri": external_data["state"]["redirect_uri"],
            }
        )

    async def _async_refresh_token(self, token: dict) -> dict:
        """Refresh tokens."""
        new_token = await self._token_request(
            {
                "grant_type": "refresh_token",
                "client_id": self._client_id,
                "refresh_token": token["refresh_token"],
            }
        )
        return {**token, **new_token}

    async def _token_request(self, data: dict) -> dict:
        """Make a token request."""
        session = HttpClient.async_get_clientsession(self._shc)

        data["client_id"] = self._client_id

        if self._client_secret is not None:
            data["client_secret"] = self._client_secret

        resp = await session.post(self._token_url, data=data)
        if resp.status >= 400 and _LOGGER.isEnabledFor(logging.DEBUG):
            body = await resp.text()
            _LOGGER.debug(
                f"Token request failed with status={resp.status}, body={body}"
            )
        resp.raise_for_status()
        return typing.cast(dict, await resp.json())


@callback
def _encode_jwt(shc: SmartHomeController, data: dict) -> str:
    """JWT encode data."""
    if (secret := shc.data.get(_DATA_JWT_SECRET)) is None:
        secret = shc.data[_DATA_JWT_SECRET] = secrets.token_hex()

    return jwt.encode(data, secret, algorithm="HS256")


# pylint: disable=unused-variable
@callback
def _decode_jwt(shc: SmartHomeController, encoded: str) -> dict:
    """JWT encode data."""
    secret = typing.cast(str, shc.data.get(_DATA_JWT_SECRET))

    try:
        return jwt.decode(encoded, secret, algorithms=["HS256"])
    except jwt.InvalidTokenError:
        return None
