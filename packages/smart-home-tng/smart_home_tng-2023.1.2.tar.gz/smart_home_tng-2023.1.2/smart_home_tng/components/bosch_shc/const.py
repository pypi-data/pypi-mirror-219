"""
Bosch SHC Integration for Smart Home - The Next Generation.

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


# pylint: disable=unused-variable
class Const:
    """Constants for the Bosch SHC integration."""

    ATTR_NAME: typing.Final = "name"
    ATTR_EVENT_TYPE: typing.Final = "event_type"
    ATTR_EVENT_SUBTYPE: typing.Final = "event_subtype"
    ATTR_LAST_TIME_TRIGGERED: typing.Final = "lastTimeTriggered"

    CONF_HOSTNAME: typing.Final = "hostname"
    CONF_SHC_CERT: typing.Final = "bosch_shc-cert.pem"
    CONF_SHC_KEY: typing.Final = "bosch_shc-key.pem"
    CONF_SUBTYPE: typing.Final = "subtype"
    CONF_SSL_CERTIFICATE: typing.Final = "ssl_certificate"
    CONF_SSL_KEY: typing.Final = "ssl_key"

    DATA_SESSION: typing.Final = "session"
    DATA_POLLING_HANDLER: typing.Final = "polling_handler"

    EVENT_BOSCH_SHC: typing.Final = "bosch_shc.event"

    SERVICE_SMOKEDETECTOR_CHECK: typing.Final = "smokedetector_check"
    SERVICE_SMOKEDETECTOR_ALARMSTATE: typing.Final = "smokedetector_alarmstate"
    SERVICE_TRIGGER_SCENARIO: typing.Final = "trigger_scenario"

    SUPPORTED_INPUTS_EVENTS_TYPES: typing.Final = {
        "PRESS_SHORT",
        "PRESS_LONG",
        "PRESS_LONG_RELEASED",
        "MOTION",
        "SCENARIO",
        "ALARM",
    }

    INPUTS_EVENTS_SUBTYPES: typing.Final = {
        "LOWER_BUTTON",
        "UPPER_BUTTON",
    }

    ALARM_EVENTS_SUBTYPES_SD: typing.Final = {
        "IDLE_OFF",
        "INTRUSION_ALARM",
        "SECONDARY_ALARM",
        "PRIMARY_ALARM",
    }

    ALARM_EVENTS_SUBTYPES_SDS: typing.Final = {
        "ALARM_OFF",
        "ALARM_ON",
        "ALARM_MUTED",
    }
