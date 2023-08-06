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

import enum
import logging
import typing

from ... import core
from ...backports import strenum
from .alexa_entity import AlexaEntity
from .capabilities import (
    Alexa,
    AlexaBrightnessController,
    AlexaCameraStreamController,
    AlexaChannelController,
    AlexaColorController,
    AlexaColorTemperatureController,
    AlexaContactSensor,
    AlexaDoorbellEventSource,
    AlexaEndpointHealth,
    AlexaEqualizerController,
    AlexaEventDetectionSensor,
    AlexaInputController,
    AlexaLockController,
    AlexaModeController,
    AlexaMotionSensor,
    AlexaPlaybackController,
    AlexaPlaybackStateReporter,
    AlexaPowerController,
    AlexaRangeController,
    AlexaSceneController,
    AlexaSecurityPanelController,
    AlexaSeekController,
    AlexaSpeaker,
    AlexaStepSpeaker,
    AlexaTemperatureSensor,
    AlexaThermostatController,
    AlexaTimeHoldController,
    AlexaToggleController,
)

_const: typing.TypeAlias = core.Const
_alexa: typing.TypeAlias = core.Alexa
_binary_sensor: typing.TypeAlias = core.BinarySensor
_camera: typing.TypeAlias = core.Camera
_climate: typing.TypeAlias = core.Climate
_cover: typing.TypeAlias = core.Cover
_fan: typing.TypeAlias = core.Fan
_light: typing.TypeAlias = core.Light
_media_player: typing.TypeAlias = core.MediaPlayer
_platform: typing.TypeAlias = core.Platform
_switch: typing.TypeAlias = core.Switch
_vacuum: typing.TypeAlias = core.Vacuum

_ENTITY_ADAPTERS: typing.Final[core.Registry[str, type[AlexaEntity]]] = core.Registry()
_LOGGER: typing.Final = logging.getLogger(__name__)


