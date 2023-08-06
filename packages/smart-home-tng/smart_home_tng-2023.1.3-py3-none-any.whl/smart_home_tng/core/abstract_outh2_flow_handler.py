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
import asyncio
import logging
import time
import typing

import async_timeout
import voluptuous as vol
import yarl

from .abstract_oauth2_implementation import AbstractOAuth2Implementation
from .config_flow import ConfigFlow
from .flow_result import FlowResult
from .local_oauth2_implementation import LocalOAuth2Implementation
from .no_url_available_error import NoURLAvailableError

_LOGGER: typing.Final = logging.getLogger(__name__)


if not typing.TYPE_CHECKING:

    class SmartHomeController:
        ...


if typing.TYPE_CHECKING:
    from .smart_home_controller import SmartHomeController


# pylint: disable=unused-variable
class AbstractOAuth2FlowHandler(ConfigFlow, metaclass=abc.ABCMeta):
    """Handle a config flow."""

    # pylint: disable=invalid-name
    DOMAIN = ""

    def __init__(
        self,
        shc: SmartHomeController,
        handler: typing.Any = None,
        context: dict[str, typing.Any] = None,
        data: typing.Any = None,
        version: int = 1,
    ) -> None:
        """Instantiate config flow."""
        super().__init__(shc, handler, context, data, version)
        if self.DOMAIN == "":
            raise TypeError(
                f"Can't instantiate class {self.__class__.__name__} without DOMAIN being set"
            )
        self._external_data: typing.Any = None
        self._flow_impl: AbstractOAuth2Implementation = None

    @property
    def version(self) -> int:
        return 1

    @property
    def flow_impl(self) -> AbstractOAuth2Implementation:
        return self._flow_impl

    @property
    def external_data(self) -> typing.Any:
        return self._external_data

    @property
    @abc.abstractmethod
    def logger(self) -> logging.Logger:
        """Return logger."""

    @property
    def extra_authorize_data(self) -> dict:
        """Extra data that needs to be appended to the authorize url."""
        return {}

    async def async_step_pick_implementation(
        self, user_input: dict = None
    ) -> FlowResult:
        """Handle a flow start."""
        implementations = await AbstractOAuth2Implementation.async_get_implementations(
            self.DOMAIN
        )

        if user_input is not None:
            self._flow_impl = implementations[user_input["implementation"]]
            return await self.async_step_auth()

        if not implementations:
            if self.DOMAIN in await self._shc.setup.async_get_application_credentials():
                return self.async_abort(reason="missing_credentials")
            return self.async_abort(reason="missing_configuration")

        req = self._shc.http.current_request.get()
        if len(implementations) == 1 and req is not None:
            # Pick first implementation if we have only one, but only
            # if this is triggered by a user interaction (request).
            self._flow_impl = list(implementations.values())[0]
            return await self.async_step_auth()

        return self.async_show_form(
            step_id="pick_implementation",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        "implementation", default=list(implementations)[0]
                    ): vol.In({key: impl.name for key, impl in implementations.items()})
                }
            ),
        )

    async def async_step_auth(
        self, user_input: dict[str, typing.Any] = None
    ) -> FlowResult:
        """Create an entry for auth."""
        # Flow has been triggered by external data
        if user_input is not None:
            self._external_data = user_input
            next_step = "authorize_rejected" if "error" in user_input else "creation"
            return self.async_external_step_done(next_step_id=next_step)

        try:
            async with async_timeout.timeout(10):
                url = await self.flow_impl.async_generate_authorize_url(self.flow_id)
        except asyncio.TimeoutError:
            return self.async_abort(reason="authorize_url_timeout")
        except NoURLAvailableError:
            return self.async_abort(
                reason="no_url_available",
                description_placeholders={
                    "docs_url": "https://www.home-assistant.io/more-info/no-url-available"
                },
            )

        url = str(yarl.URL(url).update_query(self.extra_authorize_data))

        return self.async_external_step(step_id="auth", url=url)

    async def async_step_creation(
        self, _user_input: dict[str, typing.Any] = None
    ) -> FlowResult:
        """Create config entry from external data."""
        token = await self.flow_impl.async_resolve_external_data(self.external_data)
        # Force int for non-compliant oauth2 providers
        try:
            token["expires_in"] = int(token["expires_in"])
        except ValueError as err:
            _LOGGER.warning(f"Error converting expires_in to int: {err}")
            return self.async_abort(reason="oauth_error")
        token["expires_at"] = time.time() + token["expires_in"]

        self.logger.info("Successfully authenticated")

        return await self.async_oauth_create_entry(
            {"auth_implementation": self.flow_impl.domain, "token": token}
        )

    async def async_step_authorize_rejected(self, _data: None = None) -> FlowResult:
        """Step to handle flow rejection."""
        return self.async_abort(
            reason="user_rejected_authorize",
            description_placeholders={"error": self.external_data["error"]},
        )

    async def async_oauth_create_entry(self, data: dict) -> FlowResult:
        """Create an entry for the flow.

        Ok to override if you want to fetch extra info or even add another step.
        """
        return self.async_create_entry(title=self.flow_impl.name, data=data)

    async def async_step_user(
        self, user_input: dict[str, typing.Any] = None
    ) -> FlowResult:
        """Handle a flow start."""
        return await self.async_step_pick_implementation(user_input)

    @classmethod
    def async_register_implementation(
        cls, local_impl: LocalOAuth2Implementation
    ) -> None:
        """Register a local implementation."""
        AbstractOAuth2Implementation.async_register_implementation(
            cls.DOMAIN, local_impl
        )
