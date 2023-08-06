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
import typing

from ... import core
from .alexa_capability import AlexaCapability
from .alexa_capability_resource import AlexaCapabilityResource
from .alexa_global_catalog import AlexaGlobalCatalog
from .alexa_mode_resource import AlexaModeResource
from .alexa_preset_resource import AlexaPresetResource
from .alexa_semantics import AlexaSemantics

_const: typing.TypeAlias = core.Const
_alarm_control_panel: typing.TypeAlias = core.AlarmControlPanel
_alexa: typing.TypeAlias = core.Alexa
_climate: typing.TypeAlias = core.Climate
_cover: typing.TypeAlias = core.Cover
_fan: typing.TypeAlias = core.Fan
_input_number: typing.TypeAlias = core.InputNumber
_light: typing.TypeAlias = core.Light
_media_player: typing.TypeAlias = core.MediaPlayer
_platform: typing.TypeAlias = core.Platform
_vacuum: typing.TypeAlias = core.Vacuum

_LOGGER: typing.Final = logging.getLogger(__name__)


# pylint: disable=unused-variable
class Alexa(AlexaCapability):
    """Implements Alexa Interface.

    Although endpoints implement this interface implicitly,
    The API suggests you should explicitly include this interface.

    https://developer.amazon.com/docs/device-apis/alexa-interface.html
    """

    _supported_locales = {
        "ar-SA",
        "de-DE",
        "en-AU",
        "en-CA",
        "en-GB",
        "en-IN",
        "en-US",
        "es-ES",
        "es-MX",
        "es-US",
        "fr-CA",
        "fr-FR",
        "hi-IN",
        "it-IT",
        "ja-JP",
        "pt-BR",
    }

    def name(self):
        """Return the Alexa API name of this interface."""
        return "Alexa"


class AlexaEndpointHealth(AlexaCapability):
    """Implements Alexa.EndpointHealth.

    https://developer.amazon.com/docs/smarthome/state-reporting-for-a-smart-home-skill.html#report-state-when-alexa-requests-it
    """

    _supported_locales = {
        "ar-SA",
        "de-DE",
        "en-AU",
        "en-CA",
        "en-GB",
        "en-IN",
        "en-US",
        "es-ES",
        "es-MX",
        "es-US",
        "fr-CA",
        "fr-FR",
        "hi-IN",
        "it-IT",
        "ja-JP",
        "pt-BR",
    }

    def name(self):
        """Return the Alexa API name of this interface."""
        return "Alexa.EndpointHealth"

    def properties_supported(self):
        """Return what properties this entity supports."""
        return [{"name": "connectivity"}]

    def properties_proactively_reported(self):
        """Return True if properties asynchronously reported."""
        return True

    def properties_retrievable(self):
        """Return True if properties can be retrieved."""
        return True

    def get_property(self, name):
        """Read and return a property."""
        if name != "connectivity":
            raise _alexa.UnsupportedProperty(name)

        if self._entity.state == _const.STATE_UNAVAILABLE:
            return {"value": "UNREACHABLE"}
        return {"value": "OK"}


class AlexaPowerController(AlexaCapability):
    """Implements Alexa.PowerController.

    https://developer.amazon.com/docs/device-apis/alexa-powercontroller.html
    """

    _supported_locales = {
        "ar-SA",
        "de-DE",
        "en-AU",
        "en-CA",
        "en-GB",
        "en-IN",
        "en-US",
        "es-ES",
        "es-MX",
        "es-US",
        "fr-CA",
        "fr-FR",
        "hi-IN",
        "it-IT",
        "ja-JP",
        "pt-BR",
    }

    def name(self):
        """Return the Alexa API name of this interface."""
        return "Alexa.PowerController"

    def properties_supported(self):
        """Return what properties this entity supports."""
        return [{"name": "powerState"}]

    def properties_proactively_reported(self):
        """Return True if properties asynchronously reported."""
        return True

    def properties_retrievable(self):
        """Return True if properties can be retrieved."""
        return True

    def get_property(self, name: str):
        """Read and return a property."""
        if name != "powerState":
            raise _alexa.UnsupportedProperty(name)

        domain = self._entity.domain
        if domain == _platform.CLIMATE:
            is_on = self._entity.state != _climate.HVACMode.OFF
        elif domain == _platform.FAN:
            is_on = self._entity.state == _const.STATE_ON
        elif domain == _platform.VACUUM:
            is_on = self._entity.state == _vacuum.STATE_CLEANING
        elif domain == _platform.TIMER:
            is_on = self._entity.state != _const.STATE_IDLE

        else:
            is_on = self._entity.state != _const.STATE_OFF

        return "ON" if is_on else "OFF"


class AlexaLockController(AlexaCapability):
    """Implements Alexa.LockController.

    https://developer.amazon.com/docs/device-apis/alexa-lockcontroller.html
    """

    _supported_locales = {
        "ar-SA",
        "de-DE",
        "en-AU",
        "en-CA",
        "en-GB",
        "en-IN",
        "en-US",
        "es-ES",
        "es-MX",
        "es-US",
        "fr-CA",
        "fr-FR",
        "hi-IN",
        "it-IT",
        "ja-JP",
        "pt-BR",
    }

    def name(self):
        """Return the Alexa API name of this interface."""
        return "Alexa.LockController"

    def properties_supported(self):
        """Return what properties this entity supports."""
        return [{"name": "lockState"}]

    def properties_retrievable(self):
        """Return True if properties can be retrieved."""
        return True

    def properties_proactively_reported(self):
        """Return True if properties asynchronously reported."""
        return True

    def get_property(self, name):
        """Read and return a property."""
        if name != "lockState":
            raise _alexa.UnsupportedProperty(name)

        # If its unlocking its still locked and not unlocked yet
        if self._entity.state in (_const.STATE_UNLOCKING, _const.STATE_LOCKED):
            return "LOCKED"
        # If its locking its still unlocked and not locked yet
        if self._entity.state in (_const.STATE_LOCKING, _const.STATE_UNLOCKED):
            return "UNLOCKED"
        return "JAMMED"


class AlexaSceneController(AlexaCapability):
    """Implements Alexa.SceneController.

    https://developer.amazon.com/docs/device-apis/alexa-scenecontroller.html
    """

    _supported_locales = {
        "de-DE",
        "en-AU",
        "en-CA",
        "en-GB",
        "en-IN",
        "en-US",
        "es-ES",
        "es-MX",
        "es-US",
        "fr-CA",
        "fr-FR",
        "hi-IN",
        "it-IT",
        "ja-JP",
        "pt-BR",
    }

    def __init__(self, entity: core.State, supports_deactivation):
        """Initialize the entity."""
        super().__init__(entity)
        self._supports_deactivation = supports_deactivation

    def name(self):
        """Return the Alexa API name of this interface."""
        return "Alexa.SceneController"


