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
import logging
import typing

import alexapy
import voluptuous as vol

from ... import core
from .alexa_account_info import AlexaAccountInfo
from .alexa_media_flow_handler import AlexaMediaFlowHandler
from .alexa_notification_service import AlexaNotificationService
from .const import Const
from .helpers import _catch_login_errors, _report_relogin_required
from .options_flow_handler import OptionsFlowHandler

_cv: typing.TypeAlias = core.ConfigValidation
_const: typing.TypeAlias = core.Const
_platform: typing.TypeAlias = core.Platform

_LOGGER: typing.Final = logging.getLogger(__name__)
_ACCOUNT_CONFIG_SCHEMA = vol.Schema(
    {
        vol.Required(_const.CONF_EMAIL): _cv.string,
        vol.Required(_const.CONF_PASSWORD): _cv.string,
        vol.Required(_const.CONF_URL): _cv.string,
        vol.Optional(Const.CONF_DEBUG, default=False): _cv.boolean,
        vol.Optional(Const.CONF_INCLUDE_DEVICES, default=[]): vol.All(
            _cv.ensure_list, [_cv.string]
        ),
        vol.Optional(Const.CONF_EXCLUDE_DEVICES, default=[]): vol.All(
            _cv.ensure_list, [_cv.string]
        ),
        vol.Optional(
            _const.CONF_SCAN_INTERVAL, default=Const.SCAN_INTERVAL
        ): _cv.time_period,
    }
)
CLEAR_HISTORY_SCHEMA: typing.Final = vol.Schema(
    {
        vol.Optional(Const.ATTR_EMAIL, default=[]): vol.All(
            _cv.ensure_list, [_cv.string]
        ),
        vol.Optional(Const.ATTR_NUM_ENTRIES, default=50): vol.All(
            int, vol.Range(min=1, max=50)
        ),
    }
)
FORCE_LOGOUT_SCHEMA = vol.Schema(
    {vol.Optional(Const.ATTR_EMAIL, default=[]): vol.All(_cv.ensure_list, [_cv.string])}
)
LAST_CALL_UPDATE_SCHEMA = vol.Schema(
    {vol.Optional(Const.ATTR_EMAIL, default=[]): vol.All(_cv.ensure_list, [_cv.string])}
)


