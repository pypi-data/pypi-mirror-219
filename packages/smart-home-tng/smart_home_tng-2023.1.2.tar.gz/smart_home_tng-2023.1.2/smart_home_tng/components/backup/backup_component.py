"""
Backup Component for Smart Home - The Next Generation.

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
from .backup_manager import BackupManager
from .download_backup_view import DownloadBackupView


_BACKUP_INFO: typing.Final = {vol.Required("type"): "backup/info"}
_BACKUP_REMOVE: typing.Final = {
    vol.Required("type"): "backup/remove",
    vol.Required("slug"): str,
}
_BACKUP_GENERATE: typing.Final = {vol.Required("type"): "backup/generate"}


# pylint: disable=unused-variable
class BackupComponent(core.SmartHomeControllerComponent):
    """The Backup integration."""

    def __init__(self, path: typing.Iterable[str]):
        super().__init__(path)
        self._backup_manager: BackupManager = None

    @property
    def backup_manager(self) -> BackupManager:
        return self._backup_manager

    async def async_setup(self, config: core.ConfigType) -> bool:
        # pylint: disable=no-member
        if not await super().async_setup(config):
            return False

        websocket_api = self.controller.components.websocket_api
        if not isinstance(websocket_api, core.WebSocket.Component):
            return False

        self._backup_manager = BackupManager(self.controller)

        self.controller.services.async_register(
            self.domain, "create", self._async_handle_create_service
        )

        websocket_api.register_command(self._backup_info, _BACKUP_INFO)
        websocket_api.register_command(self._backup_remove, _BACKUP_REMOVE)
        websocket_api.register_command(self._backup_generate, _BACKUP_GENERATE)

        # Register the http views.
        self.controller.http.register_view(DownloadBackupView(self))

        return True

    async def _async_handle_create_service(self, _call: core.ServiceCall) -> None:
        """Service handler for creating backups."""
        await self._backup_manager.generate_backup()

    async def _backup_info(
        self,
        connection: core.WebSocket.Connection,
        msg: dict,
    ) -> None:
        """List all stored backups."""
        connection.require_admin()

        backups = await self._backup_manager.get_backups()
        connection.send_result(
            msg["id"],
            {
                "backups": list(backups.values()),
                "backing_up": self._backup_manager.backing_up,
            },
        )

    async def _backup_remove(
        self,
        connection: core.WebSocket.Connection,
        msg: dict,
    ) -> None:
        """Remove a backup."""
        connection.require_admin()

        await self._backup_manager.remove_backup(msg["slug"])
        connection.send_result(msg["id"])

    async def _backup_generate(
        self,
        connection: core.WebSocket.Connection,
        msg: dict,
    ) -> None:
        """Generate a backup."""
        connection.require_admin()

        backup = await self._backup_manager.generate_backup()
        connection.send_result(msg["id"], backup)
