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
from .const import Const

_cv: typing.TypeAlias = core.ConfigValidation
_IGNORE_CEC_SCHEMA: typing.Final = vol.Schema(vol.All(_cv.ensure_list, [_cv.string]))
_KNOWN_HOSTS_SCHEMA: typing.Final = vol.Schema(vol.All(_cv.ensure_list, [_cv.string]))
_WANTED_UUID_SCHEMA: typing.Final = vol.Schema(vol.All(_cv.ensure_list, [_cv.string]))


# pylint: disable=unused-variable
class CastOptionsFlow(core.OptionsFlow):
    """Handle Google Cast options."""

    def __init__(
        self,
        owner: core.SmartHomeControllerComponent,
        config_entry: core.ConfigEntry,
        context: dict = None,
        init_data: typing.Any = None,
    ) -> None:
        """Initialize Google Cast options flow."""
        super().__init__(config_entry.entry_id, context, init_data)
        self._config_entry = config_entry
        self._updated_config: dict[str, typing.Any] = {}
        self._owner = owner

    async def async_step_init(self, _user_input=None):
        """Manage the Google Cast options."""
        return await self.async_step_basic_options()

    async def async_step_basic_options(self, user_input=None):
        """Manage the Google Cast options."""
        errors = {}
        current_config = self._config_entry.data
        if user_input is not None:
            bad_hosts, known_hosts = _string_to_list(
                user_input.get(Const.CONF_KNOWN_HOSTS, ""), _KNOWN_HOSTS_SCHEMA
            )

            if not bad_hosts:
                self._updated_config = dict(current_config)
                self._updated_config[Const.CONF_KNOWN_HOSTS] = known_hosts

                if self.show_advanced_options:
                    return await self.async_step_advanced_options()

                self._owner.controller.config_entries.async_update_entry(
                    self._config_entry, data=self._updated_config
                )
                return self.async_create_entry(title="", data=None)

        fields = {}
        suggested_value = _list_to_string(current_config.get(Const.CONF_KNOWN_HOSTS))
        _add_with_suggestion(fields, Const.CONF_KNOWN_HOSTS, suggested_value)

        return self.async_show_form(
            step_id="basic_options",
            data_schema=vol.Schema(fields),
            errors=errors,
            last_step=not self.show_advanced_options,
        )

    async def async_step_advanced_options(self, user_input=None):
        """Manage the Google Cast options."""
        errors = {}
        if user_input is not None:
            bad_cec, ignore_cec = _string_to_list(
                user_input.get(Const.CONF_IGNORE_CEC, ""), _IGNORE_CEC_SCHEMA
            )
            bad_uuid, wanted_uuid = _string_to_list(
                user_input.get(Const.CONF_UUID, ""), _WANTED_UUID_SCHEMA
            )

            if not bad_cec and not bad_uuid:
                self._updated_config[Const.CONF_IGNORE_CEC] = ignore_cec
                self._updated_config[Const.CONF_UUID] = wanted_uuid
                self._owner.controller.config_entries.async_update_entry(
                    self._config_entry, data=self._updated_config
                )
                return self.async_create_entry(title="", data=None)

        fields = {}
        current_config = self._config_entry.data
        suggested_value = _list_to_string(current_config.get(Const.CONF_UUID))
        _add_with_suggestion(fields, Const.CONF_UUID, suggested_value)
        suggested_value = _list_to_string(current_config.get(Const.CONF_IGNORE_CEC))
        _add_with_suggestion(fields, Const.CONF_IGNORE_CEC, suggested_value)

        return self.async_show_form(
            step_id="advanced_options",
            data_schema=vol.Schema(fields),
            errors=errors,
            last_step=True,
        )


def _list_to_string(items):
    comma_separated_string = ""
    if items:
        comma_separated_string = ",".join(items)
    return comma_separated_string


def _string_to_list(string, schema):
    invalid = False
    items = [x.strip() for x in string.split(",") if x.strip()]
    try:
        items = schema(items)
    except vol.Invalid:
        invalid = True

    return invalid, items


def _add_with_suggestion(fields, key, suggested_value):
    fields[vol.Optional(key, description={"suggested_value": suggested_value})] = str
