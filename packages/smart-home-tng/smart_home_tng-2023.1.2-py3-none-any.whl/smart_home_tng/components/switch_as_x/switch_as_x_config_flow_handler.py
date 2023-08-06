"""
Switch As X Component for Smart Home - The Next Generation.

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


TARGET_DOMAIN_OPTIONS: typing.Final = [
    core.SelectOptionDict(value=core.Platform.COVER, label="Cover"),
    core.SelectOptionDict(value=core.Platform.FAN, label="Fan"),
    core.SelectOptionDict(value=core.Platform.LIGHT, label="Light"),
    core.SelectOptionDict(value=core.Platform.LOCK, label="Lock"),
    core.SelectOptionDict(value=core.Platform.SIREN, label="Siren"),
]

CONFIG_FLOW: typing.Final[
    dict[str, core.SchemaFlow.FormStep | core.SchemaFlow.MenuStep]
] = {
    "user": core.SchemaFlow.FormStep(
        vol.Schema(
            {
                vol.Required(core.Const.CONF_ENTITY_ID): core.EntitySelector(
                    core.EntitySelectorConfig(domain=core.Platform.SWITCH),
                ),
                vol.Required(Const.CONF_TARGET_DOMAIN): core.SelectSelector(
                    core.SelectSelectorConfig(options=TARGET_DOMAIN_OPTIONS),
                ),
            }
        )
    )
}


# pylint: disable=unused-variable
class SwitchAsXConfigFlowHandler(core.SchemaFlow.ConfigFlow):
    """Handle a config flow for Switch as X."""

    config_flow = CONFIG_FLOW

    def __init__(
        self,
        owner: core.SmartHomeControllerComponent,
        context: dict[str, typing.Any] = None,
        data: typing.Any = None,
    ):
        version = 1
        super().__init__(
            owner.controller, owner.domain, context=context, data=data, version=version
        )

    def async_config_entry_title(self, options: typing.Mapping[str, typing.Any]) -> str:
        """Return config entry title and hide the wrapped entity if registered."""
        # Hide the wrapped entry if registered
        registry = self._shc.entity_registry
        entity_entry = registry.async_get(options[core.Const.CONF_ENTITY_ID])
        if entity_entry is not None and not entity_entry.hidden:
            registry.async_update_entity(
                options[core.Const.CONF_ENTITY_ID],
                hidden_by=core.EntityRegistryEntryHider.INTEGRATION,
            )

        return core.SchemaFlow.wrapped_entity_config_entry_title(
            self._shc, options[core.Const.CONF_ENTITY_ID]
        )