class AlexaBrightnessController(AlexaCapability):
    """Implements Alexa.BrightnessController.

    https://developer.amazon.com/docs/device-apis/alexa-brightnesscontroller.html
    """

    _supported_locales = {
        "ar-SA",
        "de-DE",
        "en-AU",
        "en-CA",
        "en-GB",
        "en-IN",
        "en-US",
        "es-ES",
        "es-MX",
        "es-US",
        "fr-CA",
        "fr-FR",
        "hi-IN",
        "it-IT",
        "ja-JP",
        "pt-BR",
    }

    def name(self):
        """Return the Alexa API name of this interface."""
        return "Alexa.BrightnessController"

    def properties_supported(self):
        """Return what properties this entity supports."""
        return [{"name": "brightness"}]

    def properties_proactively_reported(self):
        """Return True if properties asynchronously reported."""
        return True

    def properties_retrievable(self):
        """Return True if properties can be retrieved."""
        return True

    def get_property(self, name):
        """Read and return a property."""
        if name != "brightness":
            raise _alexa.UnsupportedProperty(name)
        if "brightness" in self._entity.attributes:
            return round(self._entity.attributes["brightness"] / 255.0 * 100)
        return 0


class AlexaColorController(AlexaCapability):
    """Implements Alexa.ColorController.

    https://developer.amazon.com/docs/device-apis/alexa-colorcontroller.html
    """

    _supported_locales = {
        "de-DE",
        "en-AU",
        "en-CA",
        "en-GB",
        "en-IN",
        "en-US",
        "es-ES",
        "es-MX",
        "es-US",
        "fr-CA",
        "fr-FR",
        "hi-IN",
        "it-IT",
        "ja-JP",
        "pt-BR",
    }

    def name(self):
        """Return the Alexa API name of this interface."""
        return "Alexa.ColorController"

    def properties_supported(self):
        """Return what properties this entity supports."""
        return [{"name": "color"}]

    def properties_proactively_reported(self):
        """Return True if properties asynchronously reported."""
        return True

    def properties_retrievable(self):
        """Return True if properties can be retrieved."""
        return True

    def get_property(self, name: str):
        """Read and return a property."""
        if name != "color":
            raise _alexa.UnsupportedProperty(name)

        hue, saturation = self._entity.attributes.get(_light.ATTR_HS_COLOR, (0, 0))

        return {
            "hue": hue,
            "saturation": saturation / 100.0,
            "brightness": self._entity.attributes.get(_light.ATTR_BRIGHTNESS, 0)
            / 255.0,
        }


class AlexaColorTemperatureController(AlexaCapability):
    """Implements Alexa.ColorTemperatureController.

    https://developer.amazon.com/docs/device-apis/alexa-colortemperaturecontroller.html
    """

    _supported_locales = {
        "de-DE",
        "en-AU",
        "en-CA",
        "en-GB",
        "en-IN",
        "en-US",
        "es-ES",
        "es-MX",
        "es-US",
        "fr-CA",
        "fr-FR",
        "hi-IN",
        "it-IT",
        "ja-JP",
        "pt-BR",
    }

    def name(self):
        """Return the Alexa API name of this interface."""
        return "Alexa.ColorTemperatureController"

    def properties_supported(self):
        """Return what properties this entity supports."""
        return [{"name": "colorTemperatureInKelvin"}]

    def properties_proactively_reported(self):
        """Return True if properties asynchronously reported."""
        return True

    def properties_retrievable(self):
        """Return True if properties can be retrieved."""
        return True

    def get_property(self, name):
        """Read and return a property."""
        if name != "colorTemperatureInKelvin":
            raise _alexa.UnsupportedProperty(name)
        if "color_temp" in self._entity.attributes:
            return core.helpers.Color.temperature_mired_to_kelvin(
                self._entity.attributes["color_temp"]
            )
        return None


class AlexaPercentageController(AlexaCapability):
    """Implements Alexa.PercentageController.

    https://developer.amazon.com/docs/device-apis/alexa-percentagecontroller.html
    """

    _supported_locales = {
        "de-DE",
        "en-AU",
        "en-CA",
        "en-GB",
        "en-IN",
        "en-US",
        "es-ES",
        "es-US",
        "fr-CA",
        "fr-FR",
        "hi-IN",
        "it-IT",
        "ja-JP",
        "pt-BR",
    }

    def name(self):
        """Return the Alexa API name of this interface."""
        return "Alexa.PercentageController"

    def properties_supported(self):
        """Return what properties this entity supports."""
        return [{"name": "percentage"}]

    def properties_proactively_reported(self):
        """Return True if properties asynchronously reported."""
        return True

    def properties_retrievable(self):
        """Return True if properties can be retrieved."""
        return True

    def get_property(self, name: str):
        """Read and return a property."""
        if name != "percentage":
            raise _alexa.UnsupportedProperty(name)

        if self._entity.domain == _platform.FAN:
            return self._entity.attributes.get(_fan.ATTR_PERCENTAGE) or 0

        if self._entity.domain == _platform.COVER:
            return self._entity.attributes.get(_cover.ATTR_CURRENT_POSITION, 0)

        return 0


class AlexaSpeaker(AlexaCapability):
    """Implements Alexa.Speaker.

    https://developer.amazon.com/docs/device-apis/alexa-speaker.html
    """

    _supported_locales = {
        "de-DE",
        "en-AU",
        "en-CA",
        "en-GB",
        "en-IN",
        "en-US",
        "es-ES",
        "es-MX",
        "fr-FR",  # Not documented as of 2021-12-04, see PR #60489
        "it-IT",
        "ja-JP",
    }

    def name(self):
        """Return the Alexa API name of this interface."""
        return "Alexa.Speaker"

    def properties_supported(self):
        """Return what properties this entity supports."""
        properties = [{"name": "volume"}]

        supported = self._entity.attributes.get(_const.ATTR_SUPPORTED_FEATURES, 0)
        if supported & _media_player.EntityFeature.VOLUME_MUTE:
            properties.append({"name": "muted"})

        return properties

    def properties_proactively_reported(self):
        """Return True if properties asynchronously reported."""
        return True

    def properties_retrievable(self):
        """Return True if properties can be retrieved."""
        return True

    def get_property(self, name: str):
        """Read and return a property."""
        if name == "volume":
            current_level = self._entity.attributes.get(
                _media_player.ATTR_MEDIA_VOLUME_LEVEL
            )
            if current_level is not None:
                return round(float(current_level) * 100)

        if name == "muted":
            return bool(
                self._entity.attributes.get(_media_player.ATTR_MEDIA_VOLUME_MUTED)
            )

        return None


class AlexaStepSpeaker(AlexaCapability):
    """Implements Alexa.StepSpeaker.

    https://developer.amazon.com/docs/device-apis/alexa-stepspeaker.html
    """

    _supported_locales = {
        "de-DE",
        "en-AU",
        "en-CA",
        "en-GB",
        "en-IN",
        "en-US",
        "es-ES",
        "fr-FR",  # Not documented as of 2021-12-04, see PR #60489
        "it-IT",
    }

    def name(self):
        """Return the Alexa API name of this interface."""
        return "Alexa.StepSpeaker"


