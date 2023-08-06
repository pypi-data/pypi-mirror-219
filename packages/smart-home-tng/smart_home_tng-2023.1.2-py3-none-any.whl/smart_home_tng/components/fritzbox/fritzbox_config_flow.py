"""
AVM FRITZ!SmartHome Integration for Smart Home - The Next Generation.

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
import typing
import urllib.parse

import pyfritzhome as fritz
import requests
import voluptuous as vol

from ... import core
from .const import Const

_DATA_SCHEMA_USER: typing.Final = vol.Schema(
    {
        vol.Required(core.Const.CONF_HOST, default=Const.DEFAULT_HOST): str,
        vol.Required(core.Const.CONF_USERNAME, default=Const.DEFAULT_USERNAME): str,
        vol.Required(core.Const.CONF_PASSWORD): str,
    }
)
_DATA_SCHEMA_CONFIRM: typing.Final = vol.Schema(
    {
        vol.Required(core.Const.CONF_USERNAME, default=Const.DEFAULT_USERNAME): str,
        vol.Required(core.Const.CONF_PASSWORD): str,
    }
)
_RESULT_INVALID_AUTH: typing.Final = "invalid_auth"
_RESULT_NO_DEVICES_FOUND: typing.Final = "no_devices_found"
_RESULT_NOT_SUPPORTED: typing.Final = "not_supported"
_RESULT_SUCCESS: typing.Final = "success"


# pylint: disable=unused-variable
class FritzboxConfigFlow(core.ConfigFlow):
    """Handle a AVM FRITZ!SmartHome config flow."""

    def __init__(
        self,
        shc: core.SmartHomeController,
        handler: str,
        context: dict[str, typing.Any] = None,
        data: typing.Any = None,
    ):
        """Initialize flow."""
        version = 1
        super().__init__(shc, handler, context, data, version)
        self._entry: core.ConfigEntry = None
        self._host: str = None
        self._name: str = None
        self._password: str = None
        self._username: str = None

    def _get_entry(self, name: str) -> core.FlowResult:
        return self.async_create_entry(
            title=name,
            data={
                core.Const.CONF_HOST: self._host,
                core.Const.CONF_PASSWORD: self._password,
                core.Const.CONF_USERNAME: self._username,
            },
        )

    async def _update_entry(self) -> None:
        assert self._entry is not None
        self.controller.config_entries.async_update_entry(
            self._entry,
            data={
                core.Const.CONF_HOST: self._host,
                core.Const.CONF_PASSWORD: self._password,
                core.Const.CONF_USERNAME: self._username,
            },
        )
        await self.controller.config_entries.async_reload(self._entry.entry_id)

    def _try_connect(self) -> str:
        """Try to connect and check auth."""
        fritzbox = fritz.Fritzhome(
            host=self._host, user=self._username, password=self._password
        )
        try:
            fritzbox.login()
            fritzbox.get_device_elements()
            fritzbox.logout()
            return _RESULT_SUCCESS
        except fritz.LoginError:
            return _RESULT_INVALID_AUTH
        except requests.exceptions.HTTPError:
            return _RESULT_NOT_SUPPORTED
        except OSError:
            return _RESULT_NO_DEVICES_FOUND

    async def async_step_user(
        self, user_input: dict[str, typing.Any] = None
    ) -> core.FlowResult:
        """Handle a flow initialized by the user."""
        errors = {}

        if user_input is not None:
            self._async_abort_entries_match(
                {core.Const.CONF_HOST: user_input[core.Const.CONF_HOST]}
            )

            self._host = user_input[core.Const.CONF_HOST]
            self._name = str(user_input[core.Const.CONF_HOST])
            self._password = user_input[core.Const.CONF_PASSWORD]
            self._username = user_input[core.Const.CONF_USERNAME]

            result = await self._shc.async_add_executor_job(self._try_connect)

            if result == _RESULT_SUCCESS:
                return self._get_entry(self._name)
            if result != _RESULT_INVALID_AUTH:
                return self.async_abort(reason=result)
            errors["base"] = result

        return self.async_show_form(
            step_id="user", data_schema=_DATA_SCHEMA_USER, errors=errors
        )

    async def async_step_ssdp(
        self, discovery_info: core.SSDP.ServiceInfo
    ) -> core.FlowResult:
        """Handle a flow initialized by discovery."""
        host = urllib.parse.urlparse(discovery_info.ssdp_location).hostname
        assert isinstance(host, str)
        self.context[core.Const.CONF_HOST] = host

        if (
            ipaddress.ip_address(host).version == 6
            and ipaddress.ip_address(host).is_link_local
        ):
            return self.async_abort(reason="ignore_ip6_link_local")

        if uuid := discovery_info.upnp.get(core.SSDP.ATTR_UPNP_UDN):
            if uuid.startswith("uuid:"):
                uuid = uuid[5:]
            await self.async_set_unique_id(uuid)
            self._abort_if_unique_id_configured({core.Const.CONF_HOST: host})

        for progress in self._async_in_progress():
            if progress.get("context", {}).get(core.Const.CONF_HOST) == host:
                return self.async_abort(reason="already_in_progress")

        # update old and user-configured config entries
        for entry in self._async_current_entries():
            if entry.data[core.Const.CONF_HOST] == host:
                if uuid and not entry.unique_id:
                    self._shc.config_entries.async_update_entry(entry, unique_id=uuid)
                return self.async_abort(reason="already_configured")

        self._host = host
        self._name = str(
            discovery_info.upnp.get(core.SSDP.ATTR_UPNP_FRIENDLY_NAME) or host
        )

        self.context["title_placeholders"] = {"name": self._name}
        return await self.async_step_confirm()

    async def async_step_confirm(
        self, user_input: dict[str, typing.Any] = None
    ) -> core.FlowResult:
        """Handle user-confirmation of discovered node."""
        errors = {}

        if user_input is not None:
            self._password = user_input[core.Const.CONF_PASSWORD]
            self._username = user_input[core.Const.CONF_USERNAME]
            result = await self._shc.async_add_executor_job(self._try_connect)

            if result == _RESULT_SUCCESS:
                assert self._name is not None
                return self._get_entry(self._name)
            if result != _RESULT_INVALID_AUTH:
                return self.async_abort(reason=result)
            errors["base"] = result

        return self.async_show_form(
            step_id="confirm",
            data_schema=_DATA_SCHEMA_CONFIRM,
            description_placeholders={"name": self._name},
            errors=errors,
        )

    async def async_step_reauth(
        self, entry_data: typing.Mapping[str, typing.Any]
    ) -> core.FlowResult:
        """Trigger a reauthentication flow."""
        entry = self._shc.config_entries.async_get_entry(self.context["entry_id"])
        assert entry is not None
        self._entry = entry
        self._host = entry_data[core.Const.CONF_HOST]
        self._name = str(entry_data[core.Const.CONF_HOST])
        self._username = entry_data[core.Const.CONF_USERNAME]

        return await self.async_step_reauth_confirm()

    async def async_step_reauth_confirm(
        self, user_input: dict[str, typing.Any] = None
    ) -> core.FlowResult:
        """Handle reauthorization flow."""
        errors = {}

        if user_input is not None:
            self._password = user_input[core.Const.CONF_PASSWORD]
            self._username = user_input[core.Const.CONF_USERNAME]

            result = await self._shc.async_add_executor_job(self._try_connect)

            if result == _RESULT_SUCCESS:
                await self._update_entry()
                return self.async_abort(reason="reauth_successful")
            if result != _RESULT_INVALID_AUTH:
                return self.async_abort(reason=result)
            errors["base"] = result

        return self.async_show_form(
            step_id="reauth_confirm",
            data_schema=vol.Schema(
                {
                    vol.Required(core.Const.CONF_USERNAME, default=self._username): str,
                    vol.Required(core.Const.CONF_PASSWORD): str,
                }
            ),
            description_placeholders={"name": self._name},
            errors=errors,
        )