# pylint: disable=unused-variable
class DisplayCategory(strenum.UppercaseStrEnum):
    """Possible display categories for Discovery response.

    https://developer.amazon.com/docs/device-apis/alexa-discovery.html#display-categories
    """

    # Describes a combination of devices set to a specific state, when the
    # state change must occur in a specific order. For example, a "watch
    # Netflix" scene might require the: 1. TV to be powered on & 2. Input set
    # to HDMI1. Applies to Scenes
    ACTIVITY_TRIGGER = enum.auto()

    # Indicates a device that emits pleasant odors and masks unpleasant odors in interior spaces.
    AIR_FRESHENER = enum.auto()

    # Indicates a device that improves the quality of air in interior spaces.
    AIR_PURIFIER = enum.auto()

    # Indicates a smart device in an automobile, such as a dash camera.
    AUTO_ACCESSORY = enum.auto()

    # Indicates a security device with video or photo functionality.
    CAMERA = enum.auto()

    # Indicates a religious holiday decoration that often contains lights.
    CHRISTMAS_TREE = enum.auto()

    # Indicates a device that makes coffee.
    COFFEE_MAKER = enum.auto()

    # Indicates a non-mobile computer, such as a desktop computer.
    COMPUTER = enum.auto()

    # Indicates an endpoint that detects and reports contact.
    CONTACT_SENSOR = enum.auto()

    # Indicates a door.
    DOOR = enum.auto()

    # Indicates a doorbell.
    DOORBELL = enum.auto()

    # Indicates a window covering on the outside of a structure.
    EXTERIOR_BLIND = enum.auto()

    # Indicates a fan.
    FAN = enum.auto()

    # Indicates a game console, such as Microsoft Xbox or Nintendo Switch
    GAME_CONSOLE = enum.auto()

    # Indicates a garage door.
    # Garage doors must implement the ModeController interface to open and close the door.
    GARAGE_DOOR = enum.auto()

    # Indicates a wearable device that transmits audio directly into the ear.
    HEADPHONES = enum.auto()

    # Indicates a smart-home hub.
    HUB = enum.auto()

    # Indicates a window covering on the inside of a structure.
    INTERIOR_BLIND = enum.auto()

    # Indicates a laptop or other mobile computer.
    LAPTOP = enum.auto()

    # Indicates light sources or fixtures.
    LIGHT = enum.auto()

    # Indicates a microwave oven.
    MICROWAVE = enum.auto()

    # Indicates a mobile phone.
    MOBILE_PHONE = enum.auto()

    # Indicates an endpoint that detects and reports motion.
    MOTION_SENSOR = enum.auto()

    # Indicates a network-connected music system.
    MUSIC_SYSTEM = enum.auto()

    # Indicates a network router.
    NETWORK_HARDWARE = enum.auto()

    # An endpoint that cannot be described in on of the other categories.
    OTHER = enum.auto()

    # Indicates an oven cooking appliance.
    OVEN = enum.auto()

    # Indicates a non-mobile phone, such as landline or an IP phone.
    PHONE = enum.auto()

    # Indicates a device that prints.
    PRINTER = enum.auto()

    # Indicates a network router.
    ROUTER = enum.auto()

    # Describes a combination of devices set to a specific state, when the
    # order of the state change is not important. For example a bedtime scene
    # might include turning off lights and lowering the thermostat, but the
    # order is unimportant.    Applies to Scenes
    SCENE_TRIGGER = enum.auto()

    # Indicates a projector screen.
    SCREEN = enum.auto()

    # Indicates a security panel.
    SECURITY_PANEL = enum.auto()

    # Indicates a security system.
    SECURITY_SYSTEM = enum.auto()

    # Indicates an electric cooking device that sits on a countertop, cooks at low temperatures,
    # and is often shaped like a cooking pot.
    SLOW_COOKER = enum.auto()

    # Indicates an endpoint that locks.
    SMARTLOCK = enum.auto()

    # Indicates modules that are plugged into an existing electrical outlet.
    # Can control a variety of devices.
    SMARTPLUG = enum.auto()

    # Indicates the endpoint is a speaker or speaker system.
    SPEAKER = enum.auto()

    # Indicates a streaming device such as Apple TV, Chromecast, or Roku.
    STREAMING_DEVICE = enum.auto()

    # Indicates in-wall switches wired to the electrical system.  Can control a
    # variety of devices.
    SWITCH = enum.auto()

    # Indicates a tablet computer.
    TABLET = enum.auto()

    # Indicates endpoints that report the temperature only.
    TEMPERATURE_SENSOR = enum.auto()

    # Indicates endpoints that control temperature, stand-alone air
    # conditioners, or heaters with direct temperature control.
    THERMOSTAT = enum.auto()

    # Indicates the endpoint is a television.
    TV = enum.auto()

    # Indicates a vacuum cleaner.
    VACUUM_CLEANER = enum.auto()

    # Indicates a network-connected wearable device,
    #  such as an Apple Watch, Fitbit, or Samsung Gear.
    WEARABLE = enum.auto()


@_ENTITY_ADAPTERS.register(_platform.ALERT)
@_ENTITY_ADAPTERS.register(_platform.AUTOMATION)
@_ENTITY_ADAPTERS.register(_platform.GROUP)
class Generic(AlexaEntity):
    """A generic, on/off device.

    The choice of last resort.
    """

    @property
    def default_display_categories(self):
        """Return the display categories for this entity."""
        if self._entity.domain == _platform.AUTOMATION:
            return [DisplayCategory.ACTIVITY_TRIGGER]

        return [DisplayCategory.OTHER]

    @property
    def interfaces(self):
        """Yield the supported interfaces."""
        return [
            AlexaPowerController(self._entity),
            AlexaEndpointHealth(self._entity),
            Alexa(self._entity),
        ]


