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

import collections
import typing

from . import (
    abstract_alexa_config,
    alexa_capability,
    alexa_component,
    alexa_config_store,
    alexa_entity,
    alexa_errors,
    alexa_intents,
)
from .climate import Climate as _climate
from .alexa_errors import _API_TEMP_UNITS


# pylint: disable=unused-variable, invalid-name
class Alexa:
    """Alexa namespace"""

    AbstractConfig: typing.TypeAlias = abstract_alexa_config.AbstractAlexaConfig
    Capability: typing.TypeAlias = alexa_capability.AlexaCapability
    Component: typing.TypeAlias = alexa_component.AlexaComponent
    ConfigStore: typing.TypeAlias = alexa_config_store.AlexaConfigStore
    Entity: typing.TypeAlias = alexa_entity.AlexaEntity

    # ----------------- Errors ----------------------------
    NoTokenAvailable: typing.TypeAlias = alexa_errors.NoTokenAvailable
    RequireRelink: typing.TypeAlias = alexa_errors.RequireRelink
    UnsupportedInterface: typing.TypeAlias = alexa_errors.UnsupportedInterface
    UnsupportedProperty: typing.TypeAlias = alexa_errors.UnsupportedProperty
    Error: typing.TypeAlias = alexa_errors.AlexaError
    InvalidEndpointError: typing.TypeAlias = alexa_errors.AlexaInvalidEndpointError
    InvalidValueError: typing.TypeAlias = alexa_errors.AlexaInvalidValueError
    InternalError: typing.TypeAlias = alexa_errors.AlexaInternalError
    NotSupportedInCurrentMode: typing.TypeAlias = (
        alexa_errors.AlexaNotSupportedInCurrentMode
    )
    UnsupportedThermostatModeError: typing.TypeAlias = (
        alexa_errors.AlexaUnsupportedThermostatModeError
    )
    TempRangeError: typing.TypeAlias = alexa_errors.AlexaTempRangeError
    BridgeUnreachableError: typing.TypeAlias = alexa_errors.AlexaBridgeUnreachableError
    SecurityPanelUnauthorizedError: typing.TypeAlias = (
        alexa_errors.AlexaSecurityPanelUnauthorizedError
    )
    SecurityPanelAuthorizationRequired: typing.TypeAlias = (
        alexa_errors.AlexaSecurityPanelAuthorizationRequired
    )
    AlreadyInOperationError: typing.TypeAlias = (
        alexa_errors.AlexaAlreadyInOperationError
    )
    InvalidDirectiveError: typing.TypeAlias = alexa_errors.AlexaInvalidDirectiveError
    VideoActionNotPermittedForContentError: typing.TypeAlias = (
        alexa_errors.AlexaVideoActionNotPermittedForContentError
    )

    # ---------------------- Const ----------------------------------------------

    EVENT_ALEXA_SMART_HOME: typing.Final = "alexa_smart_home"

    # Flash briefing constants
    CONF_UID: typing.Final = "uid"
    CONF_TITLE: typing.Final = "title"
    CONF_AUDIO: typing.Final = "audio"
    CONF_TEXT: typing.Final = "text"
    CONF_DISPLAY_URL: typing.Final = "display_url"

    CONF_FILTER: typing.Final = "filter"
    CONF_ENTITY_CONFIG: typing.Final = "entity_config"
    CONF_ENDPOINT: typing.Final = "endpoint"
    CONF_LOCALE: typing.Final = "locale"

    ATTR_UID: typing.Final = "uid"
    ATTR_UPDATE_DATE: typing.Final = "updateDate"
    ATTR_TITLE_TEXT: typing.Final = "titleText"
    ATTR_STREAM_URL: typing.Final = "streamUrl"
    ATTR_MAIN_TEXT: typing.Final = "mainText"
    ATTR_REDIRECTION_URL: typing.Final = "redirectionURL"

    SYN_RESOLUTION_MATCH: typing.Final = "ER_SUCCESS_MATCH"

    # Alexa requires timestamps to be formatted according to ISO 8601, YYYY-MM-DDThh:mm:ssZ
    # https://developer.amazon.com/es-ES/docs/alexa/device-apis/alexa-scenecontroller.html#activate-response-event
    DATE_FORMAT: typing.Final = "%Y-%m-%dT%H:%M:%SZ"

    API_DIRECTIVE: typing.Final = "directive"
    API_ENDPOINT: typing.Final = "endpoint"
    API_EVENT: typing.Final = "event"
    API_CONTEXT: typing.Final = "context"
    API_HEADER: typing.Final = "header"
    API_PAYLOAD: typing.Final = "payload"
    API_SCOPE: typing.Final = "scope"
    API_CHANGE: typing.Final = "change"
    API_PASSWORD: typing.Final = "password"

    CONF_DISPLAY_CATEGORIES: typing.Final = "display_categories"
    CONF_SUPPORTED_LOCALES: typing.Final = (
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
    )
    API_TEMP_UNITS = _API_TEMP_UNITS

    # Needs to be ordered dict for `async_api_set_thermostat_mode` which does a
    # reverse mapping of this dict and we want to map the first occurrence of OFF
    # back to HA state.
    API_THERMOSTAT_MODES: typing.Final = collections.OrderedDict(
        [
            (_climate.HVACMode.HEAT, "HEAT"),
            (_climate.HVACMode.COOL, "COOL"),
            (_climate.HVACMode.HEAT_COOL, "AUTO"),
            (_climate.HVACMode.AUTO, "AUTO"),
            (_climate.HVACMode.OFF, "OFF"),
            (_climate.HVACMode.FAN_ONLY, "CUSTOM"),
            (_climate.HVACMode.DRY, "CUSTOM"),
        ]
    )
    API_THERMOSTAT_MODES_CUSTOM: typing.Final = {
        _climate.HVACMode.DRY: "DEHUMIDIFY",
        _climate.HVACMode.FAN_ONLY: "FAN",
    }
    API_THERMOSTAT_PRESETS: typing.Final = {_climate.PRESET_ECO: "ECO"}

    # AlexaModeController does not like a single mode for the fan preset,
    # we add PRESET_MODE_NA if a fan has only one preset_mode
    PRESET_MODE_NA: typing.Final = "-"

    class Cause:
        """Possible causes for property changes.

        https://developer.amazon.com/docs/smarthome/state-reporting-for-a-smart-home-skill.html#cause-object
        """

        # Indicates that the event was caused by a customer interaction with an
        # application. For example, a customer switches on a light, or locks a door
        # using the Alexa app or an app provided by a device vendor.
        APP_INTERACTION: typing.Final = "APP_INTERACTION"

        # Indicates that the event was caused by a physical interaction with an
        # endpoint. For example manually switching on a light or manually locking a
        # door lock
        PHYSICAL_INTERACTION: typing.Final = "PHYSICAL_INTERACTION"

        # Indicates that the event was caused by the periodic poll of an appliance,
        # which found a change in value. For example, you might poll a temperature
        # sensor every hour, and send the updated temperature to Alexa.
        PERIODIC_POLL: typing.Final = "PERIODIC_POLL"

        # Indicates that the event was caused by the application of a device rule.
        # For example, a customer configures a rule to switch on a light if a
        # motion sensor detects motion. In this case, Alexa receives an event from
        # the motion sensor, and another event from the light to indicate that its
        # state change was caused by the rule.
        RULE_TRIGGER: typing.Final = "RULE_TRIGGER"

        # Indicates that the event was caused by a voice interaction with Alexa.
        # For example a user speaking to their Echo device.
        VOICE_INTERACTION: typing.Final = "VOICE_INTERACTION"

    class Inputs:
        """Valid names for the InputController.

        https://developer.amazon.com/docs/device-apis/alexa-property-schemas.html#input
        """

        VALID_SOURCE_NAME_MAP: typing.Final = {
            "antenna": "TUNER",
            "antennatv": "TUNER",
            "aux": "AUX 1",
            "aux1": "AUX 1",
            "aux2": "AUX 2",
            "aux3": "AUX 3",
            "aux4": "AUX 4",
            "aux5": "AUX 5",
            "aux6": "AUX 6",
            "aux7": "AUX 7",
            "bluray": "BLURAY",
            "blurayplayer": "BLURAY",
            "cable": "CABLE",
            "cd": "CD",
            "coax": "COAX 1",
            "coax1": "COAX 1",
            "coax2": "COAX 2",
            "composite": "COMPOSITE 1",
            "composite1": "COMPOSITE 1",
            "dvd": "DVD",
            "game": "GAME",
            "gameconsole": "GAME",
            "hdradio": "HD RADIO",
            "hdmi": "HDMI 1",
            "hdmi1": "HDMI 1",
            "hdmi2": "HDMI 2",
            "hdmi3": "HDMI 3",
            "hdmi4": "HDMI 4",
            "hdmi5": "HDMI 5",
            "hdmi6": "HDMI 6",
            "hdmi7": "HDMI 7",
            "hdmi8": "HDMI 8",
            "hdmi9": "HDMI 9",
            "hdmi10": "HDMI 10",
            "hdmiarc": "HDMI ARC",
            "input": "INPUT 1",
            "input1": "INPUT 1",
            "input2": "INPUT 2",
            "input3": "INPUT 3",
            "input4": "INPUT 4",
            "input5": "INPUT 5",
            "input6": "INPUT 6",
            "input7": "INPUT 7",
            "input8": "INPUT 8",
            "input9": "INPUT 9",
            "input10": "INPUT 10",
            "ipod": "IPOD",
            "line": "LINE 1",
            "line1": "LINE 1",
            "line2": "LINE 2",
            "line3": "LINE 3",
            "line4": "LINE 4",
            "line5": "LINE 5",
            "line6": "LINE 6",
            "line7": "LINE 7",
            "mediaplayer": "MEDIA PLAYER",
            "optical": "OPTICAL 1",
            "optical1": "OPTICAL 1",
            "optical2": "OPTICAL 2",
            "phono": "PHONO",
            "playstation": "PLAYSTATION",
            "playstation3": "PLAYSTATION 3",
            "playstation4": "PLAYSTATION 4",
            "rokumediaplayer": "MEDIA PLAYER",
            "satellite": "SATELLITE",
            "satellitetv": "SATELLITE",
            "smartcast": "SMARTCAST",
            "tuner": "TUNER",
            "tv": "TV",
            "usbdac": "USB DAC",
            "video": "VIDEO 1",
            "video1": "VIDEO 1",
            "video2": "VIDEO 2",
            "video3": "VIDEO 3",
            "xbox": "XBOX",
        }

        VALID_SOUND_MODE_MAP: typing.Final = {
            "movie": "MOVIE",
            "music": "MUSIC",
            "night": "NIGHT",
            "sport": "SPORT",
            "tv": "TV",
        }

    CardType: typing.TypeAlias = alexa_intents.CardType
    SpeechType: typing.TypeAlias = alexa_intents.SpeechType
    Intent: typing.TypeAlias = alexa_intents.Intent
    IntentResponse: typing.TypeAlias = alexa_intents.IntentResponse
