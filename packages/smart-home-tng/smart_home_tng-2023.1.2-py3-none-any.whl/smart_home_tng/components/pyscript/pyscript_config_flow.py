"""
PyScript Component for Smart Home - The Next Generation.

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


This component is based on the custom_component

Pyscript: Python Scripting for Home Assistant, Copyright (c) 2020-2022 Craig Barrat,
which may be freely used and copied according tho the terms of the Apache 2.0 License.

Original source code and documentation can be found under:
https://github.com/custom-components/pyscript
"""

import json
import typing

import voluptuous as vol

from ... import core
from .const import Const

_PYSCRIPT_SCHEMA: typing.Final = vol.Schema(
    {
        vol.Optional(Const.CONF_ALLOW_ALL_IMPORTS, default=False): bool,
        vol.Optional(Const.CONF_SHC_IS_GLOBAL, default=False): bool,
    },
    extra=vol.ALLOW_EXTRA,
)


# pylint: disable=unused-variable
class PyscriptConfigFlow(core.ConfigFlow):
    """Handle a pyscript config flow."""

    def __init__(
        self,
        owner: core.SmartHomeControllerComponent,
        context: dict[str, typing.Any] = None,
        data: typing.Any = None,
    ):
        version = 1
        super().__init__(owner.controller, owner.domain, context, data, version)
        self._owner = owner

    async def async_step_user(
        self, user_input: dict[str, typing.Any] = None
    ) -> dict[str, typing.Any]:
        """Handle a flow initialized by the user."""
        domain = self._owner.domain
        if len(self._shc.config_entries.async_entries(domain)) > 0 or (
            self.controller.components.pyscript is not None and user_input is None
        ):
            return self.async_abort(reason="single_instance_allowed")
        if user_input is not None:
            await self.async_set_unique_id(domain)
            return self.async_create_entry(title=domain, data=user_input)

        return self.async_show_form(step_id="user", data_schema=_PYSCRIPT_SCHEMA)

    async def async_step_import(
        self, import_config: dict[str, typing.Any] = None
    ) -> dict[str, typing.Any]:
        """Import a config entry from configuration.yaml."""
        # Convert OrderedDict to dict
        import_config = json.loads(json.dumps(import_config))

        # Check if import config entry matches any existing config entries
        # so we can update it if necessary
        entries = self._shc.config_entries.async_entries(self._owner.domain)
        if entries:
            entry = entries[0]
            updated_data = entry.data.copy()

            # Update values for all keys, excluding `allow_all_imports` for entries
            # set up through the UI.
            for key, val in import_config.items():
                if (
                    entry.source == core.ConfigEntrySource.IMPORT
                    or key not in Const.CONF_BOOL_ALL
                ):
                    updated_data[key] = val

            # Remove values for all keys in entry.data that are not in the imported config,
            # excluding `allow_all_imports` for entries set up through the UI.
            for key in entry.data:
                if (
                    (
                        entry.source == core.ConfigEntrySource.IMPORT
                        or key not in Const.CONF_BOOL_ALL
                    )
                    and key != Const.CONF_INSTALLED_PACKAGES
                    and key not in import_config
                ):
                    updated_data.pop(key)

            # Update and reload entry if data needs to be updated
            if updated_data != entry.data:
                self._shc.config_entries.async_update_entry(
                    entry=entry, data=updated_data
                )
                return self.async_abort(reason="updated_entry")

            return self.async_abort(reason="already_configured")

        return await self.async_step_user(user_input=import_config)