@_ENTITY_ADAPTERS.register(_platform.INPUT_BOOLEAN)
@_ENTITY_ADAPTERS.register(_platform.SWITCH)
class Switch(AlexaEntity):
    """Class to represent Switch capabilities."""

    @property
    def default_display_categories(self):
        """Return the display categories for this entity."""
        if self._entity.domain == "input_boolean":
            return [DisplayCategory.OTHER]

        device_class = self._entity.attributes.get(_const.ATTR_DEVICE_CLASS)
        if device_class == _switch.DeviceClass.OUTLET:
            return [DisplayCategory.SMARTPLUG]

        return [DisplayCategory.SWITCH]

    @property
    def interfaces(self):
        """Yield the supported interfaces."""
        return [
            AlexaPowerController(self._entity),
            AlexaContactSensor(self._entity),
            AlexaEndpointHealth(self._entity),
            Alexa(self._entity),
        ]


@_ENTITY_ADAPTERS.register(_platform.BUTTON)
@_ENTITY_ADAPTERS.register(_platform.INPUT_BUTTON)
class Button(AlexaEntity):
    """Class to represent Button capabilities."""

    @property
    def default_display_categories(self):
        """Return the display categories for this entity."""
        return [DisplayCategory.ACTIVITY_TRIGGER]

    @property
    def interfaces(self):
        """Yield the supported interfaces."""
        return [
            AlexaSceneController(self._entity, supports_deactivation=False),
            AlexaEventDetectionSensor(self._entity),
            AlexaEndpointHealth(self._entity),
            Alexa(self._entity),
        ]


@_ENTITY_ADAPTERS.register(_platform.CLIMATE)
class Climate(AlexaEntity):
    """Class to represent Climate capabilities."""

    @property
    def default_display_categories(self):
        """Return the display categories for this entity."""
        return [DisplayCategory.THERMOSTAT]

    @property
    def interfaces(self):
        """Yield the supported interfaces."""
        # If we support two modes, one being off, we allow turning on too.
        if _climate.HVACMode.OFF in self._entity.attributes.get(
            _climate.ATTR_HVAC_MODES, []
        ):
            yield AlexaPowerController(self._entity)

        yield AlexaThermostatController(self._shc, self._entity)
        yield AlexaTemperatureSensor(self._shc, self._entity)
        yield AlexaEndpointHealth(self._entity)
        yield Alexa(self._entity)


@_ENTITY_ADAPTERS.register(_platform.COVER)
class Cover(AlexaEntity):
    """Class to represent Cover capabilities."""

    @property
    def default_display_categories(self):
        """Return the display categories for this entity."""
        device_class = self._entity.attributes.get(_const.ATTR_DEVICE_CLASS)
        if device_class in (_cover.DeviceClass.GARAGE, _cover.DeviceClass.GATE):
            return [DisplayCategory.GARAGE_DOOR]
        if device_class == _cover.DeviceClass.DOOR:
            return [DisplayCategory.DOOR]
        if device_class in (
            _cover.DeviceClass.BLIND,
            _cover.DeviceClass.SHADE,
            _cover.DeviceClass.CURTAIN,
        ):
            return [DisplayCategory.INTERIOR_BLIND]
        if device_class in (
            _cover.DeviceClass.WINDOW,
            _cover.DeviceClass.AWNING,
            _cover.DeviceClass.SHUTTER,
        ):
            return [DisplayCategory.EXTERIOR_BLIND]

        return [DisplayCategory.OTHER]

    @property
    def interfaces(self):
        """Yield the supported interfaces."""
        device_class = self._entity.attributes.get(_const.ATTR_DEVICE_CLASS)
        if device_class not in (
            _cover.DeviceClass.GARAGE,
            _cover.DeviceClass.GATE,
        ):
            yield AlexaPowerController(self._entity)

        supported = self._entity.attributes.get(_const.ATTR_SUPPORTED_FEATURES, 0)
        if supported & _cover.EntityFeature.SET_POSITION:
            yield AlexaRangeController(
                self._entity, instance=f"cover.{_cover.ATTR_POSITION}"
            )
        elif supported & (_cover.EntityFeature.CLOSE | _cover.EntityFeature.OPEN):
            yield AlexaModeController(
                self._entity, instance=f"cover.{_cover.ATTR_POSITION}"
            )
        if supported & _cover.EntityFeature.SET_TILT_POSITION:
            yield AlexaRangeController(self._entity, instance="cover.tilt")
        yield AlexaEndpointHealth(self._entity)
        yield Alexa(self._entity)


