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

import time
import typing

from aiohttp import client

from .abstract_oauth2_implementation import AbstractOAuth2Implementation
from .config_entry import ConfigEntry
from .http_client import HttpClient

_CLOCK_OUT_OF_SYNC_MAX_SEC: typing.Final = 20


if not typing.TYPE_CHECKING:

    class SmartHomeController:
        ...


if typing.TYPE_CHECKING:
    from ..core.smart_home_controller import SmartHomeController


# pylint: disable=unused-variable
class OAuth2Session:
    """Session to make requests authenticated with OAuth2."""

    def __init__(
        self,
        shc: SmartHomeController,
        config_entry: ConfigEntry,
        implementation: AbstractOAuth2Implementation,
    ) -> None:
        """Initialize an OAuth2 session."""
        self._shc = shc
        self._config_entry = config_entry
        self._implementation = implementation

    @property
    def token(self) -> dict:
        """Return the token."""
        return typing.cast(dict, self._config_entry.data["token"])

    @property
    def valid_token(self) -> bool:
        """Return if token is still valid."""
        return (
            typing.cast(float, self.token["expires_at"])
            > time.time() + _CLOCK_OUT_OF_SYNC_MAX_SEC
        )

    async def async_ensure_token_valid(self) -> None:
        """Ensure that the current token is valid."""
        if self.valid_token:
            return

        new_token = await self._implementation.async_refresh_token(self.token)

        self._shc.config_entries.async_update_entry(
            self._config_entry, data={**self._config_entry.data, "token": new_token}
        )

    async def async_request(
        self, method: str, url: str, **kwargs: typing.Any
    ) -> client.ClientResponse:
        """Make a request."""
        await self.async_ensure_token_valid()
        return await async_oauth2_request(
            self._shc, self._config_entry.data["token"], method, url, **kwargs
        )


async def async_oauth2_request(
    shc: SmartHomeController, token: dict, method: str, url: str, **kwargs: typing.Any
) -> client.ClientResponse:
    """Make an OAuth2 authenticated request.

    This method will not refresh tokens. Use OAuth2 session for that.
    """
    session = HttpClient.async_get_clientsession(shc)
    headers = kwargs.pop("headers", {})
    return await session.request(
        method,
        url,
        **kwargs,
        headers={
            **headers,
            "authorization": f"Bearer {token['access_token']}",
        },
    )
