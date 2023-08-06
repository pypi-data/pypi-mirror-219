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
import datetime as dt
import typing

import attr
import voluptuous as vol

from .config_validation import ConfigValidation as cv
from .const import Const
from .mqtt_service_info import ReceivePayloadType
from .platform import Platform
from .smart_home_controller_component import SmartHomeControllerComponent
from .template import Template

_ATTR_DISCOVERY_HASH: typing.Final = "discovery_hash"
_ATTR_DISCOVERY_PAYLOAD: typing.Final = "discovery_payload"
_ATTR_DISCOVERY_TOPIC: typing.Final = "discovery_topic"
_ATTR_PAYLOAD: typing.Final = "payload"
_ATTR_QOS: typing.Final = "qos"
_ATTR_RETAIN: typing.Final = "retain"
_ATTR_TOPIC: typing.Final = "topic"

_CONF_AVAILABILITY: typing.Final = "availability"
_CONF_BROKER: typing.Final = "broker"
_CONF_BIRTH_MESSAGE: typing.Final = "birth_message"
_CONF_COMMAND_TEMPLATE: typing.Final = "command_template"
_CONF_COMMAND_TOPIC: typing.Final = "command_topic"
_CONF_DISCOVERY_PREFIX: typing.Final = "discovery_prefix"
_CONF_ENCODING: typing.Final = "encoding"
_CONF_KEEPALIVE: typing.Final = "keepalive"
_CONF_PAYLOAD: typing.Final = Const.CONF_PAYLOAD
_CONF_QOS: typing.Final = _ATTR_QOS
_CONF_RETAIN: typing.Final = _ATTR_RETAIN
_CONF_STATE_TOPIC: typing.Final = "state_topic"
_CONF_STATE_VALUE_TEMPLATE: typing.Final = "state_value_template"
_CONF_TOPIC: typing.Final = "topic"
_CONF_WILL_MESSAGE: typing.Final = "will_message"

_CONF_CERTIFICATE: typing.Final = "certificate"
_CONF_CLIENT_KEY: typing.Final = "client_key"
_CONF_CLIENT_CERT: typing.Final = "client_cert"
_CONF_TLS_INSECURE: typing.Final = "tls_insecure"
_CONF_TLS_VERSION: typing.Final = "tls_version"

_CONFIG_ENTRY_IS_SETUP: typing.Final = "mqtt_config_entry_is_setup"
_DATA_MQTT: typing.Final = "mqtt"
_DATA_MQTT_CONFIG: typing.Final = "mqtt_config"
_MQTT_DATA_DEVICE_TRACKER_LEGACY: typing.Final = "mqtt_device_tracker_legacy"
_DATA_MQTT_RELOAD_DISPATCHERS: typing.Final = "mqtt_reload_dispatchers"
_DATA_MQTT_RELOAD_ENTRY: typing.Final = "mqtt_reload_entry"
_DATA_MQTT_RELOAD_NEEDED: typing.Final = "mqtt_reload_needed"
_DATA_MQTT_UPDATED_CONFIG: typing.Final = "mqtt_updated_config"

_DEFAULT_PREFIX: typing.Final = "homeassistant"
_DEFAULT_BIRTH_WILL_TOPIC: typing.Final = _DEFAULT_PREFIX + "/status"
_DEFAULT_DISCOVERY: typing.Final = True
_DEFAULT_ENCODING: typing.Final = "utf-8"
_DEFAULT_QOS: typing.Final = 0
_DEFAULT_PAYLOAD_AVAILABLE: typing.Final = "online"
_DEFAULT_PAYLOAD_NOT_AVAILABLE: typing.Final = "offline"
_DEFAULT_RETAIN: typing.Final = False

_DEFAULT_BIRTH: typing.Final = {
    _ATTR_TOPIC: _DEFAULT_BIRTH_WILL_TOPIC,
    _CONF_PAYLOAD: _DEFAULT_PAYLOAD_AVAILABLE,
    _ATTR_QOS: _DEFAULT_QOS,
    _ATTR_RETAIN: _DEFAULT_RETAIN,
}