class AlexaPlaybackController(AlexaCapability):
    """Implements Alexa.PlaybackController.

    https://developer.amazon.com/docs/device-apis/alexa-playbackcontroller.html
    """

    _supported_locales = {
        "ar-SA",
        "de-DE",
        "en-AU",
        "en-CA",
        "en-GB",
        "en-IN",
        "en-US",
        "es-ES",
        "es-MX",
        "es-US",
        "fr-CA",
        "fr-FR",
        "hi-IN",
        "it-IT",
        "ja-JP",
        "pt-BR",
    }

    def name(self):
        """Return the Alexa API name of this interface."""
        return "Alexa.PlaybackController"

    def supported_operations(self):
        """Return the supportedOperations object.

        Supported Operations: FastForward, Next, Pause, Play, Previous, Rewind, StartOver, Stop
        """
        supported_features = self._entity.attributes.get(
            _const.ATTR_SUPPORTED_FEATURES, 0
        )

        operations = {
            _media_player.EntityFeature.NEXT_TRACK: "Next",
            _media_player.EntityFeature.PAUSE: "Pause",
            _media_player.EntityFeature.PLAY: "Play",
            _media_player.EntityFeature.PREVIOUS_TRACK: "Previous",
            _media_player.EntityFeature.STOP: "Stop",
        }

        return [
            value
            for operation, value in operations.items()
            if operation & supported_features
        ]


class AlexaInputController(AlexaCapability):
    """Implements Alexa.InputController.

    https://developer.amazon.com/docs/device-apis/alexa-inputcontroller.html
    """

    _supported_locales = {
        "ar-SA",
        "de-DE",
        "en-AU",
        "en-CA",
        "en-GB",
        "en-IN",
        "en-US",
        "es-ES",
        "es-MX",
        "es-US",
        "fr-CA",
        "fr-FR",
        "hi-IN",
        "it-IT",
        "ja-JP",
        "pt-BR",
    }

    def name(self):
        """Return the Alexa API name of this interface."""
        return "Alexa.InputController"

    def inputs(self):
        """Return the list of valid supported inputs."""
        source_list = self._entity.attributes.get(
            _media_player.ATTR_INPUT_SOURCE_LIST, []
        )
        return AlexaInputController.get_valid_inputs(source_list)

    @staticmethod
    def get_valid_inputs(source_list):
        """Return list of supported inputs."""
        input_list = []
        for source in source_list:
            if not isinstance(source, str):
                continue
            formatted_source = (
                source.lower().replace("-", "").replace("_", "").replace(" ", "")
            )
            if formatted_source in _alexa.Inputs.VALID_SOURCE_NAME_MAP:
                input_list.append(
                    {"name": _alexa.Inputs.VALID_SOURCE_NAME_MAP[formatted_source]}
                )

        return input_list


class AlexaTemperatureSensor(AlexaCapability):
    """Implements Alexa.TemperatureSensor.

    https://developer.amazon.com/docs/device-apis/alexa-temperaturesensor.html
    """

    _supported_locales = {
        "ar-SA",
        "de-DE",
        "en-AU",
        "en-CA",
        "en-GB",
        "en-IN",
        "en-US",
        "es-ES",
        "es-MX",
        "es-US",
        "fr-CA",
        "fr-FR",
        "hi-IN",
        "it-IT",
        "ja-JP",
        "pt-BR",
    }

    def __init__(self, shc: core.SmartHomeController, entity: core.State):
        """Initialize the entity."""
        super().__init__(entity)
        self._shc = shc

    def name(self):
        """Return the Alexa API name of this interface."""
        return "Alexa.TemperatureSensor"

    def properties_supported(self):
        """Return what properties this entity supports."""
        return [{"name": "temperature"}]

    def properties_proactively_reported(self):
        """Return True if properties asynchronously reported."""
        return True

    def properties_retrievable(self):
        """Return True if properties can be retrieved."""
        return True

    def get_property(self, name):
        """Read and return a property."""
        if name != "temperature":
            raise _alexa.UnsupportedProperty(name)

        unit = self._entity.attributes.get(_const.ATTR_UNIT_OF_MEASUREMENT)
        temp = self._entity.state
        if self._entity.domain == _platform.CLIMATE:
            unit = self._shc.config.units.temperature_unit
            temp = self._entity.attributes.get(_climate.ATTR_CURRENT_TEMPERATURE)

        if temp in (_const.STATE_UNAVAILABLE, _const.STATE_UNKNOWN, None):
            return None

        try:
            temp = float(temp)
        except ValueError:
            _LOGGER.warning(f"Invalid temp value {temp} for {self._entity.entity_id}")
            return None

        return {"value": temp, "scale": _alexa.API_TEMP_UNITS[unit]}


class AlexaContactSensor(AlexaCapability):
    """Implements Alexa.ContactSensor.

    The Alexa.ContactSensor interface describes the properties and events used
    to report the state of an endpoint that detects contact between two
    surfaces. For example, a contact sensor can report whether a door or window
    is open.

    https://developer.amazon.com/docs/device-apis/alexa-contactsensor.html
    """

    _supported_locales = {
        "de-DE",
        "en-AU",
        "en-CA",
        "en-GB",
        "en-IN",
        "en-US",
        "es-ES",
        "es-MX",
        "es-US",
        "fr-CA",
        "fr-FR",
        "hi-IN",
        "it-IT",
        "ja-JP",
        "pt-BR",
    }

    def name(self):
        """Return the Alexa API name of this interface."""
        return "Alexa.ContactSensor"

    def properties_supported(self):
        """Return what properties this entity supports."""
        return [{"name": "detectionState"}]

    def properties_proactively_reported(self):
        """Return True if properties asynchronously reported."""
        return True

    def properties_retrievable(self):
        """Return True if properties can be retrieved."""
        return True

    def get_property(self, name):
        """Read and return a property."""
        if name != "detectionState":
            raise _alexa.UnsupportedProperty(name)

        if self._entity.state == _const.STATE_ON:
            return "DETECTED"
        return "NOT_DETECTED"


class AlexaMotionSensor(AlexaCapability):
    """Implements Alexa.MotionSensor.

    https://developer.amazon.com/docs/device-apis/alexa-motionsensor.html
    """

    _supported_locales = {
        "de-DE",
        "en-AU",
        "en-CA",
        "en-GB",
        "en-IN",
        "en-US",
        "es-ES",
        "es-MX",
        "es-US",
        "fr-CA",
        "fr-FR",
        "hi-IN",
        "it-IT",
        "ja-JP",
        "pt-BR",
    }

    def name(self):
        """Return the Alexa API name of this interface."""
        return "Alexa.MotionSensor"

    def properties_supported(self):
        """Return what properties this entity supports."""
        return [{"name": "detectionState"}]

    def properties_proactively_reported(self):
        """Return True if properties asynchronously reported."""
        return True

    def properties_retrievable(self):
        """Return True if properties can be retrieved."""
        return True

    def get_property(self, name: str):
        """Read and return a property."""
        if name != "detectionState":
            raise _alexa.UnsupportedProperty(name)

        if self._entity.state == _const.STATE_ON:
            return "DETECTED"
        return "NOT_DETECTED"


