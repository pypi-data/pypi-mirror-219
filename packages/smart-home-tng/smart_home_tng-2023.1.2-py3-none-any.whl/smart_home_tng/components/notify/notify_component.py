"""
Notify Component for Smart Home - The Next Generation.

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
import typing

from ... import core
from .const import Const


# pylint: disable=unused-variable
class NotifyComponent(core.NotifyComponent):
    """Provides functionality to notify people."""

    def __init__(self, path: typing.Iterable[str]):
        super().__init__(path)
        self._template_warned = False
        self._notify_services = dict[str, list[core.BaseNotificationService]]()
        self._full_config: core.ConfigType = None
        self._notify_discovery_dispatcher = None

    async def async_setup(self, config: core.ConfigType) -> bool:
        """Set up the notify services."""
        self._full_config = config
        # pylint: disable=no-member
        if not await super().async_setup(config):
            return False

        setup_tasks = [
            asyncio.create_task(self._async_setup_platform(integration_name, p_config))
            for integration_name, p_config in self._shc.setup.config_per_platform(
                config, self.domain
            )
            if integration_name is not None
        ]

        if setup_tasks:
            await asyncio.wait(setup_tasks)

        self._notify_discovery_dispatcher = self._shc.setup.async_listen_platform(
            self.domain, self._async_platform_discovered
        )

        self.controller.services.async_register(
            self.domain,
            Const.SERVICE_PERSISTENT_NOTIFICATION,
            self._persistent_notification,
            schema=Const.PERSISTENT_NOTIFICATION_SERVICE_SCHEMA,
        )

        return True

    async def _async_platform_discovered(
        self, platform: str, info: core.DiscoveryInfoType
    ) -> None:
        """Handle for discovered platform."""
        await self._async_setup_platform(platform, discovery_info=info)

    async def _persistent_notification(self, service: core.ServiceCall) -> None:
        """Send notification via the built-in persistsent_notify integration."""
        shc = self.controller
        message = service.data[Const.ATTR_MESSAGE]
        message.controller = shc
        self._check_templates_warn(message)

        title = None
        if title_tpl := service.data.get(Const.ATTR_TITLE):
            title_tpl.controller = shc
            self._check_templates_warn(title_tpl)
            title = title_tpl.async_render(parse_result=False)

        self.controller.components.persistent_notification.async_create(
            message.async_render(parse_result=False), title
        )

    @core.callback
    def _check_templates_warn(self, tpl: core.Template) -> None:
        """Warn user that passing templates to notify service is deprecated."""
        if tpl.is_static or self._template_warned:
            return

        self._template_warned = True
        Const.LOGGER.warning(
            "Passing templates to notify service is deprecated and will be removed in 2021.12. "
            + "Automations and scripts handle templates automatically"
        )

    def _async_integration_has_notify_services(self, integration_name: str) -> bool:
        """Determine if an integration has notify services registered."""
        if integration_name not in self._notify_services:
            return False

        return True

    async def async_reset_platform(self, platform: str) -> None:
        """Unregister notify services for an integration."""
        if self._notify_discovery_dispatcher is not None:
            self._notify_discovery_dispatcher()
            self._notify_discovery_dispatcher = None
        if not self._async_integration_has_notify_services(platform):
            return

        tasks = [
            notify_service.async_unregister_services()
            for notify_service in self._notify_services[platform]
        ]

        await asyncio.gather(*tasks)

        del self._notify_services[platform]

    async def _async_setup_platform(
        self,
        integration_name: str,
        p_config: core.ConfigType = None,
        discovery_info: core.DiscoveryInfoType = None,
    ) -> None:
        """Set up a notify platform."""
        if p_config is None:
            p_config = {}

        platform = await self._shc.setup.async_prepare_setup_platform(
            self._full_config, core.Platform.NOTIFY, integration_name
        )

        if not isinstance(platform, core.NotifyPlatform):
            Const.LOGGER.error("Unknown notification service specified")
            return

        full_name = f"{self.domain}.{integration_name}"
        Const.LOGGER.info(f"Setting up {full_name}")
        with self._shc.setup.async_start_setup([full_name]):
            notify_service = None
            try:
                notify_service = await platform.async_get_service(
                    p_config, discovery_info
                )

                if notify_service is None:
                    # Platforms can decide not to create a service based
                    # on discovery data.
                    if discovery_info is None:
                        Const.LOGGER.error(
                            f"Failed to initialize notification service {integration_name}",
                        )
                    return

            except Exception:  # pylint: disable=broad-except
                Const.LOGGER.exception(f"Error setting up platform {integration_name}")
                return

            if discovery_info is None:
                discovery_info = {}

            conf_name = p_config.get(core.Const.CONF_NAME) or discovery_info.get(
                core.Const.CONF_NAME
            )
            target_service_name_prefix = conf_name or integration_name
            service_name = core.helpers.slugify(conf_name or core.Const.SERVICE_NOTIFY)

            await notify_service.async_setup(
                self._shc, service_name, target_service_name_prefix
            )
            await notify_service.async_register_services()

            self._notify_services.setdefault(integration_name, []).append(
                notify_service
            )
            self._shc.config.component_loaded(f"{self.domain}.{integration_name}")

    async def async_reload(self, integration_name: str) -> None:
        """Register notify services for an integration."""
        if not self._async_integration_has_notify_services(integration_name):
            return

        tasks = [
            notify_service.async_register_services()
            for notify_service in self._notify_services[integration_name]
        ]

        await asyncio.gather(*tasks)
