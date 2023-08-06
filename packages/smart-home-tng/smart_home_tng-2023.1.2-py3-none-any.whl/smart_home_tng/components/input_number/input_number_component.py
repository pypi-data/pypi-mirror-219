"""
Input Number Component for Smart Home - The Next Generation.

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
from .input_number import InputNumber
from .number_storage_collection import NumberStorageCollection
from .util import _cv_input_number

_cv: typing.TypeAlias = core.ConfigValidation
_input_number: typing.TypeAlias = core.InputNumber

_LOGGER: typing.Final = logging.getLogger(__name__)


# pylint: disable=unused-variable
class InputNumberComponent(
    core.SmartHomeControllerComponent,
    core.RecorderPlatform,
    core.ReproduceStatePlatform,
):
    """Support to set a numeric value from a slider or text box."""

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
            _input_number.ATTR_MAX,
            _input_number.ATTR_MIN,
            core.Const.ATTR_MODE,
            _input_number.ATTR_STEP,
        }

    async def async_validate_config(self, config: core.ConfigType) -> core.ConfigType:
        schema = vol.Schema(
            {
                self.domain: _cv.schema_with_slug_keys(
                    vol.All(
                        {
                            vol.Optional(core.Const.CONF_NAME): _cv.string,
                            vol.Required(_input_number.CONF_MIN): vol.Coerce(float),
                            vol.Required(_input_number.CONF_MAX): vol.Coerce(float),
                            vol.Optional(_input_number.CONF_INITIAL): vol.Coerce(float),
                            vol.Optional(_input_number.CONF_STEP, default=1): vol.All(
                                vol.Coerce(float), vol.Range(min=1e-9)
                            ),
                            vol.Optional(core.Const.CONF_ICON): _cv.icon,
                            vol.Optional(
                                core.Const.CONF_UNIT_OF_MEASUREMENT
                            ): _cv.string,
                            vol.Optional(
                                core.Const.CONF_MODE, default=_input_number.MODE_SLIDER
                            ): vol.In(
                                [_input_number.MODE_BOX, _input_number.MODE_SLIDER]
                            ),
                        },
                        _cv_input_number,
                    )
                )
            },
            extra=vol.ALLOW_EXTRA,
        )
        return schema(config)

    async def async_setup(self, config: core.ConfigType) -> bool:
        """Set up an input slider."""
        if not await super().async_setup(config):
            return False

        # pylint: disable=protected-access
        InputNumber._domain = self.domain

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
            self._shc, self.domain, self.domain, component, InputNumber.from_yaml
        )

        self._component = component
        self._yaml_collection = yaml_collection

        storage_collection = NumberStorageCollection(
            core.Store(self._shc, self.storage_version, self.storage_key),
            logging.getLogger(f"{__name__}.storage_collection"),
            id_manager,
        )
        storage_collection.sync_entity_lifecycle(
            self._shc, self.domain, self.domain, component, InputNumber
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
            _input_number.CREATE_FIELDS,
            _input_number.UPDATE_FIELDS,
        ).async_setup()

        core.Service.async_register_admin_service(
            self._shc,
            self.domain,
            core.Const.SERVICE_RELOAD,
            self._reload_service_handler,
            schema=_input_number.RELOAD_SERVICE_SCHEMA,
        )

        component.async_register_entity_service(
            _input_number.SERVICE_SET_VALUE,
            {vol.Required(_input_number.ATTR_VALUE): vol.Coerce(float)},
            InputNumber.async_set_value,
        )

        component.async_register_entity_service(
            _input_number.SERVICE_INCREMENT, {}, InputNumber.async_increment
        )

        component.async_register_entity_service(
            _input_number.SERVICE_DECREMENT, {}, InputNumber.async_decrement
        )

        return True

    async def _reload_service_handler(self, _service_call: core.ServiceCall) -> None:
        """Reload yaml entities."""
        conf = await self._component.async_prepare_reload(skip_reset=True)
        if conf is None:
            conf = {self.domain: {}}
        await self._yaml_collection.async_load(
            [
                {core.Const.CONF_ID: id_, **conf}
                for id_, conf in conf.get(self.domain, {}).items()
            ]
        )

    async def async_reproduce_states(
        self,
        states: list[core.State],
        *,
        context: core.Context = None,
        reproduce_options: dict[str, typing.Any] = None,
    ):
        """Reproduce Input number states."""
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
        if (cur_state := self._shc.states.get(state.entity_id)) is None:
            _LOGGER.warning(f"Unable to find entity {state.entity_id}")
            return

        try:
            float(state.state)
        except ValueError:
            _LOGGER.warning(
                f"Invalid state specified for {state.entity_id}: {state.state}"
            )
            return

        # Return if we are already at the right state.
        if cur_state.state == state.state:
            return

        service = _input_number.SERVICE_SET_VALUE
        service_data = {
            core.Const.ATTR_ENTITY_ID: state.entity_id,
            _input_number.ATTR_VALUE: state.state,
        }

        try:
            await self._shc.services.async_call(
                self.domain, service, service_data, context=context, blocking=True
            )
        except vol.Invalid as err:
            # If value out of range.
            _LOGGER.warning(f"Unable to reproduce state for {state.entity_id}: {err}")