# pylint: disable=unused-variable
class AlexaMediaIntegration(
    core.SmartHomeControllerComponent, core.ConfigFlowPlatform, core.NotifyPlatform
):
    """
    Support to interface with Alexa Media Devices (Echo and FireTV).
    """

    def __init__(self, path: typing.Iterable[str]):
        super().__init__(path)
        self._accounts: dict[str, AlexaAccountInfo] = {}
        self._services_registered = False
        self._config_flows: dict[tuple[str, str], core.FlowResult] = {}
        self._notify_service: AlexaNotificationService = None
        self._supported_platforms = frozenset(
            [
                _platform.CONFIG_FLOW,
                _platform.MEDIA_PLAYER,
                _platform.NOTIFY,
                _platform.SWITCH,
            ]
        )

    def __getitem__(self, item: str) -> AlexaAccountInfo:
        return self._accounts[item]

    @property
    def config_schema(self) -> typing.Callable[[core.ConfigType], core.ConfigType]:
        return vol.Schema(
            {
                self.domain: vol.Schema(
                    {
                        vol.Optional(Const.CONF_ACCOUNTS): vol.All(
                            _cv.ensure_list, [_ACCOUNT_CONFIG_SCHEMA]
                        )
                    }
                )
            },
            extra=vol.ALLOW_EXTRA,
        )

    @property
    def notify_service(self):
        return self._notify_service

    def is_account_defined(self, account: str) -> bool:
        return account in self._accounts

    def get_account_login(self, account: str) -> alexapy.AlexaLogin:
        info = self._accounts.get(account, None)
        if info:
            return info.login
        return None

    def get_config_flow(self, email: str, url: str) -> core.FlowResult:
        return self._config_flows.get((email, url))

    def register_config_flow(
        self, email: str, url: str, flow: core.FlowResult = None
    ) -> None:
        if email and url:
            key = (email, url)
            if flow:
                self._config_flows[key] = flow
            else:
                self._config_flows.pop(key, None)

    async def async_successful_login(
        self, login: alexapy.AlexaLogin, config_entry: core.ConfigEntry
    ):
        """clean up after successful login"""
        if not login or not config_entry:
            return

        self._config_flows.pop((login.email, login.url))
        if login.email not in self._accounts:
            account_info = AlexaAccountInfo(self, config_entry, login)
            await account_info.async_init()
            self._accounts[login.email] = account_info

    async def async_setup_entry(self, entry: core.ConfigEntry) -> bool:
        """Set up Alexa Media Player as config entry."""

        async def close_alexa_media(event=None) -> None:
            """Clean up Alexa connections."""
            _LOGGER.debug(f"Received shutdown request: {event}")
            for _, info in self._accounts.items():
                await info.async_close_connection()

        async def complete_startup(_event=None) -> None:
            """Run final tasks after startup."""
            _LOGGER.debug("Completing remaining startup tasks.")
            await asyncio.sleep(10)

            if self._notify_service:
                await self._notify_service.async_register_services()

        async def relogin(event=None) -> None:
            """Relogin to Alexa."""
            check_mail = alexapy.hide_email(account_info.email)
            if check_mail == event.data.get("email"):
                _LOGGER.debug(f"{check_mail}: Received relogin request: {event}")
                await self._async_unregister_services(account_info.email)
                await account_info.async_relogin()

        async def login_success(event=None) -> None:
            """Relogin to Alexa."""
            check_mail = alexapy.hide_email(account_info.email)
            if check_mail == event.data.get("email"):
                await self._async_register_services()
                _LOGGER.debug(f"Received Login success: {event}")
                await account_info.async_setup_alexa()

        account_info = AlexaAccountInfo(self, entry)
        await account_info.async_init()
        self._accounts[account_info.email] = account_info
        if not account_info.second_account_index:
            self.controller.bus.async_listen_once(
                _const.EVENT_SHC_STOP, close_alexa_media
            )
            self.controller.bus.async_listen_once(
                _const.EVENT_SHC_STARTED, complete_startup
            )
        self.controller.bus.async_listen("alexa_media.relogin_required", relogin)
        self.controller.bus.async_listen("alexa_media.relogin_success", login_success)
        try:
            result = await account_info.async_login()
            if result:
                await self._async_register_services()
            return result
        except alexapy.AlexapyConnectionError as err:
            raise core.ConfigEntryNotReady(
                str(err) or "Connection Error during login"
            ) from err

    async def async_unload_entry(self, entry: core.ConfigEntry) -> bool:
        """Unload a config entry."""

        email = entry.data["email"]
        _LOGGER.debug(f"Attempting to unload entry for {alexapy.hide_email(email)}")
        for component in Const.ALEXA_COMPONENTS + Const.DEPENDENT_ALEXA_COMPONENTS:
            _LOGGER.debug(f"Forwarding unload entry to {component}")
            await self.controller.config_entries.async_forward_entry_unload(
                entry, component
            )
        # notify has to be handled manually as the forward does not work yet
        # await notify_async_unload_entry(hass, entry)
        account_info = self._accounts.pop(email, None)
        if account_info:
            await account_info.async_close_connection()
            account_info.remove_update_listener()
        # Clean up config flows in progress
        flows_to_remove = []
        for key, flow in self._config_flows.items():
            if key[0] == email and flow:
                _LOGGER.debug(f"Aborting flow {key} {flow}")
                flows_to_remove.append(key)
                try:
                    self.controller.config_entries.flow.async_abort(flow.get("flow_id"))
                except core.UnknownFlow:
                    pass
        for flow in flows_to_remove:
            self._config_flows.pop(flow)
        # Clean up services
        await self._async_unregister_services(email)
        persistent_notification: core.PersistentNotificationComponent = (
            self.controller.components.persistent_notification
        )
        if persistent_notification:
            persistent_notification.async_dismiss(
                f"alexa_media_{core.helpers.slugify(email)}"
                + f"{core.helpers.slugify((entry.data[_const.CONF_URL])[7:])}"
            )
        _LOGGER.debug(f"Unloaded entry for {alexapy.hide_email(email)}")
        return True

    async def _async_register_services(self):
        """Register services to hass."""
        if self._services_registered:
            return
        self._services_registered = True

        self.controller.services.async_register(
            self.domain,
            Const.SERVICE_UPDATE_LAST_CALLED,
            self._async_last_call_handler,
            schema=LAST_CALL_UPDATE_SCHEMA,
        )
        self.controller.services.async_register(
            self.domain,
            Const.SERVICE_CLEAR_HISTORY,
            self._async_clear_history,
            schema=CLEAR_HISTORY_SCHEMA,
        )
        self.controller.services.async_register(
            self.domain,
            Const.SERVICE_FORCE_LOGOUT,
            self._async_force_logout,
            schema=FORCE_LOGOUT_SCHEMA,
        )

    async def _async_unregister_services(self, email: str):
        """Unregister services, if last alexa account is closed"""
        if not self._services_registered:
            return

        others_found = False
        for account, info in self._accounts.items():
            if account == email:
                continue
            others_found = True
            break

        if not others_found:
            self._services_registered = False
            self.controller.services.async_remove(
                self.domain,
                Const.SERVICE_UPDATE_LAST_CALLED,
            )
            self.controller.services.async_remove(
                self.domain,
                Const.SERVICE_CLEAR_HISTORY,
            )
            self.controller.services.async_remove(
                self.domain, Const.SERVICE_FORCE_LOGOUT
            )

    @_catch_login_errors
    async def _async_clear_history(self, call: core.ServiceCall):
        """Handle clear history service request.

        Arguments
            call.ATTR_EMAIL {List[str: None]} -- Case-sensitive Alexa emails.
                                                    Default is all known emails.
            call.ATTR_NUM_ENTRIES {int: 50} -- Number of entries to delete.

        Returns
            bool -- True if deletion successful

        """
        _LOGGER.debug(f"call {call}")
        requested_emails = call.data.get(Const.ATTR_EMAIL)
        items: int = int(call.data.get(Const.ATTR_NUM_ENTRIES))

        _LOGGER.debug(
            f"Service clear_history called for: {items} items for {requested_emails}"
        )
        success = True
        for email, info in self._accounts.items():
            if requested_emails and email not in requested_emails:
                continue
            try:
                await alexapy.AlexaAPI.clear_history(info.login, items)
            except alexapy.AlexapyLoginError:
                _report_relogin_required(self.controller, info.login, email)
                success = False
            except alexapy.AlexapyConnectionError:
                _LOGGER.error(
                    f"Unable to connect to Alexa for {alexapy.hide_email(email)};"
                    + " check your network connection and try again",
                )
        return success

    @_catch_login_errors
    async def _async_force_logout(self, call: core.ServiceCall) -> bool:
        """Handle force logout service request.

        Arguments
            call.ATTR_EMAIL {List[str: None]} -- Case-sensitive Alexa emails.
                                                    Default is all known emails.

        Returns
            bool -- True if force logout successful

        """
        requested_emails = call.data.get(Const.ATTR_EMAIL)

        _LOGGER.debug(f"Service force_logout called for: {requested_emails}")
        success = False
        for email, info in self._accounts.items():
            if requested_emails and email not in requested_emails:
                continue
            try:
                await alexapy.AlexaAPI.force_logout()
            except alexapy.AlexapyLoginError:
                _report_relogin_required(self.controller, info.login, email)
                success = True
            except alexapy.AlexapyConnectionError:
                _LOGGER.error(
                    f"Unable to connect to Alexa for {alexapy.hide_email(email)};"
                    + " check your network connection and try again",
                )
        return success

    async def _async_last_call_handler(self, call: core.ServiceCall):
        """Handle last call service request.

        Args:
        call.ATTR_EMAIL: List of case-sensitive Alexa email addresses. If None
                            all accounts are updated.

        """
        requested_emails = call.data.get(Const.ATTR_EMAIL)
        _LOGGER.debug(f"Service update_last_called for: {requested_emails}")
        for email, info in self._accounts.items():
            if requested_emails and email not in requested_emails:
                continue
            try:
                await info.update_last_called()
            except alexapy.AlexapyLoginError:
                _report_relogin_required(self.controller, info.login, email)
            except alexapy.AlexapyConnectionError:
                _LOGGER.error(
                    f"Unable to connect to Alexa for {alexapy.hide_email(email)};"
                    + " check your network connection and try again",
                )

    # ------------------------ ConfigFlow Platform --------------------------------

    def create_config_flow(
        self, context: dict, init_data: typing.Any
    ) -> core.ConfigFlow:
        return AlexaMediaFlowHandler(self, context=context, data=init_data)

    async def async_get_options_flow(  # pylint: disable=unused-argument
        self, entry: core.ConfigEntry, context: dict, init_data: typing.Any
    ) -> core.OptionsFlow:
        return OptionsFlowHandler(entry)

    async def async_setup_platform(
        self,
        platform_config: core.ConfigType,
        add_entities: core.AddEntitiesCallback,
        discovery_info: core.DiscoveryInfoType,
    ):
        platform = core.EntityPlatform.async_get_current_platform().domain
        account = (
            platform_config[_const.CONF_EMAIL]
            if platform_config
            else discovery_info["config"].get(_const.CONF_EMAIL, None)
        )
        info = self._accounts.get(account, None)
        result = False
        if info:
            if platform == _platform.MEDIA_PLAYER:
                result = await info.async_setup_media_player_platform(
                    platform_config, add_entities, discovery_info
                )
            elif platform == _platform.SWITCH:
                result = await info.async_setup_switch_platform(
                    platform_config, add_entities, discovery_info
                )
        return result

    async def async_setup_platform_devices(
        self, entry: core.ConfigEntry, async_add_entities: core.AddEntitiesCallback
    ) -> None:
        account = entry.data[_const.CONF_EMAIL]
        info = self._accounts.get(account, None)
        result = False
        if info:
            platform = core.EntityPlatform.async_get_current_platform().domain
            if platform == _platform.MEDIA_PLAYER:
                result = await info.async_setup_media_player_devices(
                    entry, async_add_entities
                )
            elif platform == _platform.SWITCH:
                result = await info.async_setup_switch_devices(
                    entry, async_add_entities
                )
        return result

    # @retry_async(limit=5, delay=2, catch_exceptions=True)
    async def async_get_service(
        self, config: core.ConfigType, discovery_info: core.DiscoveryInfoType = None
    ) -> core.BaseNotificationService:
        # pylint: disable=unused-argument
        """Get the demo notification service."""
        result = self._notify_service
        if not result:
            for account, info in self._accounts.items():
                for key, _ in info.media_player_devices.items():
                    if key not in info.media_players:
                        _LOGGER.debug(
                            f"{alexapy.hide_email(account)}: Media player "
                            + f"{alexapy.hide_serial(key)} not loaded yet; delaying load",
                        )
                        return None
            result = self._notify_service = AlexaNotificationService(self)
        return result
