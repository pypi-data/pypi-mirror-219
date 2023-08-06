"""
Multi Factor Authentication Layer for Smart Home - The Next Generation.

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
import voluptuous as vol

from ... import core
from .multi_factor_auth_module import MultiFactorAuthModule, _MULTI_FACTOR_AUTH_MODULES
from .setup_flow import SetupFlow


_DEFAULT_TITLE = "Insecure Personal Identify Number"


# pylint: disable=unused-variable
@_MULTI_FACTOR_AUTH_MODULES.register("insecure_example")
class InsecureExampleModule(MultiFactorAuthModule):
    """Example auth module validate pin."""

    def __init__(
        self, shc: core.SmartHomeController, config: dict[str, typing.Any]
    ) -> None:
        """Initialize the user data store."""
        super().__init__(shc, config)
        self._data = config["data"]

    @property
    def default_title(self) -> str:
        return _DEFAULT_TITLE

    @property
    def input_schema(self) -> vol.Schema:
        """Validate login flow input data."""
        return vol.Schema({vol.Required("pin"): str})

    @property
    def setup_schema(self) -> vol.Schema:
        """Validate async_setup_user input data."""
        return vol.Schema({vol.Required("pin"): str})

    async def async_setup_flow(self, user_id: str) -> SetupFlow:
        """Return a data entry flow handler for setup module.

        Mfa module should extend SetupFlow
        """
        return SetupFlow(self, self.setup_schema, user_id)

    async def async_setup_user(
        self, user_id: str, setup_data: typing.Any
    ) -> typing.Any:
        """Set up user to use mfa module."""
        # data shall has been validate in caller
        pin = setup_data["pin"]

        for data in self._data:
            if data["user_id"] == user_id:
                # already setup, override
                data["pin"] = pin
                return

        self._data.append({"user_id": user_id, "pin": pin})

    async def async_depose_user(self, user_id: str) -> None:
        """Remove user from mfa module."""
        found = None
        for data in self._data:
            if data["user_id"] == user_id:
                found = data
                break
        if found:
            self._data.remove(found)

    async def async_is_user_setup(self, user_id: str) -> bool:
        """Return whether user is setup."""
        return any(data["user_id"] == user_id for data in self._data)

    async def async_validate(
        self, user_id: str, user_input: dict[str, typing.Any]
    ) -> bool:
        """Return True if validation passed."""
        return any(
            data["user_id"] == user_id and data["pin"] == user_input["pin"]
            for data in self._data
        )


# pylint: disable=unused-variable
CONFIG_SCHEMA = MultiFactorAuthModule.MODULE_SCHEMA.extend(
    {
        vol.Required("data"): [
            vol.Schema({vol.Required("user_id"): str, vol.Required("pin"): str})
        ]
    },
    extra=vol.PREVENT_EXTRA,
)
