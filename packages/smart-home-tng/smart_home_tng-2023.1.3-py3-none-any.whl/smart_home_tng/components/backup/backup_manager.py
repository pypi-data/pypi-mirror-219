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

import asyncio
import hashlib
import json
import pathlib
import tarfile
import tempfile
import typing

import securetar

from ... import core
from .backup import Backup
from .const import Const


# pylint: disable=unused-variable
class BackupManager:
    """Backup manager for the Backup integration."""

    def __init__(self, shc: core.SmartHomeController) -> None:
        """Initialize the backup manager."""
        self._shc = shc
        self._backup_dir = pathlib.Path(shc.config.path("backups"))
        self._backing_up = False
        self._backups: dict[str, Backup] = {}
        self._platforms: dict[str, core.BackupPlatform] = {}
        self._loaded_backups = False
        self._loaded_platforms = False

    @property
    def backing_up(self) -> bool:
        return self._backing_up

    async def _add_platform(
        self,
        integration_domain: str,
        platform: core.BackupPlatform,
    ) -> None:
        """Add a platform to the backup manager."""
        if not isinstance(platform, core.BackupPlatform):
            Const.LOGGER.warning(
                f"{integration_domain} does not implement required functions "
                + "for the backup platform",
            )
            return
        self._platforms[integration_domain] = platform

    async def load_backups(self) -> None:
        """Load data of stored backup files."""
        backups = await self._shc.async_add_executor_job(self._read_backups)
        Const.LOGGER.debug(f"Loaded {len(backups)} backups")
        self._backups = backups
        self._loaded_backups = True

    async def load_platforms(self) -> None:
        """Load backup platforms."""
        await self._shc.setup.async_process_integration_platforms(
            core.Platform.BACKUP, self._add_platform
        )
        Const.LOGGER.debug(f"Loaded {len(self._platforms)} platforms")
        self._loaded_platforms = True

    def _read_backups(self) -> dict[str, Backup]:
        """Read backups from disk."""
        backups: dict[str, Backup] = {}
        for backup_path in self._backup_dir.glob("*.tar"):
            try:
                with tarfile.open(backup_path, "r:") as backup_file:
                    if data_file := backup_file.extractfile("./backup.json"):
                        data = json.loads(data_file.read())
                        backup = Backup(
                            slug=data["slug"],
                            name=data["name"],
                            date=data["date"],
                            path=backup_path,
                            size=round(backup_path.stat().st_size / 1_048_576, 2),
                        )
                        backups[backup.slug] = backup
            except (OSError, tarfile.TarError, json.JSONDecodeError, KeyError) as err:
                Const.LOGGER.warning(f"Unable to read backup {backup_path}: {err}")
        return backups

    async def get_backups(self) -> dict[str, Backup]:
        """Return backups."""
        if not self._loaded_backups:
            await self.load_backups()

        return self._backups

    async def get_backup(self, slug: str) -> Backup | None:
        """Return a backup."""
        if not self._loaded_backups:
            await self.load_backups()

        if not (backup := self._backups.get(slug)):
            return None

        if not backup.path.exists():
            Const.LOGGER.debug(
                f"Removing tracked backup ({backup.slug}) that does not exists "
                + f"on the expected path {backup.path}",
            )
            self._backups.pop(slug)
            return None

        return backup

    async def remove_backup(self, slug: str) -> None:
        """Remove a backup."""
        if (backup := await self.get_backup(slug)) is None:
            return

        await self._shc.async_add_executor_job(backup.path.unlink, True)
        Const.LOGGER.debug(f"Removed backup located at {backup.path}")
        self._backups.pop(slug)

    async def generate_backup(self) -> Backup:
        """Generate a backup."""
        if self._backing_up:
            raise core.SmartHomeControllerError("Backup already in progress")

        if not self._loaded_platforms:
            await self.load_platforms()

        try:
            self._backing_up = True
            pre_backup_results = await asyncio.gather(
                *(platform.async_pre_backup() for platform in self._platforms.values()),
                return_exceptions=True,
            )
            for result in pre_backup_results:
                if isinstance(result, Exception):
                    raise result

            backup_name = f"Core {core.Const.__version__}"
            date_str = core.helpers.now().isoformat()
            slug = _generate_slug(date_str, backup_name)

            backup_data = {
                "slug": slug,
                "name": backup_name,
                "date": date_str,
                "type": "partial",
                "folders": ["smart_home_tng"],
                "smart-home-controller": {"version": core.Const.__version__},
                "compressed": True,
            }
            tar_file_path = pathlib.Path(self._backup_dir, f"{backup_data['slug']}.tar")

            if not self._backup_dir.exists():
                Const.LOGGER.debug("Creating backup directory")
                self._shc.async_add_executor_job(self._backup_dir.mkdir)

            await self._shc.async_add_executor_job(
                self._generate_backup_contents,
                tar_file_path,
                backup_data,
            )
            backup = Backup(
                slug=slug,
                name=backup_name,
                date=date_str,
                path=tar_file_path,
                size=round(tar_file_path.stat().st_size / 1_048_576, 2),
            )
            if self._loaded_backups:
                self._backups[slug] = backup
            Const.LOGGER.debug(f"Generated new backup with slug {slug}")
            return backup
        finally:
            self._backing_up = False
            post_backup_results = await asyncio.gather(
                *(
                    platform.async_post_backup()
                    for platform in self._platforms.values()
                ),
                return_exceptions=True,
            )
            for result in post_backup_results:
                if isinstance(result, Exception):
                    raise result

    def _generate_backup_contents(
        self,
        tar_file_path: pathlib.Path,
        backup_data: dict[str, typing.Any],
    ) -> None:
        """Generate backup contents."""
        with tempfile.TemporaryDirectory() as tmp_dir, securetar.SecureTarFile(
            tar_file_path, "w", gzip=False
        ) as tar_file:
            tmp_dir_path = pathlib.Path(tmp_dir)
            core.helpers.save_json(
                tmp_dir_path.joinpath("./backup.json").as_posix(),
                backup_data,
            )
            with securetar.SecureTarFile(
                tmp_dir_path.joinpath("./homeassistant.tar.gz").as_posix(),
                "w",
            ) as core_tar:
                securetar.atomic_contents_add(
                    tar_file=core_tar,
                    origin_path=pathlib.Path(self._shc.config.path()),
                    excludes=Const.EXCLUDE_FROM_BACKUP,
                    arcname="data",
                )
            tar_file.add(tmp_dir_path, arcname=".")


def _generate_slug(date: str, name: str) -> str:
    """Generate a backup slug."""

    # pylint: disable=unexpected-keyword-arg
    return hashlib.sha1(
        f"{date} - {name}".lower().encode(), usedforsecurity=False
    ).hexdigest()[:8]
