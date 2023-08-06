"""
Core components of Smart Home - The Next Generation.

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

import abc
import typing

from .alexa_entity import AlexaEntity
from .callback import callback
from .context import Context
from .smart_home_controller_component import SmartHomeControllerComponent
from .alexa_intents import Intent, IntentResponse

if not typing.TYPE_CHECKING:

    class AbstractAlexaConfig:
        pass


if typing.TYPE_CHECKING:
    from .abstract_alexa_config import AbstractAlexaConfig


# pylint: disable=unused-variable
class AlexaComponent(SmartHomeControllerComponent):
    """Required base class for the Alexa Component."""

    @callback
    @abc.abstractmethod
    def async_get_entities(self, config: AbstractAlexaConfig) -> list[AlexaEntity]:
        """Return all entities that are supported by Alexa."""

    @abc.abstractmethod
    async def async_enable_proactive_mode(self, config: AbstractAlexaConfig):
        """Enable the proactive mode.

        Proactive mode makes this component report state changes to Alexa.
        """

    @abc.abstractmethod
    async def async_send_add_or_update_message(
        self, config: AbstractAlexaConfig, entity_ids: list[str]
    ):
        """Send an AddOrUpdateReport message for entities.

        https://developer.amazon.com/docs/device-apis/alexa-discovery.html#add-or-update-report
        """

    @abc.abstractmethod
    async def async_send_delete_message(
        self, config: AbstractAlexaConfig, entity_ids: list[str]
    ):
        """Send an DeleteReport message for entities.

        https://developer.amazon.com/docs/device-apis/alexa-discovery.html#deletereport-event
        """

    @abc.abstractmethod
    async def async_handle_message(
        self,
        config: AbstractAlexaConfig,
        request: dict,
        context: Context = None,
        enabled=True,
    ):
        """Handle incoming API messages.

        If enabled is False, the response to all messages will be a
        BRIDGE_UNREACHABLE error. This can be used if the API has been disabled in
        configuration.
        """

    @abc.abstractmethod
    def register_skill_handler(
        self,
        skill_id: str,
        handler: typing.Callable[
            [SmartHomeControllerComponent, Intent], typing.Awaitable[IntentResponse]
        ],
    ) -> None:
        """
        Register a handler for a Custom Skill of Alexa.

        skill_id has to be the Skill ID from the alexa developer console.
        all incoming messages for this skill are routed to that handler.

        ATTENTION: the handler has to use "async def ..." to work correctly.
        """

    @abc.abstractmethod
    def register_skill_devices(
        self, skill_id: str, known_devices: dict[str, str]
    ) -> None:
        """
        associate devices to rooms.
        """

    @abc.abstractmethod
    def get_device_room(self, skill_id: str, device_id: str) -> str:
        """returns the associated room of a alexa device."""

    @abc.abstractmethod
    async def service_call(self, domain: str, service: str, *args, **kwargs):
        """Helper to call a service like pyscript. (doesn't work with @pyscript_compile)"""
