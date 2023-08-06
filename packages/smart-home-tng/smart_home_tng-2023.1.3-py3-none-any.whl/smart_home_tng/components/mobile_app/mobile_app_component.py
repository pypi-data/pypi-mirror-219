"""
Mobile App Component for Smart Home - The Next Generation.

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
import contextlib
import http
import logging
import typing

import voluptuous as vol
from aiohttp import web

from ... import core
from .const import Const
from .helpers import (
    _decrypt_payload,
    _decrypt_payload_legacy,
    _empty_okay_response,
    _error_response,
)
from .mobile_app_binary_sensor import MobileAppBinarySensor
from .mobile_app_flow_handler import MobileAppFlowHandler
from .mobile_app_notification_service import MobileAppNotificationService
from .mobile_app_sensor import MobileAppSensor
from .mobile_app_tracker_entity import MobileAppTrackerEntity
from .push_channel import PushChannel
from .registration_view import RegistrationsView
from .webhook_commands import _WEBHOOK_COMMANDS

try:
    import nacl
    import nacl.exceptions

    CryptoError: typing.TypeAlias = nacl.exceptions.CryptoError
except OSError:
    nacl = None  # pylint: disable=invalid-name

_cv: typing.TypeAlias = core.ConfigValidation

_LOGGER: typing.Final = logging.getLogger(__name__)

_CONFIRM_NOTIFICATION: typing.Final = {
    vol.Required("type"): "mobile_app/push_notification_confirm",
    vol.Required("webhook_id"): str,
    vol.Required("confirm_id"): str,
}
_PUSH_NOTIFICATION: typing.Final = {
    vol.Required("type"): "mobile_app/push_notification_channel",
    vol.Required("webhook_id"): str,
    vol.Optional("support_confirm", default=False): bool,
}

_PLATFORMS: typing.Final = frozenset(
    [
        core.Platform.SENSOR,
        core.Platform.BINARY_SENSOR,
        core.Platform.DEVICE_TRACKER,
        core.Platform.LOGBOOK,
    ]
)
_ACTION_SCHEMA: typing.Final = _cv.DEVICE_ACTION_BASE_SCHEMA.extend(
    {
        vol.Required(core.Const.CONF_TYPE): "notify",
        vol.Required(core.Const.ATTR_MESSAGE): _cv.template,
        vol.Optional(core.Const.ATTR_TITLE): _cv.template,
        vol.Optional(core.Const.ATTR_DATA): _cv.template_complex,
    }
)

_IOS_EVENT_ZONE_ENTERED: typing.Final = "ios.zone_entered"
_IOS_EVENT_ZONE_EXITED: typing.Final = "ios.zone_exited"

_ATTR_ZONE: typing.Final = "zone"
_ATTR_SOURCE_DEVICE_NAME: typing.Final = "sourceDeviceName"
_ATTR_SOURCE_DEVICE_ID: typing.Final = "sourceDeviceID"
_EVENT_TO_DESCRIPTION: typing.Final = {
    _IOS_EVENT_ZONE_ENTERED: "entered zone",
    _IOS_EVENT_ZONE_EXITED: "exited zone",
}

_WEBHOOK_PAYLOAD_SCHEMA: typing.Final = vol.Schema(
    {
        vol.Required(Const.ATTR_WEBHOOK_TYPE): _cv.string,
        vol.Required(Const.ATTR_WEBHOOK_DATA, default={}): vol.Any(dict, list),
        vol.Optional(Const.ATTR_WEBHOOK_ENCRYPTED, default=False): _cv.boolean,
        vol.Optional(Const.ATTR_WEBHOOK_ENCRYPTED_DATA): _cv.string,
    }
)


# pylint: disable=unused-variable
class MobileAppComponent(
    core.SmartHomeControllerComponent,
    core.ActionPlatform,
    core.ConfigFlowPlatform,
    core.LogbookPlatform,
    core.NotifyPlatform,
):
    """Integrates Native Apps to Smart Home - The Next Generation."""

    def __init__(self, path: typing.Iterable[str]):
        super().__init__(path)
        self._register_flow()
        self._store: core.Store[dict[str, typing.Any]] = None
        self._deleted_ids: list[str] = []
        self._config_entries: dict[str, core.ConfigEntry] = {}
        self._devices: dict[str, core.Device] = {}
        self._push_channel: dict[str, PushChannel] = {}
        self._supported_platforms = frozenset(
            _PLATFORMS.union({core.Platform.CONFIG_FLOW, core.Platform.NOTIFY})
        )
        self._notify_service = MobileAppNotificationService(self)

    async def async_setup(self, config: core.ConfigType) -> bool:
        """Set up the mobile app component."""
        if not await super().async_setup(config):
            return False

        webhook = self.controller.components.webhook
        if not isinstance(webhook, core.WebhookComponent):
            return False
        websocket = self.controller.components.websocket_api
        if not isinstance(websocket, core.WebSocket.Component):
            return False

        shc = self._shc

        self._store = core.Store[dict[str, typing.Any]](
            shc, self.storage_version, self.storage_key
        )
        if (app_config := await self._store.async_load()) is None:
            app_config = {
                Const.DATA_DELETED_IDS: [],
            }

        self._deleted_ids = app_config.get(Const.DATA_DELETED_IDS, [])

        shc.register_view(RegistrationsView(self.domain))

        for deleted_id in self._deleted_ids:
            with contextlib.suppress(ValueError):
                webhook.register_webhook(
                    self.domain, "Deleted Webhook", deleted_id, self._handle_webhook
                )

        shc.async_create_task(
            shc.setup.async_load_platform(core.Platform.NOTIFY, self.domain, {}, config)
        )

        websocket.register_command(
            self._handle_push_notification_channel, _PUSH_NOTIFICATION
        )
        websocket.register_command(
            self._handle_push_notification_confirm, _CONFIRM_NOTIFICATION
        )

        return True

    async def async_setup_entry(self, entry: core.ConfigEntry) -> bool:
        """Set up a mobile_app entry."""
        registration = entry.data
        webhook = self.controller.components.webhook
        if not isinstance(webhook, core.WebhookComponent):
            return False

        webhook_id = registration[core.Const.CONF_WEBHOOK_ID]

        self._config_entries[webhook_id] = entry

        device_registry = self.controller.device_registry

        device = device_registry.async_get_or_create(
            config_entry_id=entry.entry_id,
            identifiers={(self.domain, registration[core.Const.ATTR_DEVICE_ID])},
            manufacturer=registration[core.Const.ATTR_MANUFACTURER],
            model=registration[core.Const.ATTR_MODEL],
            name=registration[Const.ATTR_DEVICE_NAME],
            sw_version=registration[Const.ATTR_OS_VERSION],
        )

        self._devices[webhook_id] = device

        registration_name = f"Mobile App: {registration[Const.ATTR_DEVICE_NAME]}"
        webhook.register_webhook(
            self.domain, registration_name, webhook_id, self._handle_webhook
        )

        self._shc.config_entries.async_setup_platforms(entry, _PLATFORMS)

        # await hass_notify.async_reload(hass, DOMAIN)

        return True

    async def async_setup_platform_devices(
        self, entry: core.ConfigEntry, async_add_entities: core.AddEntitiesCallback
    ) -> None:
        """Set up mobile app entities from a config entry."""
        entity_platform = core.EntityPlatform.async_get_current_platform()
        platform = entity_platform.domain
        if platform == core.Platform.BINARY_SENSOR:
            await self._async_setup_binary_sensor_platform(entry, async_add_entities)
        elif platform == core.Platform.DEVICE_TRACKER:
            await self._async_setup_device_tracker_platform(entry, async_add_entities)
        elif platform == core.Platform.SENSOR:
            await self._async_setup_sensor_platform(entry, async_add_entities)

    def _device_info(self, registration: dict) -> core.DeviceInfo:
        """Return the device info for this registration."""
        return core.DeviceInfo(
            identifiers={(self.domain, registration[core.Const.ATTR_DEVICE_ID])},
            manufacturer=registration[core.Const.ATTR_MANUFACTURER],
            model=registration[core.Const.ATTR_MODEL],
            name=registration[Const.ATTR_DEVICE_NAME],
            sw_version=registration[Const.ATTR_OS_VERSION],
        )

    # ------------------ Binary Sensor Platform ----------------------------

    async def _async_setup_binary_sensor_platform(
        self, entry: core.ConfigEntry, async_add_entities: core.AddEntitiesCallback
    ) -> None:
        """Set up mobile app binary sensor from a config entry."""
        add_entities = []

        webhook_id = entry.data[core.Const.CONF_WEBHOOK_ID]

        entity_registry = self.controller.entity_registry
        entities = entity_registry.async_entries_for_config_entry(entry.entry_id)
        for entity in entities:
            if (
                entity.domain != Const.ATTR_SENSOR_TYPE_BINARY_SENSOR
                or entity.disabled_by
            ):
                continue
            config: dict[str, typing.Any] = {
                Const.ATTR_SENSOR_ATTRIBUTES: {},
                Const.ATTR_SENSOR_DEVICE_CLASS: entity.device_class
                or entity.original_device_class,
                Const.ATTR_SENSOR_ICON: entity.original_icon,
                Const.ATTR_SENSOR_NAME: entity.original_name,
                Const.ATTR_SENSOR_STATE: None,
                Const.ATTR_SENSOR_TYPE: entity.domain,
                Const.ATTR_SENSOR_UNIQUE_ID: entity.unique_id,
                Const.ATTR_SENSOR_ENTITY_CATEGORY: entity.entity_category,
            }
            add_entities.append(MobileAppBinarySensor(self, config, entry))

        async_add_entities(add_entities)

        @core.callback
        def handle_sensor_registration(data):
            if data[core.Const.CONF_WEBHOOK_ID] != webhook_id:
                return

            async_add_entities([MobileAppBinarySensor(self, data, entry)])

        self.controller.dispatcher.async_connect(
            f"{self.domain}.{Const.ATTR_SENSOR_TYPE_BINARY_SENSOR}.register",
            handle_sensor_registration,
        )

    # ------------------ Device Action Platform --------------------------------

    async def async_get_actions(self, device_id: str) -> list[dict[str, str]]:
        """List device actions for Mobile App devices."""
        webhook_id = self._webhook_id_from_device_id(device_id)

        # pylint: disable=protected-access
        if webhook_id is None or not self._notify_service._supports_push(webhook_id):
            return []

        return [
            {
                core.Const.CONF_DEVICE_ID: device_id,
                core.Const.CONF_DOMAIN: self.domain,
                core.Const.CONF_TYPE: "notify",
            }
        ]

    async def async_validate_action_config(
        self, config: core.ConfigType
    ) -> core.ConfigType:
        return _ACTION_SCHEMA(config)

    async def async_call_action_from_config(
        self,
        config: core.ConfigType,
        variables: dict[str, typing.Any],
        context: core.Context,
    ) -> None:
        """Execute a device action."""
        webhook_id = self._webhook_id_from_device_id(config[core.Const.CONF_DEVICE_ID])

        if webhook_id is None:
            raise core.InvalidDeviceAutomationConfig(
                "Unable to resolve webhook ID from the device ID"
            )

        if (service_name := self._get_notify_service(webhook_id)) is None:
            raise core.InvalidDeviceAutomationConfig(
                "Unable to find notify service for webhook ID"
            )

        service_data = {core.Const.ATTR_TARGET: webhook_id}

        # Render it here because we have access to variables here.
        for key in (
            core.Const.ATTR_MESSAGE,
            core.Const.ATTR_TITLE,
            core.Const.ATTR_DATA,
        ):
            if key not in config:
                continue

            value_template: core.Template = config[key]
            core.Template.attach(self.controller, value_template)

            try:
                service_data[key] = core.Template.render_complex(
                    value_template, variables
                )
            except core.TemplateError as err:
                raise core.InvalidDeviceAutomationConfig(
                    f"Error rendering {key}: {err}"
                ) from err

        await self.controller.services.async_call(
            "notify",
            service_name,
            service_data,
            blocking=True,
            context=context,
        )

    async def async_get_action_capabilities(
        self, config: core.ConfigType
    ) -> dict[str, vol.Schema]:
        """List action capabilities."""
        if config[core.Const.CONF_TYPE] != "notify":
            return {}

        return {
            "extra_fields": vol.Schema(
                {
                    vol.Required(core.Const.ATTR_MESSAGE): str,
                    vol.Optional(core.Const.ATTR_TITLE): str,
                }
            )
        }

    @core.callback
    def _webhook_id_from_device_id(self, device_id: str) -> str:
        """Get webhook ID from device ID."""

        for cur_webhook_id, cur_device in self._devices.items():
            if cur_device.id == device_id:
                return cur_webhook_id

        return None

    @core.callback
    def _get_notify_service(self, webhook_id: str) -> str:
        """Return the notify service for this webhook ID."""
        notify_service = self._notify_service

        # pylint: disable=protected-access
        for (
            target_service,
            target_webhook_id,
        ) in notify_service._registered_targets.items():
            if target_webhook_id == webhook_id:
                return target_service

        return None

    # ------------------- Config Flow Platform ---------------------------------

    def create_config_flow(
        self, context: dict, init_data: typing.Any
    ) -> core.ConfigFlow:
        return MobileAppFlowHandler(self, context, init_data)

    # ------------------- Device Tracker Platform -----------------------------

    async def _async_setup_device_tracker_platform(
        self, entry: core.ConfigEntry, async_add_entities: core.AddEntitiesCallback
    ) -> None:
        """Set up OwnTracks based off an entry."""
        entity = MobileAppTrackerEntity(self, entry)
        async_add_entities([entity])

    # -------------------- Logbook Platform -----------------------------------

    def async_describe_events(self, async_describe_event: core.LogbookCallback) -> None:
        """Describe logbook events."""

        async_describe_event(_IOS_EVENT_ZONE_ENTERED)
        async_describe_event(_IOS_EVENT_ZONE_EXITED)

    def async_describe_event(self, event: core.LazyPartialState) -> dict[str, str]:
        """Describe mobile_app logbook event."""
        data = event.data
        event_description = _EVENT_TO_DESCRIPTION[event.event_type]
        zone_entity_id = data.get(_ATTR_ZONE)
        source_device_name = data.get(
            _ATTR_SOURCE_DEVICE_NAME, data.get(_ATTR_SOURCE_DEVICE_ID)
        )
        zone_name = None
        zone_icon = None
        if zone_entity_id and (
            zone_state := self.controller.states.get(zone_entity_id)
        ):
            zone_name = zone_state.attributes.get(core.Const.ATTR_FRIENDLY_NAME)
            zone_icon = zone_state.attributes.get(core.Const.ATTR_ICON)
        description = {
            core.Const.LOGBOOK_ENTRY_NAME: source_device_name,
            core.Const.LOGBOOK_ENTRY_MESSAGE: f"{event_description} {zone_name or zone_entity_id}",
            core.Const.LOGBOOK_ENTRY_ICON: zone_icon or "mdi:crosshairs-gps",
        }
        if zone_entity_id:
            description[core.Const.LOGBOOK_ENTRY_ENTITY_ID] = zone_entity_id
        return description

    # --------------------- Notify Platform -----------------------------------

    async def async_get_service(
        self, config: core.ConfigType, discovery_info: core.DiscoveryInfoType = None
    ) -> core.BaseNotificationService:
        return self._notify_service

    # --------------------- Sensor Platform -----------------------------------

    async def _async_setup_sensor_platform(
        self, entry: core.ConfigEntry, async_add_entities: core.AddEntitiesCallback
    ) -> None:
        """Set up mobile app sensor from a config entry."""
        add_entities = []

        webhook_id = entry.data[core.Const.CONF_WEBHOOK_ID]

        entity_registry = self.controller.entity_registry
        entities = entity_registry.async_entries_for_config_entry(entry.entry_id)
        for entity in entities:
            if entity.domain != Const.ATTR_SENSOR_TYPE_SENSOR or entity.disabled_by:
                continue
            config: dict[str, typing.Any] = {
                Const.ATTR_SENSOR_ATTRIBUTES: {},
                Const.ATTR_SENSOR_DEVICE_CLASS: entity.device_class
                or entity.original_device_class,
                Const.ATTR_SENSOR_ICON: entity.original_icon,
                Const.ATTR_SENSOR_NAME: entity.original_name,
                Const.ATTR_SENSOR_STATE: None,
                Const.ATTR_SENSOR_TYPE: entity.domain,
                Const.ATTR_SENSOR_UNIQUE_ID: entity.unique_id,
                Const.ATTR_SENSOR_UOM: entity.unit_of_measurement,
                Const.ATTR_SENSOR_ENTITY_CATEGORY: entity.entity_category,
            }
            add_entities.append(MobileAppSensor(self, config, entry))

        async_add_entities(add_entities)

        @core.callback
        def handle_sensor_registration(data):
            if data[core.Const.CONF_WEBHOOK_ID] != webhook_id:
                return

            async_add_entities([MobileAppSensor(self, data, entry)])

        self.controller.dispatcher.async_connect(
            f"{self.domain}.{Const.ATTR_SENSOR_TYPE_SENSOR}.register",
            handle_sensor_registration,
        )

    def _ensure_webhook_access(
        self, connection: core.WebSocket.Connection, msg: dict
    ) -> bool:
        # Validate that the webhook ID is registered to the user of the websocket connection
        config_entry = self._config_entries.get(msg["webhook_id"])

        if config_entry is None:
            connection.send_error(
                msg["id"], core.WebSocket.ERR_NOT_FOUND, "Webhook ID not found"
            )
            return False

        if config_entry.data[Const.CONF_USER_ID] != connection.user.id:
            connection.send_error(
                msg["id"],
                core.WebSocket.ERR_UNAUTHORIZED,
                "User not linked to this webhook ID",
            )
            return False
        return True

    # ---------------------- Websocket API ------------------------------------

    @core.callback
    def _handle_push_notification_confirm(
        self,
        connection: core.WebSocket.Connection,
        msg: dict,
    ):
        """Confirm receipt of a push notification."""
        if not self._ensure_webhook_access(connection, msg):
            return

        channel: PushChannel = self._push_channel.get(msg["webhook_id"])
        if channel is None:
            connection.send_error(
                msg["id"],
                core.WebSocket.ERR_NOT_FOUND,
                "Push notification channel not found",
            )
            return

        if channel.async_confirm_notification(msg["confirm_id"]):
            connection.send_result(msg["id"])
        else:
            connection.send_error(
                msg["id"],
                core.WebSocket.ERR_NOT_FOUND,
                "Push notification channel not found",
            )

    async def _handle_push_notification_channel(
        self,
        connection: core.WebSocket.Connection,
        msg: dict,
    ):
        """Set up a direct push notification channel."""
        if not self._ensure_webhook_access(connection, msg):
            return

        shc = connection.owner.controller

        webhook_id = msg["webhook_id"]
        registered_channels = self._push_channel

        if webhook_id in registered_channels:
            await registered_channels[webhook_id].async_teardown()

        @core.callback
        def on_channel_teardown():
            """Handle teardown."""
            if registered_channels.get(webhook_id) == channel:
                registered_channels.pop(webhook_id)

            # Remove subscription from connection if still exists
            connection.subscriptions.pop(msg["id"], None)

        channel = registered_channels[webhook_id] = PushChannel(
            self,
            webhook_id,
            msg["support_confirm"],
            lambda data: connection.send_event_message(msg["id"], data),
            on_channel_teardown,
        )

        connection.subscriptions[msg["id"]] = lambda: shc.async_create_task(
            channel.async_teardown()
        )
        connection.send_result(msg["id"])

    # ---------------------- Webhook API ------------------------------------

    async def _handle_webhook(
        self, webhook_id: str, request: web.Request
    ) -> web.Response:
        """Handle webhook callback."""
        if webhook_id in self._deleted_ids:
            return web.Response(status=410)

        config_entry = self._config_entries[webhook_id]

        device_name = config_entry.data[Const.ATTR_DEVICE_NAME]

        try:
            req_data = await request.json()
        except ValueError:
            _LOGGER.warning(
                f"Received invalid JSON from mobile_app device: {device_name}"
            )
            return _empty_okay_response(status=http.HTTPStatus.BAD_REQUEST)

        if (
            Const.ATTR_WEBHOOK_ENCRYPTED not in req_data
            and config_entry.data[Const.ATTR_SUPPORTS_ENCRYPTION]
        ):
            _LOGGER.warning(
                f"Refusing to accept unencrypted webhook from {device_name}",
            )
            return _error_response(Const.ERR_ENCRYPTION_REQUIRED, "Encryption required")

        try:
            req_data = _WEBHOOK_PAYLOAD_SCHEMA(req_data)
        except vol.Invalid as ex:
            err = vol.humanize.humanize_error(req_data, ex)
            _LOGGER.error(
                f"Received invalid webhook from {device_name} with payload: {err}"
            )
            return _empty_okay_response()

        webhook_type = req_data[Const.ATTR_WEBHOOK_TYPE]

        webhook_payload = req_data.get(Const.ATTR_WEBHOOK_DATA, {})

        if req_data[Const.ATTR_WEBHOOK_ENCRYPTED]:
            enc_data = req_data[Const.ATTR_WEBHOOK_ENCRYPTED_DATA]
            try:
                webhook_payload = _decrypt_payload(
                    config_entry.data[Const.CONF_SECRET], enc_data
                )
                if Const.ATTR_NO_LEGACY_ENCRYPTION not in config_entry.data:
                    data = {**config_entry.data, Const.ATTR_NO_LEGACY_ENCRYPTION: True}
                    self.controller.config_entries.async_update_entry(
                        config_entry, data=data
                    )
            except CryptoError:
                if Const.ATTR_NO_LEGACY_ENCRYPTION not in config_entry.data:
                    try:
                        webhook_payload = _decrypt_payload_legacy(
                            config_entry.data[Const.CONF_SECRET], enc_data
                        )
                    except CryptoError:
                        _LOGGER.warning(
                            "Ignoring encrypted payload because unable to decrypt"
                        )
                    except ValueError:
                        _LOGGER.warning("Ignoring invalid encrypted payload")
                else:
                    _LOGGER.warning(
                        "Ignoring encrypted payload because unable to decrypt"
                    )
            except ValueError:
                _LOGGER.warning("Ignoring invalid encrypted payload")

        if webhook_type not in _WEBHOOK_COMMANDS:
            _LOGGER.error(
                f"Received invalid webhook from {device_name} of type: {webhook_type}",
            )
            return _empty_okay_response()

        _LOGGER.debug(
            f"Received webhook payload from {device_name} for type {webhook_type}: "
            + f"{webhook_payload}",
        )

        # Shield so we make sure we finish the webhook, even if sender hangs up.
        return await asyncio.shield(
            _WEBHOOK_COMMANDS[webhook_type](self, config_entry, webhook_payload)
        )
