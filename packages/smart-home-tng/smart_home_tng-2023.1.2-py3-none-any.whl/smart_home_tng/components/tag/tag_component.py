"""
Tag Component for Smart Home - The Next Generation.

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
from .const import Const
from .tag_id_manager import TagIDManager
from .tag_storage_collection import TagStorageCollection

_ConfVal: typing.TypeAlias = core.ConfigValidation

_LOGGER: typing.Final = logging.getLogger(__name__)


# pylint: disable=unused-variable
class TagComponent(core.TagComponent, core.TriggerPlatform):
    """The Tag integration."""

    def __init__(self, path: typing.Iterable[str]):
        super().__init__(path)
        self._storage_collection: TagStorageCollection = None

    async def async_setup(self, config: core.ConfigType) -> bool:
        """Set up the Tag component."""
        if not await super().async_setup(config):
            return False

        id_manager = TagIDManager()
        storage_collection = TagStorageCollection(
            core.Store(self._shc, self.storage_version, self.storage_key),
            logging.getLogger(f"{__name__}.storage_collection"),
            id_manager,
        )
        await storage_collection.async_load()
        core.StorageCollectionWebSocket(
            storage_collection,
            self.domain,
            self.domain,
            Const.CREATE_FIELDS,
            Const.UPDATE_FIELDS,
        ).async_setup()
        self._storage_collection = storage_collection

        return True

    async def async_scan_tag(
        self, tag_id: str, device_id: str, context: core.Context = None
    ) -> None:
        """Handle when a tag is scanned."""

        self._shc.bus.async_fire(
            Const.EVENT_TAG_SCANNED,
            {Const.TAG_ID: tag_id, core.Const.CONF_DEVICE_ID: device_id},
            context=context,
        )
        helper = self._storage_collection
        if tag_id in helper.data:
            await helper.async_update_item(
                tag_id, {Const.LAST_SCANNED: core.helpers.utcnow()}
            )
        else:
            await helper.async_create_item(
                {Const.TAG_ID: tag_id, Const.LAST_SCANNED: core.helpers.utcnow()}
            )
        _LOGGER.debug(f"Tag: {tag_id} scanned by device: {device_id}")

    async def async_validate_trigger_config(
        self, config: core.ConfigType
    ) -> core.ConfigType:
        schema = _ConfVal.TRIGGER_BASE_SCHEMA.extend(
            {
                vol.Required(core.Const.CONF_PLATFORM): self.domain,
                vol.Required(Const.TAG_ID): vol.All(
                    _ConfVal.ensure_list, [_ConfVal.string]
                ),
                vol.Optional(core.Const.CONF_DEVICE_ID): vol.All(
                    _ConfVal.ensure_list, [_ConfVal.string]
                ),
            }
        )
        return schema(config)

    async def async_attach_trigger(
        self,
        config: core.ConfigType,
        action: core.TriggerActionType,
        trigger_info: core.TriggerInfo,
    ) -> core.CallbackType:
        """Listen for tag_scanned events based on configuration."""
        trigger_data = trigger_info["trigger_data"]
        tag_ids = set(config[Const.TAG_ID])
        device_ids = (
            set(config[core.Const.CONF_DEVICE_ID])
            if core.Const.CONF_DEVICE_ID in config
            else None
        )

        job = core.SmartHomeControllerJob(action)

        async def handle_event(event: core.Event) -> None:
            """Listen for tag scan events and calls the action when data matches."""
            if event.data.get(Const.TAG_ID) not in tag_ids or (
                device_ids is not None
                and event.data.get(core.Const.CONF_DEVICE_ID) not in device_ids
            ):
                return

            task = self._shc.async_run_shc_job(
                job,
                {
                    "trigger": {
                        **trigger_data,
                        "platform": self.domain,
                        "event": event,
                        "description": "Tag scanned",
                    }
                },
                event.context,
            )

            if task:
                await task

        return self._shc.bus.async_listen(Const.EVENT_TAG_SCANNED, handle_event)
