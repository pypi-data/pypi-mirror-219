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

import contextlib
import functools as ft
import http
import logging
import secrets
import typing

import nacl.secret
import voluptuous as vol
from aiohttp import web

from ... import core
from .const import Const
from .helpers import (
    _empty_okay_response,
    _error_response,
    _registration_context,
    _safe_registration,
    _supports_encryption,
    _webhook_response,
)

# pylint: disable=unused-variable

_cv: typing.TypeAlias = core.ConfigValidation
_camera: typing.TypeAlias = core.Camera
_const: typing.TypeAlias = core.Const
_LOGGER: typing.Final = logging.getLogger(__name__)
_WebhookCommand: typing.TypeAlias = typing.Callable[
    [core.SmartHomeControllerComponent, core.ConfigEntry, dict],
    typing.Awaitable[web.Response],
]
_WEBHOOK_COMMANDS: typing.Final = core.Registry[str, _WebhookCommand]()
_COMBINED_CLASSES: typing.Final = set(
    [cls.value for cls in core.BinarySensor.DeviceClass]
    + [cls.value for cls in core.Sensor.DeviceClass]
)
_SENSOR_TYPES: typing.Final = [
    Const.ATTR_SENSOR_TYPE_BINARY_SENSOR,
    Const.ATTR_SENSOR_TYPE_SENSOR,
]


def validate_schema(schema):
    """Decorate a webhook function with a schema."""
    if isinstance(schema, dict):
        schema = vol.Schema(schema)

    def wrapper(func):
        """Wrap function so we validate schema."""

        @ft.wraps(func)
        async def validate_and_run(shc, config_entry, data):
            """Validate input and call handler."""
            try:
                data = schema(data)
            except vol.Invalid as ex:
                err = vol.humanize.humanize_error(data, ex)
                _LOGGER.error(f"Received invalid webhook payload: {err}")
                return _empty_okay_response()

            return await func(shc, config_entry, data)

        return validate_and_run

    return wrapper


@_WEBHOOK_COMMANDS.register("call_service")
@validate_schema(
    {
        vol.Required(_const.ATTR_DOMAIN): _cv.string,
        vol.Required(_const.ATTR_SERVICE): _cv.string,
        vol.Optional(_const.ATTR_SERVICE_DATA, default={}): dict,
    }
)
async def webhook_call_service(
    mobile_app: core.SmartHomeControllerComponent,
    config_entry: core.ConfigEntry,
    data: dict,
):
    """Handle a call service webhook."""
    try:
        await mobile_app.controller.services.async_call(
            data[_const.ATTR_DOMAIN],
            data[_const.ATTR_SERVICE],
            data[_const.ATTR_SERVICE_DATA],
            blocking=True,
            context=_registration_context(config_entry.data),
        )
    except (vol.Invalid, core.ServiceNotFound, Exception) as ex:
        _LOGGER.error(
            "Error when calling service during mobile_app "
            + f"webhook (device name: {config_entry.data[Const.ATTR_DEVICE_NAME]}): "
            + f"{ex}",
        )
        raise web.HTTPBadRequest() from ex

    return _empty_okay_response()


@_WEBHOOK_COMMANDS.register("fire_event")
@validate_schema(
    {
        vol.Required(Const.ATTR_EVENT_TYPE): _cv.string,
        vol.Optional(Const.ATTR_EVENT_DATA, default={}): dict,
    }
)
async def webhook_fire_event(
    mobile_app: core.SmartHomeControllerComponent,
    config_entry: core.ConfigEntry,
    data: dict,
):
    """Handle a fire event webhook."""
    event_type = data[Const.ATTR_EVENT_TYPE]
    mobile_app.controller.bus.async_fire(
        event_type,
        data[Const.ATTR_EVENT_DATA],
        core.EventOrigin.REMOTE,
        context=_registration_context(config_entry.data),
    )
    return _empty_okay_response()


