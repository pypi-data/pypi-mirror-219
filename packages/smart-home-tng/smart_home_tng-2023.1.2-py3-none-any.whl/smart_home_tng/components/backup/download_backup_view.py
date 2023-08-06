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

import http

from aiohttp import hdrs, web

from ... import core
from .backup_manager import BackupManager


# pylint: disable=unused-variable
class DownloadBackupView(core.SmartHomeControllerView):
    """Generate backup view."""

    def __init__(self, owner):
        url = "/api/backup/download/{slug}"
        name = "api:backup:download"
        super().__init__(url, name)
        self._owner = owner

    async def get(
        self,
        request: web.Request,
        slug: str,
    ) -> web.FileResponse | web.Response:
        """Download a backup file."""
        if not request[core.Const.KEY_SHC_USER].is_admin:
            return web.Response(status=http.HTTPStatus.UNAUTHORIZED)

        manager: BackupManager = self._owner.backup_manager
        backup = await manager.get_backup(slug)

        if backup is None or not backup.path.exists():
            return web.Response(status=http.HTTPStatus.NOT_FOUND)

        return web.FileResponse(
            path=backup.path.as_posix(),
            headers={
                hdrs.CONTENT_DISPOSITION: (
                    f"attachment; filename={core.helpers.slugify(backup.name)}.tar"
                )
            },
        )
