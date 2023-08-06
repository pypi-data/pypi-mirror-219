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

from ... import core
from .air_quality_sensor import AirQualitySensor
from .communication_quality_sensor import CommunicationQualitySensor
from .energy_sensor import EnergySensor
from .humidity_rating_sensor import HumidityRatingSensor
from .humidity_sensor import HumiditySensor
from .power_sensor import PowerSensor
from .purity_rating_sensor import PurityRatingSensor
from .purity_sensor import PuritySensor
from .temperature_rating_sensor import TemperatureRatingSensor
from .temperature_sensor import TemperatureSensor
from .valve_tappet_sensor import ValveTappetSensor

if not typing.TYPE_CHECKING:

    class BoschShcIntegration:
        pass


if typing.TYPE_CHECKING:
    from .bosch_shc_integration import BoschShcIntegration


# pylint: disable=unused-variable
async def _async_setup_sensors(
    owner: BoschShcIntegration,
    session: bosch.SHCSession,
    config_entry: core.ConfigEntry,
) -> typing.Iterable[core.Entity]:
    """Set up the SHC sensor platform."""
    entities: list[core.Sensor.Entity] = []

    for sensor in session.device_helper.thermostats:
        entities.append(
            TemperatureSensor(
                owner,
                device=sensor,
                parent_id=session.information.unique_id,
                entry_id=config_entry.entry_id,
            )
        )
        entities.append(
            ValveTappetSensor(
                owner,
                device=sensor,
                parent_id=session.information.unique_id,
                entry_id=config_entry.entry_id,
            )
        )

    for sensor in session.device_helper.wallthermostats:
        entities.append(
            TemperatureSensor(
                owner,
                device=sensor,
                parent_id=session.information.unique_id,
                entry_id=config_entry.entry_id,
            )
        )
        entities.append(
            HumiditySensor(
                owner,
                device=sensor,
                parent_id=session.information.unique_id,
                entry_id=config_entry.entry_id,
            )
        )

    for sensor in session.device_helper.twinguards:
        entities.append(
            TemperatureSensor(
                owner,
                device=sensor,
                parent_id=session.information.unique_id,
                entry_id=config_entry.entry_id,
            )
        )
        entities.append(
            HumiditySensor(
                owner,
                device=sensor,
                parent_id=session.information.unique_id,
                entry_id=config_entry.entry_id,
            )
        )
        entities.append(
            PuritySensor(
                owner,
                device=sensor,
                parent_id=session.information.unique_id,
                entry_id=config_entry.entry_id,
            )
        )
        entities.append(
            AirQualitySensor(
                owner,
                device=sensor,
                parent_id=session.information.unique_id,
                entry_id=config_entry.entry_id,
            )
        )
        entities.append(
            TemperatureRatingSensor(
                owner,
                device=sensor,
                parent_id=session.information.unique_id,
                entry_id=config_entry.entry_id,
            )
        )
        entities.append(
            HumidityRatingSensor(
                owner,
                device=sensor,
                parent_id=session.information.unique_id,
                entry_id=config_entry.entry_id,
            )
        )
        entities.append(
            PurityRatingSensor(
                owner,
                device=sensor,
                parent_id=session.information.unique_id,
                entry_id=config_entry.entry_id,
            )
        )

    for sensor in (
        session.device_helper.smart_plugs + session.device_helper.light_switches_bsm
    ):
        entities.append(
            PowerSensor(
                owner,
                device=sensor,
                parent_id=session.information.unique_id,
                entry_id=config_entry.entry_id,
            )
        )
        entities.append(
            EnergySensor(
                owner,
                device=sensor,
                parent_id=session.information.unique_id,
                entry_id=config_entry.entry_id,
            )
        )

    for sensor in session.device_helper.smart_plugs_compact:
        entities.append(
            PowerSensor(
                owner,
                device=sensor,
                parent_id=session.information.unique_id,
                entry_id=config_entry.entry_id,
            )
        )
        entities.append(
            EnergySensor(
                owner,
                device=sensor,
                parent_id=session.information.unique_id,
                entry_id=config_entry.entry_id,
            )
        )
        entities.append(
            CommunicationQualitySensor(
                owner,
                device=sensor,
                parent_id=session.information.unique_id,
                entry_id=config_entry.entry_id,
            )
        )
    return entities
