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
import asyncio
import datetime as dt
import http
import logging
import pprint
import typing

import awesomeversion as asv
from aiohttp import web

from . import helpers
from .binary_sensor import BinarySensor
from .callback import callback
from .callback_type import CallbackType
from .cover import Cover
from .humidifier import Humidifier
from .media_player import MediaPlayer
from .sensor import Sensor
from .smart_home_controller_component import SmartHomeControllerComponent
from .state import State
from .store import Store
from .switch import Switch
from .webhook_component import WebhookComponent

_LOGGER: typing.Final = logging.getLogger(__name__)
_STORE_GOOGLE_LOCAL_WEBHOOK_ID: typing.Final = "local_webhook_id"
_SYNC_DELAY: typing.Final = 15

_LOCAL_SDK_VERSION_HEADER: typing.Final = "HA-Cloud-Version"
_LOCAL_SDK_MIN_VERSION: typing.Final = asv.AwesomeVersion("2.1.5")


@typing.overload
class _AbstractConfig:
    pass


class _Entity(abc.ABC):
    """
    Adaptation of Entity expressed in Google's terms.

    Required base class for GoogeEntity of Google Assistant Component.
    """

    @property
    @abc.abstractmethod
    def entity_id(self) -> str:
        """Return entity ID."""


class _Component(SmartHomeControllerComponent):
    """Required base class for the Google Assistant Component."""

    @callback
    @abc.abstractmethod
    def async_enable_report_state(self, google_config: _AbstractConfig) -> CallbackType:
        """Enable state reporting."""

    @abc.abstractmethod
    def api_disabled_response(self, message: dict, agent_user_id: str):
        """Return a device turned off response."""

    @abc.abstractmethod
    async def async_handle_message(
        self,
        config: _AbstractConfig,
        user_id: str,
        message: dict,
        source: str,
    ):
        """Handle incoming API messages."""

    @callback
    @abc.abstractmethod
    def async_get_entities(self, config: _AbstractConfig) -> list[_Entity]:
        """Return all entities that are supported by Google."""


class _ConfigStore:
    """A configuration store for google assistant."""

    def __init__(self, owner: SmartHomeControllerComponent):
        """Initialize a configuration store."""
        self._owner = owner
        self._store = Store(owner.controller, owner.storage_version, owner.storage_key)
        self._data = None
        self._webhook: WebhookComponent = None

    @property
    def controller(self):
        return self._owner.controller

    async def async_initialize(self):
        """Finish initializing the ConfigStore."""
        comp = self.controller.components.webhook
        if isinstance(comp, WebhookComponent):
            self._webhook = comp

        should_save_data = False
        if (data := await self._store.async_load()) is None:
            # if the store is not found create an empty one
            # Note that the first request is always a cloud request,
            # and that will store the correct agent user id to be used for local requests
            data = {
                GoogleAssistant.STORE_AGENT_USER_IDS: {},
            }
            should_save_data = True

        for agent_user_id, agent_user_data in data[
            GoogleAssistant.STORE_AGENT_USER_IDS
        ].items():
            if GoogleAssistant.STORE_GOOGLE_LOCAL_WEBHOOK_ID not in agent_user_data:
                data[GoogleAssistant.STORE_AGENT_USER_IDS][agent_user_id] = {
                    **agent_user_data,
                    GoogleAssistant.STORE_GOOGLE_LOCAL_WEBHOOK_ID: (
                        self._webhook.async_generate_id()
                    ),
                }
                should_save_data = True

        if should_save_data:
            await self._store.async_save(data)

        self._data = data

    @property
    def agent_user_ids(self):
        """Return a list of connected agent user_ids."""
        return self._data[GoogleAssistant.STORE_AGENT_USER_IDS]

    @callback
    def add_agent_user_id(self, agent_user_id):
        """Add an agent user id to store."""
        if agent_user_id not in self._data[GoogleAssistant.STORE_AGENT_USER_IDS]:
            self._data[GoogleAssistant.STORE_AGENT_USER_IDS][agent_user_id] = {
                GoogleAssistant.STORE_GOOGLE_LOCAL_WEBHOOK_ID: self._webhook.async_generate_id(),
            }
            self._store.async_delay_save(lambda: self._data, 1.0)

    @callback
    def pop_agent_user_id(self, agent_user_id):
        """Remove agent user id from store."""
        if agent_user_id in self._data[GoogleAssistant.STORE_AGENT_USER_IDS]:
            self._data[GoogleAssistant.STORE_AGENT_USER_IDS].pop(agent_user_id, None)
            self._store.async_delay_save(lambda: self._data, 1.0)


