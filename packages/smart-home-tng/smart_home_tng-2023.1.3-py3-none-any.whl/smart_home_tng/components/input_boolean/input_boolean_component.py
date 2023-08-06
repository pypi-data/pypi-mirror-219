"""
Input Boolean Component for Smart Home - The Next Generation.

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
import logging
import typing
import voluptuous as vol

from ... import core
from .const import Const
from .input_boolean import InputBoolean
from .input_boolean_storage_collection import InputBooleanStorageCollection

_cv: typing.TypeAlias = core.ConfigValidation

_LOGGER: typing.Final = logging.getLogger(__name__)


# pylint: disable=unused-variable
class InputBooleanComponent(
    core.SmartHomeControllerComponent,
    core.RecorderPlatform,
    core.ReproduceStatePlatform,
):
    """
    Support to keep track of user controlled booleans within automation.
    """

    def __init__(self, path: typing.Iterable[str]):
        super().__init__(path)
        self._component: core.EntityComponent = None
        self._yaml_collection: core.YamlCollection = None
        self._supported_platforms = frozenset(
            [core.Platform.RECORDER, core.Platform.REPRODUCE_STATE]
        )

    @property
    def entity_component(self) -> core.EntityComponent:
        return self._component

    def _is_on(self, entity_id: str) -> bool:
        """Test if input_boolean is True."""
        return self._shc.states.is_state(entity_id, core.Const.STATE_ON)

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

    async def _reload_service_handler(self, _service_call: core.ServiceCall) -> None:
        """Remove all input booleans and load new ones from config."""
        conf = await self._component.async_prepare_reload(skip_reset=True)
        if conf is None:
            return
        await self._yaml_collection.async_load(
            [
                {core.Const.CONF_ID: id_, **(conf or {})}
                for id_, conf in conf.get(self.domain, {}).items()
            ]
        )

    async def async_setup(self, config: core.ConfigType) -> bool:
        """Set up an input boolean."""
        if not await super().async_setup(config):
            return False

        component = core.EntityComponent(_LOGGER, self.domain, self._shc)
        # pylint: disable=protected-access
        InputBoolean._domain = self.domain

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
            self._shc, self.domain, self.domain, component, InputBoolean.from_yaml
        )

        storage_collection = InputBooleanStorageCollection(
            core.Store(self._shc, self.storage_version, self.storage_key),
            logging.getLogger(f"{__name__}.storage_collection"),
            id_manager,
        )
        storage_collection.sync_entity_lifecycle(
            self._shc,
            self.domain,
            self.domain,
            component,
            InputBoolean,
        )

        await yaml_collection.async_load(
            [
                {core.Const.CONF_ID: id_, **(conf or {})}
                for id_, conf in config.get(self.domain, {}).items()
            ]
        )
        await storage_collection.async_load()

        self._component = component
        self._yaml_collection = yaml_collection

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

        component.async_register_entity_service(
            core.Const.SERVICE_TURN_ON, {}, "async_turn_on"
        )

        component.async_register_entity_service(
            core.Const.SERVICE_TURN_OFF, {}, "async_turn_off"
        )

        component.async_register_entity_service(
            core.Const.SERVICE_TOGGLE, {}, "async_toggle"
        )

        return True

    async def async_reproduce_states(
        self,
        states: list[core.State],
        *,
        context: core.Context = None,
        reproduce_options: dict[str, typing.Any] = None,
    ):
        """Reproduce component states."""
        await asyncio.gather(
            *(self._async_reproduce_state(state, context=context) for state in states)
        )

    async def _async_reproduce_state(
        self,
        state: core.State,
        context: core.Context = None,
    ) -> None:
        """Reproduce input boolean states."""
        if (cur_state := self._shc.states.get(state.entity_id)) is None:
            _LOGGER.warning(f"Unable to find entity {state.entity_id}")
            return

        if state.state not in (core.Const.STATE_ON, core.Const.STATE_OFF):
            _LOGGER.warning(
                f"Invalid state specified for {state.entity_id}: {state.state}"
            )
            return

        if cur_state.state == state.state:
            return

        service = (
            core.Const.SERVICE_TURN_ON
            if state.state == core.Const.STATE_ON
            else core.Const.SERVICE_TURN_OFF
        )

        await self._shc.services.async_call(
            self.domain,
            service,
            {core.Const.ATTR_ENTITY_ID: state.entity_id},
            context=context,
            blocking=True,
        )
