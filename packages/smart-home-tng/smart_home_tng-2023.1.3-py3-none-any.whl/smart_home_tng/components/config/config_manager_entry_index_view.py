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

import asyncio

from ... import core
from ...core.config_flow import _CONFIG_HANDLERS


# pylint: disable=unused-variable
class ConfigManagerEntryIndexView(core.SmartHomeControllerView):
    """View to get available config entries."""

    def __init__(self):
        url = "/api/config/config_entries/entry"
        name = "api:config:config_entries:entry"
        super().__init__(url, name)

    async def get(self, request):
        """List available config entries."""
        shc: core.SmartHomeController = request.app[core.Const.KEY_SHC]

        kwargs = {}
        if "domain" in request.query:
            kwargs["domain"] = request.query["domain"]

        entries = shc.config_entries.async_entries(**kwargs)

        if "type" not in request.query:
            return self.json([_entry_json(entry) for entry in entries])

        integrations = {}
        type_filter = request.query["type"]

        async def load_integration(domain: str) -> core.Integration:
            """Load integration."""
            try:
                return await shc.setup.async_get_integration(domain)
            except core.IntegrationNotFound:
                return None

        # Fetch all the integrations so we can check their type
        for integration in await asyncio.gather(
            *(
                load_integration(domain)
                for domain in {entry.domain for entry in entries}
            )
        ):
            if integration:
                integrations[integration.domain] = integration

        entries = [
            entry
            for entry in entries
            if (type_filter != "helper" and entry.domain not in integrations)
            or (
                entry.domain in integrations
                and integrations[entry.domain].integration_type == type_filter
            )
        ]

        return self.json([_entry_json(entry) for entry in entries])


@core.callback
def _entry_json(entry: core.ConfigEntry) -> dict:
    """Return JSON value of a config entry."""
    supports_options = False
    handler = _CONFIG_HANDLERS.get(entry.domain)
    if handler is None:
        comp = core.SmartHomeControllerComponent.get_component(entry.domain)
        if isinstance(comp, core.SmartHomeControllerComponent):
            platform = comp.get_platform(core.Platform.CONFIG_FLOW)
            if isinstance(platform, core.ConfigFlowPlatform):
                supports_options = platform.supports_options_flow(entry)
    else:
        # work out if handler has support for options flow
        supports_options = handler.supports_options_flow(entry)

    return {
        "entry_id": entry.entry_id,
        "domain": entry.domain,
        "title": entry.title,
        "source": entry.source,
        "state": entry.state.value,
        "supports_options": supports_options,
        "supports_remove_device": entry.supports_remove_device,
        "supports_unload": entry.supports_unload,
        "pref_disable_new_entities": entry.pref_disable_new_entities,
        "pref_disable_polling": entry.pref_disable_polling,
        "disabled_by": entry.disabled_by,
        "reason": entry.reason,
    }