class AlexaThermostatController(AlexaCapability):
    """Implements Alexa.ThermostatController.

    https://developer.amazon.com/docs/device-apis/alexa-thermostatcontroller.html
    """

    _supported_locales = {
        "ar-SA",
        "de-DE",
        "en-AU",
        "en-CA",
        "en-GB",
        "en-IN",
        "en-US",
        "es-ES",
        "es-MX",
        "es-US",
        "fr-CA",
        "fr-FR",
        "hi-IN",
        "it-IT",
        "ja-JP",
        "pt-BR",
    }

    def __init__(self, shc: core.SmartHomeController, entity: core.State):
        """Initialize the entity."""
        super().__init__(entity)
        self._shc = shc

    def name(self):
        """Return the Alexa API name of this interface."""
        return "Alexa.ThermostatController"

    def properties_supported(self):
        """Return what properties this entity supports."""
        properties = [{"name": "thermostatMode"}]
        supported = self._entity.attributes.get(_const.ATTR_SUPPORTED_FEATURES, 0)
        if supported & _climate.EntityFeature.TARGET_TEMPERATURE:
            properties.append({"name": "targetSetpoint"})
        if supported & _climate.EntityFeature.TARGET_TEMPERATURE_RANGE:
            properties.append({"name": "lowerSetpoint"})
            properties.append({"name": "upperSetpoint"})
        return properties

    def properties_proactively_reported(self):
        """Return True if properties asynchronously reported."""
        return True

    def properties_retrievable(self):
        """Return True if properties can be retrieved."""
        return True

    def get_property(self, name: str):
        """Read and return a property."""
        if self._entity.state == _const.STATE_UNAVAILABLE:
            return None

        if name == "thermostatMode":
            preset = self._entity.attributes.get(_climate.ATTR_PRESET_MODE)

            if preset in _alexa.API_THERMOSTAT_PRESETS:
                mode = _alexa.API_THERMOSTAT_PRESETS[preset]
            elif self._entity.state == _const.STATE_UNKNOWN:
                return None
            else:
                mode = _alexa.API_THERMOSTAT_MODES.get(self._entity.state)
                if mode is None:
                    _LOGGER.error(
                        f"{self._entity.entity_id} ({type(self._entity)}) has unsupported "
                        + f"state value '{self._entity.state}'",
                    )
                    raise _alexa.UnsupportedProperty(name)
            return mode

        unit = self._shc.config.units.temperature_unit
        if name == "targetSetpoint":
            temp = self._entity.attributes.get(_const.ATTR_TEMPERATURE)
        elif name == "lowerSetpoint":
            temp = self._entity.attributes.get(_climate.ATTR_TARGET_TEMP_LOW)
        elif name == "upperSetpoint":
            temp = self._entity.attributes.get(_climate.ATTR_TARGET_TEMP_HIGH)
        else:
            raise _alexa.UnsupportedProperty(name)

        if temp is None:
            return None

        try:
            temp = float(temp)
        except ValueError:
            _LOGGER.warning(
                f"Invalid temp value {temp} for {name} in {self._entity.entity_id}"
            )
            return None

        return {"value": temp, "scale": _alexa.API_TEMP_UNITS[unit]}

    def configuration(self):
        """Return configuration object.

        Translates climate HVAC_MODES and PRESETS to supported Alexa ThermostatMode Values.
        ThermostatMode Value must be AUTO, COOL, HEAT, ECO, OFF, or CUSTOM.
        """
        supported_modes = []
        hvac_modes = self._entity.attributes.get(_climate.ATTR_HVAC_MODES)
        for mode in hvac_modes:
            if thermostat_mode := _alexa.API_THERMOSTAT_MODES.get(mode):
                supported_modes.append(thermostat_mode)

        preset_modes = self._entity.attributes.get(_climate.ATTR_PRESET_MODES)
        if preset_modes:
            for mode in preset_modes:
                thermostat_mode = _alexa.API_THERMOSTAT_PRESETS.get(mode)
                if thermostat_mode:
                    supported_modes.append(thermostat_mode)

        # Return False for supportsScheduling until supported with event listener in handler.
        configuration = {"supportsScheduling": False}

        if supported_modes:
            configuration["supportedModes"] = supported_modes

        return configuration


class AlexaPowerLevelController(AlexaCapability):
    """Implements Alexa.PowerLevelController.

    https://developer.amazon.com/docs/device-apis/alexa-powerlevelcontroller.html
    """

    _supported_locales = {
        "de-DE",
        "en-AU",
        "en-CA",
        "en-GB",
        "en-IN",
        "en-US",
        "es-ES",
        "es-MX",
        "fr-CA",
        "fr-FR",
        "it-IT",
        "ja-JP",
    }

    def name(self):
        """Return the Alexa API name of this interface."""
        return "Alexa.PowerLevelController"

    def properties_supported(self):
        """Return what properties this entity supports."""
        return [{"name": "powerLevel"}]

    def properties_proactively_reported(self):
        """Return True if properties asynchronously reported."""
        return True

    def properties_retrievable(self):
        """Return True if properties can be retrieved."""
        return True

    def get_property(self, name: str):
        """Read and return a property."""
        if name != "powerLevel":
            raise _alexa.UnsupportedProperty(name)


class AlexaSecurityPanelController(AlexaCapability):
    """Implements Alexa.SecurityPanelController.

    https://developer.amazon.com/docs/device-apis/alexa-securitypanelcontroller.html
    """

    _supported_locales = {
        "de-DE",
        "en-AU",
        "en-CA",
        "en-GB",
        "en-IN",
        "en-US",
        "es-ES",
        "es-MX",
        "es-US",
        "fr-CA",
        "fr-FR",
        "it-IT",
        "ja-JP",
        "pt-BR",
    }

    def name(self):
        """Return the Alexa API name of this interface."""
        return "Alexa.SecurityPanelController"

    def properties_supported(self):
        """Return what properties this entity supports."""
        return [{"name": "armState"}]

    def properties_proactively_reported(self):
        """Return True if properties asynchronously reported."""
        return True

    def properties_retrievable(self):
        """Return True if properties can be retrieved."""
        return True

    def get_property(self, name: str):
        """Read and return a property."""
        if name != "armState":
            raise _alexa.UnsupportedProperty(name)

        arm_state = self._entity.state
        if arm_state == _const.STATE_ALARM_ARMED_HOME:
            return "ARMED_STAY"
        if arm_state == _const.STATE_ALARM_ARMED_AWAY:
            return "ARMED_AWAY"
        if arm_state == _const.STATE_ALARM_ARMED_NIGHT:
            return "ARMED_NIGHT"
        if arm_state == _const.STATE_ALARM_ARMED_CUSTOM_BYPASS:
            return "ARMED_STAY"
        return "DISARMED"

    def configuration(self):
        """Return configuration object with supported authorization types."""
        code_format = self._entity.attributes.get(_const.ATTR_CODE_FORMAT)
        supported = self._entity.attributes[_const.ATTR_SUPPORTED_FEATURES]
        configuration = {}

        supported_arm_states = [{"value": "DISARMED"}]
        if supported & _alarm_control_panel.EntityFeature.ARM_AWAY:
            supported_arm_states.append({"value": "ARMED_AWAY"})
        if supported & _alarm_control_panel.EntityFeature.ARM_HOME:
            supported_arm_states.append({"value": "ARMED_STAY"})
        if supported & _alarm_control_panel.EntityFeature.ARM_NIGHT:
            supported_arm_states.append({"value": "ARMED_NIGHT"})

        configuration["supportedArmStates"] = supported_arm_states

        if code_format == _alarm_control_panel.CodeFormat.NUMBER:
            configuration["supportedAuthorizationTypes"] = [{"type": "FOUR_DIGIT_PIN"}]

        return configuration


