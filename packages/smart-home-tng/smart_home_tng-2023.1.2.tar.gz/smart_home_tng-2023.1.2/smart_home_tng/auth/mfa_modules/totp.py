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

import asyncio
import io
import typing

import pyotp
import pyqrcode
import voluptuous as vol

from ... import core
from ..user import User
from .multi_factor_auth_module import MultiFactorAuthModule, _MULTI_FACTOR_AUTH_MODULES
from .setup_flow import SetupFlow

# pylint: disable=unused-variable
REQUIREMENTS: typing.Final = ["pyotp>=2.8.0, < 2.9", "PyQRCode>=1.2.1, < 1.3"]

_STORAGE_VERSION: typing.Final = 1
_STORAGE_KEY: typing.Final = "auth_module.totp"
_STORAGE_USERS: typing.Final = "users"

_INPUT_FIELD_CODE: typing.Final = "code"

_DUMMY_SECRET: typing.Final = "FPPTH34D4E3MI2HG"


def _generate_qr_code(data: str) -> str:
    """Generate a base64 PNG string represent QR Code image of data."""
    qr_code = pyqrcode.create(data)

    with io.BytesIO() as buffer:
        qr_code.svg(file=buffer, scale=4)
        return str(
            buffer.getvalue()
            .decode("ascii")
            .replace("\n", "")
            .replace(
                '<?xml version="1.0" encoding="UTF-8"?>'
                + '<svg xmlns="http://www.w3.org/2000/svg"',
                "<svg",
            )
        )


def _generate_secret_and_qr_code(username: str) -> tuple[str, str, str]:
    """Generate a secret, url, and QR code."""
    ota_secret = pyotp.random_base32()
    url = pyotp.totp.TOTP(ota_secret).provisioning_uri(username, issuer_name="internal")
    image = _generate_qr_code(url)
    return ota_secret, url, image


_DEFAULT_TITLE: typing.Final = "Time-based One Time Password"
_MAX_RETRY_TIME: typing.Final = 5


@_MULTI_FACTOR_AUTH_MODULES.register("totp")
class TotpAuthModule(MultiFactorAuthModule):
    """Auth module validate time-based one time password."""

    def __init__(
        self, shc: core.SmartHomeController, config: dict[str, typing.Any]
    ) -> None:
        """Initialize the user data store."""
        super().__init__(shc, config)
        self._users: dict[str, str] = None
        self._user_store = core.Store[dict[str, dict[str, str]]](
            shc, _STORAGE_VERSION, _STORAGE_KEY, private=True, atomic_writes=True
        )
        self._init_lock = asyncio.Lock()

    @property
    def default_title(self) -> str:
        return _DEFAULT_TITLE

    @property
    def max_retry_time(self) -> int:
        return _MAX_RETRY_TIME

    @property
    def input_schema(self) -> vol.Schema:
        """Validate login flow input data."""
        return vol.Schema({vol.Required(_INPUT_FIELD_CODE): str})

    async def _async_load(self) -> None:
        """Load stored data."""
        async with self._init_lock:
            if self._users is not None:
                return

            if (data := await self._user_store.async_load()) is None or not isinstance(
                data, dict
            ):
                data = {_STORAGE_USERS: {}}

            self._users = data.get(_STORAGE_USERS, {})

    async def _async_save(self) -> None:
        """Save data."""
        await self._user_store.async_save({_STORAGE_USERS: self._users})

    def _add_ota_secret(self, user_id: str, secret: str = None) -> str:
        """Create a ota_secret for user."""
        ota_secret: str = secret or pyotp.random_base32()

        self._users[user_id] = ota_secret
        return ota_secret

    async def async_setup_flow(self, user_id: str) -> SetupFlow:
        """Return a data entry flow handler for setup module.

        Mfa module should extend SetupFlow
        """
        user = await self._shc.auth.async_get_user(user_id)
        assert user is not None
        return TotpSetupFlow(self, self.input_schema, user)

    async def async_setup_user(self, user_id: str, setup_data: typing.Any) -> str:
        """Set up auth module for user."""
        if self._users is None:
            await self._async_load()

        result = await self._shc.async_add_executor_job(
            self._add_ota_secret, user_id, setup_data.get("secret")
        )

        await self._async_save()
        return result

    async def async_depose_user(self, user_id: str) -> None:
        """Depose auth module for user."""
        if self._users is None:
            await self._async_load()

        if self._users.pop(user_id, None):
            await self._async_save()

    async def async_is_user_setup(self, user_id: str) -> bool:
        """Return whether user is setup."""
        if self._users is None:
            await self._async_load()

        return user_id in self._users

    async def async_validate(
        self, user_id: str, user_input: dict[str, typing.Any]
    ) -> bool:
        """Return True if validation passed."""
        if self._users is None:
            await self._async_load()

        # user_input has been validate in caller
        # set INPUT_FIELD_CODE as vol.Required is not user friendly
        return await self._shc.async_add_executor_job(
            self._validate_2fa, user_id, user_input.get(_INPUT_FIELD_CODE, "")
        )

    def _validate_2fa(self, user_id: str, code: str) -> bool:
        """Validate two factor authentication code."""
        if (ota_secret := self._users.get(user_id)) is None:  # type: ignore[union-attr]
            # even we cannot find user, we still do verify
            # to make timing the same as if user was found.
            pyotp.TOTP(_DUMMY_SECRET).verify(code, valid_window=1)
            return False

        return bool(pyotp.TOTP(ota_secret).verify(code, valid_window=1))


class TotpSetupFlow(SetupFlow):
    """Handler for the setup flow."""

    def __init__(
        self,
        auth_module: TotpAuthModule,
        setup_schema: vol.Schema,
        user: User,
        handler="totp",
    ) -> None:
        """Initialize the setup flow."""
        super().__init__(auth_module, setup_schema, user.id, handler=handler)
        # to fix typing complaint
        self._auth_module: TotpAuthModule = auth_module
        self._user = user
        self._ota_secret: str = ""
        self._url: str = None
        self._image: str = None

    async def async_step_init(
        self, user_input: dict[str, str] = None
    ) -> core.FlowResult:
        """Handle the first step of setup flow.

        Return self.async_show_form(step_id='init') if user_input is None.
        Return self.async_create_entry(data={'result': result}) if finish.
        """
        errors: dict[str, str] = {}

        shc = self._auth_module.controller
        if user_input:
            verified = await shc.async_add_executor_job(
                pyotp.TOTP(self._ota_secret).verify, user_input["code"]
            )
            if verified:
                result = await self._auth_module.async_setup_user(
                    self._user_id, {"secret": self._ota_secret}
                )
                return self.async_create_entry(
                    title=self._auth_module.name, data={"result": result}
                )
            errors["base"] = "invalid_code"
        else:
            (
                self._ota_secret,
                self._url,
                self._image,
            ) = await shc.async_add_executor_job(
                _generate_secret_and_qr_code,
                str(self._user.name),
            )

        return self.async_show_form(
            step_id="init",
            data_schema=self._setup_schema,
            description_placeholders={
                "code": self._ota_secret,
                "url": self._url,
                "qr_code": self._image,
            },
            errors=errors,
        )


# pylint: disable=unused-variable
CONFIG_SCHEMA = MultiFactorAuthModule.MODULE_SCHEMA.extend({}, extra=vol.PREVENT_EXTRA)
