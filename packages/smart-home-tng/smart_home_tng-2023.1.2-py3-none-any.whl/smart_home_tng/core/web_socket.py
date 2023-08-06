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

import asyncio
import concurrent.futures
import typing

import voluptuous as vol

from .config_validation import ConfigValidation as _cv
from .web_socket_connection import WebSocketConnection
from .web_socket_component import WebSocketComponent
from .web_socket_command_handler import (
    WebSocketCommandHandler,
    AsyncWebSocketCommandHandler,
)

_URL: typing.Final = "/api/websocket"
_PENDING_MSG_PEAK: typing.Final = 512
_PENDING_MSG_PEAK_TIME: typing.Final = 5
_MAX_PENDING_MSG: typing.Final = 2048

_ERR_ID_REUSE: typing.Final = "id_reuse"
_ERR_INVALID_FORMAT: typing.Final = "invalid_format"
_ERR_NOT_FOUND: typing.Final = "not_found"
_ERR_NOT_SUPPORTED: typing.Final = "not_supported"
_ERR_SMART_HOME_CONTROLLER_ERROR: typing.Final = "smart_home_controller_error"
_ERR_UNKNOWN_COMMAND: typing.Final = "unknown_command"
_ERR_UNKNOWN_ERROR: typing.Final = "unknown_error"
_ERR_UNAUTHORIZED: typing.Final = "unauthorized"
_ERR_TIMEOUT: typing.Final = "timeout"
_ERR_TEMPLATE_ERROR: typing.Final = "template_error"

_TYPE_RESULT: typing.Final = "result"

# Define the possible errors that occur when connections are cancelled.
# Originally, this was just asyncio.CancelledError, but issue #9546 showed
# that futures.CancelledErrors can also occur in some situations.
_CANCELLATION_ERRORS: typing.Final = (
    asyncio.CancelledError,
    concurrent.futures.CancelledError,
)

# Event types
_SIGNAL_CONNECTED: typing.Final = "websocket_connected"
_SIGNAL_DISCONNECTED: typing.Final = "websocket_disconnected"

_COMPRESSED_STATE_STATE: typing.Final = "s"
_COMPRESSED_STATE_ATTRIBUTES: typing.Final = "a"
_COMPRESSED_STATE_CONTEXT: typing.Final = "c"
_COMPRESSED_STATE_LAST_CHANGED: typing.Final = "lc"
_COMPRESSED_STATE_LAST_UPDATED: typing.Final = "lu"

_FEATURE_COALESCE_MESSAGES: typing.Final = "coalesce_messages"

# Minimal requirements of a message
_MINIMAL_MESSAGE_SCHEMA: typing.Final = vol.Schema(
    {vol.Required("id"): _cv.positive_int, vol.Required("type"): _cv.string},
    extra=vol.ALLOW_EXTRA,
)

# Base schema to extend by message handlers
_BASE_COMMAND_MESSAGE_SCHEMA: typing.Final = vol.Schema(
    {vol.Required("id"): _cv.positive_int}
)

_IDEN_TEMPLATE: typing.Final = "__IDEN__"
_IDEN_JSON_TEMPLATE: typing.Final = '"__IDEN__"'

_STATE_DIFF_ADDITIONS: typing.Final = "+"
_STATE_DIFF_REMOVALS: typing.Final = "-"

_ENTITY_EVENT_ADD: typing.Final = "a"
_ENTITY_EVENT_REMOVE: typing.Final = "r"
_ENTITY_EVENT_CHANGE: typing.Final = "c"


# pylint: disable=unused-variable, invalid-name
class WebSocket:
    """WebSocket namespace."""

    URL: typing.Final = _URL
    PENDING_MSG_PEAK: typing.Final = _PENDING_MSG_PEAK
    PENDING_MSG_PEAK_TIME: typing.Final = _PENDING_MSG_PEAK_TIME
    MAX_PENDING_MSG: typing.Final = _MAX_PENDING_MSG

    ERR_ID_REUSE: typing.Final = _ERR_ID_REUSE
    ERR_INVALID_FORMAT: typing.Final = _ERR_INVALID_FORMAT
    ERR_NOT_FOUND: typing.Final = _ERR_NOT_FOUND
    ERR_NOT_SUPPORTED: typing.Final = _ERR_NOT_SUPPORTED
    ERR_SMART_HOME_CONTROLLER_ERROR: typing.Final = _ERR_SMART_HOME_CONTROLLER_ERROR
    ERR_UNKNOWN_COMMAND: typing.Final = _ERR_UNKNOWN_COMMAND
    ERR_UNKNOWN_ERROR: typing.Final = _ERR_UNKNOWN_ERROR
    ERR_UNAUTHORIZED: typing.Final = _ERR_UNAUTHORIZED
    ERR_TIMEOUT: typing.Final = _ERR_TIMEOUT
    ERR_TEMPLATE_ERROR: typing.Final = _ERR_TEMPLATE_ERROR

    TYPE_RESULT: typing.Final = _TYPE_RESULT

    # Define the possible errors that occur when connections are cancelled.
    # Originally, this was just asyncio.CancelledError, but issue #9546 showed
    # that futures.CancelledErrors can also occur in some situations.
    CANCELLATION_ERRORS: typing.Final = _CANCELLATION_ERRORS

    # Event types
    SIGNAL_CONNECTED: typing.Final = _SIGNAL_CONNECTED
    SIGNAL_DISCONNECTED: typing.Final = _SIGNAL_DISCONNECTED

    COMPRESSED_STATE_STATE: typing.Final = _COMPRESSED_STATE_STATE
    COMPRESSED_STATE_ATTRIBUTES: typing.Final = _COMPRESSED_STATE_ATTRIBUTES
    COMPRESSED_STATE_CONTEXT: typing.Final = _COMPRESSED_STATE_CONTEXT
    COMPRESSED_STATE_LAST_CHANGED: typing.Final = _COMPRESSED_STATE_LAST_CHANGED
    COMPRESSED_STATE_LAST_UPDATED: typing.Final = _COMPRESSED_STATE_LAST_UPDATED

    FEATURE_COALESCE_MESSAGES: typing.Final = _FEATURE_COALESCE_MESSAGES

    MINIMAL_MESSAGE_SCHEMA: typing.Final = _MINIMAL_MESSAGE_SCHEMA
    BASE_COMMAND_MESSAGE_SCHEMA: typing.Final = _BASE_COMMAND_MESSAGE_SCHEMA

    IDEN_TEMPLATE: typing.Final = _IDEN_TEMPLATE
    IDEN_JSON_TEMPLATE: typing.Final = _IDEN_JSON_TEMPLATE

    STATE_DIFF_ADDITIONS: typing.Final = _STATE_DIFF_ADDITIONS
    STATE_DIFF_REMOVALS: typing.Final = _STATE_DIFF_REMOVALS

    ENTITY_EVENT_ADD: typing.Final = _ENTITY_EVENT_ADD
    ENTITY_EVENT_REMOVE: typing.Final = _ENTITY_EVENT_REMOVE
    ENTITY_EVENT_CHANGE: typing.Final = _ENTITY_EVENT_CHANGE

    AsyncCommandHandler: typing.TypeAlias = AsyncWebSocketCommandHandler
    Component: typing.TypeAlias = WebSocketComponent
    CommandHandler: typing.TypeAlias = WebSocketCommandHandler
    Connection: typing.TypeAlias = WebSocketConnection