class AlexaModeController(AlexaCapability):
    """Implements Alexa.ModeController.

    The instance property must be unique across ModeController, RangeController, ToggleController
    within the same device.
    The instance property should be a concatenated string of device domain period and single word.
    e.g. fan.speed & fan.direction.

    The instance property must not contain words from other instance property strings within the
    same device.
    e.g. Instance property cover.position & cover.tilt_position will cause the Alexa.Discovery
    directive to fail.

    An instance property string value may be reused for different devices.

    https://developer.amazon.com/docs/device-apis/alexa-modecontroller.html
    """

    _supported_locales = {
        "de-DE",
        "en-AU",
        "en-CA",
        "en-GB",
        "en-IN",
        "en-US",
        "es-ES",
        "es-MX",
        "es-US",
        "fr-CA",
        "fr-FR",
        "hi-IN",
        "it-IT",
        "ja-JP",
        "pt-BR",
    }

    def __init__(self, entity: core.State, instance: str, non_controllable=False):
        """Initialize the entity."""
        super().__init__(entity, instance)
        self._resource = None
        self._semantics = None
        self._properties_non_controllable = non_controllable

    def name(self):
        """Return the Alexa API name of this interface."""
        return "Alexa.ModeController"

    def properties_supported(self):
        """Return what properties this entity supports."""
        return [{"name": "mode"}]

    def properties_proactively_reported(self):
        """Return True if properties asynchronously reported."""
        return True

    def properties_retrievable(self):
        """Return True if properties can be retrieved."""
        return True

    def get_property(self, name):
        """Read and return a property."""
        if name != "mode":
            raise _alexa.UnsupportedProperty(name)

        # Fan Direction
        if self._instance == f"{_platform.FAN}.{_fan.ATTR_DIRECTION}":
            mode = self._entity.attributes.get(_fan.ATTR_DIRECTION, None)
            if mode in (
                _fan.DIRECTION_FORWARD,
                _fan.DIRECTION_REVERSE,
                _const.STATE_UNKNOWN,
            ):
                return f"{_fan.ATTR_DIRECTION}.{mode}"

        # Fan preset_mode
        if self._instance == f"{_platform.FAN}.{_fan.ATTR_PRESET_MODE}":
            mode = self._entity.attributes.get(_fan.ATTR_PRESET_MODE, None)
            if mode in self._entity.attributes.get(_fan.ATTR_PRESET_MODES, None):
                return f"{_fan.ATTR_PRESET_MODE}.{mode}"

        # Cover Position
        if self._instance == f"{_platform.COVER}.{_cover.ATTR_POSITION}":
            # Return state instead of position when using ModeController.
            mode = self._entity.state
            if mode in (
                _cover.STATE_OPEN,
                _cover.STATE_OPENING,
                _cover.STATE_CLOSED,
                _cover.STATE_CLOSING,
                _const.STATE_UNKNOWN,
            ):
                return f"{_cover.ATTR_POSITION}.{mode}"

        return None

    def configuration(self):
        """Return configuration with modeResources."""
        if isinstance(self._resource, AlexaCapabilityResource):
            return self._resource.serialize_configuration()

        return None

    def capability_resources(self):
        """Return capabilityResources object."""

        # Fan Direction Resource
        instance = self._instance
        if instance == f"{_platform.FAN}.{_fan.ATTR_DIRECTION}":
            self._resource = AlexaModeResource(
                [AlexaGlobalCatalog.SETTING_DIRECTION], False
            )
            self._resource.add_mode(
                f"{_fan.ATTR_DIRECTION}.{_fan.DIRECTION_FORWARD}",
                [_fan.DIRECTION_FORWARD],
            )
            self._resource.add_mode(
                f"{_fan.ATTR_DIRECTION}.{_fan.DIRECTION_REVERSE}",
                [_fan.DIRECTION_REVERSE],
            )
            return self._resource.serialize_capability_resources()

        # Fan preset_mode
        if instance == f"{_platform.FAN}.{_fan.ATTR_PRESET_MODE}":
            self._resource = AlexaModeResource(
                [AlexaGlobalCatalog.SETTING_PRESET], False
            )
            preset_modes = self._entity.attributes.get(_fan.ATTR_PRESET_MODES, [])
            for preset_mode in preset_modes:
                self._resource.add_mode(
                    f"{_fan.ATTR_PRESET_MODE}.{preset_mode}", [preset_mode]
                )
            # Fans with a single preset_mode completely break Alexa discovery, add a
            # fake preset (see issue #53832).
            if len(preset_modes) == 1:
                self._resource.add_mode(
                    f"{_fan.ATTR_PRESET_MODE}.{_alexa.PRESET_MODE_NA}",
                    [_alexa.PRESET_MODE_NA],
                )
            return self._resource.serialize_capability_resources()

        # Cover Position Resources
        if instance == f"{_platform.COVER}.{_cover.ATTR_POSITION}":
            self._resource = AlexaModeResource(
                ["Position", AlexaGlobalCatalog.SETTING_OPENING], False
            )
            self._resource.add_mode(
                f"{_cover.ATTR_POSITION}.{_cover.STATE_OPEN}",
                [AlexaGlobalCatalog.VALUE_OPEN],
            )
            self._resource.add_mode(
                f"{_cover.ATTR_POSITION}.{_cover.STATE_CLOSED}",
                [AlexaGlobalCatalog.VALUE_CLOSE],
            )
            self._resource.add_mode(
                f"{_cover.ATTR_POSITION}.custom",
                ["Custom", AlexaGlobalCatalog.SETTING_PRESET],
            )
            return self._resource.serialize_capability_resources()

        return None

    def semantics(self):
        """Build and return semantics object."""
        supported = self._entity.attributes.get(_const.ATTR_SUPPORTED_FEATURES, 0)

        # Cover Position
        if self._instance == f"{_platform.COVER}.{_cover.ATTR_POSITION}":
            lower_labels = [AlexaSemantics.ACTION_LOWER]
            raise_labels = [AlexaSemantics.ACTION_RAISE]
            self._semantics = AlexaSemantics()

            # Add open/close semantics if tilt is not supported.
            if not supported & _cover.EntityFeature.SET_TILT_POSITION:
                lower_labels.append(AlexaSemantics.ACTION_CLOSE)
                raise_labels.append(AlexaSemantics.ACTION_OPEN)
                self._semantics.add_states_to_value(
                    [AlexaSemantics.STATES_CLOSED],
                    f"{_cover.ATTR_POSITION}.{_cover.STATE_CLOSED}",
                )
                self._semantics.add_states_to_value(
                    [AlexaSemantics.STATES_OPEN],
                    f"{_cover.ATTR_POSITION}.{_cover.STATE_OPEN}",
                )

            self._semantics.add_action_to_directive(
                lower_labels,
                "SetMode",
                {"mode": f"{_cover.ATTR_POSITION}.{_cover.STATE_CLOSED}"},
            )
            self._semantics.add_action_to_directive(
                raise_labels,
                "SetMode",
                {"mode": f"{_cover.ATTR_POSITION}.{_cover.STATE_OPEN}"},
            )

            return self._semantics.serialize_semantics()

        return None


