"""
Google Cast Integration for Smart Home - The Next Generation.

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
from .cast_options_flow import _KNOWN_HOSTS_SCHEMA
from .const import Const


# pylint: disable=unused-variable
class CastConfigFlow(core.ConfigFlow):
    """Handle a config flow."""

    def __init__(
        self,
        owner: core.SmartHomeControllerComponent,
        handler: str,
        context: dict[str, typing.Any] = None,
        data: typing.Any = None,
    ):
        """Initialize flow."""
        version = 1
        super().__init__(owner.controller, handler, context, data, version)
        self._owner = owner
        self._ignore_cec = set()
        self._known_hosts = set()
        self._wanted_uuid = set()

    async def async_step_import(self, import_data=None):
        """Import data."""
        if self._async_current_entries():
            return self.async_abort(reason="single_instance_allowed")

        media_player_config = import_data or []
        for cfg in media_player_config:
            if Const.CONF_IGNORE_CEC in cfg:
                self._ignore_cec.update(set(cfg[Const.CONF_IGNORE_CEC]))
            if Const.CONF_UUID in cfg:
                self._wanted_uuid.add(cfg[Const.CONF_UUID])

        data = self._get_data()
        return self.async_create_entry(title="Google Cast", data=data)

    async def async_step_user(self, _user_input=None):
        """Handle a flow initialized by the user."""
        if self._async_current_entries():
            return self.async_abort(reason="single_instance_allowed")

        return await self.async_step_config()

    async def async_step_zeroconf(
        self, _discovery_info: core.ZeroconfServiceInfo
    ) -> core.FlowResult:
        """Handle a flow initialized by zeroconf discovery."""
        if self._async_in_progress() or self._async_current_entries():
            return self.async_abort(reason="single_instance_allowed")

        await self.async_set_unique_id(self._owner.domain)

        return await self.async_step_confirm()

    async def async_step_config(self, user_input=None):
        """Confirm the setup."""
        errors = {}
        data = {Const.CONF_KNOWN_HOSTS: self._known_hosts}

        if user_input is not None:
            bad_hosts = False
            known_hosts = user_input[Const.CONF_KNOWN_HOSTS]
            known_hosts = [x.strip() for x in known_hosts.split(",") if x.strip()]
            try:
                known_hosts = _KNOWN_HOSTS_SCHEMA(known_hosts)
            except vol.Invalid:
                errors["base"] = "invalid_known_hosts"
                bad_hosts = True
            else:
                self._known_hosts = known_hosts
                data = self._get_data()
            if not bad_hosts:
                return self.async_create_entry(title="Google Cast", data=data)

        fields = {}
        fields[vol.Optional(Const.CONF_KNOWN_HOSTS, default="")] = str

        return self.async_show_form(
            step_id="config", data_schema=vol.Schema(fields), errors=errors
        )

    async def async_step_confirm(self, user_input=None):
        """Confirm the setup."""

        data = self._get_data()

        onboarding: core.OnboardingComponent = self._shc.components.onboarding
        if user_input is not None or not onboarding.async_is_onboarded():
            return self.async_create_entry(title="Google Cast", data=data)

        return self.async_show_form(step_id="confirm")

    def _get_data(self):
        return {
            Const.CONF_IGNORE_CEC: list(self._ignore_cec),
            Const.CONF_KNOWN_HOSTS: list(self._known_hosts),
            Const.CONF_UUID: list(self._wanted_uuid),
        }
