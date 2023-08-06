"""
AVM FRITZ!Box Tools Integration for Smart Home - The Next Generation.

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

import ipaddress
import logging
import socket
import typing
import urllib.parse as url_parse

import fritzconnection as fritz
import fritzconnection.core.exceptions as fritz_exceptions
import voluptuous as vol

from ... import core
from .const import Const

_LOGGER: typing.Final = logging.getLogger(__name__)


# pylint: disable=unused-variable
class FritzboxToolsFlowHandler(core.ConfigFlow):
    """Handle a FRITZ!Box Tools config flow."""

    def __init__(
        self,
        shc: core.SmartHomeController,
        handler: str,
        context: dict[str, typing.Any] = None,
        data: typing.Any = None,
    ):
        """Initialize FRITZ!Box Tools flow."""
        version = 1
        super().__init__(shc, handler, context, data, version)
        self._host: str = None
        self._entry: core.ConfigEntry = None
        self._name: str = ""
        self._password: str = ""
        self._port: int = None
        self._username: str = ""
        self._model: str = ""

    def fritz_tools_init(self) -> str:
        """Initialize FRITZ!Box Tools class."""

        try:
            connection = fritz.FritzConnection(
                address=self._host,
                port=self._port,
                user=self._username,
                password=self._password,
                timeout=60.0,
                pool_maxsize=30,
            )
        except fritz_exceptions.FritzSecurityError:
            return Const.ERROR_AUTH_INVALID
        except fritz_exceptions.FritzConnectionException:
            return Const.ERROR_CANNOT_CONNECT
        except Exception:  # pylint: disable=broad-except
            _LOGGER.exception("Unexpected exception")
            return Const.ERROR_UNKNOWN

        self._model = connection.call_action("DeviceInfo:1", "GetInfo")["NewModelName"]

        if (
            "X_AVM-DE_UPnP1" in connection.services
            and not connection.call_action("X_AVM-DE_UPnP1", "GetInfo")["NewEnable"]
        ):
            return Const.ERROR_UPNP_NOT_CONFIGURED

        return None

    async def async_check_configured_entry(self) -> core.ConfigEntry:
        """Check if entry is configured."""
        assert self._host
        shc = self.controller
        current_host = await shc.async_add_executor_job(
            socket.gethostbyname, self._host
        )

        for entry in self._async_current_entries(include_ignore=False):
            entry_host = await shc.async_add_executor_job(
                socket.gethostbyname, entry.data[core.Const.CONF_HOST]
            )
            if entry_host == current_host:
                return entry
        return None

    @core.callback
    def _async_create_entry(self) -> core.FlowResult:
        """Async create flow handler entry."""
        consider_home = core.DeviceTracker.DEFAULT_CONSIDER_HOME.total_seconds()
        return self.async_create_entry(
            title=self._name,
            data={
                core.Const.CONF_HOST: self._host,
                core.Const.CONF_PASSWORD: self._password,
                core.Const.CONF_PORT: self._port,
                core.Const.CONF_USERNAME: self._username,
            },
            options={
                core.DeviceTracker.CONF_CONSIDER_HOME: consider_home,
                Const.CONF_OLD_DISCOVERY: Const.DEFAULT_CONF_OLD_DISCOVERY,
            },
        )

    async def async_step_ssdp(
        self, discovery_info: core.SSDP.ServiceInfo
    ) -> core.FlowResult:
        """Handle a flow initialized by discovery."""
        ssdp_location = url_parse.urlparse(discovery_info.ssdp_location or "")
        self._host = ssdp_location.hostname
        self._port = ssdp_location.port
        self._name = (
            discovery_info.upnp.get(core.SSDP.ATTR_UPNP_FRIENDLY_NAME)
            or discovery_info.upnp[core.SSDP.ATTR_UPNP_MODEL_NAME]
        )
        self.context[core.Const.CONF_HOST] = self._host

        if not self._host or ipaddress.ip_address(self._host).is_link_local:
            return self.async_abort(reason="ignore_ip6_link_local")

        if uuid := discovery_info.upnp.get(core.SSDP.ATTR_UPNP_UDN):
            if uuid.startswith("uuid:"):
                uuid = uuid[5:]
            await self.async_set_unique_id(uuid)
            self._abort_if_unique_id_configured({core.Const.CONF_HOST: self._host})

        for progress in self._async_in_progress():
            if progress.get("context", {}).get(core.Const.CONF_HOST) == self._host:
                return self.async_abort(reason="already_in_progress")

        if entry := await self.async_check_configured_entry():
            if uuid and not entry.unique_id:
                self._shc.config_entries.async_update_entry(entry, unique_id=uuid)
            return self.async_abort(reason="already_configured")

        self.context.update(
            {
                "title_placeholders": {"name": self._name.replace("FRITZ!Box ", "")},
                "configuration_url": f"http://{self._host}",
            }
        )

        return await self.async_step_confirm()

    async def async_step_confirm(
        self, user_input: dict[str, typing.Any] = None
    ) -> core.FlowResult:
        """Handle user-confirmation of discovered node."""
        if user_input is None:
            return self._show_setup_form_confirm()

        errors = {}

        self._username = user_input[core.Const.CONF_USERNAME]
        self._password = user_input[core.Const.CONF_PASSWORD]

        error = await self._shc.async_add_executor_job(self.fritz_tools_init)

        if error:
            errors["base"] = error
            return self._show_setup_form_confirm(errors)

        return self._async_create_entry()

    def _show_setup_form_init(self, errors: dict[str, str] = None) -> core.FlowResult:
        """Show the setup form to the user."""
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Optional(core.Const.CONF_HOST, default=Const.DEFAULT_HOST): str,
                    vol.Optional(
                        core.Const.CONF_PORT, default=Const.DEFAULT_PORT
                    ): vol.Coerce(int),
                    vol.Required(core.Const.CONF_USERNAME): str,
                    vol.Required(core.Const.CONF_PASSWORD): str,
                }
            ),
            errors=errors or {},
        )

    def _show_setup_form_confirm(
        self, errors: dict[str, str] = None
    ) -> core.FlowResult:
        """Show the setup form to the user."""
        return self.async_show_form(
            step_id="confirm",
            data_schema=vol.Schema(
                {
                    vol.Required(core.Const.CONF_USERNAME): str,
                    vol.Required(core.Const.CONF_PASSWORD): str,
                }
            ),
            description_placeholders={"name": self._name},
            errors=errors or {},
        )

    async def async_step_user(
        self, user_input: dict[str, typing.Any] = None
    ) -> core.FlowResult:
        """Handle a flow initiated by the user."""
        if user_input is None:
            return self._show_setup_form_init()
        self._host = user_input[core.Const.CONF_HOST]
        self._port = user_input[core.Const.CONF_PORT]
        self._username = user_input[core.Const.CONF_USERNAME]
        self._password = user_input[core.Const.CONF_PASSWORD]

        if not (error := await self._shc.async_add_executor_job(self.fritz_tools_init)):
            self._name = self._model

            if await self.async_check_configured_entry():
                error = "already_configured"

        if error:
            return self._show_setup_form_init({"base": error})

        return self._async_create_entry()

    async def async_step_reauth(
        self, entry_data: typing.Mapping[str, typing.Any]
    ) -> core.FlowResult:
        """Handle flow upon an API authentication error."""
        self._entry = self._shc.config_entries.async_get_entry(self.context["entry_id"])
        self._host = entry_data[core.Const.CONF_HOST]
        self._port = entry_data[core.Const.CONF_PORT]
        self._username = entry_data[core.Const.CONF_USERNAME]
        self._password = entry_data[core.Const.CONF_PASSWORD]
        return await self.async_step_reauth_confirm()

    def _show_setup_form_reauth_confirm(
        self, user_input: dict[str, typing.Any], errors: dict[str, str] = None
    ) -> core.FlowResult:
        """Show the reauth form to the user."""
        default_username = user_input.get(core.Const.CONF_USERNAME)
        return self.async_show_form(
            step_id="reauth_confirm",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        core.Const.CONF_USERNAME, default=default_username
                    ): str,
                    vol.Required(core.Const.CONF_PASSWORD): str,
                }
            ),
            description_placeholders={"host": self._host},
            errors=errors or {},
        )

    async def async_step_reauth_confirm(
        self, user_input: dict[str, typing.Any] = None
    ) -> core.FlowResult:
        """Dialog that informs the user that reauth is required."""
        if user_input is None:
            return self._show_setup_form_reauth_confirm(
                user_input={core.Const.CONF_USERNAME: self._username}
            )

        self._username = user_input[core.Const.CONF_USERNAME]
        self._password = user_input[core.Const.CONF_PASSWORD]

        if error := await self._shc.async_add_executor_job(self.fritz_tools_init):
            return self._show_setup_form_reauth_confirm(
                user_input=user_input, errors={"base": error}
            )

        assert isinstance(self._entry, core.ConfigEntry)
        self._shc.config_entries.async_update_entry(
            self._entry,
            data={
                core.Const.CONF_HOST: self._host,
                core.Const.CONF_PASSWORD: self._password,
                core.Const.CONF_PORT: self._port,
                core.Const.CONF_USERNAME: self._username,
            },
        )
        await self._shc.config_entries.async_reload(self._entry.entry_id)
        return self.async_abort(reason="reauth_successful")
