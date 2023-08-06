"""
Conversation Component for Smart Home - The Next Generation.

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

import logging
import typing

import voluptuous as vol

from ... import core
from .conversation_process_view import ConversationProcessView
from .default_agent import DefaultAgent

_cv: typing.TypeAlias = core.ConfigValidation
_conversation: typing.TypeAlias = core.Conversation
_intent: typing.TypeAlias = core.Intent
_websocket: typing.TypeAlias = core.WebSocket

_LOGGER: typing.Final = logging.getLogger(__name__)
_WS_PROCESS: typing.Final = {
    "type": "conversation/process",
    "text": str,
    vol.Optional("conversation_id"): str,
}
_WS_AGENT_INFO: typing.Final = {"type": "conversation/agent/info"}
_WS_ONBOARDING: typing.Final = {"type": "conversation/onboarding/set", "shown": bool}


# pylint: disable=unused-variable
class ConversationComponent(_conversation.Component):
    """Support for functionality to have conversations with Home Assistant."""

    def __init__(self, path: typing.Iterable[str]):
        super().__init__(path)
        self._agent: _conversation.AbstractAgent = None

    def set_agent(self, agent: _conversation.AbstractAgent):
        """Set the agent to handle the conversations."""
        self._agent = agent

    @property
    def config_schema(self) -> typing.Callable[[core.ConfigType], core.ConfigType]:
        return vol.Schema(
            {
                self.domain: vol.Schema(
                    {
                        vol.Optional("intents"): vol.Schema(
                            {_cv.string: vol.All(_cv.ensure_list, [_cv.string])}
                        )
                    }
                )
            },
            extra=vol.ALLOW_EXTRA,
        )

    async def async_setup(self, config: core.ConfigType) -> bool:
        """Register the process service."""
        websocket_api: core.WebSocket.Component = (
            self.controller.components.websocket_api
        )
        if not await super().async_setup(config) or not websocket_api:
            return False

        self.controller.services.async_register(
            self.domain,
            _conversation.SERVICE_PROCESS,
            self._handle_service,
            schema=_conversation.SERVICE_PROCESS_SCHEMA,
        )
        self.controller.register_view(ConversationProcessView(self))
        websocket_api.register_command(self._async_process, _WS_PROCESS)
        websocket_api.register_command(self._async_get_agent_info, _WS_AGENT_INFO)
        websocket_api.register_command(self._async_set_onboarding, _WS_ONBOARDING)

        return True

    async def _handle_service(self, service: core.ServiceCall) -> None:
        """Parse text into commands."""
        text = service.data[_conversation.ATTR_TEXT]
        _LOGGER.debug(f"Processing: <{text}>")
        agent = await self._async_get_agent()
        try:
            await agent.async_process(text, service.context)
        except _intent.IntentHandleError as err:
            _LOGGER.error(f"Error processing {text}: {err}")

    async def _async_get_agent(self) -> _conversation.AbstractAgent:
        """Return the agent (or create as new DefaultAgent)"""
        if self._agent is None:
            agent = self._agent = DefaultAgent(self)
            await agent.async_initialize(self._config)
        return self._agent

    async def _async_process(self, connection: _websocket.Connection, msg: dict):
        """Process text."""
        connection.send_result(
            msg["id"],
            await self._async_converse(
                msg["text"], msg.get("conversation_id"), connection.context(msg)
            ),
        )

    async def _async_get_agent_info(self, connection: _websocket.Connection, msg: dict):
        """Do we need onboarding."""
        agent = await self._async_get_agent()

        connection.send_result(
            msg["id"],
            {
                "onboarding": await agent.async_get_onboarding(),
                "attribution": agent.attribution,
            },
        )

    async def _async_set_onboarding(self, connection: _websocket.Connection, msg: dict):
        """Set onboarding status."""
        agent = await self._async_get_agent()

        success = await agent.async_set_onboarding(msg["shown"])

        if success:
            connection.send_result(msg["id"])
        else:
            connection.send_error(msg["id"])

    async def _async_converse(
        self, text: str, conversation_id: str, context: core.Context
    ) -> _intent.Response:
        """Process text and get intent."""
        agent = await self._async_get_agent()
        try:
            intent_result = await agent.async_process(text, context, conversation_id)
        except _intent.IntentHandleError as err:
            intent_result = _intent.Response()
            intent_result.async_set_speech(str(err))

        if intent_result is None:
            intent_result = _intent.Response()
            intent_result.async_set_speech("Sorry, I didn't understand that")

        return intent_result