@_ENTITY_ADAPTERS.register(_platform.LIGHT)
class Light(AlexaEntity):
    """Class to represent Light capabilities."""

    @property
    def default_display_categories(self):
        """Return the display categories for this entity."""
        return [DisplayCategory.LIGHT]

    @property
    def interfaces(self):
        """Yield the supported interfaces."""
        yield AlexaPowerController(self._entity)

        color_modes = self._entity.attributes.get(_light.ATTR_SUPPORTED_COLOR_MODES)
        if _light.brightness_supported(color_modes):
            yield AlexaBrightnessController(self._entity)
        if _light.color_supported(color_modes):
            yield AlexaColorController(self._entity)
        if _light.color_temp_supported(color_modes):
            yield AlexaColorTemperatureController(self._entity)

        yield AlexaEndpointHealth(self._entity)
        yield Alexa(self._entity)


@_ENTITY_ADAPTERS.register(_platform.FAN)
class Fan(AlexaEntity):
    """Class to represent Fan capabilities."""

    @property
    def default_display_categories(self):
        """Return the display categories for this entity."""
        return [DisplayCategory.FAN]

    @property
    def interfaces(self):
        """Yield the supported interfaces."""
        yield AlexaPowerController(self._entity)
        force_range_controller = True
        supported = self._entity.attributes.get(_const.ATTR_SUPPORTED_FEATURES, 0)
        if supported & _fan.EntityFeature.OSCILLATE:
            yield AlexaToggleController(
                self._entity, instance=f"fan.{_fan.ATTR_OSCILLATING}"
            )
            force_range_controller = False
        if supported & _fan.EntityFeature.PRESET_MODE:
            yield AlexaModeController(
                self._entity, instance=f"fan.{_fan.ATTR_PRESET_MODE}"
            )
            force_range_controller = False
        if supported & _fan.EntityFeature.DIRECTION:
            yield AlexaModeController(
                self._entity, instance=f"fan.{_fan.ATTR_DIRECTION}"
            )
            force_range_controller = False

        # AlexaRangeController controls the Fan Speed Percentage.
        # For fans which only support on/off, no controller is added. This makes the
        # fan impossible to turn on or off through Alexa, most likely due to a bug in Alexa.
        # As a workaround, we add a range controller which can only be set to 0% or 100%.
        if force_range_controller or supported & _fan.EntityFeature.SET_SPEED:
            yield AlexaRangeController(
                self._entity, instance=f"fan.{_fan.ATTR_PERCENTAGE}"
            )

        yield AlexaEndpointHealth(self._entity)
        yield Alexa(self._entity)


@_ENTITY_ADAPTERS.register(_platform.LOCK)
class Lock(AlexaEntity):
    """Class to represent Lock capabilities."""

    @property
    def default_display_categories(self):
        """Return the display categories for this entity."""
        return [DisplayCategory.SMARTLOCK]

    @property
    def interfaces(self):
        """Yield the supported interfaces."""
        return [
            AlexaLockController(self._entity),
            AlexaEndpointHealth(self._entity),
            Alexa(self._entity),
        ]