_DEFAULT_WILL: typing.Final = {
    _ATTR_TOPIC: _DEFAULT_BIRTH_WILL_TOPIC,
    _CONF_PAYLOAD: _DEFAULT_PAYLOAD_NOT_AVAILABLE,
    _ATTR_QOS: _DEFAULT_QOS,
    _ATTR_RETAIN: _DEFAULT_RETAIN,
}

_MQTT_CONNECTED: typing.Final = "mqtt_connected"
_MQTT_DISCONNECTED: typing.Final = "mqtt_disconnected"

_PAYLOAD_EMPTY_JSON: typing.Final = "{}"
_PAYLOAD_NONE: typing.Final = "None"

_PROTOCOL_31: typing.Final = "3.1"
_PROTOCOL_311: typing.Final = "3.1.1"

_PLATFORMS: typing.Final = [
    Platform.ALARM_CONTROL_PANEL,
    Platform.BINARY_SENSOR,
    Platform.BUTTON,
    Platform.CAMERA,
    Platform.CLIMATE,
    Platform.DEVICE_TRACKER,
    Platform.COVER,
    Platform.FAN,
    Platform.HUMIDIFIER,
    Platform.LIGHT,
    Platform.LOCK,
    Platform.NUMBER,
    Platform.SELECT,
    Platform.SCENE,
    Platform.SENSOR,
    Platform.SIREN,
    Platform.SWITCH,
    Platform.VACUUM,
]

_RELOADABLE_PLATFORMS: typing.Final = [
    Platform.ALARM_CONTROL_PANEL,
    Platform.BINARY_SENSOR,
    Platform.BUTTON,
    Platform.CAMERA,
    Platform.CLIMATE,
    Platform.COVER,
    Platform.FAN,
    Platform.HUMIDIFIER,
    Platform.LIGHT,
    Platform.LOCK,
    Platform.NUMBER,
    Platform.SCENE,
    Platform.SELECT,
    Platform.SENSOR,
    Platform.SIREN,
    Platform.SWITCH,
    Platform.VACUUM,
]

_SERVICE_PUBLISH: typing.Final = "publish"
_SERVICE_DUMP: typing.Final = "dump"

_MANDATORY_DEFAULT_VALUES: typing.Final = (Const.CONF_PORT,)

_ATTR_TOPIC_TEMPLATE: typing.Final = "topic_template"
_ATTR_PAYLOAD_TEMPLATE: typing.Final = "payload_template"

_MAX_RECONNECT_WAIT: typing.Final = 300  # seconds

_CONNECTION_SUCCESS: typing.Final = "connection_success"
_CONNECTION_FAILED: typing.Final = "connection_failed"
_CONNECTION_FAILED_RECOVERABLE: typing.Final = "connection_failed_recoverable"

_CONFIG_ENTRY_CONFIG_KEYS: typing.Final = [
    _CONF_BIRTH_MESSAGE,
    _CONF_BROKER,
    Const.CONF_DISCOVERY,
    Const.CONF_PASSWORD,
    Const.CONF_PORT,
    Const.CONF_USERNAME,
    _CONF_WILL_MESSAGE,
]

_VALID_QOS_SCHEMA: typing.Final = vol.All(vol.Coerce(int), vol.In([0, 1, 2]))