class _AbstractConfig(abc.ABC):
    """Hold the configuration for Google Assistant."""

    _unsub_report_state = None

    def __init__(self, owner: _Component):
        """Initialize abstract config."""
        self._owner = owner
        self._store = None
        self._google_sync_unsub = {}
        self._local_sdk_active = False
        self._local_last_active: dt.datetime = None
        self._local_sdk_version_warn = False
        self._is_supported_cache: dict[str, tuple[int, bool]] = {}

    @property
    def controller(self):
        return self._owner.controller

    @property
    def is_supported_cache(self) -> dict[str, tuple[int, bool]]:
        return self._is_supported_cache

    async def async_initialize(self):
        """Perform async initialization of config."""
        self._store = _ConfigStore(self._owner)
        await self._store.async_initialize()

        if not self.enabled:
            return

        async def sync_google(_):
            """Sync entities to Google."""
            await self.async_sync_entities_all()

        self.controller.async_at_start(sync_google)

    @property
    def enabled(self):
        """Return if Google is enabled."""
        return False

    @property
    def entity_config(self):
        """Return entity config."""
        return {}

    @property
    def secure_devices_pin(self):
        """Return entity config."""
        return None

    @property
    def is_reporting_state(self):
        """Return if we're actively reporting states."""
        return self._unsub_report_state is not None

    @property
    def is_local_sdk_active(self):
        """Return if we're actively accepting local messages."""
        return self._local_sdk_active

    @property
    def should_report_state(self):
        """Return if states should be proactively reported."""
        return False

    @property
    def is_local_connected(self) -> bool:
        """Return if local is connected."""
        return (
            self._local_last_active is not None
            # We get a reachable devices intent every minute.
            and self._local_last_active > helpers.utcnow() - dt.timedelta(seconds=70)
        )

    def get_local_agent_user_id(self, webhook_id):
        """Return the user ID to be used for actions received via the local SDK.

        Return None is no agent user id is found.
        """
        found_agent_user_id = None
        for agent_user_id, agent_user_data in self._store.agent_user_ids.items():
            if agent_user_data[_STORE_GOOGLE_LOCAL_WEBHOOK_ID] == webhook_id:
                found_agent_user_id = agent_user_id
                break

        return found_agent_user_id

    def get_local_webhook_id(self, agent_user_id):
        """
        Return the webhook ID to be used for actions for a given agent user id
        via the local SDK.
        """
        if data := self._store.agent_user_ids.get(agent_user_id):
            return data[_STORE_GOOGLE_LOCAL_WEBHOOK_ID]
        return None

    @abc.abstractmethod
    def get_agent_user_id(self, context):
        """Get agent user ID from context."""

    @abc.abstractmethod
    def should_expose(self, state: State) -> bool:
        """Return if entity should be exposed."""

    # pylint: disable=unused-argument
    def should_2fa(self, state: State):
        """If an entity should have 2FA checked."""
        return True

    async def async_report_state(self, message, agent_user_id: str):
        """Send a state report to Google."""
        raise NotImplementedError

    async def async_report_state_all(self, message):
        """Send a state report to Google for all previously synced users."""
        jobs = [
            self.async_report_state(message, agent_user_id)
            for agent_user_id in self._store.agent_user_ids
        ]
        await asyncio.gather(*jobs)

    @callback
    def async_enable_report_state(self):
        """Enable proactive mode."""

        if self._unsub_report_state is None:
            self._unsub_report_state = self._owner.async_enable_report_state(self)

    @callback
    def async_disable_report_state(self):
        """Disable report state."""
        if self._unsub_report_state is not None:
            self._unsub_report_state()
            self._unsub_report_state = None

    async def async_sync_entities(self, agent_user_id: str):
        """Sync all entities to Google."""
        # Remove any pending sync
        self._google_sync_unsub.pop(agent_user_id, lambda: None)()
        status = await self._async_request_sync_devices(agent_user_id)
        if status == http.HTTPStatus.NOT_FOUND:
            await self.async_disconnect_agent_user(agent_user_id)
        return status

    async def async_sync_entities_all(self):
        """Sync all entities to Google for all registered agents."""
        if not self._store.agent_user_ids:
            return 204

        res = await asyncio.gather(
            *(
                self.async_sync_entities(agent_user_id)
                for agent_user_id in self._store.agent_user_ids
            )
        )
        return max(res, default=204)

    @callback
    def async_schedule_google_sync(self, agent_user_id: str):
        """Schedule a sync."""

        async def _schedule_callback(_now):
            """Handle a scheduled sync callback."""
            self._google_sync_unsub.pop(agent_user_id, None)
            await self.async_sync_entities(agent_user_id)

        self._google_sync_unsub.pop(agent_user_id, lambda: None)()

        self._google_sync_unsub[
            agent_user_id
        ] = self.controller.tracker.async_call_later(_SYNC_DELAY, _schedule_callback)

    @callback
    def async_schedule_google_sync_all(self):
        """Schedule a sync for all registered agents."""
        for agent_user_id in self._store.agent_user_ids:
            self.async_schedule_google_sync(agent_user_id)

    async def _async_request_sync_devices(self, agent_user_id: str) -> int:
        """Trigger a sync with Google.

        Return value is the HTTP status code of the sync request.
        """
        raise NotImplementedError

    async def async_connect_agent_user(self, agent_user_id: str):
        """Add a synced and known agent_user_id.

        Called before sending a sync response to Google.
        """
        self._store.add_agent_user_id(agent_user_id)

    async def async_disconnect_agent_user(self, agent_user_id: str):
        """Turn off report state and disable further state reporting.

        Called when:
        - The user disconnects their account from Google.
        - When the cloud configuration is initialized
        - When sync entities fails with 404
        """
        self._store.pop_agent_user_id(agent_user_id)

    @callback
    def async_enable_local_sdk(self):
        """Enable the local SDK."""
        setup_successful = True
        setup_webhook_ids = []

        # Don't enable local SDK if ssl is enabled
        if self.controller.config.api and self.controller.config.api.use_ssl:
            self._local_sdk_active = False
            return

        webhook = self.controller.components.webhook
        if not isinstance(webhook, WebhookComponent):
            self._local_sdk_active = False
            return

        for user_agent_id, _ in self._store.agent_user_ids.items():
            if (webhook_id := self.get_local_webhook_id(user_agent_id)) is None:
                setup_successful = False
                break

            try:
                webhook.register_webhook(
                    self._owner.domain,
                    "Local Support for " + user_agent_id,
                    webhook_id,
                    self._handle_local_webhook,
                    local_only=True,
                )
                setup_webhook_ids.append(webhook_id)
            except ValueError:
                _LOGGER.warning(
                    f"Webhook handler {webhook_id} for agent user id {user_agent_id} "
                    + "is already defined!",
                )
                setup_successful = False
                break

        if not setup_successful:
            _LOGGER.warning(
                "Local fulfillment failed to setup, falling back to cloud fulfillment"
            )
            for setup_webhook_id in setup_webhook_ids:
                webhook.unregister_webhook(setup_webhook_id)

        self._local_sdk_active = setup_successful

    @callback
    def async_disable_local_sdk(self):
        """Disable the local SDK."""
        if not self._local_sdk_active:
            return

        webhook = self.controller.components.webhook
        if not isinstance(webhook, WebhookComponent):
            return

        for agent_user_id in self._store.agent_user_ids:
            webhook.unregister_webhook(self.get_local_webhook_id(agent_user_id))

        self._local_sdk_active = False

    async def _handle_local_webhook(self, webhook_id: str, request: web.Request):
        """Handle an incoming local SDK message."""

        self._local_last_active = helpers.utcnow()

        # Check version local SDK.
        version = request.headers.get(_LOCAL_SDK_VERSION_HEADER)
        if not self._local_sdk_version_warn and (
            not version or asv.AwesomeVersion(version) < _LOCAL_SDK_MIN_VERSION
        ):
            _LOGGER.warning(
                f"Local SDK version is too old ({version}), check documentation on "
                + "how to update to the latest version",
            )
            self._local_sdk_version_warn = True

        payload = await request.json()

        if _LOGGER.isEnabledFor(logging.DEBUG):
            js_version = request.headers.get(_LOCAL_SDK_VERSION_HEADER, "unknown")
            _LOGGER.debug(
                f"Received local message from {request.remove} "
                + f"(JS {js_version}):"
                + "\n"
                + f"{pprint.pformat(payload)}"
                + "\n",
            )

        webhook = self.controller.components.webhook
        if not isinstance(webhook, WebhookComponent):
            webhook = None

        if (agent_user_id := self.get_local_agent_user_id(webhook_id)) is None:
            # No agent user linked to this webhook, means that the user has somehow unregistered
            # removing webhook and stopping processing of this request.
            _LOGGER.error(
                f"Cannot process request for webhook {webhook_id} as no linked agent user is found:"
                + "\n"
                + f"{pprint.pformat(payload)}"
                + "\n",
            )

            if webhook:
                webhook.unregister_webhook(webhook_id)
            return None

        if not self.enabled:
            return web.json_response(
                self._owner.api_disabled_response(payload, agent_user_id)
            )

        result = await self._owner.async_handle_message(
            self,
            agent_user_id,
            payload,
            GoogleAssistant.SOURCE_LOCAL,
        )

        if _LOGGER.isEnabledFor(logging.DEBUG):
            _LOGGER.debug(
                "Responding to local message:\n" + f"{pprint.pformat(result)}" + "\n"
            )

        return web.json_response(result)


