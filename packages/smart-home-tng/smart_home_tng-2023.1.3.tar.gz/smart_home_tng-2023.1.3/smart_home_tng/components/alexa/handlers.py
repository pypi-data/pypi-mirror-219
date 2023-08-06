"""
Amazon Alexa Integration for Smart Home - The Next Generation.

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

import logging
import math
import typing

from ... import core
from .alexa_directive import AlexaDirective
from .alexa_response import AlexaResponse

_alexa: typing.TypeAlias = core.Alexa.Component
_alexa_const: typing.TypeAlias = core.Alexa
_button: typing.TypeAlias = core.Button
_climate: typing.TypeAlias = core.Climate
_color: typing.TypeAlias = core.helpers.Color
_config: typing.TypeAlias = core.Alexa.AbstractConfig
_const: typing.TypeAlias = core.Const
_cover: typing.TypeAlias = core.Cover
_fan: typing.TypeAlias = core.Fan
_input_number: typing.TypeAlias = core.InputNumber
_light: typing.TypeAlias = core.Light
_media_player: typing.TypeAlias = core.MediaPlayer
_platform: typing.TypeAlias = core.Platform
_timer: typing.TypeAlias = core.Timer
_vacuum: typing.TypeAlias = core.Vacuum

_LOGGER: typing.Final = logging.getLogger(__name__)
_DIRECTIVE_NOT_SUPPORTED: typing.Final = "Entity does not support directive"
_HANDLERS: typing.Final[
    core.Registry[
        tuple[str, str],
        typing.Callable[
            [_alexa, _config, AlexaDirective, core.Context],
            typing.Coroutine[typing.Any, typing.Any, AlexaResponse],
        ],
    ]
] = core.Registry()


def _get_entity_platform(entity: core.State) -> str:
    result = entity.domain
    if result == _platform.GROUP:
        result = _platform.SMART_HOME_CONTROLLER.value
    return result


# pylint: disable=unused-variable
@_HANDLERS.register(("Alexa.Discovery", "Discover"))
async def _async_api_discovery(
    alexa: _alexa,
    config: _config,
    directive: AlexaDirective,
    _context: core.Context,
) -> AlexaResponse:
    """Create a API formatted discovery response.

    Async friendly.
    """
    discovery_endpoints = [
        alexa_entity.serialize_discovery()
        for alexa_entity in alexa.async_get_entities(config)
        if config.should_expose(alexa_entity.entity_id)
    ]

    return directive.response(
        name="Discover.Response",
        namespace="Alexa.Discovery",
        payload={"endpoints": discovery_endpoints},
    )


@_HANDLERS.register(("Alexa.Authorization", "AcceptGrant"))
async def _async_api_accept_grant(
    alexa: _alexa,
    config: _config,
    directive: AlexaDirective,
    _context: core.Context,
) -> AlexaResponse:
    """Create a API formatted AcceptGrant response.

    Async friendly.
    """
    auth_code = directive.payload["grant"]["code"]
    _LOGGER.debug(f"AcceptGrant code: {auth_code}")

    if config.supports_auth:
        await config.async_accept_grant(auth_code)

        if config.should_report_state:
            await alexa.async_enable_proactive_mode(config)

    return directive.response(
        name="AcceptGrant.Response", namespace="Alexa.Authorization", payload={}
    )


@_HANDLERS.register(("Alexa.PowerController", "TurnOn"))
async def _async_api_turn_on(
    alexa: _alexa,
    __config: _config,
    directive: AlexaDirective,
    context: core.Context,
) -> AlexaResponse:
    """Process a turn on request."""
    entity = directive.entity
    domain = _get_entity_platform(entity)

    service = _const.SERVICE_TURN_ON
    if domain == _platform.COVER:
        service = _cover.SERVICE_OPEN
    elif domain == _platform.VACUUM:
        supported = entity.attributes.get(_const.ATTR_SUPPORTED_FEATURES, 0)
        if (
            not supported & _vacuum.EntityFeature.TURN_ON
            and supported & _vacuum.EntityFeature.START
        ):
            service = _vacuum.SERVICE_START
    elif domain == _platform.TIMER:
        service = _timer.SERVICE_START
    elif domain == _platform.MEDIA_PLAYER:
        supported = entity.attributes.get(_const.ATTR_SUPPORTED_FEATURES, 0)
        power_features = (
            _media_player.EntityFeature.TURN_ON | _media_player.EntityFeature.TURN_OFF
        )
        if not supported & power_features:
            service = _const.SERVICE_MEDIA_PLAY

    await alexa.controller.services.async_call(
        domain,
        service,
        {_const.ATTR_ENTITY_ID: entity.entity_id},
        blocking=False,
        context=context,
    )

    return directive.response()


@_HANDLERS.register(("Alexa.PowerController", "TurnOff"))
async def _async_api_turn_off(
    alexa: _alexa,
    __config: _config,
    directive: AlexaDirective,
    context: core.Context,
) -> AlexaResponse:
    """Process a turn off request."""
    entity = directive.entity
    domain = _get_entity_platform(entity)

    service = _const.SERVICE_TURN_OFF
    if entity.domain == _platform.COVER:
        service = _cover.SERVICE_CLOSE
    elif domain == _platform.VACUUM:
        supported = entity.attributes.get(_const.ATTR_SUPPORTED_FEATURES, 0)
        if (
            not supported & _vacuum.EntityFeature.TURN_OFF
            and supported & _vacuum.EntityFeature.RETURN_HOME
        ):
            service = _vacuum.SERVICE_RETURN_TO_BASE
    elif domain == _platform.TIMER:
        service = _timer.SERVICE_CANCEL
    elif domain == _platform.MEDIA_PLAYER:
        supported = entity.attributes.get(_const.ATTR_SUPPORTED_FEATURES, 0)
        power_features = (
            _media_player.EntityFeature.TURN_ON | _media_player.EntityFeature.TURN_OFF
        )
        if not supported & power_features:
            service = _const.SERVICE_MEDIA_STOP

    await alexa.controller.services.async_call(
        domain,
        service,
        {_const.ATTR_ENTITY_ID: entity.entity_id},
        blocking=False,
        context=context,
    )

    return directive.response()


@_HANDLERS.register(("Alexa.BrightnessController", "SetBrightness"))
async def _async_api_set_brightness(
    alexa: _alexa,
    __config: _config,
    directive: AlexaDirective,
    context: core.Context,
) -> AlexaResponse:
    """Process a set brightness request."""
    entity = directive.entity
    brightness = int(directive.payload["brightness"])

    await alexa.controller.services.async_call(
        entity.domain,
        _const.SERVICE_TURN_ON,
        {
            _const.ATTR_ENTITY_ID: entity.entity_id,
            _light.ATTR_BRIGHTNESS_PCT: brightness,
        },
        blocking=False,
        context=context,
    )

    return directive.response()


@_HANDLERS.register(("Alexa.BrightnessController", "AdjustBrightness"))
async def _async_api_adjust_brightness(
    alexa: _alexa,
    __config: _config,
    directive: AlexaDirective,
    context: core.Context,
) -> AlexaResponse:
    """Process an adjust brightness request."""
    entity = directive.entity
    brightness_delta = int(directive.payload["brightnessDelta"])

    # set brightness
    await alexa.controller.services.async_call(
        entity.domain,
        _const.SERVICE_TURN_ON,
        {
            _const.ATTR_ENTITY_ID: entity.entity_id,
            _light.ATTR_BRIGHTNESS_STEP_PCT: brightness_delta,
        },
        blocking=False,
        context=context,
    )

    return directive.response()


@_HANDLERS.register(("Alexa.ColorController", "SetColor"))
async def _async_api_set_color(
    alexa: _alexa,
    __config: _config,
    directive: AlexaDirective,
    context: core.Context,
) -> AlexaResponse:
    """Process a set color request."""
    entity = directive.entity
    rgb = _color.hsb_to_RGB(
        float(directive.payload["color"]["hue"]),
        float(directive.payload["color"]["saturation"]),
        float(directive.payload["color"]["brightness"]),
    )

    await alexa.controller.services.async_call(
        entity.domain,
        _const.SERVICE_TURN_ON,
        {_const.ATTR_ENTITY_ID: entity.entity_id, _light.ATTR_RGB_COLOR: rgb},
        blocking=False,
        context=context,
    )

    return directive.response()


@_HANDLERS.register(("Alexa.ColorTemperatureController", "SetColorTemperature"))
async def _async_api_set_color_temperature(
    alexa: _alexa,
    __config: _config,
    directive: AlexaDirective,
    context: core.Context,
) -> AlexaResponse:
    """Process a set color temperature request."""
    entity = directive.entity
    kelvin = int(directive.payload["colorTemperatureInKelvin"])

    await alexa.controller.services.async_call(
        entity.domain,
        _const.SERVICE_TURN_ON,
        {_const.ATTR_ENTITY_ID: entity.entity_id, _light.ATTR_KELVIN: kelvin},
        blocking=False,
        context=context,
    )

    return directive.response()


@_HANDLERS.register(("Alexa.ColorTemperatureController", "DecreaseColorTemperature"))
async def _async_api_decrease_color_temp(
    alexa: _alexa,
    __config: _config,
    directive: AlexaDirective,
    context: core.Context,
) -> AlexaResponse:
    """Process a decrease color temperature request."""
    entity = directive.entity
    current = int(entity.attributes.get(_light.ATTR_COLOR_TEMP))
    max_mireds = int(entity.attributes.get(_light.ATTR_MAX_MIREDS))

    value = min(max_mireds, current + 50)
    await alexa.controller.services.async_call(
        entity.domain,
        _const.SERVICE_TURN_ON,
        {_const.ATTR_ENTITY_ID: entity.entity_id, _light.ATTR_COLOR_TEMP: value},
        blocking=False,
        context=context,
    )

    return directive.response()


@_HANDLERS.register(("Alexa.ColorTemperatureController", "IncreaseColorTemperature"))
async def _async_api_increase_color_temp(
    alexa: _alexa,
    __config: _config,
    directive: AlexaDirective,
    context: core.Context,
) -> AlexaResponse:
    """Process an increase color temperature request."""
    entity = directive.entity
    current = int(entity.attributes.get(_light.ATTR_COLOR_TEMP))
    min_mireds = int(entity.attributes.get(_light.ATTR_MIN_MIREDS))

    value = max(min_mireds, current - 50)
    await alexa.controller.services.async_call(
        entity.domain,
        _const.SERVICE_TURN_ON,
        {_const.ATTR_ENTITY_ID: entity.entity_id, _light.ATTR_COLOR_TEMP: value},
        blocking=False,
        context=context,
    )

    return directive.response()


@_HANDLERS.register(("Alexa.SceneController", "Activate"))
async def _async_api_activate(
    alexa: _alexa,
    __config: _config,
    directive: AlexaDirective,
    context: core.Context,
) -> AlexaResponse:
    """Process an activate request."""
    entity = directive.entity
    domain = entity.domain

    service = _const.SERVICE_TURN_ON
    if domain in (_platform.BUTTON, _platform.INPUT_BUTTON):
        service = _button.SERVICE_PRESS

    await alexa.controller.services.async_call(
        domain,
        service,
        {_const.ATTR_ENTITY_ID: entity.entity_id},
        blocking=False,
        context=context,
    )

    payload = {
        "cause": {"type": _alexa_const.Cause.VOICE_INTERACTION},
        "timestamp": core.helpers.utcnow().strftime(_alexa_const.DATE_FORMAT),
    }

    return directive.response(
        name="ActivationStarted", namespace="Alexa.SceneController", payload=payload
    )


@_HANDLERS.register(("Alexa.SceneController", "Deactivate"))
async def _async_api_deactivate(
    alexa: _alexa,
    __config: _config,
    directive: AlexaDirective,
    context: core.Context,
) -> AlexaResponse:
    """Process a deactivate request."""
    entity = directive.entity
    domain = entity.domain

    await alexa.controller.services.async_call(
        domain,
        _const.SERVICE_TURN_OFF,
        {_const.ATTR_ENTITY_ID: entity.entity_id},
        blocking=False,
        context=context,
    )

    payload = {
        "cause": {"type": _alexa_const.Cause.VOICE_INTERACTION},
        "timestamp": core.helpers.utcnow().strftime(_alexa_const.DATE_FORMAT),
    }

    return directive.response(
        name="DeactivationStarted", namespace="Alexa.SceneController", payload=payload
    )


@_HANDLERS.register(("Alexa.PercentageController", "SetPercentage"))
async def _async_api_set_percentage(
    alexa: _alexa,
    __config: _config,
    directive: AlexaDirective,
    context: core.Context,
) -> AlexaResponse:
    """Process a set percentage request."""
    entity = directive.entity

    if entity.domain != _platform.FAN:
        raise _alexa_const.InvalidDirectiveError(_DIRECTIVE_NOT_SUPPORTED)

    percentage = int(directive.payload["percentage"])
    service = _fan.SERVICE_SET_PERCENTAGE
    data = {
        _const.ATTR_ENTITY_ID: entity.entity_id,
        _fan.ATTR_PERCENTAGE: percentage,
    }

    await alexa.controller.services.async_call(
        entity.domain, service, data, blocking=False, context=context
    )

    return directive.response()


@_HANDLERS.register(("Alexa.PercentageController", "AdjustPercentage"))
async def _async_api_adjust_percentage(
    alexa: _alexa,
    __config: _config,
    directive: AlexaDirective,
    context: core.Context,
) -> AlexaResponse:
    """Process an adjust percentage request."""
    entity = directive.entity

    if entity.domain != _platform.FAN:
        raise _alexa_const.InvalidDirectiveError(_DIRECTIVE_NOT_SUPPORTED)

    percentage_delta = int(directive.payload["percentageDelta"])
    current = entity.attributes.get(_fan.ATTR_PERCENTAGE, 0)
    # set percentage
    percentage = min(100, max(0, percentage_delta + current))
    service = _fan.SERVICE_SET_PERCENTAGE
    data = {
        _const.ATTR_ENTITY_ID: entity.entity_id,
        _fan.ATTR_PERCENTAGE: percentage,
    }

    await alexa.controller.services.async_call(
        entity.domain, service, data, blocking=False, context=context
    )

    return directive.response()


@_HANDLERS.register(("Alexa.LockController", "Lock"))
async def _async_api_lock(
    alexa: _alexa,
    __config: _config,
    directive: AlexaDirective,
    context: core.Context,
) -> AlexaResponse:
    """Process a lock request."""
    entity = directive.entity
    await alexa.controller.services.async_call(
        entity.domain,
        _const.SERVICE_LOCK,
        {_const.ATTR_ENTITY_ID: entity.entity_id},
        blocking=False,
        context=context,
    )

    response = directive.response()
    response.add_context_property(
        {"name": "lockState", "namespace": "Alexa.LockController", "value": "LOCKED"}
    )
    return response


@_HANDLERS.register(("Alexa.LockController", "Unlock"))
async def _async_api_unlock(
    alexa: _alexa,
    config: _config,
    directive: AlexaDirective,
    context: core.Context,
) -> AlexaResponse:
    """Process an unlock request."""
    locale = config.locale
    if locale not in {"de-DE", "en-US", "ja-JP"}:
        msg = (
            f"The unlock directive is not supported for the following locales: {locale}"
        )
        raise _alexa_const.InvalidDirectiveError(msg)

    entity = directive.entity
    await alexa.controller.services.async_call(
        entity.domain,
        _const.SERVICE_UNLOCK,
        {_const.ATTR_ENTITY_ID: entity.entity_id},
        blocking=False,
        context=context,
    )

    response = directive.response()
    response.add_context_property(
        {"namespace": "Alexa.LockController", "name": "lockState", "value": "UNLOCKED"}
    )

    return response


@_HANDLERS.register(("Alexa.Speaker", "SetVolume"))
async def _async_api_set_volume(
    alexa: _alexa,
    __config: _config,
    directive: AlexaDirective,
    context: core.Context,
) -> AlexaResponse:
    """Process a set volume request."""
    volume = round(float(directive.payload["volume"] / 100), 2)
    entity = directive.entity

    data = {
        _const.ATTR_ENTITY_ID: entity.entity_id,
        _media_player.ATTR_MEDIA_VOLUME_LEVEL: volume,
    }

    await alexa.controller.services.async_call(
        entity.domain, _const.SERVICE_VOLUME_SET, data, blocking=False, context=context
    )

    return directive.response()


@_HANDLERS.register(("Alexa.InputController", "SelectInput"))
async def _async_api_select_input(
    alexa: _alexa,
    __config: _config,
    directive: AlexaDirective,
    context: core.Context,
) -> AlexaResponse:
    """Process a set input request."""
    media_input: str = directive.payload["input"]
    entity = directive.entity

    # Attempt to map the ALL UPPERCASE payload name to a source.
    # Strips trailing 1 to match single input devices.
    source_list = entity.attributes.get(_media_player.ATTR_INPUT_SOURCE_LIST, [])
    for source in source_list:
        formatted_source = (
            source.lower().replace("-", "").replace("_", "").replace(" ", "")
        )
        media_input = media_input.lower().replace(" ", "")
        if (
            formatted_source in _alexa_const.Inputs.VALID_SOURCE_NAME_MAP
            and formatted_source == media_input
        ) or (
            media_input.endswith("1") and formatted_source == media_input.rstrip("1")
        ):
            media_input = source
            break
    else:
        msg = (
            f"failed to map input {media_input} to a media source on {entity.entity_id}"
        )
        raise _alexa_const.InvalidValueError(msg)

    data = {
        _const.ATTR_ENTITY_ID: entity.entity_id,
        _media_player.ATTR_INPUT_SOURCE: media_input,
    }

    await alexa.controller.services.async_call(
        entity.domain,
        _media_player.SERVICE_SELECT_SOURCE,
        data,
        blocking=False,
        context=context,
    )

    return directive.response()


@_HANDLERS.register(("Alexa.Speaker", "AdjustVolume"))
async def _async_api_adjust_volume(
    alexa: _alexa,
    __config: _config,
    directive: AlexaDirective,
    context: core.Context,
) -> AlexaResponse:
    """Process an adjust volume request."""
    volume_delta = int(directive.payload["volume"])

    entity = directive.entity
    current_level = entity.attributes.get(_media_player.ATTR_MEDIA_VOLUME_LEVEL)

    # read current state
    try:
        current = math.floor(int(current_level * 100))
    except ZeroDivisionError:
        current = 0

    volume = float(max(0, volume_delta + current) / 100)

    data = {
        _const.ATTR_ENTITY_ID: entity.entity_id,
        _media_player.ATTR_MEDIA_VOLUME_LEVEL: volume,
    }

    await alexa.controller.services.async_call(
        entity.domain, _const.SERVICE_VOLUME_SET, data, blocking=False, context=context
    )

    return directive.response()


@_HANDLERS.register(("Alexa.StepSpeaker", "AdjustVolume"))
async def _async_api_adjust_volume_step(
    alexa: _alexa,
    __config: _config,
    directive: AlexaDirective,
    context: core.Context,
) -> AlexaResponse:
    """Process an adjust volume step request."""
    # media_player volume up/down service does not support specifying steps
    # each component handles it differently e.g. via config.
    # This workaround will simply call the volume up/Volume down the amount of steps asked for
    # When no steps are called in the request, Alexa sends a default of 10 steps which for most
    # purposes is too high. The default  is set 1 in this case.
    entity = directive.entity
    volume_int = int(directive.payload["volumeSteps"])
    is_default = bool(directive.payload["volumeStepsDefault"])
    default_steps = 1

    if volume_int < 0:
        service_volume = _const.SERVICE_VOLUME_DOWN
        if is_default:
            volume_int = -default_steps
    else:
        service_volume = _const.SERVICE_VOLUME_UP
        if is_default:
            volume_int = default_steps

    data = {_const.ATTR_ENTITY_ID: entity.entity_id}

    for _ in range(abs(volume_int)):
        await alexa.controller.services.async_call(
            entity.domain, service_volume, data, blocking=False, context=context
        )

    return directive.response()


@_HANDLERS.register(("Alexa.StepSpeaker", "SetMute"))
@_HANDLERS.register(("Alexa.Speaker", "SetMute"))
async def _async_api_set_mute(
    alexa: _alexa,
    __config: _config,
    directive: AlexaDirective,
    context: core.Context,
) -> AlexaResponse:
    """Process a set mute request."""
    mute = bool(directive.payload["mute"])
    entity = directive.entity
    data = {
        _const.ATTR_ENTITY_ID: entity.entity_id,
        _media_player.ATTR_MEDIA_VOLUME_MUTED: mute,
    }

    await alexa.controller.services.async_call(
        entity.domain, _const.SERVICE_VOLUME_MUTE, data, blocking=False, context=context
    )

    return directive.response()


@_HANDLERS.register(("Alexa.PlaybackController", "Play"))
async def _async_api_play(
    alexa: _alexa,
    __config: _config,
    directive: AlexaDirective,
    context: core.Context,
) -> AlexaResponse:
    """Process a play request."""
    entity = directive.entity
    data = {_const.ATTR_ENTITY_ID: entity.entity_id}

    await alexa.controller.services.async_call(
        entity.domain, _const.SERVICE_MEDIA_PLAY, data, blocking=False, context=context
    )

    return directive.response()


@_HANDLERS.register(("Alexa.PlaybackController", "Pause"))
async def _async_api_pause(
    alexa: _alexa,
    __config: _config,
    directive: AlexaDirective,
    context: core.Context,
) -> AlexaResponse:
    """Process a pause request."""
    entity = directive.entity
    data = {_const.ATTR_ENTITY_ID: entity.entity_id}

    await alexa.controller.services.async_call(
        entity.domain, _const.SERVICE_MEDIA_PAUSE, data, blocking=False, context=context
    )

    return directive.response()


@_HANDLERS.register(("Alexa.PlaybackController", "Stop"))
async def _async_api_stop(
    alexa: _alexa,
    __config: _config,
    directive: AlexaDirective,
    context: core.Context,
) -> AlexaResponse:
    """Process a stop request."""
    entity = directive.entity
    data = {_const.ATTR_ENTITY_ID: entity.entity_id}

    await alexa.controller.services.async_call(
        entity.domain, _const.SERVICE_MEDIA_STOP, data, blocking=False, context=context
    )

    return directive.response()


@_HANDLERS.register(("Alexa.PlaybackController", "Next"))
async def _async_api_next(
    alexa: _alexa,
    __config: _config,
    directive: AlexaDirective,
    context: core.Context,
) -> AlexaResponse:
    """Process a next request."""
    entity = directive.entity
    data = {_const.ATTR_ENTITY_ID: entity.entity_id}

    await alexa.controller.services.async_call(
        entity.domain,
        _const.SERVICE_MEDIA_NEXT_TRACK,
        data,
        blocking=False,
        context=context,
    )

    return directive.response()


@_HANDLERS.register(("Alexa.PlaybackController", "Previous"))
async def _async_api_previous(
    alexa: _alexa,
    __config: _config,
    directive: AlexaDirective,
    context: core.Context,
) -> AlexaResponse:
    """Process a previous request."""
    entity = directive.entity
    data = {_const.ATTR_ENTITY_ID: entity.entity_id}

    await alexa.controller.services.async_call(
        entity.domain,
        _const.SERVICE_MEDIA_PREVIOUS_TRACK,
        data,
        blocking=False,
        context=context,
    )

    return directive.response()


def _temperature_from_object(
    shc: core.SmartHomeController, temp_obj: dict, interval=False
):
    """Get temperature from Temperature object in requested unit."""
    from_unit = _const.UnitOfTemperature.CELSIUS
    temp = float(temp_obj["value"])

    if temp_obj["scale"] == "FAHRENHEIT":
        from_unit = _const.UnitOfTemperature.FAHRENHEIT
    elif temp_obj["scale"] == "KELVIN" and not interval:
        # convert to Celsius if absolute temperature
        temp -= 273.15

    return shc.config.units.temperature(temp, from_unit)


@_HANDLERS.register(("Alexa.ThermostatController", "SetTargetTemperature"))
async def _async_api_set_target_temp(
    alexa: _alexa,
    __config: _config,
    directive: AlexaDirective,
    context: core.Context,
) -> AlexaResponse:
    """Process a set target temperature request."""
    controller = alexa.controller
    entity = directive.entity
    min_temp = entity.attributes.get(_climate.ATTR_MIN_TEMP)
    max_temp = entity.attributes.get(_climate.ATTR_MAX_TEMP)
    unit = alexa.controller.config.units.temperature_unit

    data = {_const.ATTR_ENTITY_ID: entity.entity_id}

    payload = directive.payload
    response = directive.response()
    if "targetSetpoint" in payload:
        temp = _temperature_from_object(controller, payload["targetSetpoint"])
        if temp < min_temp or temp > max_temp:
            raise _alexa_const.TempRangeError(controller, temp, min_temp, max_temp)
        data[_const.ATTR_TEMPERATURE] = temp
        response.add_context_property(
            {
                "name": "targetSetpoint",
                "namespace": "Alexa.ThermostatController",
                "value": {"value": temp, "scale": _alexa_const.API_TEMP_UNITS[unit]},
            }
        )
    if "lowerSetpoint" in payload:
        temp_low = _temperature_from_object(alexa.controller, payload["lowerSetpoint"])
        if temp_low < min_temp or temp_low > max_temp:
            raise _alexa_const.TempRangeError(controller, temp_low, min_temp, max_temp)
        data[_climate.ATTR_TARGET_TEMP_LOW] = temp_low
        response.add_context_property(
            {
                "name": "lowerSetpoint",
                "namespace": "Alexa.ThermostatController",
                "value": {
                    "value": temp_low,
                    "scale": _alexa_const.API_TEMP_UNITS[unit],
                },
            }
        )
    if "upperSetpoint" in payload:
        temp_high = _temperature_from_object(controller, payload["upperSetpoint"])
        if temp_high < min_temp or temp_high > max_temp:
            raise _alexa_const.TempRangeError(controller, temp_high, min_temp, max_temp)
        data[_climate.ATTR_TARGET_TEMP_HIGH] = temp_high
        response.add_context_property(
            {
                "name": "upperSetpoint",
                "namespace": "Alexa.ThermostatController",
                "value": {
                    "value": temp_high,
                    "scale": _alexa_const.API_TEMP_UNITS[unit],
                },
            }
        )

    await controller.services.async_call(
        entity.domain,
        _climate.SERVICE_SET_TEMPERATURE,
        data,
        blocking=False,
        context=context,
    )

    return response


@_HANDLERS.register(("Alexa.ThermostatController", "AdjustTargetTemperature"))
async def _async_api_adjust_target_temp(
    alexa: _alexa,
    __config: _config,
    directive: AlexaDirective,
    context: core.Context,
) -> AlexaResponse:
    """Process an adjust target temperature request."""
    controller = alexa.controller
    entity = directive.entity
    min_temp = entity.attributes.get(_climate.ATTR_MIN_TEMP)
    max_temp = entity.attributes.get(_climate.ATTR_MAX_TEMP)
    unit = controller.config.units.temperature_unit

    temp_delta = _temperature_from_object(
        controller, directive.payload["targetSetpointDelta"], interval=True
    )
    target_temp = float(entity.attributes.get(_const.ATTR_TEMPERATURE)) + temp_delta

    if target_temp < min_temp or target_temp > max_temp:
        raise _alexa_const.TempRangeError(controller, target_temp, min_temp, max_temp)

    data = {
        _const.ATTR_ENTITY_ID: entity.entity_id,
        _const.ATTR_TEMPERATURE: target_temp,
    }

    response = directive.response()
    await controller.services.async_call(
        entity.domain,
        _climate.SERVICE_SET_TEMPERATURE,
        data,
        blocking=False,
        context=context,
    )
    response.add_context_property(
        {
            "name": "targetSetpoint",
            "namespace": "Alexa.ThermostatController",
            "value": {"value": target_temp, "scale": _alexa_const.API_TEMP_UNITS[unit]},
        }
    )

    return response


@_HANDLERS.register(("Alexa.ThermostatController", "SetThermostatMode"))
async def _async_api_set_thermostat_mode(
    alexa: _alexa,
    __config: _config,
    directive: AlexaDirective,
    context: core.Context,
) -> AlexaResponse:
    """Process a set thermostat mode request."""
    entity = directive.entity
    mode = directive.payload["thermostatMode"]
    mode = mode if isinstance(mode, str) else mode["value"]

    data = {_const.ATTR_ENTITY_ID: entity.entity_id}

    preset = next(
        (k for k, v in _alexa_const.API_THERMOSTAT_PRESETS.items() if v == mode), None
    )

    if preset:
        presets = entity.attributes.get(_climate.ATTR_PRESET_MODES, [])

        if preset not in presets:
            msg = f"The requested thermostat mode {preset} is not supported"
            raise _alexa_const.UnsupportedThermostatModeError(msg)

        service = _climate.SERVICE_SET_PRESET_MODE
        data[_climate.ATTR_PRESET_MODE] = preset

    elif mode == "CUSTOM":
        operation_list = entity.attributes.get(_climate.ATTR_HVAC_MODES)
        custom_mode = directive.payload["thermostatMode"]["customName"]
        custom_mode = next(
            (
                k
                for k, v in _alexa_const.API_THERMOSTAT_MODES_CUSTOM.items()
                if v == custom_mode
            ),
            None,
        )
        if custom_mode not in operation_list:
            msg = (
                f"The requested thermostat mode {mode}: {custom_mode} is not supported"
            )
            raise _alexa_const.UnsupportedThermostatModeError(msg)

        service = _climate.SERVICE_SET_HVAC_MODE
        data[_climate.ATTR_HVAC_MODE] = custom_mode

    else:
        operation_list = entity.attributes.get(_climate.ATTR_HVAC_MODES)
        shc_modes = {
            k: v for k, v in _alexa_const.API_THERMOSTAT_MODES.items() if v == mode
        }
        shc_mode = next(iter(set(shc_modes).intersection(operation_list)), None)
        if shc_mode not in operation_list:
            msg = f"The requested thermostat mode {mode} is not supported"
            raise _alexa_const.UnsupportedThermostatModeError(msg)

        service = _climate.SERVICE_SET_HVAC_MODE
        data[_climate.ATTR_HVAC_MODE] = shc_mode

    response = directive.response()
    await alexa.controller.services.async_call(
        _platform.CLIMATE.value, service, data, blocking=False, context=context
    )
    response.add_context_property(
        {
            "name": "thermostatMode",
            "namespace": "Alexa.ThermostatController",
            "value": mode,
        }
    )

    return response


@_HANDLERS.register(("Alexa", "ReportState"))
async def _async_api_reportstate(
    __alexa: _alexa,
    __config: _config,
    directive: AlexaDirective,
    _context: core.Context,
) -> AlexaResponse:
    """Process a ReportState request."""
    return directive.response(name="StateReport")


@_HANDLERS.register(("Alexa.SecurityPanelController", "Arm"))
async def _async_api_arm(
    alexa: _alexa,
    __config: _config,
    directive: AlexaDirective,
    context: core.Context,
) -> AlexaResponse:
    """Process a Security Panel Arm request."""
    entity = directive.entity
    service = None
    arm_state = directive.payload["armState"]
    data = {_const.ATTR_ENTITY_ID: entity.entity_id}

    if entity.state != _const.STATE_ALARM_DISARMED:
        msg = "You must disarm the system before you can set the requested arm state."
        raise _alexa_const.SecurityPanelAuthorizationRequired(msg)

    if arm_state == "ARMED_AWAY":
        service = _const.SERVICE_ALARM_ARM_AWAY
    elif arm_state == "ARMED_NIGHT":
        service = _const.SERVICE_ALARM_ARM_NIGHT
    elif arm_state == "ARMED_STAY":
        service = _const.SERVICE_ALARM_ARM_HOME
    else:
        raise _alexa_const.InvalidDirectiveError(_DIRECTIVE_NOT_SUPPORTED)

    await alexa.controller.services.async_call(
        entity.domain, service, data, blocking=False, context=context
    )

    # return 0 until alarm integration supports an exit delay
    payload = {"exitDelayInSeconds": 0}

    response = directive.response(
        name="Arm.Response", namespace="Alexa.SecurityPanelController", payload=payload
    )

    response.add_context_property(
        {
            "name": "armState",
            "namespace": "Alexa.SecurityPanelController",
            "value": arm_state,
        }
    )

    return response


@_HANDLERS.register(("Alexa.SecurityPanelController", "Disarm"))
async def _async_api_disarm(
    alexa: _alexa,
    __config: _config,
    directive: AlexaDirective,
    context: core.Context,
) -> AlexaResponse:
    """Process a Security Panel Disarm request."""
    entity = directive.entity
    data = {_const.ATTR_ENTITY_ID: entity.entity_id}
    response = directive.response()

    # Per Alexa Documentation: If you receive a Disarm directive,
    # and the system is already disarmed,
    # respond with a success response, not an error response.
    if entity.state == _const.STATE_ALARM_DISARMED:
        return response

    payload = directive.payload
    if "authorization" in payload:
        value = payload["authorization"]["value"]
        if payload["authorization"]["type"] == "FOUR_DIGIT_PIN":
            data["code"] = value

    await alexa.controller.services.async_call(
        entity.domain, _const.SERVICE_ALARM_DISARM, data, blocking=True, context=context
    )

    response.add_context_property(
        {
            "name": "armState",
            "namespace": "Alexa.SecurityPanelController",
            "value": "DISARMED",
        }
    )

    return response


@_HANDLERS.register(("Alexa.ModeController", "SetMode"))
async def _async_api_set_mode(
    alexa: _alexa,
    __config: _config,
    directive: AlexaDirective,
    context: core.Context,
) -> AlexaResponse:
    """Process a SetMode directive."""
    entity = directive.entity
    instance = directive.instance
    domain = entity.domain
    service = None
    data = {_const.ATTR_ENTITY_ID: entity.entity_id}
    mode = directive.payload["mode"]

    # Fan Direction
    if instance == f"{_platform.FAN}.{_fan.ATTR_DIRECTION}":
        direction = mode.split(".")[1]
        if direction in (_fan.DIRECTION_REVERSE, _fan.DIRECTION_FORWARD):
            service = _fan.SERVICE_SET_DIRECTION
            data[_fan.ATTR_DIRECTION] = direction

    # Fan preset_mode
    elif instance == f"{_platform.FAN}.{_fan.ATTR_PRESET_MODE}":
        preset_mode = mode.split(".")[1]
        if (
            preset_mode != _alexa_const.PRESET_MODE_NA
            and preset_mode in entity.attributes.get(_fan.ATTR_PRESET_MODES)
        ):
            service = _fan.SERVICE_SET_PRESET_MODE
            data[_fan.ATTR_PRESET_MODE] = preset_mode
        else:
            msg = f"Entity '{entity.entity_id}' does not support Preset '{preset_mode}'"
            raise _alexa_const.InvalidValueError(msg)

    # Cover Position
    elif instance == f"{_platform.COVER}.{_cover.ATTR_POSITION}":
        position = mode.split(".")[1]

        if position == _cover.STATE_CLOSED:
            service = _cover.SERVICE_CLOSE
        elif position == _cover.STATE_OPEN:
            service = _cover.SERVICE_OPEN
        elif position == "custom":
            service = _cover.SERVICE_STOP

    if not service:
        raise _alexa_const.InvalidDirectiveError(_DIRECTIVE_NOT_SUPPORTED)

    await alexa.controller.services.async_call(
        domain, service, data, blocking=False, context=context
    )

    response = directive.response()
    response.add_context_property(
        {
            "namespace": "Alexa.ModeController",
            "instance": instance,
            "name": "mode",
            "value": mode,
        }
    )

    return response


@_HANDLERS.register(("Alexa.ModeController", "AdjustMode"))
async def _async_api_adjust_mode(
    __alexa: _alexa,
    __config: _config,
    _directive: AlexaDirective,
    _context: core.Context,
) -> AlexaResponse:
    """Process a AdjustMode request.

    Requires capabilityResources supportedModes to be ordered.
    Only supportedModes with ordered=True support the adjustMode directive.
    """

    # Currently no supportedModes are configured with ordered=True to support this request.
    raise _alexa_const.InvalidDirectiveError(_DIRECTIVE_NOT_SUPPORTED)


@_HANDLERS.register(("Alexa.ToggleController", "TurnOn"))
async def _async_api_toggle_on(
    alexa: _alexa,
    __config: _config,
    directive: AlexaDirective,
    context: core.Context,
) -> AlexaResponse:
    """Process a toggle on request."""
    entity = directive.entity
    instance = directive.instance
    domain = entity.domain

    # Fan Oscillating
    if instance != f"{_platform.FAN}.{_fan.ATTR_OSCILLATING}":
        raise _alexa_const.InvalidDirectiveError(_DIRECTIVE_NOT_SUPPORTED)

    service = _fan.SERVICE_OSCILLATE
    data = {
        _const.ATTR_ENTITY_ID: entity.entity_id,
        _fan.ATTR_OSCILLATING: True,
    }

    await alexa.controller.services.async_call(
        domain, service, data, blocking=False, context=context
    )

    response = directive.response()
    response.add_context_property(
        {
            "namespace": "Alexa.ToggleController",
            "instance": instance,
            "name": "toggleState",
            "value": "ON",
        }
    )

    return response


@_HANDLERS.register(("Alexa.ToggleController", "TurnOff"))
async def _async_api_toggle_off(
    alexa: _alexa,
    __config: _config,
    directive: AlexaDirective,
    context: core.Context,
) -> AlexaResponse:
    """Process a toggle off request."""
    entity = directive.entity
    instance = directive.instance
    domain = entity.domain

    # Fan Oscillating
    if instance != f"{_platform.FAN}.{_fan.ATTR_OSCILLATING}":
        raise _alexa_const.InvalidDirectiveError(_DIRECTIVE_NOT_SUPPORTED)

    service = _fan.SERVICE_OSCILLATE
    data = {
        _const.ATTR_ENTITY_ID: entity.entity_id,
        _fan.ATTR_OSCILLATING: False,
    }

    await alexa.controller.services.async_call(
        domain, service, data, blocking=False, context=context
    )

    response = directive.response()
    response.add_context_property(
        {
            "namespace": "Alexa.ToggleController",
            "instance": instance,
            "name": "toggleState",
            "value": "OFF",
        }
    )

    return response


@_HANDLERS.register(("Alexa.RangeController", "SetRangeValue"))
async def _async_api_set_range(
    alexa: _alexa,
    __config: _config,
    directive: AlexaDirective,
    context: core.Context,
) -> AlexaResponse:
    """Process a next request."""
    entity = directive.entity
    instance = directive.instance
    domain = entity.domain
    service = None
    data = {_const.ATTR_ENTITY_ID: entity.entity_id}
    range_value = directive.payload["rangeValue"]

    # Cover Position
    if instance == f"{_platform.COVER}.{_cover.ATTR_POSITION}":
        range_value = int(range_value)
        if range_value == 0:
            service = _cover.SERVICE_CLOSE
        elif range_value == 100:
            service = _cover.SERVICE_OPEN
        else:
            service = _cover.SERVICE_SET_POSITION
            data[_cover.ATTR_POSITION] = range_value

    # Cover Tilt
    elif instance == f"{_platform.COVER}.tilt":
        range_value = int(range_value)
        if range_value == 0:
            service = _cover.SERVICE_CLOSE_TILT
        elif range_value == 100:
            service = _cover.SERVICE_OPEN_TILT
        else:
            service = _cover.SERVICE_SET_TILT_POSITION
            data[_cover.ATTR_TILT_POSITION] = range_value

    # Fan Speed
    elif instance == f"{_platform.FAN}.{_fan.ATTR_PERCENTAGE}":
        range_value = int(range_value)
        if range_value == 0:
            service = _const.SERVICE_TURN_OFF
        else:
            supported = entity.attributes.get(_const.ATTR_SUPPORTED_FEATURES, 0)
            if supported and _fan.EntityFeature.SET_SPEED:
                service = _fan.SERVICE_SET_PERCENTAGE
                data[_fan.ATTR_PERCENTAGE] = range_value
            else:
                service = _const.SERVICE_TURN_ON

    # Input Number Value
    elif instance == f"{_platform.INPUT_NUMBER}.{_input_number.ATTR_VALUE}":
        range_value = float(range_value)
        service = _input_number.SERVICE_SET_VALUE
        min_value = float(entity.attributes[_input_number.ATTR_MIN])
        max_value = float(entity.attributes[_input_number.ATTR_MAX])
        data[_input_number.ATTR_VALUE] = min(max_value, max(min_value, range_value))

    # Vacuum Fan Speed
    elif instance == f"{_platform.VACUUM}.{_vacuum.ATTR_FAN_SPEED}":
        service = _vacuum.SERVICE_SET_FAN_SPEED
        speed_list = entity.attributes[_vacuum.ATTR_FAN_SPEED_LIST]
        speed = next(
            (v for i, v in enumerate(speed_list) if i == int(range_value)), None
        )

        if not speed:
            msg = "Entity does not support value"
            raise _alexa_const.InvalidValueError(msg)

        data[_vacuum.ATTR_FAN_SPEED] = speed

    else:
        raise _alexa_const.InvalidDirectiveError(_DIRECTIVE_NOT_SUPPORTED)

    await alexa.controller.services.async_call(
        domain, service, data, blocking=False, context=context
    )

    response = directive.response()
    response.add_context_property(
        {
            "namespace": "Alexa.RangeController",
            "instance": instance,
            "name": "rangeValue",
            "value": range_value,
        }
    )

    return response


@_HANDLERS.register(("Alexa.RangeController", "AdjustRangeValue"))
async def _async_api_adjust_range(
    alexa: _alexa,
    __config: _config,
    directive: AlexaDirective,
    context: core.Context,
) -> AlexaResponse:
    """Process a next request."""
    entity = directive.entity
    instance = directive.instance
    domain = entity.domain
    service = None
    data: dict[str, typing.Any] = {_const.ATTR_ENTITY_ID: entity.entity_id}
    range_delta = directive.payload["rangeValueDelta"]
    range_delta_default = bool(directive.payload["rangeValueDeltaDefault"])
    response_value: int = 0

    # Cover Position
    if instance == f"{_platform.COVER}.{_cover.ATTR_POSITION}":
        range_delta = int(range_delta * 20) if range_delta_default else int(range_delta)
        service = _const.SERVICE_SET_COVER_POSITION
        if (current := entity.attributes.get(_cover.ATTR_POSITION)) is None:
            msg = f"Unable to determine {entity.entity_id} current position"
            raise _alexa_const.InvalidValueError(msg)
        position = response_value = min(100, max(0, range_delta + current))
        if position == 100:
            service = _cover.SERVICE_OPEN
        elif position == 0:
            service = _cover.SERVICE_CLOSE
        else:
            data[_cover.ATTR_POSITION] = position

    # Cover Tilt
    elif instance == f"{_platform.COVER}.tilt":
        range_delta = int(range_delta * 20) if range_delta_default else int(range_delta)
        service = _const.SERVICE_SET_COVER_TILT_POSITION
        current = entity.attributes.get(_cover.ATTR_TILT_POSITION)
        if current is None:
            msg = f"Unable to determine {entity.entity_id} current tilt position"
            raise _alexa_const.InvalidValueError(msg)
        tilt_position = response_value = min(100, max(0, range_delta + current))
        if tilt_position == 100:
            service = _cover.SERVICE_OPEN_TILT
        elif tilt_position == 0:
            service = _cover.SERVICE_CLOSE_TILT
        else:
            data[_cover.ATTR_TILT_POSITION] = tilt_position

    # Fan speed percentage
    elif instance == f"{_platform.FAN}.{_fan.ATTR_PERCENTAGE}":
        percentage_step = entity.attributes.get(_fan.ATTR_PERCENTAGE_STEP, 20)
        range_delta = (
            int(range_delta * percentage_step)
            if range_delta_default
            else int(range_delta)
        )
        service = _fan.SERVICE_SET_PERCENTAGE
        if (current := entity.attributes.get(_fan.ATTR_PERCENTAGE)) is None:
            msg = f"Unable to determine {entity.entity_id} current fan speed"
            raise _alexa_const.InvalidValueError(msg)
        percentage = response_value = min(100, max(0, range_delta + current))
        if percentage:
            data[_fan.ATTR_PERCENTAGE] = percentage
        else:
            service = _const.SERVICE_TURN_OFF

    # Input Number Value
    elif instance == f"{_platform.INPUT_NUMBER}.{_input_number.ATTR_VALUE}":
        range_delta = float(range_delta)
        service = _input_number.SERVICE_SET_VALUE
        min_value = float(entity.attributes[_input_number.ATTR_MIN])
        max_value = float(entity.attributes[_input_number.ATTR_MAX])
        current = float(entity.state)
        data[_input_number.ATTR_VALUE] = response_value = min(
            max_value, max(min_value, range_delta + current)
        )

    # Vacuum Fan Speed
    elif instance == f"{_platform.VACUUM}.{_vacuum.ATTR_FAN_SPEED}":
        range_delta = int(range_delta)
        service = _vacuum.SERVICE_SET_FAN_SPEED
        speed_list = entity.attributes[_vacuum.ATTR_FAN_SPEED_LIST]
        current_speed = entity.attributes[_vacuum.ATTR_FAN_SPEED]
        current_speed_index = next(
            (i for i, v in enumerate(speed_list) if v == current_speed), 0
        )
        new_speed_index = min(
            len(speed_list) - 1, max(0, current_speed_index + range_delta)
        )
        speed = next(
            (v for i, v in enumerate(speed_list) if i == new_speed_index), None
        )
        data[_vacuum.ATTR_FAN_SPEED] = response_value = speed

    else:
        raise _alexa_const.InvalidDirectiveError(_DIRECTIVE_NOT_SUPPORTED)

    await alexa.controller.services.async_call(
        domain, service, data, blocking=False, context=context
    )

    response = directive.response()
    response.add_context_property(
        {
            "namespace": "Alexa.RangeController",
            "instance": instance,
            "name": "rangeValue",
            "value": response_value,
        }
    )

    return response


@_HANDLERS.register(("Alexa.ChannelController", "ChangeChannel"))
async def _async_api_changechannel(
    alexa: _alexa,
    __config: _config,
    directive: AlexaDirective,
    context: core.Context,
) -> AlexaResponse:
    """Process a change channel request."""
    channel = "0"
    entity = directive.entity
    channel_payload = directive.payload["channel"]
    metadata_payload = directive.payload["channelMetadata"]
    payload_name = "number"

    if "number" in channel_payload:
        channel = channel_payload["number"]
        payload_name = "number"
    elif "callSign" in channel_payload:
        channel = channel_payload["callSign"]
        payload_name = "callSign"
    elif "affiliateCallSign" in channel_payload:
        channel = channel_payload["affiliateCallSign"]
        payload_name = "affiliateCallSign"
    elif "uri" in channel_payload:
        channel = channel_payload["uri"]
        payload_name = "uri"
    elif "name" in metadata_payload:
        channel = metadata_payload["name"]
        payload_name = "callSign"

    data = {
        _const.ATTR_ENTITY_ID: entity.entity_id,
        _media_player.ATTR_MEDIA_CONTENT_ID: channel,
        _media_player.ATTR_MEDIA_CONTENT_TYPE: _media_player.MediaType.CHANNEL,
    }

    await alexa.controller.services.async_call(
        entity.domain,
        _media_player.SERVICE_PLAY_MEDIA,
        data,
        blocking=False,
        context=context,
    )

    response = directive.response()

    response.add_context_property(
        {
            "namespace": "Alexa.ChannelController",
            "name": "channel",
            "value": {payload_name: channel},
        }
    )

    return response


@_HANDLERS.register(("Alexa.ChannelController", "SkipChannels"))
async def _async_api_skipchannel(
    alexa: _alexa,
    __config: _config,
    directive: AlexaDirective,
    context: core.Context,
) -> AlexaResponse:
    """Process a skipchannel request."""
    channel = int(directive.payload["channelCount"])
    entity = directive.entity

    data = {_const.ATTR_ENTITY_ID: entity.entity_id}

    if channel < 0:
        service_media = _const.SERVICE_MEDIA_PREVIOUS_TRACK
    else:
        service_media = _const.SERVICE_MEDIA_NEXT_TRACK

    for _ in range(abs(channel)):
        await alexa.controller.services.async_call(
            entity.domain, service_media, data, blocking=False, context=context
        )

    response = directive.response()

    response.add_context_property(
        {
            "namespace": "Alexa.ChannelController",
            "name": "channel",
            "value": {"number": ""},
        }
    )

    return response


@_HANDLERS.register(("Alexa.SeekController", "AdjustSeekPosition"))
async def _async_api_seek(
    alexa: _alexa,
    __config: _config,
    directive: AlexaDirective,
    context: core.Context,
) -> AlexaResponse:
    """Process a seek request."""
    entity = directive.entity
    position_delta = int(directive.payload["deltaPositionMilliseconds"])

    current_position = entity.attributes.get(_media_player.ATTR_MEDIA_POSITION)
    if current_position is None:
        msg = f"{entity} did not return the current media position."
        raise _alexa_const.VideoActionNotPermittedForContentError(msg)

    seek_position = max(int(current_position) + int(position_delta / 1000), 0)

    media_duration = entity.attributes.get(_media_player.ATTR_MEDIA_DURATION)
    if media_duration and 0 < int(media_duration) < seek_position:
        seek_position = media_duration

    data = {
        _const.ATTR_ENTITY_ID: entity.entity_id,
        _media_player.ATTR_MEDIA_SEEK_POSITION: seek_position,
    }

    await alexa.controller.services.async_call(
        str(_platform.MEDIA_PLAYER),
        _const.SERVICE_MEDIA_SEEK,
        data,
        blocking=False,
        context=context,
    )

    # convert seconds to milliseconds for StateReport.
    seek_position = int(seek_position * 1000)

    payload = {"properties": [{"name": "positionMilliseconds", "value": seek_position}]}
    return directive.response(
        name="StateReport", namespace="Alexa.SeekController", payload=payload
    )


@_HANDLERS.register(("Alexa.EqualizerController", "SetMode"))
async def _async_api_set_eq_mode(
    alexa: _alexa,
    __config: _config,
    directive: AlexaDirective,
    context: core.Context,
) -> AlexaResponse:
    """Process a SetMode request for EqualizerController."""
    mode = directive.payload["mode"]
    entity = directive.entity
    data = {_const.ATTR_ENTITY_ID: entity.entity_id}

    sound_mode_list = entity.attributes.get(_media_player.ATTR_SOUND_MODE_LIST)
    if sound_mode_list and mode.lower() in sound_mode_list:
        data[_media_player.ATTR_SOUND_MODE] = mode.lower()
    else:
        msg = f"failed to map sound mode {mode} to a mode on {entity.entity_id}"
        raise _alexa_const.InvalidValueError(msg)

    await alexa.controller.services.async_call(
        entity.domain,
        _media_player.SERVICE_SELECT_SOUND_MODE,
        data,
        blocking=False,
        context=context,
    )

    return directive.response()


@_HANDLERS.register(("Alexa.EqualizerController", "AdjustBands"))
@_HANDLERS.register(("Alexa.EqualizerController", "ResetBands"))
@_HANDLERS.register(("Alexa.EqualizerController", "SetBands"))
async def _async_api_bands_directive(
    __alexa: _alexa,
    __config: _config,
    _directive: AlexaDirective,
    _context: core.Context,
) -> AlexaResponse:
    """Handle an AdjustBands, ResetBands, SetBands request.

    Only mode directives are currently supported for the EqualizerController.
    """
    # Currently bands directives are not supported.
    raise _alexa_const.InvalidDirectiveError(_DIRECTIVE_NOT_SUPPORTED)


@_HANDLERS.register(("Alexa.TimeHoldController", "Hold"))
async def _async_api_hold(
    alexa: _alexa,
    __config: _config,
    directive: AlexaDirective,
    context: core.Context,
) -> AlexaResponse:
    """Process a TimeHoldController Hold request."""
    entity = directive.entity
    data = {_const.ATTR_ENTITY_ID: entity.entity_id}

    if entity.domain == _platform.TIMER:
        service = _timer.SERVICE_PAUSE

    elif entity.domain == _platform.VACUUM:
        service = _vacuum.SERVICE_START_PAUSE

    else:
        raise _alexa_const.InvalidDirectiveError(_DIRECTIVE_NOT_SUPPORTED)

    await alexa.controller.services.async_call(
        entity.domain, service, data, blocking=False, context=context
    )

    return directive.response()


@_HANDLERS.register(("Alexa.TimeHoldController", "Resume"))
async def _async_api_resume(
    alexa: _alexa,
    __config: _config,
    directive: AlexaDirective,
    context: core.Context,
) -> AlexaResponse:
    """Process a TimeHoldController Resume request."""
    entity = directive.entity
    data = {_const.ATTR_ENTITY_ID: entity.entity_id}

    if entity.domain == _platform.TIMER:
        service = _timer.SERVICE_START

    elif entity.domain == _platform.VACUUM:
        service = _vacuum.SERVICE_START_PAUSE

    else:
        raise _alexa_const.InvalidDirectiveError(_DIRECTIVE_NOT_SUPPORTED)

    await alexa.controller.services.async_call(
        entity.domain, service, data, blocking=False, context=context
    )

    return directive.response()


@_HANDLERS.register(("Alexa.CameraStreamController", "InitializeCameraStreams"))
async def _async_api_initialize_camera_stream(
    alexa: _alexa,
    __config: _config,
    directive: AlexaDirective,
    _context: core.Context,
) -> AlexaResponse:
    """Process a InitializeCameraStreams request."""
    entity = directive.entit
    camera: core.Camera.Component = alexa.controller.components.camera
    stream_source = await camera.async_request_stream(entity.entity_id, fmt="hls")
    state = alexa.controller.states.get(entity.entity_id)
    assert state
    camera_image = state.attributes[_const.ATTR_ENTITY_PICTURE]

    try:
        external_url = alexa.controller.get_url(
            allow_internal=False,
            allow_ip=False,
            require_ssl=True,
            require_standard_port=True,
        )
    except core.NoURLAvailableError as err:
        raise _alexa_const.InvalidValueError(
            "Failed to find suitable URL to serve to Alexa"
        ) from err

    payload = {
        "cameraStreams": [
            {
                "uri": f"{external_url}{stream_source}",
                "protocol": "HLS",
                "resolution": {"width": 1280, "height": 720},
                "authorizationType": "NONE",
                "videoCodec": "H264",
                "audioCodec": "AAC",
            }
        ],
        "imageUri": f"{external_url}{camera_image}",
    }
    return directive.response(
        name="Response", namespace="Alexa.CameraStreamController", payload=payload
    )
