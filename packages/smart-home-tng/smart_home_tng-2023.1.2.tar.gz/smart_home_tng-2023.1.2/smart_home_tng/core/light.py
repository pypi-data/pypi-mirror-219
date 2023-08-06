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

# pylint: disable=unused-variable

import csv
import dataclasses
import enum
import logging
import os
import typing

import voluptuous as vol

from ..backports import strenum
from .helpers.color import Color
from .callback import callback
from .config_validation import ConfigValidation as _cv
from .current_controller import _get_current_controller
from .smart_home_controller_error import SmartHomeControllerError
from .toggle import Toggle

if not typing.TYPE_CHECKING:

    class SmartHomeController:
        pass


if typing.TYPE_CHECKING:
    from .smart_home_controller import SmartHomeController

_LOGGER: typing.Final = logging.getLogger(__name__)


class _EntityFeature(enum.IntEnum):
    """Supported features of the light entity."""

    EFFECT = 4
    FLASH = 8
    TRANSITION = 32


# These SUPPORT_* constants are deprecated as of Home Assistant 2022.5.
# Please use the LightEntityFeature enum instead.
_SUPPORT_BRIGHTNESS: typing.Final = 1  # Deprecated, replaced by color modes
_SUPPORT_COLOR_TEMP: typing.Final = 2  # Deprecated, replaced by color modes
_SUPPORT_COLOR: typing.Final = 16  # Deprecated, replaced by color modes

# Color mode of the light
_ATTR_COLOR_MODE: typing.Final = "color_mode"
# List of color modes supported by the light
_ATTR_SUPPORTED_COLOR_MODES: typing.Final = "supported_color_modes"


class _ColorMode(strenum.LowercaseStrEnum):
    """Possible light color modes."""

    UNKNOWN = enum.auto()  # Ambiguous color mode
    ONOFF = enum.auto()  # Must be the only supported mode
    BRIGHTNESS = enum.auto()  # Must be the only supported mode
    COLOR_TEMP = enum.auto()
    HS = enum.auto()
    XY = enum.auto()
    RGB = enum.auto()
    RGBW = enum.auto()
    RGBWW = enum.auto()
    WHITE = enum.auto()  # Must *NOT* be the only supported mode


_VALID_COLOR_MODES: typing.Final = frozenset(
    {
        _ColorMode.ONOFF,
        _ColorMode.BRIGHTNESS,
        _ColorMode.COLOR_TEMP,
        _ColorMode.HS,
        _ColorMode.XY,
        _ColorMode.RGB,
        _ColorMode.RGBW,
        _ColorMode.RGBWW,
        _ColorMode.WHITE,
    }
)
_COLOR_MODES_BRIGHTNESS: typing.Final = frozenset(
    _VALID_COLOR_MODES - {_ColorMode.ONOFF}
)
_COLOR_MODES_COLOR: typing.Final = frozenset(
    {
        _ColorMode.HS,
        _ColorMode.RGB,
        _ColorMode.RGBW,
        _ColorMode.RGBWW,
        _ColorMode.XY,
    }
)

# Float that represents transition time in seconds to make change.
_ATTR_TRANSITION: typing.Final = "transition"

# Lists holding color values
_ATTR_RGB_COLOR: typing.Final = "rgb_color"
_ATTR_RGBW_COLOR: typing.Final = "rgbw_color"
_ATTR_RGBWW_COLOR: typing.Final = "rgbww_color"
_ATTR_XY_COLOR: typing.Final = "xy_color"
_ATTR_HS_COLOR: typing.Final = "hs_color"
_ATTR_COLOR_TEMP: typing.Final = "color_temp"
_ATTR_KELVIN: typing.Final = "kelvin"
_ATTR_MIN_MIREDS: typing.Final = "min_mireds"
_ATTR_MAX_MIREDS: typing.Final = "max_mireds"
_ATTR_COLOR_NAME: typing.Final = "color_name"
_ATTR_WHITE: typing.Final = "white"

# Brightness of the light, 0..255 or percentage
_ATTR_BRIGHTNESS: typing.Final = "brightness"
_ATTR_BRIGHTNESS_PCT: typing.Final = "brightness_pct"
_ATTR_BRIGHTNESS_STEP: typing.Final = "brightness_step"
_ATTR_BRIGHTNESS_STEP_PCT: typing.Final = "brightness_step_pct"

# String representing a profile (built-in ones or external defined).
_ATTR_PROFILE: typing.Final = "profile"

