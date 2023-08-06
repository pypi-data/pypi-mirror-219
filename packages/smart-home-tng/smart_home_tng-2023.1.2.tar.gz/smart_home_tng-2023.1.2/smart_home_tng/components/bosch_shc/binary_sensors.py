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

import boschshcpy as bosch
import voluptuous as vol

from ... import core
from .battery_sensor import BatterySensor
from .const import Const
from .motion_detection_sensor import MotionDetectionSensor
from .shutter_contact_sensor import ShutterContactSensor
from .smoke_detection_sensor import SmokeDetectionSensor
from .smoke_detection_system_sensor import SmokeDetectionSystemSensor
from .water_leakage_detection_sensor import WaterLeakageDetectionSensor

if not typing.TYPE_CHECKING:

    class BoschShcIntegration:
        pass


if typing.TYPE_CHECKING:
    from .bosch_shc_integration import BoschShcIntegration

_cv: typing.TypeAlias = core.ConfigValidation


# pylint: disable=unused-variable
async def _async_setup_binary_sensors(
    owner: BoschShcIntegration,
    session: bosch.SHCSession,
    config_entry: core.ConfigEntry,
) -> typing.Iterable[core.Entity]:
    """Set up the SHC binary sensor platform."""
    entities = []

    for binary_sensor in session.device_helper.shutter_contacts:
        entities.append(
            ShutterContactSensor(
                owner,
                device=binary_sensor,
                parent_id=session.information.unique_id,
                entry_id=config_entry.entry_id,
            )
        )

    for binary_sensor in session.device_helper.motion_detectors:
        entities.append(
            MotionDetectionSensor(
                owner,
                device=binary_sensor,
                parent_id=session.information.unique_id,
                entry_id=config_entry.entry_id,
            )
        )

    for binary_sensor in session.device_helper.smoke_detectors:
        entities.append(
            SmokeDetectionSensor(
                owner,
                device=binary_sensor,
                parent_id=session.information.unique_id,
                entry_id=config_entry.entry_id,
            )
        )

    binary_sensor = session.device_helper.smoke_detection_system
    if binary_sensor:
        entities.append(
            SmokeDetectionSystemSensor(
                owner,
                device=binary_sensor,
                parent_id=session.information.unique_id,
                entry_id=config_entry.entry_id,
            )
        )

    for binary_sensor in session.device_helper.water_leakage_detectors:
        entities.append(
            WaterLeakageDetectionSensor(
                owner,
                device=binary_sensor,
                parent_id=session.information.unique_id,
                entry_id=config_entry.entry_id,
            )
        )

    for binary_sensor in (
        session.device_helper.motion_detectors
        + session.device_helper.shutter_contacts
        + session.device_helper.smoke_detectors
        + session.device_helper.thermostats
        + session.device_helper.twinguards
        + session.device_helper.universal_switches
        + session.device_helper.wallthermostats
        + session.device_helper.water_leakage_detectors
    ):
        if binary_sensor.supports_batterylevel:
            entities.append(
                BatterySensor(
                    owner,
                    device=binary_sensor,
                    parent_id=session.information.unique_id,
                    entry_id=config_entry.entry_id,
                )
            )

    platform = core.EntityPlatform.async_get_current_platform()

    platform.async_register_entity_service(
        Const.SERVICE_SMOKEDETECTOR_CHECK,
        {},
        "async_request_smoketest",
    )
    platform.async_register_entity_service(
        Const.SERVICE_SMOKEDETECTOR_ALARMSTATE,
        {
            vol.Required(core.Const.ATTR_COMMAND): _cv.string,
        },
        "async_request_alarmstate",
    )

    return entities
