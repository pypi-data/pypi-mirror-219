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

import logging
import typing

import voluptuous as vol

from ... import core
from .cover_switch import async_setup_covers
from .fan_switch import async_setup_fans
from .light_switch import async_setup_lights
from .switch_as_x_config_flow_handler import SwitchAsXConfigFlowHandler

_LOGGER: typing.Final = logging.getLogger(__name__)
_CONF_TARGET_DOMAIN: typing.Final = "target_domain"


# pylint: disable=unused-variable
class SwitchAsComponent(core.SmartHomeControllerComponent, core.ConfigFlowPlatform):
    """Component to wrap switch entities in entities of other domains."""

    def __init__(self, path: typing.Iterable[str]):
        super().__init__(path)
        self._register_flow()
        self._supported_platforms = frozenset(
            [
                core.Platform.CONFIG_FLOW,
                core.Platform.COVER,
                core.Platform.FAN,
                core.Platform.LIGHT,
                core.Platform.LOCK,
                core.Platform.SIREN,
            ]
        )

    async def async_setup_entry(self, entry: core.ConfigEntry) -> bool:
        """Set up a config entry."""
        shc = self.controller
        registry = shc.entity_registry
        device_registry = shc.device_registry
        try:
            entity_id = registry.async_validate_entity_id(
                entry.options[core.Const.CONF_ENTITY_ID]
            )
        except vol.Invalid:
            # The entity is identified by an unknown entity registry ID
            _LOGGER.error(
                "Failed to setup switch_as_x for unknown entity "
                + f"{entry.options[core.Const.CONF_ENTITY_ID]}",
            )
            return False

        async def async_registry_updated(event: core.Event) -> None:
            """Handle entity registry update."""
            data = event.data
            if data["action"] == "remove":
                await shc.config_entries.async_remove(entry.entry_id)

            if data["action"] != "update":
                return

            if "entity_id" in data["changes"]:
                # Entity_id changed, reload the config entry
                await shc.config_entries.async_reload(entry.entry_id)

            if device_id and "device_id" in data["changes"]:
                # If the tracked switch is no longer in the device, remove our config entry
                # from the device
                if (
                    not (
                        entity_entry := registry.async_get(
                            data[core.Const.CONF_ENTITY_ID]
                        )
                    )
                    or not device_registry.async_get(device_id)
                    or entity_entry.device_id == device_id
                ):
                    # No need to do any cleanup
                    return

                device_registry.async_update_device(
                    device_id, remove_config_entry_id=entry.entry_id
                )

        entry.async_on_unload(
            shc.tracker.async_track_entity_registry_updated_event(
                entity_id, async_registry_updated
            )
        )

        device_id = _async_add_to_device(shc, entry, entity_id)

        await shc.config_entries.async_forward_entry_setups(
            entry, (entry.options[_CONF_TARGET_DOMAIN],)
        )
        return True

    async def async_unload_entry(self, entry: core.ConfigEntry) -> bool:
        """Unload a config entry."""
        return await self.controller.config_entries.async_unload_platforms(
            entry, (entry.options[_CONF_TARGET_DOMAIN],)
        )

    async def async_remove_entry(self, entry: core.ConfigEntry) -> None:
        """Unload a config entry."""
        # Unhide the wrapped entry if registered
        registry = self.controller.entity_registry
        try:
            entity_id = registry.async_validate_entity_id(
                entry.options[core.Const.CONF_ENTITY_ID]
            )
        except vol.Invalid:
            # The source entity has been removed from the entity registry
            return

        if not (entity_entry := registry.async_get(entity_id)):
            return

        if entity_entry.hidden_by == core.EntityRegistryEntryHider.INTEGRATION:
            registry.async_update_entity(entity_id, hidden_by=None)

    async def async_setup_platform_devices(
        self, entry: core.ConfigEntry, async_add_entities: core.AddEntitiesCallback
    ) -> None:
        entity_platform = core.EntityPlatform.async_get_current_platform()
        platform = entity_platform.domain
        if platform == core.Platform.COVER:
            await async_setup_covers(self, entry, async_add_entities)
        elif platform == core.Platform.FAN:
            await async_setup_fans(self, entry, async_add_entities)
        elif platform == core.Platform.LIGHT:
            await async_setup_lights(self, entry, async_add_entities)

    def create_config_flow(
        self, context: dict, init_data: typing.Any
    ) -> core.ConfigFlow:
        return SwitchAsXConfigFlowHandler(self, context, init_data)


@core.callback
def _async_add_to_device(
    shc: core.SmartHomeController, entry: core.ConfigEntry, entity_id: str
) -> str:
    """Add our config entry to the tracked entity's device."""
    registry = shc.entity_registry
    device_registry = shc.device_registry
    device_id = None

    if (
        not (wrapped_switch := registry.async_get(entity_id))
        or not (device_id := wrapped_switch.device_id)
        or not (device_registry.async_get(device_id))
    ):
        return device_id

    device_registry.async_update_device(device_id, add_config_entry_id=entry.entry_id)

    return device_id