@_WEBHOOK_COMMANDS.register("stream_camera")
@validate_schema({vol.Required(Const.ATTR_CAMERA_ENTITY_ID): _cv.string})
async def webhook_stream_camera(
    mobile_app: core.SmartHomeControllerComponent,
    config_entry: core.ConfigEntry,
    data: dict,
):
    """Handle a request to HLS-stream a camera."""
    if (
        camera_state := mobile_app.controller.states.get(
            data[Const.ATTR_CAMERA_ENTITY_ID]
        )
    ) is None:
        return _webhook_response(
            {"success": False},
            registration=config_entry.data,
            status=http.HTTPStatus.BAD_REQUEST,
        )

    resp = {"mjpeg_path": f"/api/camera_proxy_stream/{camera_state.entity_id}"}

    if (
        camera_state.attributes[_const.ATTR_SUPPORTED_FEATURES]
        & _camera.EntityFeature.STREAM
    ):
        try:
            camera: core.Camera.Component = mobile_app.controller.components.camera
            resp["hls_path"] = await camera.async_request_stream(
                camera_state.entity_id, "hls"
            )
        except core.SmartHomeControllerError:
            resp["hls_path"] = None
    else:
        resp["hls_path"] = None

    return _webhook_response(resp, registration=config_entry.data)


@_WEBHOOK_COMMANDS.register("render_template")
@validate_schema(
    {
        str: {
            vol.Required(Const.ATTR_TEMPLATE): _cv.string,
            vol.Optional(Const.ATTR_TEMPLATE_VARIABLES, default={}): dict,
        }
    }
)
async def webhook_render_template(
    mobile_app: core.SmartHomeControllerComponent,
    config_entry: core.ConfigEntry,
    data: dict,
):
    """Handle a render template webhook."""
    resp = {}
    for key, item in data.items():
        try:
            tpl = core.Template(item[Const.ATTR_TEMPLATE], mobile_app.controller)
            resp[key] = tpl.async_render(item.get(Const.ATTR_TEMPLATE_VARIABLES))
        except core.TemplateError as ex:
            resp[key] = {"error": str(ex)}

    return _webhook_response(resp, registration=config_entry.data)


@_WEBHOOK_COMMANDS.register("update_location")
@validate_schema(
    vol.Schema(
        _cv.key_dependency(_const.ATTR_GPS, _const.ATTR_GPS_ACCURACY),
        {
            vol.Optional(_const.ATTR_LOCATION_NAME): _cv.string,
            vol.Optional(_const.ATTR_GPS): _cv.gps,
            vol.Optional(_const.ATTR_GPS_ACCURACY): _cv.positive_int,
            vol.Optional(_const.ATTR_BATTERY): _cv.positive_int,
            vol.Optional(Const.ATTR_SPEED): _cv.positive_int,
            vol.Optional(Const.ATTR_ALTITUDE): vol.Coerce(float),
            vol.Optional(Const.ATTR_COURSE): _cv.positive_int,
            vol.Optional(Const.ATTR_VERTICAL_ACCURACY): _cv.positive_int,
        },
    )
)
async def webhook_update_location(
    mobile_app: core.SmartHomeControllerComponent,
    config_entry: core.ConfigEntry,
    data: dict,
):
    """Handle an update location webhook."""
    domain = mobile_app.domain
    SIGNAL_LOCATION_UPDATE: typing.Final = domain + ".location_update.{}"

    mobile_app.controller.dispatcher.async_send(
        SIGNAL_LOCATION_UPDATE.format(config_entry.entry_id), data
    )
    return _empty_okay_response()


@_WEBHOOK_COMMANDS.register("update_registration")
@validate_schema(
    {
        vol.Optional(Const.ATTR_APP_DATA): Const.SCHEMA_APP_DATA,
        vol.Required(Const.ATTR_APP_VERSION): _cv.string,
        vol.Required(Const.ATTR_DEVICE_NAME): _cv.string,
        vol.Required(Const.ATTR_MANUFACTURER): _cv.string,
        vol.Required(Const.ATTR_MODEL): _cv.string,
        vol.Optional(Const.ATTR_OS_VERSION): _cv.string,
    }
)
async def webhook_update_registration(
    mobile_app: core.SmartHomeControllerComponent,
    config_entry: core.ConfigEntry,
    data: dict,
):
    """Handle an update registration webhook."""
    new_registration = {**config_entry.data, **data}

    device_registry = mobile_app.controller.device_registry
    domain = mobile_app.domain

    device_registry.async_get_or_create(
        config_entry_id=config_entry.entry_id,
        identifiers={(domain, config_entry.data[_const.ATTR_DEVICE_ID])},
        manufacturer=new_registration[Const.ATTR_MANUFACTURER],
        model=new_registration[Const.ATTR_MODEL],
        name=new_registration[Const.ATTR_DEVICE_NAME],
        sw_version=new_registration[Const.ATTR_OS_VERSION],
    )

    mobile_app.controller.config_entries.async_update_entry(
        config_entry, data=new_registration
    )

    # await hass_notify.async_reload(hass, DOMAIN)

    return _webhook_response(
        _safe_registration(new_registration),
        registration=new_registration,
    )


