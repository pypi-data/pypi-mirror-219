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

import collections
import logging
import typing

import voluptuous as vol

from ... import core
from .google_assistant_flow import GoogleAssistantFlow
from .google_assistant_view import GoogleAssistantView
from .google_config import GoogleConfig
from .google_entity import GoogleEntity
from .google_errors import SmartHomeError
from .request_data import RequestData
from .smart_home import (
    _HANDLERS,
    _async_get_entities,
    create_sync_response,
    async_devices_sync_response,
)
from .sync_button import async_setup_buttons

_cv: typing.TypeAlias = core.ConfigValidation
_const: typing.TypeAlias = core.Const
_google: typing.TypeAlias = core.GoogleAssistant
_LOGGER: typing.Final = logging.getLogger(__name__)

# Seconds to wait to group states
_REPORT_STATE_WINDOW: typing.Final = 1
# Time to wait until the homegraph updates
# https://github.com/actions-on-google/smart-home-nodejs/issues/196#issuecomment-439156639
_INITIAL_REPORT_DELAY: typing.Final = 60

_CONF_ALLOW_UNLOCK: typing.Final = "allow_unlock"
_PLATFORMS: typing.Final = [core.Platform.BUTTON]
_ENTITY_SCHEMA: typing.Final = vol.Schema(
    {
        vol.Optional(core.Const.CONF_NAME): _cv.string,
        vol.Optional(core.GoogleAssistant.CONF_EXPOSE, default=True): _cv.boolean,
        vol.Optional(core.GoogleAssistant.CONF_ALIASES): vol.All(
            _cv.ensure_list, [_cv.string]
        ),
        vol.Optional(core.GoogleAssistant.CONF_ROOM_HINT): _cv.string,
    }
)
_GOOGLE_SERVICE_ACCOUNT: typing.Final = vol.Schema(
    {
        vol.Required(core.GoogleAssistant.CONF_PRIVATE_KEY): _cv.string,
        vol.Required(core.GoogleAssistant.CONF_CLIENT_EMAIL): _cv.string,
    },
    extra=vol.ALLOW_EXTRA,
)


def _check_report_state(data):
    if (
        data[core.GoogleAssistant.CONF_REPORT_STATE]
        and core.GoogleAssistant.CONF_SERVICE_ACCOUNT not in data
    ):
        raise vol.Invalid("If report state is enabled, a service account must exist")
    return data


_GOOGLE_ASSISTANT_SCHEMA: typing.Final = vol.All(
    vol.Schema(
        {
            vol.Required(core.GoogleAssistant.CONF_PROJECT_ID): _cv.string,
            vol.Optional(
                core.GoogleAssistant.CONF_EXPOSE_BY_DEFAULT,
                default=core.GoogleAssistant.DEFAULT_EXPOSE_BY_DEFAULT,
            ): _cv.boolean,
            vol.Optional(
                core.GoogleAssistant.CONF_EXPOSED_DOMAINS,
                default=core.GoogleAssistant.DEFAULT_EXPOSED_DOMAINS,
            ): _cv.ensure_list,
            vol.Optional(core.GoogleAssistant.CONF_ENTITY_CONFIG): {
                _cv.entity_id: _ENTITY_SCHEMA
            },
            # str on purpose, makes sure it is configured correctly.
            vol.Optional(core.GoogleAssistant.CONF_SECURE_DEVICES_PIN): str,
            vol.Optional(
                core.GoogleAssistant.CONF_REPORT_STATE, default=False
            ): _cv.boolean,
            vol.Optional(
                core.GoogleAssistant.CONF_SERVICE_ACCOUNT
            ): _GOOGLE_SERVICE_ACCOUNT,
            # deprecated configuration options
            vol.Remove(_CONF_ALLOW_UNLOCK): _cv.boolean,
            vol.Remove(core.Const.CONF_API_KEY): _cv.string,
        },
        extra=vol.PREVENT_EXTRA,
    ),
    _check_report_state,
)
_TO_REDACT: typing.Final = [
    "uuid",
    "baseUrl",
    "webhookId",
    _google.CONF_SERVICE_ACCOUNT,
    _google.CONF_SECURE_DEVICES_PIN,
    _const.CONF_API_KEY,
]
_COMMON_COMMAND_PREFIX: typing.Final = "action.devices.commands."


