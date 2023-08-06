"""
Amazon Alexa Integration for Smart Home - The Next Generation.

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
import datetime as dt
import http
import json
import logging
import typing

import aiohttp
import async_timeout

from ... import core

_const: typing.TypeAlias = core.Const

_LOGGER: typing.Final = logging.getLogger(__name__)

_LWA_TOKEN_URI: typing.Final = "https://api.amazon.com/auth/o2/token"
_LWA_HEADERS: typing.Final = {
    "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8"
}

_PREEMPTIVE_REFRESH_TTL_IN_SECONDS: typing.Final = 300
_STORAGE_KEY: typing.Final = "alexa.auth"
_STORAGE_VERSION: typing.Final = 1
_STORAGE_EXPIRE_TIME: typing.Final = "expire_time"
_STORAGE_ACCESS_TOKEN: typing.Final = "access_token"
_STORAGE_REFRESH_TOKEN: typing.Final = "refresh_token"


# pylint: disable=unused-variable
class Auth:
    """Handle authentication to send events to Alexa."""

    def __init__(
        self, shc: core.SmartHomeController, client_id: str, client_secret: str
    ):
        """Initialize the Auth class."""
        self._shc = shc

        self._client_id = client_id
        self._client_secret = client_secret

        self._prefs = None
        self._store = core.Store(shc, _STORAGE_VERSION, _STORAGE_KEY)
        self._get_token_lock = asyncio.Lock()

    async def async_do_auth(self, accept_grant_code: str):
        """Do authentication with an AcceptGrant code."""
        # access token not retrieved yet for the first time, so this should
        # be an access token request

        lwa_params = {
            "grant_type": "authorization_code",
            "code": accept_grant_code,
            _const.CONF_CLIENT_ID: self._client_id,
            _const.CONF_CLIENT_SECRET: self._client_secret,
        }
        _LOGGER.debug(
            f"Calling LWA to get the access token (first time), with: {json.dumps(lwa_params)}",
        )

        return await self._async_request_new_token(lwa_params)

    @core.callback
    def async_invalidate_access_token(self):
        """Invalidate access token."""
        self._prefs[_STORAGE_ACCESS_TOKEN] = None

    async def async_get_access_token(self):
        """Perform access token or token refresh request."""
        async with self._get_token_lock:
            if self._prefs is None:
                await self.async_load_preferences()

            if self.is_token_valid:
                _LOGGER.debug("Token still valid, using it")
                return self._prefs[_STORAGE_ACCESS_TOKEN]

            if self._prefs[_STORAGE_REFRESH_TOKEN] is None:
                _LOGGER.debug("Token invalid and no refresh token available")
                return None

            lwa_params = {
                "grant_type": "refresh_token",
                "refresh_token": self._prefs[_STORAGE_REFRESH_TOKEN],
                _const.CONF_CLIENT_ID: self._client_id,
                _const.CONF_CLIENT_SECRET: self._client_secret,
            }

            _LOGGER.debug("Calling LWA to refresh the access token")
            return await self._async_request_new_token(lwa_params)

    @property
    def is_token_valid(self):
        """Check if a token is already loaded and if it is still valid."""
        if not self._prefs[_STORAGE_ACCESS_TOKEN]:
            return False

        expire_time = core.helpers.parse_datetime(self._prefs[_STORAGE_EXPIRE_TIME])
        preemptive_expire_time = expire_time - dt.timedelta(
            seconds=_PREEMPTIVE_REFRESH_TTL_IN_SECONDS
        )

        return core.helpers.utcnow() < preemptive_expire_time

    async def _async_request_new_token(self, lwa_params: dict):
        try:
            session = core.HttpClient.async_get_clientsession(self._shc)
            async with async_timeout.timeout(10):
                response = await session.post(
                    _LWA_TOKEN_URI,
                    headers=_LWA_HEADERS,
                    data=lwa_params,
                    allow_redirects=True,
                )

        except (asyncio.TimeoutError, aiohttp.ClientError):
            _LOGGER.error("Timeout calling LWA to get auth token")
            return None

        _LOGGER.debug(f"LWA response header: {response.headers}")
        _LOGGER.debug(f"LWA response status: {response.status}")

        if response.status != http.HTTPStatus.OK:
            _LOGGER.error("Error calling LWA to get auth token")
            return None

        response_json = await response.json()
        _LOGGER.debug(f"LWA response body  : {response_json}")

        access_token = response_json["access_token"]
        refresh_token = response_json["refresh_token"]
        expires_in = response_json["expires_in"]
        expire_time = core.helpers.utcnow() + dt.timedelta(seconds=expires_in)

        await self._async_update_preferences(
            access_token, refresh_token, expire_time.isoformat()
        )

        return access_token

    async def async_load_preferences(self):
        """Load preferences with stored tokens."""
        self._prefs = await self._store.async_load()

        if self._prefs is None:
            self._prefs = {
                _STORAGE_ACCESS_TOKEN: None,
                _STORAGE_REFRESH_TOKEN: None,
                _STORAGE_EXPIRE_TIME: None,
            }

    async def _async_update_preferences(
        self, access_token: str, refresh_token: str, expire_time: dt.datetime
    ):
        """Update user preferences."""
        if self._prefs is None:
            await self.async_load_preferences()

        if access_token is not None:
            self._prefs[_STORAGE_ACCESS_TOKEN] = access_token
        if refresh_token is not None:
            self._prefs[_STORAGE_REFRESH_TOKEN] = refresh_token
        if expire_time is not None:
            self._prefs[_STORAGE_EXPIRE_TIME] = expire_time
        await self._store.async_save(self._prefs)