class AlexaRangeController(AlexaCapability):
    """Implements Alexa.RangeController.

    The instance property must be unique across ModeController, RangeController, ToggleController
    within the same device.
    The instance property should be a concatenated string of device domain period and single word.
    e.g. fan.speed & fan.direction.

    The instance property must not contain words from other instance property strings within the
    same device.
    e.g. Instance property cover.position & cover.tilt_position will cause the Alexa.Discovery
    directive to fail.

    An instance property string value may be reused for different devices.

    https://developer.amazon.com/docs/device-apis/alexa-rangecontroller.html
    """

    _supported_locales = {
        "de-DE",
        "en-AU",
        "en-CA",
        "en-GB",
        "en-IN",
        "en-US",
        "es-ES",
        "es-MX",
        "es-US",
        "fr-CA",
        "fr-FR",
        "hi-IN",
        "it-IT",
        "ja-JP",
        "pt-BR",
    }

    def __init__(self, entity: core.State, instance: str, non_controllable=False):
        """Initialize the entity."""
        super().__init__(entity, instance)
        self._resource = None
        self._semantics = None
        self._properties_non_controllable = non_controllable

    def name(self):
        """Return the Alexa API name of this interface."""
        return "Alexa.RangeController"

    def properties_supported(self):
        """Return what properties this entity supports."""
        return [{"name": "rangeValue"}]

    def properties_proactively_reported(self):
        """Return True if properties asynchronously reported."""
        return True

    def properties_retrievable(self):
        """Return True if properties can be retrieved."""
        return True

    def get_property(self, name: str):
        """Read and return a property."""
        if name != "rangeValue":
            raise _alexa.UnsupportedProperty(name)

        # Return None for unavailable and unknown states.
        # Allows the Alexa.EndpointHealth Interface to handle the unavailable state
        # in a stateReport.
        if self._entity.state in (_const.STATE_UNAVAILABLE, _const.STATE_UNKNOWN, None):
            return None

        instance = self._instance
        # Cover Position
        if instance == f"{_platform.COVER}.{_cover.ATTR_POSITION}":
            return self._entity.attributes.get(_cover.ATTR_CURRENT_POSITION)

        # Cover Tilt
        if instance == f"{_platform.COVER}.tilt":
            return self._entity.attributes.get(_cover.ATTR_CURRENT_TILT_POSITION)

        # Fan speed percentage
        if instance == f"{_platform.FAN}.{_fan.ATTR_PERCENTAGE}":
            supported = self._entity.attributes.get(_const.ATTR_SUPPORTED_FEATURES, 0)
            if supported and _fan.EntityFeature.SET_SPEED:
                return self._entity.attributes.get(_fan.ATTR_PERCENTAGE)
            return 100 if self._entity.state == _const.STATE_ON else 0

        # Input Number Value
        if instance == f"{_platform.INPUT_NUMBER}.{_input_number.ATTR_VALUE}":
            return float(self._entity.state)

        # Vacuum Fan Speed
        if instance == f"{_platform.VACUUM}.{_vacuum.ATTR_FAN_SPEED}":
            speed_list = self._entity.attributes.get(_vacuum.ATTR_FAN_SPEED_LIST)
            speed = self._entity.attributes.get(_vacuum.ATTR_FAN_SPEED)
            if speed_list is not None and speed is not None:
                speed_index = next(
                    (i for i, v in enumerate(speed_list) if v == speed), None
                )
                return speed_index

        return None

    def configuration(self):
        """Return configuration with presetResources."""
        if isinstance(self._resource, AlexaCapabilityResource):
            return self._resource.serialize_configuration()

        return None

    def capability_resources(self):
        """Return capabilityResources object."""

        instance = self._instance
        # Fan Speed Percentage Resources
        if instance == f"{_platform.FAN}.{_fan.ATTR_PERCENTAGE}":
            percentage_step = self._entity.attributes.get(_fan.ATTR_PERCENTAGE_STEP)
            self._resource = AlexaPresetResource(
                labels=["Percentage", AlexaGlobalCatalog.SETTING_FAN_SPEED],
                min_value=0,
                max_value=100,
                # precision must be a divider of 100 and must be an integer; set step
                # size to 1 for a consistent behavior except for on/off fans
                precision=1 if percentage_step else 100,
                unit=AlexaGlobalCatalog.UNIT_PERCENT,
            )
            return self._resource.serialize_capability_resources()

        # Cover Position Resources
        if instance == f"{_platform.COVER}.{_cover.ATTR_POSITION}":
            self._resource = AlexaPresetResource(
                ["Position", AlexaGlobalCatalog.SETTING_OPENING],
                min_value=0,
                max_value=100,
                precision=1,
                unit=AlexaGlobalCatalog.UNIT_PERCENT,
            )
            return self._resource.serialize_capability_resources()

        # Cover Tilt Resources
        if instance == f"{_platform.COVER}.tilt":
            self._resource = AlexaPresetResource(
                ["Tilt", "Angle", AlexaGlobalCatalog.SETTING_DIRECTION],
                min_value=0,
                max_value=100,
                precision=1,
                unit=AlexaGlobalCatalog.UNIT_PERCENT,
            )
            return self._resource.serialize_capability_resources()

        # Input Number Value
        if instance == f"{_platform.INPUT_NUMBER}.{_input_number.ATTR_VALUE}":
            min_value = float(self._entity.attributes["min"])
            max_value = float(self._entity.attributes["max"])
            precision = float(self._entity.attributes.get("step", 1))
            unit = self._entity.attributes.get(_const.ATTR_UNIT_OF_MEASUREMENT)

            self._resource = AlexaPresetResource(
                ["Value", AlexaGlobalCatalog.SETTING_PRESET],
                min_value=min_value,
                max_value=max_value,
                precision=precision,
                unit=unit,
            )
            self._resource.add_preset(
                value=min_value, labels=[AlexaGlobalCatalog.VALUE_MINIMUM]
            )
            self._resource.add_preset(
                value=max_value, labels=[AlexaGlobalCatalog.VALUE_MAXIMUM]
            )
            return self._resource.serialize_capability_resources()

        # Vacuum Fan Speed Resources
        if instance == f"{_platform.VACUUM}.{_vacuum.ATTR_FAN_SPEED}":
            speed_list = self._entity.attributes[_vacuum.ATTR_FAN_SPEED_LIST]
            max_value = len(speed_list) - 1
            self._resource = AlexaPresetResource(
                labels=[AlexaGlobalCatalog.SETTING_FAN_SPEED],
                min_value=0,
                max_value=max_value,
                precision=1,
            )
            for index, speed in enumerate(speed_list):
                labels = [speed.replace("_", " ")]
                if index == 1:
                    labels.append(AlexaGlobalCatalog.VALUE_MINIMUM)
                if index == max_value:
                    labels.append(AlexaGlobalCatalog.VALUE_MAXIMUM)
                self._resource.add_preset(value=index, labels=labels)

            return self._resource.serialize_capability_resources()

        return None

    def semantics(self):
        """Build and return semantics object."""
        supported = self._entity.attributes.get(_const.ATTR_SUPPORTED_FEATURES, 0)

        instance = self._instance
        # Cover Position
        if instance == f"{_platform.COVER}.{_cover.ATTR_POSITION}":
            lower_labels = [AlexaSemantics.ACTION_LOWER]
            raise_labels = [AlexaSemantics.ACTION_RAISE]
            self._semantics = AlexaSemantics()

            # Add open/close semantics if tilt is not supported.
            if not supported & _cover.EntityFeature.SET_TILT_POSITION:
                lower_labels.append(AlexaSemantics.ACTION_CLOSE)
                raise_labels.append(AlexaSemantics.ACTION_OPEN)
                self._semantics.add_states_to_value(
                    [AlexaSemantics.STATES_CLOSED], value=0
                )
                self._semantics.add_states_to_range(
                    [AlexaSemantics.STATES_OPEN], min_value=1, max_value=100
                )

            self._semantics.add_action_to_directive(
                lower_labels, "SetRangeValue", {"rangeValue": 0}
            )
            self._semantics.add_action_to_directive(
                raise_labels, "SetRangeValue", {"rangeValue": 100}
            )
            return self._semantics.serialize_semantics()

        # Cover Tilt
        if instance == "cover.tilt":
            self._semantics = AlexaSemantics()
            self._semantics.add_action_to_directive(
                [AlexaSemantics.ACTION_CLOSE], "SetRangeValue", {"rangeValue": 0}
            )
            self._semantics.add_action_to_directive(
                [AlexaSemantics.ACTION_OPEN], "SetRangeValue", {"rangeValue": 100}
            )
            self._semantics.add_states_to_value([AlexaSemantics.STATES_CLOSED], value=0)
            self._semantics.add_states_to_range(
                [AlexaSemantics.STATES_OPEN], min_value=1, max_value=100
            )
            return self._semantics.serialize_semantics()

        # Fan Speed Percentage
        if instance == f"{_platform.FAN}.{_fan.ATTR_PERCENTAGE}":
            lower_labels = [AlexaSemantics.ACTION_LOWER]
            raise_labels = [AlexaSemantics.ACTION_RAISE]
            self._semantics = AlexaSemantics()

            self._semantics.add_action_to_directive(
                lower_labels, "SetRangeValue", {"rangeValue": 0}
            )
            self._semantics.add_action_to_directive(
                raise_labels, "SetRangeValue", {"rangeValue": 100}
            )
            return self._semantics.serialize_semantics()

        return None


