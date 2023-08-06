"""
Timer Component for Smart Home - The Next Generation.

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
from .timer import Timer, _format_timedelta
from .timer_storage_collectiion import TimerStorageCollection

_cv: typing.TypeAlias = core.ConfigValidation
_timer: typing.TypeAlias = core.Timer

_LOGGER: typing.Final = logging.getLogger(__name__)
_VALID_STATES: typing.Final = {
    _timer.STATUS_IDLE,
    _timer.STATUS_ACTIVE,
    _timer.STATUS_PAUSED,
}


# pylint: disable=unused-variable
class TimerComponent(core.SmartHomeControllerComponent, core.ReproduceStatePlatform):
    """Support for Timers."""

    def __init__(self, path: typing.Iterable[str]):
        super().__init__(path)
        self._supported_platforms = frozenset([core.Platform.REPRODUCE_STATE])
        self._component: core.EntityComponent = None
        self._yaml_collection: core.YamlCollection = None
        # pylint: disable=protected-access
        Timer._domain = self.domain

    @property
    def entity_component(self) -> core.EntityComponent:
        return self._component

    async def async_validate_config(self, config: core.ConfigType) -> core.ConfigType:
        schema = vol.Schema(
            {
                self.domain: _cv.schema_with_slug_keys(
                    vol.All(
                        _none_to_empty_dict,
                        {
                            vol.Optional(core.Const.CONF_NAME): _cv.string,
                            vol.Optional(core.Const.CONF_ICON): _cv.icon,
                            vol.Optional(
                                _timer.CONF_DURATION, default=_timer.DEFAULT_DURATION
                            ): vol.All(_cv.time_period, _format_timedelta),
                            vol.Optional(
                                _timer.CONF_RESTORE, default=_timer.DEFAULT_RESTORE
                            ): _cv.boolean,
                        },
                    )
                )
            },
            extra=vol.ALLOW_EXTRA,
        )
        return schema(config)

    async def async_setup(self, config: core.ConfigType) -> bool:
        """Set up an input select."""
        if not await super().async_setup(config):
            return False

        component = core.EntityComponent(_LOGGER, self.domain, self._shc)
        id_manager = core.IDManager()

        yaml_collection = core.YamlCollection(
            logging.getLogger(f"{__name__}.yaml_collection"), id_manager
        )
        yaml_collection.sync_entity_lifecycle(
            self._shc,
            self.domain,
            self.domain,
            component,
            Timer.from_yaml,
        )

        storage_collection = TimerStorageCollection(
            core.Store(self._shc, self.storage_version, self.storage_key),
            logging.getLogger(f"{__name__}.storage_collection"),
            id_manager,
        )
        storage_collection.sync_entity_lifecycle(
            self._shc, self.domain, self.domain, component, Timer
        )

        self._component = component
        self._yaml_collection = yaml_collection

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
            _timer.CREATE_FIELDS,
            _timer.UPDATE_FIELDS,
        ).async_setup()

        core.Service.async_register_admin_service(
            self._shc,
            self.domain,
            core.Const.SERVICE_RELOAD,
            self._reload_service_handler,
            schema=_timer.RELOAD_SERVICE_SCHEMA,
        )
        component.async_register_entity_service(
            _timer.SERVICE_START,
            {
                vol.Optional(
                    _timer.ATTR_DURATION, default=_timer.DEFAULT_DURATION
                ): _cv.time_period
            },
            Timer.async_start,
        )
        component.async_register_entity_service(
            _timer.SERVICE_PAUSE, {}, Timer.async_pause
        )
        component.async_register_entity_service(
            _timer.SERVICE_CANCEL, {}, Timer.async_cancel
        )
        component.async_register_entity_service(
            _timer.SERVICE_FINISH, {}, Timer.async_finish
        )

        return True

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
        """Reproduce Timer states."""
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

        if state.state not in _VALID_STATES:
            _LOGGER.warning(
                f"Invalid state specified for {state.entity_id}: {state.state}"
            )
            return

        # Return if we are already at the right state.
        if cur_state.state == state.state and cur_state.attributes.get(
            _timer.ATTR_DURATION
        ) == state.attributes.get(_timer.ATTR_DURATION):
            return

        service_data = {core.Const.ATTR_ENTITY_ID: state.entity_id}

        if state.state == _timer.STATUS_ACTIVE:
            service = _timer.SERVICE_START
            if _timer.ATTR_DURATION in state.attributes:
                service_data[_timer.ATTR_DURATION] = state.attributes[
                    _timer.ATTR_DURATION
                ]
        elif state.state == _timer.STATUS_PAUSED:
            service = _timer.SERVICE_PAUSE
        elif state.state == _timer.STATUS_IDLE:
            service = _timer.SERVICE_CANCEL

        await self._shc.services.async_call(
            self.domain, service, service_data, context=context, blocking=True
        )


def _none_to_empty_dict(value):
    if value is None:
        return {}
    return value