# If the light should flash, can be FLASH_SHORT or FLASH_LONG.
_ATTR_FLASH: typing.Final = "flash"
_FLASH_SHORT: typing.Final = "short"
_FLASH_LONG: typing.Final = "long"

# List of possible effects
_ATTR_EFFECT_LIST: typing.Final = "effect_list"

# Apply an effect to the light, can be EFFECT_COLORLOOP.
_ATTR_EFFECT: typing.Final = "effect"
_EFFECT_COLORLOOP: typing.Final = "colorloop"
_EFFECT_RANDOM: typing.Final = "random"
_EFFECT_WHITE: typing.Final = "white"

_COLOR_GROUP: typing.Final = "Color descriptors"

_LIGHT_PROFILES_FILE: typing.Final = "light_profiles.csv"

# Service call validation schemas
_VALID_TRANSITION: typing.Final = vol.All(vol.Coerce(float), vol.Clamp(min=0, max=6553))
_VALID_BRIGHTNESS: typing.Final = vol.All(vol.Coerce(int), vol.Clamp(min=0, max=255))
_VALID_BRIGHTNESS_PCT: typing.Final = vol.All(
    vol.Coerce(float), vol.Range(min=0, max=100)
)
_VALID_BRIGHTNESS_STEP: typing.Final = vol.All(
    vol.Coerce(int), vol.Clamp(min=-255, max=255)
)
_VALID_BRIGHTNESS_STEP_PCT: typing.Final = vol.All(
    vol.Coerce(float), vol.Clamp(min=-100, max=100)
)
_VALID_FLASH: typing.Final = vol.In([_FLASH_SHORT, _FLASH_LONG])

_LIGHT_TURN_ON_SCHEMA: typing.Final = {
    vol.Exclusive(_ATTR_PROFILE, _COLOR_GROUP): _cv.string,
    _ATTR_TRANSITION: _VALID_TRANSITION,
    vol.Exclusive(_ATTR_BRIGHTNESS, _ATTR_BRIGHTNESS): _VALID_BRIGHTNESS,
    vol.Exclusive(_ATTR_BRIGHTNESS_PCT, _ATTR_BRIGHTNESS): _VALID_BRIGHTNESS_PCT,
    vol.Exclusive(_ATTR_BRIGHTNESS_STEP, _ATTR_BRIGHTNESS): _VALID_BRIGHTNESS_STEP,
    vol.Exclusive(
        _ATTR_BRIGHTNESS_STEP_PCT, _ATTR_BRIGHTNESS
    ): _VALID_BRIGHTNESS_STEP_PCT,
    vol.Exclusive(_ATTR_COLOR_NAME, _COLOR_GROUP): _cv.string,
    vol.Exclusive(_ATTR_COLOR_TEMP, _COLOR_GROUP): vol.All(
        vol.Coerce(int), vol.Range(min=1)
    ),
    vol.Exclusive(_ATTR_KELVIN, _COLOR_GROUP): _cv.positive_int,
    vol.Exclusive(_ATTR_HS_COLOR, _COLOR_GROUP): vol.All(
        vol.Coerce(tuple),
        vol.ExactSequence(
            (
                vol.All(vol.Coerce(float), vol.Range(min=0, max=360)),
                vol.All(vol.Coerce(float), vol.Range(min=0, max=100)),
            )
        ),
    ),
    vol.Exclusive(_ATTR_RGB_COLOR, _COLOR_GROUP): vol.All(
        vol.Coerce(tuple), vol.ExactSequence((_cv.byte,) * 3)
    ),
    vol.Exclusive(_ATTR_RGBW_COLOR, _COLOR_GROUP): vol.All(
        vol.Coerce(tuple), vol.ExactSequence((_cv.byte,) * 4)
    ),
    vol.Exclusive(_ATTR_RGBWW_COLOR, _COLOR_GROUP): vol.All(
        vol.Coerce(tuple), vol.ExactSequence((_cv.byte,) * 5)
    ),
    vol.Exclusive(_ATTR_XY_COLOR, _COLOR_GROUP): vol.All(
        vol.Coerce(tuple), vol.ExactSequence((_cv.small_float, _cv.small_float))
    ),
    vol.Exclusive(_ATTR_WHITE, _COLOR_GROUP): _VALID_BRIGHTNESS,
    _ATTR_FLASH: _VALID_FLASH,
    _ATTR_EFFECT: _cv.string,
}

