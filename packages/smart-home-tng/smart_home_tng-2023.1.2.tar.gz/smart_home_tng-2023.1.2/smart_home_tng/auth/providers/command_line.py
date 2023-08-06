"""
Authentication Provider Layer for Smart Home - The Next Generation.

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
import collections.abc
import logging
import os
import typing

import voluptuous as vol

from ... import core
from ..credentials import Credentials
from ..invalid_auth_error import InvalidAuthError
from ..user_meta import UserMeta
from .auth_provider import AuthProvider, _AUTH_PROVIDERS
from .login_flow import LoginFlow

_CONF_ARGS: typing.Final = "args"
_CONF_META: typing.Final = "meta"

_LOGGER = logging.getLogger(__name__)

_DEFAULT_TITLE = "Command Line Authentication"


# pylint: disable=unused-variable
@_AUTH_PROVIDERS.register("command_line")
class CommandLineAuthProvider(AuthProvider):
    """Auth provider validating credentials by calling a command."""

    # which keys to accept from a program's stdout
    ALLOWED_META_KEYS: typing.Final = ("name",)

    def __init__(self, *args: typing.Any, **kwargs: typing.Any) -> None:
        """Extend parent's __init__.

        Adds self._user_meta dictionary to hold the user-specific
        attributes provided by external programs.
        """
        super().__init__(*args, **kwargs)
        self._user_meta: dict[str, dict[str, typing.Any]] = {}

    @property
    def default_title(self) -> str:
        return _DEFAULT_TITLE

    async def async_login_flow(self, _context: dict[str, typing.Any]) -> LoginFlow:
        """Return a flow to login."""
        return CommandLineLoginFlow(self)

    async def async_validate_login(self, username: str, password: str) -> None:
        """Validate a username and password."""
        env = {"username": username, "password": password}
        try:
            process = await asyncio.create_subprocess_exec(
                self._config[core.Const.CONF_COMMAND],
                *self._config[_CONF_ARGS],
                env=env,
                stdout=asyncio.subprocess.PIPE if self._config[_CONF_META] else None,
            )
            stdout, _ = await process.communicate()
        except OSError as err:
            # happens when command doesn't exist or permission is denied
            _LOGGER.error(f"Error while authenticating {username}: {err}")
            raise InvalidAuthError from err

        if process.returncode != 0:
            _LOGGER.error(
                f"User {username} failed to authenticate, "
                + f"command exited with code {process.returncode}"
            )
            raise InvalidAuthError

        if self._config[_CONF_META]:
            meta: dict[str, str] = {}
            for _line in stdout.splitlines():
                try:
                    line = _line.decode().lstrip()
                    if line.startswith("#"):
                        continue
                    key, value = line.split("=", 1)
                except ValueError:
                    # malformed line
                    continue
                key = key.strip()
                value = value.strip()
                if key in self.ALLOWED_META_KEYS:
                    meta[key] = value
            self._user_meta[username] = meta

    async def async_get_or_create_credentials(
        self, flow_result: collections.abc.Mapping[str, str]
    ) -> Credentials:
        """Get credentials based on the flow result."""
        username = flow_result["username"]
        for credential in await self.async_credentials():
            if credential.data["username"] == username:
                return credential

        # Create new credentials.
        return self.async_create_credentials({"username": username})

    async def async_user_meta_for_credentials(
        self, credentials: Credentials
    ) -> UserMeta:
        """Return extra user metadata for credentials.

        Currently, only name is supported.
        """
        meta = self._user_meta.get(credentials.data["username"], {})
        return UserMeta(name=meta.get("name"), is_active=True)


class CommandLineLoginFlow(LoginFlow):
    """Handler for the login flow."""

    async def async_step_init(
        self, user_input: dict[str, str] = None
    ) -> core.FlowResult:
        """Handle the step of the form."""
        errors = {}

        if user_input is not None:
            user_input["username"] = user_input["username"].strip()
            try:
                await typing.cast(
                    CommandLineAuthProvider, self._auth_provider
                ).async_validate_login(user_input["username"], user_input["password"])
            except InvalidAuthError:
                errors["base"] = "invalid_auth"

            if not errors:
                user_input.pop("password")
                return await self.async_finish(user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Required("username"): str,
                    vol.Required("password"): str,
                }
            ),
            errors=errors,
        )


# pylint: disable=unused-variable
CONFIG_SCHEMA: typing.Final = AuthProvider.AUTH_PROVIDER_SCHEMA.extend(
    {
        vol.Required(core.Const.CONF_COMMAND): vol.All(
            str, os.path.normpath, msg="must be an absolute path"
        ),
        vol.Optional(_CONF_ARGS, default=None): vol.Any(vol.DefaultTo(list), [str]),
        vol.Optional(_CONF_META, default=False): bool,
    },
    extra=vol.PREVENT_EXTRA,
)
