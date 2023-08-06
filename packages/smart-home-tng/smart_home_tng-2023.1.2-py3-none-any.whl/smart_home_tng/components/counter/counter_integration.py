"""
Counter Integration for Smart Home - The Next Generation.

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
from .counter import Counter
from .counter_storage_collection import CounterStorageCollection

_LOGGER: typing.Final = logging.getLogger(__name__)
_cv: typing.TypeAlias = core.ConfigValidation


# pylint: disable=unused-variable
class CounterIntegration(
    core.SmartHomeControllerComponent, core.ReproduceStatePlatform
):
    """Component to count within automations."""

    def __init__(self, path: typing.Iterable[str]):
        super().__init__(path)
        self._supported_platforms = frozenset([core.Platform.REPRODUCE_STATE])
        self._component: core.EntityComponent = None

    @property
    def entity_component(self) -> core.EntityComponent:
        return self._component

    async def async_setup(self, config: core.ConfigType) -> bool:
        """Set up the counters."""
        if not await super().async_setup(config):
            return False

        component = core.EntityComponent(_LOGGER, self.domain, self._shc)
        id_manager = core.IDManager()
        self._component = component

        yaml_collection = core.YamlCollection(
            logging.getLogger(f"{__name__}.yaml_collection"), id_manager
        )
        yaml_collection.sync_entity_lifecycle(
            self._shc, self.domain, self.domain, component, Counter.from_yaml
        )

        storage_collection = CounterStorageCollection(
            core.Store(self._shc, self.storage_version, self.storage_key),
            logging.getLogger(f"{__name__}.storage_collection"),
            id_manager,
        )
        storage_collection.sync_entity_lifecycle(
            self._shc, self.domain, self.domain, component, Counter
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

        component.async_register_entity_service(
            Const.SERVICE_INCREMENT, {}, Counter.async_increment
        )
        component.async_register_entity_service(
            Const.SERVICE_DECREMENT, {}, Counter.async_decrement
        )
        component.async_register_entity_service(
            Const.SERVICE_RESET, {}, Counter.async_reset
        )
        component.async_register_entity_service(
            Const.SERVICE_CONFIGURE,
            {
                vol.Optional(Const.ATTR_MINIMUM): vol.Any(None, vol.Coerce(int)),
                vol.Optional(Const.ATTR_MAXIMUM): vol.Any(None, vol.Coerce(int)),
                vol.Optional(Const.ATTR_STEP): _cv.positive_int,
                vol.Optional(Const.ATTR_INITIAL): _cv.positive_int,
                vol.Optional(Const.VALUE): _cv.positive_int,
            },
            Counter.async_configure,
        )
        return True

    async def async_validate_config(self, config: core.ConfigType) -> core.ConfigType:
        CONFIG_SCHEMA: typing.Final = vol.Schema(
            {
                self.domain: _cv.schema_with_slug_keys(
                    vol.All(
                        _none_to_empty_dict,
                        {
                            vol.Optional(core.Const.CONF_ICON): _cv.icon,
                            vol.Optional(
                                Const.CONF_INITIAL, default=Const.DEFAULT_INITIAL
                            ): _cv.positive_int,
                            vol.Optional(core.Const.CONF_NAME): _cv.string,
                            vol.Optional(
                                core.Const.CONF_MAXIMUM, default=None
                            ): vol.Any(None, vol.Coerce(int)),
                            vol.Optional(
                                core.Const.CONF_MINIMUM, default=None
                            ): vol.Any(None, vol.Coerce(int)),
                            vol.Optional(Const.CONF_RESTORE, default=True): _cv.boolean,
                            vol.Optional(
                                Const.CONF_STEP, default=Const.DEFAULT_STEP
                            ): _cv.positive_int,
                        },
                    )
                )
            },
            extra=vol.ALLOW_EXTRA,
        )
        return CONFIG_SCHEMA(config)

    async def async_reproduce_states(
        self,
        states: list[core.State],
        *,
        context: core.Context = None,
        reproduce_options: dict[str, typing.Any] = None,
    ):
        """Reproduce Counter states."""
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

        if not state.state.isdigit():
            _LOGGER.warning(
                f"Invalid state specified for {state.entity_id}: {state.state}"
            )
            return

        # Return if we are already at the right state.
        if (
            cur_state.state == state.state
            and cur_state.attributes.get(Const.ATTR_INITIAL)
            == state.attributes.get(Const.ATTR_INITIAL)
            and cur_state.attributes.get(Const.ATTR_MAXIMUM)
            == state.attributes.get(Const.ATTR_MAXIMUM)
            and cur_state.attributes.get(Const.ATTR_MINIMUM)
            == state.attributes.get(Const.ATTR_MINIMUM)
            and cur_state.attributes.get(Const.ATTR_STEP)
            == state.attributes.get(Const.ATTR_STEP)
        ):
            return

        service_data = {
            core.Const.ATTR_ENTITY_ID: state.entity_id,
            Const.VALUE: state.state,
        }
        service = Const.SERVICE_CONFIGURE
        if Const.ATTR_INITIAL in state.attributes:
            service_data[Const.ATTR_INITIAL] = state.attributes[Const.ATTR_INITIAL]
        if Const.ATTR_MAXIMUM in state.attributes:
            service_data[Const.ATTR_MAXIMUM] = state.attributes[Const.ATTR_MAXIMUM]
        if Const.ATTR_MINIMUM in state.attributes:
            service_data[Const.ATTR_MINIMUM] = state.attributes[Const.ATTR_MINIMUM]
        if Const.ATTR_STEP in state.attributes:
            service_data[Const.ATTR_STEP] = state.attributes[Const.ATTR_STEP]

        await self._shc.services.async_call(
            self.domain, service, service_data, context=context, blocking=True
        )


def _none_to_empty_dict(value):
    if value is None:
        return {}
    return value