class AlexaToggleController(AlexaCapability):
    """Implements Alexa.ToggleController.

    The instance property must be unique across ModeController, RangeController, ToggleController
    within the same device.
    The instance property should be a concatenated string of device domain period and single word.
    e.g. fan.speed & fan.direction.

    The instance property must not contain words from other instance property strings within the
    same device.
    e.g. Instance property cover.position & cover.tilt_position will cause the Alexa.Discovery
    directive to fail.

    An instance property string value may be reused for different devices.

    https://developer.amazon.com/docs/device-apis/alexa-togglecontroller.html
    """

    _supported_locales = {
        "de-DE",
        "en-AU",
        "en-CA",
        "en-GB",
        "en-IN",
        "en-US",
        "es-ES",
        "es-MX",
        "es-US",
        "fr-CA",
        "fr-FR",
        "hi-IN",
        "it-IT",
        "ja-JP",
        "pt-BR",
    }

    def __init__(self, entity: core.State, instance: str, non_controllable=False):
        """Initialize the entity."""
        super().__init__(entity, instance)
        self._resource = None
        self._semantics = None
        self._properties_non_controllable = non_controllable

    def name(self):
        """Return the Alexa API name of this interface."""
        return "Alexa.ToggleController"

    def properties_supported(self):
        """Return what properties this entity supports."""
        return [{"name": "toggleState"}]

    def properties_proactively_reported(self):
        """Return True if properties asynchronously reported."""
        return True

    def properties_retrievable(self):
        """Return True if properties can be retrieved."""
        return True

    def get_property(self, name):
        """Read and return a property."""
        if name != "toggleState":
            raise _alexa.UnsupportedProperty(name)

        # Fan Oscillating
        if self._instance == f"{_platform.FAN}.{_fan.ATTR_OSCILLATING}":
            is_on = bool(self._entity.attributes.get(_fan.ATTR_OSCILLATING))
            return "ON" if is_on else "OFF"

        return None

    def capability_resources(self):
        """Return capabilityResources object."""

        # Fan Oscillating Resource
        if self._instance == f"{_platform.FAN}.{_fan.ATTR_OSCILLATING}":
            self._resource = AlexaCapabilityResource(
                [AlexaGlobalCatalog.SETTING_OSCILLATE, "Rotate", "Rotation"]
            )
            return self._resource.serialize_capability_resources()

        return None


class AlexaChannelController(AlexaCapability):
    """Implements Alexa.ChannelController.

    https://developer.amazon.com/docs/device-apis/alexa-channelcontroller.html
    """

    _supported_locales = {
        "ar-SA",
        "de-DE",
        "en-AU",
        "en-CA",
        "en-GB",
        "en-IN",
        "en-US",
        "es-ES",
        "es-MX",
        "es-US",
        "fr-CA",
        "fr-FR",
        "hi-IN",
        "it-IT",
        "ja-JP",
        "pt-BR",
    }

    def name(self):
        """Return the Alexa API name of this interface."""
        return "Alexa.ChannelController"


class AlexaDoorbellEventSource(AlexaCapability):
    """Implements Alexa.DoorbellEventSource.

    https://developer.amazon.com/docs/device-apis/alexa-doorbelleventsource.html
    """

    _supported_locales = {
        "ar-SA",
        "de-DE",
        "en-AU",
        "en-CA",
        "en-GB",
        "en-IN",
        "en-US",
        "es-ES",
        "es-MX",
        "es-US",
        "fr-CA",
        "fr-FR",
        "hi-IN",
        "it-IT",
        "ja-JP",
        "pt-BR",
    }

    def name(self):
        """Return the Alexa API name of this interface."""
        return "Alexa.DoorbellEventSource"

    def capability_proactively_reported(self):
        """Return True for proactively reported capability."""
        return True


