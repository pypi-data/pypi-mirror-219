"""
Core components of Smart Home - The Next Generation.

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

# pylint: disable=unused-variable

import dataclasses
import datetime as dt
import enum
import typing

import awesomeversion as asv
import voluptuous as vol

from ..backports import strenum
from .const import Const
from .entity_category import EntityCategory
from .entity_description import EntityDescription
from .restore_entity import RestoreEntity
from .smart_home_controller_error import SmartHomeControllerError


class _EntityFeature(enum.IntEnum):
    """Supported features of the update entity."""

    INSTALL = 1
    SPECIFIC_VERSION = 2
    PROGRESS = 4
    BACKUP = 8
    RELEASE_NOTES = 16


class _DeviceClass(strenum.LowercaseStrEnum):
    """Device class for update."""

    FIRMWARE = enum.auto()


_DEVICE_CLASSES_SCHEMA: typing.Final = vol.All(vol.Lower, vol.Coerce(_DeviceClass))

_SERVICE_INSTALL: typing.Final = "install"
_SERVICE_SKIP: typing.Final = "skip"

_ATTR_AUTO_UPDATE: typing.Final = "auto_update"
_ATTR_BACKUP: typing.Final = "backup"
_ATTR_INSTALLED_VERSION: typing.Final = "installed_version"
_ATTR_IN_PROGRESS: typing.Final = "in_progress"
_ATTR_LATEST_VERSION: typing.Final = "latest_version"
_ATTR_RELEASE_SUMMARY: typing.Final = "release_summary"
_ATTR_RELEASE_URL: typing.Final = "release_url"
_ATTR_SKIPPED_VERSION: typing.Final = "skipped_version"
_ATTR_TITLE: typing.Final = "title"
_ATTR_VERSION: typing.Final = "version"
_SCAN_INTERVAL: typing.Final = dt.timedelta(minutes=15)


@dataclasses.dataclass
class _EntityDescription(EntityDescription):
    """A class that describes update entities."""

    device_class: _DeviceClass | str = None
    entity_category: EntityCategory = EntityCategory.CONFIG


class _Entity(RestoreEntity):
    """Representation of an update entity."""

    _entity_description: _EntityDescription
    _attr_auto_update: bool = False
    _attr_installed_version: str = None
    _attr_device_class: _DeviceClass | str
    _attr_in_progress: bool | int = False
    _attr_latest_version: str = None
    _attr_release_summary: str = None
    _attr_release_url: str = None
    _attr_state: None = None
    _attr_supported_features: int = 0
    _attr_title: str = None
    __skipped_version: str = None
    __in_progress: bool = False

    @property
    def entity_description(self) -> _EntityDescription:
        return super().entity_description

    @property
    def auto_update(self) -> bool:
        """Indicate if the device or service has auto update enabled."""
        return self._attr_auto_update

    @property
    def installed_version(self) -> str:
        """Version installed and in use."""
        return self._attr_installed_version

    @property
    def device_class(self) -> str:
        """Return the class of this entity."""
        if hasattr(self, "_attr_device_class"):
            return str(self._attr_device_class)
        if hasattr(self, "_entity_description"):
            return str(self.entity_description.device_class)
        return None

    @property
    def entity_category(self) -> EntityCategory:
        """Return the category of the entity, if any."""
        if hasattr(self, "_attr_entity_category"):
            return self._attr_entity_category
        if hasattr(self, "_entity_description"):
            return self.entity_description.entity_category
        if self.supported_features & _EntityFeature.INSTALL:
            return EntityCategory.CONFIG
        return EntityCategory.DIAGNOSTIC

    @property
    def entity_picture(self) -> str:
        """Return the entity picture to use in the frontend.

        Update entities return the brand icon based on the integration
        domain by default.
        """
        if self.platform is None:
            return None

        return (
            f"https://brands.home-assistant.io/_/{self.platform.platform_name}/icon.png"
        )

    @property
    def in_progress(self) -> bool | int:
        """Update installation progress.

        Needs UpdateEntityFeature.PROGRESS flag to be set for it to be used.

        Can either return a boolean (True if in progress, False if not)
        or an integer to indicate the progress in from 0 to 100%.
        """
        return self._attr_in_progress

    @property
    def latest_version(self) -> str:
        """Latest version available for install."""
        return self._attr_latest_version

    @property
    def release_summary(self) -> str:
        """Summary of the release notes or changelog.

        This is not suitable for long changelogs, but merely suitable
        for a short excerpt update description of max 255 characters.
        """
        return self._attr_release_summary

    @property
    def release_url(self) -> str:
        """URL to the full release notes of the latest version available."""
        return self._attr_release_url

    @property
    def supported_features(self) -> int:
        """Flag supported features."""
        return self._attr_supported_features

    @property
    def title(self) -> str:
        """Title of the software.

        This helps to differentiate between the device or entity name
        versus the title of the software installed.
        """
        return self._attr_title

    @typing.final
    async def async_skip(self) -> None:
        """Skip the current offered version to update."""
        if (latest_version := self.latest_version) is None:
            raise SmartHomeControllerError(
                f"Cannot skip an unknown version for {self.name}"
            )
        if self.installed_version == latest_version:
            raise SmartHomeControllerError(
                f"No update available to skip for {self.name}"
            )
        self.__skipped_version = latest_version
        self.async_write_state()

    @typing.final
    async def async_clear_skipped(self) -> None:
        """Clear the skipped version."""
        self.__skipped_version = None
        self.async_write_state()

    async def async_install(
        self, version: str, backup: bool, **kwargs: typing.Any
    ) -> None:
        """Install an update.

        Version can be specified to install a specific version. When `None`, the
        latest version needs to be installed.

        The backup parameter indicates a backup should be taken before
        installing the update.
        """
        await self._shc.async_add_executor_job(self.install, version, backup, **kwargs)

    def install(self, version: str, backup: bool, **kwargs: typing.Any) -> None:
        """Install an update.

        Version can be specified to install a specific version. When `None`, the
        latest version needs to be installed.

        The backup parameter indicates a backup should be taken before
        installing the update.
        """
        raise NotImplementedError()

    async def async_release_notes(self) -> str:
        """Return full release notes.

        This is suitable for a long changelog that does not fit in the release_summary property.
        The returned string can contain markdown.
        """
        return await self._shc.async_add_executor_job(self.release_notes)

    def release_notes(self) -> str:
        """Return full release notes.

        This is suitable for a long changelog that does not fit in the release_summary property.
        The returned string can contain markdown.
        """
        raise NotImplementedError()

    @property
    @typing.final
    def state(self) -> str:
        """Return the entity state."""
        if (installed_version := self.installed_version) is None or (
            latest_version := self.latest_version
        ) is None:
            return None

        if latest_version == self.__skipped_version:
            return Const.STATE_OFF
        if latest_version == installed_version:
            return Const.STATE_OFF

        try:
            newer = asv.AwesomeVersion(latest_version) > installed_version
            return Const.STATE_ON if newer else Const.STATE_OFF
        except asv.AwesomeVersionCompareException:
            # Can't compare versions, already tried exact match
            return Const.STATE_ON

    @typing.final
    @property
    def state_attributes(self) -> dict[str, typing.Any]:
        """Return state attributes."""
        if (release_summary := self.release_summary) is not None:
            release_summary = release_summary[:255]

        # If entity supports progress, return the in_progress value.
        # Otherwise, we use the internal progress value.
        if self.supported_features & _EntityFeature.PROGRESS:
            in_progress = self.in_progress
        else:
            in_progress = self.__in_progress

        # Clear skipped version in case it matches the current installed
        # version or the latest version diverged.
        if (
            self.installed_version is not None
            and self.__skipped_version == self.installed_version
        ) or (
            self.latest_version is not None
            and self.__skipped_version != self.latest_version
        ):
            self.__skipped_version = None

        return {
            _ATTR_AUTO_UPDATE: self.auto_update,
            _ATTR_INSTALLED_VERSION: self.installed_version,
            _ATTR_IN_PROGRESS: in_progress,
            _ATTR_LATEST_VERSION: self.latest_version,
            _ATTR_RELEASE_SUMMARY: release_summary,
            _ATTR_RELEASE_URL: self.release_url,
            _ATTR_SKIPPED_VERSION: self.__skipped_version,
            _ATTR_TITLE: self.title,
        }

    @typing.final
    async def async_install_with_progress(self, version: str, backup: bool) -> None:
        """Install update and handle progress if needed.

        Handles setting the in_progress state in case the entity doesn't
        support it natively.
        """
        if not self.supported_features & _EntityFeature.PROGRESS:
            self.__in_progress = True
            self.async_write_state()

        try:
            await self.async_install(version, backup)
        finally:
            # No matter what happens, we always stop progress in the end
            self._attr_in_progress = False
            self.__in_progress = False
            self.async_write_state()

    async def async_internal_added_to_shc(self) -> None:
        """Call when the update entity is added to hass.

        It is used to restore the skipped version, if any.
        """
        await super().async_internal_added_to_shc()
        state = await self.async_get_last_state()
        if (
            state is not None
            and state.attributes.get(_ATTR_SKIPPED_VERSION) is not None
        ):
            self.__skipped_version = state.attributes[_ATTR_SKIPPED_VERSION]


# pylint: disable=unused-variable, invalid-name
class Update:
    """Update namespace."""

    DeviceClass: typing.TypeAlias = _DeviceClass
    Entity: typing.TypeAlias = _Entity
    EntityDescription: typing.TypeAlias = _EntityDescription
    EntityFeature: typing.TypeAlias = _EntityFeature

    DEVICE_CLASSES_SCHEMA: typing.Final = _DEVICE_CLASSES_SCHEMA
    SERVICE_INSTALL: typing.Final = _SERVICE_INSTALL
    SERVICE_SKIP: typing.Final = _SERVICE_SKIP
    ATTR_AUTO_UPDATE: typing.Final = _ATTR_AUTO_UPDATE
    ATTR_BACKUP: typing.Final = _ATTR_BACKUP
    ATTR_INSTALLED_VERSION: typing.Final = _ATTR_INSTALLED_VERSION
    ATTR_IN_PROGRESS: typing.Final = _ATTR_IN_PROGRESS
    ATTR_LATEST_VERSION: typing.Final = _ATTR_LATEST_VERSION
    ATTR_RELEASE_SUMMARY: typing.Final = _ATTR_RELEASE_SUMMARY
    ATTR_RELEASE_URL: typing.Final = _ATTR_RELEASE_URL
    ATTR_SKIPPED_VERSION: typing.Final = _ATTR_SKIPPED_VERSION
    ATTR_TITLE: typing.Final = _ATTR_TITLE
    ATTR_VERSION: typing.Final = _ATTR_VERSION
    SCAN_INTERVAL: typing.Final = _SCAN_INTERVAL
