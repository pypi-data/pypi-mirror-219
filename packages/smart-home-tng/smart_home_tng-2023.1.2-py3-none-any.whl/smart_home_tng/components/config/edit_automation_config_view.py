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

import uuid

from ... import core
from .edit_id_based_config_view import EditIdBasedConfigView


# pylint: disable=unused-variable
class EditAutomationConfigView(EditIdBasedConfigView):
    """Edit automation config."""

    def __init__(self, component: core.AutomationComponent):
        super().__init__(
            component.domain,
            "config",
            core.SetupManager.AUTOMATION_CONFIG_PATH,
            core.ConfigValidation.string,
            data_schema=None,
            post_write_hook=self.hook,
            data_validator=component.async_validate_config_item,
        )
        self._automation_comp = component

    async def hook(self, action, config_key):
        """post_write_hook for Config View that reloads automations."""
        domain = self._automation_comp.domain
        shc = self._automation_comp.controller
        await shc.services.async_call(domain, core.Const.SERVICE_RELOAD)

        if action != self.ACTION_DELETE:
            return

        ent_reg = self._automation_comp.controller.entity_registry

        entity_id = ent_reg.async_get_entity_id(domain, domain, config_key)

        if entity_id is None:
            return

        ent_reg.async_remove(entity_id)

    def _write_value(
        self,
        shc: core.SmartHomeController,
        data: core.JsonType,
        config_key: str,
        new_value: core.JsonType,
    ):
        """Set value."""
        updated_value = {core.Const.CONF_ID: config_key}

        # Iterate through some keys that we want to have ordered in the output
        for key in ("alias", "description", "trigger", "condition", "action"):
            if key in new_value:
                updated_value[key] = new_value[key]

        # We cover all current fields above, but just in case we start
        # supporting more fields in the future.
        updated_value.update(new_value)

        updated = False
        for index, cur_value in enumerate(data):
            # When people copy paste their automations to the config file,
            # they sometimes forget to add IDs. Fix it here.
            if core.Const.CONF_ID not in cur_value:
                cur_value[core.Const.CONF_ID] = uuid.uuid4().hex

            elif cur_value[core.Const.CONF_ID] == config_key:
                data[index] = updated_value
                updated = True

        if not updated:
            data.append(updated_value)