@_WEBHOOK_COMMANDS.register("enable_encryption")
async def webhook_enable_encryption(
    mobile_app: core.SmartHomeControllerComponent,
    config_entry: core.ConfigEntry,
    data: dict,
):
    """Handle a encryption enable webhook."""
    if config_entry.data[Const.ATTR_SUPPORTS_ENCRYPTION]:
        _LOGGER.warning(
            f"Refusing to enable encryption for {config_entry.data[Const.ATTR_DEVICE_NAME]} "
            + "because it is already enabled!",
        )
        return _error_response(
            Const.ERR_ENCRYPTION_ALREADY_ENABLED, "Encryption already enabled"
        )

    if not _supports_encryption():
        _LOGGER.warning(
            f"Unable to enable encryption for {config_entry.data[Const.ATTR_DEVICE_NAME]} "
            + "because libsodium is unavailable!",
        )
        return _error_response(
            Const.ERR_ENCRYPTION_NOT_AVAILABLE, "Encryption is unavailable"
        )

    secret = secrets.token_hex(nacl.secret.SecretBox.KEY_SIZE)

    data = {
        **config_entry.data,
        Const.ATTR_SUPPORTS_ENCRYPTION: True,
        Const.CONF_SECRET: secret,
    }

    mobile_app.controller.config_entries.async_update_entry(config_entry, data=data)

    return web.json_response({"secret": secret})


def _validate_state_class_sensor(value: dict):
    """Validate we only set state class for sensors."""
    if (
        Const.ATTR_SENSOR_STATE_CLASS in value
        and value[Const.ATTR_SENSOR_TYPE] != Const.ATTR_SENSOR_TYPE_SENSOR
    ):
        raise vol.Invalid("state_class only allowed for sensors")

    return value


def _gen_unique_id(webhook_id, sensor_unique_id):
    """Return a unique sensor ID."""
    return f"{webhook_id}_{sensor_unique_id}"


def _extract_sensor_unique_id(webhook_id, unique_id):
    """Return a unique sensor ID."""
    return unique_id[len(webhook_id) + 1 :]