# pylint: disable=unused-variable
class GoogleAssistantIntegration(
    core.GoogleAssistant.Component,
    core.ConfigFlowPlatform,
    core.DiagnosticsPlatform,
    core.LogbookPlatform,
):
    """Support for Actions on Google Assistant Smart Home Control."""

    def __init__(self, path: typing.Iterable[str]):
        super().__init__(path)
        self._register_flow()
        self._configs: dict[str, GoogleConfig] = {}
        self._supported_platforms = frozenset(
            _PLATFORMS
            + [
                core.Platform.CONFIG_FLOW,
                core.Platform.DIAGNOSTICS,
                core.Platform.LOGBOOK,
            ]
        )

    @property
    def config_schema(self) -> typing.Callable[[core.ConfigType], core.ConfigType]:
        return vol.Schema(
            {vol.Optional(self.domain): _GOOGLE_ASSISTANT_SCHEMA}, extra=vol.ALLOW_EXTRA
        )

    @property
    def platform_schema(self) -> typing.Callable[[core.ConfigType], core.ConfigType]:
        return _cv.PLATFORM_SCHEMA

    @property
    def platform_schema_base(
        self,
    ) -> typing.Callable[[core.ConfigType], core.ConfigType]:
        return _cv.PLATFORM_SCHEMA_BASE

    async def async_setup(self, config: core.ConfigType) -> bool:
        """Activate Google Actions component."""
        if not await super().async_setup(config):
            return False
        if self.domain not in config:
            return True

        self.controller.async_create_task(
            self.controller.config_entries.flow.async_init(
                self.domain,
                context={"source": core.ConfigEntrySource.IMPORT},
                data={
                    core.GoogleAssistant.CONF_PROJECT_ID: self._config[
                        core.GoogleAssistant.CONF_PROJECT_ID
                    ]
                },
            )
        )

        return True

    async def async_setup_entry(self, entry: core.ConfigEntry) -> bool:
        """Set up from a config entry."""

        config = self._config

        if entry.source == core.ConfigEntrySource.IMPORT:
            # if project was changed, remove entry a new will be setup
            if (
                config[core.GoogleAssistant.CONF_PROJECT_ID]
                != entry.data[core.GoogleAssistant.CONF_PROJECT_ID]
            ):
                self.controller.async_create_task(
                    self.controller.config_entries.async_remove(entry.entry_id)
                )
                return False

        config.update(entry.data)

        device_registry = self.controller.device_registry
        device_registry.async_get_or_create(
            config_entry_id=entry.entry_id,
            identifiers={(self.domain, config[core.GoogleAssistant.CONF_PROJECT_ID])},
            manufacturer="Google",
            model="Google Assistant",
            name=config[core.GoogleAssistant.CONF_PROJECT_ID],
            entry_type=core.DeviceRegistryEntryType.SERVICE,
        )

        google_config = GoogleConfig(self, config)
        await google_config.async_initialize()

        self._configs[entry.entry_id] = google_config

        self.controller.http.register_view(GoogleAssistantView(self, google_config))

        if google_config.should_report_state:
            google_config.async_enable_report_state()

        async def request_sync_service_handler(call: core.ServiceCall) -> None:
            """Handle request sync service calls."""
            agent_user_id = call.data.get("agent_user_id") or call.context.user_id

            if agent_user_id is None:
                _LOGGER.warning(
                    "No agent_user_id supplied for request_sync. "
                    + "Call as a user or pass in user id as agent_user_id"
                )
                return

            await google_config.async_sync_entities(agent_user_id)

        # Register service only if key is provided
        if core.GoogleAssistant.CONF_SERVICE_ACCOUNT in config:
            self.controller.services.async_register(
                self.domain,
                core.GoogleAssistant.SERVICE_REQUEST_SYNC,
                request_sync_service_handler,
            )

        self.controller.config_entries.async_setup_platforms(entry, _PLATFORMS)

        return True

    async def async_setup_platform_devices(
        self, entry: core.ConfigEntry, async_add_entities: core.AddEntitiesCallback
    ) -> None:
        entity_platform = core.EntityPlatform.async_get_current_platform()
        platform = entity_platform.domain
        google_config = self._configs[entry.entry_id]
        if platform == core.Platform.BUTTON:
            await async_setup_buttons(
                entry, async_add_entities, self._config, google_config
            )

    def async_enable_report_state(
        self, google_config: core.GoogleAssistant.AbstractConfig
    ) -> core.CallbackType:
        """Enable state reporting."""
        checker = None
        unsub_pending: core.CallbackType = None
        pending: collections.deque[dict[str, typing.Any]] = collections.deque([{}])
        shc = self.controller

        async def report_states(_now=None):
            """Report the states."""
            nonlocal pending
            nonlocal unsub_pending

            pending.append({})

            # We will report all batches except last one because those are finalized.
            while len(pending) > 1:
                await google_config.async_report_state_all(
                    {"devices": {"states": pending.popleft()}}
                )

            # If things got queued up in last batch while we were reporting,
            # schedule ourselves again
            if pending[0]:
                unsub_pending = shc.tracker.async_call_later(
                    _REPORT_STATE_WINDOW, report_states_job
                )
            else:
                unsub_pending = None

        report_states_job = core.SmartHomeControllerJob(report_states)

        async def async_entity_state_listener(changed_entity, _old_state, new_state):
            nonlocal unsub_pending

            if not shc.is_running:
                return

            if not new_state:
                return

            if not google_config.should_expose(new_state):
                return

            entity = GoogleEntity(google_config, new_state)

            if not entity.is_supported():
                return

            try:
                entity_data = entity.query_serialize()
            except SmartHomeError as err:
                _LOGGER.debug(f"Not reporting state for {changed_entity}: {err.code}")
                return

            if not checker.async_is_significant_change(
                new_state, extra_arg=entity_data
            ):
                return

            _LOGGER.debug(
                f"Scheduling report state for {changed_entity}: {entity_data}"
            )

            # If a significant change is already scheduled and we have another significant one,
            # let's create a new batch of changes
            if changed_entity in pending[-1]:
                pending.append({})

            pending[-1][changed_entity] = entity_data

            if unsub_pending is None:
                unsub_pending = shc.tracker.async_call_later(
                    _REPORT_STATE_WINDOW, report_states_job
                )

        @core.callback
        def extra_significant_check(
            _old_state: str,
            _old_attrs: dict,
            old_extra_arg: dict,
            _new_state: str,
            _new_attrs: dict,
            new_extra_arg: dict,
        ):
            """Check if the serialized data has changed."""
            return old_extra_arg != new_extra_arg

        async def initial_report(_now):
            """Report initially all states."""
            nonlocal unsub, checker
            entities = {}

            checker = await core.SignificantChange.create_checker(
                self.controller, self.domain, extra_significant_check
            )

            for entity in _async_get_entities(shc, google_config):
                if not entity.should_expose():
                    continue

                try:
                    entity_data = entity.query_serialize()
                except SmartHomeError:
                    continue

                # Tell our significant change checker that we're reporting
                # So it knows with subsequent changes what was already reported.
                if not checker.async_is_significant_change(
                    entity.state, extra_arg=entity_data
                ):
                    continue

                entities[entity.entity_id] = entity_data

            if not entities:
                return

            await google_config.async_report_state_all(
                {"devices": {"states": entities}}
            )

            unsub = shc.tracker.async_track_state_change(
                core.Const.MATCH_ALL, async_entity_state_listener
            )

        unsub = shc.tracker.async_call_later(_INITIAL_REPORT_DELAY, initial_report)

        @core.callback
        def unsub_all():
            unsub()
            if unsub_pending:
                unsub_pending()  # pylint: disable=not-callable

        return unsub_all

    async def async_handle_message(
        self,
        config: core.GoogleAssistant.AbstractConfig,
        user_id: str,
        message: dict,
        source: str,
    ):
        """Handle incoming API messages."""
        data = RequestData(
            config, user_id, source, message["requestId"], message.get("devices")
        )

        response = await self._process(data, message)

        if response and "errorCode" in response["payload"]:
            _LOGGER.error(f"Error handling message {message}: {response['payload']}")

        return response

    async def _process(self, data: RequestData, message: dict):
        """Process a message."""
        inputs: list = message.get("inputs")

        if len(inputs) != 1:
            return {
                "requestId": data.request_id,
                "payload": {"errorCode": _google.ERR_PROTOCOL_ERROR},
            }

        if (handler := _HANDLERS.get(inputs[0].get("intent"))) is None:
            return {
                "requestId": data.request_id,
                "payload": {"errorCode": _google.ERR_PROTOCOL_ERROR},
            }

        try:
            result = await handler(self.controller, data, inputs[0].get("payload"))
        except SmartHomeError as err:
            return {"requestId": data.request_id, "payload": {"errorCode": err.code}}
        except Exception:  # pylint: disable=broad-except
            _LOGGER.exception("Unexpected error")
            return {
                "requestId": data.request_id,
                "payload": {"errorCode": _google.ERR_UNKNOWN_ERROR},
            }

        if result is None:
            return None

        return {"requestId": data.request_id, "payload": result}

    def api_disabled_response(self, message: dict, agent_user_id: str):
        """Return a device turned off response."""
        inputs: list = message.get("inputs")

        if inputs and inputs[0].get("intent") == "action.devices.SYNC":
            payload = create_sync_response(agent_user_id, [])
        else:
            payload = {"errorCode": "deviceTurnedOff"}

        return {
            "requestId": message.get("requestId"),
            "payload": payload,
        }

    def async_get_entities(
        self, config: _google.AbstractConfig
    ) -> list[_google.Entity]:
        return _async_get_entities(self.controller, config)

    # ---------------- ConfigFlow Platform -------------------------------

    def create_config_flow(
        self, context: dict, init_data: typing.Any
    ) -> core.ConfigFlow:
        return GoogleAssistantFlow(self, context, init_data)

    # ---------------- Diagnostics Platform -------------------------------

    async def async_get_config_entry_diagnostics(
        self, config_entry: core.ConfigEntry
    ) -> typing.Any:
        """Return diagnostic information."""
        config = self._configs[config_entry.entry_id]
        yaml_config = self._config
        devices = await async_devices_sync_response(
            self.controller, config, core.Diagnostics.REDACTED
        )
        sync = create_sync_response(core.Diagnostics.REDACTED, devices)

        return {
            "config_entry": core.Diagnostics.async_redact_data(
                config_entry.as_dict(), _TO_REDACT
            ),
            "yaml_config": core.Diagnostics.async_redact_data(yaml_config, _TO_REDACT),
            "sync": core.Diagnostics.async_redact_data(sync, _TO_REDACT),
        }

    # ----------------- Logbook Component ----------------------------------

    def async_describe_events(self, async_describe_event: core.LogbookCallback) -> None:
        async_describe_event(_google.EVENT_COMMAND_RECEIVED)

    def async_describe_event(self, event: core.LazyPartialState) -> dict[str, str]:
        """Describe a logbook event."""
        commands = []

        for command_payload in event.data["execution"]:
            command = command_payload["command"]
            if command.startswith(_COMMON_COMMAND_PREFIX):
                command = command[len(_COMMON_COMMAND_PREFIX) :]
            commands.append(command)

        message = f"sent command {', '.join(commands)}"
        if event.data["source"] != _google.SOURCE_CLOUD:
            message += f" (via {event.data['source']})"

        return {
            _const.LOGBOOK_ENTRY_NAME: "Google Assistant",
            _const.LOGBOOK_ENTRY_MESSAGE: message,
        }
