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

import typing

from ... import core
from .auth import Auth

_alexa: typing.TypeAlias = core.Alexa
_const: typing.TypeAlias = core.Const


# pylint: disable=unused-variable
class AlexaConfig(_alexa.AbstractConfig):
    """Alexa config."""

    def __init__(self, shc: core.SmartHomeController, config: core.ConfigType):
        """Initialize Alexa config."""
        super().__init__(shc)
        self._config = config

        client_id = config.get(_const.CONF_CLIENT_ID)
        client_secret = config.get(_const.CONF_CLIENT_SECRET)
        if client_id and client_secret:
            self._auth = Auth(self._shc, client_id, client_secret)
        else:
            self._auth = None

    @property
    def supports_auth(self):
        """Return if config supports auth."""
        return self._auth is not None

    @property
    def should_report_state(self) -> bool:
        """Return if we should proactively report states."""
        return self._auth is not None and self.authorized

    @property
    def endpoint(self):
        """Endpoint for report state."""
        return self._config.get(_alexa.CONF_ENDPOINT)

    @property
    def entity_config(self):
        """Return entity config."""
        return self._config.get(_alexa.CONF_ENTITY_CONFIG, {})

    @property
    def locale(self):
        """Return config locale."""
        return self._config.get(_alexa.CONF_LOCALE)

    @core.callback
    def user_identifier(self):
        """Return an identifier for the user that represents this config."""
        return ""

    def should_expose(self, entity_id: str) -> bool:
        """If an entity should be exposed."""
        conf_filter = self._config[_alexa.CONF_FILTER]
        if not conf_filter.empty_filter:
            return conf_filter(entity_id)

        entity_registry = self._shc.entity_registry
        if registry_entry := entity_registry.async_get(entity_id):
            auxiliary_entity = (
                registry_entry.entity_category is not None
                or registry_entry.hidden_by is not None
            )
        else:
            auxiliary_entity = False
        return not auxiliary_entity

    @core.callback
    def async_invalidate_access_token(self):
        """Invalidate access token."""
        self._auth.async_invalidate_access_token()

    async def async_get_access_token(self):
        """Get an access token."""
        return await self._auth.async_get_access_token()

    async def async_accept_grant(self, code: str):
        """Accept a grant."""
        return await self._auth.async_do_auth(code)