@_WEBHOOK_COMMANDS.register("register_sensor")
@validate_schema(
    vol.All(
        {
            vol.Optional(Const.ATTR_SENSOR_ATTRIBUTES, default={}): dict,
            vol.Optional(Const.ATTR_SENSOR_DEVICE_CLASS): vol.All(
                vol.Lower, vol.In(_COMBINED_CLASSES)
            ),
            vol.Required(Const.ATTR_SENSOR_NAME): _cv.string,
            vol.Required(Const.ATTR_SENSOR_TYPE): vol.In(_SENSOR_TYPES),
            vol.Required(Const.ATTR_SENSOR_UNIQUE_ID): _cv.string,
            vol.Optional(Const.ATTR_SENSOR_UOM): _cv.string,
            vol.Optional(Const.ATTR_SENSOR_STATE, default=None): vol.Any(
                None, bool, str, int, float
            ),
            vol.Optional(
                Const.ATTR_SENSOR_ENTITY_CATEGORY
            ): _cv.ENTITY_CATEGORIES_SCHEMA,
            vol.Optional(Const.ATTR_SENSOR_ICON, default="mdi:cellphone"): _cv.icon,
            vol.Optional(Const.ATTR_SENSOR_STATE_CLASS): vol.In(
                core.Sensor.STATE_CLASSES
            ),
            vol.Optional(Const.ATTR_SENSOR_DISABLED): bool,
        },
        _validate_state_class_sensor,
    )
)
async def webhook_register_sensor(
    mobile_app: core.SmartHomeControllerComponent,
    config_entry: core.ConfigEntry,
    data: dict,
):
    """Handle a register sensor webhook."""
    entity_type = data[Const.ATTR_SENSOR_TYPE]
    unique_id = data[Const.ATTR_SENSOR_UNIQUE_ID]
    device_name = config_entry.data[Const.ATTR_DEVICE_NAME]

    unique_store_key = _gen_unique_id(
        config_entry.data[_const.CONF_WEBHOOK_ID], unique_id
    )
    entity_registry = mobile_app.controller.entity_registry
    existing_sensor = entity_registry.async_get_entity_id(
        entity_type, mobile_app.domain, unique_store_key
    )

    data[_const.CONF_WEBHOOK_ID] = config_entry.data[_const.CONF_WEBHOOK_ID]

    # If sensor already is registered, update current state instead
    if existing_sensor:
        _LOGGER.debug(
            f"Re-register for {device_name} of existing sensor {unique_id}",
            device_name,
            unique_id,
        )

        entry = entity_registry.async_get(existing_sensor)
        changes = {}

        if (
            new_name := f"{device_name} {data[Const.ATTR_SENSOR_NAME]}"
        ) != entry.original_name:
            changes["original_name"] = new_name

        if (
            should_be_disabled := data.get(Const.ATTR_SENSOR_DISABLED)
        ) is None or should_be_disabled == entry.disabled:
            pass
        elif should_be_disabled:
            changes["disabled_by"] = core.EntityRegistryEntryDisabler.INTEGRATION
        else:
            changes["disabled_by"] = None

        for ent_reg_key, data_key in (
            ("device_class", Const.ATTR_SENSOR_DEVICE_CLASS),
            ("unit_of_measurement", Const.ATTR_SENSOR_UOM),
            ("entity_category", Const.ATTR_SENSOR_ENTITY_CATEGORY),
            ("original_icon", Const.ATTR_SENSOR_ICON),
        ):
            if data_key in data and getattr(entry, ent_reg_key) != data[data_key]:
                changes[ent_reg_key] = data[data_key]

        if changes:
            entity_registry.async_update_entity(existing_sensor, **changes)

        signal_sensor_update = mobile_app.domain + ".sensor.update"
        mobile_app.controller.dispatcher.async_send(
            signal_sensor_update, unique_store_key, data
        )
    else:
        data[_const.CONF_UNIQUE_ID] = unique_store_key
        data[
            _const.CONF_NAME
        ] = f"{config_entry.data[Const.ATTR_DEVICE_NAME]} {data[Const.ATTR_SENSOR_NAME]}"

        register_signal = f"{mobile_app.domain}.{data[Const.ATTR_SENSOR_TYPE]}.register"
        mobile_app.controller.dispatcher.async_send(register_signal, data)

    return _webhook_response(
        {"success": True},
        registration=config_entry.data,
        status=http.HTTPStatus.CREATED,
    )


@_WEBHOOK_COMMANDS.register("update_sensor_states")
@validate_schema(
    vol.All(
        _cv.ensure_list,
        [
            # Partial schema, enough to identify schema.
            # We don't validate everything because otherwise 1 invalid sensor
            # will invalidate all sensors.
            vol.Schema(
                {
                    vol.Required(Const.ATTR_SENSOR_TYPE): vol.In(_SENSOR_TYPES),
                    vol.Required(Const.ATTR_SENSOR_UNIQUE_ID): _cv.string,
                },
                extra=vol.ALLOW_EXTRA,
            )
        ],
    )
)
async def webhook_update_sensor_states(
    mobile_app: core.SmartHomeControllerComponent,
    config_entry: core.ConfigEntry,
    data: dict,
):
    """Handle an update sensor states webhook."""
    sensor_schema_full = vol.Schema(
        {
            vol.Optional(Const.ATTR_SENSOR_ATTRIBUTES, default={}): dict,
            vol.Optional(Const.ATTR_SENSOR_ICON, default="mdi:cellphone"): _cv.icon,
            vol.Required(Const.ATTR_SENSOR_STATE): vol.Any(None, bool, str, int, float),
            vol.Required(Const.ATTR_SENSOR_TYPE): vol.In(_SENSOR_TYPES),
            vol.Required(Const.ATTR_SENSOR_UNIQUE_ID): _cv.string,
        }
    )

    device_name = config_entry.data[Const.ATTR_DEVICE_NAME]
    resp = {}
    entity_registry = mobile_app.controller.entity_registry

    for sensor in data:
        entity_type = sensor[Const.ATTR_SENSOR_TYPE]

        unique_id = sensor[Const.ATTR_SENSOR_UNIQUE_ID]

        unique_store_key = _gen_unique_id(
            config_entry.data[_const.CONF_WEBHOOK_ID], unique_id
        )

        if not (
            entity_id := entity_registry.async_get_entity_id(
                entity_type, mobile_app.domain, unique_store_key
            )
        ):
            _LOGGER.debug(
                f"Refusing to update {device_name} non-registered sensor: {unique_store_key}",
            )
            err_msg = f"{entity_type} {unique_id} is not registered"
            resp[unique_id] = {
                "success": False,
                "error": {"code": Const.ERR_SENSOR_NOT_REGISTERED, "message": err_msg},
            }
            continue

        try:
            sensor = sensor_schema_full(sensor)
        except vol.Invalid as err:
            err_msg = vol.humanize.humanize_error(sensor, err)
            _LOGGER.error(
                f"Received invalid sensor payload from {device_name} for {unique_id}: "
                + f"{err_msg}",
            )
            resp[unique_id] = {
                "success": False,
                "error": {"code": Const.ERR_INVALID_FORMAT, "message": err_msg},
            }
            continue

        sensor[_const.CONF_WEBHOOK_ID] = config_entry.data[_const.CONF_WEBHOOK_ID]
        signal_sensor_update = f"{mobile_app.domain}.sensor.update"
        mobile_app.controller.dispatcher.async_send(
            signal_sensor_update,
            unique_store_key,
            sensor,
        )

        resp[unique_id] = {"success": True}

        # Check if disabled
        entry = entity_registry.async_get(entity_id)

        if entry.disabled_by:
            resp[unique_id]["is_disabled"] = True

    return _webhook_response(resp, registration=config_entry.data)


