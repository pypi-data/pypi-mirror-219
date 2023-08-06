"""
Philips Hue Integration for Smart Home - The Next Generation.

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

Hue V1 API specific platform implementation.
"""


# pylint: disable=unused-variable
async def remove_devices(bridge, api_ids, current):
    """Get items that are removed from api."""
    removed_items = []

    for item_id in current:
        if item_id in api_ids:
            continue

        # Device is removed from Hue, so we remove it from Home Assistant
        entity = current[item_id]
        removed_items.append(item_id)
        await entity.async_remove(force_remove=True)
        ent_registry = bridge.controller.entity_registry
        if entity.entity_id in ent_registry.entities:
            ent_registry.async_remove(entity.entity_id)
        dev_registry = bridge.controller.device_registry
        device = dev_registry.async_get_device(
            identifiers={(bridge.owner.domain, entity.device_id)}
        )
        if device is not None:
            dev_registry.async_update_device(
                device.id, remove_config_entry_id=bridge.config_entry.entry_id
            )

    for item_id in removed_items:
        del current[item_id]