@_ENTITY_ADAPTERS.register(_platform.MEDIA_PLAYER)
class MediaPlayer(AlexaEntity):
    """Class to represent MediaPlayer capabilities."""

    @property
    def default_display_categories(self):
        """Return the display categories for this entity."""
        device_class = self._entity.attributes.get(_const.ATTR_DEVICE_CLASS)
        if device_class == _media_player.DeviceClass.SPEAKER:
            return [DisplayCategory.SPEAKER]

        return [DisplayCategory.TV]

    @property
    def interfaces(self):
        """Yield the supported interfaces."""
        yield AlexaPowerController(self._entity)

        supported = self._entity.attributes.get(_const.ATTR_SUPPORTED_FEATURES, 0)
        if supported & _media_player.EntityFeature.VOLUME_SET:
            yield AlexaSpeaker(self._entity)
        elif supported & _media_player.EntityFeature.VOLUME_STEP:
            yield AlexaStepSpeaker(self._entity)

        playback_features = (
            _media_player.EntityFeature.PLAY
            | _media_player.EntityFeature.PAUSE
            | _media_player.EntityFeature.STOP
            | _media_player.EntityFeature.NEXT_TRACK
            | _media_player.EntityFeature.PREVIOUS_TRACK
        )
        if supported & playback_features:
            yield AlexaPlaybackController(self._entity)
            yield AlexaPlaybackStateReporter(self._entity)

        if supported & _media_player.EntityFeature.SEEK:
            yield AlexaSeekController(self._entity)

        if supported & _media_player.EntityFeature.SELECT_SOURCE:
            inputs = AlexaInputController.get_valid_inputs(
                self._entity.attributes.get(_media_player.ATTR_INPUT_SOURCE_LIST, [])
            )
            if len(inputs) > 0:
                yield AlexaInputController(self._entity)

        if supported & _media_player.EntityFeature.PLAY_MEDIA:
            yield AlexaChannelController(self._entity)

        # AlexaEqualizerController is disabled for denonavr
        # since it blocks alexa from discovering any devices.
        domain = self._shc.entity_sources.get(self.entity_id, {}).get("domain")
        if (
            supported & _media_player.EntityFeature.SELECT_SOUND_MODE
            and domain != "denonavr"
        ):
            inputs = AlexaEqualizerController.get_valid_inputs(
                self._entity.attributes.get(_media_player.ATTR_SOUND_MODE_LIST, [])
            )
            if len(inputs) > 0:
                yield AlexaEqualizerController(self._entity)

        yield AlexaEndpointHealth(self._entity)
        yield Alexa(self._entity)


@_ENTITY_ADAPTERS.register(_platform.SCENE)
class Scene(AlexaEntity):
    """Class to represent Scene capabilities."""

    @property
    def default_display_categories(self):
        """Return the display categories for this entity."""
        return [DisplayCategory.SCENE_TRIGGER]

    @property
    def interfaces(self):
        """Yield the supported interfaces."""
        return [
            AlexaSceneController(self._entity, supports_deactivation=False),
            Alexa(self._entity),
        ]


@_ENTITY_ADAPTERS.register(_platform.SCRIPT)
class Script(AlexaEntity):
    """Class to represent Script capabilities."""

    @property
    def default_display_categories(self):
        """Return the display categories for this entity."""
        return [DisplayCategory.ACTIVITY_TRIGGER]

    @property
    def interfaces(self):
        """Yield the supported interfaces."""
        return [
            AlexaSceneController(self._entity, supports_deactivation=False),
            Alexa(self._entity),
        ]


@_ENTITY_ADAPTERS.register(_platform.SENSOR)
class Sensor(AlexaEntity):
    """Class to represent Sensor capabilities."""

    @property
    def default_display_categories(self):
        """Return the display categories for this entity."""
        # although there are other kinds of sensors, all but temperature
        # sensors are currently ignored.
        return [DisplayCategory.TEMPERATURE_SENSOR]

    @property
    def interfaces(self):
        """Yield the supported interfaces."""
        attrs = self._entity.attributes
        if attrs.get(_const.ATTR_UNIT_OF_MEASUREMENT) in (
            _const.UnitOfTemperature.FAHRENHEIT,
            _const.UnitOfTemperature.CELSIUS,
        ):
            yield AlexaTemperatureSensor(self._shc, self._entity)
            yield AlexaEndpointHealth(self._entity)
            yield Alexa(self._entity)


