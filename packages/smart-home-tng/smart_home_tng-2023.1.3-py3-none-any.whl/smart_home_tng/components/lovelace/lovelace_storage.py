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

from ... import core
from .config_not_found import ConfigNotFound
from .const import Const
from .lovelace_config import LovelaceConfig


# pylint: disable=unused-variable
class LovelaceStorage(LovelaceConfig):
    """Class to handle Storage based Lovelace config."""

    def __init__(
        self,
        shc: core.SmartHomeController,
        config,
        default_storage_key: str,
        config_storage_version: int = 1,
    ):
        """Initialize Lovelace config based on storage helper."""
        url_path = None
        if config is not None:
            url_path = config[Const.CONF_URL_PATH]
        super().__init__(shc, url_path, config)
        if config is None:
            storage_key = default_storage_key
        else:
            storage_key = default_storage_key + f".{config[core.Const.CONF_ID]}"

        self._store = core.Store(shc, config_storage_version, storage_key)
        self._data = None

    @property
    def mode(self) -> str:
        """Return mode of the lovelace config."""
        return Const.MODE_STORAGE

    async def async_get_info(self):
        """Return the Lovelace storage info."""
        if self._data is None:
            await self._load()

        if self._data["config"] is None:
            return {"mode": "auto-gen"}

        return self._config_info(self.mode, self._data["config"])

    async def async_load(self, force):
        """Load config."""
        if self._shc.config.safe_mode:
            raise ConfigNotFound

        if self._data is None:
            await self._load()

        if (config := self._data["config"]) is None:
            raise ConfigNotFound

        return config

    async def async_save(self, config):
        """Save config."""
        if self._shc.config.safe_mode:
            raise core.SmartHomeControllerError("Saving not supported in safe mode")

        if self._data is None:
            await self._load()
        self._data["config"] = config
        self._config_updated()
        await self._store.async_save(self._data)

    async def async_delete(self):
        """Delete config."""
        if self._shc.config.safe_mode:
            raise core.SmartHomeControllerError("Deleting not supported in safe mode")

        await self._store.async_remove()
        self._data = None
        self._config_updated()

    async def _load(self):
        """Load the config."""
        data = await self._store.async_load()
        self._data = data if data else {"config": None}