_LIGHT_TURN_OFF_SCHEMA: typing.Final = {
    _ATTR_TRANSITION: _VALID_TRANSITION,
    _ATTR_FLASH: _VALID_FLASH,
}


def _coerce_none(value: str) -> None:
    """Coerce an empty string as None."""

    if not isinstance(value, str):
        raise vol.Invalid("Expected a string")

    if value:
        raise vol.Invalid("Not an empty string")


_PROFILE_SCHEMA: typing.Final = vol.Schema(
    vol.Any(
        vol.ExactSequence(
            (
                str,
                vol.Any(_cv.small_float, _coerce_none),
                vol.Any(_cv.small_float, _coerce_none),
                vol.Any(_cv.byte, _coerce_none),
            )
        ),
        vol.ExactSequence(
            (
                str,
                vol.Any(_cv.small_float, _coerce_none),
                vol.Any(_cv.small_float, _coerce_none),
                vol.Any(_cv.byte, _coerce_none),
                vol.Any(_VALID_TRANSITION, _coerce_none),
            )
        ),
    )
)


@dataclasses.dataclass
class _Profile:
    """Representation of a profile."""

    name: str
    color_x: float = dataclasses.field(repr=False)
    color_y: float = dataclasses.field(repr=False)
    brightness: int
    transition: int = None
    hs_color: tuple[float, float] = dataclasses.field(init=False)

    # pylint: disable=invalid-name
    SCHEMA: vol.Schema = dataclasses.field(init=False)

    def __post_init__(self) -> None:
        """Convert xy to hs color."""
        if None in (self.color_x, self.color_y):
            self.hs_color = None
            return

        self.hs_color = Color.xy_to_hs(
            typing.cast(float, self.color_x), typing.cast(float, self.color_y)
        )

    @classmethod
    def from_csv_row(cls, csv_row: list[str]):
        """Create profile from a CSV row tuple."""
        return cls(*_PROFILE_SCHEMA(csv_row))


class _Profiles:
    """Representation of available color profiles."""

    def __init__(self) -> None:
        """Initialize profiles."""
        self._shc: SmartHomeController = None
        self._data: dict[str, _Profile] = {}

    @property
    def controller(self) -> SmartHomeController:
        if self._shc is None:
            self._shc = _get_current_controller()
        return self._shc

    def _load_profile_data(self) -> dict[str, _Profile]:
        """Load built-in profiles and custom profiles."""
        profile_paths = [
            os.path.join(
                os.path.dirname(__file__), "../components/light/", _LIGHT_PROFILES_FILE
            ),
            self.controller.config.path(_LIGHT_PROFILES_FILE),
        ]
        profiles = {}

        for profile_path in profile_paths:
            if not os.path.isfile(profile_path):
                continue
            with open(profile_path, encoding="utf8") as inp:
                reader = csv.reader(inp)

                # Skip the header
                next(reader, None)

                try:
                    for rec in reader:
                        profile = _Profile.from_csv_row(rec)
                        profiles[profile.name] = profile

                except vol.MultipleInvalid as ex:
                    _LOGGER.error(
                        f"Error parsing light profile row '{rec}' from {profile_path}: {ex}",
                    )
                    continue
        return profiles

    async def async_initialize(self) -> None:
        """Load and cache profiles."""
        self._data = await self.controller.async_add_executor_job(
            self._load_profile_data
        )

    @callback
    def apply_default(self, entity_id: str, state_on: bool, params: dict) -> None:
        """Return the default profile for the given light."""
        for _entity_id in (entity_id, "group.all_lights"):
            name = f"{_entity_id}.default"
            if name in self._data:
                if not state_on or not params:
                    self.apply_profile(name, params)
                elif self._data[name].transition is not None:
                    params.setdefault(_ATTR_TRANSITION, self._data[name].transition)

    @callback
    def apply_profile(self, name: str, params: dict) -> None:
        """Apply a profile."""
        if (profile := self._data.get(name)) is None:
            return

        color_attributes = (
            _ATTR_COLOR_NAME,
            _ATTR_COLOR_TEMP,
            _ATTR_HS_COLOR,
            _ATTR_RGB_COLOR,
            _ATTR_RGBW_COLOR,
            _ATTR_RGBWW_COLOR,
            _ATTR_XY_COLOR,
            _ATTR_WHITE,
        )

        if profile.hs_color is not None and not any(
            color_attribute in params for color_attribute in color_attributes
        ):
            params[_ATTR_HS_COLOR] = profile.hs_color
        if profile.brightness is not None:
            params.setdefault(_ATTR_BRIGHTNESS, profile.brightness)
        if profile.transition is not None:
            params.setdefault(_ATTR_TRANSITION, profile.transition)


