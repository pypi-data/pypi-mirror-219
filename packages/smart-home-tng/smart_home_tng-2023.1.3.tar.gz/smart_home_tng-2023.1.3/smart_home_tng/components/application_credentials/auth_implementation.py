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

from ... import core


# pylint: disable=unused-variable
class AuthImplementation(core.LocalOAuth2Implementation):
    """Application Credentials local oauth2 implementation."""

    def __init__(
        self,
        shc: core.SmartHomeController,
        auth_domain: str,
        credential: core.ClientCredential,
        authorization_server: core.AuthorizationServer,
    ) -> None:
        """Initialize AuthImplementation."""
        super().__init__(
            shc,
            auth_domain,
            credential.client_id,
            credential.client_secret,
            authorization_server.authorize_url,
            authorization_server.token_url,
        )
        self._name = credential.name

    @property
    def name(self) -> str:
        """Name of the implementation."""
        return self._name or self._client_id
