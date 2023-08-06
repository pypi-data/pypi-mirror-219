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

import logging
import typing

import voluptuous as vol

from ... import core
from .alexa_config import AlexaConfig
from .alexa_entity import _generate_alexa_id
from .alexa_flash_briefing_view import AlexaFlashBriefingView
from .alexa_intents_view import _HANDLERS, AlexaIntentsView
from .alexa_response import AlexaResponse
from .entity_wrapper import _ENTITY_ADAPTERS
from .smart_home_view import SmartHomeView
from .state_report import (
    async_send_changereport_message,
    async_send_doorbell_event_message,
)

_cv: typing.TypeAlias = core.ConfigValidation
_alexa: typing.TypeAlias = core.Alexa
_const: typing.TypeAlias = core.Const
_entity_filter: typing.TypeAlias = core.EntityFilter
_platform: typing.TypeAlias = core.Platform

_CONF_FLASH_BRIEFINGS: typing.Final = "flash_briefings"
_CONF_SMART_HOME: typing.Final = "smart_home"
_DEFAULT_LOCALE: typing.Final = "en-US"

_ALEXA_ENTITY_SCHEMA: typing.Final = vol.Schema(
    {
        vol.Optional(_const.CONF_DESCRIPTION): _cv.string,
        vol.Optional(_alexa.CONF_DISPLAY_CATEGORIES): _cv.string,
        vol.Optional(_const.CONF_NAME): _cv.string,
    }
)

_SMART_HOME_SCHEMA: typing.Final = vol.Schema(
    {
        vol.Optional(_alexa.CONF_ENDPOINT): _cv.string,
        vol.Optional(_const.CONF_CLIENT_ID): _cv.string,
        vol.Optional(_const.CONF_CLIENT_SECRET): _cv.string,
        vol.Optional(_alexa.CONF_LOCALE, default=_DEFAULT_LOCALE): vol.In(
            _alexa.CONF_SUPPORTED_LOCALES
        ),
        vol.Optional(
            _alexa.CONF_FILTER, default={}
        ): _entity_filter.Const.FILTER_SCHEMA,
        vol.Optional(_alexa.CONF_ENTITY_CONFIG): {_cv.entity_id: _ALEXA_ENTITY_SCHEMA},
    }
)

_LOGGER: typing.Final = logging.getLogger(__name__)