_PROFILES: typing.Final = _Profiles()


@dataclasses.dataclass
class _EntityDescription(Toggle.EntityDescription):
    """A class that describes binary sensor entities."""


class _Entity(Toggle.Entity):
    """Base class for light entities."""

    _entity_description: _EntityDescription
    _attr_brightness: int = None
    _attr_color_mode: _ColorMode | str = None
    _attr_color_temp: int = None
    _attr_effect_list: list[str] = None
    _attr_effect: str = None
    _attr_hs_color: tuple[float, float] = None
    _attr_max_mireds: int = 500
    _attr_min_mireds: int = 153
    _attr_rgb_color: tuple[int, int, int] = None
    _attr_rgbw_color: tuple[int, int, int, int] = None
    _attr_rgbww_color: tuple[int, int, int, int, int] | None = None
    _attr_supported_color_modes: set[_ColorMode] | set[str] = None
    _attr_supported_features: int = 0
    _attr_xy_color: tuple[float, float] = None

    @property
    def entity_description(self) -> _EntityDescription:
        return super().entity_description

    @property
    def brightness(self) -> int:
        """Return the brightness of this light between 0..255."""
        return self._attr_brightness

    @property
    def color_mode(self) -> _ColorMode | str:
        """Return the color mode of the light."""
        return self._attr_color_mode

    @property
    def _light_internal_color_mode(self) -> str:
        """Return the color mode of the light with backwards compatibility."""
        if (color_mode := self.color_mode) is None:
            # Backwards compatibility for color_mode added in 2021.4
            # Add warning in 2021.6, remove in 2021.10
            supported = self._light_internal_supported_color_modes

            if _ColorMode.HS in supported and self.hs_color is not None:
                return _ColorMode.HS
            if _ColorMode.COLOR_TEMP in supported and self.color_temp is not None:
                return _ColorMode.COLOR_TEMP
            if _ColorMode.BRIGHTNESS in supported and self.brightness is not None:
                return _ColorMode.BRIGHTNESS
            if _ColorMode.ONOFF in supported:
                return _ColorMode.ONOFF
            return _ColorMode.UNKNOWN

        return color_mode

    @property
    def hs_color(self) -> tuple[float, float]:
        """Return the hue and saturation color value [float, float]."""
        return self._attr_hs_color

    @property
    def xy_color(self) -> tuple[float, float]:
        """Return the xy color value [float, float]."""
        return self._attr_xy_color

    @property
    def rgb_color(self) -> tuple[int, int, int]:
        """Return the rgb color value [int, int, int]."""
        return self._attr_rgb_color

    @property
    def rgbw_color(self) -> tuple[int, int, int, int]:
        """Return the rgbw color value [int, int, int, int]."""
        return self._attr_rgbw_color

    @property
    def _light_internal_rgbw_color(self) -> tuple[int, int, int, int]:
        """Return the rgbw color value [int, int, int, int]."""
        rgbw_color = self.rgbw_color
        return rgbw_color

    @property
    def rgbww_color(self) -> tuple[int, int, int, int, int]:
        """Return the rgbww color value [int, int, int, int, int]."""
        return self._attr_rgbww_color

    @property
    def color_temp(self) -> int:
        """Return the CT color value in mireds."""
        return self._attr_color_temp

    @property
    def min_mireds(self) -> int:
        """Return the coldest color_temp that this light supports."""
        # Default to the Philips Hue value that HA has always assumed
        # https://developers.meethue.com/documentation/core-concepts
        return self._attr_min_mireds

    @property
    def max_mireds(self) -> int:
        """Return the warmest color_temp that this light supports."""
        # Default to the Philips Hue value that HA has always assumed
        # https://developers.meethue.com/documentation/core-concepts
        return self._attr_max_mireds

    @property
    def effect_list(self) -> list[str]:
        """Return the list of supported effects."""
        return self._attr_effect_list

    @property
    def effect(self) -> str:
        """Return the current effect."""
        return self._attr_effect

    @property
    def capability_attributes(self):
        """Return capability attributes."""
        data = {}
        supported_features = self.supported_features
        supported_color_modes = self._light_internal_supported_color_modes

        if _ColorMode.COLOR_TEMP in supported_color_modes:
            data[_ATTR_MIN_MIREDS] = self.min_mireds
            data[_ATTR_MAX_MIREDS] = self.max_mireds

        if supported_features & _EntityFeature.EFFECT:
            data[_ATTR_EFFECT_LIST] = self.effect_list

        data[_ATTR_SUPPORTED_COLOR_MODES] = sorted(supported_color_modes)

        return data

    def _light_internal_convert_color(self, color_mode: _ColorMode | str) -> dict:
        data: dict[str, tuple] = {}
        if color_mode == _ColorMode.HS and self.hs_color:
            hs_color = self.hs_color
            data[_ATTR_HS_COLOR] = (round(hs_color[0], 3), round(hs_color[1], 3))
            data[_ATTR_RGB_COLOR] = Color.hs_to_RGB(*hs_color)
            data[_ATTR_XY_COLOR] = Color.hs_to_xy(*hs_color)
        elif color_mode == _ColorMode.XY and self.xy_color:
            xy_color = self.xy_color
            data[_ATTR_HS_COLOR] = Color.xy_to_hs(*xy_color)
            data[_ATTR_RGB_COLOR] = Color.xy_to_RGB(*xy_color)
            data[_ATTR_XY_COLOR] = (round(xy_color[0], 6), round(xy_color[1], 6))
        elif color_mode == _ColorMode.RGB and self.rgb_color:
            rgb_color = self.rgb_color
            data[_ATTR_HS_COLOR] = Color.RGB_to_hs(*rgb_color)
            data[_ATTR_RGB_COLOR] = tuple(int(x) for x in rgb_color[0:3])
            data[_ATTR_XY_COLOR] = Color.RGB_to_xy(*rgb_color)
        elif color_mode == _ColorMode.RGBW and self._light_internal_rgbw_color:
            rgbw_color = self._light_internal_rgbw_color
            rgb_color = Color.rgbw_to_rgb(*rgbw_color)
            data[_ATTR_HS_COLOR] = Color.RGB_to_hs(*rgb_color)
            data[_ATTR_RGB_COLOR] = tuple(int(x) for x in rgb_color[0:3])
            data[_ATTR_RGBW_COLOR] = tuple(int(x) for x in rgbw_color[0:4])
            data[_ATTR_XY_COLOR] = Color.RGB_to_xy(*rgb_color)
        elif color_mode == _ColorMode.RGBWW and self.rgbww_color:
            rgbww_color = self.rgbww_color
            rgb_color = Color.rgbww_to_rgb(
                *rgbww_color, self.min_mireds, self.max_mireds
            )
            data[_ATTR_HS_COLOR] = Color.RGB_to_hs(*rgb_color)
            data[_ATTR_RGB_COLOR] = tuple(int(x) for x in rgb_color[0:3])
            data[_ATTR_RGBWW_COLOR] = tuple(int(x) for x in rgbww_color[0:5])
            data[_ATTR_XY_COLOR] = Color.RGB_to_xy(*rgb_color)
        elif color_mode == _ColorMode.COLOR_TEMP and self.color_temp:
            hs_color = Color.temperature_to_hs(
                Color.temperature_mired_to_kelvin(self.color_temp)
            )
            data[_ATTR_HS_COLOR] = (round(hs_color[0], 3), round(hs_color[1], 3))
            data[_ATTR_RGB_COLOR] = Color.hs_to_RGB(*hs_color)
            data[_ATTR_XY_COLOR] = Color.hs_to_xy(*hs_color)
        return data

    @typing.final
    @property
    def state_attributes(self):
        """Return state attributes."""
        if not self.is_on:
            return None

        data = {}
        supported_features = self.supported_features
        color_mode = self._light_internal_color_mode

        if color_mode not in self._light_internal_supported_color_modes:
            # Increase severity to warning in 2021.6, reject in 2021.10
            _LOGGER.debug(
                f"{self.entity_id}: set to unsupported color_mode: {color_mode}, "
                + f"supported_color_modes: {self._light_internal_supported_color_modes}",
            )

        data[_ATTR_COLOR_MODE] = color_mode

        if color_mode in _COLOR_MODES_BRIGHTNESS:
            data[_ATTR_BRIGHTNESS] = self.brightness

        if color_mode == _ColorMode.COLOR_TEMP:
            data[_ATTR_COLOR_TEMP] = self.color_temp

        if color_mode in _COLOR_MODES_COLOR or color_mode == _ColorMode.COLOR_TEMP:
            data.update(self._light_internal_convert_color(color_mode))

        if supported_features & _EntityFeature.EFFECT:
            data[_ATTR_EFFECT] = self.effect

        return {key: val for key, val in data.items() if val is not None}

    @property
    def _light_internal_supported_color_modes(self) -> set[_ColorMode] | set[str]:
        """Calculate supported color modes with backwards compatibility."""
        if (supported_modes := self.supported_color_modes) is not None:
            return supported_modes

        # Backwards compatibility for supported_color_modes added in 2021.4
        # Add warning in 2021.6, remove in 2021.10
        supported_features = self.supported_features
        supported_color_modes: set[_ColorMode] = set()

        if supported_features & _ColorMode.COLOR_TEMP:
            supported_color_modes.add(_ColorMode.COLOR_TEMP)
        if supported_features & _SUPPORT_COLOR:
            supported_color_modes.add(_ColorMode.HS)
        if supported_features & _SUPPORT_BRIGHTNESS and not supported_color_modes:
            supported_color_modes = {_ColorMode.BRIGHTNESS}

        if not supported_color_modes:
            supported_color_modes = {_ColorMode.ONOFF}

        return supported_color_modes

    @property
    def supported_color_modes(self) -> set[_ColorMode] | set[str]:
        """Flag supported color modes."""
        return self._attr_supported_color_modes

    @property
    def supported_features(self) -> int:
        """Flag supported features."""
        return self._attr_supported_features


