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

import abc
import time
import typing

from .callback import callback
from .config_entry import ConfigEntry
from .oauth2_provider import OAuth2Provider
from .registry import Registry


_PROVIDERS: typing.Final[Registry[str, OAuth2Provider]] = Registry()
_AbstractImplementationT = typing.TypeVar(
    "_AbstractImplementationT", bound="AbstractOAuth2Implementation"
)


# pylint: disable=unused-variable
class AbstractOAuth2Implementation(abc.ABC):
    """Base class to abstract OAuth2 authentication."""

    @property
    @abc.abstractmethod
    def name(self) -> str:
        """Name of the implementation."""

    @property
    @abc.abstractmethod
    def domain(self) -> str:
        """Domain that is providing the implementation."""

    @abc.abstractmethod
    async def async_generate_authorize_url(self, flow_id: str) -> str:
        """Generate a url for the user to authorize.

        This step is called when a config flow is initialized. It should redirect the
        user to the vendor website where they can authorize Home Assistant.

        The implementation is responsible to get notified when the user is authorized
        and pass this to the specified config flow. Do as little work as possible once
        notified. You can do the work inside async_resolve_external_data. This will
        give the best UX.

        Pass external data in with:

        await hass.config_entries.flow.async_configure(
            flow_id=flow_id, user_input={'code': 'abcd', 'state': { … }
        )

        """

    @abc.abstractmethod
    async def async_resolve_external_data(self, external_data: typing.Any) -> dict:
        """Resolve external data to tokens.

        Turn the data that the implementation passed to the config flow as external
        step data into tokens. These tokens will be stored as 'token' in the
        config entry data.
        """

    async def async_refresh_token(self, token: dict) -> dict:
        """Refresh a token and update expires info."""
        new_token = await self._async_refresh_token(token)
        # Force int for non-compliant oauth2 providers
        new_token["expires_in"] = int(new_token["expires_in"])
        new_token["expires_at"] = time.time() + new_token["expires_in"]
        return new_token

    @abc.abstractmethod
    async def _async_refresh_token(self, token: dict) -> dict:
        """Refresh a token."""

    @staticmethod
    @callback
    def async_register_implementation(
        domain: str, implementation: _AbstractImplementationT
    ) -> None:
        """Register an OAuth2 flow implementation for an integration."""
        _IMPLEMENTATIONS.setdefault(domain, {})[implementation.domain] = implementation

    async def async_get_implementations(
        domain: str,
    ):
        """Return OAuth2 implementations for specified domain."""
        registered = _IMPLEMENTATIONS.get(domain, {})

        if _PROVIDERS is None:
            return registered

        registered = registered.copy()
        for get_impl in _PROVIDERS:
            for impl in await get_impl(domain):
                registered[impl.domain] = impl

        return registered

    @staticmethod
    async def async_get_config_entry_implementation(
        config_entry: ConfigEntry,
    ):
        """Return the implementation for this config entry."""
        implementations = await AbstractOAuth2Implementation.async_get_implementations(
            config_entry.domain
        )
        implementation = implementations.get(config_entry.data["auth_implementation"])

        if implementation is None:
            raise ValueError("Implementation not available")

        return implementation

    @callback
    def async_add_implementation_provider(
        provider_domain: str, async_provide_implementation: OAuth2Provider
    ) -> None:
        """Add an implementation provider.

        If no implementation found, return None.
        """
        _PROVIDERS[provider_domain] = async_provide_implementation


_IMPLEMENTATIONS: typing.Final[
    Registry[str, dict[str, AbstractOAuth2Implementation]]
] = Registry()
