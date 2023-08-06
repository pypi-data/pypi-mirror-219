"""
Input Datetime Component for Smart Home - The Next Generation.

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
from .date_time_storage_collection import DateTimeStorageCollection
from .input_datetime import InputDatetime
from .utils import has_date_or_time

_cv: typing.TypeAlias = core.ConfigValidation

_LOGGER: typing.Final = logging.getLogger(__name__)


def _validate_set_datetime_attrs(config):
    """Validate set_datetime service attributes."""
    has_date_or_time_attr = any(
        key in config for key in (core.Const.ATTR_DATE, core.Const.ATTR_TIME)
    )
    if (
        sum(
            [
                has_date_or_time_attr,
                Const.ATTR_DATETIME in config,
                Const.ATTR_TIMESTAMP in config,
            ]
        )
        > 1
    ):
        raise vol.Invalid(f"Cannot use together: {', '.join(config.keys())}")
    return config


def _valid_initial(conf):
    """Check the initial value is valid."""
    if not (initial := conf.get(Const.CONF_INITIAL)):
        return conf

    if conf[Const.CONF_HAS_DATE] and conf[Const.CONF_HAS_TIME]:
        if core.helpers.parse_datetime(initial) is not None:
            return conf
        raise vol.Invalid(f"Initial value '{initial}' can't be parsed as a datetime")

    if conf[Const.CONF_HAS_DATE]:
        if core.helpers.parse_date(initial) is not None:
            return conf
        raise vol.Invalid(f"Initial value '{initial}' can't be parsed as a date")

    if core.helpers.parse_time(initial) is not None:
        return conf
    raise vol.Invalid(f"Initial value '{initial}' can't be parsed as a time")


# pylint: disable=unused-variable
class InputDatetimeComponent(
    core.SmartHomeControllerComponent,
    core.RecorderPlatform,
    core.ReproduceStatePlatform,
):
    """Support to select a date and/or a time."""

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

    async def async_setup(self, config: core.ConfigType) -> bool:
        """Set up an input datetime."""
        if not await super().async_setup(config):
            return False

        # pylint: disable=protected-access
        InputDatetime._domain = self.domain

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
            self._shc, self.domain, self.domain, component, InputDatetime.from_yaml
        )

        self._component = component
        self._yaml_collection = yaml_collection

        storage_collection = DateTimeStorageCollection(
            core.Store(self._shc, self.storage_version, self.storage_key),
            logging.getLogger(f"{__name__}.storage_collection"),
            id_manager,
        )
        storage_collection.sync_entity_lifecycle(
            self._shc, self.domain, self.domain, component, InputDatetime
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
            "set_datetime",
            vol.All(
                vol.Schema(
                    {
                        vol.Optional(core.Const.ATTR_DATE): _cv.date,
                        vol.Optional(core.Const.ATTR_TIME): _cv.time,
                        vol.Optional(Const.ATTR_DATETIME): _cv.datetime,
                        vol.Optional(Const.ATTR_TIMESTAMP): vol.Coerce(float),
                    },
                    extra=vol.ALLOW_EXTRA,
                ),
                _cv.has_at_least_one_key(
                    core.Const.ATTR_DATE,
                    core.Const.ATTR_TIME,
                    Const.ATTR_DATETIME,
                    Const.ATTR_TIMESTAMP,
                ),
                _validate_set_datetime_attrs,
            ),
            InputDatetime.async_set_datetime,
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

    async def async_validate_config(self, config: core.ConfigType) -> core.ConfigType:
        schema = vol.Schema(
            {
                self.domain: _cv.schema_with_slug_keys(
                    vol.All(
                        {
                            vol.Optional(core.Const.CONF_NAME): _cv.string,
                            vol.Optional(
                                Const.CONF_HAS_DATE, default=False
                            ): _cv.boolean,
                            vol.Optional(
                                Const.CONF_HAS_TIME, default=False
                            ): _cv.boolean,
                            vol.Optional(core.Const.CONF_ICON): _cv.icon,
                            vol.Optional(Const.CONF_INITIAL): _cv.string,
                        },
                        has_date_or_time,
                        _valid_initial,
                    )
                )
            },
            extra=vol.ALLOW_EXTRA,
        )
        return schema(config)

    def exclude_attributes(self) -> set[str]:
        """Exclude some attributes from being recorded in the database."""
        return {core.Const.ATTR_EDITABLE, Const.CONF_HAS_DATE, Const.CONF_HAS_TIME}

    async def async_reproduce_states(
        self,
        states: list[core.State],
        *,
        context: core.Context = None,
        reproduce_options: dict[str, typing.Any] = None,
    ):
        """Reproduce Input datetime states."""
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

        has_time = cur_state.attributes.get(Const.CONF_HAS_TIME)
        has_date = cur_state.attributes.get(Const.CONF_HAS_DATE)

        if not (
            (_is_valid_datetime(state.state) and has_date and has_time)
            or (_is_valid_date(state.state) and has_date and not has_time)
            or (_is_valid_time(state.state) and has_time and not has_date)
        ):
            _LOGGER.warning(
                f"Invalid state specified for {state.entity_id}: {state.state}"
            )
            return

        # Return if we are already at the right state.
        if cur_state.state == state.state:
            return

        service_data = {core.Const.ATTR_ENTITY_ID: state.entity_id}

        if has_time and has_date:
            service_data[Const.ATTR_DATETIME] = state.state
        elif has_time:
            service_data[core.Const.ATTR_TIME] = state.state
        elif has_date:
            service_data[core.Const.ATTR_DATE] = state.state

        await self._shc.services.async_call(
            self.domain, "set_datetime", service_data, context=context, blocking=True
        )


def _is_valid_datetime(string: str) -> bool:
    """Test if string dt is a valid datetime."""
    try:
        return core.helpers.parse_datetime(string) is not None
    except ValueError:
        return False


def _is_valid_date(string: str) -> bool:
    """Test if string dt is a valid date."""
    return core.helpers.parse_date(string) is not None


def _is_valid_time(string: str) -> bool:
    """Test if string dt is a valid time."""
    return core.helpers.parse_time(string) is not None