@_ENTITY_ADAPTERS.register(_platform.BINARY_SENSOR)
class BinarySensor(AlexaEntity):
    """Class to represent BinarySensor capabilities."""

    # pylint: disable=invalid-name
    TYPE_CONTACT: typing.Final = "contact"
    TYPE_MOTION: typing.Final = "motion"
    TYPE_PRESENCE: typing.Final = "presence"

    @property
    def default_display_categories(self):
        """Return the display categories for this entity."""
        sensor_type = self.get_type()
        if sensor_type is self.TYPE_CONTACT:
            return [DisplayCategory.CONTACT_SENSOR]
        if sensor_type is self.TYPE_MOTION:
            return [DisplayCategory.MOTION_SENSOR]
        if sensor_type is self.TYPE_PRESENCE:
            return [DisplayCategory.CAMERA]
        return ""

    @property
    def interfaces(self):
        """Yield the supported interfaces."""
        sensor_type = self.get_type()
        if sensor_type is self.TYPE_CONTACT:
            yield AlexaContactSensor(self._entity)
        elif sensor_type is self.TYPE_MOTION:
            yield AlexaMotionSensor(self._entity)
        elif sensor_type is self.TYPE_PRESENCE:
            yield AlexaEventDetectionSensor(self._entity)

        # yield additional interfaces based on specified display category in config.
        entity_conf = self._config.entity_config.get(self._entity.entity_id, {})
        if _alexa.CONF_DISPLAY_CATEGORIES in entity_conf:
            display_categories = entity_conf[_alexa.CONF_DISPLAY_CATEGORIES]
            if display_categories == DisplayCategory.DOORBELL:
                yield AlexaDoorbellEventSource(self._entity)
            elif display_categories == DisplayCategory.CONTACT_SENSOR:
                yield AlexaContactSensor(self._entity)
            elif display_categories == DisplayCategory.MOTION_SENSOR:
                yield AlexaMotionSensor(self._entity)
            elif display_categories == DisplayCategory.CAMERA:
                yield AlexaEventDetectionSensor(self._entity)

        yield AlexaEndpointHealth(self._entity)
        yield Alexa(self._entity)

    def get_type(self):
        """Return the type of binary sensor."""
        attrs = self._entity.attributes
        device_class = attrs.get(_const.ATTR_DEVICE_CLASS)
        if device_class in (
            _binary_sensor.DeviceClass.DOOR,
            _binary_sensor.DeviceClass.GARAGE_DOOR,
            _binary_sensor.DeviceClass.OPENING,
            _binary_sensor.DeviceClass.WINDOW,
        ):
            return self.TYPE_CONTACT

        if device_class == _binary_sensor.DeviceClass.MOTION:
            return self.TYPE_MOTION

        if device_class == _binary_sensor.DeviceClass.PRESENCE:
            return self.TYPE_PRESENCE
        return ""


@_ENTITY_ADAPTERS.register(_platform.ALARM_CONTROL_PANEL)
class AlarmControlPanel(AlexaEntity):
    """Class to represent Alarm capabilities."""

    @property
    def default_display_categories(self):
        """Return the display categories for this entity."""
        return [DisplayCategory.SECURITY_PANEL]

    @property
    def interfaces(self):
        """Yield the supported interfaces."""
        if not self._entity.attributes.get("code_arm_required"):
            yield AlexaSecurityPanelController(self._entity)
            yield AlexaEndpointHealth(self._entity)
            yield Alexa(self._entity)


