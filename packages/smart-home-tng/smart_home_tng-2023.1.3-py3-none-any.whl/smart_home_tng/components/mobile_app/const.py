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

import typing
import voluptuous as vol

from ... import core

_cv: typing.TypeAlias = core.ConfigValidation


# pylint: disable=unused-variable
class Const:
    """Contansts for the Mobile App Component."""

    CONF_CLOUDHOOK_URL: typing.Final = "cloudhook_url"
    CONF_REMOTE_UI_URL: typing.Final = "remote_ui_url"
    CONF_SECRET: typing.Final = "secret"
    CONF_USER_ID: typing.Final = "user_id"

    ATTR_APP_DATA: typing.Final = "app_data"
    ATTR_APP_ID: typing.Final = "app_id"
    ATTR_APP_NAME: typing.Final = "app_name"
    ATTR_APP_VERSION: typing.Final = "app_version"
    ATTR_CONFIG_ENTRY_ID: typing.Final = "entry_id"
    ATTR_DEVICE_NAME: typing.Final = "device_name"
    ATTR_MANUFACTURER: typing.Final = "manufacturer"
    ATTR_MODEL: typing.Final = "model"
    ATTR_NO_LEGACY_ENCRYPTION: typing.Final = "no_legacy_encryption"
    ATTR_OS_NAME: typing.Final = "os_name"
    ATTR_OS_VERSION: typing.Final = "os_version"
    ATTR_PUSH_WEBSOCKET_CHANNEL: typing.Final = "push_websocket_channel"
    ATTR_PUSH_TOKEN: typing.Final = "push_token"
    ATTR_PUSH_URL: typing.Final = "push_url"
    ATTR_PUSH_RATE_LIMITS: typing.Final = "rateLimits"
    ATTR_PUSH_RATE_LIMITS_ERRORS: typing.Final = "errors"
    ATTR_PUSH_RATE_LIMITS_MAXIMUM: typing.Final = "maximum"
    ATTR_PUSH_RATE_LIMITS_RESETS_AT: typing.Final = "resetsAt"
    ATTR_PUSH_RATE_LIMITS_SUCCESSFUL: typing.Final = "successful"
    ATTR_SUPPORTS_ENCRYPTION: typing.Final = "supports_encryption"

    ATTR_EVENT_DATA: typing.Final = "event_data"
    ATTR_EVENT_TYPE: typing.Final = "event_type"

    ATTR_TEMPLATE: typing.Final = "template"
    ATTR_TEMPLATE_VARIABLES: typing.Final = "variables"

    ATTR_SPEED: typing.Final = "speed"
    ATTR_ALTITUDE: typing.Final = "altitude"
    ATTR_COURSE: typing.Final = "course"
    ATTR_VERTICAL_ACCURACY: typing.Final = "vertical_accuracy"

    ATTR_WEBHOOK_DATA: typing.Final = "data"
    ATTR_WEBHOOK_ENCRYPTED: typing.Final = "encrypted"
    ATTR_WEBHOOK_ENCRYPTED_DATA: typing.Final = "encrypted_data"
    ATTR_WEBHOOK_ID: typing.Final = "webhook_id"
    ATTR_WEBHOOK_TYPE: typing.Final = "type"

    ERR_ENCRYPTION_ALREADY_ENABLED: typing.Final = "encryption_already_enabled"
    ERR_ENCRYPTION_NOT_AVAILABLE: typing.Final = "encryption_not_available"
    ERR_ENCRYPTION_REQUIRED: typing.Final = "encryption_required"
    ERR_SENSOR_NOT_REGISTERED: typing.Final = "not_registered"
    ERR_INVALID_FORMAT: typing.Final = "invalid_format"

    ATTR_SENSOR_ATTRIBUTES: typing.Final = "attributes"
    ATTR_SENSOR_DEVICE_CLASS: typing.Final = "device_class"
    ATTR_SENSOR_DISABLED: typing.Final = "disabled"
    ATTR_SENSOR_ENTITY_CATEGORY: typing.Final = "entity_category"
    ATTR_SENSOR_ICON: typing.Final = "icon"
    ATTR_SENSOR_NAME: typing.Final = "name"
    ATTR_SENSOR_STATE: typing.Final = "state"
    ATTR_SENSOR_STATE_CLASS: typing.Final = "state_class"
    ATTR_SENSOR_TYPE: typing.Final = "type"
    ATTR_SENSOR_TYPE_BINARY_SENSOR: typing.Final = "binary_sensor"
    ATTR_SENSOR_TYPE_SENSOR: typing.Final = "sensor"
    ATTR_SENSOR_UNIQUE_ID: typing.Final = "unique_id"
    ATTR_SENSOR_UOM: typing.Final = "unit_of_measurement"
    ATTR_CAMERA_ENTITY_ID: typing.Final = "camera_entity_id"

    SCHEMA_APP_DATA: typing.Final = vol.Schema(
        {
            vol.Inclusive(ATTR_PUSH_TOKEN, "push_cloud"): _cv.string,
            vol.Inclusive(ATTR_PUSH_URL, "push_cloud"): _cv.url,
            # Set to True to indicate that this registration will connect via websocket channel
            # to receive push notifications.
            vol.Optional(ATTR_PUSH_WEBSOCKET_CHANNEL): _cv.boolean,
        },
        extra=vol.ALLOW_EXTRA,
    )

    DATA_CONFIG_ENTRIES: typing.Final = "config_entries"
    DATA_DELETED_IDS: typing.Final = "deleted_ids"
    DATA_DEVICES: typing.Final = "devices"
    DATA_NOTIFY: typing.Final = "notify"
    DATA_PUSH_CHANNEL: typing.Final = "push_channel"
