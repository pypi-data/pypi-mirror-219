"""
Web Socket Api Component for Smart Home - The Next Generation.

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
import contextvars
import datetime
import functools
import json
import logging
import typing

import voluptuous as vol

from ... import auth, core
from ...core import ConfigValidation as cv
from ...core.generated import supported_brands
from .active_connection import _ActiveConnection, _current_connection
from .helpers import _error_message
from .web_socket_api_view import WebSocketAPIView

_LOGGER: typing.Final = logging.getLogger(__name__)


_subscribe_allow_list: set[str] = {
    core.Const.EVENT_AREA_REGISTRY_UPDATED,
    core.Const.EVENT_COMPONENT_LOADED,
    core.Const.EVENT_CORE_CONFIG_UPDATE,
    core.Const.EVENT_DEVICE_REGISTRY_UPDATED,
    core.Const.EVENT_ENTITY_REGISTRY_UPDATED,
    core.Const.EVENT_SERVICE_REGISTERED,
    core.Const.EVENT_SERVICE_REMOVED,
    core.Const.EVENT_STATE_CHANGED,
    core.Const.EVENT_THEMES_UPDATED,
}

_CALL_SERVICE: typing.Final = {
    vol.Required("type"): "call_service",
    vol.Required("domain"): str,
    vol.Required("service"): str,
    vol.Optional("target"): cv.ENTITY_SERVICE_FIELDS,
    vol.Optional("service_data"): dict,
}
_ENTITY_SOURCE: typing.Final = {
    vol.Required("type"): "entity/source",
    vol.Optional("entity_id"): [cv.entity_id],
}
_FIRE_EVENT: typing.Final = {
    vol.Required("type"): "fire_event",
    vol.Required("event_type"): str,
    vol.Optional("event_data"): dict,
}
_INTEGRATION_SETUP_INFO: typing.Final = {vol.Required("type"): "integration/setup_info"}
_GET_CONFIG: typing.Final = {vol.Required("type"): "get_config"}
_GET_SERVICES: typing.Final = {vol.Required("type"): "get_services"}
_GET_STATES: typing.Final = {vol.Required("type"): "get_states"}
_MANIFEST_GET: typing.Final = {
    vol.Required("type"): "manifest/get",
    vol.Required("integration"): str,
}
_MANIFEST_LIST: typing.Final = {
    vol.Required("type"): "manifest/list",
    vol.Optional("integrations"): [str],
}
_PING: typing.Final = {vol.Required("type"): "ping"}
_RENDER_TEMPLATE: typing.Final = {
    vol.Required("type"): "render_template",
    vol.Required("template"): str,
    vol.Optional("entity_ids"): cv.entity_ids,
    vol.Optional("variables"): dict,
    vol.Optional("timeout"): vol.Coerce(float),
    vol.Optional("strict", default=False): bool,
}
_SUBSCRIBE_BOOTSTRAP_INTEGRATIONS: typing.Final = {
    vol.Required("type"): "subscribe_bootstrap_integrations",
}
_SUBSCRIBE_EVENTS: typing.Final = {
    vol.Required("type"): "subscribe_events",
    vol.Optional("event_type", default=core.Const.MATCH_ALL): str,
}
_UNSUBSCRIBE_EVENTS: typing.Final = {
    vol.Required("type"): "unsubscribe_events",
    vol.Required("subscription"): cv.positive_int,
}
_SUBSCRIBE_ENTITIES: typing.Final = {
    vol.Required("type"): "subscribe_entities",
    vol.Optional("entity_ids"): cv.entity_ids,
}
_EXECUTE_SCRIPT: typing.Final = {
    vol.Required("type"): "execute_script",
    vol.Required("sequence"): cv.SCRIPT_SCHEMA,
    vol.Optional("variables"): dict,
}
_SUBSCRIBE_TRIGGER: typing.Final = {
    vol.Required("type"): "subscribe_trigger",
    vol.Required("trigger"): cv.TRIGGER_SCHEMA,
    vol.Optional("variables"): dict,
}
_TEST_CONDITION: typing.Final = {
    vol.Required("type"): "test_condition",
    vol.Required("condition"): cv.CONDITION_SCHEMA,
    vol.Optional("variables"): dict,
}
_VALIDATE_CONFIG: typing.Final = {
    vol.Required("type"): "validate_config",
    vol.Optional("trigger"): cv.match_all,
    vol.Optional("condition"): cv.match_all,
    vol.Optional("action"): cv.match_all,
}
_SUPPORTED_BRANDS: typing.Final = {
    vol.Required("type"): "supported_brands",
}
_SUPPORTED_FEATURES: typing.Final = {
    vol.Required("type"): "supported_features",
    vol.Required("features"): {str: int},
}


# pylint: disable=unused-variable, invalid-name
class WebSocketAPI(core.WebSocket.Component):
    """Web Socket Api for Smart Home - The Next Generation."""

    Connection: typing.TypeAlias = _ActiveConnection

    def __init__(self, path: typing.Iterable[str]):
        super().__init__(path)
        self._handlers: dict[str, tuple[core.WebSocket.CommandHandler, vol.Schema]] = {}
        self._connection_counter = 0

    @property
    def current_connection(self) -> contextvars.ContextVar[core.WebSocket.Connection]:
        return _current_connection

    @property
    def open_connections(self) -> int:
        return self._connection_counter

    def connection_opened(self) -> None:
        self._connection_counter += 1
        self._shc.dispatcher.async_send(core.WebSocket.SIGNAL_CONNECTED)

    def connection_closed(self) -> None:
        if self._connection_counter > 0:
            self._connection_counter -= 1
        self._shc.dispatcher.async_send(core.WebSocket.SIGNAL_DISCONNECTED)

    def has_handler(self, msg_type: str) -> bool:
        return msg_type in self._handlers

    def get_handler(
        self, msg_type: str
    ) -> tuple[core.WebSocket.CommandHandler, vol.Schema]:
        return self._handlers.get(msg_type)

    async def async_setup(self, config: core.ConfigType) -> bool:
        """Initialize the websocket API."""
        # pylint: disable=no-member
        if not await super().async_setup(config):
            return False

        shc = self._shc
        shc.register_view(WebSocketAPIView(self))

        self.register_command(_handle_call_service, _CALL_SERVICE)
        self.register_command(_handle_entity_source, _ENTITY_SOURCE)
        self.register_command(_handle_fire_event, _FIRE_EVENT)
        self.register_command(_handle_get_config, _GET_CONFIG)
        self.register_command(_handle_get_services, _GET_SERVICES)
        self.register_command(_handle_get_states, _GET_STATES)
        self.register_command(_handle_manifest_get, _MANIFEST_GET)
        self.register_command(_handle_integration_setup_info, _INTEGRATION_SETUP_INFO)
        self.register_command(_handle_manifest_list, _MANIFEST_LIST)
        self.register_command(_handle_ping, _PING)
        self.register_command(_handle_render_template, _RENDER_TEMPLATE)
        self.register_command(
            _handle_subscribe_bootstrap_integrations,
            _SUBSCRIBE_BOOTSTRAP_INTEGRATIONS,
        )
        self.register_command(_handle_subscribe_events, _SUBSCRIBE_EVENTS)
        self.register_command(_handle_unsubscribe_events, _UNSUBSCRIBE_EVENTS)
        self.register_command(_handle_subscribe_entities, _SUBSCRIBE_ENTITIES)

        self.register_command(_handle_execute_script, _EXECUTE_SCRIPT)
        self.register_command(_handle_subscribe_trigger, _SUBSCRIBE_TRIGGER)
        self.register_command(_handle_test_condition, _TEST_CONDITION)
        self.register_command(_handle_validate_config, _VALIDATE_CONFIG)
        self.register_command(_handle_supported_brands, _SUPPORTED_BRANDS)
        self.register_command(_handle_supported_features, _SUPPORTED_FEATURES)
        return True

    def require_admin(self, connection: core.WebSocket.Connection) -> None:
        """Check admin and call function."""
        user = connection.user

        if user is None or not user.is_admin:
            raise core.Unauthorized()

    def register_command(
        self,
        command_or_handler: str
        | core.WebSocket.CommandHandler
        | core.WebSocket.AsyncCommandHandler,
        schema: vol.Schema | dict[vol.Marker, typing.Any],
        handler: core.WebSocket.CommandHandler
        | core.WebSocket.AsyncCommandHandler = None,
    ) -> None:
        """Register a websocket command."""
        # pylint: disable=protected-access
        if handler is None:
            handler = command_or_handler
            if isinstance(schema, dict):
                command = schema["type"]
            else:
                command = command_or_handler
        else:
            command = command_or_handler
        if not isinstance(schema, vol.Schema):
            schema = core.WebSocket.BASE_COMMAND_MESSAGE_SCHEMA.extend(schema)

        self._handlers[command] = (handler, schema)

    def result_message(
        self, iden: int, result: typing.Any = None
    ) -> dict[str, typing.Any]:
        """Return a success result message."""
        return {
            "id": iden,
            "type": core.WebSocket.TYPE_RESULT,
            "success": True,
            "result": result,
        }

    def error_message(
        self, iden: int, code: str, message: str
    ) -> dict[str, typing.Any]:
        """Return an error result message."""
        return _error_message(iden, code, message)

    def event_message(
        self, iden: core.JsonType | int, event: typing.Any
    ) -> dict[str, typing.Any]:
        """Return an event message."""
        return {"id": iden, "type": "event", "event": event}

    def cached_event_message(self, iden: int, event: core.Event) -> str:
        """Return an event message.

        Serialize to json once per message.

        Since we can have many clients connected that are
        all getting many of the same events (mostly state changed)
        we can avoid serializing the same data for each connection.
        """
        return _cached_event_message(self, event).replace(
            core.WebSocket.IDEN_JSON_TEMPLATE, str(iden), 1
        )

    def cached_state_diff_message(self, iden: int, event: core.Event) -> str:
        """Return an event message.

        Serialize to json once per message.

        Since we can have many clients connected that are
        all getting many of the same events (mostly state changed)
        we can avoid serializing the same data for each connection.
        """
        return _cached_state_diff_message(self, event).replace(
            core.WebSocket.IDEN_JSON_TEMPLATE, str(iden), 1
        )

    def compressed_state_dict_add(self, state: core.State) -> dict[str, typing.Any]:
        """Build a compressed dict of a state for adds.

        Omits the lu (last_updated) if it matches (lc) last_changed.

        Sends c (context) as a string if it only contains an id.
        """
        if state.context.parent_id is None and state.context.user_id is None:
            context: dict[str, typing.Any] | str = state.context.context_id
        else:
            context = state.context.as_dict()
        compressed_state: dict[str, typing.Any] = {
            core.WebSocket.COMPRESSED_STATE_STATE: state.state,
            core.WebSocket.COMPRESSED_STATE_ATTRIBUTES: state.attributes,
            core.WebSocket.COMPRESSED_STATE_CONTEXT: context,
            core.WebSocket.COMPRESSED_STATE_LAST_CHANGED: state.last_changed.timestamp(),
        }
        if state.last_changed != state.last_updated:
            compressed_state[
                core.WebSocket.COMPRESSED_STATE_LAST_UPDATED
            ] = state.last_updated.timestamp()
        return compressed_state

    def message_to_json(self, message: dict[str, typing.Any]) -> str:
        """Serialize a websocket message to json."""
        try:
            return core.Const.JSON_DUMP(message)
        except (ValueError, TypeError):
            # pylint: disable=unexpected-keyword-arg
            msg = core.helpers.format_unserializable_data(
                core.helpers.find_paths_unserializable_data(
                    message, dump=core.Const.JSON_DUMP
                )
            )
            _LOGGER.error(
                f"Unable to serialize to JSON. Bad data found at {msg}",
            )
            return core.Const.JSON_DUMP(
                _error_message(
                    message["id"],
                    core.WebSocket.ERR_UNKNOWN_ERROR,
                    "Invalid JSON in response",
                )
            )

    @staticmethod
    def _output_error(
        connection: core.WebSocket.Connection, iden: int, message_id: str, message: str
    ) -> bool:
        """Output error message."""
        connection.send_message(_error_message(iden, message_id, message))
        return False

    def check_user(
        self,
        connection: core.WebSocket.Connection,
        iden: int,
        only_owner: bool = False,
        only_system_user: bool = False,
        allow_system_user: bool = True,
        only_active_user: bool = True,
        only_inactive_user: bool = False,
    ) -> bool:
        """Check current user."""

        if only_owner and not connection.user.is_owner:
            return self._output_error(
                connection, iden, "only_owner", "Only allowed as owner"
            )

        if only_system_user and not connection.user.system_generated:
            return self._output_error(
                connection, iden, "only_system_user", "Only allowed as system user"
            )

        if not allow_system_user and connection.user.system_generated:
            return self._output_error(
                connection, iden, "not_system_user", "Not allowed as system user"
            )

        if only_active_user and not connection.user.is_active:
            return self._output_error(
                connection, iden, "only_active_user", "Only allowed as active user"
            )

        if only_inactive_user and connection.user.is_active:
            return self._output_error(
                connection, iden, "only_inactive_user", "Not allowed as active user"
            )

        return True

    # ------------------ Decorators --------------------------------

    @staticmethod
    def register_subscripable_event(event_type: str):
        if event_type not in _subscribe_allow_list:
            _subscribe_allow_list.add(event_type)

    @staticmethod
    def subscribe_allow_list() -> set[str]:
        return _subscribe_allow_list.copy()


@functools.lru_cache(maxsize=128)
def _cached_event_message(comp: core.WebSocket.Component, event: core.Event) -> str:
    """Cache and serialize the event to json.

    The IDEN_TEMPLATE is used which will be replaced
    with the actual iden in cached_event_message
    """
    return comp.message_to_json(comp.event_message(core.WebSocket.IDEN_TEMPLATE, event))


@functools.lru_cache(maxsize=128)
def _cached_state_diff_message(
    comp: core.WebSocket.Component, event: core.Event
) -> str:
    """Cache and serialize the event to json.

    The IDEN_TEMPLATE is used which will be replaced
    with the actual iden in cached_event_message
    """
    return comp.message_to_json(
        comp.event_message(core.WebSocket.IDEN_TEMPLATE, _state_diff_event(comp, event))
    )


def _state_diff_event(comp: core.WebSocket.Component, event: core.Event) -> dict:
    """Convert a state_changed event to the minimal version.

    State update example

    {
        "a": {entity_id: compressed_state,…}
        "c": {entity_id: diff,…}
        "r": [entity_id,…]
    }
    """
    if (event_new_state := event.data["new_state"]) is None:
        return {core.WebSocket.ENTITY_EVENT_REMOVE: [event.data["entity_id"]]}
    assert isinstance(event_new_state, core.State)
    if (event_old_state := event.data["old_state"]) is None:
        return {
            core.WebSocket.ENTITY_EVENT_ADD: {
                event_new_state.entity_id: comp.compressed_state_dict_add(
                    event_new_state
                )
            }
        }
    assert isinstance(event_old_state, core.State)
    return _state_diff(event_old_state, event_new_state)


def _state_diff(
    old_state: core.State, new_state: core.State
) -> dict[str, dict[str, dict[str, dict[str, str | list[str]]]]]:
    """Create a diff dict that can be used to overlay changes."""
    diff: dict = {core.WebSocket.STATE_DIFF_ADDITIONS: {}}
    additions = diff[core.WebSocket.STATE_DIFF_ADDITIONS]
    if old_state.state != new_state.state:
        additions[core.WebSocket.COMPRESSED_STATE_STATE] = new_state.state
    if old_state.last_changed != new_state.last_changed:
        additions[
            core.WebSocket.COMPRESSED_STATE_LAST_CHANGED
        ] = new_state.last_changed.timestamp()
    elif old_state.last_updated != new_state.last_updated:
        additions[
            core.WebSocket.COMPRESSED_STATE_LAST_UPDATED
        ] = new_state.last_updated.timestamp()
    if old_state.context.parent_id != new_state.context.parent_id:
        additions.setdefault(core.WebSocket.COMPRESSED_STATE_CONTEXT, {})[
            "parent_id"
        ] = new_state.context.parent_id
    if old_state.context.user_id != new_state.context.user_id:
        additions.setdefault(core.WebSocket.COMPRESSED_STATE_CONTEXT, {})[
            "user_id"
        ] = new_state.context.user_id
    if old_state.context.context_id != new_state.context.context_id:
        if core.WebSocket.COMPRESSED_STATE_CONTEXT in additions:
            additions[core.WebSocket.COMPRESSED_STATE_CONTEXT][
                "id"
            ] = new_state.context.context_id
        else:
            additions[
                core.WebSocket.COMPRESSED_STATE_CONTEXT
            ] = new_state.context.context_id
    old_attributes = old_state.attributes
    for key, value in new_state.attributes.items():
        if old_attributes.get(key) != value:
            additions.setdefault(core.WebSocket.COMPRESSED_STATE_ATTRIBUTES, {})[
                key
            ] = value
    if removed := set(old_attributes).difference(new_state.attributes):
        diff[core.WebSocket.STATE_DIFF_REMOVALS] = {
            core.WebSocket.COMPRESSED_STATE_ATTRIBUTES: removed
        }
    return {core.WebSocket.ENTITY_EVENT_CHANGE: {new_state.entity_id: diff}}


def _pong_message(iden: int) -> dict[str, typing.Any]:
    """Return a pong message."""
    return {"id": iden, "type": "pong"}


@core.callback
def _handle_subscribe_events(
    connection: core.WebSocket.Connection,
    msg: dict[str, typing.Any],
) -> None:
    """Handle subscribe events command."""

    owner = connection.owner
    event_type = msg["event_type"]
    if event_type in _FRONTEND_EVENT_TRANSLATIONS:
        event_type = _FRONTEND_EVENT_TRANSLATIONS[event_type]

    if not connection.user.is_admin and event_type not in _subscribe_allow_list:
        raise core.Unauthorized

    if event_type == core.Const.EVENT_STATE_CHANGED:

        @core.callback
        def forward_events(event: core.Event) -> None:
            """Forward state changed events to websocket."""
            if not connection.user.permissions.check_entity(
                event.data["entity_id"], auth.permissions.Const.POLICY_READ
            ):
                return

            connection.send_message(
                lambda: owner.cached_event_message(msg["id"], event)
            )

    else:

        @core.callback
        def forward_events(event: core.Event) -> None:
            """Forward events to websocket."""
            connection.send_message(
                lambda: owner.cached_event_message(msg["id"], event)
            )

    connection.subscriptions[msg["id"]] = owner.controller.bus.async_listen(
        event_type, forward_events, run_immediately=True
    )

    connection.send_result(msg["id"])


_FRONTEND_EVENT_TRANSLATIONS: typing.Final = dict[str, str](
    {
        "component_loaded": core.Const.EVENT_COMPONENT_LOADED,
        "core_config_updated": core.Const.EVENT_CORE_CONFIG_UPDATE,
        "service_registered": core.Const.EVENT_SERVICE_REGISTERED,
        "service_removed": core.Const.EVENT_SERVICE_REMOVED,
        "service_call": core.Const.EVENT_CALL_SERVICE,
        "panels_updated": "panels.updated",
        "state_changed": core.Const.EVENT_STATE_CHANGED,
        "themes_updated": "themes.updated",
        "persistent_notifications_updated": "persistent_notifications.updated",
        "repairs_issue_registry_updated": "repairs_issue_registry.updated",
        "lovelace_updated": "lovelace.updated",
        "area_registry_updated": core.Const.EVENT_AREA_REGISTRY_UPDATED,
        "device_registry_updated": core.Const.EVENT_DEVICE_REGISTRY_UPDATED,
        "entity_registry_updated": core.Const.EVENT_ENTITY_REGISTRY_UPDATED,
        "config_entry_discovered": core.ConfigEntry.EVENT_FLOW_DISCOVERED,
    }
)


@core.callback
def _handle_subscribe_bootstrap_integrations(
    connection: core.WebSocket.Connection,
    msg: dict[str, typing.Any],
) -> None:
    """Handle subscribe bootstrap integrations command."""
    shc = connection.owner.controller

    @core.callback
    def forward_bootstrap_integrations(message: dict[str, typing.Any]) -> None:
        """Forward bootstrap integrations to websocket."""
        connection.send_event_message(msg["id"], message)

    connection.subscriptions[msg["id"]] = shc.dispatcher.async_connect(
        core.Const.SIGNAL_BOOTSTRAP_INTEGRATONS, forward_bootstrap_integrations
    )

    connection.send_result(msg["id"])


@core.callback
def _handle_unsubscribe_events(
    connection: core.WebSocket.Connection,
    msg: dict[str, typing.Any],
) -> None:
    """Handle unsubscribe events command."""
    subscription = msg["subscription"]

    if subscription in connection.subscriptions:
        connection.subscriptions.pop(subscription)()
        connection.send_result(msg["id"])
    else:
        connection.send_error(
            msg["id"], core.WebSocket.ERR_NOT_FOUND, "Subscription not found."
        )


async def _handle_call_service(
    connection: core.WebSocket.Connection,
    msg: dict[str, typing.Any],
) -> None:
    """Handle call service command."""
    blocking = True
    # We do not support templates.
    target = msg.get("target")
    if core.Template.is_complex(target):
        raise vol.Invalid("Templates are not supported here")

    try:
        context = connection.context(msg)
        await connection.owner.controller.services.async_call(
            msg["domain"],
            msg["service"],
            msg.get("service_data"),
            blocking,
            context,
            target=target,
        )
        connection.send_result(msg["id"], {"context": context})
    except core.ServiceNotFound as err:
        if err.domain == msg["domain"] and err.service == msg["service"]:
            connection.send_error(
                msg["id"], core.WebSocket.ERR_NOT_FOUND, "Service not found."
            )
        else:
            connection.send_error(
                msg["id"],
                core.WebSocket.ERR_SMART_HOME_CONTROLLER_ERROR,
                str(err),
            )
    except vol.Invalid as err:
        connection.send_error(msg["id"], core.WebSocket.ERR_INVALID_FORMAT, str(err))
    except core.SmartHomeControllerError as err:
        connection.logger.exception(err)
        connection.send_error(
            msg["id"], core.WebSocket.ERR_SMART_HOME_CONTROLLER_ERROR, str(err)
        )
    except Exception as err:  # pylint: disable=broad-except
        connection.logger.exception(err)
        connection.send_error(msg["id"], core.WebSocket.ERR_UNKNOWN_ERROR, str(err))


@core.callback
def _async_get_allowed_states(
    connection: core.WebSocket.Connection,
) -> list[core.State]:
    shc = connection.owner.controller
    if connection.user.permissions.access_all_entities("read"):
        return shc.states.async_all()
    entity_perm = connection.user.permissions.check_entity
    return [
        state
        for state in shc.states.async_all()
        if entity_perm(state.entity_id, "read")
    ]


@core.callback
def _handle_get_states(
    connection: core.WebSocket.Connection,
    msg: dict[str, typing.Any],
) -> None:
    """Handle get states command."""
    states = _async_get_allowed_states(connection)

    # JSON serialize here so we can recover if it blows up due to the
    # state machine containing unserializable data. This command is required
    # to succeed for the UI to show.
    response = connection.owner.result_message(msg["id"], states)
    try:
        connection.send_message(core.Const.JSON_DUMP(response))
        return
    except (ValueError, TypeError):
        # pylint: disable=unexpected-keyword-arg
        data = core.helpers.format_unserializable_data(
            core.helpers.find_paths_unserializable_data(
                response, dump=core.Const.JSON_DUMP
            )
        )
        connection.logger.error(
            f"Unable to serialize to JSON. Bad data found at {data}"
        )
    del response

    # If we can't serialize, we'll filter out unserializable states
    serialized = []
    for state in states:
        try:
            serialized.append(core.Const.JSON_DUMP(state))
        except (ValueError, TypeError):
            # Error is already logged above
            pass

    # We now have partially serialized states. Craft some JSON.
    response2 = core.Const.JSON_DUMP(
        WebSocketAPI.result_message(msg["id"], ["TO_REPLACE"])
    )
    response2 = response2.replace('"TO_REPLACE"', ", ".join(serialized))
    connection.send_message(response2)


@core.callback
def _handle_subscribe_entities(
    connection: core.WebSocket.Connection,
    msg: dict[str, typing.Any],
) -> None:
    """Handle subscribe entities command."""
    entity_ids = set(msg.get("entity_ids", []))
    owner = connection.owner
    shc = owner.controller

    @core.callback
    def forward_entity_changes(event: core.Event) -> None:
        """Forward entity state changed events to websocket."""
        if not connection.user.permissions.check_entity(
            event.data["entity_id"], auth.permissions.Const.POLICY_READ
        ):
            return
        if entity_ids and event.data["entity_id"] not in entity_ids:
            return

        connection.send_message(
            lambda: owner.cached_state_diff_message(msg["id"], event)
        )

    # We must never await between sending the states and listening for
    # state changed events or we will introduce a race condition
    # where some states are missed
    states = _async_get_allowed_states(connection)
    connection.subscriptions[msg["id"]] = shc.bus.async_listen(
        core.Const.EVENT_STATE_CHANGED, forward_entity_changes, run_immediately=True
    )
    connection.send_result(msg["id"])
    data: dict[str, dict[str, dict]] = {
        core.WebSocket.ENTITY_EVENT_ADD: {
            state.entity_id: owner.compressed_state_dict_add(state)
            for state in states
            if not entity_ids or state.entity_id in entity_ids
        }
    }

    # JSON serialize here so we can recover if it blows up due to the
    # state machine containing unserializable data. This command is required
    # to succeed for the UI to show.
    response = owner.event_message(msg["id"], data)
    try:
        connection.send_message(core.Const.JSON_DUMP(response))
        return
    except (ValueError, TypeError):
        # pylint: disable=unexpected-keyword-arg
        invalid_data = core.helpers.format_unserializable_data(
            core.helpers.find_paths_unserializable_data(
                response, dump=core.Const.JSON_DUMP
            )
        )
        connection.logger.error(
            f"Unable to serialize to JSON. Bad data found at {invalid_data}",
        )
    del response

    add_entities = data[core.WebSocket.ENTITY_EVENT_ADD]
    cannot_serialize: list[str] = []
    for entity_id, state_dict in add_entities.items():
        try:
            core.Const.JSON_DUMP(state_dict)
        except (ValueError, TypeError):
            cannot_serialize.append(entity_id)

    for entity_id in cannot_serialize:
        del add_entities[entity_id]

    connection.send_message(
        core.Const.JSON_DUMP(connection.owner.event_message(msg["id"], data))
    )


async def _handle_get_services(
    connection: core.WebSocket.Connection,
    msg: dict[str, typing.Any],
) -> None:
    """Handle get services command."""
    descriptions = await core.Service.async_get_all_descriptions(
        connection.owner.controller
    )
    connection.send_result(msg["id"], descriptions)


@core.callback
def _handle_get_config(
    connection: core.WebSocket.Connection,
    msg: dict[str, typing.Any],
) -> None:
    """Handle get config command."""
    connection.send_result(msg["id"], connection.owner.controller.config.as_dict())


async def _handle_manifest_list(
    connection: core.WebSocket.Connection,
    msg: dict[str, typing.Any],
) -> None:
    """Handle integrations command."""
    shc = connection.owner.controller
    wanted_integrations = msg.get("integrations")
    if wanted_integrations is None:
        wanted_integrations = shc.setup.async_get_loaded_integrations()
    integrations = await asyncio.gather(
        *(shc.setup.async_get_integration(domain) for domain in wanted_integrations)
    )
    connection.send_result(
        msg["id"], [integration.manifest for integration in integrations]
    )


async def _handle_manifest_get(
    connection: core.WebSocket.Connection,
    msg: dict[str, typing.Any],
) -> None:
    """Handle integrations command."""
    try:
        integration = await connection.owner.controller.setup.async_get_integration(
            msg["integration"]
        )
        connection.send_result(msg["id"], integration.manifest)
    except core.IntegrationNotFound:
        connection.send_error(
            msg["id"], core.WebSocket.ERR_NOT_FOUND, "Integration not found"
        )


async def _handle_integration_setup_info(
    connection: core.WebSocket.Connection,
    msg: dict[str, typing.Any],
) -> None:
    """Handle integrations command."""
    shc = connection.owner.controller
    connection.send_result(
        msg["id"],
        [
            {"domain": integration, "seconds": timedelta.total_seconds()}
            for integration, timedelta in typing.cast(
                dict[str, datetime.timedelta], shc.data[shc.setup.DATA_SETUP_TIME]
            ).items()
        ],
    )


async def _handle_supported_brands(
    connection: core.WebSocket.Connection,
    msg: dict[str, typing.Any],
) -> None:
    """Handle supported brands command."""
    data = {}

    ints_or_excs = await connection.owner.controller.setup.async_get_integrations(
        supported_brands.HAS_SUPPORTED_BRANDS
    )
    for int_or_exc in ints_or_excs.values():
        if isinstance(int_or_exc, Exception):
            raise int_or_exc
        data[int_or_exc.domain] = int_or_exc.manifest["supported_brands"]
    connection.send_result(msg["id"], data)


async def _handle_supported_features(
    connection: core.WebSocket.Connection,
    msg: dict[str, typing.Any],
) -> None:
    """Handle setting supported features."""
    connection.supported_features = msg["features"]
    connection.send_result(msg["id"])


@core.callback
def _handle_ping(
    connection: core.WebSocket.Connection,
    msg: dict[str, typing.Any],
) -> None:
    """Handle ping command."""
    connection.send_message(_pong_message(msg["id"]))


async def _handle_render_template(
    connection: core.WebSocket.Connection,
    msg: dict[str, typing.Any],
) -> None:
    """Handle render_template command."""
    shc = connection.owner.controller
    template_str = msg["template"]
    template_obj = core.Template(template_str, shc)
    variables = msg.get("variables")
    timeout = msg.get("timeout")
    info = None

    if timeout:
        try:
            timed_out = await template_obj.async_render_will_timeout(
                timeout, variables, strict=msg["strict"]
            )
        except core.TemplateError as ex:
            connection.send_error(msg["id"], core.WebSocket.ERR_TEMPLATE_ERROR, str(ex))
            return

        if timed_out:
            connection.send_error(
                msg["id"],
                core.WebSocket.ERR_TEMPLATE_ERROR,
                f"Exceeded maximum execution time of {timeout}s",
            )
            return

    @core.callback
    def template_listener(
        _event: core.Event, updates: list[core.TrackTemplateResult]
    ) -> None:
        nonlocal info
        track_template_result = updates.pop()
        result = track_template_result.result
        if isinstance(result, core.TemplateError):
            connection.send_error(
                msg["id"], core.WebSocket.ERR_TEMPLATE_ERROR, str(result)
            )
            return

        connection.send_event_message(
            msg["id"], {"result": result, "listeners": info.listeners}
        )

    try:
        info = shc.tracker.async_track_template_result(
            [core.TrackTemplate(template_obj, variables)],
            template_listener,
            raise_on_template_error=True,
            strict=msg["strict"],
        )
    except core.TemplateError as ex:
        connection.send_error(msg["id"], core.WebSocket.ERR_TEMPLATE_ERROR, str(ex))
        return

    connection.subscriptions[msg["id"]] = info.async_remove

    connection.send_result(msg["id"])

    shc.call_soon_threadsafe(info.async_refresh)


@core.callback
def _handle_entity_source(
    connection: core.WebSocket.Connection,
    msg: dict[str, typing.Any],
) -> None:
    """Handle entity source command."""
    raw_sources = connection.owner.controller.entity_sources
    entity_perm = connection.user.permissions.check_entity

    if "entity_id" not in msg:
        if connection.user.permissions.access_all_entities("read"):
            sources = raw_sources
        else:
            sources = {
                entity_id: source
                for entity_id, source in raw_sources.items()
                if entity_perm(entity_id, "read")
            }

        connection.send_result(msg["id"], sources)
        return

    sources = {}

    for entity_id in msg["entity_id"]:
        if not entity_perm(entity_id, "read"):
            raise core.Unauthorized(
                context=connection.context(msg),
                permission=auth.permissions.Const.POLICY_READ,
                perm_category=auth.permissions.Const.CAT_ENTITIES,
            )

        if (source := raw_sources.get(entity_id)) is None:
            connection.send_error(
                msg["id"], core.WebSocket.ERR_NOT_FOUND, "Entity not found"
            )
            return

        sources[entity_id] = source

    connection.send_result(msg["id"], sources)


async def _handle_fire_event(
    connection: core.WebSocket.Connection,
    msg: dict[str, typing.Any],
) -> None:
    """Handle fire event command."""
    connection.require_admin()

    context = connection.context(msg)

    connection.owner.controller.bus.async_fire(
        msg["event_type"], msg.get("event_data"), context=context
    )
    connection.send_result(msg["id"], {"context": context})


async def _handle_execute_script(
    connection: core.WebSocket.Connection,
    msg: dict[str, typing.Any],
) -> None:
    """Handle execute script command."""
    connection.require_admin()

    owner = connection.owner
    shc = owner.controller
    context = connection.context(msg)
    script_obj = core.Scripts.Script(
        shc, msg["sequence"], f"{owner.domain} script", owner.domain
    )
    await script_obj.async_run(msg.get("variables"), context=context)
    connection.send_result(msg["id"], {"context": context})


async def _handle_subscribe_trigger(
    connection: core.WebSocket.Connection,
    msg: dict[str, typing.Any],
) -> None:
    """Handle subscribe trigger command."""
    connection.require_admin()

    owner = connection.owner
    shc = owner.controller
    trigger_config = await core.Scripts.async_validate_trigger_config(
        shc, msg["trigger"]
    )

    @core.callback
    def forward_triggers(
        variables: dict[str, typing.Any], context: core.Context = None
    ) -> None:
        """Forward events to websocket."""
        message = owner.event_message(
            msg["id"], {"variables": variables, "context": context}
        )
        connection.send_message(
            json.dumps(
                message,
                cls=core.ExtendedJsonEncoder,
                allow_nan=False,
                separators=(",", ":"),
            )
        )

    connection.subscriptions[msg["id"]] = (
        await core.Scripts.async_initialize_triggers(
            shc,
            trigger_config,
            forward_triggers,
            owner.domain,
            owner.domain,
            connection.logger.log,
            variables=msg.get("variables"),
        )
    ) or (
        # Some triggers won't return an unsub function. Since the caller expects
        # a subscription, we're going to fake one.
        lambda: None
    )
    connection.send_result(msg["id"])


async def _handle_test_condition(
    connection: core.WebSocket.Connection,
    msg: dict[str, typing.Any],
) -> None:
    """Handle test condition command."""
    connection.require_admin()

    shc = connection.owner.controller
    # Do static + dynamic validation of the condition
    config = cv.CONDITION_SCHEMA(msg["condition"])
    config = await core.ScriptCondition.async_validate_condition_config(shc, config)
    # Test the condition
    check_condition = await core.ScriptCondition.async_automation_condition_from_config(
        shc, config
    )
    connection.send_result(
        msg["id"], {"result": check_condition(shc, msg.get("variables"))}
    )


async def _handle_validate_config(
    connection: core.WebSocket.Connection,
    msg: dict[str, typing.Any],
) -> None:
    """Handle validate config command."""

    shc = connection.owner.controller

    result = {}

    actions: core.ActionPlatform = core.Scripts.get_action_protocol(shc)

    for key, schema, validator in (
        ("trigger", cv.TRIGGER_SCHEMA, core.Scripts.async_validate_trigger_config),
        (
            "condition",
            cv.CONDITION_SCHEMA,
            core.ScriptCondition.async_validate_automation_condition_config,
        ),
        ("action", cv.SCRIPT_SCHEMA, actions.async_validate_actions_config),
    ):
        if key not in msg:
            continue

        try:
            await validator(shc, schema(msg[key]))
        except vol.Invalid as err:
            result[key] = {"valid": False, "error": str(err)}
        else:
            result[key] = {"valid": True, "error": None}

    connection.send_result(msg["id"], result)