def _valid_topic(value: typing.Any) -> str:
    """Validate that this is a valid topic name/filter."""
    value = cv.string(value)
    try:
        raw_value = value.encode("utf-8")
    except UnicodeError as err:
        raise vol.Invalid("MQTT topic name/filter must be valid UTF-8 string.") from err
    if not raw_value:
        raise vol.Invalid("MQTT topic name/filter must not be empty.")
    if len(raw_value) > 65535:
        raise vol.Invalid(
            "MQTT topic name/filter must not be longer than 65535 encoded bytes."
        )
    if "\0" in value:
        raise vol.Invalid("MQTT topic name/filter must not contain null character.")
    if any(char <= "\u001F" for char in value):
        raise vol.Invalid("MQTT topic name/filter must not contain control characters.")
    if any("\u007f" <= char <= "\u009F" for char in value):
        raise vol.Invalid("MQTT topic name/filter must not contain control characters.")
    if any("\ufdd0" <= char <= "\ufdef" for char in value):
        raise vol.Invalid("MQTT topic name/filter must not contain non-characters.")
    if any((ord(char) & 0xFFFF) in (0xFFFE, 0xFFFF) for char in value):
        raise vol.Invalid("MQTT topic name/filter must not contain noncharacters.")

    return value


def _valid_subscribe_topic(value: typing.Any) -> str:
    """Validate that we can subscribe using this MQTT topic."""
    value = _valid_topic(value)
    for i in (i for i, c in enumerate(value) if c == "+"):
        if (i > 0 and value[i - 1] != "/") or (
            i < len(value) - 1 and value[i + 1] != "/"
        ):
            raise vol.Invalid(
                "Single-level wildcard must occupy an entire level of the filter"
            )

    index = value.find("#")
    if index != -1:
        if index != len(value) - 1:
            # If there are multiple wildcards, this will also trigger
            raise vol.Invalid(
                "Multi-level wildcard must be the last "
                + "character in the topic filter."
            )
        if len(value) > 1 and value[index - 1] != "/":
            raise vol.Invalid(
                "Multi-level wildcard must be after a topic level separator."
            )

    return value


def _valid_subscribe_topic_template(value: typing.Any) -> Template:
    """Validate either a jinja2 template or a valid MQTT subscription topic."""
    tpl = Template(value)

    if tpl.is_static:
        _valid_subscribe_topic(value)

    return tpl


def _valid_publish_topic(value: typing.Any) -> str:
    """Validate that we can publish using this MQTT topic."""
    value = _valid_topic(value)
    if "+" in value or "#" in value:
        raise vol.Invalid("Wildcards can not be used in topic names")
    return value


_MQTT_WILL_BIRTH_SCHEMA: typing.Final = vol.Schema(
    {
        vol.Required(_ATTR_TOPIC): _valid_publish_topic,
        vol.Required(_ATTR_PAYLOAD, _CONF_PAYLOAD): cv.string,
        vol.Optional(_ATTR_QOS, default=_DEFAULT_QOS): _VALID_QOS_SCHEMA,
        vol.Optional(_ATTR_RETAIN, default=_DEFAULT_RETAIN): cv.boolean,
    },
    required=True,
)


# Service call validation schema
_MQTT_PUBLISH_SCHEMA: typing.Final = vol.All(
    vol.Schema(
        {
            vol.Exclusive(_ATTR_TOPIC, _CONF_TOPIC): _valid_publish_topic,
            vol.Exclusive(_ATTR_TOPIC_TEMPLATE, _CONF_TOPIC): cv.string,
            vol.Exclusive(_ATTR_PAYLOAD, _CONF_PAYLOAD): cv.string,
            vol.Exclusive(_ATTR_PAYLOAD_TEMPLATE, _CONF_PAYLOAD): cv.string,
            vol.Optional(_ATTR_QOS, default=_DEFAULT_QOS): _VALID_QOS_SCHEMA,
            vol.Optional(_ATTR_RETAIN, default=_DEFAULT_RETAIN): cv.boolean,
        },
        required=True,
    ),
    cv.has_at_least_one_key(_ATTR_TOPIC, _ATTR_TOPIC_TEMPLATE),
)


