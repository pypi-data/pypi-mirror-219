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

import os
import pathlib
import time

from ... import core
from .config_not_found import ConfigNotFound
from .const import Const
from .lovelace_config import LovelaceConfig


# pylint: disable=unused-variable
class LovelaceYAML(LovelaceConfig):
    """Class to handle YAML-based Lovelace config."""

    def __init__(self, shc: core.SmartHomeController, url_path: str, config):
        """Initialize the YAML config."""
        super().__init__(shc, url_path, config)

        self._path = shc.config.path(
            config[core.Const.CONF_FILENAME] if config else Const.LOVELACE_CONFIG_FILE
        )
        self._cache = None

    @property
    def mode(self) -> str:
        """Return mode of the lovelace config."""
        return Const.MODE_YAML

    async def async_get_info(self):
        """Return the YAML storage mode."""
        try:
            config = await self.async_load(False)
        except ConfigNotFound:
            return {
                "mode": self.mode,
                "error": f"{self._path} not found",
            }

        return self._config_info(self.mode, config)

    async def async_load(self, force):
        """Load config."""
        is_updated, config = await self._shc.async_add_executor_job(
            self._load_config, force
        )
        if is_updated:
            self._config_updated()
        return config

    def _load_config(self, force):
        """Load the actual config."""
        # Check for a cached version of the config
        if not force and self._cache is not None:
            config, last_update = self._cache
            modtime = os.path.getmtime(self._path)
            if config and last_update > modtime:
                return False, config

        is_updated = self._cache is not None

        try:
            config = core.YamlLoader.load_yaml(
                self._path, core.Secrets(pathlib.Path(self._shc.config.config_dir))
            )
        except FileNotFoundError:
            raise ConfigNotFound from None

        self._cache = (config, time.time())
        return is_updated, config
