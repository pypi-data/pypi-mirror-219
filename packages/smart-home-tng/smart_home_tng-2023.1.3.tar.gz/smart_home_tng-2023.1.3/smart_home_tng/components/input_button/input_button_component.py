"""
Input Button Component for Smart Home - The Next Generation.

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
import typing
import voluptuous as vol

from ... import core
from .const import Const
from .input_button import InputButton
from .input_button_storage_collection import InputButtonStorageCollection

_cv: typing.TypeAlias = core.ConfigValidation

_LOGGER: typing.Final = logging.getLogger(__name__)


# pylint: disable=unused-variable
class InputButtonComponent(core.SmartHomeControllerComponent, core.RecorderPlatform):
    """
    Support to keep track of user controlled buttons which
    can be used in automations.
    """

    def __init__(self, path: typing.Iterable[str]):
        super().__init__(path)
        self._component: core.EntityComponent = None
        self._yaml_collection: core.YamlCollection = None
        self._supported_platforms = frozenset([core.Platform.RECORDER])

    @property
    def entity_component(self) -> core.EntityComponent:
        return self._component

    def exclude_attributes(self) -> set[str]:
        """Exclude editable hint from being recorded in the database."""
        return {core.Const.ATTR_EDITABLE}

    async def async_validate_config(self, config: core.ConfigType) -> core.ConfigType:
        schema = vol.Schema(
            {
                self.domain: _cv.schema_with_slug_keys(
                    vol.Any(Const.UPDATE_FIELDS, None)
                )
            },
            extra=vol.ALLOW_EXTRA,
        )
        return schema(config)

    async def async_setup(self, config: core.ConfigType) -> bool:
        """Set up an input button."""
        if not await super().async_setup(config):
            return False

        # pylint: disable=protected-access
        InputButton._domain = self.domain

        component = core.EntityComponent(_LOGGER, self.domain, self._shc)
        self._component = component

        # Process integration platforms right away since
        # we will create entities before firing EVENT_COMPONENT_LOADED
        await self._shc.setup.async_process_integration_platform_for_component(
            self.domain
        )

        id_manager = core.IDManager()

        yaml_collection = core.YamlCollection(
            logging.getLogger(f"{__name__}.yaml_collection"), id_manager
        )
        yaml_collection.sync_entity_lifecycle(
            self._shc, self.domain, self.domain, component, InputButton.from_yaml
        )
        self._yaml_collection = yaml_collection

        storage_collection = InputButtonStorageCollection(
            core.Store(self._shc, self.storage_version, self.storage_key),
            logging.getLogger(f"{__name__}.storage_collection"),
            id_manager,
        )
        storage_collection.sync_entity_lifecycle(
            self._shc, self.domain, self.domain, component, InputButton
        )

        await yaml_collection.async_load(
            [
                {core.Const.CONF_ID: id_, **(conf or {})}
                for id_, conf in config.get(self.domain, {}).items()
            ]
        )
        await storage_collection.async_load()

        core.StorageCollectionWebSocket(
            storage_collection,
            self.domain,
            self.domain,
            Const.CREATE_FIELDS,
            Const.UPDATE_FIELDS,
        ).async_setup()

        core.Service.async_register_admin_service(
            self._shc,
            self.domain,
            core.Const.SERVICE_RELOAD,
            self._reload_service_handler,
            schema=Const.RELOAD_SERVICE_SCHEMA,
        )

        # pylint: disable=protected-access
        component.async_register_entity_service(
            core.Const.SERVICE_PRESS, {}, "_async_press_action"
        )

        return True

    async def _reload_service_handler(self, _service_call: core.ServiceCall) -> None:
        """Remove all input buttons and load new ones from config."""
        conf = await self._component.async_prepare_reload(skip_reset=True)
        if conf is None:
            return
        await self._yaml_collection.async_load(
            [
                {core.Const.CONF_ID: id_, **(conf or {})}
                for id_, conf in conf.get(self.domain, {}).items()
            ]
        )
