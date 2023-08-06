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
import collections
import logging
import typing

import attr
import pyotp
import voluptuous as vol

from ... import core
from .multi_factor_auth_module import MultiFactorAuthModule, _MULTI_FACTOR_AUTH_MODULES
from .setup_flow import SetupFlow

_cv: typing.TypeAlias = core.ConfigValidation

# pylint: disable=unused-variable
REQUIREMENTS: typing.Final = ["pyotp>=2.8.0, < 2.9"]

_CONF_MESSAGE: typing.Final = "message"

_STORAGE_VERSION: typing.Final = 1
_STORAGE_KEY: typing.Final = "auth_module.notify"
_STORAGE_USERS: typing.Final = "users"

_INPUT_FIELD_CODE: typing.Final = "code"

_LOGGER: typing.Final = logging.getLogger(__name__)


def _generate_secret() -> str:
    """Generate a secret."""
    return str(pyotp.random_base32())


def _generate_random() -> int:
    """Generate a 32 digit number."""
    return int(pyotp.random_base32(length=32, chars=list("1234567890")))


def _generate_otp(secret: str, count: int) -> str:
    """Generate one time password."""
    return str(pyotp.HOTP(secret).at(count))


def _verify_otp(secret: str, otp: str, count: int) -> bool:
    """Verify one time password."""
    return bool(pyotp.HOTP(secret).verify(otp, count))


@attr.s(slots=True)
class _NotifySetting:
    """Store notify setting for one user."""

    secret: str = attr.ib(factory=_generate_secret)  # not persistent
    counter: int = attr.ib(factory=_generate_random)  # not persistent
    notify_service: str = attr.ib(default=None)
    target: str = attr.ib(default=None)


_UsersDict = dict[str, _NotifySetting]


_DEFAULT_TITLE = "Notify One-Time Password"


@_MULTI_FACTOR_AUTH_MODULES.register("notify")
class NotifyAuthModule(MultiFactorAuthModule):
    """Auth module send hmac-based one time password by notify service."""

    def __init__(
        self, shc: core.SmartHomeController, config: dict[str, typing.Any]
    ) -> None:
        """Initialize the user data store."""
        super().__init__(shc, config)
        self._user_settings: _UsersDict = None
        self._user_store = core.Store[dict[str, dict[str, typing.Any]]](
            shc, _STORAGE_VERSION, _STORAGE_KEY, private=True, atomic_writes=True
        )
        self._include = config.get(core.Const.CONF_INCLUDE, [])
        self._exclude = config.get(core.Const.CONF_EXCLUDE, [])
        self._message_template = config[_CONF_MESSAGE]
        self._init_lock = asyncio.Lock()

    @property
    def default_title(self) -> str:
        return _DEFAULT_TITLE

    @property
    def input_schema(self) -> vol.Schema:
        """Validate login flow input data."""
        return vol.Schema({vol.Required(_INPUT_FIELD_CODE): str})

    async def _async_load(self) -> None:
        """Load stored data."""
        async with self._init_lock:
            if self._user_settings is not None:
                return

            if (data := await self._user_store.async_load()) is None or not isinstance(
                data, dict
            ):
                data = {_STORAGE_USERS: {}}

            self._user_settings = {
                user_id: _NotifySetting(**setting)
                for user_id, setting in data.get(_STORAGE_USERS, {}).items()
            }

    async def _async_save(self) -> None:
        """Save data."""
        if self._user_settings is None:
            return

        await self._user_store.async_save(
            {
                _STORAGE_USERS: {
                    user_id: attr.asdict(
                        notify_setting,
                        filter=attr.filters.exclude(
                            attr.fields(_NotifySetting).secret,
                            attr.fields(_NotifySetting).counter,
                        ),
                    )
                    for user_id, notify_setting in self._user_settings.items()
                }
            }
        )

    @core.callback
    def aync_get_available_notify_services(self) -> list[str]:
        """Return list of notify services."""
        unordered_services = set()

        for service in self._shc.services.async_services().get("notify", {}):
            if service not in self._exclude:
                unordered_services.add(service)

        if self._include:
            unordered_services &= set(self._include)

        return sorted(unordered_services)

    async def async_setup_flow(self, user_id: str) -> SetupFlow:
        """Return a data entry flow handler for setup module.

        Mfa module should extend SetupFlow
        """
        return NotifySetupFlow(
            self, self.input_schema, user_id, self.aync_get_available_notify_services()
        )

    async def async_setup_user(
        self, user_id: str, setup_data: typing.Any
    ) -> typing.Any:
        """Set up auth module for user."""
        if self._user_settings is None:
            await self._async_load()
            assert self._user_settings is not None

        self._user_settings[user_id] = _NotifySetting(
            notify_service=setup_data.get("notify_service"),
            target=setup_data.get("target"),
        )

        await self._async_save()

    async def async_depose_user(self, user_id: str) -> None:
        """Depose auth module for user."""
        if self._user_settings is None:
            await self._async_load()
            assert self._user_settings is not None

        if self._user_settings.pop(user_id, None):
            await self._async_save()

    async def async_is_user_setup(self, user_id: str) -> bool:
        """Return whether user is setup."""
        if self._user_settings is None:
            await self._async_load()
            assert self._user_settings is not None

        return user_id in self._user_settings

    async def async_validate(
        self, user_id: str, user_input: dict[str, typing.Any]
    ) -> bool:
        """Return True if validation passed."""
        if self._user_settings is None:
            await self._async_load()
            assert self._user_settings is not None

        if (notify_setting := self._user_settings.get(user_id)) is None:
            return False

        # user_input has been validate in caller
        return await self._shc.async_add_executor_job(
            _verify_otp,
            notify_setting.secret,
            user_input.get(_INPUT_FIELD_CODE, ""),
            notify_setting.counter,
        )

    async def async_initialize_login_mfa_step(self, user_id: str) -> None:
        """Generate code and notify user."""
        if self._user_settings is None:
            await self._async_load()
            assert self._user_settings is not None

        if (notify_setting := self._user_settings.get(user_id)) is None:
            raise ValueError("Cannot find user_id")

        def generate_secret_and_one_time_password() -> str:
            """Generate and send one time password."""
            assert notify_setting
            # secret and counter are not persistent
            notify_setting.secret = _generate_secret()
            notify_setting.counter = _generate_random()
            return _generate_otp(notify_setting.secret, notify_setting.counter)

        code = await self._shc.async_add_executor_job(
            generate_secret_and_one_time_password
        )

        await self.async_notify_user(user_id, code)

    async def async_notify_user(self, user_id: str, code: str) -> None:
        """Send code by user's notify service."""
        if self._user_settings is None:
            await self._async_load()
            assert self._user_settings is not None

        if (notify_setting := self._user_settings.get(user_id)) is None:
            _LOGGER.error(f"Cannot find user {user_id}")
            return

        await self.async_notify(
            code,
            notify_setting.notify_service,
            notify_setting.target,
        )

    async def async_notify(
        self, code: str, notify_service: str, target: str = None
    ) -> None:
        """Send code by notify service."""
        data = {"message": self._message_template.format(code)}
        if target:
            data["target"] = [target]

        await self._shc.services.async_call("notify", notify_service, data)


