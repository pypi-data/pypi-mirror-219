"""
Update Component for Smart Home - The Next Generation.

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

import datetime as dt
import logging
import typing

import voluptuous as vol

from ... import core

_cv: typing.TypeAlias = core.ConfigValidation
_LOGGER: typing.Final = logging.getLogger(__name__)
_WS_RELEASE_NOTES: typing.Final = {
    vol.Required("type"): "update/release_notes",
    vol.Required("entity_id"): _cv.entity_id,
}


# pylint: disable=unused-variable
class UpdateComponent(
    core.SmartHomeControllerComponent,
    core.RecorderPlatform,
    core.SignificantChangePlatform,
    core.TriggerPlatform,
):
    """Component to allow for providing device or service updates."""

    def __init__(self, path: typing.Iterable[str]):
        super().__init__(path)
        self._entities: core.EntityComponent = None
        self._supported_platforms = frozenset(
            {
                core.Platform.RECORDER,
                core.Platform.SIGNIFICANT_CHANGE,
                core.Platform.TRIGGER,
            }
        )

    @property
    def entity_component(self) -> core.EntityComponent:
        return self._entities

    @property
    def scan_interval(self) -> dt.timedelta:
        return core.Update.SCAN_INTERVAL

    async def async_setup(self, config: core.ConfigType) -> bool:
        """Set up Select entities."""
        websocket_api = self.controller.components.websocket_api
        if not isinstance(
            websocket_api, core.WebSocket.Component
        ) or not await super().async_setup(config):
            return False

        component = self._entities = core.EntityComponent(
            _LOGGER, self.domain, self.controller, self.scan_interval
        )
        await component.async_setup(config)

        component.async_register_entity_service(
            core.Update.SERVICE_INSTALL,
            {
                vol.Optional(core.Update.ATTR_VERSION): _cv.string,
                vol.Optional(core.Update.ATTR_BACKUP, default=False): _cv.boolean,
            },
            _async_install,
            [core.Update.EntityFeature.INSTALL],
        )

        component.async_register_entity_service(
            core.Update.SERVICE_SKIP,
            {},
            _async_skip,
        )
        component.async_register_entity_service(
            "clear_skipped",
            {},
            _async_clear_skipped,
        )

        websocket_api.register_command(self._ws_release_notes, _WS_RELEASE_NOTES)

        return True

    async def async_setup_entry(self, entry: core.ConfigEntry) -> bool:
        """Set up a config entry."""
        component = self._entities
        return await component.async_setup_entry(entry)

    async def async_unload_entry(self, entry: core.ConfigEntry) -> None:
        """Unload a config entry."""
        component = self._entities
        return await component.async_unload_entry(entry)

    async def _ws_release_notes(
        self,
        connection: core.WebSocket.Connection,
        msg: dict,
    ) -> None:
        """Get the full release notes for a entity."""
        connection.require_admin()

        component = self._entities
        entity: core.Update.Entity = component.get_entity(msg["entity_id"])

        if entity is None:
            connection.send_error(
                msg["id"], core.WebSocket.ERR_NOT_FOUND, "Entity not found"
            )
            return

        if not entity.supported_features & core.Update.EntityFeature.RELEASE_NOTES:
            connection.send_error(
                msg["id"],
                core.WebSocket.ERR_NOT_SUPPORTED,
                "Entity does not support release notes",
            )
            return

        connection.send_result(
            msg["id"],
            await entity.async_release_notes(),
        )

    # -------------------- Recorder Platform ----------------------

    def exclude_attributes(self) -> set[str]:
        """Exclude large and chatty update attributes from being recorded in the database."""
        return {
            core.Const.ATTR_ENTITY_PICTURE,
            core.Update.ATTR_IN_PROGRESS,
            core.Update.ATTR_RELEASE_SUMMARY,
        }

    # ------------------ Significant Change Platform -------------------

    def check_significant_change(
        self,
        old_state: str,
        old_attrs: dict,
        new_state: str,
        new_attrs: dict,
        **_kwargs: typing.Any,
    ) -> bool:
        """Test if state significantly changed."""
        if old_state != new_state:
            return True

        if old_attrs.get(core.Update.ATTR_INSTALLED_VERSION) != new_attrs.get(
            core.Update.ATTR_INSTALLED_VERSION
        ):
            return True

        if old_attrs.get(core.Update.ATTR_LATEST_VERSION) != new_attrs.get(
            core.Update.ATTR_LATEST_VERSION
        ):
            return True

        return False

    # -------------------- Trigger Plafform -----------------------

    @property
    def trigger_schema(self) -> typing.Callable[[core.ConfigType], core.ConfigType]:
        TRIGGER_SCHEMA: typing.Final = vol.All(
            core.Toggle.TRIGGER_SCHEMA,
            vol.Schema(
                {vol.Required(core.Const.CONF_DOMAIN): self.domain},
                extra=vol.ALLOW_EXTRA,
            ),
        )
        return TRIGGER_SCHEMA

    async def async_attach_trigger(
        self,
        config: core.ConfigType,
        action: core.TriggerActionType,
        trigger_info: core.TriggerInfo,
    ) -> core.CallbackType:
        """Listen for state changes based on configuration."""
        return await core.Toggle.async_attach_trigger(
            self.controller, config, action, trigger_info
        )

    async def async_get_triggers(self, device_id: str) -> list[dict[str, str]]:
        """List device triggers."""
        return await core.Toggle.async_get_triggers(
            self.controller, device_id, self.domain
        )

    async def async_get_trigger_capabilities(
        self, config: core.ConfigType
    ) -> dict[str, vol.Schema]:
        """List trigger capabilities."""
        return await core.Toggle.async_get_trigger_capabilities(config)


async def _async_install(
    entity: core.Update.Entity, service_call: core.ServiceCall
) -> None:
    """Service call wrapper to validate the call."""
    # If version is not specified, but no update is available.
    if (version := service_call.data.get(core.Update.ATTR_VERSION)) is None and (
        entity.installed_version == entity.latest_version
        or entity.latest_version is None
    ):
        raise core.SmartHomeControllerError(f"No update available for {entity.name}")

    # If version is specified, but not supported by the entity.
    if (
        version is not None
        and not entity.supported_features & core.Update.EntityFeature.SPECIFIC_VERSION
    ):
        raise core.SmartHomeControllerError(
            f"Installing a specific version is not supported for {entity.name}"
        )

    # If backup is requested, but not supported by the entity.
    if (
        backup := service_call.data[core.Update.ATTR_BACKUP]
    ) and not entity.supported_features & core.Update.EntityFeature.BACKUP:
        raise core.SmartHomeControllerError(
            f"Backup is not supported for {entity.name}"
        )

    # Update is already in progress.
    if entity.in_progress is not False:
        raise core.SmartHomeControllerError(
            f"Update installation already in progress for {entity.name}"
        )

    await entity.async_install_with_progress(version, backup)


async def _async_skip(
    entity: core.Update.Entity, _service_call: core.ServiceCall
) -> None:
    """Service call wrapper to validate the call."""
    if entity.auto_update:
        raise core.SmartHomeControllerError(
            f"Skipping update is not supported for {entity.name}"
        )
    await entity.async_skip()


async def _async_clear_skipped(
    entity: core.Update.Entity, _service_call: core.ServiceCall
) -> None:
    """Service call wrapper to validate the call."""
    if entity.auto_update:
        raise core.SmartHomeControllerError(
            f"Clearing skipped update is not supported for {entity.name}"
        )
    await entity.async_clear_skipped()
