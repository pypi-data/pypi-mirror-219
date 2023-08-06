"""
Home Assistant Cloud Component for Smart Home - The Next Generation.

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
import dataclasses
import typing

import async_timeout
import aiohttp
import attr
import awesomeversion as asv
import hass_nabucasa as nabucasa  # pylint: disable=import-error
import voluptuous as vol
import yarl

from ... import core
from .cloud_client import CloudClient
from .cloud_forgot_password_view import CloudForgotPasswordView
from .cloud_login_view import CloudLoginView
from .cloud_logout_view import CloudLogoutView
from .cloud_oauth2_implementation import CloudOAuth2Implementation
from .cloud_preferences import CloudPreferences
from .cloud_register_view import CloudRegisterView
from .cloud_remote_binary import CloudRemoteBinary
from .cloud_resend_confirm_view import CloudResendConfirmView
from .const import Const
from .google_actions_sync_view import GoogleActionsSyncView
from .helpers import _ws_handle_cloud_errors
from .speech_to_text_provider import SpeechToTextProvider
from .text_to_speech_provider import TextToSpeechProvider, _CONF_GENDER

_cv: typing.TypeAlias = core.ConfigValidation
_account_link: typing.TypeAlias = nabucasa.account_link
_cloud_api: typing.TypeAlias = nabucasa.cloud_api
_thingtalk: typing.TypeAlias = nabucasa.thingtalk


# from alexa const
_CONF_DISPLAY_CATEGORIES: typing.Final = "display_categories"

# from google assistant const
_CONF_ROOM_HINT: typing.Final = "room"

_DEFAULT_MODE: typing.Final = Const.MODE_PROD

_SERVICE_REMOTE_CONNECT: typing.Final = "remote_connect"
_SERVICE_REMOTE_DISCONNECT: typing.Final = "remote_disconnect"

_SIGNAL_CLOUD_CONNECTION_STATE: typing.Final = "CLOUD_CONNECTION_STATE"


_ALEXA_ENTITY_SCHEMA: typing.Final = vol.Schema(
    {
        vol.Optional(core.Const.CONF_DESCRIPTION): _cv.string,
        vol.Optional(_CONF_DISPLAY_CATEGORIES): _cv.string,
        vol.Optional(core.Const.CONF_NAME): _cv.string,
    }
)

_GOOGLE_ENTITY_SCHEMA: typing.Final = vol.Schema(
    {
        vol.Optional(core.Const.CONF_NAME): _cv.string,
        vol.Optional(Const.CONF_ALIASES): vol.All(_cv.ensure_list, [_cv.string]),
        vol.Optional(_CONF_ROOM_HINT): _cv.string,
    }
)

_ASSISTANT_SCHEMA: typing.Final = vol.Schema(
    {
        vol.Optional(
            Const.CONF_FILTER, default=dict
        ): core.EntityFilter.Const.FILTER_SCHEMA
    }
)

_ALEXA_SCHEMA: typing.Final = _ASSISTANT_SCHEMA.extend(
    {vol.Optional(Const.CONF_ENTITY_CONFIG): {_cv.entity_id: _ALEXA_ENTITY_SCHEMA}}
)

_GACTIONS_SCHEMA: typing.Final = _ASSISTANT_SCHEMA.extend(
    {vol.Optional(Const.CONF_ENTITY_CONFIG): {_cv.entity_id: _GOOGLE_ENTITY_SCHEMA}}
)
_CACHE_TIMEOUT: typing.Final = 3600

_CURRENT_VERSION: typing.Final = asv.AwesomeVersion(core.Const.__version__)

_CLOUD_STATUS: typing.Final = {vol.Required("type"): "cloud/status"}
_CLOUD_SUBSCRIPTION: typing.Final = {vol.Required("type"): "cloud/subscription"}
_CLOUD_UPDATE_PREFS: typing.Final = {
    vol.Required("type"): "cloud/update_prefs",
    vol.Optional(Const.PREF_ENABLE_GOOGLE): bool,
    vol.Optional(Const.PREF_ENABLE_ALEXA): bool,
    vol.Optional(Const.PREF_ALEXA_REPORT_STATE): bool,
    vol.Optional(Const.PREF_GOOGLE_REPORT_STATE): bool,
    vol.Optional(Const.PREF_ALEXA_DEFAULT_EXPOSE): [str],
    vol.Optional(Const.PREF_GOOGLE_DEFAULT_EXPOSE): [str],
    vol.Optional(Const.PREF_GOOGLE_SECURE_DEVICES_PIN): vol.Any(None, str),
    vol.Optional(Const.PREF_TTS_DEFAULT_VOICE): vol.All(
        vol.Coerce(tuple), vol.In(nabucasa.voice.MAP_VOICE)
    ),
}
_CLOUD_HOOK_CREATE: typing.Final = {
    vol.Required("type"): "cloud/cloudhook/create",
    vol.Required("webhook_id"): str,
}
_CLOUD_HOOK_DELETE: typing.Final = {
    vol.Required("type"): "cloud/cloudhook/delete",
    vol.Required("webhook_id"): str,
}
_CLOUD_REMOTE_CONNECT: typing.Final = {"type": "cloud/remote/connect"}
_CLOUD_REMOTE_DISCONNECT: typing.Final = {"type": "cloud/remote/disconnect"}
_CLOUD_ASSISTANT_LIST: typing.Final = {"type": "cloud/google_assistant/entities"}
_CLOUD_ASSISTANT_UPDATE: typing.Final = {
    "type": "cloud/google_assistant/entities/update",
    "entity_id": str,
    vol.Optional("should_expose"): vol.Any(None, bool),
    vol.Optional("override_name"): str,
    vol.Optional("aliases"): [str],
    vol.Optional("disable_2fa"): bool,
}
_CLOUD_ALEXA_LIST: typing.Final = {"type": "cloud/alexa/entities"}
_CLOUD_ALEXA_UPDATE: typing.Final = {
    "type": "cloud/alexa/entities/update",
    "entity_id": str,
    vol.Optional("should_expose"): vol.Any(None, bool),
}
_CLOUD_ALEXA_SYNC: typing.Final = {"type": "cloud/alexa/sync"}
_CLOUD_THINKTALK_CONVERT: typing.Final = {
    "type": "cloud/thingtalk/convert",
    "query": str,
}
_CLOUD_TTS_INFO: typing.Final = {"type": "cloud/tts/info"}


# pylint: disable=unused-variable
class CloudComponent(
    core.CloudComponent,
    core.SpeechToTextPlatform,
    core.SystemHealthPlatform,
    core.TTS.Platform,
):
    """Component to integrate the Home Assistant cloud."""

    def __init__(self, path: typing.Iterable[str]):
        super().__init__(path)
        self._cloud: nabucasa.Cloud = None
        self._prefs: CloudPreferences = None
        self._loaded = False
        self._services: typing.Any = None
        self._supported_platforms = frozenset(
            [
                core.Platform.BINARY_SENSOR,
                core.Platform.STT,
                core.Platform.SYSTEM_HEALTH,
                core.Platform.TTS,
            ]
        )

    @property
    def cloud(self) -> nabucasa.Cloud:
        return self._cloud

    @property
    def active_subscription(self) -> bool:
        """Test if user has an active subscription."""
        return self.is_logged_in and not self.cloud.subscription_expired

    @property
    def is_connected(self) -> bool:
        """Test if connected to the cloud."""
        return self._cloud is not None and self._cloud.iot.connected

    @property
    def is_logged_in(self) -> bool:
        """Test if user is logged in.

        Note: This returns True even if not currently connected to the cloud.
        """
        return self._cloud is not None and self._cloud.is_logged_in

    @property
    def remote_ui_url(self) -> str:
        """Get the remote UI URL."""
        if not self.is_logged_in:
            raise core.CloudNotAvailable()

        if not self._prefs.client.prefs.remote_enabled:
            raise core.CloudNotAvailable

        if not (remote_domain := self._cloud.client.prefs.remote_domain):
            raise core.CloudNotAvailable

        return f"https://{remote_domain}"

    async def async_validate_config(self, config: core.ConfigType) -> core.ConfigType:
        """Validate Cloud configuration."""
        # pylint: disable=no-value-for-parameter
        schema = vol.Schema(
            {
                self.domain: vol.Schema(
                    {
                        vol.Optional(
                            core.Const.CONF_MODE, default=_DEFAULT_MODE
                        ): vol.In([Const.MODE_DEV, Const.MODE_PROD]),
                        vol.Optional(Const.CONF_COGNITO_CLIENT_ID): str,
                        vol.Optional(Const.CONF_USER_POOL_ID): str,
                        vol.Optional(core.Const.CONF_REGION): str,
                        vol.Optional(Const.CONF_RELAYER): str,
                        vol.Optional(Const.CONF_SUBSCRIPTION_INFO_URL): vol.Url(),
                        vol.Optional(Const.CONF_CLOUDHOOK_CREATE_URL): vol.Url(),
                        vol.Optional(Const.CONF_REMOTE_API_URL): vol.Url(),
                        vol.Optional(Const.CONF_ACME_DIRECTORY_SERVER): vol.Url(),
                        vol.Optional(Const.CONF_ALEXA): _ALEXA_SCHEMA,
                        vol.Optional(Const.CONF_GOOGLE_ACTIONS): _GACTIONS_SCHEMA,
                        vol.Optional(Const.CONF_ALEXA_ACCESS_TOKEN_URL): vol.Url(),
                        vol.Optional(
                            Const.CONF_GOOGLE_ACTIONS_REPORT_STATE_URL
                        ): vol.Url(),
                        vol.Optional(Const.CONF_ACCOUNT_LINK_URL): vol.Url(),
                        vol.Optional(Const.CONF_VOICE_API_URL): vol.Url(),
                    }
                )
            },
            extra=vol.ALLOW_EXTRA,
        )
        return schema(config)

    async def async_setup(self, config: core.ConfigType) -> bool:
        """Initialize the Home Assistant cloud."""
        if not await super().async_setup(config):
            return False

        websocket = self.controller.components.websocket_api
        if not isinstance(websocket, core.WebSocket.Component):
            return False

        # Process configs
        self._config = config
        if self.domain in config:
            kwargs = dict(config[self.domain])
        else:
            kwargs = {core.Const.CONF_MODE: _DEFAULT_MODE}

        # Alexa/Google custom config
        alexa_conf = kwargs.pop(Const.CONF_ALEXA, None) or _ALEXA_SCHEMA({})
        google_conf = kwargs.pop(Const.CONF_GOOGLE_ACTIONS, None) or _GACTIONS_SCHEMA(
            {}
        )

        # Cloud settings
        prefs = CloudPreferences(self)
        await prefs.async_initialize()

        # Initialize Cloud
        websession = core.HttpClient.async_get_clientsession(self.controller)
        client = CloudClient(self, prefs, websession, alexa_conf, google_conf)
        self._cloud = nabucasa.Cloud(client, **kwargs)

        shc = self.controller
        shc.bus.async_listen_once(core.Const.EVENT_SHC_STOP, self._shutdown)

        _remote_handle_prefs_updated(self._cloud)

        core.Service.async_register_admin_service(
            shc, self.domain, _SERVICE_REMOTE_CONNECT, self._service_handler
        )
        core.Service.async_register_admin_service(
            shc, self.domain, _SERVICE_REMOTE_DISCONNECT, self._service_handler
        )

        self._cloud.iot.register_on_connect(self._on_connect)
        self._cloud.iot.register_on_disconnect(self._on_disconnect)
        self._cloud.register_on_initialized(self._on_initialized)

        await self._cloud.initialize()

        # Set up HTTP API
        websocket.register_command(self._cloud_status, _CLOUD_STATUS)
        websocket.register_command(self._cloud_subscription, _CLOUD_SUBSCRIPTION)
        websocket.register_command(self._cloud_update_prefs, _CLOUD_UPDATE_PREFS)
        websocket.register_command(self._cloud_hook_create, _CLOUD_HOOK_CREATE)
        websocket.register_command(self._cloud_hook_delete, _CLOUD_HOOK_DELETE)
        websocket.register_command(self._cloud_remote_connect, _CLOUD_REMOTE_CONNECT)
        websocket.register_command(
            self._cloud_remote_disconnect, _CLOUD_REMOTE_DISCONNECT
        )
        websocket.register_command(self._cloud_assistant_list, _CLOUD_ASSISTANT_LIST)
        websocket.register_command(
            self._cloud_assistant_update, _CLOUD_ASSISTANT_UPDATE
        )
        websocket.register_command(self._cloud_alexa_list, _CLOUD_ALEXA_LIST)
        websocket.register_command(self._cloud_alexa_update, _CLOUD_ALEXA_UPDATE)
        websocket.register_command(self._cloud_alexa_sync, _CLOUD_ALEXA_SYNC)
        websocket.register_command(
            self._cloud_thingtalk_convert, _CLOUD_THINKTALK_CONVERT
        )
        websocket.register_command(self._cloud_tts_info, _CLOUD_TTS_INFO)

        shc.http.register_view(GoogleActionsSyncView(self))
        shc.http.register_view(CloudLoginView(self))
        shc.http.register_view(CloudLogoutView(self))
        shc.http.register_view(CloudRegisterView(self))
        shc.http.register_view(CloudResendConfirmView(self))
        shc.http.register_view(CloudForgotPasswordView(self))

        # Set up cloud account link.
        core.AbstractOAuth2Implementation.async_add_implementation_provider(
            self.domain, self._async_provide_oauth2_implementation
        )

        return True

    async def async_setup_platform(
        self,
        _platform_config: core.ConfigType,
        add_entities: core.AddEntitiesCallback,
        discovery_info: core.DiscoveryInfoType,
    ):
        if self._current_platform == core.Platform.BINARY_SENSOR:
            # Set up the cloud binary sensors.
            if discovery_info is None:
                return
            cloud = self._cloud

            add_entities([CloudRemoteBinary(cloud)])

    def listen_connection_change(
        self,
        target: typing.Callable[
            [core.CloudConnectionState], typing.Awaitable[None] | None
        ],
    ) -> typing.Callable[[], None]:
        """Notify on connection state changes."""
        return self.controller.dispatcher.async_connect(
            _SIGNAL_CLOUD_CONNECTION_STATE, target
        )

    async def async_create_cloudhook(self, webhook_id: str) -> str:
        """Create a cloudhook."""
        if not self.is_connected:
            raise core.CloudNotConnected

        if not self.is_logged_in:
            raise core.CloudNotAvailable

        hook = await self._cloud.cloudhooks.async_create(webhook_id, True)
        return hook["cloudhook_url"]

    async def async_delete_cloudhook(self, webhook_id: str) -> None:
        """Delete a cloudhook."""
        if self._cloud is None:
            raise core.CloudNotAvailable

        await self._cloud.cloudhooks.async_delete(webhook_id)

    def is_cloudhook_request(self, request):
        """Test if a request came from a cloudhook.

        Async friendly.
        """
        return isinstance(request, core.MockRequest)

    async def _shutdown(self, _event: core.Event):
        """Shutdown event."""
        await self.cloud.stop()

    async def _service_handler(self, service: core.ServiceCall) -> None:
        """Handle service for cloud."""
        if service.service == _SERVICE_REMOTE_CONNECT:
            await self._prefs.async_update(remote_enabled=True)
        elif service.service == _SERVICE_REMOTE_DISCONNECT:
            await self._prefs.async_update(remote_enabled=False)

    async def _on_connect(self):
        """Discover RemoteUI binary sensor."""

        # Prevent multiple discovery
        if self._loaded:
            return
        self._loaded = True

        await self.controller.setup.async_load_platform(
            core.Platform.BINARY_SENSOR, self.domain, {}, self._config
        )
        await self.controller.setup.async_load_platform(
            core.Platform.STT, self.domain, {}, self._config
        )
        await self.controller.setup.async_load_platform(
            core.Platform.TTS, self.domain, {}, self._config
        )

        self.controller.dispatcher.async_send(
            _SIGNAL_CLOUD_CONNECTION_STATE,
            core.CloudConnectionState.CLOUD_CONNECTED,
        )

    async def _on_disconnect(self):
        """Handle cloud disconnect."""
        self.controller.dispatcher.async_send(
            _SIGNAL_CLOUD_CONNECTION_STATE,
            core.CloudConnectionState.CLOUD_DISCONNECTED,
        )

    async def _on_initialized(self):
        """Update preferences."""
        await self._prefs.async_update(remote_domain=self._cloud.remote.instance_domain)

    async def _async_provide_oauth2_implementation(self, domain: str):
        """Provide an implementation for a domain."""
        services = await self._get_services()

        for service in services:
            if (
                service["service"] == domain
                and _CURRENT_VERSION >= service["min_version"]
                and (
                    service.get("accepts_new_authorizations", True)
                    or (
                        (
                            entries := self.controller.config_entries.async_entries(
                                domain
                            )
                        )
                        and any(
                            entry.data.get("auth_implementation") == self.domain
                            for entry in entries
                        )
                    )
                )
            ):
                return [CloudOAuth2Implementation(self, domain)]

        return []

    async def _get_services(self):
        """Get the available services."""
        if (services := self._services) is not None:
            return services

        try:
            services = await _account_link.async_fetch_available_services(self._cloud)
        except (aiohttp.ClientError, asyncio.TimeoutError):
            return []

        self._services = services

        @core.callback
        def clear_services(_now):
            """Clear services cache."""
            self._services = None

        self.controller.tracker.async_call_later(_CACHE_TIMEOUT, clear_services)

        return services

    # ----------------- Speech To Text Platform -----------------------------

    async def async_get_stt_engine(
        self, config: core.ConfigType, discovery_info: core.DiscoveryInfoType = None
    ) -> core.SpeechToTextProvider:
        return SpeechToTextProvider(self._cloud)

    # ------------------ System Health Platform -----------------------------

    def register_system_health_info(self, info: core.SystemHealthRegistration) -> None:
        """Register system health callbacks."""
        info.async_register_info(self._system_health_info, "/config/cloud")

    async def _system_health_info(self):
        """Get info for the info page."""
        cloud = self._cloud
        client: CloudClient = cloud.client

        data = {
            "logged_in": cloud.is_logged_in,
        }

        if cloud.is_logged_in:
            data["subscription_expiration"] = cloud.expiration_date
            data["relayer_connected"] = cloud.is_connected
            data["remote_enabled"] = client.prefs.remote_enabled
            data["remote_connected"] = cloud.remote.is_connected
            data["alexa_enabled"] = client.prefs.alexa_enabled
            data["google_enabled"] = client.prefs.google_enabled
            data["remote_server"] = cloud.remote.snitun_server

        system_health = core.SmartHomeControllerComponent.get_component(
            core.Const.SYSTEM_HEALTH_COMPONENT_NAME
        )
        if isinstance(system_health, core.SystemHealthComponent):
            data["can_reach_cert_server"] = system_health.async_check_can_reach_url(
                cloud.acme_directory_server
            )
            data["can_reach_cloud_auth"] = system_health.async_check_can_reach_url(
                f"https://cognito-idp.{cloud.region}.amazonaws.com/"
                + f"{cloud.user_pool_id}/.well-known/jwks.json",
            )
            data["can_reach_cloud"] = system_health.async_check_can_reach_url(
                yarl.URL(cloud.relayer).with_scheme("https").with_path("/status")
            )

        return data

    # ------------------------ Text To Speech Platform -----------------------------

    async def async_get_tts_engine(
        self, config: core.ConfigType, discovery_info: core.DiscoveryInfoType = None
    ) -> core.TTS.Provider:
        """Set up Cloud speech component."""
        cloud = self._cloud

        if discovery_info is not None:
            language = None
            gender = None
        else:
            language = config[core.Const.CONF_LANG]
            gender = config[_CONF_GENDER]

        return TextToSpeechProvider(self.controller, cloud, language, gender)

    # ---------------------------- Websocket Commands -------------------------

    def _check_cloud_auth(
        self,
        connection: core.WebSocket.Connection,
        msg: dict,
    ) -> bool:
        """Require to be logged into the cloud."""
        if not self._cloud.is_logged_in:
            connection.send_message(
                connection.error_message(
                    msg["id"], "not_logged_in", "You need to be logged in to the cloud."
                )
            )
            return False
        return True

    async def _cloud_status(
        self,
        connection: core.WebSocket.Connection,
        msg: dict,
    ):
        """Handle request for account info.

        Async friendly.
        """
        cloud = self._cloud
        connection.send_message(
            connection.result_message(
                msg["id"], await _account_data(self.controller, cloud)
            )
        )

    async def _cloud_subscription(
        self,
        connection: core.WebSocket.Connection,
        msg: dict,
    ):
        """Handle request for account info."""
        if self._check_cloud_auth(connection, msg):
            try:
                async with async_timeout.timeout(Const.REQUEST_TIMEOUT):
                    data = await _cloud_api.async_subscription_info(self._cloud)
            except aiohttp.ClientError:
                connection.send_error(
                    msg["id"], "request_failed", "Failed to request subscription"
                )
            else:
                connection.send_result(msg["id"], data)

    async def _cloud_update_prefs(
        self,
        connection: core.WebSocket.Connection,
        msg: dict,
    ):
        """Handle request for account info."""
        if self._check_cloud_auth(connection, msg):
            changes = dict(msg)
            changes.pop("id")
            changes.pop("type")

            # If we turn alexa linking on, validate that we can fetch access token
            if changes.get(Const.PREF_ALEXA_REPORT_STATE):
                alexa_config = await self._cloud.client.get_alexa_config()
                try:
                    async with async_timeout.timeout(10):
                        await alexa_config.async_get_access_token()
                except asyncio.TimeoutError:
                    connection.send_error(
                        msg["id"],
                        "alexa_timeout",
                        "Timeout validating Alexa access token.",
                    )
                    return
                except (core.NoTokenAvailable, core.RequireRelink):
                    connection.send_error(
                        msg["id"],
                        "alexa_relink",
                        "Please go to the Alexa app and re-link the Home Assistant "
                        + "skill and then try to enable state reporting.",
                    )
                    await alexa_config.set_authorized(False)
                    return

                await alexa_config.set_authorized(True)

            await self._cloud.client.prefs.async_update(**changes)

            connection.send_result(msg["id"])

    @_ws_handle_cloud_errors
    async def _cloud_hook_create(
        self,
        connection: core.WebSocket.Connection,
        msg: dict,
    ):
        """Handle request for account info."""
        if self._check_cloud_auth(connection, msg):
            hook = await self._cloud.cloudhooks.async_create(msg["webhook_id"], False)
            connection.send_result(msg["id"], hook)

    @_ws_handle_cloud_errors
    async def _cloud_hook_delete(
        self,
        connection: core.WebSocket.Connection,
        msg: dict,
    ):
        """Handle request for account info."""
        if self._check_cloud_auth(connection, msg):
            await self._cloud.cloudhooks.async_delete(msg["webhook_id"])
            connection.send_result(msg["id"])

    @_ws_handle_cloud_errors
    async def _cloud_remote_connect(
        self,
        connection: core.WebSocket.Connection,
        msg: dict,
    ):
        """Handle request for connect remote."""
        connection.require_admin()
        if self._check_cloud_auth(connection, msg):
            await self._cloud.client.prefs.async_update(remote_enabled=True)
            connection.send_result(
                msg["id"], await _account_data(self.controller, self._cloud)
            )

    @_ws_handle_cloud_errors
    async def _cloud_remote_disconnect(
        self,
        connection: core.WebSocket.Connection,
        msg: dict,
    ):
        """Handle request for disconnect remote."""
        connection.require_admin()
        if self._check_cloud_auth(connection, msg):
            cloud = self._cloud
            await cloud.client.prefs.async_update(remote_enabled=False)
            connection.send_result(
                msg["id"], await _account_data(self.controller, cloud)
            )

    @_ws_handle_cloud_errors
    async def _cloud_assistant_list(
        self,
        connection: core.WebSocket.Connection,
        msg: dict,
    ):
        """List all google assistant entities."""
        connection.require_admin()
        if self._check_cloud_auth(connection, msg):
            cloud = self._cloud
            gconf = await cloud.client.get_google_config()
            google = self.controller.components.google_assistant
            if isinstance(google, core.GoogleAssistantComponent):
                entities = google.async_get_entities(gconf)
            else:
                entities = []

            result = []

            for entity in entities:
                result.append(
                    {
                        "entity_id": entity.entity_id,
                        "traits": [trait.name for trait in entity.traits()],
                        "might_2fa": entity.might_2fa_traits(),
                    }
                )

            connection.send_result(msg["id"], result)

    @_ws_handle_cloud_errors
    async def _cloud_assistant_update(
        self,
        connection: core.WebSocket.Connection,
        msg: dict,
    ):
        """Update google assistant config."""
        connection.require_admin()
        if self._check_cloud_auth(connection, msg):
            cloud = self._cloud
            changes = dict(msg)
            changes.pop("type")
            changes.pop("id")

            await cloud.client.prefs.async_update_google_entity_config(**changes)

            connection.send_result(
                msg["id"],
                cloud.client.prefs.google_entity_configs.get(msg["entity_id"]),
            )

    @_ws_handle_cloud_errors
    async def _cloud_alexa_list(
        self,
        connection: core.WebSocket.Connection,
        msg: dict,
    ):
        """List all alexa entities."""
        connection.require_admin()
        if self._check_cloud_auth(connection, msg):
            cloud = self._cloud
            alexa_config = await cloud.client.get_alexa_config()
            alexa = self.controller.components.alexa
            if isinstance(alexa, core.AlexaComponent):
                entities = alexa.async_get_entities(alexa_config)
            else:
                entities = []

            result = []

            for entity in entities:
                result.append(
                    {
                        "entity_id": entity.entity_id,
                        "display_categories": entity.default_display_categories(),
                        "interfaces": [ifc.name() for ifc in entity.interfaces()],
                    }
                )

            connection.send_result(msg["id"], result)

    @_ws_handle_cloud_errors
    async def _cloud_alexa_update(
        self,
        connection: core.WebSocket.Connection,
        msg: dict,
    ):
        """Update alexa entity config."""
        connection.require_admin()
        if self._check_cloud_auth(connection, msg):
            cloud = self._cloud
            changes = dict(msg)
            changes.pop("type")
            changes.pop("id")

            await cloud.client.prefs.async_update_alexa_entity_config(**changes)

            connection.send_result(
                msg["id"], cloud.client.prefs.alexa_entity_configs.get(msg["entity_id"])
            )

    async def _cloud_alexa_sync(
        self,
        connection: core.WebSocket.Connection,
        msg: dict,
    ):
        """Sync with Alexa."""
        connection.require_admin()
        if self._check_cloud_auth(connection, msg):
            cloud = self._cloud
            alexa_config = await cloud.client.get_alexa_config()

            async with async_timeout.timeout(10):
                try:
                    success = await alexa_config.async_sync_entities()
                except core.NoTokenAvailable:
                    connection.send_error(
                        msg["id"],
                        "alexa_relink",
                        "Please go to the Alexa app and re-link the Home Assistant skill.",
                    )
                    return

            if success:
                connection.send_result(msg["id"])
            else:
                connection.send_error(
                    msg["id"], core.WebSocket.ERR_UNKNOWN_ERROR, "Unknown error"
                )

    async def _cloud_thingtalk_convert(
        self,
        connection: core.WebSocket.Connection,
        msg: dict,
    ):
        """Convert a query."""

        cloud = self._cloud

        async with async_timeout.timeout(10):
            try:
                connection.send_result(
                    msg["id"],
                    await _thingtalk.async_convert(cloud, msg["query"]),
                )
            except _thingtalk.ThingTalkConversionError as err:
                connection.send_error(
                    msg["id"], core.WebSocket.ERR_UNKNOWN_ERROR, str(err)
                )

    def _cloud_tts_info(hass, connection, msg):
        """Fetch available tts info."""
        connection.send_result(
            msg["id"],
            {
                "languages": [
                    (lang, gender.value) for lang, gender in nabucasa.voice.MAP_VOICE
                ]
            },
        )


async def _account_data(shc: core.SmartHomeController, cloud: nabucasa.Cloud):
    """Generate the auth data JSON response."""

    assert shc.config.api
    if not cloud.is_logged_in:
        return {
            "logged_in": False,
            "cloud": nabucasa.const.STATE_DISCONNECTED,
            "http_use_ssl": shc.config.api.use_ssl,
        }

    claims = cloud.claims
    client = cloud.client
    remote = cloud.remote

    alexa_config = await client.get_alexa_config()
    google_config = await client.get_google_config()

    # Load remote certificate
    if remote.certificate:
        certificate = attr.asdict(remote.certificate)
    else:
        certificate = None

    if cloud.iot.last_disconnect_reason:
        cloud_last_disconnect_reason = dataclasses.asdict(
            cloud.iot.last_disconnect_reason
        )
    else:
        cloud_last_disconnect_reason = None

    return {
        "alexa_entities": client.alexa_user_config["filter"].config,
        "alexa_registered": alexa_config.authorized,
        "cloud": cloud.iot.state,
        "cloud_last_disconnect_reason": cloud_last_disconnect_reason,
        "email": claims["email"],
        "google_entities": client.google_user_config["filter"].config,
        "google_registered": google_config.has_registered_user_agent,
        "google_local_connected": google_config.is_local_connected,
        "logged_in": True,
        "prefs": client.prefs.as_dict(),
        "remote_certificate": certificate,
        "remote_connected": remote.is_connected,
        "remote_domain": remote.instance_domain,
        "http_use_ssl": shc.config.api.use_ssl,
        "active_subscription": not cloud.subscription_expired,
    }


@core.callback
def _remote_handle_prefs_updated(cloud: nabucasa.Cloud) -> None:
    """Handle remote preferences updated."""
    cur_pref = cloud.client.prefs.remote_enabled
    lock = asyncio.Lock()

    # Sync remote connection with prefs
    async def remote_prefs_updated(prefs: CloudPreferences) -> None:
        """Update remote status."""
        nonlocal cur_pref

        async with lock:
            if prefs.remote_enabled == cur_pref:
                return

            if cur_pref := prefs.remote_enabled:
                await cloud.remote.connect()
            else:
                await cloud.remote.disconnect()

    cloud.client.prefs.async_listen_updates(remote_prefs_updated)