@_WEBHOOK_COMMANDS.register("get_zones")
async def webhook_get_zones(
    mobile_app: core.SmartHomeControllerComponent,
    config_entry: core.ConfigEntry,
    _data: dict,
):
    """Handle a get zones webhook."""
    zones_domain = mobile_app.controller.components.zone.domain
    zones = [
        mobile_app.controller.states.get(entity_id)
        for entity_id in sorted(
            mobile_app.controller.states.async_entity_ids(zones_domain)
        )
    ]
    return _webhook_response(zones, registration=config_entry.data)


@_WEBHOOK_COMMANDS.register("get_config")
async def webhook_get_config(
    mobile_app: core.SmartHomeControllerComponent,
    config_entry: core.ConfigEntry,
    _data: dict,
):
    """Handle a get config webhook."""
    config = mobile_app.controller.config.as_dict()
    frontend: core.FrontendComponent = mobile_app.controller.components.frontend

    resp = {
        "latitude": config["latitude"],
        "longitude": config["longitude"],
        "elevation": config["elevation"],
        "unit_system": config["unit_system"],
        "location_name": config["location_name"],
        "time_zone": config["time_zone"],
        "components": config["components"],
        "version": config["version"],
        "theme_color": frontend.get_manifest("theme_color"),
    }

    if Const.CONF_CLOUDHOOK_URL in config_entry.data:
        resp[Const.CONF_CLOUDHOOK_URL] = config_entry.data[Const.CONF_CLOUDHOOK_URL]

    with contextlib.suppress(core.CloudNotAvailable):
        cloud: core.CloudComponent = mobile_app.controller.components.cloud
        if cloud is not None:
            resp[Const.CONF_REMOTE_UI_URL] = cloud.remote_ui_url

    webhook_id = config_entry.data[_const.CONF_WEBHOOK_ID]

    entities = {}
    for entry in mobile_app.controller.entity_registry.async_entries_for_config_entry(
        config_entry.entry_id
    ):
        if entry.domain in ("binary_sensor", "sensor"):
            unique_id = _extract_sensor_unique_id(webhook_id, entry.unique_id)
        else:
            unique_id = entry.unique_id

        entities[unique_id] = {"disabled": entry.disabled}

    resp["entities"] = entities

    return _webhook_response(resp, registration=config_entry.data)


@_WEBHOOK_COMMANDS.register("scan_tag")
@validate_schema({vol.Required("tag_id"): _cv.string})
async def webhook_scan_tag(
    mobile_app: core.SmartHomeControllerComponent,
    config_entry: core.ConfigEntry,
    data: dict,
):
    """Handle a fire event webhook."""
    tag: core.TagComponent = mobile_app.controller.components.tag
    await tag.async_scan_tag(
        data["tag_id"],
        config_entry.data[Const.ATTR_DEVICE_ID],
        _registration_context(config_entry.data),
    )
    return _empty_okay_response()
