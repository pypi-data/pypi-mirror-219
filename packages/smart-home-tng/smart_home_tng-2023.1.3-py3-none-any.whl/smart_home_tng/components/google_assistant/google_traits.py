"""
Google Assistant Integration  for Smart Home - The Next Generation.

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

import enum
import logging
import typing

from ...backports import strenum
from ... import core
from .google_errors import SmartHomeError, ChallengeNeeded

_acp: typing.TypeAlias = core.AlarmControlPanel
_binary_sensor: typing.TypeAlias = core.BinarySensor
_button: typing.TypeAlias = core.Button
_camera: typing.TypeAlias = core.Camera
_const: typing.TypeAlias = core.Const
_cover: typing.TypeAlias = core.Cover
_climate: typing.TypeAlias = core.Climate
_fan: typing.TypeAlias = core.Fan
_humidifier: typing.TypeAlias = core.Humidifier
_light: typing.TypeAlias = core.Light
_media_player: typing.TypeAlias = core.MediaPlayer
_sensor: typing.TypeAlias = core.Sensor
_vacuum: typing.TypeAlias = core.Vacuum
_color: typing.TypeAlias = core.helpers.Color
_google: typing.TypeAlias = core.GoogleAssistant
_helpers: typing.TypeAlias = core.helpers

_LOGGER: typing.Final = logging.getLogger(__name__)

# pylint: disable=unused-variable

PREFIX_TRAITS: typing.Final = "action.devices.traits."
TRAIT_CAMERA_STREAM: typing.Final = f"{PREFIX_TRAITS}CameraStream"
TRAIT_ONOFF: typing.Final = f"{PREFIX_TRAITS}OnOff"
TRAIT_DOCK: typing.Final = f"{PREFIX_TRAITS}Dock"
TRAIT_STARTSTOP: typing.Final = f"{PREFIX_TRAITS}StartStop"
TRAIT_BRIGHTNESS: typing.Final = f"{PREFIX_TRAITS}Brightness"
TRAIT_COLOR_SETTING: typing.Final = f"{PREFIX_TRAITS}ColorSetting"
TRAIT_SCENE: typing.Final = f"{PREFIX_TRAITS}Scene"
TRAIT_TEMPERATURE_SETTING: typing.Final = f"{PREFIX_TRAITS}TemperatureSetting"
TRAIT_TEMPERATURE_CONTROL: typing.Final = f"{PREFIX_TRAITS}TemperatureControl"
TRAIT_LOCKUNLOCK: typing.Final = f"{PREFIX_TRAITS}LockUnlock"
TRAIT_FANSPEED: typing.Final = f"{PREFIX_TRAITS}FanSpeed"
TRAIT_MODES: typing.Final = f"{PREFIX_TRAITS}Modes"
TRAIT_INPUTSELECTOR: typing.Final = f"{PREFIX_TRAITS}InputSelector"
TRAIT_OPENCLOSE: typing.Final = f"{PREFIX_TRAITS}OpenClose"
TRAIT_VOLUME: typing.Final = f"{PREFIX_TRAITS}Volume"
TRAIT_ARMDISARM: typing.Final = f"{PREFIX_TRAITS}ArmDisarm"
TRAIT_HUMIDITY_SETTING: typing.Final = f"{PREFIX_TRAITS}HumiditySetting"
TRAIT_TRANSPORT_CONTROL: typing.Final = f"{PREFIX_TRAITS}TransportControl"
TRAIT_MEDIA_STATE: typing.Final = f"{PREFIX_TRAITS}MediaState"
TRAIT_CHANNEL: typing.Final = f"{PREFIX_TRAITS}Channel"
TRAIT_LOCATOR: typing.Final = f"{PREFIX_TRAITS}Locator"
TRAIT_ENERGYSTORAGE: typing.Final = f"{PREFIX_TRAITS}EnergyStorage"
TRAIT_SENSOR_STATE: typing.Final = f"{PREFIX_TRAITS}SensorState"

PREFIX_COMMANDS: typing.Final = "action.devices.commands."
COMMAND_ONOFF: typing.Final = f"{PREFIX_COMMANDS}OnOff"
COMMAND_GET_CAMERA_STREAM: typing.Final = f"{PREFIX_COMMANDS}GetCameraStream"
COMMAND_DOCK: typing.Final = f"{PREFIX_COMMANDS}Dock"
COMMAND_STARTSTOP: typing.Final = f"{PREFIX_COMMANDS}StartStop"
COMMAND_PAUSEUNPAUSE: typing.Final = f"{PREFIX_COMMANDS}PauseUnpause"
COMMAND_BRIGHTNESS_ABSOLUTE: typing.Final = f"{PREFIX_COMMANDS}BrightnessAbsolute"
COMMAND_COLOR_ABSOLUTE: typing.Final = f"{PREFIX_COMMANDS}ColorAbsolute"
COMMAND_ACTIVATE_SCENE: typing.Final = f"{PREFIX_COMMANDS}ActivateScene"
COMMAND_THERMOSTAT_TEMPERATURE_SETPOINT: typing.Final = (
    f"{PREFIX_COMMANDS}ThermostatTemperatureSetpoint"
)
COMMAND_THERMOSTAT_TEMPERATURE_SET_RANGE: typing.Final = (
    f"{PREFIX_COMMANDS}ThermostatTemperatureSetRange"
)
COMMAND_THERMOSTAT_SET_MODE: typing.Final = f"{PREFIX_COMMANDS}ThermostatSetMode"
COMMAND_LOCKUNLOCK: typing.Final = f"{PREFIX_COMMANDS}LockUnlock"
COMMAND_FANSPEED: typing.Final = f"{PREFIX_COMMANDS}SetFanSpeed"
COMMAND_FANSPEEDRELATIVE: typing.Final = f"{PREFIX_COMMANDS}SetFanSpeedRelative"
COMMAND_MODES: typing.Final = f"{PREFIX_COMMANDS}SetModes"
COMMAND_INPUT: typing.Final = f"{PREFIX_COMMANDS}SetInput"
COMMAND_NEXT_INPUT: typing.Final = f"{PREFIX_COMMANDS}NextInput"
COMMAND_PREVIOUS_INPUT: typing.Final = f"{PREFIX_COMMANDS}PreviousInput"
COMMAND_OPENCLOSE: typing.Final = f"{PREFIX_COMMANDS}OpenClose"
COMMAND_OPENCLOSE_RELATIVE: typing.Final = f"{PREFIX_COMMANDS}OpenCloseRelative"
COMMAND_SET_VOLUME: typing.Final = f"{PREFIX_COMMANDS}setVolume"
COMMAND_VOLUME_RELATIVE: typing.Final = f"{PREFIX_COMMANDS}volumeRelative"
COMMAND_MUTE: typing.Final = f"{PREFIX_COMMANDS}mute"
COMMAND_ARMDISARM: typing.Final = f"{PREFIX_COMMANDS}ArmDisarm"
COMMAND_MEDIA_NEXT: typing.Final = f"{PREFIX_COMMANDS}mediaNext"
COMMAND_MEDIA_PAUSE: typing.Final = f"{PREFIX_COMMANDS}mediaPause"
COMMAND_MEDIA_PREVIOUS: typing.Final = f"{PREFIX_COMMANDS}mediaPrevious"
COMMAND_MEDIA_RESUME: typing.Final = f"{PREFIX_COMMANDS}mediaResume"
COMMAND_MEDIA_SEEK_RELATIVE: typing.Final = f"{PREFIX_COMMANDS}mediaSeekRelative"
COMMAND_MEDIA_SEEK_TO_POSITION: typing.Final = f"{PREFIX_COMMANDS}mediaSeekToPosition"
COMMAND_MEDIA_SHUFFLE: typing.Final = f"{PREFIX_COMMANDS}mediaShuffle"
COMMAND_MEDIA_STOP: typing.Final = f"{PREFIX_COMMANDS}mediaStop"
COMMAND_REVERSE: typing.Final = f"{PREFIX_COMMANDS}Reverse"
COMMAND_SET_HUMIDITY: typing.Final = f"{PREFIX_COMMANDS}SetHumidity"
COMMAND_SELECT_CHANNEL: typing.Final = f"{PREFIX_COMMANDS}selectChannel"
COMMAND_LOCATE: typing.Final = f"{PREFIX_COMMANDS}Locate"
COMMAND_CHARGE: typing.Final = f"{PREFIX_COMMANDS}Charge"

TRAITS: typing.Final = []

FAN_SPEED_MAX_SPEED_COUNT: typing.Final = 5


class _EntityDomain(strenum.LowercaseStrEnum):
    """supported Smart Home - TNG entity domains"""

    # pylint: disable=invalid-name
    ALARM_CONTROL_PANEL = enum.auto()
    BINARY_SENSOR = enum.auto()
    BUTTON = enum.auto()
    CAMERA = enum.auto()
    CLIMATE = enum.auto()
    COVER = enum.auto()
    FAN = enum.auto()
    GROUP = enum.auto()
    HUMIDIFIER = enum.auto()
    INPUT_BOOLEAN = enum.auto()
    INPUT_BUTTON = enum.auto()
    INPUT_SELECT = enum.auto()
    LIGHT = enum.auto()
    LOCK = enum.auto()
    MEDIA_PLAYER = enum.auto()
    SCENE = enum.auto()
    SELECT = enum.auto()
    SENSOR = enum.auto()
    SCRIPT = enum.auto()
    SWITCH = enum.auto()
    VACUUM = enum.auto()


def _register_trait(trait):
    """Decorate a function to register a trait."""
    TRAITS.append(trait)
    return trait


def _google_temp_unit(units):
    """Return Google temperature unit."""
    if units == _const.UnitOfTemperature.FAHRENHEIT:
        return "F"
    return "C"


def _next_selected(items: list[str], selected: str) -> str:
    """Return the next item in a item list starting at given value.

    If selected is missing in items, None is returned
    """
    if selected is None:
        return None
    try:
        index = items.index(selected)
    except ValueError:
        return None

    next_item = 0 if index == len(items) - 1 else index + 1
    return items[next_item]


# pylint: disable=unused-argument
class _Trait:
    """Represents a Trait inside Google Assistant skill."""

    _commands: list[str] = []
    _name: str = None

    @staticmethod
    def might_2fa(domain, features, device_class):
        """Return if the trait might ask for 2FA."""
        return False

    def __init__(self, state: core.State, config: _google.AbstractConfig):
        """Initialize a trait for a state."""
        self._state = state
        self._config = config

    @property
    def name(self) -> str:
        return self._name

    @property
    def commands(self) -> list[str]:
        return self._commands

    @property
    def controller(self):
        return self._config.controller

    def sync_attributes(self):
        """Return attributes for a sync request."""
        raise NotImplementedError

    def query_attributes(self):
        """Return the attributes of this trait for this entity."""
        raise NotImplementedError

    def can_execute(self, command, params):
        """Test if command can be executed."""
        return command in self.commands

    async def execute(self, command, data, params, challenge):
        """Execute a trait command."""
        raise NotImplementedError


@_register_trait
class BrightnessTrait(_Trait):
    """Trait to control brightness of a device.

    https://developers.google.com/actions/smarthome/traits/brightness
    """

    _name = TRAIT_BRIGHTNESS
    _commands = [COMMAND_BRIGHTNESS_ABSOLUTE]

    @staticmethod
    def supported(domain, features, device_class, attributes):
        """Test if state is supported."""
        if domain == _EntityDomain.LIGHT:
            color_modes = attributes.get(_light.ATTR_SUPPORTED_COLOR_MODES)
            return _light.brightness_supported(color_modes)

        return False

    def sync_attributes(self):
        """Return brightness attributes for a sync request."""
        return {}

    def query_attributes(self):
        """Return brightness query attributes."""
        domain = self._state.domain
        response = {}

        if domain == _EntityDomain.LIGHT:
            brightness = self._state.attributes.get(_light.ATTR_BRIGHTNESS)
            if brightness is not None:
                response["brightness"] = round(100 * (brightness / 255))
            else:
                response["brightness"] = 0

        return response

    async def execute(self, command, data, params, challenge):
        """Execute a brightness command."""
        if self._state.domain == _EntityDomain.LIGHT:
            await self.controller.services.async_call(
                str(_EntityDomain.LIGHT),
                _const.SERVICE_TURN_ON,
                {
                    _const.ATTR_ENTITY_ID: self._state.entity_id,
                    _light.ATTR_BRIGHTNESS_PCT: params["brightness"],
                },
                blocking=not self._config.should_report_state,
                context=data.context,
            )


@_register_trait
class CameraStreamTrait(_Trait):
    """Trait to stream from cameras.

    https://developers.google.com/actions/smarthome/traits/camerastream
    """

    _name = TRAIT_CAMERA_STREAM
    _commands = [COMMAND_GET_CAMERA_STREAM]

    stream_info = None

    @staticmethod
    def supported(domain, features, device_class, _):
        """Test if state is supported."""
        if domain == _EntityDomain.CAMERA:
            return features & _camera.EntityFeature.STREAM

        return False

    def sync_attributes(self):
        """Return stream attributes for a sync request."""
        return {
            "cameraStreamSupportedProtocols": ["hls"],
            "cameraStreamNeedAuthToken": False,
            "cameraStreamNeedDrmEncryption": False,
        }

    def query_attributes(self):
        """Return camera stream attributes."""
        return self.stream_info or {}

    async def execute(self, command, data, params, challenge):
        """Execute a get camera stream command."""
        camera: _camera.Component = self.controller.components.camera
        url = await camera.async_request_stream(self._state.entity_id, "hls")
        self.stream_info = {
            "cameraStreamAccessUrl": f"{self.controller.get_url()}{url}",
            "cameraStreamReceiverAppId": _const.CAST_APP_ID_HOMEASSISTANT_MEDIA,
        }


@_register_trait
class OnOffTrait(_Trait):
    """Trait to offer basic on and off functionality.

    https://developers.google.com/actions/smarthome/traits/onoff
    """

    _name = TRAIT_ONOFF
    _commands = [COMMAND_ONOFF]

    @staticmethod
    def supported(domain, features, device_class, _):
        """Test if state is supported."""
        return domain in (
            _EntityDomain.GROUP,
            _EntityDomain.INPUT_BOOLEAN,
            _EntityDomain.SWITCH,
            _EntityDomain.FAN,
            _EntityDomain.LIGHT,
            _EntityDomain.MEDIA_PLAYER,
            _EntityDomain.HUMIDIFIER,
        )

    def sync_attributes(self):
        """Return OnOff attributes for a sync request."""
        if self._state.attributes.get(_const.ATTR_ASSUMED_STATE, False):
            return {"commandOnlyOnOff": True}
        return {}

    def query_attributes(self):
        """Return OnOff query attributes."""
        return {"on": self._state.state not in (_const.STATE_OFF, _const.STATE_UNKNOWN)}

    async def execute(self, command, data, params, challenge):
        """Execute an OnOff command."""
        if (domain := self._state.domain) == _EntityDomain.GROUP:
            service_domain = "homeassistant"
        else:
            service_domain = domain

        service = _const.SERVICE_TURN_ON if params["on"] else _const.SERVICE_TURN_OFF

        await self.controller.services.async_call(
            service_domain,
            service,
            {_const.ATTR_ENTITY_ID: self._state.entity_id},
            blocking=not self._config.should_report_state,
            context=data.context,
        )


@_register_trait
class ColorSettingTrait(_Trait):
    """Trait to offer color temperature functionality.

    https://developers.google.com/actions/smarthome/traits/colortemperature
    """

    _name = TRAIT_COLOR_SETTING
    _commands = [COMMAND_COLOR_ABSOLUTE]

    @staticmethod
    def supported(domain, features, device_class, attributes):
        """Test if state is supported."""
        if domain != _EntityDomain.LIGHT:
            return False

        color_modes = attributes.get(_light.ATTR_SUPPORTED_COLOR_MODES)
        return _light.color_temp_supported(color_modes) or _light.color_supported(
            color_modes
        )

    def sync_attributes(self):
        """Return color temperature attributes for a sync request."""
        attrs = self._state.attributes
        color_modes = attrs.get(_light.ATTR_SUPPORTED_COLOR_MODES)
        response = {}

        if _light.color_supported(color_modes):
            response["colorModel"] = "hsv"

        if _light.color_temp_supported(color_modes):
            # Max Kelvin is Min Mireds K = 1000000 / mireds
            # Min Kelvin is Max Mireds K = 1000000 / mireds
            response["colorTemperatureRange"] = {
                "temperatureMaxK": _color.temperature_mired_to_kelvin(
                    attrs.get(_light.ATTR_MIN_MIREDS)
                ),
                "temperatureMinK": _color.temperature_mired_to_kelvin(
                    attrs.get(_light.ATTR_MAX_MIREDS)
                ),
            }

        return response

    def query_attributes(self):
        """Return color temperature query attributes."""
        color_mode = self._state.attributes.get(_light.ATTR_COLOR_MODE)

        color = {}

        if _light.color_supported([color_mode]):
            color_hs = self._state.attributes.get(_light.ATTR_HS_COLOR)
            brightness = self._state.attributes.get(_light.ATTR_BRIGHTNESS, 1)
            if color_hs is not None:
                color["spectrumHsv"] = {
                    "hue": color_hs[0],
                    "saturation": color_hs[1] / 100,
                    "value": brightness / 255,
                }

        if _light.color_temp_supported([color_mode]):
            temp = self._state.attributes.get(_light.ATTR_COLOR_TEMP)
            # Some faulty integrations might put 0 in here, raising exception.
            if temp == 0:
                _LOGGER.warning(
                    f"Entity {self._state.entity_id} has incorrect color temperature "
                    + f"{temp}",
                )
            elif temp is not None:
                color["temperatureK"] = _color.temperature_mired_to_kelvin(temp)

        response = {}

        if color:
            response["color"] = color

        return response

    async def execute(self, command, data, params, challenge):
        """Execute a color temperature command."""
        if "temperature" in params["color"]:
            temp = _color.temperature_kelvin_to_mired(params["color"]["temperature"])
            min_temp = self._state.attributes[_light.ATTR_MIN_MIREDS]
            max_temp = self._state.attributes[_light.ATTR_MAX_MIREDS]

            if temp < min_temp or temp > max_temp:
                raise SmartHomeError(
                    _google.ERR_VALUE_OUT_OF_RANGE,
                    f"Temperature should be between {min_temp} and {max_temp}",
                )

            await self.controller.services.async_call(
                str(_EntityDomain.LIGHT),
                _const.SERVICE_TURN_ON,
                {
                    _const.ATTR_ENTITY_ID: self._state.entity_id,
                    _light.ATTR_COLOR_TEMP: temp,
                },
                blocking=not self._config.should_report_state,
                context=data.context,
            )

        elif "spectrumRGB" in params["color"]:
            # Convert integer to hex format and left pad with 0's till length 6
            hex_value = f"{params['color']['spectrumRGB']:06x}"
            color = _color.RGB_to_hs(*_color.rgb_hex_to_rgb_list(hex_value))

            await self.controller.services.async_call(
                str(_EntityDomain.LIGHT),
                _const.SERVICE_TURN_ON,
                {
                    _const.ATTR_ENTITY_ID: self._state.entity_id,
                    _light.ATTR_HS_COLOR: color,
                },
                blocking=not self._config.should_report_state,
                context=data.context,
            )

        elif "spectrumHSV" in params["color"]:
            color = params["color"]["spectrumHSV"]
            saturation = color["saturation"] * 100
            brightness = color["value"] * 255

            await self.controller.services.async_call(
                str(_EntityDomain.LIGHT),
                _const.SERVICE_TURN_ON,
                {
                    _const.ATTR_ENTITY_ID: self._state.entity_id,
                    _light.ATTR_HS_COLOR: [color["hue"], saturation],
                    _light.ATTR_BRIGHTNESS: brightness,
                },
                blocking=not self._config.should_report_state,
                context=data.context,
            )


@_register_trait
class SceneTrait(_Trait):
    """Trait to offer scene functionality.

    https://developers.google.com/actions/smarthome/traits/scene
    """

    _name = TRAIT_SCENE
    _commands = [COMMAND_ACTIVATE_SCENE]

    @staticmethod
    def supported(domain, features, device_class, _):
        """Test if state is supported."""
        return domain in (
            _EntityDomain.BUTTON,
            _EntityDomain.INPUT_BUTTON,
            _EntityDomain.SCENE,
            _EntityDomain.SCRIPT,
        )

    def sync_attributes(self):
        """Return scene attributes for a sync request."""
        # None of the supported domains can support sceneReversible
        return {}

    def query_attributes(self):
        """Return scene query attributes."""
        return {}

    async def execute(self, command, data, params, challenge):
        """Execute a scene command."""
        service = _const.SERVICE_TURN_ON
        domain = self._state.domain
        if domain in (_EntityDomain.BUTTON, _EntityDomain.INPUT_BUTTON):
            service = _button.SERVICE_PRESS

        # Don't block for scripts or buttons, as they can be slow.
        await self.controller.services.async_call(
            self._state.domain,
            service,
            {_const.ATTR_ENTITY_ID: self._state.entity_id},
            blocking=(not self._config.should_report_state)
            and domain == _EntityDomain.SCENE,
            context=data.context,
        )


@_register_trait
class DockTrait(_Trait):
    """Trait to offer dock functionality.

    https://developers.google.com/actions/smarthome/traits/dock
    """

    _name = TRAIT_DOCK
    _commands = [COMMAND_DOCK]

    @staticmethod
    def supported(domain, features, device_class, _):
        """Test if state is supported."""
        return domain == _EntityDomain.VACUUM

    def sync_attributes(self):
        """Return dock attributes for a sync request."""
        return {}

    def query_attributes(self):
        """Return dock query attributes."""
        return {"isDocked": self._state.state == _vacuum.STATE_DOCKED}

    async def execute(self, command, data, params, challenge):
        """Execute a dock command."""
        await self.controller.services.async_call(
            self._state.domain,
            _vacuum.SERVICE_RETURN_TO_BASE,
            {_const.ATTR_ENTITY_ID: self._state.entity_id},
            blocking=not self._config.should_report_state,
            context=data.context,
        )


@_register_trait
class LocatorTrait(_Trait):
    """Trait to offer locate functionality.

    https://developers.google.com/actions/smarthome/traits/locator
    """

    _name = TRAIT_LOCATOR
    _commands = [COMMAND_LOCATE]

    @staticmethod
    def supported(domain, features, device_class, _):
        """Test if state is supported."""
        return (
            domain == _EntityDomain.VACUUM and features & _vacuum.EntityFeature.LOCATE
        )

    def sync_attributes(self):
        """Return locator attributes for a sync request."""
        return {}

    def query_attributes(self):
        """Return locator query attributes."""
        return {}

    async def execute(self, command, data, params, challenge):
        """Execute a locate command."""
        if params.get("silence", False):
            raise SmartHomeError(
                _google.ERR_FUNCTION_NOT_SUPPORTED,
                "Silencing a Locate request is not yet supported",
            )

        await self.controller.services.async_call(
            self._state.domain,
            _vacuum.SERVICE_LOCATE,
            {_const.ATTR_ENTITY_ID: self._state.entity_id},
            blocking=not self._config.should_report_state,
            context=data.context,
        )


@_register_trait
class EnergyStorageTrait(_Trait):
    """Trait to offer EnergyStorage functionality.

    https://developers.google.com/actions/smarthome/traits/energystorage
    """

    _name = TRAIT_ENERGYSTORAGE
    _commands = [COMMAND_CHARGE]

    @staticmethod
    def supported(domain, features, device_class, _):
        """Test if state is supported."""
        return (
            domain == _EntityDomain.VACUUM and features & _vacuum.EntityFeature.BATTERY
        )

    def sync_attributes(self):
        """Return EnergyStorage attributes for a sync request."""
        return {
            "isRechargeable": True,
            "queryOnlyEnergyStorage": True,
        }

    def query_attributes(self):
        """Return EnergyStorage query attributes."""
        battery_level = self._state.attributes.get(_const.ATTR_BATTERY_LEVEL)
        if battery_level is None:
            return {}
        if battery_level == 100:
            descriptive_capacity_remaining = "FULL"
        elif 75 <= battery_level < 100:
            descriptive_capacity_remaining = "HIGH"
        elif 50 <= battery_level < 75:
            descriptive_capacity_remaining = "MEDIUM"
        elif 25 <= battery_level < 50:
            descriptive_capacity_remaining = "LOW"
        elif 0 <= battery_level < 25:
            descriptive_capacity_remaining = "CRITICALLY_LOW"
        return {
            "descriptiveCapacityRemaining": descriptive_capacity_remaining,
            "capacityRemaining": [{"rawValue": battery_level, "unit": "PERCENTAGE"}],
            "capacityUntilFull": [
                {"rawValue": 100 - battery_level, "unit": "PERCENTAGE"}
            ],
            "isCharging": self._state.state == _vacuum.STATE_DOCKED,
            "isPluggedIn": self._state.state == _vacuum.STATE_DOCKED,
        }

    async def execute(self, command, data, params, challenge):
        """Execute a dock command."""
        raise SmartHomeError(
            _google.ERR_FUNCTION_NOT_SUPPORTED,
            "Controlling charging of a vacuum is not yet supported",
        )


@_register_trait
class StartStopTrait(_Trait):
    """Trait to offer StartStop functionality.

    https://developers.google.com/actions/smarthome/traits/startstop
    """

    _name = TRAIT_STARTSTOP
    _commands = [COMMAND_STARTSTOP, COMMAND_PAUSEUNPAUSE]

    @staticmethod
    def supported(domain, features, device_class, _):
        """Test if state is supported."""
        if domain == _EntityDomain.VACUUM:
            return True

        if domain == _EntityDomain.COVER and features & _cover.EntityFeature.STOP:
            return True

        return False

    def sync_attributes(self):
        """Return StartStop attributes for a sync request."""
        domain = self._state.domain
        if domain == _EntityDomain.VACUUM:
            return {
                "pausable": self._state.attributes.get(
                    _const.ATTR_SUPPORTED_FEATURES, 0
                )
                & _vacuum.EntityFeature.PAUSE
                != 0
            }
        return {}

    def query_attributes(self):
        """Return StartStop query attributes."""
        domain = self._state.domain
        state = self._state.state

        if domain == _EntityDomain.VACUUM:
            return {
                "isRunning": state == _vacuum.STATE_CLEANING,
                "isPaused": state == _const.STATE_PAUSED,
            }

        return {"isRunning": state in (_cover.STATE_CLOSING, _cover.STATE_OPENING)}

    async def execute(self, command, data, params, challenge):
        """Execute a StartStop command."""
        domain = self._state.domain
        if domain == _EntityDomain.VACUUM:
            return await self._execute_vacuum(command, data, params, challenge)
        return await self._execute_cover(command, data, params, challenge)

    async def _execute_vacuum(self, command, data, params, challenge):
        """Execute a StartStop command."""
        if command == COMMAND_STARTSTOP:
            if params["start"]:
                await self.controller.services.async_call(
                    self._state.domain,
                    _vacuum.SERVICE_START,
                    {_const.ATTR_ENTITY_ID: self._state.entity_id},
                    blocking=not self._config.should_report_state,
                    context=data.context,
                )
            else:
                await self.controller.services.async_call(
                    self._state.domain,
                    _vacuum.SERVICE_STOP,
                    {_const.ATTR_ENTITY_ID: self._state.entity_id},
                    blocking=not self._config.should_report_state,
                    context=data.context,
                )
        elif command == COMMAND_PAUSEUNPAUSE:
            if params["pause"]:
                await self.controller.services.async_call(
                    self._state.domain,
                    _vacuum.SERVICE_PAUSE,
                    {_const.ATTR_ENTITY_ID: self._state.entity_id},
                    blocking=not self._config.should_report_state,
                    context=data.context,
                )
            else:
                await self.controller.services.async_call(
                    self._state.domain,
                    _vacuum.SERVICE_START,
                    {_const.ATTR_ENTITY_ID: self._state.entity_id},
                    blocking=not self._config.should_report_state,
                    context=data.context,
                )

    async def _execute_cover(self, command, data, params, challenge):
        """Execute a StartStop command."""
        if command == COMMAND_STARTSTOP:
            if params["start"] is False:
                if self._state.state in (
                    _cover.STATE_CLOSING,
                    _cover.STATE_OPENING,
                ) or self._state.attributes.get(_const.ATTR_ASSUMED_STATE):
                    await self.controller.services.async_call(
                        self._state.domain,
                        _cover.SERVICE_STOP,
                        {_const.ATTR_ENTITY_ID: self._state.entity_id},
                        blocking=not self._config.should_report_state,
                        context=data.context,
                    )
                else:
                    raise SmartHomeError(
                        _google.ERR_ALREADY_STOPPED,
                        "Cover is already stopped",
                    )
            else:
                raise SmartHomeError(
                    _google.ERR_NOT_SUPPORTED,
                    "Starting a cover is not supported",
                )
        else:
            raise SmartHomeError(
                _google.ERR_NOT_SUPPORTED,
                f"Command {command} is not supported",
            )


@_register_trait
class TemperatureControlTrait(_Trait):
    """
    Trait for devices (other than thermostats) that support controlling temperature.
    Workaround for Temperature sensors.

    https://developers.google.com/assistant/smarthome/traits/temperaturecontrol
    """

    _name = TRAIT_TEMPERATURE_CONTROL

    @staticmethod
    def supported(domain, features, device_class, _):
        """Test if state is supported."""
        return (
            domain == _EntityDomain.SENSOR
            and device_class == _sensor.DeviceClass.TEMPERATURE
        )

    def sync_attributes(self):
        """Return temperature attributes for a sync request."""
        return {
            "temperatureUnitForUX": _google_temp_unit(
                self.controller.config.units.temperature_unit
            ),
            "queryOnlyTemperatureSetting": True,
            "temperatureRange": {
                "minThresholdCelsius": -100,
                "maxThresholdCelsius": 100,
            },
        }

    def query_attributes(self):
        """Return temperature states."""
        response = {}
        unit = self.controller.config.units.temperature_unit
        current_temp = self._state.state
        if current_temp not in (_const.STATE_UNKNOWN, _const.STATE_UNAVAILABLE):
            temp = round(
                core.TemperatureConverter.convert(
                    float(current_temp), unit, _const.UnitOfTemperature.CELSIUS
                ),
                1,
            )
            response["temperatureSetpointCelsius"] = temp
            response["temperatureAmbientCelsius"] = temp

        return response

    async def execute(self, command, data, params, challenge):
        """Unsupported."""
        raise SmartHomeError(
            _google.ERR_NOT_SUPPORTED, "Execute is not supported by sensor"
        )


@_register_trait
class TemperatureSettingTrait(_Trait):
    """Trait to offer handling both temperature point and modes functionality.

    https://developers.google.com/actions/smarthome/traits/temperaturesetting
    """

    _name = TRAIT_TEMPERATURE_SETTING
    _commands = [
        COMMAND_THERMOSTAT_TEMPERATURE_SETPOINT,
        COMMAND_THERMOSTAT_TEMPERATURE_SET_RANGE,
        COMMAND_THERMOSTAT_SET_MODE,
    ]
    # We do not support "on" as we are unable to know how to restore
    # the last mode.
    hvac_to_google = {
        _climate.HVACMode.HEAT: "heat",
        _climate.HVACMode.COOL: "cool",
        _climate.HVACMode.OFF: "off",
        _climate.HVACMode.AUTO: "auto",
        _climate.HVACMode.HEAT_COOL: "heatcool",
        _climate.HVACMode.FAN_ONLY: "fan-only",
        _climate.HVACMode.DRY: "dry",
    }
    google_to_hvac = {value: key for key, value in hvac_to_google.items()}

    preset_to_google = {_climate.PRESET_ECO: "eco"}
    google_to_preset = {value: key for key, value in preset_to_google.items()}

    @staticmethod
    def supported(domain, features, device_class, _):
        """Test if state is supported."""
        return domain == _EntityDomain.CLIMATE

    @property
    def climate_google_modes(self):
        """Return supported Google modes."""
        modes = []
        attrs = self._state.attributes

        for mode in attrs.get(_climate.ATTR_HVAC_MODES, []):
            google_mode = self.hvac_to_google.get(mode)
            if google_mode and google_mode not in modes:
                modes.append(google_mode)

        for preset in attrs.get(core.Climate.ATTR_PRESET_MODES, []):
            google_mode = self.preset_to_google.get(preset)
            if google_mode and google_mode not in modes:
                modes.append(google_mode)

        return modes

    def sync_attributes(self):
        """Return temperature point and modes attributes for a sync request."""
        response = {}
        response["thermostatTemperatureUnit"] = _google_temp_unit(
            self.controller.config.units.temperature_unit
        )

        modes = self.climate_google_modes

        # Some integrations don't support modes (e.g. opentherm), but Google doesn't
        # support changing the temperature if we don't have any modes. If there's
        # only one Google doesn't support changing it, so the default mode here is
        # only cosmetic.
        if len(modes) == 0:
            modes.append("heat")

        if "off" in modes and any(
            mode in modes for mode in ("heatcool", "heat", "cool")
        ):
            modes.append("on")
        response["availableThermostatModes"] = modes

        return response

    def query_attributes(self):
        """Return temperature point and modes query attributes."""
        response = {}
        attrs = self._state.attributes
        unit = self.controller.config.units.temperature_unit

        operation = self._state.state
        preset = attrs.get(_climate.ATTR_PRESET_MODE)
        supported = attrs.get(_const.ATTR_SUPPORTED_FEATURES, 0)

        if preset in self.preset_to_google:
            response["thermostatMode"] = self.preset_to_google[preset]
        else:
            response["thermostatMode"] = self.hvac_to_google.get(operation, "none")

        current_temp = attrs.get(_climate.ATTR_CURRENT_TEMPERATURE)
        if current_temp is not None:
            response["thermostatTemperatureAmbient"] = round(
                core.TemperatureConverter.convert(
                    current_temp, unit, _const.UnitOfTemperature.CELSIUS
                ),
                1,
            )

        current_humidity = attrs.get(_climate.ATTR_CURRENT_HUMIDITY)
        if current_humidity is not None:
            response["thermostatHumidityAmbient"] = current_humidity

        if operation in (_climate.HVACMode.AUTO, _climate.HVACMode.HEAT_COOL):
            if supported & _climate.EntityFeature.TARGET_TEMPERATURE_RANGE:
                response["thermostatTemperatureSetpointHigh"] = round(
                    core.TemperatureConverter.convert(
                        attrs[_climate.ATTR_TARGET_TEMP_HIGH],
                        unit,
                        _const.UnitOfTemperature.CELSIUS,
                    ),
                    1,
                )
                response["thermostatTemperatureSetpointLow"] = round(
                    core.TemperatureConverter.convert(
                        attrs[_climate.ATTR_TARGET_TEMP_LOW],
                        unit,
                        _const.UnitOfTemperature.CELSIUS,
                    ),
                    1,
                )
            else:
                if (target_temp := attrs.get(_const.ATTR_TEMPERATURE)) is not None:
                    target_temp = round(
                        core.TemperatureConverter.convert(
                            target_temp, unit, _const.UnitOfTemperature.CELSIUS
                        ),
                        1,
                    )
                    response["thermostatTemperatureSetpointHigh"] = target_temp
                    response["thermostatTemperatureSetpointLow"] = target_temp
        else:
            if (target_temp := attrs.get(_const.ATTR_TEMPERATURE)) is not None:
                response["thermostatTemperatureSetpoint"] = round(
                    core.TemperatureConverter.convert(
                        target_temp, unit, _const.UnitOfTemperature.CELSIUS
                    ),
                    1,
                )

        return response

    async def execute(self, command, data, params, challenge):
        """Execute a temperature point or mode command."""
        # All sent in temperatures are always in Celsius
        unit = self.controller.config.units.temperature_unit
        min_temp = self._state.attributes[_climate.ATTR_MIN_TEMP]
        max_temp = self._state.attributes[_climate.ATTR_MAX_TEMP]

        if command == COMMAND_THERMOSTAT_TEMPERATURE_SETPOINT:
            temp = core.TemperatureConverter.convert(
                params["thermostatTemperatureSetpoint"],
                _const.UnitOfTemperature.CELSIUS,
                unit,
            )
            if unit == _const.UnitOfTemperature.FAHRENHEIT:
                temp = round(temp)

            if temp < min_temp or temp > max_temp:
                raise SmartHomeError(
                    _google.ERR_VALUE_OUT_OF_RANGE,
                    f"Temperature should be between {min_temp} and {max_temp}",
                )

            await self.controller.services.async_call(
                str(_EntityDomain.CLIMATE),
                _climate.SERVICE_SET_TEMPERATURE,
                {
                    _const.ATTR_ENTITY_ID: self._state.entity_id,
                    _const.ATTR_TEMPERATURE: temp,
                },
                blocking=not self._config.should_report_state,
                context=data.context,
            )

        elif command == COMMAND_THERMOSTAT_TEMPERATURE_SET_RANGE:
            temp_high = core.TemperatureConverter.convert(
                params["thermostatTemperatureSetpointHigh"],
                _const.UnitOfTemperature.CELSIUS,
                unit,
            )
            if unit == _const.UnitOfTemperature.FAHRENHEIT:
                temp_high = round(temp_high)

            if temp_high < min_temp or temp_high > max_temp:
                raise SmartHomeError(
                    _google.ERR_VALUE_OUT_OF_RANGE,
                    (
                        f"Upper bound for temperature range should be between "
                        f"{min_temp} and {max_temp}"
                    ),
                )

            temp_low = core.TemperatureConverter.convert(
                params["thermostatTemperatureSetpointLow"],
                _const.UnitOfTemperature.CELSIUS,
                unit,
            )
            if unit == _const.UnitOfTemperature.FAHRENHEIT:
                temp_low = round(temp_low)

            if temp_low < min_temp or temp_low > max_temp:
                raise SmartHomeError(
                    _google.ERR_VALUE_OUT_OF_RANGE,
                    (
                        f"Lower bound for temperature range should be between "
                        f"{min_temp} and {max_temp}"
                    ),
                )

            supported = self._state.attributes.get(_const.ATTR_SUPPORTED_FEATURES)
            svc_data = {_const.ATTR_ENTITY_ID: self._state.entity_id}

            if supported & _climate.EntityFeature.TARGET_TEMPERATURE_RANGE:
                svc_data[_climate.ATTR_TARGET_TEMP_HIGH] = temp_high
                svc_data[_climate.ATTR_TARGET_TEMP_LOW] = temp_low
            else:
                svc_data[_const.ATTR_TEMPERATURE] = (temp_high + temp_low) / 2

            await self.controller.services.async_call(
                str(_EntityDomain.CLIMATE),
                _climate.SERVICE_SET_TEMPERATURE,
                svc_data,
                blocking=not self._config.should_report_state,
                context=data.context,
            )

        elif command == COMMAND_THERMOSTAT_SET_MODE:
            target_mode = params["thermostatMode"]
            supported = self._state.attributes.get(_const.ATTR_SUPPORTED_FEATURES)

            if target_mode == "on":
                await self.controller.services.async_call(
                    str(_EntityDomain.CLIMATE),
                    _const.SERVICE_TURN_ON,
                    {_const.ATTR_ENTITY_ID: self._state.entity_id},
                    blocking=not self._config.should_report_state,
                    context=data.context,
                )
                return

            if target_mode == "off":
                await self.controller.services.async_call(
                    str(_EntityDomain.CLIMATE),
                    _const.SERVICE_TURN_OFF,
                    {_const.ATTR_ENTITY_ID: self._state.entity_id},
                    blocking=not self._config.should_report_state,
                    context=data.context,
                )
                return

            if target_mode in self.google_to_preset:
                await self.controller.services.async_call(
                    str(_EntityDomain.CLIMATE),
                    _climate.SERVICE_SET_PRESET_MODE,
                    {
                        _climate.ATTR_PRESET_MODE: self.google_to_preset[target_mode],
                        _const.ATTR_ENTITY_ID: self._state.entity_id,
                    },
                    blocking=not self._config.should_report_state,
                    context=data.context,
                )
                return

            await self.controller.services.async_call(
                str(_EntityDomain.CLIMATE),
                _climate.SERVICE_SET_HVAC_MODE,
                {
                    _const.ATTR_ENTITY_ID: self._state.entity_id,
                    _climate.ATTR_HVAC_MODE: self.google_to_hvac[target_mode],
                },
                blocking=not self._config.should_report_state,
                context=data.context,
            )


@_register_trait
class HumiditySettingTrait(_Trait):
    """Trait to offer humidity setting functionality.

    https://developers.google.com/actions/smarthome/traits/humiditysetting
    """

    _name = TRAIT_HUMIDITY_SETTING
    _commands = [COMMAND_SET_HUMIDITY]

    @staticmethod
    def supported(domain, features, device_class, _):
        """Test if state is supported."""
        if domain == _EntityDomain.HUMIDIFIER:
            return True

        return (
            domain == _EntityDomain.SENSOR
            and device_class == _sensor.DeviceClass.HUMIDITY
        )

    def sync_attributes(self):
        """Return humidity attributes for a sync request."""
        response = {}
        attrs = self._state.attributes
        domain = self._state.domain

        if domain == _EntityDomain.SENSOR:
            device_class = attrs.get(_const.ATTR_DEVICE_CLASS)
            if device_class == _sensor.DeviceClass.HUMIDITY:
                response["queryOnlyHumiditySetting"] = True

        elif domain == _EntityDomain.HUMIDIFIER:
            response["humiditySetpointRange"] = {
                "minPercent": round(
                    float(self._state.attributes[_humidifier.ATTR_MIN_HUMIDITY])
                ),
                "maxPercent": round(
                    float(self._state.attributes[_humidifier.ATTR_MAX_HUMIDITY])
                ),
            }

        return response

    def query_attributes(self):
        """Return humidity query attributes."""
        response = {}
        attrs = self._state.attributes
        domain = self._state.domain

        if domain == _EntityDomain.SENSOR:
            device_class = attrs.get(_const.ATTR_DEVICE_CLASS)
            if device_class == _sensor.DeviceClass.HUMIDITY:
                current_humidity = self._state.state
                if current_humidity not in (
                    _const.STATE_UNKNOWN,
                    _const.STATE_UNAVAILABLE,
                ):
                    response["humidityAmbientPercent"] = round(float(current_humidity))

        elif domain == _EntityDomain.HUMIDIFIER:
            target_humidity = attrs.get(_humidifier.ATTR_HUMIDITY)
            if target_humidity is not None:
                response["humiditySetpointPercent"] = round(float(target_humidity))

        return response

    async def execute(self, command, data, params, challenge):
        """Execute a humidity command."""
        if self._state.domain == _EntityDomain.SENSOR:
            raise SmartHomeError(
                _google.ERR_NOT_SUPPORTED, "Execute is not supported by sensor"
            )

        if command == COMMAND_SET_HUMIDITY:
            await self.controller.services.async_call(
                str(_EntityDomain.HUMIDIFIER),
                _humidifier.SERVICE_SET_HUMIDITY,
                {
                    _const.ATTR_ENTITY_ID: self._state.entity_id,
                    _humidifier.ATTR_HUMIDITY: params["humidity"],
                },
                blocking=not self._config.should_report_state,
                context=data.context,
            )


@_register_trait
class LockUnlockTrait(_Trait):
    """Trait to lock or unlock a lock.

    https://developers.google.com/actions/smarthome/traits/lockunlock
    """

    _name = TRAIT_LOCKUNLOCK
    _commands = [COMMAND_LOCKUNLOCK]

    @staticmethod
    def supported(domain, features, device_class, _):
        """Test if state is supported."""
        return domain == _EntityDomain.LOCK

    @staticmethod
    def might_2fa(domain, features, device_class):
        """Return if the trait might ask for 2FA."""
        return True

    def sync_attributes(self):
        """Return LockUnlock attributes for a sync request."""
        return {}

    def query_attributes(self):
        """Return LockUnlock query attributes."""
        if self._state.state == _const.STATE_JAMMED:
            return {"isJammed": True}

        # If its unlocking its not yet unlocked so we consider is locked
        return {
            "isLocked": self._state.state
            in (_const.STATE_UNLOCKING, _const.STATE_LOCKED)
        }

    async def execute(self, command, data, params, challenge):
        """Execute an LockUnlock command."""
        if params["lock"]:
            service = _const.SERVICE_LOCK
        else:
            _verify_pin_challenge(data, self._state, challenge)
            service = _const.SERVICE_UNLOCK

        await self.controller.services.async_call(
            str(_EntityDomain.LOCK),
            service,
            {_const.ATTR_ENTITY_ID: self._state.entity_id},
            blocking=not self._config.should_report_state,
            context=data.context,
        )


@_register_trait
class ArmDisArmTrait(_Trait):
    """Trait to Arm or Disarm a Security System.

    https://developers.google.com/actions/smarthome/traits/armdisarm
    """

    _name = TRAIT_ARMDISARM
    _commands = [COMMAND_ARMDISARM]

    state_to_service = {
        _const.STATE_ALARM_ARMED_HOME: _const.SERVICE_ALARM_ARM_HOME,
        _const.STATE_ALARM_ARMED_AWAY: _const.SERVICE_ALARM_ARM_AWAY,
        _const.STATE_ALARM_ARMED_NIGHT: _const.SERVICE_ALARM_ARM_NIGHT,
        _const.STATE_ALARM_ARMED_CUSTOM_BYPASS: _const.SERVICE_ALARM_ARM_CUSTOM_BYPASS,
        _const.STATE_ALARM_TRIGGERED: _const.SERVICE_ALARM_TRIGGER,
    }

    state_to_support = {
        _const.STATE_ALARM_ARMED_HOME: _acp.EntityFeature.ARM_HOME,
        _const.STATE_ALARM_ARMED_AWAY: _acp.EntityFeature.ARM_AWAY,
        _const.STATE_ALARM_ARMED_NIGHT: _acp.EntityFeature.ARM_NIGHT,
        _const.STATE_ALARM_ARMED_CUSTOM_BYPASS: _acp.EntityFeature.ARM_CUSTOM_BYPASS,
        _const.STATE_ALARM_TRIGGERED: _acp.EntityFeature.TRIGGER,
    }

    @staticmethod
    def supported(domain, features, device_class, _):
        """Test if state is supported."""
        return domain == _EntityDomain.ALARM_CONTROL_PANEL

    @staticmethod
    def might_2fa(domain, features, device_class):
        """Return if the trait might ask for 2FA."""
        return True

    def _supported_states(self):
        """Return supported states."""
        features = self._state.attributes.get(_const.ATTR_SUPPORTED_FEATURES, 0)
        return [
            state
            for state, required_feature in self.state_to_support.items()
            if features & required_feature != 0
        ]

    def sync_attributes(self):
        """Return ArmDisarm attributes for a sync request."""
        response = {}
        levels = []
        for state in self._supported_states():
            # level synonyms are generated from state names
            # 'armed_away' becomes 'armed away' or 'away'
            level_synonym = [state.replace("_", " ")]
            if state != _const.STATE_ALARM_TRIGGERED:
                level_synonym.append(state.split("_")[1])

            level = {
                "level_name": state,
                "level_values": [{"level_synonym": level_synonym, "lang": "en"}],
            }
            levels.append(level)

        response["availableArmLevels"] = {"levels": levels, "ordered": False}
        return response

    def query_attributes(self):
        """Return ArmDisarm query attributes."""
        if "next_state" in self._state.attributes:
            armed_state = self._state.attributes["next_state"]
        else:
            armed_state = self._state.state
        response = {"isArmed": armed_state in self.state_to_service}
        if response["isArmed"]:
            response.update({"currentArmLevel": armed_state})
        return response

    async def execute(self, command, data, params, challenge):
        """Execute an ArmDisarm command."""
        if params["arm"] and not params.get("cancel"):
            # If no arm level given, we can only arm it if there is
            # only one supported arm type. We never default to triggered.
            if not (arm_level := params.get("armLevel")):
                states = self._supported_states()

                if _const.STATE_ALARM_TRIGGERED in states:
                    states.remove(_const.STATE_ALARM_TRIGGERED)

                if len(states) != 1:
                    raise SmartHomeError(_google.ERR_NOT_SUPPORTED, "ArmLevel missing")

                arm_level = states[0]

            if self._state.state == arm_level:
                raise SmartHomeError(
                    _google.ERR_ALREADY_ARMED, "System is already armed"
                )
            if self._state.attributes["code_arm_required"]:
                _verify_pin_challenge(data, self._state, challenge)
            service = self.state_to_service[arm_level]
        # disarm the system without asking for code when
        # 'cancel' arming action is received while current status is pending
        elif (
            params["arm"]
            and params.get("cancel")
            and self._state.state == _const.STATE_ALARM_PENDING
        ):
            service = _const.SERVICE_ALARM_DISARM
        else:
            if self._state.state == _const.STATE_ALARM_DISARMED:
                raise SmartHomeError(
                    _google.ERR_ALREADY_DISARMED, "System is already disarmed"
                )
            _verify_pin_challenge(data, self._state, challenge)
            service = _const.SERVICE_ALARM_DISARM

        await self.controller.services.async_call(
            str(_EntityDomain.ALARM_CONTROL_PANEL),
            service,
            {
                _const.ATTR_ENTITY_ID: self._state.entity_id,
                _const.ATTR_CODE: data.config.secure_devices_pin,
            },
            blocking=not self._config.should_report_state,
            context=data.context,
        )


def _get_fan_speed(speed_name: str) -> dict[str, typing.Any]:
    """Return a fan speed synonyms for a speed name."""
    speed_synonyms = _google.FAN_SPEEDS.get(speed_name, [f"{speed_name}"])
    return {
        "speed_name": speed_name,
        "speed_values": [
            {
                "speed_synonym": speed_synonyms,
                "lang": "en",
            }
        ],
    }


@_register_trait
class FanSpeedTrait(_Trait):
    """Trait to control speed of Fan.

    https://developers.google.com/actions/smarthome/traits/fanspeed
    """

    _name = TRAIT_FANSPEED
    _commands = [COMMAND_FANSPEED, COMMAND_REVERSE]

    def __init__(self, state, config):
        """Initialize a trait for a state."""
        super().__init__(state, config)
        if state.domain == _EntityDomain.FAN:
            speed_count = min(
                FAN_SPEED_MAX_SPEED_COUNT,
                round(
                    100 / (self._state.attributes.get(_fan.ATTR_PERCENTAGE_STEP) or 1.0)
                ),
            )
            self._ordered_speed = [
                f"{speed}/{speed_count}" for speed in range(1, speed_count + 1)
            ]

    @staticmethod
    def supported(domain, features, device_class, _):
        """Test if state is supported."""
        if domain == _EntityDomain.FAN:
            return features & _fan.EntityFeature.SET_SPEED
        if domain == _EntityDomain.CLIMATE:
            return features & _climate.EntityFeature.FAN_MODE
        return False

    def sync_attributes(self):
        """Return speed point and modes attributes for a sync request."""
        domain = self._state.domain
        speeds = []
        result = {}

        if domain == _EntityDomain.FAN:
            reversible = bool(
                self._state.attributes.get(_const.ATTR_SUPPORTED_FEATURES, 0)
                & _fan.EntityFeature.DIRECTION
            )

            result.update(
                {
                    "reversible": reversible,
                    "supportsFanSpeedPercent": True,
                }
            )

            if self._ordered_speed:
                result.update(
                    {
                        "availableFanSpeeds": {
                            "speeds": [
                                _get_fan_speed(speed) for speed in self._ordered_speed
                            ],
                            "ordered": True,
                        },
                    }
                )

        elif domain == _EntityDomain.CLIMATE:
            modes = self._state.attributes.get(_climate.ATTR_FAN_MODES) or []
            for mode in modes:
                speed = {
                    "speed_name": mode,
                    "speed_values": [{"speed_synonym": [mode], "lang": "en"}],
                }
                speeds.append(speed)

            result.update(
                {
                    "reversible": False,
                    "availableFanSpeeds": {"speeds": speeds, "ordered": True},
                }
            )

        return result

    def query_attributes(self):
        """Return speed point and modes query attributes."""

        attrs = self._state.attributes
        domain = self._state.domain
        response = {}
        if domain == _EntityDomain.CLIMATE:
            speed = attrs.get(_climate.ATTR_FAN_MODE) or "off"
            response["currentFanSpeedSetting"] = speed

        if domain == _EntityDomain.FAN:
            percent = attrs.get(_fan.ATTR_PERCENTAGE) or 0
            response["currentFanSpeedPercent"] = percent
            response[
                "currentFanSpeedSetting"
            ] = _helpers.percentage_to_ordered_list_item(self._ordered_speed, percent)

        return response

    async def execute_fanspeed(self, data, params):
        """Execute an SetFanSpeed command."""
        domain = self._state.domain
        if domain == _EntityDomain.CLIMATE:
            await self.controller.services.async_call(
                domain,
                _climate.SERVICE_SET_FAN_MODE,
                {
                    _const.ATTR_ENTITY_ID: self._state.entity_id,
                    _climate.ATTR_FAN_MODE: params["fanSpeed"],
                },
                blocking=not self._config.should_report_state,
                context=data.context,
            )

        if domain == _EntityDomain.FAN:
            if fan_speed := params.get("fanSpeed"):
                fan_speed_percent = _helpers.ordered_list_item_to_percentage(
                    self._ordered_speed, fan_speed
                )
            else:
                fan_speed_percent = params.get("fanSpeedPercent")

            await self.controller.services.async_call(
                domain,
                _fan.SERVICE_SET_PERCENTAGE,
                {
                    _const.ATTR_ENTITY_ID: self._state.entity_id,
                    _fan.ATTR_PERCENTAGE: fan_speed_percent,
                },
                blocking=not self._config.should_report_state,
                context=data.context,
            )

    async def execute_reverse(self, data, params):
        """Execute a Reverse command."""
        if domain := self._state.domain == _EntityDomain.FAN:
            if (
                self._state.attributes.get(_fan.ATTR_DIRECTION)
                == _fan.DIRECTION_FORWARD
            ):
                direction = _fan.DIRECTION_REVERSE
            else:
                direction = _fan.DIRECTION_FORWARD

            await self.controller.services.async_call(
                domain,
                _fan.SERVICE_SET_DIRECTION,
                {
                    _const.ATTR_ENTITY_ID: self._state.entity_id,
                    _fan.ATTR_DIRECTION: direction,
                },
                blocking=not self._config.should_report_state,
                context=data.context,
            )

    async def execute(self, command, data, params, challenge):
        """Execute a smart home command."""
        if command == COMMAND_FANSPEED:
            await self.execute_fanspeed(data, params)
        elif command == COMMAND_REVERSE:
            await self.execute_reverse(data, params)


@_register_trait
class ModesTrait(_Trait):
    """Trait to set modes.

    https://developers.google.com/actions/smarthome/traits/modes
    """

    _name = TRAIT_MODES
    _commands = [COMMAND_MODES]

    SYNONYMS: typing.Final = {
        "preset mode": ["preset mode", "mode", "preset"],
        "sound mode": ["sound mode", "effects"],
        "option": ["option", "setting", "mode", "value"],
    }

    @staticmethod
    def supported(domain, features, device_class, _):
        """Test if state is supported."""
        if domain == _EntityDomain.FAN and features & _fan.EntityFeature.PRESET_MODE:
            return True

        if domain == _EntityDomain.INPUT_SELECT:
            return True

        if domain == _EntityDomain.SELECT:
            return True

        if (
            domain == _EntityDomain.HUMIDIFIER
            and features & _humidifier.EntityFeature.MODES
        ):
            return True

        if domain == _EntityDomain.LIGHT and features & _light.EntityFeature.EFFECT:
            return True

        if domain != _EntityDomain.MEDIA_PLAYER:
            return False

        return features & _media_player.EntityFeature.SELECT_SOUND_MODE

    def _generate(self, name, settings):
        """Generate a list of modes."""
        mode = {
            "name": name,
            "name_values": [
                {"name_synonym": self.SYNONYMS.get(name, [name]), "lang": "en"}
            ],
            "settings": [],
            "ordered": False,
        }
        for setting in settings:
            mode["settings"].append(
                {
                    "setting_name": setting,
                    "setting_values": [
                        {
                            "setting_synonym": self.SYNONYMS.get(setting, [setting]),
                            "lang": "en",
                        }
                    ],
                }
            )
        return mode

    def sync_attributes(self):
        """Return mode attributes for a sync request."""
        modes = []

        for domain, attr, name in (
            (str(_EntityDomain.FAN), _fan.ATTR_PRESET_MODES, "preset mode"),
            (
                str(_EntityDomain.MEDIA_PLAYER),
                _media_player.ATTR_SOUND_MODE_LIST,
                "sound mode",
            ),
            (str(_EntityDomain.INPUT_SELECT), core.Select.ATTR_OPTIONS, "option"),
            (str(_EntityDomain.SELECT), core.Select.ATTR_OPTIONS, "option"),
            (str(_EntityDomain.HUMIDIFIER), _humidifier.ATTR_AVAILABLE_MODES, "mode"),
            (str(_EntityDomain.LIGHT), _light.ATTR_EFFECT_LIST, "effect"),
        ):
            if self._state.domain != domain:
                continue

            if (items := self._state.attributes.get(attr)) is not None:
                modes.append(self._generate(name, items))

            # Shortcut since all domains are currently unique
            break

        payload = {"availableModes": modes}

        return payload

    def query_attributes(self):
        """Return current modes."""
        attrs = self._state.attributes
        response = {}
        mode_settings = {}
        domain = self._state.domain

        if domain == _EntityDomain.FAN:
            if _fan.ATTR_PRESET_MODES in attrs:
                mode_settings["preset mode"] = attrs.get(_fan.ATTR_PRESET_MODE)
        elif domain == _EntityDomain.MEDIA_PLAYER:
            if _media_player.ATTR_SOUND_MODE_LIST in attrs:
                mode_settings["sound mode"] = attrs.get(_media_player.ATTR_SOUND_MODE)
        elif domain == _EntityDomain.INPUT_SELECT:
            mode_settings["option"] = self._state.state
        elif domain == _EntityDomain.SELECT:
            mode_settings["option"] = self._state.state
        elif domain == _EntityDomain.HUMIDIFIER:
            if _const.ATTR_MODE in attrs:
                mode_settings["mode"] = attrs.get(_const.ATTR_MODE)
        elif domain == _EntityDomain.LIGHT and _light.ATTR_EFFECT in attrs:
            mode_settings["effect"] = attrs.get(_light.ATTR_EFFECT)

        if mode_settings:
            response["on"] = self._state.state not in (
                _const.STATE_OFF,
                _const.STATE_UNKNOWN,
            )
            response["currentModeSettings"] = mode_settings

        return response

    async def execute(self, command, data, params, challenge):
        """Execute a SetModes command."""
        settings = params.get("updateModeSettings")
        domain = self._state.domain

        if domain == _EntityDomain.FAN:
            preset_mode = settings["preset mode"]
            await self.controller.services.async_call(
                domain,
                _fan.SERVICE_SET_PRESET_MODE,
                {
                    _const.ATTR_ENTITY_ID: self._state.entity_id,
                    _fan.ATTR_PRESET_MODE: preset_mode,
                },
                blocking=not self._config.should_report_state,
                context=data.context,
            )
            return

        if domain == _EntityDomain.INPUT_SELECT:
            option = settings["option"]
            await self.controller.services.async_call(
                domain,
                _const.SERVICE_SELECT_OPTION,
                {
                    _const.ATTR_ENTITY_ID: self._state.entity_id,
                    core.Select.ATTR_OPTION: option,
                },
                blocking=not self._config.should_report_state,
                context=data.context,
            )
            return

        if domain == _EntityDomain.SELECT:
            option = settings["option"]
            await self.controller.services.async_call(
                domain,
                _const.SERVICE_SELECT_OPTION,
                {
                    _const.ATTR_ENTITY_ID: self._state.entity_id,
                    core.Select.ATTR_OPTION: option,
                },
                blocking=not self._config.should_report_state,
                context=data.context,
            )
            return

        if domain == _EntityDomain.HUMIDIFIER:
            requested_mode = settings["mode"]
            await self.controller.services.async_call(
                domain,
                _humidifier.SERVICE_SET_MODE,
                {
                    _const.ATTR_MODE: requested_mode,
                    _const.ATTR_ENTITY_ID: self._state.entity_id,
                },
                blocking=not self._config.should_report_state,
                context=data.context,
            )
            return

        if domain == _EntityDomain.LIGHT:
            requested_effect = settings["effect"]
            await self.controller.services.async_call(
                domain,
                _const.SERVICE_TURN_ON,
                {
                    _const.ATTR_ENTITY_ID: self._state.entity_id,
                    _light.ATTR_EFFECT: requested_effect,
                },
                blocking=not self._config.should_report_state,
                context=data.context,
            )
            return

        if domain == _EntityDomain.MEDIA_PLAYER and (
            sound_mode := settings.get("sound mode")
        ):
            await self.controller.services.async_call(
                domain,
                _media_player.SERVICE_SELECT_SOUND_MODE,
                {
                    _const.ATTR_ENTITY_ID: self._state.entity_id,
                    _media_player.ATTR_SOUND_MODE: sound_mode,
                },
                blocking=not self._config.should_report_state,
                context=data.context,
            )

        _LOGGER.info(
            f"Received an Options command for unrecognised domain {domain}",
        )
        return


@_register_trait
class InputSelectorTrait(_Trait):
    """Trait to set modes.

    https://developers.google.com/assistant/smarthome/traits/inputselector
    """

    _name = TRAIT_INPUTSELECTOR
    _commands = [COMMAND_INPUT, COMMAND_NEXT_INPUT, COMMAND_PREVIOUS_INPUT]

    SYNONYMS: typing.Final[dict[str, list[str]]] = {}

    @staticmethod
    def supported(domain, features, device_class, _):
        """Test if state is supported."""
        if domain == _EntityDomain.MEDIA_PLAYER and (
            features & _media_player.EntityFeature.SELECT_SOURCE
        ):
            return True

        return False

    def sync_attributes(self):
        """Return mode attributes for a sync request."""
        attrs = self._state.attributes
        inputs = [
            {"key": source, "names": [{"name_synonym": [source], "lang": "en"}]}
            for source in attrs.get(_media_player.ATTR_INPUT_SOURCE_LIST, [])
        ]

        payload = {"availableInputs": inputs, "orderedInputs": True}

        return payload

    def query_attributes(self):
        """Return current modes."""
        attrs = self._state.attributes
        return {"currentInput": attrs.get(_media_player.ATTR_INPUT_SOURCE, "")}

    async def execute(self, command, data, params, challenge):
        """Execute an SetInputSource command."""
        sources = self._state.attributes.get(_media_player.ATTR_INPUT_SOURCE_LIST) or []
        source = self._state.attributes.get(_media_player.ATTR_INPUT_SOURCE)

        if command == COMMAND_INPUT:
            requested_source = params.get("newInput")
        elif command == COMMAND_NEXT_INPUT:
            requested_source = _next_selected(sources, source)
        elif command == COMMAND_PREVIOUS_INPUT:
            requested_source = _next_selected(list(reversed(sources)), source)
        else:
            raise SmartHomeError(_google.ERR_NOT_SUPPORTED, "Unsupported command")

        if requested_source not in sources:
            raise SmartHomeError(_google.ERR_UNSUPPORTED_INPUT, "Unsupported input")

        await self.controller.services.async_call(
            self._state.domain,
            _media_player.SERVICE_SELECT_SOURCE,
            {
                _const.ATTR_ENTITY_ID: self._state.entity_id,
                _media_player.ATTR_INPUT_SOURCE: requested_source,
            },
            blocking=not self._config.should_report_state,
            context=data.context,
        )


@_register_trait
class OpenCloseTrait(_Trait):
    """Trait to open and close a cover.

    https://developers.google.com/actions/smarthome/traits/openclose
    """

    # Cover device classes that require 2FA
    COVER_2FA: typing.Final = (
        _cover.DeviceClass.DOOR,
        _cover.DeviceClass.GARAGE,
        _cover.DeviceClass.GATE,
    )

    _name = TRAIT_OPENCLOSE
    _commands = [COMMAND_OPENCLOSE, COMMAND_OPENCLOSE_RELATIVE]

    @staticmethod
    def supported(domain, features, device_class, _):
        """Test if state is supported."""
        if domain == _EntityDomain.COVER:
            return True

        return domain == _EntityDomain.BINARY_SENSOR and device_class in (
            _binary_sensor.DeviceClass.DOOR,
            _binary_sensor.DeviceClass.GARAGE_DOOR,
            _binary_sensor.DeviceClass.LOCK,
            _binary_sensor.DeviceClass.OPENING,
            _binary_sensor.DeviceClass.WINDOW,
        )

    @staticmethod
    def might_2fa(domain, features, device_class):
        """Return if the trait might ask for 2FA."""
        return (
            domain == _EntityDomain.COVER and device_class in OpenCloseTrait.COVER_2FA
        )

    def sync_attributes(self):
        """Return opening direction."""
        response = {}
        features = self._state.attributes.get(_const.ATTR_SUPPORTED_FEATURES, 0)
        domain = self._state.domain

        if domain == _EntityDomain.BINARY_SENSOR:
            response["queryOnlyOpenClose"] = True
            response["discreteOnlyOpenClose"] = True
        elif (
            domain == _EntityDomain.COVER
            and features & _cover.EntityFeature.SET_POSITION == 0
        ):
            response["discreteOnlyOpenClose"] = True

            if (
                features & _cover.EntityFeature.OPEN == 0
                and features & _cover.EntityFeature.CLOSE == 0
            ):
                response["queryOnlyOpenClose"] = True

        if self._state.attributes.get(_const.ATTR_ASSUMED_STATE):
            response["commandOnlyOpenClose"] = True

        return response

    def query_attributes(self):
        """Return state query attributes."""
        domain = self._state.domain
        response = {}

        # When it's an assumed state, we will return empty state
        # This shouldn't happen because we set `commandOnlyOpenClose`
        # but Google still queries. Erroring here will cause device
        # to show up offline.
        if self._state.attributes.get(_const.ATTR_ASSUMED_STATE):
            return response

        if domain == _EntityDomain.COVER:
            if self._state.state == _const.STATE_UNKNOWN:
                raise SmartHomeError(
                    _google.ERR_NOT_SUPPORTED, "Querying state is not supported"
                )

            position = self._state.attributes.get(_cover.ATTR_CURRENT_POSITION)

            if position is not None:
                response["openPercent"] = position
            elif self._state.state != _cover.STATE_CLOSED:
                response["openPercent"] = 100
            else:
                response["openPercent"] = 0

        elif domain == _EntityDomain.BINARY_SENSOR:
            if self._state.state == _const.STATE_ON:
                response["openPercent"] = 100
            else:
                response["openPercent"] = 0

        return response

    async def execute(self, command, data, params, challenge):
        """Execute an Open, close, Set position command."""
        domain = self._state.domain
        features = self._state.attributes.get(_const.ATTR_SUPPORTED_FEATURES, 0)

        if domain == _EntityDomain.COVER:
            svc_params = {_const.ATTR_ENTITY_ID: self._state.entity_id}
            should_verify = False
            if command == COMMAND_OPENCLOSE_RELATIVE:
                position = self._state.attributes.get(_cover.ATTR_CURRENT_POSITION)
                if position is None:
                    raise SmartHomeError(
                        _google.ERR_NOT_SUPPORTED,
                        "Current position not know for relative command",
                    )
                position = max(0, min(100, position + params["openRelativePercent"]))
            else:
                position = params["openPercent"]

            if position == 0:
                service = _cover.SERVICE_CLOSE
                should_verify = False
            elif position == 100:
                service = _cover.SERVICE_OPEN
                should_verify = True
            elif features & _cover.EntityFeature.SET_POSITION:
                service = _cover.SERVICE_SET_POSITION
                if position > 0:
                    should_verify = True
                svc_params[_cover.ATTR_POSITION] = position
            else:
                raise SmartHomeError(
                    _google.ERR_NOT_SUPPORTED, "No support for partial open close"
                )

            if (
                should_verify
                and self._state.attributes.get(_const.ATTR_DEVICE_CLASS)
                in OpenCloseTrait.COVER_2FA
            ):
                _verify_pin_challenge(data, self._state, challenge)

            await self.controller.services.async_call(
                domain,
                service,
                svc_params,
                blocking=not self._config.should_report_state,
                context=data.context,
            )


@_register_trait
class VolumeTrait(_Trait):
    """Trait to control volume of a device.

    https://developers.google.com/actions/smarthome/traits/volume
    """

    _name = TRAIT_VOLUME
    _commands = [COMMAND_SET_VOLUME, COMMAND_VOLUME_RELATIVE, COMMAND_MUTE]

    @staticmethod
    def supported(domain, features, device_class, _):
        """Test if trait is supported."""
        if domain == _EntityDomain.MEDIA_PLAYER:
            return features & (
                _media_player.EntityFeature.VOLUME_SET
                | _media_player.EntityFeature.VOLUME_STEP
            )

        return False

    def sync_attributes(self):
        """Return volume attributes for a sync request."""
        features = self._state.attributes.get(_const.ATTR_SUPPORTED_FEATURES, 0)
        return {
            "volumeCanMuteAndUnmute": bool(
                features & _media_player.EntityFeature.VOLUME_MUTE
            ),
            "commandOnlyVolume": self._state.attributes.get(
                _const.ATTR_ASSUMED_STATE, False
            ),
            # Volume amounts in SET_VOLUME and VOLUME_RELATIVE are on a scale
            # from 0 to this value.
            "volumeMaxLevel": 100,
            # Default change for queries like "Hey Google, volume up".
            # 10% corresponds to the default behavior for the
            # media_player.volume{up,down} services.
            "levelStepSize": 10,
        }

    def query_attributes(self):
        """Return volume query attributes."""
        response = {}

        level = self._state.attributes.get(_media_player.ATTR_MEDIA_VOLUME_LEVEL)
        if level is not None:
            # Convert 0.0-1.0 to 0-100
            response["currentVolume"] = round(level * 100)

        muted = self._state.attributes.get(_media_player.ATTR_MEDIA_VOLUME_MUTED)
        if muted is not None:
            response["isMuted"] = bool(muted)

        return response

    async def _set_volume_absolute(self, data, level):
        await self.controller.services.async_call(
            self._state.domain,
            _const.SERVICE_VOLUME_SET,
            {
                _const.ATTR_ENTITY_ID: self._state.entity_id,
                _media_player.ATTR_MEDIA_VOLUME_LEVEL: level,
            },
            blocking=not self._config.should_report_state,
            context=data.context,
        )

    async def _execute_set_volume(self, data, params):
        level = max(0, min(100, params["volumeLevel"]))

        if not (
            self._state.attributes.get(_const.ATTR_SUPPORTED_FEATURES, 0)
            & _media_player.EntityFeature.VOLUME_SET
        ):
            raise SmartHomeError(_google.ERR_NOT_SUPPORTED, "Command not supported")

        await self._set_volume_absolute(data, level / 100)

    async def _execute_volume_relative(self, data, params):
        relative = params["relativeSteps"]
        features = self._state.attributes.get(_const.ATTR_SUPPORTED_FEATURES, 0)

        if features & _media_player.EntityFeature.VOLUME_SET:
            current = self._state.attributes.get(_media_player.ATTR_MEDIA_VOLUME_LEVEL)
            target = max(0.0, min(1.0, current + relative / 100))

            await self._set_volume_absolute(data, target)

        elif features & _media_player.EntityFeature.VOLUME_STEP:
            svc = _const.SERVICE_VOLUME_UP
            if relative < 0:
                svc = _const.SERVICE_VOLUME_DOWN
                relative = -relative

            for _ in range(relative):
                await self.controller.services.async_call(
                    self._state.domain,
                    svc,
                    {_const.ATTR_ENTITY_ID: self._state.entity_id},
                    blocking=not self._config.should_report_state,
                    context=data.context,
                )
        else:
            raise SmartHomeError(_google.ERR_NOT_SUPPORTED, "Command not supported")

    async def _execute_mute(self, data, params):
        mute = params["mute"]

        if not (
            self._state.attributes.get(_const.ATTR_SUPPORTED_FEATURES, 0)
            & _media_player.EntityFeature.VOLUME_MUTE
        ):
            raise SmartHomeError(_google.ERR_NOT_SUPPORTED, "Command not supported")

        await self.controller.services.async_call(
            self._state.domain,
            _const.SERVICE_VOLUME_MUTE,
            {
                _const.ATTR_ENTITY_ID: self._state.entity_id,
                _media_player.ATTR_MEDIA_VOLUME_MUTED: mute,
            },
            blocking=not self._config.should_report_state,
            context=data.context,
        )

    async def execute(self, command, data, params, challenge):
        """Execute a volume command."""
        if command == COMMAND_SET_VOLUME:
            await self._execute_set_volume(data, params)
        elif command == COMMAND_VOLUME_RELATIVE:
            await self._execute_volume_relative(data, params)
        elif command == COMMAND_MUTE:
            await self._execute_mute(data, params)
        else:
            raise SmartHomeError(_google.ERR_NOT_SUPPORTED, "Command not supported")


def _verify_pin_challenge(data, state, challenge):
    """Verify a pin challenge."""
    if not data.config.should_2fa(state):
        return
    if not data.config.secure_devices_pin:
        raise SmartHomeError(_google.ERR_CHALLENGE_NOT_SETUP, "Challenge is not set up")

    if not challenge:
        raise ChallengeNeeded(_google.CHALLENGE_PIN_NEEDED)

    if challenge.get("pin") != data.config.secure_devices_pin:
        raise ChallengeNeeded(_google.CHALLENGE_FAILED_PIN_NEEDED)


def _verify_ack_challenge(data, state, challenge):
    """Verify an ack challenge."""
    if not data.config.should_2fa(state):
        return
    if not challenge or not challenge.get("ack"):
        raise ChallengeNeeded(_google.CHALLENGE_ACK_NEEDED)


MEDIA_COMMAND_SUPPORT_MAPPING: typing.Final = {
    COMMAND_MEDIA_NEXT: _media_player.EntityFeature.NEXT_TRACK,
    COMMAND_MEDIA_PAUSE: _media_player.EntityFeature.PAUSE,
    COMMAND_MEDIA_PREVIOUS: _media_player.EntityFeature.PREVIOUS_TRACK,
    COMMAND_MEDIA_RESUME: _media_player.EntityFeature.PLAY,
    COMMAND_MEDIA_SEEK_RELATIVE: _media_player.EntityFeature.SEEK,
    COMMAND_MEDIA_SEEK_TO_POSITION: _media_player.EntityFeature.SEEK,
    COMMAND_MEDIA_SHUFFLE: _media_player.EntityFeature.SHUFFLE_SET,
    COMMAND_MEDIA_STOP: _media_player.EntityFeature.STOP,
}

MEDIA_COMMAND_ATTRIBUTES: typing.Final = {
    COMMAND_MEDIA_NEXT: "NEXT",
    COMMAND_MEDIA_PAUSE: "PAUSE",
    COMMAND_MEDIA_PREVIOUS: "PREVIOUS",
    COMMAND_MEDIA_RESUME: "RESUME",
    COMMAND_MEDIA_SEEK_RELATIVE: "SEEK_RELATIVE",
    COMMAND_MEDIA_SEEK_TO_POSITION: "SEEK_TO_POSITION",
    COMMAND_MEDIA_SHUFFLE: "SHUFFLE",
    COMMAND_MEDIA_STOP: "STOP",
}


@_register_trait
class TransportControlTrait(_Trait):
    """Trait to control media playback.

    https://developers.google.com/actions/smarthome/traits/transportcontrol
    """

    _name = TRAIT_TRANSPORT_CONTROL
    _commands = [
        COMMAND_MEDIA_NEXT,
        COMMAND_MEDIA_PAUSE,
        COMMAND_MEDIA_PREVIOUS,
        COMMAND_MEDIA_RESUME,
        COMMAND_MEDIA_SEEK_RELATIVE,
        COMMAND_MEDIA_SEEK_TO_POSITION,
        COMMAND_MEDIA_SHUFFLE,
        COMMAND_MEDIA_STOP,
    ]

    @staticmethod
    def supported(domain, features, device_class, _):
        """Test if state is supported."""
        if domain == _EntityDomain.MEDIA_PLAYER:
            for feature in MEDIA_COMMAND_SUPPORT_MAPPING.values():
                if features & feature:
                    return True

        return False

    def sync_attributes(self):
        """Return opening direction."""
        response = {}

        if self._state.domain == _EntityDomain.MEDIA_PLAYER:
            features = self._state.attributes.get(_const.ATTR_SUPPORTED_FEATURES, 0)

            support = []
            for command, feature in MEDIA_COMMAND_SUPPORT_MAPPING.items():
                if features & feature:
                    support.append(MEDIA_COMMAND_ATTRIBUTES[command])
            response["transportControlSupportedCommands"] = support

        return response

    def query_attributes(self):
        """Return the attributes of this trait for this entity."""
        return {}

    async def execute(self, command, data, params, challenge):
        """Execute a media command."""
        service_attrs = {_const.ATTR_ENTITY_ID: self._state.entity_id}

        if command == COMMAND_MEDIA_SEEK_RELATIVE:
            service = _const.SERVICE_MEDIA_SEEK

            rel_position = params["relativePositionMs"] / 1000
            seconds_since = 0  # Default to 0 seconds
            if self._state.state == _const.STATE_PLAYING:
                now = _helpers.utcnow()
                upd_at = self._state.attributes.get(
                    _media_player.ATTR_MEDIA_POSITION_UPDATED_AT, now
                )
                seconds_since = (now - upd_at).total_seconds()
            position = self._state.attributes.get(_media_player.ATTR_MEDIA_POSITION, 0)
            max_position = self._state.attributes.get(
                _media_player.ATTR_MEDIA_DURATION, 0
            )
            service_attrs[_media_player.ATTR_MEDIA_SEEK_POSITION] = min(
                max(position + seconds_since + rel_position, 0), max_position
            )
        elif command == COMMAND_MEDIA_SEEK_TO_POSITION:
            service = _const.SERVICE_MEDIA_SEEK

            max_position = self._state.attributes.get(
                _media_player.ATTR_MEDIA_DURATION, 0
            )
            service_attrs[_media_player.ATTR_MEDIA_SEEK_POSITION] = min(
                max(params["absPositionMs"] / 1000, 0), max_position
            )
        elif command == COMMAND_MEDIA_NEXT:
            service = _const.SERVICE_MEDIA_NEXT_TRACK
        elif command == COMMAND_MEDIA_PAUSE:
            service = _const.SERVICE_MEDIA_PAUSE
        elif command == COMMAND_MEDIA_PREVIOUS:
            service = _const.SERVICE_MEDIA_PREVIOUS_TRACK
        elif command == COMMAND_MEDIA_RESUME:
            service = _const.SERVICE_MEDIA_PLAY
        elif command == COMMAND_MEDIA_SHUFFLE:
            service = _const.SERVICE_SHUFFLE_SET

            # Google Assistant only supports enabling shuffle
            service_attrs[_media_player.ATTR_MEDIA_SHUFFLE] = True
        elif command == COMMAND_MEDIA_STOP:
            service = _const.SERVICE_MEDIA_STOP
        else:
            raise SmartHomeError(_google.ERR_NOT_SUPPORTED, "Command not supported")

        await self.controller.services.async_call(
            self._state.domain,
            service,
            service_attrs,
            blocking=not self._config.should_report_state,
            context=data.context,
        )


@_register_trait
class MediaStateTrait(_Trait):
    """Trait to get media playback state.

    https://developers.google.com/actions/smarthome/traits/mediastate
    """

    # pylint: disable=abstract-method
    _name = TRAIT_MEDIA_STATE
    _commands: list[str] = []

    activity_lookup = {
        _const.STATE_OFF: "INACTIVE",
        _const.STATE_IDLE: "STANDBY",
        _const.STATE_PLAYING: "ACTIVE",
        _const.STATE_ON: "STANDBY",
        _const.STATE_PAUSED: "STANDBY",
        _const.STATE_STANDBY: "STANDBY",
        _const.STATE_UNAVAILABLE: "INACTIVE",
        _const.STATE_UNKNOWN: "INACTIVE",
    }

    playback_lookup = {
        _const.STATE_OFF: "STOPPED",
        _const.STATE_IDLE: "STOPPED",
        _const.STATE_PLAYING: "PLAYING",
        _const.STATE_ON: "STOPPED",
        _const.STATE_PAUSED: "PAUSED",
        _const.STATE_STANDBY: "STOPPED",
        _const.STATE_UNAVAILABLE: "STOPPED",
        _const.STATE_UNKNOWN: "STOPPED",
    }

    @staticmethod
    def supported(domain, features, device_class, _):
        """Test if state is supported."""
        return domain == _EntityDomain.MEDIA_PLAYER

    def sync_attributes(self):
        """Return attributes for a sync request."""
        return {"supportActivityState": True, "supportPlaybackState": True}

    def query_attributes(self):
        """Return the attributes of this trait for this entity."""
        return {
            "activityState": self.activity_lookup.get(self._state.state, "INACTIVE"),
            "playbackState": self.playback_lookup.get(self._state.state, "STOPPED"),
        }


@_register_trait
class ChannelTrait(_Trait):
    """Trait to get media playback state.

    https://developers.google.com/actions/smarthome/traits/channel
    """

    _name = TRAIT_CHANNEL
    _commands = [COMMAND_SELECT_CHANNEL]

    @staticmethod
    def supported(domain, features, device_class, _):
        """Test if state is supported."""
        if (
            domain == _EntityDomain.MEDIA_PLAYER
            and (features & _media_player.EntityFeature.PLAY_MEDIA)
            and device_class == _media_player.DeviceClass.TV
        ):
            return True

        return False

    def sync_attributes(self):
        """Return attributes for a sync request."""
        return {"availableChannels": [], "commandOnlyChannels": True}

    def query_attributes(self):
        """Return channel query attributes."""
        return {}

    async def execute(self, command, data, params, challenge):
        """Execute an setChannel command."""
        if command == COMMAND_SELECT_CHANNEL:
            channel_number = params.get("channelNumber")
        else:
            raise SmartHomeError(_google.ERR_NOT_SUPPORTED, "Unsupported command")

        if not channel_number:
            raise SmartHomeError(
                _google.ERR_NO_AVAILABLE_CHANNEL,
                "Channel is not available",
            )

        await self.controller.services.async_call(
            self._state.domain,
            _media_player.SERVICE_PLAY_MEDIA,
            {
                _const.ATTR_ENTITY_ID: self._state.entity_id,
                _media_player.ATTR_MEDIA_CONTENT_ID: channel_number,
                _media_player.ATTR_MEDIA_CONTENT_TYPE: _media_player.MediaType.CHANNEL,
            },
            blocking=not self._config.should_report_state,
            context=data.context,
        )


@_register_trait
class SensorStateTrait(_Trait):
    """Trait to get sensor state.

    https://developers.google.com/actions/smarthome/traits/sensorstate
    """

    # pylint: disable=abstract-method

    sensor_types = {
        _sensor.DeviceClass.AQI: ("AirQuality", "AQI"),
        _sensor.DeviceClass.CO: ("CarbonMonoxideLevel", "PARTS_PER_MILLION"),
        _sensor.DeviceClass.CO2: ("CarbonDioxideLevel", "PARTS_PER_MILLION"),
        _sensor.DeviceClass.PM25: ("PM2.5", "MICROGRAMS_PER_CUBIC_METER"),
        _sensor.DeviceClass.PM10: ("PM10", "MICROGRAMS_PER_CUBIC_METER"),
        _sensor.DeviceClass.VOLATILE_ORGANIC_COMPOUNDS: (
            "VolatileOrganicCompounds",
            "PARTS_PER_MILLION",
        ),
    }

    _name = TRAIT_SENSOR_STATE
    _commands: list[str] = []

    @classmethod
    def supported(cls, domain, features, device_class, _):
        """Test if state is supported."""
        return domain == _EntityDomain.SENSOR and device_class in cls.sensor_types

    def sync_attributes(self):
        """Return attributes for a sync request."""
        device_class = self._state.attributes.get(_const.ATTR_DEVICE_CLASS)
        if (data := self.sensor_types.get(device_class)) is not None:
            return {
                "sensorStatesSupported": {
                    "name": data[0],
                    "numericCapabilities": {"rawValueUnit": data[1]},
                }
            }
        return None

    def query_attributes(self):
        """Return the attributes of this trait for this entity."""
        device_class = self._state.attributes.get(_const.ATTR_DEVICE_CLASS)
        if (data := self.sensor_types.get(device_class)) is not None:
            return {
                "currentSensorStateData": [
                    {"name": data[0], "rawValue": self._state.state}
                ]
            }
        return None