# pylint: disable=unused-variable, invalid-name
class GoogleAssistant:
    """Google Assistant namespace."""

    GOOGLE_ASSISTANT_API_ENDPOINT: typing.Final = "/api/google_assistant"

    CONF_ALIASES: typing.Final = "aliases"
    CONF_CLIENT_EMAIL: typing.Final = "client_email"
    CONF_ENTITY_CONFIG: typing.Final = "entity_config"
    CONF_EXPOSE: typing.Final = "expose"
    CONF_EXPOSE_BY_DEFAULT: typing.Final = "expose_by_default"
    CONF_EXPOSED_DOMAINS: typing.Final = "exposed_domains"
    CONF_PRIVATE_KEY: typing.Final = "private_key"
    CONF_PROJECT_ID: typing.Final = "project_id"
    CONF_REPORT_STATE: typing.Final = "report_state"
    CONF_ROOM_HINT: typing.Final = "room"
    CONF_SECURE_DEVICES_PIN: typing.Final = "secure_devices_pin"
    CONF_SERVICE_ACCOUNT: typing.Final = "service_account"

    DATA_CONFIG: typing.Final = "config"

    DEFAULT_EXPOSE_BY_DEFAULT: typing.Final = True
    DEFAULT_EXPOSED_DOMAINS: typing.Final = [
        "alarm_control_panel",
        "binary_sensor",
        "climate",
        "cover",
        "fan",
        "group",
        "humidifier",
        "input_boolean",
        "input_select",
        "light",
        "lock",
        "media_player",
        "scene",
        "script",
        "select",
        "sensor",
        "switch",
        "vacuum",
    ]

    # https://developers.google.com/assistant/smarthome/guides
    PREFIX_TYPES: typing.Final = "action.devices.types."
    TYPE_ALARM: typing.Final = f"{PREFIX_TYPES}SECURITYSYSTEM"
    TYPE_AWNING: typing.Final = f"{PREFIX_TYPES}AWNING"
    TYPE_BLINDS: typing.Final = f"{PREFIX_TYPES}BLINDS"
    TYPE_CAMERA: typing.Final = f"{PREFIX_TYPES}CAMERA"
    TYPE_CURTAIN: typing.Final = f"{PREFIX_TYPES}CURTAIN"
    TYPE_DEHUMIDIFIER: typing.Final = f"{PREFIX_TYPES}DEHUMIDIFIER"
    TYPE_DOOR: typing.Final = f"{PREFIX_TYPES}DOOR"
    TYPE_FAN: typing.Final = f"{PREFIX_TYPES}FAN"
    TYPE_GARAGE: typing.Final = f"{PREFIX_TYPES}GARAGE"
    TYPE_HUMIDIFIER: typing.Final = f"{PREFIX_TYPES}HUMIDIFIER"
    TYPE_LIGHT: typing.Final = f"{PREFIX_TYPES}LIGHT"
    TYPE_LOCK: typing.Final = f"{PREFIX_TYPES}LOCK"
    TYPE_OUTLET: typing.Final = f"{PREFIX_TYPES}OUTLET"
    TYPE_RECEIVER: typing.Final = f"{PREFIX_TYPES}AUDIO_VIDEO_RECEIVER"
    TYPE_SCENE: typing.Final = f"{PREFIX_TYPES}SCENE"
    TYPE_SENSOR: typing.Final = f"{PREFIX_TYPES}SENSOR"
    TYPE_SETTOP: typing.Final = f"{PREFIX_TYPES}SETTOP"
    TYPE_SHUTTER: typing.Final = f"{PREFIX_TYPES}SHUTTER"
    TYPE_SPEAKER: typing.Final = f"{PREFIX_TYPES}SPEAKER"
    TYPE_SWITCH: typing.Final = f"{PREFIX_TYPES}SWITCH"
    TYPE_THERMOSTAT: typing.Final = f"{PREFIX_TYPES}THERMOSTAT"
    TYPE_TV: typing.Final = f"{PREFIX_TYPES}TV"
    TYPE_WINDOW: typing.Final = f"{PREFIX_TYPES}WINDOW"
    TYPE_VACUUM: typing.Final = f"{PREFIX_TYPES}VACUUM"

    SERVICE_REQUEST_SYNC: typing.Final = "request_sync"
    HOMEGRAPH_URL: typing.Final = "https://homegraph.googleapis.com/"
    HOMEGRAPH_SCOPE: typing.Final = "https://www.googleapis.com/auth/homegraph"
    HOMEGRAPH_TOKEN_URL: typing.Final = "https://accounts.google.com/o/oauth2/token"
    REQUEST_SYNC_BASE_URL: typing.Final = f"{HOMEGRAPH_URL}v1/devices:requestSync"
    REPORT_STATE_BASE_URL: typing.Final = (
        f"{HOMEGRAPH_URL}v1/devices:reportStateAndNotification"
    )

    # Error codes used for SmartHomeError class
    # https://developers.google.com/actions/reference/smarthome/errors-exceptions
    ERR_ALREADY_ARMED: typing.Final = "alreadyArmed"
    ERR_ALREADY_DISARMED: typing.Final = "alreadyDisarmed"
    ERR_ALREADY_STOPPED: typing.Final = "alreadyStopped"
    ERR_CHALLENGE_NEEDED: typing.Final = "challengeNeeded"
    ERR_CHALLENGE_NOT_SETUP: typing.Final = "challengeFailedNotSetup"
    ERR_DEVICE_NOT_FOUND: typing.Final = "deviceNotFound"
    ERR_DEVICE_OFFLINE: typing.Final = "deviceOffline"
    ERR_FUNCTION_NOT_SUPPORTED: typing.Final = "functionNotSupported"
    ERR_NO_AVAILABLE_CHANNEL: typing.Final = "noAvailableChannel"
    ERR_NOT_SUPPORTED: typing.Final = "notSupported"
    ERR_PIN_INCORRECT: typing.Final = "pinIncorrect"
    ERR_PROTOCOL_ERROR: typing.Final = "protocolError"
    ERR_TOO_MANY_FAILED_ATTEMPTS: typing.Final = "tooManyFailedAttempts"
    ERR_UNKNOWN_ERROR: typing.Final = "unknownError"
    ERR_UNSUPPORTED_INPUT: typing.Final = "unsupportedInput"
    ERR_USER_CANCELLED: typing.Final = "userCancelled"
    ERR_VALUE_OUT_OF_RANGE: typing.Final = "valueOutOfRange"

    # Event types
    EVENT_COMMAND_RECEIVED: typing.Final = "google_assistant.command"
    EVENT_QUERY_RECEIVED: typing.Final = "google_assistant.query"
    EVENT_SYNC_RECEIVED: typing.Final = "google_assistant.sync"

    DOMAIN_TO_GOOGLE_TYPES: typing.Final = {
        "alarm_control_panel": TYPE_ALARM,
        "button": TYPE_SCENE,
        "camera": TYPE_CAMERA,
        "climate": TYPE_THERMOSTAT,
        "cover": TYPE_BLINDS,
        "fan": TYPE_FAN,
        "group": TYPE_SWITCH,
        "humidifier": TYPE_HUMIDIFIER,
        "input_boolean": TYPE_SWITCH,
        "input_button": TYPE_SCENE,
        "input_select": TYPE_SENSOR,
        "light": TYPE_LIGHT,
        "lock": TYPE_LOCK,
        "media_player": TYPE_SETTOP,
        "scene": TYPE_SCENE,
        "script": TYPE_SCENE,
        "select": TYPE_SENSOR,
        "sensor": TYPE_SENSOR,
        "switch": TYPE_SWITCH,
        "vacuum": TYPE_VACUUM,
    }

    DEVICE_CLASS_TO_GOOGLE_TYPES: typing.Final = {
        ("binary_sensor", BinarySensor.DeviceClass.DOOR): TYPE_DOOR,
        ("binary_sensor", BinarySensor.DeviceClass.LOCK): TYPE_SENSOR,
        ("binary_sensor", BinarySensor.DeviceClass.OPENING): TYPE_SENSOR,
        ("binary_sensor", BinarySensor.DeviceClass.WINDOW): TYPE_WINDOW,
        (
            "binary_sensor",
            BinarySensor.DeviceClass.GARAGE_DOOR,
        ): TYPE_GARAGE,
        ("cover", Cover.DeviceClass.AWNING): TYPE_AWNING,
        ("cover", Cover.DeviceClass.CURTAIN): TYPE_CURTAIN,
        ("cover", Cover.DeviceClass.DOOR): TYPE_DOOR,
        ("cover", Cover.DeviceClass.GARAGE): TYPE_GARAGE,
        ("cover", Cover.DeviceClass.GATE): TYPE_GARAGE,
        ("cover", Cover.DeviceClass.SHUTTER): TYPE_SHUTTER,
        (
            "humidifier",
            Humidifier.DeviceClass.DEHUMIDIFIER,
        ): TYPE_DEHUMIDIFIER,
        (
            "humidifier",
            Humidifier.DeviceClass.HUMIDIFIER,
        ): TYPE_HUMIDIFIER,
        (
            "media_player",
            MediaPlayer.DeviceClass.RECEIVER,
        ): TYPE_RECEIVER,
        (
            "media_player",
            MediaPlayer.DeviceClass.SPEAKER,
        ): TYPE_SPEAKER,
        ("media_player", MediaPlayer.DeviceClass.TV): TYPE_TV,
        ("sensor", Sensor.DeviceClass.HUMIDITY): TYPE_SENSOR,
        ("sensor", Sensor.DeviceClass.TEMPERATURE): TYPE_SENSOR,
        ("switch", Switch.DeviceClass.OUTLET): TYPE_OUTLET,
        ("switch", Switch.DeviceClass.SWITCH): TYPE_SWITCH,
    }

    CHALLENGE_ACK_NEEDED: typing.Final = "ackNeeded"
    CHALLENGE_FAILED_PIN_NEEDED: typing.Final = "challengeFailedPinNeeded"
    CHALLENGE_PIN_NEEDED: typing.Final = "pinNeeded"

    STORE_AGENT_USER_IDS: typing.Final = "agent_user_ids"
    STORE_GOOGLE_LOCAL_WEBHOOK_ID: typing.Final = "local_webhook_id"

    SOURCE_CLOUD: typing.Final = "cloud"
    SOURCE_LOCAL: typing.Final = "local"

    NOT_EXPOSE_LOCAL: typing.Final = {TYPE_ALARM, TYPE_LOCK}

    FAN_SPEEDS: typing.Final = {
        "5/5": ["High", "Max", "Fast", "5"],
        "4/5": ["Medium High", "4"],
        "3/5": ["Medium", "3"],
        "2/5": ["Medium Low", "2"],
        "1/5": ["Low", "Min", "Slow", "1"],
        "4/4": ["High", "Max", "Fast", "4"],
        "3/4": ["Medium High", "3"],
        "2/4": ["Medium Low", "2"],
        "1/4": ["Low", "Min", "Slow", "1"],
        "3/3": ["High", "Max", "Fast", "3"],
        "2/3": ["Medium", "2"],
        "1/3": ["Low", "Min", "Slow", "1"],
        "2/2": ["High", "Max", "Fast", "2"],
        "1/2": ["Low", "Min", "Slow", "1"],
        "1/1": ["Normal", "1"],
    }

    AbstractConfig: typing.TypeAlias = _AbstractConfig
    ConfigStore: typing.TypeAlias = _ConfigStore
    Component: typing.TypeAlias = _Component
    Entity: typing.TypeAlias = _Entity
