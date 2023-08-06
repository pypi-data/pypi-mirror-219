"""
Amazon Alexa Integration for Smart Home - The Next Generation.

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
import http
import json
import logging
import typing

import aiohttp
import async_timeout

from ... import core
from .alexa_entity import AlexaEntity
from .alexa_response import AlexaResponse

_alexa: typing.TypeAlias = core.Alexa

_DEFAULT_TIMEOUT: typing.Final = 10
_LOGGER: typing.Final = logging.getLogger(__name__)

# pylint: disable=unused-variable


async def async_send_changereport_message(
    controller: core.SmartHomeController,
    config: _alexa.AbstractConfig,
    alexa_entity: AlexaEntity,
    alexa_properties,
    *,
    invalidate_access_token=True,
):
    """Send a ChangeReport message for an Alexa entity.

    https://developer.amazon.com/docs/smarthome/state-reporting-for-a-smart-home-skill.html#report-state-with-changereport-events
    """
    try:
        token = await config.async_get_access_token()
    except (_alexa.RequireRelink, _alexa.NoTokenAvailable):
        await config.set_authorized(False)
        _LOGGER.error(
            "Error when sending ChangeReport to Alexa, could not get access token"
        )
        return

    headers = {"Authorization": f"Bearer {token}"}

    endpoint = alexa_entity.alexa_id

    payload = {
        _alexa.API_CHANGE: {
            "cause": {"type": _alexa.Cause.APP_INTERACTION},
            "properties": alexa_properties,
        }
    }

    message = AlexaResponse(name="ChangeReport", namespace="Alexa", payload=payload)
    message.set_endpoint_full(token, endpoint)

    message_serialized = message.serialize()
    session = core.HttpClient.async_get_clientsession(controller)

    try:
        async with async_timeout.timeout(_DEFAULT_TIMEOUT):
            response = await session.post(
                config.endpoint,
                headers=headers,
                json=message_serialized,
                allow_redirects=True,
            )

    except (asyncio.TimeoutError, aiohttp.ClientError):
        _LOGGER.error(f"Timeout sending report to Alexa for {alexa_entity.entity_id}")
        return

    response_text = await response.text()

    _LOGGER.debug(f"Sent: {json.dumps(message_serialized)}")
    _LOGGER.debug(f"Received ({response.status}): {response_text}")

    if response.status == http.HTTPStatus.ACCEPTED:
        return

    response_json = json.loads(response_text)

    if response_json["payload"]["code"] == "INVALID_ACCESS_TOKEN_EXCEPTION":
        if invalidate_access_token:
            # Invalidate the access token and try again
            config.async_invalidate_access_token()
            return await async_send_changereport_message(
                controller,
                config,
                alexa_entity,
                alexa_properties,
                invalidate_access_token=False,
            )
        await config.set_authorized(False)

    _LOGGER.error(
        f"Error when sending ChangeReport for {alexa_entity.entity_id} to Alexa: "
        + f"{response_json['payload']['code']}: {response_json['payload']['description']}",
    )


async def async_send_doorbell_event_message(
    controller: core.SmartHomeController,
    config: _alexa.AbstractConfig,
    alexa_entity: AlexaEntity,
):
    """Send a DoorbellPress event message for an Alexa entity.

    https://developer.amazon.com/en-US/docs/alexa/device-apis/alexa-doorbelleventsource.html
    """
    token = await config.async_get_access_token()

    headers = {"Authorization": f"Bearer {token}"}

    endpoint = alexa_entity.alexa_id()

    message = AlexaResponse(
        name="DoorbellPress",
        namespace="Alexa.DoorbellEventSource",
        payload={
            "cause": {"type": _alexa.Cause.PHYSICAL_INTERACTION},
            "timestamp": core.helpers.utcnow().strftime(_alexa.DATE_FORMAT),
        },
    )

    message.set_endpoint_full(token, endpoint)

    message_serialized = message.serialize()
    session = core.HttpClient.async_get_clientsession(controller)

    try:
        async with async_timeout.timeout(_DEFAULT_TIMEOUT):
            response = await session.post(
                config.endpoint,
                headers=headers,
                json=message_serialized,
                allow_redirects=True,
            )

    except (asyncio.TimeoutError, aiohttp.ClientError):
        _LOGGER.error(f"Timeout sending report to Alexa for {alexa_entity.entity_id}")
        return

    response_text = await response.text()

    _LOGGER.debug(f"Sent: {json.dumps(message_serialized)}")
    _LOGGER.debug(f"Received ({response.status}): {response_text}")

    if response.status == http.HTTPStatus.ACCEPTED:
        return

    response_json = json.loads(response_text)

    _LOGGER.error(
        f"Error when sending DoorbellPress event for {alexa_entity.entity_id} to Alexa: "
        + f"{response_json['payload']['code']}: {response_json['payload']['description']}",
    )
