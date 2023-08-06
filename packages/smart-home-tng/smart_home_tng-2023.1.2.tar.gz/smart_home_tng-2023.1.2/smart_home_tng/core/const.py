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

import collections.abc
import functools
import json
import re
import typing

import aiohttp.hdrs

from ..backports import strenum
from .. import __about__
from .json_encoder import JsonEncoder


# pylint: disable=unused-variable
class Const:
    """global constants for Smart Home - The Next Generation"""

    __version__: typing.Final = __about__.__version__
    REQUIRED_PYTHON_VER: typing.Final[tuple[int, int, int]] = (3, 11, 0)
    REQUIRED_NEXT_PYTHON_VER: typing.Final[tuple[int, int, int]] = (3, 11, 0)
    # Truthy date string triggers showing related deprecation warning messages.
    REQUIRED_NEXT_PYTHON_SHC_RELEASE: typing.Final = ""

    # Format for platform files
    PLATFORM_FORMAT: typing.Final = "{platform}.{domain}"

    # Can be used to specify a catch all when registering state or event listeners.
    MATCH_ALL: typing.Final = "*"

    # Entity target all constant
    ENTITY_MATCH_NONE: typing.Final = "none"
    ENTITY_MATCH_ALL: typing.Final = "all"
    ENTITY_MATCH_ANY: typing.Final = "any"

    # If no name is specified
    DEVICE_DEFAULT_NAME: typing.Final = "Unnamed Device"

    # Max characters for data stored in the recorder (changes to these limits would require
    # a database migration)
    MAX_LENGTH_EVENT_EVENT_TYPE: typing.Final = 64
    MAX_LENGTH_EVENT_ORIGIN: typing.Final = 32
    MAX_LENGTH_EVENT_CONTEXT_ID: typing.Final = 36
    MAX_LENGTH_STATE_DOMAIN: typing.Final = 64
    MAX_LENGTH_STATE_ENTITY_ID: typing.Final = 255
    MAX_LENGTH_STATE_STATE: typing.Final = 255

    MAX_LOAD_CONCURRENTLY: typing.Final = 4
    MAX_EXPECTED_ENTITY_IDS: typing.Final = 16384
    SHUTDOWN_RUN_CALLBACK_THREADSAFE: typing.Final = "_shutdown_run_callback_threadsafe"

    # Sun events
    SUN_EVENT_SUNSET: typing.Final = "sunset"
    SUN_EVENT_SUNRISE: typing.Final = "sunrise"

    # Cache Headers
    CACHE_TIME: typing.Final = 31 * 86400  # = 1 month
    CACHE_HEADERS: typing.Final[collections.abc.Mapping[str, str]] = {
        aiohttp.hdrs.CACHE_CONTROL: f"public, max-age={CACHE_TIME}"
    }

    CONF_SERVER_HOST: typing.Final = "server_host"
    CONF_SERVER_PORT: typing.Final = "server_port"
    CONF_BASE_URL: typing.Final = "base_url"
    CONF_SSL_CERTIFICATE: typing.Final = "ssl_certificate"
    CONF_SSL_PEER_CERTIFICATE: typing.Final = "ssl_peer_certificate"
    CONF_SSL_KEY: typing.Final = "ssl_key"
    CONF_CORS_ORIGINS: typing.Final = "cors_allowed_origins"
    CONF_USE_X_FORWARDED_FOR: typing.Final = "use_x_forwarded_for"
    CONF_TRUSTED_PROXIES: typing.Final = "trusted_proxies"
    CONF_LOGIN_ATTEMPTS_THRESHOLD: typing.Final = "login_attempts_threshold"
    CONF_IP_BAN_ENABLED: typing.Final = "ip_ban_enabled"
    CONF_SSL_PROFILE: typing.Final = "ssl_profile"

    SSL_MODERN: typing.Final = "modern"
    SSL_INTERMEDIATE: typing.Final = "intermediate"

    # #### CONFIG ####
    CONF_ABOVE: typing.Final = "above"
    CONF_ACCESS_TOKEN: typing.Final = "access_token"
    CONF_ADDRESS: typing.Final = "address"
    CONF_AFTER: typing.Final = "after"
    CONF_ALIAS: typing.Final = "alias"
    CONF_ALLOWLIST_EXTERNAL_URLS: typing.Final = "allowlist_external_urls"
    CONF_API_KEY: typing.Final = "api_key"
    CONF_API_TOKEN: typing.Final = "api_token"
    CONF_API_VERSION: typing.Final = "api_version"
    CONF_ARMING_TIME: typing.Final = "arming_time"
    CONF_AT: typing.Final = "at"
    CONF_ATTRIBUTE: typing.Final = "attribute"
    CONF_AUTH_MFA_MODULES: typing.Final = "auth_mfa_modules"
    CONF_AUTH_PROVIDERS: typing.Final = "auth_providers"
    CONF_AUTHENTICATION: typing.Final = "authentication"
    CONF_BASE: typing.Final = "base"
    CONF_BEFORE: typing.Final = "before"
    CONF_BELOW: typing.Final = "below"
    CONF_BINARY_SENSORS: typing.Final = "binary_sensors"
    CONF_BRIGHTNESS: typing.Final = "brightness"
    CONF_BROADCAST_ADDRESS: typing.Final = "broadcast_address"
    CONF_BROADCAST_PORT: typing.Final = "broadcast_port"
    CONF_CHOOSE: typing.Final = "choose"
    CONF_CLIENT_ID: typing.Final = "client_id"
    CONF_CLIENT_SECRET: typing.Final = "client_secret"
    CONF_CODE: typing.Final = "code"
    CONF_COLOR_TEMP: typing.Final = "color_temp"
    CONF_COMMAND: typing.Final = "command"
    CONF_COMMAND_CLOSE: typing.Final = "command_close"
    CONF_COMMAND_OFF: typing.Final = "command_off"
    CONF_COMMAND_ON: typing.Final = "command_on"
    CONF_COMMAND_OPEN: typing.Final = "command_open"
    CONF_COMMAND_STATE: typing.Final = "command_state"
    CONF_COMMAND_STOP: typing.Final = "command_stop"
    CONF_COMPONENTS: typing.Final = "components"
    CONF_CONDITION: typing.Final = "condition"
    CONF_CONDITIONS: typing.Final = "conditions"
    CONF_CONFIG_DIR: typing.Final = "config_dir"
    CONF_CONFIG_SOURCE: typing.Final = "config_source"
    CONF_CONTINUE_ON_ERROR: typing.Final = "continue_on_error"
    CONF_CONTINUE_ON_TIMEOUT: typing.Final = "continue_on_timeout"
    CONF_COUNT: typing.Final = "count"
    CONF_COVERS: typing.Final = "covers"
    CONF_CURRENCY: typing.Final = "currency"
    CONF_CUSTOMIZE: typing.Final = "customize"
    CONF_CUSTOMIZE_DOMAIN: typing.Final = "customize_domain"
    CONF_CUSTOMIZE_GLOB: typing.Final = "customize_glob"
    CONF_DEFAULT: typing.Final = "default"
    CONF_DELAY: typing.Final = "delay"
    CONF_DELAY_TIME: typing.Final = "delay_time"
    CONF_DESCRIPTION: typing.Final = "description"
    CONF_DEVICE: typing.Final = "device"
    CONF_DEVICES: typing.Final = "devices"
    CONF_DEVICE_CLASS: typing.Final = "device_class"
    CONF_DEVICE_ID: typing.Final = "device_id"
    CONF_DISARM_AFTER_TRIGGER: typing.Final = "disarm_after_trigger"
    CONF_DISCOVERY: typing.Final = "discovery"
    CONF_DISKS: typing.Final = "disks"
    CONF_DISPLAY_CURRENCY: typing.Final = "display_currency"
    CONF_DISPLAY_OPTIONS: typing.Final = "display_options"
    CONF_DOMAIN: typing.Final = "domain"
    CONF_DOMAINS: typing.Final = "domains"
    CONF_EFFECT: typing.Final = "effect"
    CONF_ELEVATION: typing.Final = "elevation"
    CONF_ELSE: typing.Final = "else"
    CONF_EMAIL: typing.Final = "email"
    CONF_ENABLED: typing.Final = "enabled"
    CONF_ENTITIES: typing.Final = "entities"
    CONF_ENTITY_CATEGORY: typing.Final = "entity_category"
    CONF_ENTITY_ID: typing.Final = "entity_id"
    CONF_ENTITY_NAMESPACE: typing.Final = "entity_namespace"
    CONF_ENTITY_PICTURE_TEMPLATE: typing.Final = "entity_picture_template"
    CONF_ERROR: typing.Final = "error"
    CONF_EVENT: typing.Final = "event"
    CONF_EVENT_DATA: typing.Final = "event_data"
    CONF_EVENT_DATA_TEMPLATE: typing.Final = "event_data_template"
    CONF_EXCLUDE: typing.Final = "exclude"
    CONF_EXTERNAL_URL: typing.Final = "external_url"
    CONF_FILENAME: typing.Final = "filename"
    CONF_FILE_PATH: typing.Final = "file_path"
    CONF_FOR: typing.Final = "for"
    CONF_FOR_EACH: typing.Final = "for_each"
    CONF_FORCE_UPDATE: typing.Final = "force_update"
    CONF_FRIENDLY_NAME: typing.Final = "friendly_name"
    CONF_FRIENDLY_NAME_TEMPLATE: typing.Final = "friendly_name_template"
    CONF_HEADERS: typing.Final = "headers"
    CONF_HOST: typing.Final = "host"
    CONF_HOSTS: typing.Final = "hosts"
    CONF_HS: typing.Final = "hs"
    CONF_ICON: typing.Final = "icon"
    CONF_ICON_TEMPLATE: typing.Final = "icon_template"
    CONF_ID: typing.Final = "id"
    CONF_IF: typing.Final = "if"
    CONF_INCLUDE: typing.Final = "include"
    CONF_INTERNAL_URL: typing.Final = "internal_url"
    CONF_IP_ADDRESS: typing.Final = "ip_address"
    CONF_LATITUDE: typing.Final = "latitude"
    CONF_LEGACY_TEMPLATES: typing.Final = "legacy_templates"
    CONF_LIGHTS: typing.Final = "lights"
    CONF_LOCATION: typing.Final = "location"
    CONF_LOCATION_NAME: typing.Final = "location_name"
    CONF_LONGITUDE: typing.Final = "longitude"
    CONF_MAC: typing.Final = "mac"
    CONF_MATCH: typing.Final = "match"
    CONF_MAXIMUM: typing.Final = "maximum"
    CONF_MEDIA_DIRS: typing.Final = "media_dirs"
    CONF_METHOD: typing.Final = "method"
    CONF_MINIMUM: typing.Final = "minimum"
    CONF_MODE: typing.Final = "mode"
    CONF_MODEL: typing.Final = "model"
    CONF_MONITORED_CONDITIONS: typing.Final = "monitored_conditions"
    CONF_MONITORED_VARIABLES: typing.Final = "monitored_variables"
    CONF_NAME: typing.Final = "name"
    CONF_OFFSET: typing.Final = "offset"
    CONF_OPTIMISTIC: typing.Final = "optimistic"
    CONF_PACKAGES: typing.Final = "packages"
    CONF_PARALLEL: typing.Final = "parallel"
    CONF_PARAMS: typing.Final = "params"
    CONF_PASSWORD: typing.Final = "password"
    CONF_PATH: typing.Final = "path"
    CONF_PAYLOAD: typing.Final = "payload"
    CONF_PAYLOAD_OFF: typing.Final = "payload_off"
    CONF_PAYLOAD_ON: typing.Final = "payload_on"
    CONF_PENDING_TIME: typing.Final = "pending_time"
    CONF_PIN: typing.Final = "pin"
    CONF_PLATFORM: typing.Final = "platform"
    CONF_PORT: typing.Final = "port"
    CONF_PREFIX: typing.Final = "prefix"
    CONF_PROFILE_NAME: typing.Final = "profile_name"
    CONF_PROTOCOL: typing.Final = "protocol"
    CONF_PROXY_SSL: typing.Final = "proxy_ssl"
    CONF_QUOTE: typing.Final = "quote"
    CONF_RADIUS: typing.Final = "radius"
    CONF_RECIPIENT: typing.Final = "recipient"
    CONF_REGION: typing.Final = "region"
    CONF_REPEAT: typing.Final = "repeat"
    CONF_RESOURCE: typing.Final = "resource"
    CONF_RESOURCES: typing.Final = "resources"
    CONF_RESOURCE_TEMPLATE: typing.Final = "resource_template"
    CONF_RGB: typing.Final = "rgb"
    CONF_ROOM: typing.Final = "room"
    CONF_SAFE_MODE: typing.Final = "safe_mode"
    CONF_SCAN_INTERVAL: typing.Final = "scan_interval"
    CONF_SCENE: typing.Final = "scene"
    CONF_SELECTOR: typing.Final = "selector"
    CONF_SENDER: typing.Final = "sender"
    CONF_SENSORS: typing.Final = "sensors"
    CONF_SENSOR_TYPE: typing.Final = "sensor_type"
    CONF_SEQUENCE: typing.Final = "sequence"
    CONF_SERVICE: typing.Final = "service"
    CONF_SERVICE_DATA: typing.Final = "data"
    CONF_SERVICE_DATA_TEMPLATE: typing.Final = "data_template"
    CONF_SERVICE_TEMPLATE: typing.Final = "service_template"
    CONF_SHOW_ON_MAP: typing.Final = "show_on_map"
    CONF_SLAVE: typing.Final = "slave"
    CONF_SOURCE: typing.Final = "source"
    CONF_SSL: typing.Final = "ssl"
    CONF_STATE: typing.Final = "state"
    CONF_STATE_TEMPLATE: typing.Final = "state_template"
    CONF_STATES: typing.Final = "states"
    CONF_STOP: typing.Final = "stop"
    CONF_STORED_TRACES: typing.Final = "stored_traces"
    CONF_STRUCTURE: typing.Final = "structure"
    CONF_SWITCHES: typing.Final = "switches"
    CONF_TARGET: typing.Final = "target"
    CONF_TEMPERATURE_UNIT: typing.Final = "temperature_unit"
    CONF_THEN: typing.Final = "then"
    CONF_TIMEOUT: typing.Final = "timeout"
    CONF_TIME_ZONE: typing.Final = "time_zone"
    CONF_TOKEN: typing.Final = "token"
    CONF_TOTP: typing.Final = "totp"
    CONF_TRIGGER_TIME: typing.Final = "trigger_time"
    CONF_TTL: typing.Final = "ttl"
    CONF_TYPE: typing.Final = "type"
    CONF_UNIQUE_ID: typing.Final = "unique_id"
    CONF_UNIT_OF_MEASUREMENT: typing.Final = "unit_of_measurement"
    CONF_UNIT_SYSTEM: typing.Final = "unit_system"
    CONF_UNTIL: typing.Final = "until"
    CONF_URL: typing.Final = "url"
    CONF_USERNAME: typing.Final = "username"
    CONF_VALUE_TEMPLATE: typing.Final = "value_template"
    CONF_VARIABLES: typing.Final = "variables"
    CONF_VERIFY_SSL: typing.Final = "verify_ssl"
    CONF_VERSION: typing.Final = "version"
    CONF_WAIT_FOR_TRIGGER: typing.Final = "wait_for_trigger"
    CONF_WAIT_TEMPLATE: typing.Final = "wait_template"
    CONF_WEBHOOK_ID: typing.Final = "webhook_id"
    CONF_WEEKDAY: typing.Final = "weekday"
    CONF_WHILE: typing.Final = "while"
    CONF_WHITELIST: typing.Final = "whitelist"
    CONF_ALLOWLIST_EXTERNAL_DIRS: typing.Final = "allowlist_external_dirs"
    LEGACY_CONF_WHITELIST_EXTERNAL_DIRS: typing.Final = "whitelist_external_dirs"
    CONF_WHITE_VALUE: typing.Final = "white_value"
    CONF_XY: typing.Final = "xy"
    CONF_ZONE: typing.Final = "zone"

    # #### EVENTS ####
    EVENT_COLLECTION_CHANGE_ADDED: typing.Final = "collection.added"
    EVENT_COLLECTION_CHANGE_UPDATED: typing.Final = "collection.updated"
    EVENT_COLLECTION_CHANGE_REMOVED: typing.Final = "collection.removed"

    EVENT_CALL_SERVICE: typing.Final = "service.call"
    EVENT_COMPONENT_LOADED: typing.Final = "component.loaded"
    EVENT_CORE_CONFIG_UPDATE: typing.Final = "core_config.updated"
    EVENT_SHC_CLOSE: typing.Final = "smart_home_tng.close"
    EVENT_SHC_START: typing.Final = "smart_home_tng.start"
    EVENT_SHC_STARTED: typing.Final = "smart_home_tng.started"
    EVENT_SHC_STOP: typing.Final = "smart_home_tng.stop"
    EVENT_SHC_FINAL_WRITE: typing.Final = "smart_home_tng.final_write"
    EVENT_LOGBOOK_ENTRY: typing.Final = "logbook.entry"
    EVENT_SERVICE_REGISTERED: typing.Final = "service.registered"
    EVENT_SERVICE_REMOVED: typing.Final = "service.removed"
    EVENT_STATE_CHANGED: typing.Final = "state.changed"
    EVENT_THEMES_UPDATED: typing.Final = "themes.updated"
    EVENT_AREA_REGISTRY_UPDATED: typing.Final = "area_registry.updated"
    EVENT_DEVICE_REGISTRY_UPDATED: typing.Final = "device_registry.updated"
    EVENT_ENTITY_REGISTRY_UPDATED: typing.Final = "entity_registry.updated"
    CONFIG_ENTRY_RECONFIGURE_NOTIFICATION_ID: typing.Final = "config_entry.reconfigure"

    # #### DEVICE CLASSES ####
    # DEVICE_CLASS_* below are deprecated as of 2021.12
    # use the SensorDeviceClass enum instead.
    DEVICE_CLASS_AQI: typing.Final = "aqi"
    DEVICE_CLASS_BATTERY: typing.Final = "battery"
    DEVICE_CLASS_CO: typing.Final = "carbon_monoxide"
    DEVICE_CLASS_CO2: typing.Final = "carbon_dioxide"
    DEVICE_CLASS_CURRENT: typing.Final = "current"
    DEVICE_CLASS_DATE: typing.Final = "date"
    DEVICE_CLASS_ENERGY: typing.Final = "energy"
    DEVICE_CLASS_FREQUENCY: typing.Final = "frequency"
    DEVICE_CLASS_GAS: typing.Final = "gas"
    DEVICE_CLASS_HUMIDITY: typing.Final = "humidity"
    DEVICE_CLASS_ILLUMINANCE: typing.Final = "illuminance"
    DEVICE_CLASS_MONETARY: typing.Final = "monetary"
    DEVICE_CLASS_NITROGEN_DIOXIDE: typing.Final = "nitrogen_dioxide"
    DEVICE_CLASS_NITROGEN_MONOXIDE: typing.Final = "nitrogen_monoxide"
    DEVICE_CLASS_NITROUS_OXIDE: typing.Final = "nitrous_oxide"
    DEVICE_CLASS_OZONE: typing.Final = "ozone"
    DEVICE_CLASS_PM1: typing.Final = "pm1"
    DEVICE_CLASS_PM10: typing.Final = "pm10"
    DEVICE_CLASS_PM25: typing.Final = "pm25"
    DEVICE_CLASS_POWER_FACTOR: typing.Final = "power_factor"
    DEVICE_CLASS_POWER: typing.Final = "power"
    DEVICE_CLASS_PRESSURE: typing.Final = "pressure"
    DEVICE_CLASS_SIGNAL_STRENGTH: typing.Final = "signal_strength"
    DEVICE_CLASS_SULPHUR_DIOXIDE: typing.Final = "sulphur_dioxide"
    DEVICE_CLASS_TEMPERATURE: typing.Final = "temperature"
    DEVICE_CLASS_TIMESTAMP: typing.Final = "timestamp"
    DEVICE_CLASS_VOLATILE_ORGANIC_COMPOUNDS: typing.Final = "volatile_organic_compounds"
    DEVICE_CLASS_VOLTAGE: typing.Final = "voltage"

    # #### NextGenerationHttp Keys ####
    KEY_AUTHENTICATED: typing.Final = "shc.authenticated"
    KEY_SHC: typing.Final = "shc"
    KEY_SHC_USER: typing.Final = "shc.user"
    KEY_SHC_REFRESH_TOKEN_ID: typing.Final = "shc.refresh_token_id"
    KEY_BANNED_IPS: typing.Final = "shc.banned_ips"
    KEY_FAILED_LOGIN_ATTEMPTS: typing.Final = "shc.failed_login_attempts"
    KEY_LOGIN_THRESHOLD: typing.Final = "shc.login_threshold"

    NOTIFICATION_ID_BAN: typing.Final = "ip-ban"
    NOTIFICATION_ID_LOGIN: typing.Final = "http-login"
    NOTIFICATION_ID_INVALID_CONFIG: typing.Final = "invalid-config"

    IP_BANS_FILE: typing.Final = "ip_bans.yaml"
    ATTR_BANNED_AT: typing.Final = "banned_at"
    ATTR_COMPONENT: typing.Final = "component"

    SECRET_YAML: typing.Final = "secrets.yaml"

    # #### STATES ####
    STATE_ON: typing.Final = "on"
    STATE_OFF: typing.Final = "off"
    STATE_HOME: typing.Final = "home"
    STATE_NOT_HOME: typing.Final = "not_home"
    STATE_UNKNOWN: typing.Final = "unknown"
    STATE_OPEN: typing.Final = "open"
    STATE_OPENING: typing.Final = "opening"
    STATE_CLOSED: typing.Final = "closed"
    STATE_CLOSING: typing.Final = "closing"
    STATE_BUFFERING: typing.Final = "buffering"
    STATE_PLAYING: typing.Final = "playing"
    STATE_PAUSED: typing.Final = "paused"
    STATE_IDLE: typing.Final = "idle"
    STATE_STANDBY: typing.Final = "standby"
    STATE_ALARM_DISARMED: typing.Final = "disarmed"
    STATE_ALARM_ARMED_HOME: typing.Final = "armed_home"
    STATE_ALARM_ARMED_AWAY: typing.Final = "armed_away"
    STATE_ALARM_ARMED_NIGHT: typing.Final = "armed_night"
    STATE_ALARM_ARMED_VACATION: typing.Final = "armed_vacation"
    STATE_ALARM_ARMED_CUSTOM_BYPASS: typing.Final = "armed_custom_bypass"
    STATE_ALARM_PENDING: typing.Final = "pending"
    STATE_ALARM_ARMING: typing.Final = "arming"
    STATE_ALARM_DISARMING: typing.Final = "disarming"
    STATE_ALARM_TRIGGERED: typing.Final = "triggered"
    STATE_LOCKED: typing.Final = "locked"
    STATE_UNLOCKED: typing.Final = "unlocked"
    STATE_LOCKING: typing.Final = "locking"
    STATE_UNLOCKING: typing.Final = "unlocking"
    STATE_JAMMED: typing.Final = "jammed"
    STATE_UNAVAILABLE: typing.Final = "unavailable"
    STATE_OK: typing.Final = "ok"
    STATE_PROBLEM: typing.Final = "problem"

    # #### STATE AND EVENT ATTRIBUTES ####
    # Attribution
    ATTR_ATTRIBUTION: typing.Final = "attribution"

    # Credentials
    ATTR_CREDENTIALS: typing.Final = "credentials"

    # Contains time-related attributes
    ATTR_NOW: typing.Final = "now"
    ATTR_DATE: typing.Final = "date"
    ATTR_TIME: typing.Final = "time"
    ATTR_SECONDS: typing.Final = "seconds"

    # Contains domain, service for a SERVICE_CALL event
    ATTR_DOMAIN: typing.Final = "domain"
    ATTR_SERVICE: typing.Final = "service"
    ATTR_SERVICE_DATA: typing.Final = "service_data"
    ATTR_SOURCE_TYPE: typing.Final = "source_type"

    # Notfify Component
    ATTR_DATA: typing.Final = "data"

    # Text to notify user of
    ATTR_MESSAGE: typing.Final = "message"

    # Target of the notification (user, device, etc)
    ATTR_TARGET: typing.Final = "target"

    # Title of notification
    ATTR_TITLE: typing.Final = "title"

    # IDs
    ATTR_ID: typing.Final = "id"

    # Name
    ATTR_NAME: typing.Final = "name"

    # Contains one string or a list of strings, each being an entity id
    ATTR_ENTITY_ID: typing.Final = "entity_id"

    # Contains one string or a list of strings, each being an area id
    ATTR_AREA_ID: typing.Final = "area_id"

    # Contains one string, the device ID
    ATTR_DEVICE_ID: typing.Final = "device_id"

    # String with a friendly name for the entity
    ATTR_FRIENDLY_NAME: typing.Final = "friendly_name"

    # A picture to represent entity
    ATTR_ENTITY_PICTURE: typing.Final = "entity_picture"

    ATTR_IDENTIFIERS: typing.Final = "identifiers"

    # Icon to use in the frontend
    ATTR_ICON: typing.Final = "icon"

    # The unit of measurement if applicable
    ATTR_UNIT_OF_MEASUREMENT: typing.Final = "unit_of_measurement"

    CONF_UNIT_SYSTEM_METRIC: typing.Final = "metric"
    CONF_UNIT_SYSTEM_IMPERIAL: typing.Final = "imperial"

    # Electrical attributes
    ATTR_VOLTAGE: typing.Final = "voltage"

    # Location of the device/sensor
    ATTR_LOCATION: typing.Final = "location"

    ATTR_MODE: typing.Final = "mode"

    ATTR_CONFIGURATION_URL: typing.Final = "configuration_url"
    ATTR_CONNECTIONS: typing.Final = "connections"
    ATTR_DEFAULT_NAME: typing.Final = "default_name"
    ATTR_MANUFACTURER: typing.Final = "manufacturer"
    ATTR_MODEL: typing.Final = "model"
    ATTR_SUGGESTED_AREA: typing.Final = "suggested_area"
    ATTR_SW_VERSION: typing.Final = "sw_version"
    ATTR_HW_VERSION: typing.Final = "hw_version"
    ATTR_VIA_DEVICE: typing.Final = "via_device"

    ATTR_BATTERY: typing.Final = "battery"
    ATTR_BATTERY_CHARGING: typing.Final = "battery_charging"
    ATTR_BATTERY_LEVEL: typing.Final = "battery_level"
    ATTR_WAKEUP: typing.Final = "wake_up_interval"

    # For devices which support a code attribute
    ATTR_CODE: typing.Final = "code"
    ATTR_CODE_FORMAT: typing.Final = "code_format"

    # For calling a device specific command
    ATTR_COMMAND: typing.Final = "command"

    # For devices which support an armed state
    ATTR_ARMED: typing.Final = "device_armed"

    # For devices which support a locked state
    ATTR_LOCKED: typing.Final = "locked"

    # For sensors that support 'tripping', eg. motion and door sensors
    ATTR_TRIPPED: typing.Final = "device_tripped"

    # For sensors that support 'tripping' this holds the most recent
    # time the device was tripped
    ATTR_LAST_TRIP_TIME: typing.Final = "last_tripped_time"

    # For all entity's, this hold whether or not it should be hidden
    ATTR_HIDDEN: typing.Final = "hidden"

    # Location of the entity
    ATTR_LATITUDE: typing.Final = "latitude"
    ATTR_LONGITUDE: typing.Final = "longitude"

    # Accuracy of location in meters
    ATTR_GPS_ACCURACY: typing.Final = "gps_accuracy"
    ATTR_GPS: typing.Final = "gps"

    ATTR_LOCATION_NAME: typing.Final = "location_name"

    # If state is assumed
    ATTR_ASSUMED_STATE: typing.Final = "assumed_state"
    ATTR_STATE: typing.Final = "state"

    ATTR_EDITABLE: typing.Final = "editable"

    # The entity has been restored with restore state
    ATTR_RESTORED: typing.Final = "restored"

    # Bitfield of supported component features for the entity
    ATTR_SUPPORTED_FEATURES: typing.Final = "supported_features"

    # Class of device within its domain
    ATTR_DEVICE_CLASS: typing.Final = "device_class"

    # Temperature attribute
    ATTR_TEMPERATURE: typing.Final = "temperature"

    # Persons attribute
    ATTR_PERSONS: typing.Final = "persons"

    ATTR_HOST_NAME: typing.Final = "host_name"
    ATTR_IP: typing.Final = "ip"
    ATTR_MAC: typing.Final = "mac"

    # Float that represents transition time in seconds to make change.
    ATTR_TRANSITION: typing.Final = "transition"

    # #### UNITS OF MEASUREMENT ####
    # Apparent power units
    class UnitOfApparentPower(strenum.StrEnum):
        """Apparent power units."""

        VOLT_AMPERE = "VA"

    # Power units
    class UnitOfPower(strenum.StrEnum):
        """Power units."""

        WATT = "W"
        KILO_WATT = "kW"
        BTU_PER_HOUR = "BTU/h"

    # Reactive power units
    POWER_VOLT_AMPERE_REACTIVE: typing.Final = "var"

    # Energy units
    class UnitOfEnergy(strenum.StrEnum):
        """Energy units."""

        GIGA_JOULE = "GJ"
        KILO_WATT_HOUR = "kWh"
        MEGA_JOULE = "MJ"
        MEGA_WATT_HOUR = "MWh"
        WATT_HOUR = "Wh"

    class UnitOfElectricCurrent(strenum.StrEnum):
        """Electric current units."""

        MILLIAMPERE = "mA"
        AMPERE = "A"

    class UnitOfElectricPotential(strenum.StrEnum):
        """Electric potential units."""

        MILLIVOLT = "mV"
        VOLT = "V"

    # Degree units
    DEGREE: typing.Final = "°"

    # Currency units
    CURRENCY_EURO: typing.Final = "€"
    CURRENCY_DOLLAR: typing.Final = "$"
    CURRENCY_CENT: typing.Final = "¢"

    # Temperature units
    class UnitOfTemperature(strenum.StrEnum):
        """Temperature units."""

        CELSIUS = "°C"
        FAHRENHEIT = "°F"
        KELVIN = "K"

    # Time units
    class UnitOfTime(strenum.StrEnum):
        """Time units."""

        MICROSECONDS = "µs"
        MILLISECONDS = "ms"
        SECONDS = "s"
        MINUTES = "min"
        HOURS = "h"
        DAYS = "d"
        WEEKS = "w"
        MONTHS = "m"
        YEARS = "y"

    # Length units
    class UnitOfLength(strenum.StrEnum):
        """Length units."""

        MILLIMETERS = "mm"
        CENTIMETERS = "cm"
        METERS = "m"
        KILOMETERS = "km"
        INCHES = "in"
        FEET = "ft"
        YARDS = "yd"
        MILES = "mi"

    # Frequency units
    class UnitOfFrequency(strenum.StrEnum):
        """Frequency units."""

        HERTZ = "Hz"
        KILOHERTZ = "kHz"
        MEGAHERTZ = "MHz"
        GIGAHERTZ = "GHz"

    # Pressure units
    class UnitOfPressure(strenum.StrEnum):
        """Pressure units."""

        PA = "Pa"
        HPA = "hPa"
        KPA = "kPa"
        BAR = "bar"
        CBAR = "cbar"
        MBAR = "mbar"
        MMHG = "mmHg"
        INHG = "inHg"
        PSI = "psi"

    # Sound pressure units
    class UnitOfSoundPressure(strenum.StrEnum):
        DECIBEL = "dB"
        WEIGHTED_DECIBEL_A = "dBA"

    # Volume units
    class UnitOfVolume(strenum.StrEnum):
        """Volume units."""

        CUBIC_FEET = "ft³"
        CENTUM_CUBIC_FEET = "CCF"
        CUBIC_METERS = "m³"
        LITERS = "L"
        MILLILITERS = "mL"
        GALLONS = "gal"
        """Assumed to be US gallons in conversion utilities.

        British/Imperial gallons are not yet supported"""
        FLUID_OUNCES = "fl. oz."
        """Assumed to be US fluid ounces in conversion utilities.

        British/Imperial fluid ounces are not yet supported"""

    # Volume Flow Rate units
    VOLUME_FLOW_RATE_CUBIC_METERS_PER_HOUR: typing.Final = "m³/h"
    VOLUME_FLOW_RATE_CUBIC_FEET_PER_MINUTE: typing.Final = "ft³/m"

    # Area units
    AREA_SQUARE_METERS: typing.Final = "m²"

    # Mass units
    class UnitOfMass(strenum.StrEnum):
        """Mass units."""

        GRAMS = "g"
        KILOGRAMS = "kg"
        MILLIGRAMS = "mg"
        MICROGRAMS = "µg"
        OUNCES = "oz"
        POUNDS = "lb"

    # Conductivity units
    CONDUCTIVITY: typing.Final = "µS/cm"

    # Light units
    LIGHT_LUX: typing.Final = "lx"

    # UV Index units
    UV_INDEX: typing.Final = "UV index"

    # Percentage units
    PERCENTAGE: typing.Final = "%"

    # Rotational speed units
    REVOLUTIONS_PER_MINUTE: typing.Final = "rpm"

    class UnitOfIrradiance(strenum.StrEnum):
        """Irradiance units."""

        WATTS_PER_SQUARE_METER = "W/m²"
        BTUS_PER_HOUR_SQUARE_FOOT = "BTU/(h⋅ft²)"

    class UnitOfVolumetricFlux(strenum.StrEnum):
        """Volumetric flux, commonly used for precipitation intensity.

        The derivation of these units is a volume of rain amassing in a container
        with constant cross section in a given time
        """

        INCHES_PER_DAY = "in/d"
        """Derived from in³/(in².d)"""

        INCHES_PER_HOUR = "in/h"
        """Derived from in³/(in².h)"""

        MILLIMETERS_PER_DAY = "mm/d"
        """Derived from mm³/(mm².d)"""

        MILLIMETERS_PER_HOUR = "mm/h"
        """Derived from mm³/(mm².h)"""

    class UnitOfPrecipitationDepth(strenum.StrEnum):
        """Precipitation depth.

        The derivation of these units is a volume of rain amassing in a container
        with constant cross section
        """

        INCHES = "in"
        """Derived from in³/in²"""

        MILLIMETERS = "mm"
        """Derived from mm³/mm²"""

        CENTIMETERS = "cm"
        """Derived from cm³/cm²"""

    # Concentration units
    CONCENTRATION_MICROGRAMS_PER_CUBIC_METER: typing.Final = "µg/m³"
    CONCENTRATION_MILLIGRAMS_PER_CUBIC_METER: typing.Final = "mg/m³"
    CONCENTRATION_MICROGRAMS_PER_CUBIC_FOOT: typing.Final = "μg/ft³"
    CONCENTRATION_PARTS_PER_CUBIC_METER: typing.Final = "p/m³"
    CONCENTRATION_PARTS_PER_MILLION: typing.Final = "ppm"
    CONCENTRATION_PARTS_PER_BILLION: typing.Final = "ppb"

    # Speed units
    class UnitOfSpeed(strenum.StrEnum):
        """Speed units."""

        FEET_PER_SECOND = "ft/s"
        METERS_PER_SECOND = "m/s"
        KILOMETERS_PER_HOUR = "km/h"
        KNOTS = "kn"
        MILES_PER_HOUR = "mph"

    # Signal_strength units
    SIGNAL_STRENGTH_DECIBELS: typing.Final = "dB"
    SIGNAL_STRENGTH_DECIBELS_MILLIWATT: typing.Final = "dBm"

    # Data units
    class UnitOfInformation(strenum.StrEnum):
        """Information units."""

        BITS = "bit"
        KILOBITS = "kbit"
        MEGABITS = "Mbit"
        GIGABITS = "Gbit"
        BYTES = "B"
        KILOBYTES = "kB"
        MEGABYTES = "MB"
        GIGABYTES = "GB"
        TERABYTES = "TB"
        PETABYTES = "PB"
        EXABYTES = "EB"
        ZETTABYTES = "ZB"
        YOTTABYTES = "YB"
        KIBIBYTES = "KiB"
        GIBIBYTES = "GiB"
        MEBIBYTES = "MiB"
        TEBIBYTES = "TiB"
        PEBIBYTES = "PiB"
        EXBIBYTES = "EiB"
        ZEBIBYTES = "ZiB"
        YOBIBYTES = "YiB"

    # Data_rate units
    class UnitOfDataRate(strenum.StrEnum):
        """Data rate units."""

        BITS_PER_SECOND = "bit/s"
        KILOBITS_PER_SECOND = "kbit/s"
        MEGABITS_PER_SECOND = "Mbit/s"
        GIGABITS_PER_SECOND = "Gbit/s"
        BYTES_PER_SECOND = "B/s"
        KILOBYTES_PER_SECOND = "kB/s"
        MEGABYTES_PER_SECOND = "MB/s"
        GIGABYTES_PER_SECOND = "GB/s"
        KIBIBYTES_PER_SECOND = "KiB/s"
        MEBIBYTES_PER_SECOND = "MiB/s"
        GIBIBYTES_PER_SECOND = "GiB/s"

    # #### SERVICES ####
    SERVICE_SHC_STOP: typing.Final = "stop"
    SERVICE_SHC_RESTART: typing.Final = "restart"

    SERVICE_TURN_ON: typing.Final = "turn_on"
    SERVICE_TURN_OFF: typing.Final = "turn_off"
    SERVICE_TOGGLE: typing.Final = "toggle"
    SERVICE_RELOAD: typing.Final = "reload"

    SERVICE_VOLUME_UP: typing.Final = "volume_up"
    SERVICE_VOLUME_DOWN: typing.Final = "volume_down"
    SERVICE_VOLUME_MUTE: typing.Final = "volume_mute"
    SERVICE_VOLUME_SET: typing.Final = "volume_set"
    SERVICE_MEDIA_PLAY_PAUSE: typing.Final = "media_play_pause"
    SERVICE_MEDIA_PLAY: typing.Final = "media_play"
    SERVICE_MEDIA_PAUSE: typing.Final = "media_pause"
    SERVICE_MEDIA_STOP: typing.Final = "media_stop"
    SERVICE_MEDIA_NEXT_TRACK: typing.Final = "media_next_track"
    SERVICE_MEDIA_PREVIOUS_TRACK: typing.Final = "media_previous_track"
    SERVICE_MEDIA_SEEK: typing.Final = "media_seek"
    SERVICE_REPEAT_SET: typing.Final = "repeat_set"
    SERVICE_SHUFFLE_SET: typing.Final = "shuffle_set"

    SERVICE_ALARM_DISARM: typing.Final = "alarm_disarm"
    SERVICE_ALARM_ARM_HOME: typing.Final = "alarm_arm_home"
    SERVICE_ALARM_ARM_AWAY: typing.Final = "alarm_arm_away"
    SERVICE_ALARM_ARM_NIGHT: typing.Final = "alarm_arm_night"
    SERVICE_ALARM_ARM_VACATION: typing.Final = "alarm_arm_vacation"
    SERVICE_ALARM_ARM_CUSTOM_BYPASS: typing.Final = "alarm_arm_custom_bypass"
    SERVICE_ALARM_TRIGGER: typing.Final = "alarm_trigger"

    SERVICE_LOCK: typing.Final = "lock"
    SERVICE_UNLOCK: typing.Final = "unlock"

    SERVICE_OPEN: typing.Final = "open"
    SERVICE_CLOSE: typing.Final = "close"

    SERVICE_CLOSE_COVER: typing.Final = "close_cover"
    SERVICE_CLOSE_COVER_TILT: typing.Final = "close_cover_tilt"
    SERVICE_OPEN_COVER: typing.Final = "open_cover"
    SERVICE_OPEN_COVER_TILT: typing.Final = "open_cover_tilt"
    SERVICE_SAVE_PERSISTENT_STATES: typing.Final = "save_persistent_states"
    SERVICE_SET_COVER_POSITION: typing.Final = "set_cover_position"
    SERVICE_SET_COVER_TILT_POSITION: typing.Final = "set_cover_tilt_position"
    SERVICE_STOP_COVER: typing.Final = "stop_cover"
    SERVICE_STOP_COVER_TILT: typing.Final = "stop_cover_tilt"
    SERVICE_TOGGLE_COVER_TILT: typing.Final = "toggle_cover_tilt"

    SERVICE_SELECT_OPTION: typing.Final = "select_option"
    SERVICE_PRESS: typing.Final = "press"
    SERVICE_NOTIFY: typing.Final = "notify"
    # NOTIFY Component
    CONF_FIELDS: typing.Final = "fields"
    # Platform specific data
    ATTR_TITLE_DEFAULT: typing.Final = "Smart Home - The Next Generation"

    # #### API / REMOTE ####
    SERVER_PORT: typing.Final = 8123

    URL_ROOT: typing.Final = "/"
    URL_API: typing.Final = "/api/"
    URL_API_STREAM: typing.Final = "/api/stream"
    URL_API_CONFIG: typing.Final = "/api/config"
    URL_API_STATES: typing.Final = "/api/states"
    URL_API_STATES_ENTITY: typing.Final = "/api/states/{}"
    URL_API_EVENTS: typing.Final = "/api/events"
    URL_API_EVENTS_EVENT: typing.Final = "/api/events/{}"
    URL_API_SERVICES: typing.Final = "/api/services"
    URL_API_SERVICES_SERVICE: typing.Final = "/api/services/{}/{}"
    URL_API_COMPONENTS: typing.Final = "/api/components"
    URL_API_ERROR_LOG: typing.Final = "/api/error_log"
    URL_API_LOG_OUT: typing.Final = "/api/log_out"
    URL_API_TEMPLATE: typing.Final = "/api/template"

    HTTP_BASIC_AUTHENTICATION: typing.Final = "basic"
    HTTP_BEARER_AUTHENTICATION: typing.Final = "bearer_token"
    HTTP_DIGEST_AUTHENTICATION: typing.Final = "digest"

    HTTP_HEADER_X_REQUESTED_WITH: typing.Final = "X-Requested-With"

    CONTENT_TYPE_JSON: typing.Final = "application/json"
    CONTENT_TYPE_MULTIPART: typing.Final = "multipart/x-mixed-replace; boundary={}"
    CONTENT_TYPE_TEXT_PLAIN: typing.Final = "text/plain"

    # The exit code to send to request a restart
    RESTART_EXIT_CODE: typing.Final = 100

    UNIT_NOT_RECOGNIZED_TEMPLATE: typing.Final = "{} is not a recognized {} unit."

    LENGTH: typing.Final = "length"
    MASS: typing.Final = "mass"
    PRESSURE: typing.Final = "pressure"
    VOLUME: typing.Final = "volume"
    TEMPERATURE: typing.Final = "temperature"
    SPEED: typing.Final = "speed"
    WIND_SPEED: typing.Final = "wind_speed"
    ILLUMINANCE: typing.Final = "illuminance"
    ACCUMULATED_PRECIPITATION: typing.Final = "accumulated_precipitation"

    WEEKDAYS: typing.Final[list[str]] = [
        "mon",
        "tue",
        "wed",
        "thu",
        "fri",
        "sat",
        "sun",
    ]

    # The degree of precision for platforms
    PRECISION_WHOLE: typing.Final = 1
    PRECISION_HALVES: typing.Final = 0.5
    PRECISION_TENTHS: typing.Final = 0.1

    # Static list of entities that will never be exposed to
    # cloud, alexa, or google_home components
    CLOUD_NEVER_EXPOSED_ENTITIES: typing.Final[list[str]] = ["group.all_locks"]

    # ENTITY_CATEGOR* below are deprecated as of 2021.12
    # use the EntityCategory enum instead.
    ENTITY_CATEGORY_CONFIG: typing.Final = "config"
    ENTITY_CATEGORY_DIAGNOSTIC: typing.Final = "diagnostic"
    ENTITY_CATEGORIES: typing.Final[list[str]] = [
        ENTITY_CATEGORY_CONFIG,
        ENTITY_CATEGORY_DIAGNOSTIC,
    ]

    # The ID of the Home Assistant Media Player Cast App
    CAST_APP_ID_HOMEASSISTANT_MEDIA: typing.Final = "B45F4572"
    # The ID of the Home Assistant Lovelace Cast App
    CAST_APP_ID_HOMEASSISTANT_LOVELACE: typing.Final = "A078F6B0"

    # User used by Supervisor
    SIGNAL_BOOTSTRAP_INTEGRATONS: typing.Final = "bootstrap_integrations"
    LOGSEVERITY: typing.Final = {
        "CRITICAL": 50,
        "FATAL": 50,
        "ERROR": 40,
        "WARNING": 30,
        "WARN": 30,
        "INFO": 20,
        "DEBUG": 10,
        "NOTSET": 0,
    }

    MEDIA_SOURCE_URI_SCHEME: typing.Final = "media-source://"
    MEDIA_SOURCE_URI_SCHEME_REGEX: typing.Final = re.compile(
        r"^media-source:\/\/(?:(?P<domain>(?!_)[\da-z_]+(?<!_))(?:\/(?P<identifier>(?!\/).+))?)?$"
    )

    LOGBOOK_ENTRY_ICON: typing.Final = "icon"
    LOGBOOK_ENTRY_MESSAGE: typing.Final = "message"
    LOGBOOK_ENTRY_NAME: typing.Final = "name"
    LOGBOOK_ENTRY_ENTITY_ID: typing.Final = "entity_id"
    LOGBOOK_ENTRY_SOURCE: typing.Final = "source"
    LOGBOOK_ENTRY_CONTEXT_ID: typing.Final = "context_id"

    DEFAULT_STORED_TRACES: typing.Final = 5  # Stored traces per script or automation

    EVENT_AUTOMATION_RELOADED: typing.Final = "automation.reloaded"
    EVENT_AUTOMATION_TRIGGERED: typing.Final = "automation.triggered"
    EVENT_SCRIPT_STARTED: typing.Final = "script.started"

    # -------- Weather Platform Constants --------
    ATTR_CONDITION_CLASS: typing.Final = "condition_class"
    ATTR_CONDITION_CLEAR_NIGHT: typing.Final = "clear-night"
    ATTR_CONDITION_CLOUDY: typing.Final = "cloudy"
    ATTR_CONDITION_EXCEPTIONAL: typing.Final = "exceptional"
    ATTR_CONDITION_FOG: typing.Final = "fog"
    ATTR_CONDITION_HAIL: typing.Final = "hail"
    ATTR_CONDITION_LIGHTNING: typing.Final = "lightning"
    ATTR_CONDITION_LIGHTNING_RAINY: typing.Final = "lightning-rainy"
    ATTR_CONDITION_PARTLYCLOUDY: typing.Final = "partlycloudy"
    ATTR_CONDITION_POURING: typing.Final = "pouring"
    ATTR_CONDITION_RAINY: typing.Final = "rainy"
    ATTR_CONDITION_SNOWY: typing.Final = "snowy"
    ATTR_CONDITION_SNOWY_RAINY: typing.Final = "snowy-rainy"
    ATTR_CONDITION_SUNNY: typing.Final = "sunny"
    ATTR_CONDITION_WINDY: typing.Final = "windy"
    ATTR_CONDITION_WINDY_VARIANT: typing.Final = "windy-variant"
    ATTR_FORECAST: typing.Final = "forecast"
    ATTR_FORECAST_CONDITION: typing.Final = "condition"
    ATTR_FORECAST_NATIVE_PRECIPITATION: typing.Final = "native_precipitation"
    ATTR_FORECAST_PRECIPITATION: typing.Final = "precipitation"
    ATTR_FORECAST_PRECIPITATION_PROBABILITY: typing.Final = "precipitation_probability"
    ATTR_FORECAST_NATIVE_PRESSURE: typing.Final = "native_pressure"
    ATTR_FORECAST_PRESSURE: typing.Final = "pressure"
    ATTR_FORECAST_NATIVE_TEMP: typing.Final = "native_temperature"
    ATTR_FORECAST_TEMP: typing.Final = "temperature"
    ATTR_FORECAST_NATIVE_TEMP_LOW: typing.Final = "native_templow"
    ATTR_FORECAST_TEMP_LOW: typing.Final = "templow"
    ATTR_FORECAST_TIME: typing.Final = "datetime"
    ATTR_FORECAST_WIND_BEARING: typing.Final = "wind_bearing"
    ATTR_FORECAST_NATIVE_WIND_SPEED: typing.Final = "native_wind_speed"
    ATTR_FORECAST_WIND_SPEED: typing.Final = "wind_speed"
    ATTR_WEATHER_HUMIDITY: typing.Final = "humidity"
    ATTR_WEATHER_OZONE: typing.Final = "ozone"
    ATTR_WEATHER_PRESSURE: typing.Final = "pressure"
    ATTR_WEATHER_PRESSURE_UNIT: typing.Final = "pressure_unit"
    ATTR_WEATHER_TEMPERATURE: typing.Final = "temperature"
    ATTR_WEATHER_TEMPERATURE_UNIT: typing.Final = "temperature_unit"
    ATTR_WEATHER_VISIBILITY: typing.Final = "visibility"
    ATTR_WEATHER_VISIBILITY_UNIT: typing.Final = "visibility_unit"
    ATTR_WEATHER_WIND_BEARING: typing.Final = "wind_bearing"
    ATTR_WEATHER_WIND_SPEED: typing.Final = "wind_speed"
    ATTR_WEATHER_WIND_SPEED_UNIT: typing.Final = "wind_speed_unit"
    ATTR_WEATHER_PRECIPITATION_UNIT: typing.Final = "precipitation_unit"

    JSON_DUMP: typing.Final = functools.partial(
        json.dumps, cls=JsonEncoder, allow_nan=False, separators=(",", ":")
    )

    MDNS_TARGET_IP: typing.Final = "224.0.0.251"

    # Constants for device automations.
    CONF_CHANGED_STATES: typing.Final = "changed_states"

    # State Trigger
    CONF_FROM: typing.Final = "from"
    CONF_TO: typing.Final = "to"
    CONF_NOT_FROM: typing.Final = "not_from"
    CONF_NOT_TO: typing.Final = "not_to"

    # ------- Predefined Component Domains -------

    PERSISTENT_NOTIFICATION_COMPONENT_NAME: typing.Final = "persistent_notification"
    PERSON_COMPONENT_NAME: typing.Final = "person"
    PROXIMITY_COMPONENT_NAME: typing.Final = "proximity"
    RECORDER_COMPONENT_NAME: typing.Final = "recorder"
    SCENE_COMPONENT_NAME: typing.Final = "scene"
    SCRIPT_COMPONENT_NAME: typing.Final = "script"
    SENSOR_COMPONENT_NAME: typing.Final = "sensor"
    SSDP_COMPONENT_NAME: typing.Final = "ssdp"
    STREAM_COMPONENT_NAME: typing.Final = "stream"
    SYSTEM_HEALTH_COMPONENT_NAME: typing.Final = "system_health"
    TRACE_COMPONENT_NAME: typing.Final = "trace"
    USB_COMPONENT_NAME: typing.Final = "usb"
    WEATHER_COMPONENT_NAME: typing.Final = "weather"
    WEBHOOK_COMPONENT_NAME: typing.Final = "webhook"
    ZEROCONF_COMPONENT_NAME: typing.Final = "zeroconf"
    ZONE_COMPONENT_NAME: typing.Final = "zone"
    CORE_COMPONENT_NAME: typing.Final = "homeassistant"
