"""
Configuration API for Smart Home - The Next Generation.

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

from ... import core
from .edit_key_based_config_view import EditKeyBasedConfigView


# pylint: disable=unused-variable
class EditScriptConfigView(EditKeyBasedConfigView):
    """Edit script config."""

    def __init__(self, component: core.ScriptComponent):
        super().__init__(
            component.domain,
            "config",
            core.SetupManager.SCRIPT_CONFIG_PATH,
            core.ConfigValidation.string,
            data_schema=None,
            post_write_hook=self.hook,
            data_validator=component.async_validate_config_item,
        )
        self._script_comp = component

    def _write_value(self, _shc, data, config_key, new_value):
        """Set value."""
        data[config_key] = new_value

    async def hook(self, action: str, config_key: str):
        """post_write_hook for Config View that reloads scripts."""
        shc = self._script_comp.controller
        domain = self._script_comp.domain
        await shc.services.async_call(domain, core.Const.SERVICE_RELOAD)

        if action != self.ACTION_DELETE:
            return

        ent_reg = shc.entity_registry

        entity_id = ent_reg.async_get_entity_id(domain, domain, config_key)

        if entity_id is None:
            return

        ent_reg.async_remove(entity_id)