class NotifySetupFlow(SetupFlow):
    """Handler for the setup flow."""

    def __init__(
        self,
        auth_module: NotifyAuthModule,
        setup_schema: vol.Schema,
        user_id: str,
        available_notify_services: list[str],
    ) -> None:
        """Initialize the setup flow."""
        super().__init__(auth_module, setup_schema, user_id)
        # to fix typing complaint
        self._auth_module: NotifyAuthModule = auth_module
        self._available_notify_services = available_notify_services
        self._secret: str = None
        self._count: int = None
        self._notify_service: str = None
        self._target: str = None

    async def async_step_init(
        self, user_input: dict[str, str] = None
    ) -> core.FlowResult:
        """Let user select available notify services."""
        errors: dict[str, str] = {}

        controller = self._auth_module.controller
        if user_input:
            self._notify_service = user_input["notify_service"]
            self._target = user_input.get("target")
            self._secret = await controller.async_add_executor_job(_generate_secret)
            self._count = await controller.async_add_executor_job(_generate_random)

            return await self.async_step_setup()

        if not self._available_notify_services:
            return self.async_abort(reason="no_available_service")

        schema: dict[str, typing.Any] = collections.OrderedDict()
        schema["notify_service"] = vol.In(self._available_notify_services)
        schema["target"] = vol.Optional(str)

        return self.async_show_form(
            step_id="init", data_schema=vol.Schema(schema), errors=errors
        )

    async def async_step_setup(
        self, user_input: dict[str, str] = None
    ) -> core.FlowResult:
        """Verify user can receive one-time password."""
        errors: dict[str, str] = {}

        controller = self._auth_module.controller
        if user_input:
            verified = await controller.async_add_executor_job(
                _verify_otp, self._secret, user_input["code"], self._count
            )
            if verified:
                await self._auth_module.async_setup_user(
                    self._user_id,
                    {"notify_service": self._notify_service, "target": self._target},
                )
                return self.async_create_entry(title=self._auth_module.name, data={})

            errors["base"] = "invalid_code"

        # generate code every time, no retry logic
        assert self._secret and self._count
        code = await controller.async_add_executor_job(
            _generate_otp, self._secret, self._count
        )

        assert self._notify_service
        try:
            await self._auth_module.async_notify(
                code, self._notify_service, self._target
            )
        except core.ServiceNotFound:
            return self.async_abort(reason="notify_service_not_exist")

        return self.async_show_form(
            step_id="setup",
            data_schema=self._setup_schema,
            description_placeholders={"notify_service": self._notify_service},
            errors=errors,
        )


# pylint: disable=unused-variable
CONFIG_SCHEMA = MultiFactorAuthModule.MODULE_SCHEMA.extend(
    {
        vol.Optional(core.Const.CONF_INCLUDE): vol.All(_cv.ensure_list, [_cv.string]),
        vol.Optional(core.Const.CONF_EXCLUDE): vol.All(_cv.ensure_list, [_cv.string]),
        vol.Optional(
            _CONF_MESSAGE,
            default="{} is your Smart Home - The Next Generation login code",
        ): str,
    },
    extra=vol.PREVENT_EXTRA,
)
