"""
Input Select Component for Smart Home - The Next Generation.

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
import collections.abc
import logging
import typing

import voluptuous as vol

from ... import core
from .const import Const
from .input_select import InputSelect
from .input_select_storage_collection import InputSelectStorageCollection
from .input_select_store import InputSelectStore
from .util import _cv_input_select

_cv: typing.TypeAlias = core.ConfigValidation

_LOGGER: typing.Final = logging.getLogger(__name__)
_ATTR_GROUP: typing.Final = [core.Select.ATTR_OPTION, core.Select.ATTR_OPTIONS]


def _check_attr_equal(
    attr1: collections.abc.Mapping, attr2: collections.abc.Mapping, attr_str: str
) -> bool:
    """Return true if the given attributes are equal."""
    return attr1.get(attr_str) == attr2.get(attr_str)


# pylint: disable=unused-variable
class InputSelectComponent(
    core.SmartHomeControllerComponent,
    core.RecorderPlatform,
    core.ReproduceStatePlatform,
):
    """Support to select an option from a list."""

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
        return {core.Const.ATTR_EDITABLE}

    @property
    def config_schema(self) -> typing.Callable[[core.ConfigType], core.ConfigType]:
        return vol.Schema(
            {
                self.domain: _cv.schema_with_slug_keys(
                    vol.All(
                        {
                            vol.Optional(core.Const.CONF_NAME): _cv.string,
                            vol.Required(Const.CONF_OPTIONS): vol.All(
                                _cv.ensure_list, vol.Length(min=1), [_cv.string]
                            ),
                            vol.Optional(Const.CONF_INITIAL): _cv.string,
                            vol.Optional(core.Const.CONF_ICON): _cv.icon,
                        },
                        _cv_input_select,
                    )
                )
            },
            extra=vol.ALLOW_EXTRA,
        )

    async def async_setup(self, config: core.ConfigType) -> bool:
        """Set up an input select."""
        if not await super().async_setup(config):
            return False

        # pylint: disable=protected-access
        InputSelect._domain = self.domain

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
            self._shc, self.domain, self.domain, component, self._entity_from_config
        )
        self._component = component
        self._yaml_collection = yaml_collection

        storage_collection = InputSelectStorageCollection(
            InputSelectStore(
                self._shc,
                self.storage_version,
                self.storage_key,
                minor_version=Const.STORAGE_VERSION_MINOR,
            ),
            logging.getLogger(f"{__name__}.storage_collection"),
            id_manager,
        )
        storage_collection.sync_entity_lifecycle(
            self._shc, self.domain, self.domain, component, InputSelect
        )

        await yaml_collection.async_load(
            [
                {core.Const.CONF_ID: id_, **cfg}
                for id_, cfg in config.get(self.domain, {}).items()
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
            Const.SERVICE_SELECT_OPTION,
            {vol.Required(core.Select.ATTR_OPTION): _cv.string},
            "async_select_option",
        )

        component.async_register_entity_service(
            Const.SERVICE_SELECT_NEXT,
            {vol.Optional(Const.ATTR_CYCLE, default=True): bool},
            "async_next",
        )

        component.async_register_entity_service(
            Const.SERVICE_SELECT_PREVIOUS,
            {vol.Optional(Const.ATTR_CYCLE, default=True): bool},
            "async_previous",
        )

        component.async_register_entity_service(
            Const.SERVICE_SELECT_FIRST,
            {},
            core.callback(lambda entity, call: entity.async_select_index(0)),
        )

        component.async_register_entity_service(
            Const.SERVICE_SELECT_LAST,
            {},
            core.callback(lambda entity, call: entity.async_select_index(-1)),
        )

        component.async_register_entity_service(
            Const.SERVICE_SET_OPTIONS,
            {
                vol.Required(core.Select.ATTR_OPTIONS): vol.All(
                    _cv.ensure_list, vol.Length(min=1), [_cv.string]
                )
            },
            "async_set_options",
        )

        return True

    def _entity_from_config(self, config: core.ConfigType) -> InputSelect:
        return InputSelect(self, config, False)

    async def _reload_service_handler(self, _service_call: core.ServiceCall) -> None:
        """Reload yaml entities."""
        conf = await self._component.async_prepare_reload(skip_reset=True)
        if conf is None:
            conf = {self.domain: {}}
        await self._yaml_collection.async_load(
            [
                {core.Const.CONF_ID: id_, **cfg}
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
        """Reproduce Input select states."""
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
        # Return if we can't find entity
        if (cur_state := self._shc.states.get(state.entity_id)) is None:
            _LOGGER.warning(f"Unable to find entity {state.entity_id}")
            return

        # Return if we are already at the right state.
        if cur_state.state == state.state and all(
            _check_attr_equal(cur_state.attributes, state.attributes, attr)
            for attr in _ATTR_GROUP
        ):
            return

        # Set service data
        service_data = {core.Const.ATTR_ENTITY_ID: state.entity_id}

        # If options are specified, call SERVICE_SET_OPTIONS
        if core.Select.ATTR_OPTIONS in state.attributes:
            service = Const.SERVICE_SET_OPTIONS
            service_data[core.Select.ATTR_OPTIONS] = state.attributes[
                core.Select.ATTR_OPTIONS
            ]

            await self._shc.services.async_call(
                self.domain, service, service_data, context=context, blocking=True
            )

            # Remove ATTR_OPTIONS from service_data so we can reuse service_data in next call
            del service_data[core.Select.ATTR_OPTIONS]

        # Call SERVICE_SELECT_OPTION
        service = Const.SERVICE_SELECT_OPTION
        service_data[core.Select.ATTR_OPTION] = state.state

        await self._shc.services.async_call(
            self.domain, service, service_data, context=context, blocking=True
        )
