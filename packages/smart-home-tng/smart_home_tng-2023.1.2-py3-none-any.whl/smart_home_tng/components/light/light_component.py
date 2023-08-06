"""
Light Component for Smart Home - The Next Generation.

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
import logging
import datetime as dt
import typing
import voluptuous as vol

from ... import core
from .light_intent_handler import LightIntentHandler

_cv: typing.TypeAlias = core.ConfigValidation
_light: typing.TypeAlias = core.Light
_color: typing.TypeAlias = core.helpers.Color
_intent: typing.TypeAlias = core.Intent
_significant_change: typing.TypeAlias = core.SignificantChange
_toggle: typing.TypeAlias = core.Toggle

_LOGGER: typing.Final = logging.getLogger(__name__)
_TYPE_BRIGHTNESS_INCREASE: typing.Final = "brightness_increase"
_TYPE_BRIGHTNESS_DECREASE: typing.Final = "brightness_decrease"
_TYPE_FLASH: typing.Final = "flash"


def _preprocess_data(data):
    """Preprocess the service data."""
    base = {
        entity_field: data.pop(entity_field)
        for entity_field in _cv.ENTITY_SERVICE_FIELDS
        if entity_field in data
    }

    _light.preprocess_turn_on_alternatives(data)
    base["params"] = data
    return base


# pylint: disable=unused-variable, too-many-ancestors
class LightComponent(
    core.SmartHomeControllerComponent,
    core.ActionPlatform,
    core.ConditionPlatform,
    core.GroupPlatform,
    _intent.Platform,
    core.RecorderPlatform,
    core.ReproduceStatePlatform,
    core.SignificantChangePlatform,
):
    """Provides functionality to interact with lights."""

    def __init__(self, path: typing.Iterable[str]):
        super().__init__(path)
        self._entity_component: core.EntityComponent = None
        self._supported_platforms = frozenset(
            [
                core.Platform.ACTION,
                core.Platform.CONDITION,
                core.Platform.GROUP,
                core.Platform.INTENT,
                core.Platform.RECORDER,
                core.Platform.REPRODUCE_STATE,
                core.Platform.SIGNIFICANT_CHANGE,
                core.Platform.TRIGGER,
            ]
        )

    @property
    def entity_component(self) -> core.EntityComponent:
        return self._entity_component

    @property
    def scan_interval(self) -> dt.timedelta:
        return dt.timedelta(seconds=30)

    def _is_on(self, entity_id: str) -> bool:
        """Return if the lights are on based on the statemachine."""
        return self.controller.states.is_state(entity_id, core.Const.STATE_ON)

    async def async_setup(self, config: core.ConfigType) -> bool:
        """Expose light control via state machine and services."""
        component = self._entity_component = core.EntityComponent(
            _LOGGER, self.domain, self.controller, self.scan_interval
        )
        await component.async_setup(config)

        await _light.PROFILES.async_initialize()

        # Listen for light on and light off service calls.

        component.async_register_entity_service(
            core.Const.SERVICE_TURN_ON,
            vol.All(
                _cv.make_entity_service_schema(_light.TURN_ON_SCHEMA), _preprocess_data
            ),
            self._async_handle_light_on_service,
        )

        component.async_register_entity_service(
            core.Const.SERVICE_TURN_OFF,
            vol.All(
                _cv.make_entity_service_schema(_light.TURN_OFF_SCHEMA), _preprocess_data
            ),
            self._async_handle_light_off_service,
        )

        component.async_register_entity_service(
            core.Const.SERVICE_TOGGLE,
            vol.All(
                _cv.make_entity_service_schema(_light.TURN_ON_SCHEMA), _preprocess_data
            ),
            self._async_handle_toggle_service,
        )

        return True

    async def _async_handle_light_off_service(self, light, call):
        """Handle turning off a light."""
        params = dict(call.data["params"])

        if _light.ATTR_TRANSITION not in params:
            _light.PROFILES.apply_default(light.entity_id, True, params)

        await light.async_turn_off(**_light.filter_turn_off_params(light, params))

    async def _async_handle_toggle_service(self, light, call):
        """Handle toggling a light."""
        if light.is_on:
            await self._async_handle_light_off_service(light, call)
        else:
            await self._async_handle_light_on_service(light, call)

    async def _async_handle_light_on_service(self, light, call):
        """Handle turning a light on.

        If brightness is set to 0, this service will turn the light off.
        """
        params = dict(call.data["params"])

        # Only process params once we processed brightness step
        if params and (
            _light.ATTR_BRIGHTNESS_STEP in params
            or _light.ATTR_BRIGHTNESS_STEP_PCT in params
        ):
            brightness = light.brightness if light.is_on else 0

            if _light.ATTR_BRIGHTNESS_STEP in params:
                brightness += params.pop(_light.ATTR_BRIGHTNESS_STEP)

            else:
                brightness += round(
                    params.pop(_light.ATTR_BRIGHTNESS_STEP_PCT) / 100 * 255
                )

            params[_light.ATTR_BRIGHTNESS] = max(0, min(255, brightness))

            _light.preprocess_turn_on_alternatives(params)

        if (not params or not light.is_on) or (
            params and _light.ATTR_TRANSITION not in params
        ):
            _light.PROFILES.apply_default(light.entity_id, light.is_on, params)

        legacy_supported_color_modes = (
            light._light_internal_supported_color_modes  # pylint: disable=protected-access
        )
        supported_color_modes = light.supported_color_modes

        # If a color temperature is specified, emulate it if not supported by the light
        if _light.ATTR_COLOR_TEMP in params:
            if (
                supported_color_modes
                and _light.ColorMode.COLOR_TEMP not in supported_color_modes
                and _light.ColorMode.RGBWW in supported_color_modes
            ):
                color_temp = params.pop(_light.ATTR_COLOR_TEMP)
                brightness = params.get(_light.ATTR_BRIGHTNESS, light.brightness)
                params[_light.ATTR_RGBWW_COLOR] = _color.temperature_to_rgbww(
                    color_temp, brightness, light.min_mireds, light.max_mireds
                )
            elif _light.ColorMode.COLOR_TEMP not in legacy_supported_color_modes:
                color_temp = params.pop(_light.ATTR_COLOR_TEMP)
                if _light.color_supported(legacy_supported_color_modes):
                    temp_k = _color.temperature_mired_to_kelvin(color_temp)
                    params[_light.ATTR_HS_COLOR] = _color.temperature_to_hs(temp_k)

        # If a color is specified, convert to the color space supported by the light
        # Backwards compatibility: Fall back to hs color if light.supported_color_modes
        # is not implemented
        if not supported_color_modes:
            if (rgb_color := params.pop(_light.ATTR_RGB_COLOR, None)) is not None:
                params[_light.ATTR_HS_COLOR] = _color.RGB_to_hs(*rgb_color)
            elif (xy_color := params.pop(_light.ATTR_XY_COLOR, None)) is not None:
                params[_light.ATTR_HS_COLOR] = _color.xy_to_hs(*xy_color)
            elif (rgbw_color := params.pop(_light.ATTR_RGBW_COLOR, None)) is not None:
                rgb_color = _color.rgbw_to_rgb(*rgbw_color)
                params[_light.ATTR_HS_COLOR] = _color.RGB_to_hs(*rgb_color)
            elif (rgbww_color := params.pop(_light.ATTR_RGBWW_COLOR, None)) is not None:
                rgb_color = _color.rgbww_to_rgb(
                    *rgbww_color, light.min_mireds, light.max_mireds
                )
                params[_light.ATTR_HS_COLOR] = _color.RGB_to_hs(*rgb_color)
        elif (
            _light.ATTR_HS_COLOR in params
            and _light.ColorMode.HS not in supported_color_modes
        ):
            hs_color = params.pop(_light.ATTR_HS_COLOR)
            if _light.ColorMode.RGB in supported_color_modes:
                params[_light.ATTR_RGB_COLOR] = _color.hs_to_RGB(*hs_color)
            elif _light.ColorMode.RGBW in supported_color_modes:
                rgb_color = _color.hs_to_RGB(*hs_color)
                params[_light.ATTR_RGBW_COLOR] = _color.rgb_to_rgbw(*rgb_color)
            elif _light.ColorMode.RGBWW in supported_color_modes:
                rgb_color = _color.hs_to_RGB(*hs_color)
                params[_light.ATTR_RGBWW_COLOR] = _color.rgb_to_rgbww(
                    *rgb_color, light.min_mireds, light.max_mireds
                )
            elif _light.ColorMode.XY in supported_color_modes:
                params[_light.ATTR_XY_COLOR] = _color.hs_to_xy(*hs_color)
        elif (
            _light.ATTR_RGB_COLOR in params
            and _light.ColorMode.RGB not in supported_color_modes
        ):
            rgb_color = params.pop(_light.ATTR_RGB_COLOR)
            if _light.ColorMode.RGBW in supported_color_modes:
                params[_light.ATTR_RGBW_COLOR] = _color.rgb_to_rgbw(*rgb_color)
            elif _light.ColorMode.RGBWW in supported_color_modes:
                params[_light.ATTR_RGBWW_COLOR] = _color.rgb_to_rgbww(
                    *rgb_color, light.min_mireds, light.max_mireds
                )
            elif _light.ColorMode.HS in supported_color_modes:
                params[_light.ATTR_HS_COLOR] = _color.RGB_to_hs(*rgb_color)
            elif _light.ColorMode.XY in supported_color_modes:
                params[_light.ATTR_XY_COLOR] = _color.RGB_to_xy(*rgb_color)
        elif (
            _light.ATTR_XY_COLOR in params
            and _light.ColorMode.XY not in supported_color_modes
        ):
            xy_color = params.pop(_light.ATTR_XY_COLOR)
            if _light.ColorMode.HS in supported_color_modes:
                params[_light.ATTR_HS_COLOR] = _color.xy_to_hs(*xy_color)
            elif _light.ColorMode.RGB in supported_color_modes:
                params[_light.ATTR_RGB_COLOR] = _color.xy_to_RGB(*xy_color)
            elif _light.ColorMode.RGBW in supported_color_modes:
                rgb_color = _color.xy_to_RGB(*xy_color)
                params[_light.ATTR_RGBW_COLOR] = _color.rgb_to_rgbw(*rgb_color)
            elif _light.ColorMode.RGBWW in supported_color_modes:
                rgb_color = _color.xy_to_RGB(*xy_color)
                params[_light.ATTR_RGBWW_COLOR] = _color.rgb_to_rgbww(
                    *rgb_color, light.min_mireds, light.max_mireds
                )
        elif (
            _light.ATTR_RGBW_COLOR in params
            and _light.ColorMode.RGBW not in supported_color_modes
        ):
            rgbw_color = params.pop(_light.ATTR_RGBW_COLOR)
            rgb_color = _color.rgbw_to_rgb(*rgbw_color)
            if _light.ColorMode.RGB in supported_color_modes:
                params[_light.ATTR_RGB_COLOR] = rgb_color
            elif _light.ColorMode.RGBWW in supported_color_modes:
                params[_light.ATTR_RGBWW_COLOR] = _color.rgb_to_rgbww(
                    *rgb_color, light.min_mireds, light.max_mireds
                )
            elif _light.ColorMode.HS in supported_color_modes:
                params[_light.ATTR_HS_COLOR] = _color.RGB_to_hs(*rgb_color)
            elif _light.ColorMode.XY in supported_color_modes:
                params[_light.ATTR_XY_COLOR] = _color.RGB_to_xy(*rgb_color)
        elif (
            _light.ATTR_RGBWW_COLOR in params
            and _light.ColorMode.RGBWW not in supported_color_modes
        ):
            rgbww_color = params.pop(_light.ATTR_RGBWW_COLOR)
            rgb_color = _color.rgbww_to_rgb(
                *rgbww_color, light.min_mireds, light.max_mireds
            )
            if _light.ColorMode.RGB in supported_color_modes:
                params[_light.ATTR_RGB_COLOR] = rgb_color
            elif _light.ColorMode.RGBW in supported_color_modes:
                params[_light.ATTR_RGBW_COLOR] = _color.rgb_to_rgbw(*rgb_color)
            elif _light.ColorMode.HS in supported_color_modes:
                params[_light.ATTR_HS_COLOR] = _color.RGB_to_hs(*rgb_color)
            elif _light.ColorMode.XY in supported_color_modes:
                params[_light.ATTR_XY_COLOR] = _color.RGB_to_xy(*rgb_color)

        # If both white and brightness are specified, override white
        if (
            supported_color_modes
            and _light.ATTR_WHITE in params
            and _light.ColorMode.WHITE in supported_color_modes
        ):
            params[_light.ATTR_WHITE] = params.pop(
                _light.ATTR_BRIGHTNESS, params[_light.ATTR_WHITE]
            )

        # Remove deprecated white value if the light supports color mode
        if (
            params.get(_light.ATTR_BRIGHTNESS) == 0
            or params.get(_light.ATTR_WHITE) == 0
        ):
            await self._async_handle_light_off_service(light, call)
        else:
            await light.async_turn_on(**_light.filter_turn_on_params(light, params))

    async def async_setup_entry(self, entry: core.ConfigEntry) -> bool:
        """Set up a config entry."""
        return await self.entity_component.async_setup_entry(entry)

    async def async_unload_entry(self, entry: core.ConfigEntry) -> bool:
        """Unload a config entry."""
        return await self.entity_component.async_unload_entry(entry)

    # ---------------------- Action Platform ----------------------------------

    @property
    def action_schema(self) -> typing.Callable[[core.ConfigType], core.ConfigType]:
        """Validate Action Configuration"""
        ACTION_SCHEMA: typing.Final = _cv.DEVICE_ACTION_BASE_SCHEMA.extend(
            {
                vol.Required(core.Const.ATTR_ENTITY_ID): _cv.entity_id,
                vol.Required(core.Const.CONF_DOMAIN): self.domain,
                vol.Required(core.Const.CONF_TYPE): vol.In(
                    _toggle.DEVICE_ACTION_TYPES
                    + [
                        _TYPE_BRIGHTNESS_INCREASE,
                        _TYPE_BRIGHTNESS_DECREASE,
                        _TYPE_FLASH,
                    ]
                ),
                vol.Optional(_light.ATTR_BRIGHTNESS_PCT): _light.VALID_BRIGHTNESS_PCT,
                vol.Optional(_light.ATTR_FLASH): _light.VALID_FLASH,
            }
        )
        return ACTION_SCHEMA

    async def async_call_action_from_config(
        self,
        config: core.ConfigType,
        variables: dict[str, typing.Any],
        context: core.Context,
    ) -> None:
        """Change state based on configuration."""
        action_type = config[core.Const.CONF_TYPE]
        if (
            action_type in _toggle.DEVICE_ACTION_TYPES
            and action_type != _toggle.CONF_TURN_ON
        ):
            await _toggle.async_call_action_from_config(
                self.controller, config, variables, context, self.domain
            )
            return

        data = {core.Const.ATTR_ENTITY_ID: config[core.Const.ATTR_ENTITY_ID]}

        if action_type == _TYPE_BRIGHTNESS_INCREASE:
            data[_light.ATTR_BRIGHTNESS_STEP_PCT] = 10
        elif action_type == _TYPE_BRIGHTNESS_DECREASE:
            data[_light.ATTR_BRIGHTNESS_STEP_PCT] = -10
        elif _light.ATTR_BRIGHTNESS_PCT in config:
            data[_light.ATTR_BRIGHTNESS_PCT] = config[_light.ATTR_BRIGHTNESS_PCT]

        if action_type == _TYPE_FLASH:
            if _light.ATTR_FLASH in config:
                data[_light.ATTR_FLASH] = config[_light.ATTR_FLASH]
            else:
                data[_light.ATTR_FLASH] = _light.FLASH_SHORT

        await self.controller.services.async_call(
            self.domain,
            core.Const.SERVICE_TURN_ON,
            data,
            blocking=True,
            context=context,
        )

    # ---------------------- Condition Platform ----------------------------------

    @property
    def condition_schema(self) -> typing.Callable[[core.ConfigType], core.ConfigType]:
        CONDITION_SCHEMA: typing.Final = _toggle.CONDITION_SCHEMA.extend(
            {vol.Required(core.Const.CONF_DOMAIN): self.domain}
        )
        return CONDITION_SCHEMA

    async def async_condition_from_config(
        self, config: core.ConfigType
    ) -> core.ConditionCheckerType:
        """Evaluate state based on configuration."""
        return _toggle.async_condition_from_config(self.controller, config)

    async def async_get_conditions(
        self, device_id: str
    ) -> list[dict[str, typing.Any]] | typing.Awaitable[list[dict[str, typing.Any]]]:
        """List device conditions."""
        return await _toggle.async_get_conditions(
            self.controller, device_id, self.domain
        )

    async def async_get_condition_capabilities(
        self, config: core.ConfigType
    ) -> dict[str, vol.Schema] | typing.Awaitable[dict[str, vol.Schema]]:
        """List condition capabilities."""
        return await _toggle.async_get_condition_capabilities(self.controller, config)

    # ---------------------- Group Platform ----------------------------------

    @core.callback
    def async_describe_on_off_states(
        self, registry: core.GroupIntegrationRegistry
    ) -> None:
        """Describe group on off states."""
        registry.on_off_states({core.Const.STATE_ON}, core.Const.STATE_OFF)

    # ------------------------ Intent Platform ----------------------------------

    async def async_setup_intents(self) -> None:
        """Set up the light intents."""
        self.controller.intents.register_handler(LightIntentHandler(self))

    # ---------------------- Recorder Platform ----------------------------------

    @core.callback
    def exclude_attributes(self) -> set[str]:
        """Exclude static attributes from being recorded in the database."""
        return {
            _light.ATTR_SUPPORTED_COLOR_MODES,
            _light.ATTR_EFFECT_LIST,
            _light.ATTR_MIN_MIREDS,
            _light.ATTR_MAX_MIREDS,
        }

    # --------------------- Reproduce State Platform ------------------------------

    async def async_reproduce_states(
        self,
        states: typing.Iterable[core.State],
        *,
        context: core.Context = None,
        reproduce_options: dict[str, typing.Any] = None,
    ) -> None:
        """Reproduce Light states."""
        await asyncio.gather(
            *(
                _async_reproduce_state(
                    self, state, context=context, reproduce_options=reproduce_options
                )
                for state in states
            )
        )

    # -------------------- Significant Change Platform ---------------------------

    @core.callback
    def check_significant_change(
        self,
        old_state: str,
        old_attrs: dict,
        new_state: str,
        new_attrs: dict,
        **kwargs: typing.Any,
    ) -> bool:
        """Test if state significantly changed."""
        if old_state != new_state:
            return True

        if old_attrs.get(_light.ATTR_EFFECT) != new_attrs.get(_light.ATTR_EFFECT):
            return True

        old_color = old_attrs.get(_light.ATTR_HS_COLOR)
        new_color = new_attrs.get(_light.ATTR_HS_COLOR)

        if old_color and new_color:
            # Range 0..360
            if _significant_change.check_absolute_change(old_color[0], new_color[0], 5):
                return True

            # Range 0..100
            if _significant_change.check_absolute_change(old_color[1], new_color[1], 3):
                return True

        if _significant_change.check_absolute_change(
            old_attrs.get(_light.ATTR_BRIGHTNESS),
            new_attrs.get(_light.ATTR_BRIGHTNESS),
            3,
        ):
            return True

        if _significant_change.check_absolute_change(
            # Default range 153..500
            old_attrs.get(_light.ATTR_COLOR_TEMP),
            new_attrs.get(_light.ATTR_COLOR_TEMP),
            5,
        ):
            return True

        return False


_VALID_STATES: typing.Final = {core.Const.STATE_ON, core.Const.STATE_OFF}

_ATTR_GROUP: typing.Final = [
    _light.ATTR_BRIGHTNESS,
    _light.ATTR_BRIGHTNESS_PCT,
    _light.ATTR_EFFECT,
    _light.ATTR_FLASH,
    _light.ATTR_TRANSITION,
]

_COLOR_GROUP: typing.Final = [
    _light.ATTR_HS_COLOR,
    _light.ATTR_COLOR_TEMP,
    _light.ATTR_RGB_COLOR,
    _light.ATTR_RGBW_COLOR,
    _light.ATTR_RGBWW_COLOR,
    _light.ATTR_XY_COLOR,
    # The following color attributes are deprecated
    _light.ATTR_PROFILE,
    _light.ATTR_COLOR_NAME,
    _light.ATTR_KELVIN,
]


class ColorModeAttr(typing.NamedTuple):
    """Map service data parameter to state attribute for a color mode."""

    parameter: str
    state_attr: str


_COLOR_MODE_TO_ATTRIBUTE: typing.Final = {
    _light.ColorMode.COLOR_TEMP: ColorModeAttr(
        _light.ATTR_COLOR_TEMP, _light.ATTR_COLOR_TEMP
    ),
    _light.ColorMode.HS: ColorModeAttr(_light.ATTR_HS_COLOR, _light.ATTR_HS_COLOR),
    _light.ColorMode.RGB: ColorModeAttr(_light.ATTR_RGB_COLOR, _light.ATTR_RGB_COLOR),
    _light.ColorMode.RGBW: ColorModeAttr(
        _light.ATTR_RGBW_COLOR, _light.ATTR_RGBW_COLOR
    ),
    _light.ColorMode.RGBWW: ColorModeAttr(
        _light.ATTR_RGBWW_COLOR, _light.ATTR_RGBWW_COLOR
    ),
    _light.ColorMode.WHITE: ColorModeAttr(_light.ATTR_WHITE, _light.ATTR_BRIGHTNESS),
    _light.ColorMode.XY: ColorModeAttr(_light.ATTR_XY_COLOR, _light.ATTR_XY_COLOR),
}

_DEPRECATED_GROUP: typing.Final = [
    _light.ATTR_BRIGHTNESS_PCT,
    _light.ATTR_COLOR_NAME,
    _light.ATTR_FLASH,
    _light.ATTR_KELVIN,
    _light.ATTR_PROFILE,
    _light.ATTR_TRANSITION,
]

_DEPRECATION_WARNING: typing.Final = (
    "The use of other attributes than device state attributes is deprecated and "
    + "will be removed in a future release. Invalid attributes are %s. Read the "
    + "logs for further details: https://www.home-assistant.io/integrations/scene/"
)


def _color_mode_same(cur_state: core.State, state: core.State) -> bool:
    """Test if color_mode is same."""
    cur_color_mode = cur_state.attributes.get(
        _light.ATTR_COLOR_MODE, _light.ColorMode.UNKNOWN
    )
    saved_color_mode = state.attributes.get(
        _light.ATTR_COLOR_MODE, _light.ColorMode.UNKNOWN
    )

    # Guard for scenes etc. which where created before color modes were introduced
    if saved_color_mode == _light.ColorMode.UNKNOWN:
        return True
    return cur_color_mode == saved_color_mode


async def _async_reproduce_state(
    light: LightComponent,
    state: core.State,
    *,
    context: core.Context = None,
    reproduce_options: dict[str, typing.Any] = None,
) -> None:
    """Reproduce a single state."""
    if (cur_state := light.controller.states.get(state.entity_id)) is None:
        _LOGGER.warning(f"Unable to find entity {state.entity_id}")
        return

    if state.state not in _VALID_STATES:
        _LOGGER.warning(f"Invalid state specified for {state.entity_id}: {state.state}")
        return

    # Warn if deprecated attributes are used
    deprecated_attrs = [attr for attr in state.attributes if attr in _DEPRECATED_GROUP]
    if deprecated_attrs:
        _LOGGER.warning(_DEPRECATION_WARNING, deprecated_attrs)

    # Return if we are already at the right state.
    if (
        cur_state.state == state.state
        and _color_mode_same(cur_state, state)
        and all(
            _check_attr_equal(cur_state.attributes, state.attributes, attr)
            for attr in _ATTR_GROUP + _COLOR_GROUP
        )
    ):
        return

    service_data: dict[str, typing.Any] = {core.Const.ATTR_ENTITY_ID: state.entity_id}

    if reproduce_options is not None and _light.ATTR_TRANSITION in reproduce_options:
        service_data[_light.ATTR_TRANSITION] = reproduce_options[_light.ATTR_TRANSITION]

    if state.state == core.Const.STATE_ON:
        service = core.Const.SERVICE_TURN_ON
        for attr in _ATTR_GROUP:
            # All attributes that are not colors
            if attr in state.attributes:
                service_data[attr] = state.attributes[attr]

        if (
            state.attributes.get(_light.ATTR_COLOR_MODE, _light.ColorMode.UNKNOWN)
            != _light.ColorMode.UNKNOWN
        ):
            color_mode = state.attributes[_light.ATTR_COLOR_MODE]
            if color_mode_attr := _COLOR_MODE_TO_ATTRIBUTE.get(color_mode):
                if color_mode_attr.state_attr not in state.attributes:
                    _LOGGER.warning(
                        f"Color mode {color_mode} specified but attribute "
                        + f"{color_mode_attr.state_attr} missing for: "
                        + f"{state.entity_id}"
                    )
                    return
                service_data[color_mode_attr.parameter] = state.attributes[
                    color_mode_attr.state_attr
                ]
        else:
            # Fall back to Choosing the first color that is specified
            for color_attr in _COLOR_GROUP:
                if color_attr in state.attributes:
                    service_data[color_attr] = state.attributes[color_attr]
                    break

    elif state.state == core.Const.STATE_OFF:
        service = core.Const.SERVICE_TURN_OFF

    await light.controller.services.async_call(
        light.domain, service, service_data, context=context, blocking=True
    )


def _check_attr_equal(
    attr1: typing.Mapping, attr2: typing.Mapping, attr_str: str
) -> bool:
    """Return true if the given attributes are equal."""
    return attr1.get(attr_str) == attr2.get(attr_str)
