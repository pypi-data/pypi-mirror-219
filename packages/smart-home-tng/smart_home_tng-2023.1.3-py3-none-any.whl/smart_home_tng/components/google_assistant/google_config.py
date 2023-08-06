"""
Google Assistant Integration  for Smart Home - The Next Generation.

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
import logging
import typing
import uuid

import aiohttp
import jwt

from ... import core

_LOGGER: typing.Final = logging.getLogger(__name__)


# pylint: disable=unused-variable
class GoogleConfig(core.GoogleAssistant.AbstractConfig):
    """Config for manual setup of Google."""

    def __init__(self, owner: core.GoogleAssistant.Component, config: core.ConfigType):
        """Initialize the config."""
        super().__init__(owner)
        self._config = config
        self._access_token = None
        self._access_token_renew = None

    async def async_initialize(self):
        """Perform async initialization of config."""
        await super().async_initialize()

        self.async_enable_local_sdk()

    @property
    def owner(self) -> core.GoogleAssistant.Component:
        return self._owner

    @property
    def enabled(self):
        """Return if Google is enabled."""
        return True

    @property
    def entity_config(self):
        """Return entity config."""
        return self._config.get(core.GoogleAssistant.CONF_ENTITY_CONFIG) or {}

    @property
    def secure_devices_pin(self):
        """Return entity config."""
        return self._config.get(core.GoogleAssistant.CONF_SECURE_DEVICES_PIN)

    @property
    def should_report_state(self):
        """Return if states should be proactively reported."""
        return self._config.get(core.GoogleAssistant.CONF_REPORT_STATE)

    def should_expose(self, state) -> bool:
        """Return if entity should be exposed."""
        expose_by_default = self._config.get(
            core.GoogleAssistant.CONF_EXPOSE_BY_DEFAULT
        )
        exposed_domains = self._config.get(core.GoogleAssistant.CONF_EXPOSED_DOMAINS)

        if state.attributes.get("view") is not None:
            # Ignore entities that are views
            return False

        if state.entity_id in core.Const.CLOUD_NEVER_EXPOSED_ENTITIES:
            return False

        entity_registry = self.controller.entity_registry
        registry_entry = entity_registry.async_get(state.entity_id)
        if registry_entry:
            auxiliary_entity = (
                registry_entry.entity_category is not None
                or registry_entry.hidden_by is not None
            )
        else:
            auxiliary_entity = False

        explicit_expose = self.entity_config.get(state.entity_id, {}).get(
            core.GoogleAssistant.CONF_EXPOSE
        )

        domain_exposed_by_default = (
            expose_by_default and state.domain in exposed_domains
        )

        # Expose an entity by default if the entity's domain is exposed by default
        # and the entity is not a config or diagnostic entity
        entity_exposed_by_default = domain_exposed_by_default and not auxiliary_entity

        # Expose an entity if the entity's is exposed by default and
        # the configuration doesn't explicitly exclude it from being
        # exposed, or if the entity is explicitly exposed
        is_default_exposed = entity_exposed_by_default and explicit_expose is not False

        return is_default_exposed or explicit_expose

    def get_agent_user_id(self, context):
        """Get agent user ID making request."""
        return context.user_id

    def should_2fa(self, _state):
        """If an entity should have 2FA checked."""
        return True

    async def _async_request_sync_devices(self, agent_user_id: str):
        if core.GoogleAssistant.CONF_SERVICE_ACCOUNT in self._config:
            return await self.async_call_homegraph_api(
                core.GoogleAssistant.REQUEST_SYNC_BASE_URL,
                {"agentUserId": agent_user_id},
            )

        _LOGGER.error("No configuration for request_sync available")
        return http.HTTPStatus.INTERNAL_SERVER_ERROR

    async def _async_update_token(self, force=False):
        if core.GoogleAssistant.CONF_SERVICE_ACCOUNT not in self._config:
            _LOGGER.error("Trying to get homegraph api token without service account")
            return

        now = core.helpers.utcnow()
        if not self._access_token or now > self._access_token_renew or force:
            token = await _get_homegraph_token(
                self.controller,
                _get_homegraph_jwt(
                    now,
                    self._config[core.GoogleAssistant.CONF_SERVICE_ACCOUNT][
                        core.GoogleAssistant.CONF_CLIENT_EMAIL
                    ],
                    self._config[core.GoogleAssistant.CONF_SERVICE_ACCOUNT][
                        core.GoogleAssistant.CONF_PRIVATE_KEY
                    ],
                ),
            )
            self._access_token = token["access_token"]
            self._access_token_renew = now + dt.timedelta(seconds=token["expires_in"])

    async def async_call_homegraph_api(self, url, data):
        """Call a homegraph api with authentication."""
        session = core.HttpClient.async_get_clientsession(self.controller)

        async def _call():
            headers = {
                "Authorization": f"Bearer {self._access_token}",
                "X-GFE-SSL": "yes",
            }
            async with session.post(url, headers=headers, json=data) as res:
                _LOGGER.debug(
                    f"Response on {url} with data {data} was {await res.text()}"
                )
                res.raise_for_status()
                return res.status

        try:
            await self._async_update_token()
            try:
                return await _call()
            except aiohttp.ClientResponseError as error:
                if error.status == http.HTTPStatus.UNAUTHORIZED:
                    _LOGGER.warning(
                        f"Request for {url} unauthorized, renewing token and retrying"
                    )
                    await self._async_update_token(True)
                    return await _call()
                raise
        except aiohttp.ClientResponseError as error:
            _LOGGER.error(f"Request for {url} failed: {error.status}")
            return error.status
        except (asyncio.TimeoutError, aiohttp.ClientError):
            _LOGGER.error(f"Could not contact {url}")
            return http.HTTPStatus.INTERNAL_SERVER_ERROR

    async def async_report_state(self, message, agent_user_id: str):
        """Send a state report to Google."""
        data = {
            "requestId": uuid.uuid4().hex,
            "agentUserId": agent_user_id,
            "payload": message,
        }
        await self.async_call_homegraph_api(
            core.GoogleAssistant.REPORT_STATE_BASE_URL, data
        )


def _get_homegraph_jwt(time, iss, key):
    now = int(time.timestamp())

    jwt_raw = {
        "iss": iss,
        "scope": core.GoogleAssistant.HOMEGRAPH_SCOPE,
        "aud": core.GoogleAssistant.HOMEGRAPH_TOKEN_URL,
        "iat": now,
        "exp": now + 3600,
    }
    return jwt.encode(jwt_raw, key, algorithm="RS256")


async def _get_homegraph_token(
    shc: core.SmartHomeController, jwt_signed: str
) -> dict[str, typing.Any] | list[typing.Any] | typing.Any:
    headers = {
        "Authorization": f"Bearer {jwt_signed}",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    data = {
        "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
        "assertion": jwt_signed,
    }

    session = core.HttpClient.async_get_clientsession(shc)
    async with session.post(
        core.GoogleAssistant.HOMEGRAPH_TOKEN_URL, headers=headers, data=data
    ) as res:
        res.raise_for_status()
        return await res.json()