class AlexaPlaybackStateReporter(AlexaCapability):
    """Implements Alexa.PlaybackStateReporter.

    https://developer.amazon.com/docs/device-apis/alexa-playbackstatereporter.html
    """

    _supported_locales = {
        "ar-SA",
        "de-DE",
        "en-AU",
        "en-CA",
        "en-GB",
        "en-IN",
        "en-US",
        "es-ES",
        "es-MX",
        "es-US",
        "fr-CA",
        "fr-FR",
        "hi-IN",
        "it-IT",
        "ja-JP",
        "pt-BR",
    }

    def name(self):
        """Return the Alexa API name of this interface."""
        return "Alexa.PlaybackStateReporter"

    def properties_supported(self):
        """Return what properties this entity supports."""
        return [{"name": "playbackState"}]

    def properties_proactively_reported(self):
        """Return True if properties asynchronously reported."""
        return True

    def properties_retrievable(self):
        """Return True if properties can be retrieved."""
        return True

    def get_property(self, name: str):
        """Read and return a property."""
        if name != "playbackState":
            raise _alexa.UnsupportedProperty(name)

        playback_state = self._entity.state
        if playback_state == _const.STATE_PLAYING:
            return {"state": "PLAYING"}
        if playback_state == _const.STATE_PAUSED:
            return {"state": "PAUSED"}

        return {"state": "STOPPED"}


class AlexaSeekController(AlexaCapability):
    """Implements Alexa.SeekController.

    https://developer.amazon.com/docs/device-apis/alexa-seekcontroller.html
    """

    _supported_locales = {
        "ar-SA",
        "de-DE",
        "en-AU",
        "en-CA",
        "en-GB",
        "en-IN",
        "en-US",
        "es-ES",
        "es-MX",
        "es-US",
        "fr-CA",
        "fr-FR",
        "hi-IN",
        "it-IT",
        "ja-JP",
        "pt-BR",
    }

    def name(self):
        """Return the Alexa API name of this interface."""
        return "Alexa.SeekController"


class AlexaEventDetectionSensor(AlexaCapability):
    """Implements Alexa.EventDetectionSensor.

    https://developer.amazon.com/docs/device-apis/alexa-eventdetectionsensor.html
    """

    _supported_locales = {"en-US"}

    def name(self):
        """Return the Alexa API name of this interface."""
        return "Alexa.EventDetectionSensor"

    def properties_supported(self):
        """Return what properties this entity supports."""
        return [{"name": "humanPresenceDetectionState"}]

    def properties_proactively_reported(self):
        """Return True if properties asynchronously reported."""
        return True

    def get_property(self, name: str):
        """Read and return a property."""
        if name != "humanPresenceDetectionState":
            raise _alexa.UnsupportedProperty(name)

        human_presence = "NOT_DETECTED"
        state = self._entity.state

        # Return None for unavailable and unknown states.
        # Allows the Alexa.EndpointHealth Interface to handle the unavailable state
        # in a stateReport.
        if state in (_const.STATE_UNAVAILABLE, _const.STATE_UNKNOWN, None):
            return None

        if self._entity.domain == f"{_platform.IMAGE_PROCESSING}":
            if int(state):
                human_presence = "DETECTED"
        elif state == _const.STATE_ON or self._entity.domain in [
            f"{_platform.INPUT_BUTTON}",
            f"{_platform.BUTTON}",
        ]:
            human_presence = "DETECTED"

        return {"value": human_presence}

    def configuration(self):
        """Return supported detection types."""
        return {
            "detectionMethods": ["AUDIO", "VIDEO"],
            "detectionModes": {
                "humanPresence": {
                    "featureAvailability": "ENABLED",
                    "supportsNotDetected": self._entity.domain
                    not in [f"{_platform.BUTTON}", f"{_platform.INPUT_BUTTON}"],
                }
            },
        }


# pylint: disable=invalid-name
class AlexaEqualizerController(AlexaCapability):
    """Implements Alexa.EqualizerController.

    https://developer.amazon.com/en-US/docs/alexa/device-apis/alexa-equalizercontroller.html
    """

    _supported_locales = {
        "de-DE",
        "en-AU",
        "en-CA",
        "en-GB",
        "en-IN",
        "en-US",
        "es-ES",
        "es-MX",
        "es-US",
        "fr-CA",
        "fr-FR",
        "hi-IN",
        "it-IT",
        "ja-JP",
        "pt-BR",
    }

    VALID_SOUND_MODES: typing.Final = {
        "MOVIE",
        "MUSIC",
        "NIGHT",
        "SPORT",
        "TV",
    }

    def name(self):
        """Return the Alexa API name of this interface."""
        return "Alexa.EqualizerController"

    def properties_supported(self):
        """Return what properties this entity supports.

        Either bands, mode or both can be specified. Only mode is supported at this time.
        """
        return [{"name": "mode"}]

    def properties_retrievable(self):
        """Return True if properties can be retrieved."""
        return True

    def get_property(self, name):
        """Read and return a property."""
        if name != "mode":
            raise _alexa.UnsupportedProperty(name)

        sound_mode = self._entity.attributes.get(_media_player.ATTR_SOUND_MODE)
        if sound_mode and sound_mode.upper() in self.VALID_SOUND_MODES:
            return sound_mode.upper()

        return None

    def configurations(self):
        """Return the sound modes supported in the configurations object."""
        configurations = None
        supported_sound_modes = self.get_valid_inputs(
            self._entity.attributes.get(_media_player.ATTR_SOUND_MODE_LIST, [])
        )
        if supported_sound_modes:
            configurations = {"modes": {"supported": supported_sound_modes}}

        return configurations

    @classmethod
    def get_valid_inputs(cls, sound_mode_list):
        """Return list of supported inputs."""
        input_list = []
        for sound_mode in sound_mode_list:
            sound_mode = sound_mode.upper()

            if sound_mode in cls.VALID_SOUND_MODES:
                input_list.append({"name": sound_mode})

        return input_list


class AlexaTimeHoldController(AlexaCapability):
    """Implements Alexa.TimeHoldController.

    https://developer.amazon.com/docs/device-apis/alexa-timeholdcontroller.html
    """

    _supported_locales = {"en-US"}

    def __init__(self, entity, allow_remote_resume=False):
        """Initialize the entity."""
        super().__init__(entity)
        self._allow_remote_resume = allow_remote_resume

    def name(self):
        """Return the Alexa API name of this interface."""
        return "Alexa.TimeHoldController"

    def configuration(self):
        """Return configuration object.

        Set allowRemoteResume to True if Alexa can restart the operation on the device.
        When false, Alexa does not send the Resume directive.
        """
        return {"allowRemoteResume": self._allow_remote_resume}


class AlexaCameraStreamController(AlexaCapability):
    """Implements Alexa.CameraStreamController.

    https://developer.amazon.com/docs/device-apis/alexa-camerastreamcontroller.html
    """

    _supported_locales = {
        "ar-SA",
        "de-DE",
        "en-AU",
        "en-CA",
        "en-GB",
        "en-IN",
        "en-US",
        "es-ES",
        "es-MX",
        "es-US",
        "fr-CA",
        "fr-FR",
        "hi-IN",
        "it-IT",
        "ja-JP",
        "pt-BR",
    }

    def name(self):
        """Return the Alexa API name of this interface."""
        return "Alexa.CameraStreamController"

    def camera_stream_configurations(self):
        """Return cameraStreamConfigurations object."""
        return [
            {
                "protocols": ["HLS"],
                "resolutions": [{"width": 1280, "height": 720}],
                "authorizationTypes": ["NONE"],
                "videoCodecs": ["H264"],
                "audioCodecs": ["AAC"],
            }
        ]
