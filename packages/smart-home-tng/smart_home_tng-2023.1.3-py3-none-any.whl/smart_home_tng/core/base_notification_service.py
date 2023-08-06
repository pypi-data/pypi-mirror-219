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

import functools
import typing

from . import helpers
from .config_validation import ConfigValidation as cv
from .const import Const
from .service import Service
from .service_call import ServiceCall
from .smart_home_controller import SmartHomeController
from .yaml_loader import YamlLoader


# pylint: disable=unused-variable
class BaseNotificationService:
    """An abstract class for notification services."""

    # While not purely typed, it makes typehinting more useful for us
    # and removes the need for constant None checks or asserts.
    def __init__(self, shc: SmartHomeController) -> None:
        self._shc = shc
        # Name => target
        self._registered_targets: dict[str, str] = None
        self._services_dict: dict = None

    @property
    def registered_targets(self):
        return self._registered_targets

    # pylint: disable=unused-argument
    def send_message(self, message: str, **kwargs: typing.Any) -> None:
        """Send a message.

        kwargs can contain ATTR_TITLE to specify a title.
        """
        raise NotImplementedError()

    async def async_send_message(self, message: str, **kwargs: typing.Any) -> None:
        """Send a message.

        kwargs can contain ATTR_TITLE to specify a title.
        """
        await self._shc.async_add_executor_job(
            functools.partial(self.send_message, message, **kwargs)
        )

    async def _async_notify_message_service(self, service: ServiceCall) -> None:
        """Handle sending notification message service calls."""
        kwargs = {}
        message = service.data[Const.ATTR_MESSAGE]

        if title := service.data.get(Const.ATTR_TITLE):
            title.controller = self._shc
            kwargs[Const.ATTR_TITLE] = title.async_render(parse_result=False)

        if self._registered_targets.get(service.service) is not None:
            kwargs[Const.ATTR_TARGET] = [self._registered_targets[service.service]]
        elif service.data.get(Const.ATTR_TARGET) is not None:
            kwargs[Const.ATTR_TARGET] = service.data.get(Const.ATTR_TARGET)

        message.controller = self._shc
        kwargs[Const.ATTR_MESSAGE] = message.async_render(parse_result=False)
        kwargs[Const.ATTR_DATA] = service.data.get(Const.ATTR_DATA)

        await self.async_send_message(**kwargs)

    async def async_setup(
        self,
        shc: SmartHomeController,
        service_name: str,
        target_service_name_prefix: str,
    ) -> None:
        """Store the data for the notify service."""
        # pylint: disable=attribute-defined-outside-init
        self._shc = shc
        self._service_name = service_name
        self._target_service_name_prefix = target_service_name_prefix
        self._registered_targets = {}

        # Load service descriptions from notify/services.yaml
        integration = await shc.setup.async_get_integration("notify")
        services_yaml = integration.file_path / "services.yaml"
        self._services_dict = typing.cast(
            dict,
            await shc.async_add_executor_job(YamlLoader.load_yaml, str(services_yaml)),
        )

    async def async_register_services(self) -> None:
        """Create or update the notify services."""
        if hasattr(self, "targets"):
            stale_targets = set(self._registered_targets)

            for name, target in self.targets.items():
                target_name = helpers.slugify(
                    f"{self._target_service_name_prefix}_{name}"
                )
                if target_name in stale_targets:
                    stale_targets.remove(target_name)
                if (
                    target_name in self._registered_targets
                    and target == self._registered_targets[target_name]
                ):
                    continue
                self._registered_targets[target_name] = target
                self._shc.services.async_register(
                    "notify",
                    target_name,
                    self._async_notify_message_service,
                    schema=cv.NOTIFY_SERVICE_SCHEMA,
                )
                # Register the service description
                service_desc = {
                    Const.CONF_NAME: f"Send a notification via {target_name}",
                    Const.CONF_DESCRIPTION: (
                        "Sends a notification message using "
                        + f"the {target_name} integration."
                    ),
                    Const.CONF_FIELDS: self._services_dict[Const.SERVICE_NOTIFY][
                        Const.CONF_FIELDS
                    ],
                }
                Service.async_set_service_schema(
                    self._shc, "notify", target_name, service_desc
                )

            for stale_target_name in stale_targets:
                del self._registered_targets[stale_target_name]
                self._shc.services.async_remove(
                    "notify",
                    stale_target_name,
                )

        if self._shc.services.has_service("notify", self._service_name):
            return

        self._shc.services.async_register(
            "notify",
            self._service_name,
            self._async_notify_message_service,
            schema=cv.NOTIFY_SERVICE_SCHEMA,
        )

        # Register the service description
        service_desc = {
            Const.CONF_NAME: f"Send a notification with {self._service_name}",
            Const.CONF_DESCRIPTION: (
                "Sends a notification message using the "
                + f"{self._service_name} service."
            ),
            Const.CONF_FIELDS: self._services_dict[Const.SERVICE_NOTIFY][
                Const.CONF_FIELDS
            ],
        }
        Service.async_set_service_schema(
            self._shc, "notify", self._service_name, service_desc
        )

    async def async_unregister_services(self) -> None:
        """Unregister the notify services."""
        if self._registered_targets:
            remove_targets = set(self._registered_targets)
            for remove_target_name in remove_targets:
                del self._registered_targets[remove_target_name]
                self._shc.services.async_remove(
                    "notify",
                    remove_target_name,
                )

        if not self._shc.services.has_service("notify", self._service_name):
            return

        self._shc.services.async_remove(
            "notify",
            self._service_name,
        )
