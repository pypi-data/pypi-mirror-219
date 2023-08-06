"""
Dashboards Component for Smart Home - The Next Generation.

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
import uuid
import voluptuous as vol

from ... import core
from .const import Const
from .lovelace_config import LovelaceConfig


_LOGGER: typing.Final = logging.getLogger(__name__)

_CREATE_SCHEMA: typing.Final = vol.Schema(Const.RESOURCE_CREATE_FIELDS)
_UPDATE_SCHEMA: typing.Final = vol.Schema(Const.RESOURCE_UPDATE_FIELDS)


# pylint: disable=unused-variable
class ResourceStorageCollection(core.StorageCollection):
    """Collection to store resources."""

    def __init__(
        self,
        shc: core.SmartHomeController,
        ll_config: LovelaceConfig,
        storage_key: str,
        storage_version: int = 1,
    ) -> None:
        """Initialize the storage collection."""
        super().__init__(
            core.Store(shc, storage_version, storage_key),
            _LOGGER,
        )
        self._ll_config = ll_config
        self._loaded = False

    @property
    def loaded(self) -> bool:
        return self._loaded

    async def async_load(self) -> None:
        if self.loaded:
            return
        self._loaded = True
        await super().async_load()

    async def async_get_info(self):
        """Return the resources info for YAML mode."""
        if not self.loaded:
            await self.async_load()

        return {"resources": len(self.async_items() or [])}

    async def _async_load_data(self) -> dict:
        """Load the data."""
        if (data := await self.store.async_load()) is not None:
            return typing.cast(typing.Optional[dict], data)

        # Import it from config.
        try:
            conf = await self._ll_config.async_load(False)
        except core.SmartHomeControllerError:
            return None

        if core.Const.CONF_RESOURCES not in conf:
            return None

        # Remove it from config and save both resources + config
        data = conf[core.Const.CONF_RESOURCES]

        try:
            Const.RESOURCE_SCHEMA(data)
        except vol.Invalid as err:
            _LOGGER.warning(f"Resource import failed. Data invalid: {err}")
            return None

        conf.pop(core.Const.CONF_RESOURCES)

        for item in data:
            item[core.Const.CONF_ID] = uuid.uuid4().hex

        data = {"items": data}

        await self.store.async_save(data)
        await self._ll_config.async_save(conf)

        return data

    async def _process_create_data(self, data: dict) -> dict:
        """Validate the config is valid."""
        data = _CREATE_SCHEMA(data)
        data[core.Const.CONF_TYPE] = data.pop(Const.CONF_RESOURCE_TYPE_WS)
        return data

    @core.callback
    def _get_suggested_id(self, info: dict) -> str:
        """Return unique ID."""
        return uuid.uuid4().hex

    async def _update_data(self, data: dict, update_data: dict) -> dict:
        """Return a new updated data object."""
        if not self.loaded:
            await self.async_load()

        update_data = _UPDATE_SCHEMA(update_data)
        if Const.CONF_RESOURCE_TYPE_WS in update_data:
            update_data[core.Const.CONF_TYPE] = update_data.pop(
                Const.CONF_RESOURCE_TYPE_WS
            )

        return {**data, **update_data}
