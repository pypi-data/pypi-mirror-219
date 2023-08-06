"""
Google Cast Integration for Smart Home - The Next Generation.

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
import threading
import typing

import pychromecast as google
import voluptuous as vol
from pychromecast.controllers import multizone

from ... import core
from .cast_config_flow import CastConfigFlow
from .cast_media_player_entity import async_setup_media_players
from .cast_options_flow import CastOptionsFlow
from .cast_platform import CastPlatform
from .const import Const

_cv: typing.TypeAlias = core.ConfigValidation

_LOGGER: typing.Final = logging.getLogger(__name__)
_PLATFORMS: typing.Final = [core.Platform.MEDIA_PLAYER]
_ENTITY_SCHEMA: typing.Final = vol.All(
    vol.Schema(
        {
            vol.Optional(Const.CONF_UUID): _cv.string,
            vol.Optional(Const.CONF_IGNORE_CEC): vol.All(_cv.ensure_list, [_cv.string]),
        }
    ),
)


# pylint: disable=unused-variable
class GoogleCastIntegration(core.SmartHomeControllerComponent, core.ConfigFlowPlatform):
    """Component to embed Google Cast."""

    def __init__(self, path: typing.Iterable[str]):
        super().__init__(path)
        self._register_flow()
        self._browser: google.discovery.CastBrowser = None
        self._mz_mgr = multizone.MultizoneManager()
        self._added_cast_devices: set[str] = set()
        self._cast_platforms: dict[str | core.Platform, CastPlatform] = {}
        self._unknown_models: dict[str, typing.Any] = {}
        self._supported_platforms = frozenset(_PLATFORMS + [core.Platform.CONFIG_FLOW])
        self._discovery_running = threading.Lock()

    @property
    def added_cast_devices(self) -> set[str]:
        return self._added_cast_devices

    @property
    def browser(self) -> google.discovery.CastBrowser:
        return self._browser

    @property
    def cast_platforms(self) -> dict[str, CastPlatform]:
        return self._cast_platforms

    @property
    def discovery_running(self) -> threading.Lock:
        return self._discovery_running

    @property
    def mz_mgr(self) -> multizone.MultizoneManager:
        return self._mz_mgr

    @property
    def unknown_models(self):
        return self._unknown_models

    def get_platform(
        self, platform: core.Platform | str
    ) -> core.PlatformImplementation:
        return super().get_platform(platform)

    async def async_setup(self, config: core.ConfigType) -> bool:
        """Set up the Cast component."""
        if not await super().async_setup(config):
            return False

        if (conf := config.get(self.domain)) is not None:
            media_player_config_validated = []
            media_player_config = conf.get("media_player", {})
            if not isinstance(media_player_config, list):
                media_player_config = [media_player_config]
            for cfg in media_player_config:
                try:
                    cfg = _ENTITY_SCHEMA(cfg)
                    media_player_config_validated.append(cfg)
                except vol.Error as ex:
                    _LOGGER.warning(f"Invalid config '{cfg}': {ex}")

            self.controller.async_create_task(
                self.controller.config_entries.flow.async_init(
                    self.domain,
                    context={"source": core.ConfigEntrySource.IMPORT},
                    data=media_player_config_validated,
                )
            )

        return True

    async def async_setup_platform(
        self,
        platform_config: core.ConfigType,
        add_entities: core.AddEntitiesCallback,
        discovery_info: core.DiscoveryInfoType,
    ):
        return await super().async_setup_platform(
            platform_config, add_entities, discovery_info
        )

    async def async_setup_entry(self, entry: core.ConfigEntry) -> bool:
        """Set up Cast from a config entry."""
        shc = self.controller
        # await home_assistant_cast.async_setup_ha_cast(hass, entry)
        shc.config_entries.async_setup_platforms(entry, _PLATFORMS)
        await shc.setup.async_process_integration_platforms(
            self.domain, self._register_cast_platform
        )
        return True

    async def _register_cast_platform(
        self, integration_domain: str, platform: core.PlatformImplementation
    ):
        """Register a cast platform."""
        if not isinstance(platform, CastPlatform):
            raise core.SmartHomeControllerError(f"Invalid cast platform {platform}")
        self._cast_platforms[integration_domain] = platform

    async def async_remove_entry(self, entry: core.ConfigEntry) -> None:
        """Remove Home Assistant Cast user."""
        # await home_assistant_cast.async_remove_user(hass, entry)

    async def async_remove_config_entry_device(
        self, entry: core.ConfigEntry, device_entry: core.Device
    ) -> bool:
        """Remove cast config entry from a device.

        The actual cleanup is done in CastMediaPlayerEntity.async_will_remove_from_hass.
        """
        return True

    async def async_setup_platform_devices(
        self, entry: core.ConfigEntry, async_add_entities: core.AddEntitiesCallback
    ) -> None:
        entity_platform = core.EntityPlatform.async_get_current_platform()
        platform = entity_platform.domain
        if platform == core.Platform.MEDIA_PLAYER:
            await async_setup_media_players(self, entry, async_add_entities)

    # ------------------------------ Config Flow Platform -------------------------------

    def create_config_flow(
        self, context: dict, init_data: typing.Any
    ) -> core.ConfigFlow:
        return CastConfigFlow(self, self.domain, context, init_data)

    async def async_get_options_flow(
        self,
        entry: core.ConfigEntry,
        context: dict = None,
        init_data: typing.Any = None,
    ) -> core.OptionsFlow:
        """Get the options flow for this handler."""
        return CastOptionsFlow(self, entry, context, init_data)