@attr.s(slots=True, frozen=True)
class _ReceiveMessage:
    """MQTT Message."""

    topic: str = attr.ib()
    payload: ReceivePayloadType = attr.ib()
    qos: int = attr.ib()
    retain: bool = attr.ib()
    subscribed_topic: str = attr.ib(default=None)
    timestamp: dt.datetime = attr.ib(default=None)


_AsyncMessageCallbackType = typing.Callable[
    [_ReceiveMessage], typing.Coroutine[typing.Any, typing.Any, None]
]
_MessageCallbackType = typing.Callable[[_ReceiveMessage], None]


class _Component(SmartHomeControllerComponent):
    """Required base class for MQTT component."""

    @abc.abstractmethod
    async def async_subscribe(
        self,
        topic: str,
        msg_callback: _AsyncMessageCallbackType | _MessageCallbackType,
        qos: int = _DEFAULT_QOS,
        encoding: str = "utf-8",
    ) -> typing.Callable[[], None]:
        """Subscribe to an MQTT topic.

        Call the return value to unsubscribe.
        """


# pylint: disable=unused-variable, invalid-name
class MQTT:
    """MQTT protocol namespace."""

    valid_topic: typing.Final = _valid_topic
    valid_subscribe_topic: typing.Final = _valid_subscribe_topic
    valid_subscribe_topic_template: typing.Final = _valid_subscribe_topic_template
    valid_publish_topic: typing.Final = _valid_publish_topic

    Component: typing.TypeAlias = _Component

    ATTR_DISCOVERY_HASH: typing.Final = _ATTR_DISCOVERY_HASH
    ATTR_DISCOVERY_PAYLOAD: typing.Final = _ATTR_DISCOVERY_PAYLOAD
    ATTR_DISCOVERY_TOPIC: typing.Final = _ATTR_DISCOVERY_TOPIC
    ATTR_PAYLOAD: typing.Final = _ATTR_PAYLOAD
    ATTR_QOS: typing.Final = _ATTR_QOS
    ATTR_RETAIN: typing.Final = _ATTR_RETAIN
    ATTR_TOPIC: typing.Final = _ATTR_TOPIC

    CONF_AVAILABILITY: typing.Final = _CONF_AVAILABILITY
    CONF_BROKER: typing.Final = _CONF_BROKER
    CONF_BIRTH_MESSAGE: typing.Final = _CONF_BIRTH_MESSAGE
    CONF_COMMAND_TEMPLATE: typing.Final = _CONF_COMMAND_TEMPLATE
    CONF_COMMAND_TOPIC: typing.Final = _CONF_COMMAND_TOPIC
    CONF_DISCOVERY_PREFIX: typing.Final = _CONF_DISCOVERY_PREFIX
    CONF_ENCODING: typing.Final = _CONF_ENCODING
    CONF_KEEPALIVE: typing.Final = _CONF_KEEPALIVE
    CONF_PAYLOAD: typing.Final = _CONF_PAYLOAD
    CONF_QOS: typing.Final = _CONF_QOS
    CONF_RETAIN: typing.Final = _CONF_RETAIN
    CONF_STATE_TOPIC: typing.Final = _CONF_STATE_TOPIC
    CONF_STATE_VALUE_TEMPLATE: typing.Final = _CONF_STATE_VALUE_TEMPLATE
    CONF_TOPIC: typing.Final = _CONF_TOPIC
    CONF_WILL_MESSAGE: typing.Final = _CONF_WILL_MESSAGE

    CONF_CERTIFICATE: typing.Final = _CONF_CERTIFICATE
    CONF_CLIENT_KEY: typing.Final = _CONF_CLIENT_KEY
    CONF_CLIENT_CERT: typing.Final = _CONF_CLIENT_CERT
    CONF_TLS_INSECURE: typing.Final = _CONF_TLS_INSECURE
    CONF_TLS_VERSION: typing.Final = _CONF_TLS_VERSION

    CONFIG_ENTRY_IS_SETUP: typing.Final = _CONFIG_ENTRY_IS_SETUP
    DATA_MQTT: typing.Final = _DATA_MQTT
    DATA_MQTT_CONFIG: typing.Final = _DATA_MQTT_CONFIG
    MQTT_DATA_DEVICE_TRACKER_LEGACY: typing.Final = _MQTT_DATA_DEVICE_TRACKER_LEGACY
    DATA_MQTT_RELOAD_DISPATCHERS: typing.Final = _DATA_MQTT_RELOAD_DISPATCHERS
    DATA_MQTT_RELOAD_ENTRY: typing.Final = _DATA_MQTT_RELOAD_ENTRY
    DATA_MQTT_RELOAD_NEEDED: typing.Final = _DATA_MQTT_RELOAD_NEEDED
    DATA_MQTT_UPDATED_CONFIG: typing.Final = _DATA_MQTT_UPDATED_CONFIG

    DEFAULT_PREFIX: typing.Final = _DEFAULT_PREFIX
    DEFAULT_BIRTH_WILL_TOPIC: typing.Final = _DEFAULT_BIRTH_WILL_TOPIC
    DEFAULT_DISCOVERY: typing.Final = _DEFAULT_DISCOVERY
    DEFAULT_ENCODING: typing.Final = _DEFAULT_ENCODING
    DEFAULT_QOS: typing.Final = _DEFAULT_QOS
    DEFAULT_PAYLOAD_AVAILABLE: typing.Final = _DEFAULT_PAYLOAD_AVAILABLE
    DEFAULT_PAYLOAD_NOT_AVAILABLE: typing.Final = _DEFAULT_PAYLOAD_NOT_AVAILABLE
    DEFAULT_RETAIN: typing.Final = _DEFAULT_RETAIN

    DEFAULT_BIRTH: typing.Final = _DEFAULT_BIRTH

    DEFAULT_WILL: typing.Final = _DEFAULT_WILL

    MQTT_CONNECTED: typing.Final = _MQTT_CONNECTED
    MQTT_DISCONNECTED: typing.Final = _MQTT_DISCONNECTED

    PAYLOAD_EMPTY_JSON: typing.Final = _PAYLOAD_EMPTY_JSON
    PAYLOAD_NONE: typing.Final = _PAYLOAD_NONE

    PROTOCOL_31: typing.Final = _PROTOCOL_31
    PROTOCOL_311: typing.Final = _PROTOCOL_311

    PLATFORMS: typing.Final = _PLATFORMS

    RELOADABLE_PLATFORMS: typing.Final = _RELOADABLE_PLATFORMS

    SERVICE_PUBLISH: typing.Final = _SERVICE_PUBLISH
    SERVICE_DUMP: typing.Final = _SERVICE_DUMP

    MANDATORY_DEFAULT_VALUES: typing.Final = _MANDATORY_DEFAULT_VALUES

    ATTR_TOPIC_TEMPLATE: typing.Final = _ATTR_TOPIC_TEMPLATE
    ATTR_PAYLOAD_TEMPLATE: typing.Final = _ATTR_PAYLOAD_TEMPLATE

    MAX_RECONNECT_WAIT: typing.Final = _MAX_RECONNECT_WAIT

    CONNECTION_SUCCESS: typing.Final = _CONNECTION_SUCCESS
    CONNECTION_FAILED: typing.Final = _CONNECTION_FAILED
    CONNECTION_FAILED_RECOVERABLE: typing.Final = _CONNECTION_FAILED_RECOVERABLE

    CONFIG_ENTRY_CONFIG_KEYS: typing.Final = _CONFIG_ENTRY_CONFIG_KEYS

    VALID_QOS_SCHEMA: typing.Final = _VALID_QOS_SCHEMA

    MQTT_WILL_BIRTH_SCHEMA: typing.Final = _MQTT_WILL_BIRTH_SCHEMA

    MQTT_PUBLISH_SCHEMA: typing.Final = _MQTT_PUBLISH_SCHEMA
