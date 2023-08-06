"""
Application Credentials Integration for Smart Home - The Next Generation.

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
import typing

import voluptuous as vol

from ... import core
from .application_credentials_storage_collection import (
    ApplicationCredentialsStorageCollection,
)
from .auth_implementation import AuthImplementation
from .const import Const

_LOGGER: typing.Final = logging.getLogger(__name__)

_INTEGRATION_LIST: typing.Final = {
    vol.Required("type"): "application_credentials/config"
}


# pylint: disable=unused-variable
class ApplicationCredentials(core.SmartHomeControllerComponent):
    """The Application Credentials integration.

    This integration provides APIs for managing local OAuth credentials on behalf
    of other integrations. Integrations register an authorization server, and then
    the APIs are used to add one or more client credentials. Integrations may also
    provide credentials from yaml for backwards compatibility.
    """

    def __init__(self, path: typing.Iterable[str]):
        super().__init__(path)
        self._storage_collection: ApplicationCredentialsStorageCollection = None

    async def async_setup(self, config: core.ConfigType) -> bool:
        """Set up Application Credentials."""
        if not await super().async_setup(config):
            return False

        api = self.controller.components.websocket_api
        if not isinstance(api, core.WebSocket.Component):
            return False

        id_manager = core.IDManager()
        self._storage_collection = ApplicationCredentialsStorageCollection(
            self,
            core.Store(self._shc, self.storage_version, self.storage_key),
            logging.getLogger(f"{__name__}.storage_collection"),
            id_manager,
        )
        await self._storage_collection.async_load()

        core.StorageCollectionWebSocket(
            self._storage_collection,
            self.domain,
            self.domain,
            Const.CREATE_FIELDS,
            Const.UPDATE_FIELDS,
        ).async_setup()

        api.register_command(_handle_integration_list, _INTEGRATION_LIST)

        core.AbstractOAuth2Implementation.async_add_implementation_provider(
            self.domain, self._async_provide_implementation
        )

        return True

    async def async_import_client_credential(
        self,
        domain: str,
        credential: core.ClientCredential,
        auth_domain: str = None,
    ) -> None:
        """Import an existing credential from configuration.yaml."""
        item = {
            core.Const.CONF_DOMAIN: domain,
            core.Const.CONF_CLIENT_ID: credential.client_id,
            core.Const.CONF_CLIENT_SECRET: credential.client_secret,
            Const.CONF_AUTH_DOMAIN: auth_domain if auth_domain else domain,
        }
        item[core.Const.CONF_NAME] = (
            credential.name if credential.name else Const.DEFAULT_IMPORT_NAME
        )
        await self._storage_collection.async_import_item(item)

    async def _async_provide_implementation(
        self, domain: str
    ) -> list[core.AbstractOAuth2Implementation]:
        """Return registered OAuth implementations."""

        platform = await self._get_platform(domain)
        if not platform:
            return []

        credentials = self._storage_collection.async_client_credentials(domain)
        authorization_server = await platform.async_get_authorization_server()
        if authorization_server is not None:
            return [
                AuthImplementation(
                    self._shc, auth_domain, credential, authorization_server
                )
                for auth_domain, credential in credentials.items()
            ]
        return [
            await platform.async_get_auth_implementation(
                self._shc, auth_domain, credential
            )
            for auth_domain, credential in credentials.items()
        ]

    async def _get_platform(self, domain: str) -> core.ApplicationCredentialsPlatform:
        """Register an application_credentials platform."""
        try:
            await self._shc.shc.setup.async_get_integration(domain)
        except core.IntegrationNotFound as err:
            _LOGGER.debug(f"Integration '{domain}' does not exist: {err}")
            return None

        platform = None
        try:
            component = core.SmartHomeControllerComponent.get_component(domain)
            if component is not None:
                platform = component.get_platform(core.Platform.APPLICATION_CREDENTIALS)
                if not isinstance(platform, core.ApplicationCredentialsPlatform):
                    platform = None
            if platform is None:
                _LOGGER.debug(
                    f"Integration '{domain}' does not provide application_credentials.",
                )
        except ImportError as err:
            _LOGGER.debug(
                f"Integration '{domain}' does not provide application_credentials: {err}",
            )

        return platform


async def _handle_integration_list(
    connection: core.WebSocket.Connection,
    msg: dict[str, typing.Any],
) -> None:
    """Handle integrations command."""
    shc = connection.owner.controller
    connection.send_result(
        msg["id"], {"domains": await shc.setup.async_get_application_credentials()}
    )
