"""
Home Assistant Cloud Component for Smart Home - The Next Generation.

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
import logging
import typing

import hass_nabucasa.account_link as nabucasa_account_link  # pylint: disable=import-error

from ... import core

_LOGGER: typing.Final = logging.getLogger(__name__)


# pylint: disable=unused-variable
class CloudOAuth2Implementation(core.AbstractOAuth2Implementation):
    """Cloud implementation of the OAuth2 flow."""

    def __init__(self, owner: core.CloudComponent, service: str) -> None:
        """Initialize cloud OAuth2 implementation."""
        self._owner = owner
        self._service = service

    @property
    def name(self) -> str:
        """Name of the implementation."""
        return "Home Assistant Cloud"

    @property
    def domain(self) -> str:
        """Domain that is providing the implementation."""
        return self._owner.domain

    async def async_generate_authorize_url(self, flow_id: str) -> str:
        """Generate a url for the user to authorize."""
        helper = nabucasa_account_link.AuthorizeAccountHelper(
            self._owner.cloud, self._service
        )
        authorize_url = await helper.async_get_authorize_url()

        async def await_tokens():
            """Wait for tokens and pass them on when received."""
            try:
                tokens = await helper.async_get_tokens()

            except asyncio.TimeoutError:
                _LOGGER.info(f"Timeout fetching tokens for flow {flow_id}")
            except nabucasa_account_link.AccountLinkException as err:
                _LOGGER.info(f"Failed to fetch tokens for flow {flow_id}: {err.code}")
            else:
                await self._owner.controller.config_entries.flow.async_configure(
                    flow_id=flow_id, user_input=tokens
                )

        self._owner.controller.async_create_task(await_tokens())

        return authorize_url

    async def async_resolve_external_data(self, external_data: typing.Any) -> dict:
        """Resolve external data to tokens."""
        # We already passed in tokens
        return external_data

    async def _async_refresh_token(self, token: dict) -> dict:
        """Refresh a token."""
        new_token = await nabucasa_account_link.async_fetch_access_token(
            self._owner.cloud, self._service, token["refresh_token"]
        )
        return {**token, **new_token}