def _legacy_supported_features(
    supported_features: int, supported_color_modes: list[str]
) -> int:
    """Calculate supported features with backwards compatibility."""
    # Backwards compatibility for supported_color_modes added in 2021.4
    if supported_color_modes is None:
        return supported_features
    if any(mode in supported_color_modes for mode in _COLOR_MODES_COLOR):
        supported_features |= _SUPPORT_COLOR
    if any(mode in supported_color_modes for mode in _COLOR_MODES_BRIGHTNESS):
        supported_features |= _SUPPORT_BRIGHTNESS
    if _ColorMode.COLOR_TEMP in supported_color_modes:
        supported_features |= _SUPPORT_COLOR_TEMP

    return supported_features


# pylint: disable=invalid-name
class Light:
    """Light namespace."""

    Entity: typing.TypeAlias = _Entity
    EntityDescription: typing.TypeAlias = _EntityDescription
    EntityFeature: typing.TypeAlias = _EntityFeature

    ColorMode: typing.TypeAlias = _ColorMode
    Profile: typing.TypeAlias = _Profile
    Profiles: typing.TypeAlias = _Profiles

    PLATFORM_SCHEMA: typing.Final = _cv.PLATFORM_SCHEMA
    PLATFORM_SCHEMA_BASE: typing.Final = _cv.PLATFORM_SCHEMA_BASE
    PROFILES: typing.Final = _PROFILES

    ATTR_COLOR_MODE: typing.Final = _ATTR_COLOR_MODE
    ATTR_SUPPORTED_COLOR_MODES: typing.Final = _ATTR_SUPPORTED_COLOR_MODES

    # Float that represents transition time in seconds to make change.
    ATTR_TRANSITION: typing.Final = _ATTR_TRANSITION

    # Lists holding color values
    ATTR_RGB_COLOR: typing.Final = _ATTR_RGB_COLOR
    ATTR_RGBW_COLOR: typing.Final = _ATTR_RGBW_COLOR
    ATTR_RGBWW_COLOR: typing.Final = _ATTR_RGBWW_COLOR
    ATTR_XY_COLOR: typing.Final = _ATTR_XY_COLOR
    ATTR_HS_COLOR: typing.Final = _ATTR_HS_COLOR
    ATTR_COLOR_TEMP: typing.Final = _ATTR_COLOR_TEMP
    ATTR_KELVIN: typing.Final = _ATTR_KELVIN
    ATTR_MIN_MIREDS: typing.Final = _ATTR_MIN_MIREDS
    ATTR_MAX_MIREDS: typing.Final = _ATTR_MAX_MIREDS
    ATTR_COLOR_NAME: typing.Final = _ATTR_COLOR_NAME
    ATTR_WHITE: typing.Final = _ATTR_WHITE

    # Brightness of the light, 0..255 or percentage
    ATTR_BRIGHTNESS: typing.Final = _ATTR_BRIGHTNESS
    ATTR_BRIGHTNESS_PCT: typing.Final = _ATTR_BRIGHTNESS_PCT
    ATTR_BRIGHTNESS_STEP: typing.Final = _ATTR_BRIGHTNESS_STEP
    ATTR_BRIGHTNESS_STEP_PCT: typing.Final = _ATTR_BRIGHTNESS_STEP_PCT

    # String representing a profile (built-in ones or external defined).
    ATTR_PROFILE: typing.Final = _ATTR_PROFILE

    # If the light should flash, can be FLASH_SHORT or FLASH_LONG.
    ATTR_FLASH: typing.Final = _ATTR_FLASH
    FLASH_SHORT: typing.Final = _FLASH_SHORT
    FLASH_LONG: typing.Final = _FLASH_LONG

    # List of possible effects
    ATTR_EFFECT_LIST: typing.Final = _ATTR_EFFECT_LIST

    # Apply an effect to the light, can be EFFECT_COLORLOOP.
    ATTR_EFFECT: typing.Final = _ATTR_EFFECT
    EFFECT_COLORLOOP: typing.Final = _EFFECT_COLORLOOP
    EFFECT_RANDOM: typing.Final = _EFFECT_RANDOM
    EFFECT_WHITE: typing.Final = _EFFECT_WHITE

    COLOR_GROUP: typing.Final = _COLOR_GROUP

    PROFILES_FILE: typing.Final = _LIGHT_PROFILES_FILE

    # Service call validation schemas
    VALID_TRANSITION: typing.Final = _VALID_TRANSITION
    VALID_BRIGHTNESS: typing.Final = _VALID_BRIGHTNESS
    VALID_BRIGHTNESS_PCT: typing.Final = _VALID_BRIGHTNESS_PCT
    VALID_BRIGHTNESS_STEP: typing.Final = _VALID_BRIGHTNESS_STEP
    VALID_BRIGHTNESS_STEP_PCT: typing.Final = _VALID_BRIGHTNESS_STEP_PCT
    VALID_FLASH: typing.Final = _VALID_FLASH

    TURN_ON_SCHEMA: typing.Final = _LIGHT_TURN_ON_SCHEMA
    TURN_OFF_SCHEMA: typing.Final = _LIGHT_TURN_OFF_SCHEMA

    COLOR_MODES_BRIGHTNESS: typing.Final = _COLOR_MODES_BRIGHTNESS
    COLOR_MODES_COLOR: typing.Final = _COLOR_MODES_COLOR

    VALID_COLOR_MODES: typing.Final = _VALID_COLOR_MODES

    @staticmethod
    def valid_supported_color_modes(
        color_modes: typing.Iterable[ColorMode | str],
    ) -> set[ColorMode | str]:
        """Validate the given color modes."""
        color_modes = set(color_modes)
        if (
            not color_modes
            or _ColorMode.UNKNOWN in color_modes
            or (_ColorMode.BRIGHTNESS in color_modes and len(color_modes) > 1)
            or (_ColorMode.ONOFF in color_modes and len(color_modes) > 1)
            or (
                _ColorMode.WHITE in color_modes
                and not Light.color_supported(color_modes)
            )
        ):
            raise vol.Error(f"Invalid supported_color_modes {sorted(color_modes)}")
        return color_modes

    @staticmethod
    def brightness_supported(color_modes: typing.Iterable[ColorMode | str]) -> bool:
        """Test if brightness is supported."""
        if not color_modes:
            return False
        return any(mode in _COLOR_MODES_BRIGHTNESS for mode in color_modes)

    @staticmethod
    def color_supported(color_modes: typing.Iterable[ColorMode | str]) -> bool:
        """Test if color is supported."""
        if not color_modes:
            return False
        return any(mode in _COLOR_MODES_COLOR for mode in color_modes)

    @staticmethod
    def color_temp_supported(color_modes: typing.Iterable[ColorMode | str]) -> bool:
        """Test if color temperature is supported."""
        if not color_modes:
            return False
        return _ColorMode.COLOR_TEMP in color_modes

    @staticmethod
    def get_supported_color_modes(shc: SmartHomeController, entity_id: str) -> set:
        """Get supported color modes for a light entity.

        First try the statemachine, then entity registry.
        This is the equivalent of entity helper get_supported_features.
        """
        if state := shc.states.get(entity_id):
            return state.attributes.get(_ATTR_SUPPORTED_COLOR_MODES)

        entity_registry = shc.entity_registry
        if not (entry := entity_registry.async_get(entity_id)):
            raise SmartHomeControllerError(f"Unknown entity {entity_id}")
        if not entry.capabilities:
            return None

        return entry.capabilities.get(_ATTR_SUPPORTED_COLOR_MODES)

    @staticmethod
    def filter_turn_off_params(light, params):
        """Filter out params not used in turn off or not supported by the light."""
        supported_features = light.supported_features

        if not supported_features & _EntityFeature.FLASH:
            params.pop(_ATTR_FLASH, None)
        if not supported_features & _EntityFeature.TRANSITION:
            params.pop(_ATTR_TRANSITION, None)

        return {k: v for k, v in params.items() if k in (_ATTR_TRANSITION, _ATTR_FLASH)}

    @staticmethod
    def filter_turn_on_params(light, params):
        """Filter out params not supported by the light."""
        supported_features = light.supported_features

        if not supported_features & _EntityFeature.EFFECT:
            params.pop(_ATTR_EFFECT, None)
        if not supported_features & _EntityFeature.FLASH:
            params.pop(_ATTR_FLASH, None)
        if not supported_features & _EntityFeature.TRANSITION:
            params.pop(_ATTR_TRANSITION, None)

        supported_color_modes = (
            light._light_internal_supported_color_modes  # pylint:disable=protected-access
        )
        if not Light.brightness_supported(supported_color_modes):
            params.pop(_ATTR_BRIGHTNESS, None)
        if _ColorMode.COLOR_TEMP not in supported_color_modes:
            params.pop(_ATTR_COLOR_TEMP, None)
        if _ColorMode.HS not in supported_color_modes:
            params.pop(_ATTR_HS_COLOR, None)
        if _ColorMode.RGB not in supported_color_modes:
            params.pop(_ATTR_RGB_COLOR, None)
        if _ColorMode.RGBW not in supported_color_modes:
            params.pop(_ATTR_RGBW_COLOR, None)
        if _ColorMode.RGBWW not in supported_color_modes:
            params.pop(_ATTR_RGBWW_COLOR, None)
        if _ColorMode.WHITE not in supported_color_modes:
            params.pop(_ATTR_WHITE, None)
        if _ColorMode.XY not in supported_color_modes:
            params.pop(_ATTR_XY_COLOR, None)

        return params

    @staticmethod
    def preprocess_turn_on_alternatives(params):
        """Process extra data for turn light on request.

        Async friendly.
        """
        # Bail out, we process this later.
        if _ATTR_BRIGHTNESS_STEP in params or _ATTR_BRIGHTNESS_STEP_PCT in params:
            return

        if _ATTR_PROFILE in params:
            _PROFILES.apply_profile(params.pop(_ATTR_PROFILE), params)

        if (color_name := params.pop(_ATTR_COLOR_NAME, None)) is not None:
            try:
                params[_ATTR_RGB_COLOR] = Color.name_to_rgb(color_name)
            except ValueError:
                _LOGGER.warning(
                    f"Got unknown color {color_name}, falling back to white"
                )
                params[_ATTR_RGB_COLOR] = (255, 255, 255)

        if (kelvin := params.pop(_ATTR_KELVIN, None)) is not None:
            mired = Color.temperature_kelvin_to_mired(kelvin)
            params[_ATTR_COLOR_TEMP] = int(mired)

        brightness_pct = params.pop(_ATTR_BRIGHTNESS_PCT, None)
        if brightness_pct is not None:
            params[_ATTR_BRIGHTNESS] = round(255 * brightness_pct / 100)

    @staticmethod
    def filter_supported_color_modes(
        color_modes: typing.Iterable[ColorMode],
    ) -> set[ColorMode]:
        """Filter the given color modes."""
        color_modes = set(color_modes)
        if (
            not color_modes
            or _ColorMode.UNKNOWN in color_modes
            or (
                _ColorMode.WHITE in color_modes
                and not Light.color_supported(color_modes)
            )
        ):
            raise SmartHomeControllerError

        if _ColorMode.ONOFF in color_modes and len(color_modes) > 1:
            color_modes.remove(_ColorMode.ONOFF)
        if _ColorMode.BRIGHTNESS in color_modes and len(color_modes) > 1:
            color_modes.remove(_ColorMode.BRIGHTNESS)
        return color_modes
