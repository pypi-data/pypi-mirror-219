"""
Recorder Component for Smart Home - The Next Generation.

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

import datetime
import typing
import voluptuous as vol

from ... import core
from .const import Const
from . import task

_cv: typing.TypeAlias = core.ConfigValidation


if not typing.TYPE_CHECKING:

    class Recorder:
        ...


if typing.TYPE_CHECKING:
    from .recorder import Recorder


_SERVICE_PURGE: typing.Final = "purge"
_SERVICE_PURGE_ENTITIES: typing.Final = "purge_entities"
_SERVICE_ENABLE: typing.Final = "enable"
_SERVICE_DISABLE: typing.Final = "disable"

_SERVICE_PURGE_SCHEMA: typing.Final = vol.Schema(
    {
        vol.Optional(Const.ATTR_KEEP_DAYS): _cv.positive_int,
        vol.Optional(Const.ATTR_REPACK, default=False): _cv.boolean,
        vol.Optional(Const.ATTR_APPLY_FILTER, default=False): _cv.boolean,
    }
)

_ATTR_DOMAINS: typing.Final = "domains"
_ATTR_ENTITY_GLOBS: typing.Final = "entity_globs"

_SERVICE_PURGE_ENTITIES_SCHEMA: typing.Final = vol.Schema(
    {
        vol.Optional(_ATTR_DOMAINS, default=[]): vol.All(_cv.ensure_list, [_cv.string]),
        vol.Optional(_ATTR_ENTITY_GLOBS, default=[]): vol.All(
            _cv.ensure_list, [_cv.string]
        ),
    }
).extend(_cv.ENTITY_SERVICE_FIELDS)

_SERVICE_ENABLE_SCHEMA: typing.Final = vol.Schema({})
_SERVICE_DISABLE_SCHEMA: typing.Final = vol.Schema({})


@core.callback
def _async_register_purge_service(
    shc: core.SmartHomeController, instance: Recorder
) -> None:
    async def async_handle_purge_service(service: core.ServiceCall) -> None:
        """Handle calls to the purge service."""
        kwargs = service.data
        keep_days = kwargs.get(Const.ATTR_KEEP_DAYS, instance.keep_days)
        repack = typing.cast(bool, kwargs[Const.ATTR_REPACK])
        apply_filter = typing.cast(bool, kwargs[Const.ATTR_APPLY_FILTER])
        purge_before = core.helpers.utcnow() - datetime.timedelta(days=keep_days)
        instance.queue_task(task.PurgeTask(purge_before, repack, apply_filter))

    shc.services.async_register(
        instance.owner.domain,
        _SERVICE_PURGE,
        async_handle_purge_service,
        schema=_SERVICE_PURGE_SCHEMA,
    )


@core.callback
def _async_register_purge_entities_service(
    shc: core.SmartHomeController, instance: Recorder
) -> None:
    async def async_handle_purge_entities_service(service: core.ServiceCall) -> None:
        """Handle calls to the purge entities service."""
        entity_ids = await core.Service.async_extract_entity_ids(shc, service)
        domains = service.data.get(_ATTR_DOMAINS, [])
        entity_globs = service.data.get(_ATTR_ENTITY_GLOBS, [])
        entity_filter = core.EntityFilter.generate_filter(
            domains, list(entity_ids), [], [], entity_globs
        )
        instance.queue_task(task.PurgeEntitiesTask(entity_filter))

    shc.services.async_register(
        instance.owner.domain,
        _SERVICE_PURGE_ENTITIES,
        async_handle_purge_entities_service,
        schema=_SERVICE_PURGE_ENTITIES_SCHEMA,
    )


@core.callback
def _async_register_enable_service(
    shc: core.SmartHomeController, instance: Recorder
) -> None:
    async def async_handle_enable_service(_service: core.ServiceCall) -> None:
        instance.set_enable(True)

    shc.services.async_register(
        instance.owner.domain,
        _SERVICE_ENABLE,
        async_handle_enable_service,
        schema=_SERVICE_ENABLE_SCHEMA,
    )


@core.callback
def _async_register_disable_service(
    shc: core.SmartHomeController, instance: Recorder
) -> None:
    async def async_handle_disable_service(_service: core.ServiceCall) -> None:
        instance.set_enable(False)

    shc.services.async_register(
        instance.owner.domain,
        _SERVICE_DISABLE,
        async_handle_disable_service,
        schema=_SERVICE_DISABLE_SCHEMA,
    )


# pylint: disable=unused-variable
@core.callback
def async_register_services(shc: core.SmartHomeController, instance: Recorder) -> None:
    """Register recorder services."""
    _async_register_purge_service(shc, instance)
    _async_register_purge_entities_service(shc, instance)
    _async_register_enable_service(shc, instance)
    _async_register_disable_service(shc, instance)