# pylint: disable=unused-variable
class AlexaIntegration(_alexa.Component, core.LogbookPlatform):
    """Support for Alexa skill service end point."""

    def __init__(self, path: typing.Iterable[str]):
        super().__init__(path)
        self._supported_platforms = frozenset([_platform.LOGBOOK])
        self._smart_home_view: SmartHomeView = None
        self._known_devices: dict[str, dict[str, str]] = {}

    @property
    def config_schema(self) -> typing.Callable[[core.ConfigType], core.ConfigType]:
        return vol.Schema(
            {
                self.domain: {
                    _CONF_FLASH_BRIEFINGS: {
                        vol.Required(_const.CONF_PASSWORD): _cv.string,
                        _cv.string: vol.All(
                            _cv.ensure_list,
                            [
                                {
                                    vol.Optional(_alexa.CONF_UID): _cv.string,
                                    vol.Required(_alexa.CONF_TITLE): _cv.template,
                                    vol.Optional(_alexa.CONF_AUDIO): _cv.template,
                                    vol.Required(
                                        _alexa.CONF_TEXT, default=""
                                    ): _cv.template,
                                    vol.Optional(_alexa.CONF_DISPLAY_URL): _cv.template,
                                }
                            ],
                        ),
                    },
                    # vol.Optional here would mean we couldn't distinguish between an empty
                    # smart_home: and none at all.
                    _CONF_SMART_HOME: vol.Any(_SMART_HOME_SCHEMA, None),
                }
            },
            extra=vol.ALLOW_EXTRA,
        )

    async def async_setup(self, config: core.ConfigType) -> bool:
        """Activate the Alexa integration."""
        if not await super().async_setup(config):
            return False
        if self._config is None:
            return True

        flash_briefings_config: core.ConfigType = self._config.get(
            _CONF_FLASH_BRIEFINGS, None
        )

        self.controller.register_view(AlexaIntentsView(self))

        if flash_briefings_config:
            self.controller.register_view(
                AlexaFlashBriefingView(self, flash_briefings_config)
            )

        smart_home_config = self._config.get(_CONF_SMART_HOME, _SMART_HOME_SCHEMA({}))

        # Activate Smart Home functionality of Alexa component.
        #
        # This is optional, triggered by having a `smart_home:` sub-section in the
        # alexa configuration.
        #
        # Even if that's disabled, the functionality in this module may still be used
        # by the cloud component which will call async_handle_message directly.

        alexa_config = AlexaConfig(self.controller, smart_home_config)
        await alexa_config.async_initialize()
        self._smart_home_view = SmartHomeView(self, alexa_config)
        self.controller.register_view(self._smart_home_view)

        if alexa_config.should_report_state:
            await self.async_enable_proactive_mode(alexa_config)

        return True

    async def async_enable_proactive_mode(self, config: core.Alexa.AbstractConfig):
        """Enable the proactive mode.

        Proactive mode makes this component report state changes to Alexa.
        """
        # Validate we can get access token.
        await config.async_get_access_token()

        @core.callback
        def extra_significant_check(  # pylint: disable=unused-argument
            old_state: str,
            old_attrs: dict,
            old_extra_arg: dict,
            new_state: str,
            new_attrs: dict,
            new_extra_arg: dict,
        ):
            """Check if the serialized data has changed."""
            return old_extra_arg is not None and old_extra_arg != new_extra_arg

        checker = await core.SignificantChange.create_checker(
            self.controller, self.domain, extra_significant_check
        )

        async def async_entity_state_listener(
            changed_entity: str,
            old_state: core.State,
            new_state: core.State,
        ):
            if not self.controller.is_running:
                return

            if not new_state:
                return

            if new_state.domain not in _ENTITY_ADAPTERS:
                return

            if not config.should_expose(changed_entity):
                _LOGGER.debug(
                    f"Not exposing {changed_entity} because filtered by config"
                )
                return

            alexa_changed_entity = _ENTITY_ADAPTERS[new_state.domain](
                self.controller, config, new_state
            )

            # Determine how entity should be reported on
            should_report = False
            should_doorbell = False

            for interface in alexa_changed_entity.interfaces:
                if not should_report and interface.properties_proactively_reported():
                    should_report = True

                if interface.name() == "Alexa.DoorbellEventSource":
                    should_doorbell = True
                    break

            if not should_report and not should_doorbell:
                return

            if should_doorbell:
                if new_state.state == _const.STATE_ON and (
                    old_state is None or old_state.state != _const.STATE_ON
                ):
                    await async_send_doorbell_event_message(
                        self.controller, config, alexa_changed_entity
                    )
                return

            alexa_properties = list(alexa_changed_entity.serialize_properties())

            if not checker.async_is_significant_change(
                new_state, extra_arg=alexa_properties
            ):
                return

            await async_send_changereport_message(
                self.controller,
                config,
                alexa_changed_entity,
                alexa_properties,
            )

        return self.controller.tracker.async_track_state_change(
            _const.MATCH_ALL, async_entity_state_listener
        )

    @core.callback
    def async_get_entities(self, config: _alexa.AbstractConfig) -> list[_alexa.Entity]:
        """Return all entities that are supported by Alexa."""
        entities = []
        for state in self.controller.states.async_all():
            if state.entity_id in _const.CLOUD_NEVER_EXPOSED_ENTITIES:
                continue

            if state.domain not in _ENTITY_ADAPTERS:
                continue

            alexa_entity = _ENTITY_ADAPTERS[state.domain](
                self.controller, config, state
            )

            if not list(alexa_entity.interfaces):
                continue

            entities.append(alexa_entity)

        return entities

    async def async_send_add_or_update_message(
        self, config: _alexa.AbstractConfig, entity_ids: list[str]
    ):
        """Send an AddOrUpdateReport message for entities.

        https://developer.amazon.com/docs/device-apis/alexa-discovery.html#add-or-update-report
        """
        token = await config.async_get_access_token()

        headers = {"Authorization": f"Bearer {token}"}

        endpoints = []

        for entity_id in entity_ids:
            if (domain := entity_id.split(".", 1)[0]) not in _ENTITY_ADAPTERS:
                continue

            if (state := self.controller.states.get(entity_id)) is None:
                continue

            alexa_entity = _ENTITY_ADAPTERS[domain](self.controller, config, state)
            endpoints.append(alexa_entity.serialize_discovery())

        payload = {
            "endpoints": endpoints,
            "scope": {"type": "BearerToken", "token": token},
        }

        message = AlexaResponse(
            name="AddOrUpdateReport", namespace="Alexa.Discovery", payload=payload
        )

        message_serialized = message.serialize()
        session = core.HttpClient.async_get_clientsession(self.controller)

        return await session.post(
            config.endpoint,
            headers=headers,
            json=message_serialized,
            allow_redirects=True,
        )

    async def async_send_delete_message(
        self, config: _alexa.AbstractConfig, entity_ids: list[str]
    ):
        """Send an DeleteReport message for entities.

        https://developer.amazon.com/docs/device-apis/alexa-discovery.html#deletereport-event
        """
        token = await config.async_get_access_token()

        headers = {"Authorization": f"Bearer {token}"}

        endpoints = []

        for entity_id in entity_ids:
            domain = entity_id.split(".", 1)[0]

            if domain not in _ENTITY_ADAPTERS:
                continue

            endpoints.append({"endpointId": _generate_alexa_id(entity_id)})

        payload = {
            "endpoints": endpoints,
            "scope": {"type": "BearerToken", "token": token},
        }

        message = AlexaResponse(
            name="DeleteReport", namespace="Alexa.Discovery", payload=payload
        )

        message_serialized = message.serialize()
        session = core.HttpClient.async_get_clientsession(self.controller)

        return await session.post(
            config.endpoint,
            headers=headers,
            json=message_serialized,
            allow_redirects=True,
        )

    async def async_handle_message(
        self,
        config: _alexa.AbstractConfig,
        request: dict,
        context: core.Context = None,
        enabled=True,
    ):
        """Handle incoming API messages.

        If enabled is False, the response to all messages will be a
        BRIDGE_UNREACHABLE error. This can be used if the API has been disabled in
        configuration.
        """
        return await self._smart_home_view.async_handle_message(
            self.controller, config, request, context, enabled
        )

    # ------------------------------- Logbook Platform -----------------------------

    def async_describe_events(self, async_describe_event: core.LogbookCallback) -> None:
        async_describe_event(_alexa.EVENT_ALEXA_SMART_HOME)

    def async_describe_event(self, event: core.LazyPartialState) -> dict[str, str]:
        """Describe a logbook event."""
        data = event.data

        if entity_id := data["request"].get("entity_id"):
            state = self.controller.states.get(entity_id)
            name = state.name if state else entity_id
            message = (
                f"sent command {data['request']['namespace']}/"
                + f"{data['request']['name']} for {name}"
            )
        else:
            message = (
                f"sent command {data['request']['namespace']}/{data['request']['name']}"
            )

        return {
            _const.LOGBOOK_ENTRY_NAME: "Amazon Alexa",
            _const.LOGBOOK_ENTRY_MESSAGE: message,
            _const.LOGBOOK_ENTRY_ENTITY_ID: entity_id,
        }

    def register_skill_handler(
        self,
        skill_id: str,
        handler: typing.Callable[
            [core.SmartHomeControllerComponent, _alexa.Intent],
            typing.Awaitable[_alexa.IntentResponse],
        ],
    ) -> None:
        """
        Register a handler for a Custom Skill of Alexa.

        skill_id has to be the Skill ID from the alexa developer console.
        all incoming messages for this skill are routed to that handler.

        ATTENTION: the handler has to use "async def ..." to work correctly.
        """
        if (
            skill_id is None
            or handler is None
            or not skill_id.startswith("amzn1.ask.skill.")
        ):
            return

        _HANDLERS[skill_id] = handler

    def register_skill_devices(
        self, skill_id: str, known_devices: dict[str, str]
    ) -> None:
        """
        associate devices to rooms.
        """
        if skill_id is not None and skill_id != "" and known_devices is not None:
            self._known_devices[skill_id] = known_devices

    def get_device_room(self, skill_id: str, device_id: str) -> str:
        """returns the associated room of a alexa device."""
        return self._known_devices.get(skill_id, {}).get(device_id)

    async def service_call(self, domain: str, service: str, *args, **kwargs):
        service_args = {}
        for keyword, typ, default in [
            (
                "context",
                [core.Context],
                None,
            ),
            ("blocking", [bool], None),
            ("limit", [float, int], None),
        ]:
            if keyword in kwargs and type(kwargs[keyword]) in typ:
                service_args[keyword] = kwargs.pop(keyword)
            elif default:
                service_args[keyword] = default

        if len(args) != 0:
            raise TypeError(f"service {domain}.{service} takes only keyword arguments")

        await self.controller.services.async_call(
            domain, service, kwargs, **service_args
        )
