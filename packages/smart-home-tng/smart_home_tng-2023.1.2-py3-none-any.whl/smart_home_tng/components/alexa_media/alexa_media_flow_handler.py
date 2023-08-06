"""
Amazon Alexa MediaPlayer Integration for Smart Home - The Next Generation.

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

This integration is based custom_component "alexa_media_player"
from the Home Assistant Community Store (HACS), which is distributed
under the Terms of the Apache License, Version 2.0

The original source code and license terms can be found under:
https://github.com/custom_components/alexa_media_player
"""

import asyncio
import datetime as dt
import functools as ft
import logging
import typing

import aiohttp
import alexapy
import voluptuous as vol
import yarl

from ... import core
from .alexa_media_authorization_callback_view import AlexaMediaAuthorizationCallbackView
from .alexa_media_authorization_proxy_view import AlexaMediaAuthorizationProxyView
from .const import Const
from .helpers import _calculate_uuid

_const: typing.TypeAlias = core.Const

if not typing.TYPE_CHECKING:

    class AlexaMediaIntegration:
        pass


if typing.TYPE_CHECKING:
    from .alexa_media_integration import AlexaMediaIntegration

_LOGGER: typing.Final = logging.getLogger(__name__)
_DATA_SCHEMA: typing.Final = typing.OrderedDict(
    [
        (vol.Required(_const.CONF_EMAIL), str),
        (vol.Required(_const.CONF_PASSWORD), str),
        (vol.Required(_const.CONF_URL, default="amazon.com"), str),
        (vol.Optional(Const.CONF_SECURITYCODE), str),
        (vol.Optional(Const.CONF_OTPSECRET), str),
        (vol.Optional(Const.CONF_DEBUG, default=False), bool),
        (vol.Optional(Const.CONF_INCLUDE_DEVICES, default=""), str),
        (vol.Optional(Const.CONF_EXCLUDE_DEVICES, default=""), str),
        (vol.Optional(_const.CONF_SCAN_INTERVAL, default=60), int),
    ]
)
_TOTP_REGISTER_SCHEMA: typing.Final = typing.OrderedDict(
    [(vol.Optional(Const.CONF_TOTP_REGISTER, default=False), bool)]
)
_PROXY_WARNING_SCHEMA: typing.Final = typing.OrderedDict(
    [(vol.Optional(Const.CONF_PROXY_WARNING, default=False), bool)]
)


