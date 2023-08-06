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

import typing


# pylint: disable=unused-variable
class Const:
    """Constants for the cloud component."""

    REQUEST_TIMEOUT: typing.Final = 10

    PREF_ENABLE_ALEXA: typing.Final = "alexa_enabled"
    PREF_ENABLE_GOOGLE: typing.Final = "google_enabled"
    PREF_ENABLE_REMOTE: typing.Final = "remote_enabled"
    PREF_GOOGLE_SECURE_DEVICES_PIN: typing.Final = "google_secure_devices_pin"
    PREF_CLOUDHOOKS: typing.Final = "cloudhooks"
    PREF_CLOUD_USER: typing.Final = "cloud_user"
    PREF_GOOGLE_ENTITY_CONFIGS: typing.Final = "google_entity_configs"
    PREF_GOOGLE_REPORT_STATE: typing.Final = "google_report_state"
    PREF_ALEXA_ENTITY_CONFIGS: typing.Final = "alexa_entity_configs"
    PREF_ALEXA_REPORT_STATE: typing.Final = "alexa_report_state"
    PREF_OVERRIDE_NAME: typing.Final = "override_name"
    PREF_DISABLE_2FA: typing.Final = "disable_2fa"
    PREF_ALIASES: typing.Final = "aliases"
    PREF_SHOULD_EXPOSE: typing.Final = "should_expose"
    PREF_GOOGLE_LOCAL_WEBHOOK_ID: typing.Final = "google_local_webhook_id"
    PREF_USERNAME: typing.Final = "username"
    PREF_REMOTE_DOMAIN: typing.Final = "remote_domain"
    PREF_ALEXA_DEFAULT_EXPOSE: typing.Final = "alexa_default_expose"
    PREF_GOOGLE_DEFAULT_EXPOSE: typing.Final = "google_default_expose"
    PREF_TTS_DEFAULT_VOICE: typing.Final = "tts_default_voice"
    DEFAULT_TTS_DEFAULT_VOICE: typing.Final = ("en-US", "female")
    DEFAULT_DISABLE_2FA: typing.Final = False
    DEFAULT_ALEXA_REPORT_STATE: typing.Final = True
    DEFAULT_GOOGLE_REPORT_STATE: typing.Final = True
    DEFAULT_EXPOSED_DOMAINS: typing.Final = [
        "climate",
        "cover",
        "fan",
        "humidifier",
        "light",
        "lock",
        "scene",
        "script",
        "sensor",
        "switch",
        "vacuum",
        "water_heater",
    ]

    CONF_ALEXA: typing.Final = "alexa"
    CONF_ALIASES: typing.Final = "aliases"
    CONF_COGNITO_CLIENT_ID: typing.Final = "cognito_client_id"
    CONF_ENTITY_CONFIG: typing.Final = "entity_config"
    CONF_FILTER: typing.Final = "filter"
    CONF_GOOGLE_ACTIONS: typing.Final = "google_actions"
    CONF_RELAYER: typing.Final = "relayer"
    CONF_USER_POOL_ID: typing.Final = "user_pool_id"
    CONF_SUBSCRIPTION_INFO_URL: typing.Final = "subscription_info_url"
    CONF_CLOUDHOOK_CREATE_URL: typing.Final = "cloudhook_create_url"
    CONF_REMOTE_API_URL: typing.Final = "remote_api_url"
    CONF_ACME_DIRECTORY_SERVER: typing.Final = "acme_directory_server"
    CONF_ALEXA_ACCESS_TOKEN_URL: typing.Final = "alexa_access_token_url"
    CONF_GOOGLE_ACTIONS_REPORT_STATE_URL: typing.Final = (
        "google_actions_report_state_url"
    )
    CONF_ACCOUNT_LINK_URL: typing.Final = "account_link_url"
    CONF_VOICE_API_URL: typing.Final = "voice_api_url"

    MODE_DEV: typing.Final = "development"
    MODE_PROD: typing.Final = "production"

    DISPATCHER_REMOTE_UPDATE: typing.Final = "cloud_remote_update"
