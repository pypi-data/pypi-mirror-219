"""
Input Text Component for Smart Home - The Next Generation.

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
from .input_storage_collection import InputTextStorageCollection, _cv_input_text
from .input_text import InputText

_cv: typing.TypeAlias = core.ConfigValidation

_LOGGER: typing.Final = logging.getLogger(__name__)


# pylint: disable=unused-variable
class InputTextComponent(
    core.SmartHomeControllerComponent,
    core.RecorderPlatform,
    core.ReproduceStatePlatform,
):
    """Support to enter a value into a text box."""

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

    def exclude_attributes(self) -> set[str]:
        """Exclude editable hint from being recorded in the database."""
        return {
            core.Const.ATTR_EDITABLE,
            Const.ATTR_MAX,
            Const.ATTR_MIN,
            core.Const.ATTR_MODE,
            Const.ATTR_PATTERN,
        }

    async def async_validate_config(self, config: core.ConfigType) -> core.ConfigType:
        schema = vol.Schema(
            {
                self.domain: _cv.schema_with_slug_keys(
                    vol.All(
                        lambda value: value or {},
                        {
                            vol.Optional(core.Const.CONF_NAME): _cv.string,
                            vol.Optional(
                                Const.CONF_MIN, default=Const.CONF_MIN_VALUE
                            ): vol.Coerce(int),
                            vol.Optional(
                                Const.CONF_MAX, default=Const.CONF_MAX_VALUE
                            ): vol.Coerce(int),
                            vol.Optional(Const.CONF_INITIAL, ""): _cv.string,
                            vol.Optional(core.Const.CONF_ICON): _cv.icon,
                            vol.Optional(
                                core.Const.CONF_UNIT_OF_MEASUREMENT
                            ): _cv.string,
                            vol.Optional(Const.CONF_PATTERN): _cv.string,
                            vol.Optional(
                                core.Const.CONF_MODE, default=Const.MODE_TEXT
                            ): vol.In([Const.MODE_TEXT, Const.MODE_PASSWORD]),
                        },
                        _cv_input_text,
                    ),
                )
            },
            extra=vol.ALLOW_EXTRA,
        )
        return schema(config)

    async def async_setup(self, config: core.ConfigType) -> bool:
        """Set up an input text."""
        if not await super().async_setup(config):
            return False

        # pylint: disable=protected-access
        InputText._domain = self.domain

        component = core.EntityComponent(_LOGGER, self.domain, self._shc)

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
            self._shc, self.domain, self.domain, component, InputText.from_yaml
        )

        self._component = component
        self._yaml_collection = yaml_collection

        storage_collection = InputTextStorageCollection(
            core.Store(self._shc, self.storage_version, self.storage_key),
            logging.getLogger(f"{__name__}.storage_collection"),
            id_manager,
        )
        storage_collection.sync_entity_lifecycle(
            self._shc, self.domain, self.domain, component, InputText
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

        component.async_register_entity_service(
            Const.SERVICE_SET_VALUE,
            {vol.Required(Const.ATTR_VALUE): _cv.string},
            "async_set_value",
        )

        return True

    async def _reload_service_handler(self, _service_call: core.ServiceCall) -> None:
        """Reload yaml entities."""
        conf = await self._component.async_prepare_reload(skip_reset=True)
        if conf is None:
            conf = {self.domain: {}}
        await self._yaml_collection.async_load(
            [
                {core.Const.CONF_ID: id_, **(cfg or {})}
                for id_, cfg in conf.get(self.domain, {}).items()
            ]
        )

    async def async_reproduce_states(
        self,
        states: list[core.State],
        *,
        context: core.Context = None,
        reproduce_options: dict[str, typing.Any] = None,
    ):
        """Reproduce Input text states."""
        # Reproduce states in parallel.
        await asyncio.gather(
            *(self._async_reproduce_state(state, context=context) for state in states)
        )

    async def _async_reproduce_state(
        self,
        state: core.State,
        context: core.Context = None,
    ) -> None:
        """Reproduce a single state."""
        # Return if we can't find the entity
        if (cur_state := self._shc.states.get(state.entity_id)) is None:
            _LOGGER.warning(f"Unable to find entity {state.entity_id}", state.entity_id)
            return

        # Return if we are already at the right state.
        if cur_state.state == state.state:
            return

        # Call service
        service = Const.SERVICE_SET_VALUE
        service_data = {
            core.Const.ATTR_ENTITY_ID: state.entity_id,
            Const.ATTR_VALUE: state.state,
        }

        await self._shc.services.async_call(
            self.domain, service, service_data, context=context, blocking=True
        )