# pylint: disable=unused-variable
class AlexaMediaFlowHandler(core.ConfigFlow):
    """Handle a Alexa Media config flow."""

    def _update_ord_dict(
        self, old_dict: typing.OrderedDict, new_dict: dict
    ) -> typing.OrderedDict:
        result = typing.OrderedDict()
        for k, v in old_dict.items():
            for key, value in new_dict.items():
                if k == key:
                    result.update([(key, value)])
                    break
            if k not in result:
                result.update([(k, v)])
        return result

    def __init__(
        self,
        owner: AlexaMediaIntegration,
        context: dict[str, typing.Any] = None,
        data: typing.Any = None,
    ):
        """Initialize the config flow."""
        handler = owner.domain
        version = 1
        shc = owner.controller
        super().__init__(shc, handler, context, data, version)
        self._owner = owner
        self._login: alexapy.AlexaLogin = None
        self._securitycode: str = None
        self._automatic_steps: int = 0
        self._config = typing.OrderedDict()
        self._proxy_schema: typing.OrderedDict = None
        self._proxy: alexapy.AlexaProxy = None
        self._proxy_view: AlexaMediaAuthorizationProxyView = None
        self._data_schema = _DATA_SCHEMA

    async def async_step_import(self, import_config: core.ConfigType):
        """Import a config entry from configuration.yaml."""
        return await self.async_step_user_legacy(import_config)

    async def async_step_user(self, user_input=None):
        """Provide a proxy for login."""
        self._save_user_input_to_config(user_input=user_input)
        try:
            url = self.controller.get_url(prefer_external=True)
        except core.NoURLAvailableError:
            url = ""
        if self._proxy_schema is None:
            self._proxy_schema = typing.OrderedDict(
                [
                    (
                        vol.Required(
                            _const.CONF_EMAIL,
                            default=self._config.get(_const.CONF_EMAIL, ""),
                        ),
                        str,
                    ),
                    (
                        vol.Required(
                            _const.CONF_PASSWORD,
                            default=self._config.get(_const.CONF_PASSWORD, ""),
                        ),
                        str,
                    ),
                    (
                        vol.Required(
                            _const.CONF_URL,
                            default=self._config.get(_const.CONF_URL, "amazon.com"),
                        ),
                        str,
                    ),
                    (
                        vol.Required(
                            Const.CONF_CONTROLLER_URL,
                            default=self._config.get(Const.CONF_CONTROLLER_URL, url),
                        ),
                        str,
                    ),
                    (
                        vol.Optional(
                            Const.CONF_OTPSECRET,
                            default=self._config.get(Const.CONF_OTPSECRET, ""),
                        ),
                        str,
                    ),
                    (
                        vol.Optional(
                            Const.CONF_DEBUG,
                            default=self._config.get(Const.CONF_DEBUG, False),
                        ),
                        bool,
                    ),
                    (
                        vol.Optional(
                            Const.CONF_INCLUDE_DEVICES,
                            default=self._config.get(Const.CONF_INCLUDE_DEVICES, ""),
                        ),
                        str,
                    ),
                    (
                        vol.Optional(
                            Const.CONF_EXCLUDE_DEVICES,
                            default=self._config.get(Const.CONF_EXCLUDE_DEVICES, ""),
                        ),
                        str,
                    ),
                    (
                        vol.Optional(
                            _const.CONF_SCAN_INTERVAL,
                            default=self._config.get(_const.CONF_SCAN_INTERVAL, 60),
                        ),
                        int,
                    ),
                ]
            )

        if not user_input:
            return self.async_show_form(
                step_id="user",
                data_schema=vol.Schema(self._proxy_schema),
                description_placeholders={"message": ""},
            )
        if self._login is None:
            self._login = self._owner.get_account_login(self._config[_const.CONF_EMAIL])
        try:
            if not self._login or self._login.session.closed:
                _LOGGER.debug("Creating new login")
                uuid, index = await _calculate_uuid(
                    component=self._owner,
                    email=self._config.get(_const.CONF_EMAIL),
                    url=self._config[_const.CONF_URL],
                )
                self._login = alexapy.AlexaLogin(
                    url=self._config[_const.CONF_URL],
                    email=self._config.get(_const.CONF_EMAIL, ""),
                    password=self._config.get(_const.CONF_PASSWORD, ""),
                    outputpath=self.controller.config.path,
                    debug=self._config[Const.CONF_DEBUG],
                    otp_secret=self._config.get(Const.CONF_OTPSECRET, ""),
                    oauth=self._config.get(Const.CONF_OAUTH, {}),
                    uuid=uuid,
                    oauth_login=True,
                )
            else:
                _LOGGER.debug("Using existing login")
                if email := self._config.get(_const.CONF_EMAIL):
                    self._login.email = email
                if password := self._config.get(_const.CONF_PASSWORD):
                    self._login.password = password
                if otp_secret := self._config.get(Const.CONF_OTPSECRET):
                    self._login.set_totp(otp_secret)

        except alexapy.AlexapyPyotpInvalidKey:
            return self.async_show_form(
                step_id="user",
                errors={"base": "2fa_key_invalid"},
                description_placeholders={"message": ""},
            )
        url: str = user_input.get(Const.CONF_CONTROLLER_URL)
        if url is None:
            try:
                url = self.controller.get_url(prefer_external=True)
            except core.NoURLAvailableError:
                _LOGGER.debug(
                    "No Home Assistant URL found in config or detected; forcing user form"
                )
                return self.async_show_form(
                    step_id="user",
                    data_schema=vol.Schema(self._proxy_schema),
                    description_placeholders={"message": ""},
                )
        url_valid: bool = False
        url_error: str = ""
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url) as resp:
                    url_valid = resp.status == 200
            except aiohttp.ClientConnectionError as err:
                url_valid = False
                url_error = str(err)
            except aiohttp.InvalidURL as err:
                url_valid = False
                url_error = str(err.__cause__)
        if not url_valid:
            _LOGGER.debug(f"Unable to connect to provided Home Assistant url: {url}")
            return self.async_show_form(
                step_id="proxy_warning",
                data_schema=vol.Schema(_PROXY_WARNING_SCHEMA),
                errors={},
                description_placeholders={
                    "email": self._login.email,
                    "hass_url": url,
                    "error": url_error,
                },
            )
        if (
            user_input
            and user_input.get(Const.CONF_OTPSECRET)
            and user_input.get(Const.CONF_OTPSECRET).replace(" ", "")
        ):
            otp: str = self._login.get_totp_token()
            if otp:
                _LOGGER.debug(f"Generating OTP from {otp}")
                return self.async_show_form(
                    step_id="totp_register",
                    data_schema=vol.Schema(_TOTP_REGISTER_SCHEMA),
                    errors={},
                    description_placeholders={
                        "email": self._login.email,
                        "url": self._login.url,
                        "message": otp,
                    },
                )
        return await self.async_step_start_proxy(user_input)

    async def async_step_start_proxy(self, user_input=None):
        # pylint: disable=unused-argument
        """Start proxy for login."""
        _LOGGER.debug(
            f"Starting proxy for {alexapy.hide_email(self._login.email)} - {self._login.url}",
        )
        if not self._proxy:
            try:
                self._proxy = alexapy.AlexaProxy(
                    self._login,
                    str(
                        yarl.URL(self._config.get(Const.CONF_CONTROLLER_URL)).with_path(
                            Const.AUTH_PROXY_PATH
                        )
                    ),
                )
            except ValueError as ex:
                return self.async_show_form(
                    step_id="user",
                    errors={"base": "invalid_url"},
                    description_placeholders={"message": str(ex)},
                )
        # Swap the login object
        self._proxy.change_login(self._login)
        if not self._proxy_view:
            self._proxy_view = AlexaMediaAuthorizationProxyView(self._proxy.all_handler)
        else:
            _LOGGER.debug("Found existing proxy_view")
            self._proxy_view.handler = self._proxy.all_handler
        self.controller.register_view(AlexaMediaAuthorizationCallbackView())
        self.controller.register_view(self._proxy_view)
        callback_url = (
            yarl.URL(self._config[Const.CONF_CONTROLLER_URL])
            .with_path(Const.AUTH_CALLBACK_PATH)
            .with_query({"flow_id": self.flow_id})
        )

        proxy_url = self._proxy.access_url().with_query(
            {"config_flow_id": self.flow_id, "callback_url": str(callback_url)}
        )
        self._login.session.cookie_jar.clear()
        return self.async_external_step(step_id="check_proxy", url=str(proxy_url))

    async def async_step_check_proxy(self, user_input=None):
        # pylint: disable=unused-argument
        """Check status of proxy for login."""
        _LOGGER.debug(
            f"Checking proxy response for {alexapy.hide_email(self._login.email)} - "
            + f"{self._login.url}",
        )
        self._proxy_view.reset()
        return self.async_external_step_done(next_step_id="finish_proxy")

    async def async_step_finish_proxy(self, user_input=None):
        # pylint: disable=unused-argument
        """Finish auth."""
        if await self._login.test_loggedin():
            await self._login.finalize_login()
            self._config[_const.CONF_EMAIL] = self._login.email
            self._config[_const.CONF_PASSWORD] = self._login.password
            return await self._test_login()
        return self.async_abort(reason="login_failed")

    async def async_step_user_legacy(self, user_input=None):
        """Handle legacy input for the config flow."""
        # pylint: disable=too-many-return-statements
        self._save_user_input_to_config(user_input=user_input)
        self._data_schema = self._update_schema_defaults()
        if not user_input:
            self._automatic_steps = 0
            return self.async_show_form(
                step_id="user",
                data_schema=vol.Schema(self._data_schema),
                description_placeholders={"message": ""},
            )
        email = self._config[_const.CONF_EMAIL]
        url = self._config[_const.CONF_URL]
        title = f"{email} - {url}"
        if (
            not self._config.get("reauth")
            and title in _configured_instances(self._owner)
            and not self._owner.get_config_flow(email=email, url=url)
        ):
            _LOGGER.debug("Existing account found")
            self._automatic_steps = 0
            return self.async_show_form(
                step_id="user",
                data_schema=vol.Schema(self._data_schema),
                errors={_const.CONF_EMAIL: "identifier_exists"},
                description_placeholders={"message": ""},
            )
        if self._login is None:
            try:
                self._login = self._owner.get_account_login(
                    self._config[_const.CONF_EMAIL]
                )
            except KeyError:
                self._login = None
        try:
            if not self._login or self._login.session.closed:
                email = self._config[_const.CONF_EMAIL]
                url = self._config[_const.CONF_URL]
                _LOGGER.debug("Creating new login")
                uuid, index = await _calculate_uuid(
                    component=self._owner, email=email, url=url
                )
                self._login = alexapy.AlexaLogin(
                    url=url,
                    email=email,
                    password=self._config[_const.CONF_PASSWORD],
                    outputpath=self.controller.config.path,
                    debug=self._config[Const.CONF_DEBUG],
                    otp_secret=self._config.get(Const.CONF_OTPSECRET, ""),
                    uuid=uuid,
                    oauth_login=True,
                )
            else:
                _LOGGER.debug("Using existing login")
            if (
                not self._config.get("reauth")
                and user_input
                and user_input.get(Const.CONF_OTPSECRET)
                and user_input.get(Const.CONF_OTPSECRET).replace(" ", "")
            ):
                otp: str = self._login.get_totp_token()
                if otp:
                    _LOGGER.debug(f"Generating OTP from {otp}")
                    return self.async_show_form(
                        step_id="totp_register",
                        data_schema=vol.Schema(_TOTP_REGISTER_SCHEMA),
                        errors={},
                        description_placeholders={
                            "email": self._login.email,
                            "url": self._login.url,
                            "message": otp,
                        },
                    )
                return self.async_show_form(
                    step_id="user",
                    errors={"base": "2fa_key_invalid"},
                    description_placeholders={"message": ""},
                )
            if self._login.status:
                _LOGGER.debug("Resuming existing flow")
                return await self._test_login()
            _LOGGER.debug(f"Trying to login {self._login.status}")
            await self._login.login(
                data=self._config,
            )
            return await self._test_login()
        except alexapy.AlexapyConnectionError:
            self._automatic_steps = 0
            return self.async_show_form(
                step_id="user_legacy",
                errors={"base": "connection_error"},
                description_placeholders={"message": ""},
            )
        except alexapy.AlexapyPyotpInvalidKey:
            self._automatic_steps = 0
            return self.async_show_form(
                step_id="user_legacy",
                errors={"base": "2fa_key_invalid"},
                description_placeholders={"message": ""},
            )
        except BaseException as ex:  # pylint: disable=broad-except
            _LOGGER.warning(f"Unknown error: {ex}")
            if self._config[Const.CONF_DEBUG]:
                raise
            self._automatic_steps = 0
            return self.async_show_form(
                step_id="user_legacy",
                errors={"base": "unknown_error"},
                description_placeholders={"message": str(ex)},
            )

    async def async_step_proxy_warning(self, user_input=None):
        """Handle the proxy_warning for the config flow."""
        self._save_user_input_to_config(user_input=user_input)
        if user_input and user_input.get(Const.CONF_PROXY_WARNING) is False:
            _LOGGER.debug("User is not accepting warning, go back")
            return self.async_show_form(
                step_id="user",
                data_schema=vol.Schema(self._proxy_schema),
                description_placeholders={"message": ""},
            )
        _LOGGER.debug("User is ignoring proxy warning; starting proxy anyway")
        return await self.async_step_start_proxy(user_input)

    async def async_step_totp_register(self, user_input=None):
        """Handle the input processing of the config flow."""
        self._save_user_input_to_config(user_input=user_input)
        if user_input and user_input.get(Const.CONF_TOTP_REGISTER) is False:
            _LOGGER.debug("Not registered, regenerating")
            otp: str = self._login.get_totp_token()
            if otp:
                _LOGGER.debug(f"Generating OTP from {otp}")
                return self.async_show_form(
                    step_id="totp_register",
                    data_schema=vol.Schema(_TOTP_REGISTER_SCHEMA),
                    errors={},
                    description_placeholders={
                        "email": self._login.email,
                        "url": self._login.url,
                        "message": otp,
                    },
                )
        return await self.async_step_start_proxy(user_input)

    async def async_step_process(self, step_id, user_input=None):
        """Handle the input processing of the config flow."""
        _LOGGER.debug(
            f"Processing input for {step_id}: {alexapy.obfuscate(user_input)}",
        )
        self._save_user_input_to_config(user_input=user_input)
        if user_input:
            return await self.async_step_user(user_input=None)
        return await self._test_login()

    async def async_step_reauth(self, user_input=None):
        """Handle reauth processing for the config flow."""
        self._save_user_input_to_config(user_input)
        self._config["reauth"] = True
        reauth_schema = self._update_schema_defaults()
        _LOGGER.debug(
            f"Creating reauth form with {alexapy.obfuscate(self._config)}",
        )
        self._automatic_steps = 0
        if self._login is None:
            try:
                self._login = self._owner.get_account_login(
                    self._config[_const.CONF_EMAIL]
                )
            except KeyError:
                self._login = None
        seconds_since_login: int = (
            (dt.datetime.now() - self._login.stats["login_timestamp"]).seconds
            if self._login
            else 60
        )
        if seconds_since_login < 60:
            _LOGGER.debug(
                f"Relogin requested within {seconds_since_login} seconds; manual login required",
            )
            return self.async_show_form(
                step_id="user",
                data_schema=vol.Schema(reauth_schema),
                description_placeholders={"message": "REAUTH"},
            )
        _LOGGER.debug("Attempting automatic relogin")
        await asyncio.sleep(15)
        return await self.async_step_user_legacy(self._config)

    async def _test_login(self):
        # pylint: disable=too-many-statements, too-many-return-statements
        login = self._login
        email = login.email
        persistent_notification: core.PersistentNotificationComponent = (
            self.controller.components.persistent_notification
        )
        _LOGGER.debug(f"Testing login status: {login.status}")
        if login.status and login.status.get("login_successful"):
            existing_entry = await self.async_set_unique_id(f"{email} - {login.url}")
            self._config.pop("reauth", None)
            self._config.pop(Const.CONF_SECURITYCODE, None)
            self._config.pop(Const.CONF_CONTROLLER_URL, None)
            self._config[Const.CONF_OAUTH] = {
                "access_token": login.access_token,
                "refresh_token": login.refresh_token,
                "expires_in": login.expires_in,
                "mac_dms": login.mac_dms,
            }
            if existing_entry:
                self.controller.config_entries.async_update_entry(
                    existing_entry, data=self._config
                )
                _LOGGER.debug(f"Reauth successful for {alexapy.hide_email(email)}")
                self.controller.bus.async_fire(
                    "alexa_media.relogin_success",
                    event_data={"email": alexapy.hide_email(email), "url": login.url},
                )
                if persistent_notification:
                    persistent_notification.async_dismiss(
                        f"alexa_media_{core.helpers.slugify(email)}"
                        + f"{core.helpers.slugify(login.url[7:])}"
                    )
                await self._owner.async_successful_login(self._login, existing_entry)
                return self.async_abort(reason="reauth_successful")
            _LOGGER.debug(
                f"Setting up Alexa devices with {dict(alexapy.obfuscate(self._config))}",
            )
            self._abort_if_unique_id_configured(self._config)
            return self.async_create_entry(
                title=f"{login.email} - {login.url}", data=self._config
            )
        if login.status and login.status.get("securitycode_required"):
            _LOGGER.debug(
                f"Creating config_flow to request 2FA. Saved security code {self._securitycode}",
            )
            generated_securitycode: str = login.get_totp_token()
            if (
                self._securitycode or generated_securitycode
            ) and self._automatic_steps < 2:
                if self._securitycode:
                    _LOGGER.debug(
                        f"Automatically submitting securitycode {self._securitycode}"
                    )
                else:
                    _LOGGER.debug(
                        "Automatically submitting generated securitycode "
                        + f"{generated_securitycode}",
                    )
                self._automatic_steps += 1
                await asyncio.sleep(5)
                # pylint: disable=no-member
                if generated_securitycode:
                    return await self.async_step_twofactor(
                        user_input={Const.CONF_SECURITYCODE: generated_securitycode}
                    )
                return await self.async_step_twofactor(
                    user_input={Const.CONF_SECURITYCODE: self._securitycode}
                )
        if login.status and (login.status.get("login_failed")):
            _LOGGER.debug(f"Login failed: {login.status.get('login_failed')}")
            await login.close()
            if persistent_notification:
                persistent_notification.async_dismiss(
                    f"alexa_media_{core.helpers.slugify(email)}"
                    + f"{core.helpers.slugify(login.url[7:])}"
                )
            return self.async_abort(reason="login_failed")
        new_schema = self._update_schema_defaults()
        if login.status and login.status.get("error_message"):
            # pylint: disable=line-too-long
            _LOGGER.debug(f"Login error detected: {login.status.get('error_message')}")
            if (
                login.status.get("error_message")
                in {
                    "There was a problem\n            Enter a valid email or mobile number\n          "
                }
                and self._automatic_steps < 2
            ):
                _LOGGER.debug(
                    f"Trying automatic resubmission {self._automatic_steps} "
                    + "for error_message 'valid email'",
                )
                self._automatic_steps += 1
                await asyncio.sleep(5)
                return await self.async_step_user_legacy(user_input=self._config)
            _LOGGER.debug(
                "Done with automatic resubmission for error_message 'valid email'; "
                + "returning error message",
            )
        self._automatic_steps = 0
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(new_schema),
            description_placeholders={
                "message": f"  \n> {login.status.get('error_message','')}"
            },
        )

    def _save_user_input_to_config(self, user_input=None) -> None:
        """Process user_input to save to self.config.

        user_input can be a dictionary of strings or an internally
        saved config_entry data entry. This function will convert all to internal strings.

        """
        if user_input is None:
            return
        if Const.CONF_CONTROLLER_URL in user_input:
            self._config[Const.CONF_CONTROLLER_URL] = user_input[
                Const.CONF_CONTROLLER_URL
            ]
        self._securitycode = user_input.get(Const.CONF_SECURITYCODE)
        if self._securitycode is not None:
            self._config[Const.CONF_SECURITYCODE] = self._securitycode
        elif Const.CONF_SECURITYCODE in self._config:
            self._config.pop(Const.CONF_SECURITYCODE)
        if user_input.get(Const.CONF_OTPSECRET) and user_input.get(
            Const.CONF_OTPSECRET
        ).replace(" ", ""):
            self._config[Const.CONF_OTPSECRET] = user_input[
                Const.CONF_OTPSECRET
            ].replace(" ", "")
        elif user_input.get(Const.CONF_OTPSECRET):
            # a blank line
            self._config.pop(Const.CONF_OTPSECRET)
        if _const.CONF_EMAIL in user_input:
            self._config[_const.CONF_EMAIL] = user_input[_const.CONF_EMAIL]
        if _const.CONF_PASSWORD in user_input:
            self._config[_const.CONF_PASSWORD] = user_input[_const.CONF_PASSWORD]
        if _const.CONF_URL in user_input:
            self._config[_const.CONF_URL] = user_input[_const.CONF_URL]
        if Const.CONF_DEBUG in user_input:
            self._config[Const.CONF_DEBUG] = user_input[Const.CONF_DEBUG]
        if _const.CONF_SCAN_INTERVAL in user_input:
            scan_interval = user_input[_const.CONF_SCAN_INTERVAL]
            if isinstance(scan_interval, dt.timedelta):
                scan_interval = scan_interval.total_seconds()
            self._config[_const.CONF_SCAN_INTERVAL] = scan_interval
        if Const.CONF_INCLUDE_DEVICES in user_input:
            devices = user_input[Const.CONF_INCLUDE_DEVICES]
            if isinstance(devices, list):
                self._config[Const.CONF_INCLUDE_DEVICES] = (
                    ft.reduce(lambda x, y: f"{x},{y}", devices) if devices else ""
                )
            else:
                self._config[Const.CONF_INCLUDE_DEVICES] = devices
        if Const.CONF_EXCLUDE_DEVICES in user_input:
            devices = user_input[Const.CONF_EXCLUDE_DEVICES]
            if isinstance(devices, list):
                self._config[Const.CONF_EXCLUDE_DEVICES] = (
                    ft.reduce(lambda x, y: f"{x},{y}", devices) if devices else ""
                )
            else:
                self._config[Const.CONF_EXCLUDE_DEVICES] = devices

    def _update_schema_defaults(self) -> typing.OrderedDict:
        new_schema = self._update_ord_dict(
            self._data_schema,
            {
                vol.Required(
                    _const.CONF_EMAIL, default=self._config.get(_const.CONF_EMAIL, "")
                ): str,
                vol.Required(
                    _const.CONF_PASSWORD,
                    default=self._config.get(_const.CONF_PASSWORD, ""),
                ): str,
                vol.Optional(
                    Const.CONF_SECURITYCODE,
                    default=self._securitycode if self._securitycode else "",
                ): str,
                vol.Optional(
                    Const.CONF_OTPSECRET,
                    default=self._config.get(Const.CONF_OTPSECRET, ""),
                ): str,
                vol.Required(
                    _const.CONF_URL,
                    default=self._config.get(_const.CONF_URL, "amazon.com"),
                ): str,
                vol.Optional(
                    Const.CONF_DEBUG,
                    default=bool(self._config.get(Const.CONF_DEBUG, False)),
                ): bool,
                vol.Optional(
                    Const.CONF_INCLUDE_DEVICES,
                    default=self._config.get(Const.CONF_INCLUDE_DEVICES, ""),
                ): str,
                vol.Optional(
                    Const.CONF_EXCLUDE_DEVICES,
                    default=self._config.get(Const.CONF_EXCLUDE_DEVICES, ""),
                ): str,
                vol.Optional(
                    _const.CONF_SCAN_INTERVAL,
                    default=self._config.get(_const.CONF_SCAN_INTERVAL, 60),
                ): int,
            },
        )
        return new_schema


@core.callback
def _configured_instances(component: core.SmartHomeControllerComponent):
    """Return a set of configured Alexa Media instances."""
    return {
        entry.title
        for entry in component.controller.config_entries.async_entries(component.domain)
    }
