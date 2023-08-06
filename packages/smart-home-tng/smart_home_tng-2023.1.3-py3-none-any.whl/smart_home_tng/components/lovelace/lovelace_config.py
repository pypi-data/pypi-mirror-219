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

import abc

from ... import core
from .const import Const


# pylint: disable=unused-variable
class LovelaceConfig(abc.ABC):
    """Base class for Lovelace config."""

    def __init__(self, shc: core.SmartHomeController, url_path: str, config):
        """Initialize Lovelace config."""
        self._shc = shc
        self._url_path = None
        if config:
            self._config = {**config, Const.CONF_URL_PATH: url_path}
            self._url_path = url_path
        else:
            self._config = None

    @property
    def config(self) -> core.ConfigType:
        return self._config

    @config.setter
    def config(self, value: core.ConfigType) -> None:
        self._config = value
        self._config_updated()

    @property
    def url_path(self) -> str:
        """Return url path."""
        return self._url_path

    @property
    @abc.abstractmethod
    def mode(self) -> str:
        """Return mode of the lovelace config."""

    @abc.abstractmethod
    async def async_get_info(self):
        """Return the config info."""

    @abc.abstractmethod
    async def async_load(self, force: bool):
        """Load config."""

    async def async_save(self, config):
        """Save config."""
        raise core.SmartHomeControllerError("Not supported")

    async def async_delete(self):
        """Delete config."""
        raise core.SmartHomeControllerError("Not supported")

    @core.callback
    def _config_updated(self):
        """Fire config updated event."""
        self._shc.bus.async_fire(
            Const.EVENT_LOVELACE_UPDATED, {"url_path": self.url_path}
        )

    @staticmethod
    def _config_info(mode, config):
        """Generate info about the config."""
        return {
            "mode": mode,
            "views": len(config.get("views", [])),
        }