@_ENTITY_ADAPTERS.register(_platform.IMAGE_PROCESSING)
class ImageProcessingEntity(AlexaEntity):
    """Class to represent image_processing capabilities."""

    @property
    def default_display_categories(self):
        """Return the display categories for this entity."""
        return [DisplayCategory.CAMERA]

    @property
    def interfaces(self):
        """Yield the supported interfaces."""
        yield AlexaEventDetectionSensor(self._entity)
        yield AlexaEndpointHealth(self._entity)
        yield Alexa(self._entity)


@_ENTITY_ADAPTERS.register(_platform.INPUT_NUMBER)
class InputNumber(AlexaEntity):
    """Class to represent input_number capabilities."""

    @property
    def default_display_categories(self):
        """Return the display categories for this entity."""
        return [DisplayCategory.OTHER]

    @property
    def interfaces(self):
        """Yield the supported interfaces."""

        yield AlexaRangeController(self._entity, instance="input_number.value")
        yield AlexaEndpointHealth(self._entity)
        yield Alexa(self._entity)


@_ENTITY_ADAPTERS.register(_platform.TIMER)
class Timer(AlexaEntity):
    """Class to represent Timer capabilities."""

    @property
    def default_display_categories(self):
        """Return the display categories for this entity."""
        return [DisplayCategory.OTHER]

    @property
    def interfaces(self):
        """Yield the supported interfaces."""
        yield AlexaTimeHoldController(self._entity, allow_remote_resume=True)
        yield AlexaPowerController(self._entity)
        yield Alexa(self._entity)


@_ENTITY_ADAPTERS.register(_platform.VACUUM)
class Vacuum(AlexaEntity):
    """Class to represent vacuum capabilities."""

    @property
    def default_display_categories(self):
        """Return the display categories for this entity."""
        return [DisplayCategory.VACUUM_CLEANER]

    @property
    def interfaces(self):
        """Yield the supported interfaces."""
        supported = self._entity.attributes.get(_const.ATTR_SUPPORTED_FEATURES, 0)
        if (
            (supported & _vacuum.EntityFeature.TURN_ON)
            or (supported & _vacuum.EntityFeature.START)
        ) and (
            (supported & _vacuum.EntityFeature.TURN_OFF)
            or (supported & _vacuum.EntityFeature.RETURN_HOME)
        ):
            yield AlexaPowerController(self._entity)

        if supported & _vacuum.EntityFeature.FAN_SPEED:
            yield AlexaRangeController(
                self._entity, instance=f"vacuum.{_vacuum.ATTR_FAN_SPEED}"
            )

        if supported & _vacuum.EntityFeature.PAUSE:
            support_resume = bool(supported & _vacuum.EntityFeature.START)
            yield AlexaTimeHoldController(
                self._entity, allow_remote_resume=support_resume
            )

        yield AlexaEndpointHealth(self._entity)
        yield Alexa(self._entity)


@_ENTITY_ADAPTERS.register(_platform.CAMERA)
class Camera(AlexaEntity):
    """Class to represent Camera capabilities."""

    @property
    def default_display_categories(self):
        """Return the display categories for this entity."""
        return [DisplayCategory.CAMERA]

    @property
    def interfaces(self):
        """Yield the supported interfaces."""
        if self._check_requirements():
            supported = self._entity.attributes.get(_const.ATTR_SUPPORTED_FEATURES, 0)
            if supported & _camera.EntityFeature.STREAM:
                yield AlexaCameraStreamController(self._entity)

        yield AlexaEndpointHealth(self._entity)
        yield Alexa(self._entity)

    def _check_requirements(self):
        """Check the hass URL for HTTPS scheme."""
        if "stream" not in self._shc.config.components:
            _LOGGER.debug(
                f"{self.entity_id} requires stream component for AlexaCameraStreamController",
                self.entity_id,
            )
            return False

        try:
            self._shc.get_url(
                allow_internal=False,
                allow_ip=False,
                require_ssl=True,
                require_standard_port=True,
            )
        except core.NoURLAvailableError:
            _LOGGER.debug(
                f"{self.entity_id} requires HTTPS for AlexaCameraStreamController"
            )
            return False

        return True
