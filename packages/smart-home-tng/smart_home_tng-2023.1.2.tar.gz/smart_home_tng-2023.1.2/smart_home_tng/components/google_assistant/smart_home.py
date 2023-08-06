"""
Google Assistant Integration  for Smart Home - The Next Generation.

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

# pylint: disable=unused-variable

import asyncio
import itertools
import logging
import typing

from ... import core
from .google_entity import GoogleEntity
from .google_errors import SmartHomeError
from .request_data import RequestData

_const: typing.TypeAlias = core.Const
_google: typing.TypeAlias = core.GoogleAssistant
_EXECUTE_LIMIT: typing.Final = 2  # Wait 2 seconds for execute to finish

_SmartHomeHandler: typing.TypeAlias = typing.Callable[
    [core.SmartHomeController, RequestData, typing.Any],
    typing.Awaitable[dict | None],
]
_HANDLERS: typing.Final = core.Registry[str, _SmartHomeHandler]()
_LOGGER: typing.Final = logging.getLogger(__name__)


async def async_devices_sync_response(
    shc: core.SmartHomeController, config: _google.AbstractConfig, agent_user_id: str
):
    """Generate the device serialization."""
    entities = _async_get_entities(shc, config)
    instance_uuid = await shc.async_get_instance_id()
    devices = []

    for entity in entities:
        if not entity.should_expose():
            continue

        try:
            devices.append(entity.sync_serialize(agent_user_id, instance_uuid))
        except Exception:  # pylint: disable=broad-except
            _LOGGER.exception(f"Error serializing {entity.entity_id}")

    return devices


@_HANDLERS.register("action.devices.SYNC")
async def async_devices_sync(
    shc: core.SmartHomeController, data: RequestData, _payload: typing.Any
):
    """Handle action.devices.SYNC request.

    https://developers.google.com/assistant/smarthome/develop/process-intents#SYNC
    """
    shc.bus.async_fire(
        _google.EVENT_SYNC_RECEIVED,
        {"request_id": data.request_id, "source": data.source},
        context=data.context,
    )

    agent_user_id = data.config.get_agent_user_id(data.context)
    await data.config.async_connect_agent_user(agent_user_id)

    devices = await async_devices_sync_response(shc, data.config, agent_user_id)
    response = create_sync_response(agent_user_id, devices)

    _LOGGER.debug(f"Syncing entities response: {response}")

    return response


@_HANDLERS.register("action.devices.QUERY")
async def async_devices_query(
    shc: core.SmartHomeController, data: RequestData, payload
):
    """Handle action.devices.QUERY request.

    https://developers.google.com/assistant/smarthome/develop/process-intents#QUERY
    """
    payload_devices = payload.get("devices", [])

    shc.bus.async_fire(
        _google.EVENT_QUERY_RECEIVED,
        {
            "request_id": data.request_id,
            _const.ATTR_ENTITY_ID: [device["id"] for device in payload_devices],
            "source": data.source,
        },
        context=data.context,
    )

    devices = {}
    for device in payload_devices:
        devid = device["id"]

        if not (state := shc.states.get(devid)):
            # If we can't find a state, the device is offline
            devices[devid] = {"online": False}
            continue

        entity = GoogleEntity(data.config, state)
        try:
            devices[devid] = entity.query_serialize()
        except Exception:  # pylint: disable=broad-except
            _LOGGER.exception(f"Unexpected error serializing query for {state}")
            devices[devid] = {"online": False}

    return {"devices": devices}


async def _entity_execute(entity: GoogleEntity, data: RequestData, executions):
    """Execute all commands for an entity.

    Returns a dict if a special result needs to be set.
    """
    for execution in executions:
        try:
            await entity.execute(data, execution)
        except SmartHomeError as err:
            return {
                "ids": [entity.entity_id],
                "status": "ERROR",
                **err.to_response(),
            }

    return None


@_HANDLERS.register("action.devices.EXECUTE")
async def handle_devices_execute(
    shc: core.SmartHomeController, data: RequestData, payload
):
    """Handle action.devices.EXECUTE request.

    https://developers.google.com/assistant/smarthome/develop/process-intents#EXECUTE
    """
    entities = {}
    executions = {}
    results = {}

    for command in payload["commands"]:
        shc.bus.async_fire(
            _google.EVENT_COMMAND_RECEIVED,
            {
                "request_id": data.request_id,
                _const.ATTR_ENTITY_ID: [device["id"] for device in command["devices"]],
                "execution": command["execution"],
                "source": data.source,
            },
            context=data.context,
        )

        for device, execution in itertools.product(
            command["devices"], command["execution"]
        ):
            entity_id = device["id"]

            # Happens if error occurred. Skip entity for further processing
            if entity_id in results:
                continue

            if entity_id in entities:
                executions[entity_id].append(execution)
                continue

            if (state := shc.states.get(entity_id)) is None:
                results[entity_id] = {
                    "ids": [entity_id],
                    "status": "ERROR",
                    "errorCode": _google.ERR_DEVICE_OFFLINE,
                }
                continue

            entities[entity_id] = GoogleEntity(data.config, state)
            executions[entity_id] = [execution]

    try:
        execute_results = await asyncio.wait_for(
            asyncio.shield(
                asyncio.gather(
                    *(
                        _entity_execute(entities[entity_id], data, execution)
                        for entity_id, execution in executions.items()
                    )
                )
            ),
            _EXECUTE_LIMIT,
        )
        for entity_id, result in zip(executions, execute_results):
            if result is not None:
                results[entity_id] = result
    except asyncio.TimeoutError:
        pass

    final_results = list(results.values())

    for entity in entities.values():
        if entity.entity_id in results:
            continue

        entity.async_update()

        final_results.append(
            {
                "ids": [entity.entity_id],
                "status": "SUCCESS",
                "states": entity.query_serialize(),
            }
        )

    return {"commands": final_results}


@_HANDLERS.register("action.devices.DISCONNECT")
async def async_devices_disconnect(
    _shc: core.SmartHomeController, data: RequestData, _payload
):
    """Handle action.devices.DISCONNECT request.

    https://developers.google.com/assistant/smarthome/develop/process-intents#DISCONNECT
    """
    assert data.context.user_id is not None
    await data.config.async_disconnect_agent_user(data.context.user_id)
    return None


@_HANDLERS.register("action.devices.IDENTIFY")
async def async_devices_identify(
    _shc: core.SmartHomeController, data: RequestData, _payload
):
    """Handle action.devices.IDENTIFY request.

    https://developers.google.com/assistant/smarthome/develop/local#implement_the_identify_handler
    """
    return {
        "device": {
            "id": data.config.get_agent_user_id(data.context),
            "isLocalOnly": True,
            "isProxy": True,
            "deviceInfo": {
                "hwVersion": "UNKNOWN_HW_VERSION",
                "manufacturer": "Home Assistant",
                "model": "Home Assistant",
                "swVersion": _const.__version__,
            },
        }
    }


@_HANDLERS.register("action.devices.REACHABLE_DEVICES")
async def async_devices_reachable(
    shc: core.SmartHomeController, data: RequestData, _payload
):
    """Handle action.devices.REACHABLE_DEVICES request.

    https://developers.google.com/assistant/smarthome/develop/local#implement_the_reachable_devices_handler_hub_integrations_only
    """
    google_ids = {dev["id"] for dev in (data.devices or [])}

    return {
        "devices": [
            entity.reachable_device_serialize()
            for entity in _async_get_entities(shc, data.config)
            if entity.entity_id in google_ids and entity.should_expose_local()
        ]
    }


@_HANDLERS.register("action.devices.PROXY_SELECTED")
async def async_devices_proxy_selected(
    _shc: core.SmartHomeController, _data: RequestData, _payload
):
    """Handle action.devices.PROXY_SELECTED request.

    When selected for local SDK.
    """
    return {}


def create_sync_response(agent_user_id: str, devices: list):
    """Return an empty sync response."""
    return {
        "agentUserId": agent_user_id,
        "devices": devices,
    }


@core.callback
def _async_get_entities(
    shc: core.SmartHomeController, config: core.GoogleAssistant.AbstractConfig
) -> list[GoogleEntity]:
    """Return all entities that are supported by Google."""
    entities = []
    for state in shc.states.async_all():
        if state.entity_id in core.Const.CLOUD_NEVER_EXPOSED_ENTITIES:
            continue

        entity = GoogleEntity(config, state)

        if entity.is_supported():
            entities.append(entity)

    return entities
