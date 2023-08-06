"""
Homematic Integration for Smart Home - The Next Generation.

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

import copy
import logging
import typing

from ... import core
from .const import Const
from .hm_device import HMDevice

if not typing.TYPE_CHECKING:

    class HomematicIntegration:
        pass


if typing.TYPE_CHECKING:
    from .homematic_integration import HomematicIntegration

_LOGGER: typing.Final = logging.getLogger(__name__)

_HM_STATE_SHC_CAST: typing.Final = {
    "IPGarage": {0: "closed", 1: "open", 2: "ventilation", 3: None},
    "RotaryHandleSensor": {0: "closed", 1: "tilted", 2: "open"},
    "RotaryHandleSensorIP": {0: "closed", 1: "tilted", 2: "open"},
    "WaterSensor": {0: "dry", 1: "wet", 2: "water"},
    "CO2Sensor": {0: "normal", 1: "added", 2: "strong"},
    "IPSmoke": {0: "off", 1: "primary", 2: "intrusion", 3: "secondary"},
    "RFSiren": {
        0: "disarmed",
        1: "extsens_armed",
        2: "allsens_armed",
        3: "alarm_blocked",
    },
    "IPLockDLD": {0: None, 1: "locked", 2: "unlocked"},
}


_SENSOR_DESCRIPTIONS: typing.Final[dict[str, core.Sensor.EntityDescription]] = {
    "HUMIDITY": core.Sensor.EntityDescription(
        key="HUMIDITY",
        native_unit_of_measurement=core.Const.PERCENTAGE,
        device_class=core.Sensor.DeviceClass.HUMIDITY,
        state_class=core.Sensor.StateClass.MEASUREMENT,
    ),
    "ACTUAL_TEMPERATURE": core.Sensor.EntityDescription(
        key="ACTUAL_TEMPERATURE",
        native_unit_of_measurement=core.Const.UnitOfTemperature.CELSIUS,
        device_class=core.Sensor.DeviceClass.TEMPERATURE,
        state_class=core.Sensor.StateClass.MEASUREMENT,
    ),
    "TEMPERATURE": core.Sensor.EntityDescription(
        key="TEMPERATURE",
        native_unit_of_measurement=core.Const.UnitOfTemperature.CELSIUS,
        device_class=core.Sensor.DeviceClass.TEMPERATURE,
        state_class=core.Sensor.StateClass.MEASUREMENT,
    ),
    "LUX": core.Sensor.EntityDescription(
        key="LUX",
        native_unit_of_measurement=core.Const.LIGHT_LUX,
        device_class=core.Sensor.DeviceClass.ILLUMINANCE,
        state_class=core.Sensor.StateClass.MEASUREMENT,
    ),
    "CURRENT_ILLUMINATION": core.Sensor.EntityDescription(
        key="CURRENT_ILLUMINATION",
        native_unit_of_measurement=core.Const.LIGHT_LUX,
        device_class=core.Sensor.DeviceClass.ILLUMINANCE,
        state_class=core.Sensor.StateClass.MEASUREMENT,
    ),
    "ILLUMINATION": core.Sensor.EntityDescription(
        key="ILLUMINATION",
        native_unit_of_measurement=core.Const.LIGHT_LUX,
        device_class=core.Sensor.DeviceClass.ILLUMINANCE,
        state_class=core.Sensor.StateClass.MEASUREMENT,
    ),
    "AVERAGE_ILLUMINATION": core.Sensor.EntityDescription(
        key="AVERAGE_ILLUMINATION",
        native_unit_of_measurement=core.Const.LIGHT_LUX,
        device_class=core.Sensor.DeviceClass.ILLUMINANCE,
        state_class=core.Sensor.StateClass.MEASUREMENT,
    ),
    "LOWEST_ILLUMINATION": core.Sensor.EntityDescription(
        key="LOWEST_ILLUMINATION",
        native_unit_of_measurement=core.Const.LIGHT_LUX,
        device_class=core.Sensor.DeviceClass.ILLUMINANCE,
        state_class=core.Sensor.StateClass.MEASUREMENT,
    ),
    "HIGHEST_ILLUMINATION": core.Sensor.EntityDescription(
        key="HIGHEST_ILLUMINATION",
        native_unit_of_measurement=core.Const.LIGHT_LUX,
        device_class=core.Sensor.DeviceClass.ILLUMINANCE,
        state_class=core.Sensor.StateClass.MEASUREMENT,
    ),
    "POWER": core.Sensor.EntityDescription(
        key="POWER",
        native_unit_of_measurement=core.Const.UnitOfPower.WATT,
        device_class=core.Sensor.DeviceClass.POWER,
        state_class=core.Sensor.StateClass.MEASUREMENT,
    ),
    "IEC_POWER": core.Sensor.EntityDescription(
        key="IEC_POWER",
        native_unit_of_measurement=core.Const.UnitOfPower.WATT,
        device_class=core.Sensor.DeviceClass.POWER,
        state_class=core.Sensor.StateClass.MEASUREMENT,
    ),
    "CURRENT": core.Sensor.EntityDescription(
        key="CURRENT",
        native_unit_of_measurement=core.Const.UnitOfElectricsCurrent.MILLIAMPERE,
        device_class=core.Sensor.DeviceClass.CURRENT,
        state_class=core.Sensor.StateClass.MEASUREMENT,
    ),
    "CONCENTRATION": core.Sensor.EntityDescription(
        key="CONCENTRATION",
        native_unit_of_measurement=core.Const.CONCENTRATION_PARTS_PER_MILLION,
        device_class=core.Sensor.DeviceClass.CO2,
        state_class=core.Sensor.StateClass.MEASUREMENT,
    ),
    "ENERGY_COUNTER": core.Sensor.EntityDescription(
        key="ENERGY_COUNTER",
        native_unit_of_measurement=core.Const.UnitOfEnergy.WATT_HOUR,
        device_class=core.Sensor.DeviceClass.ENERGY,
        state_class=core.Sensor.StateClass.TOTAL_INCREASING,
    ),
    "IEC_ENERGY_COUNTER": core.Sensor.EntityDescription(
        key="IEC_ENERGY_COUNTER",
        native_unit_of_measurement=core.Const.UnitOfEnergy.WATT_HOUR,
        device_class=core.Sensor.DeviceClass.ENERGY,
        state_class=core.Sensor.StateClass.TOTAL_INCREASING,
    ),
    "VOLTAGE": core.Sensor.EntityDescription(
        key="VOLTAGE",
        native_unit_of_measurement=core.Const.UnitOfElectricPotential.VOLT,
        device_class=core.Sensor.DeviceClass.VOLTAGE,
        state_class=core.Sensor.StateClass.MEASUREMENT,
    ),
    "GAS_POWER": core.Sensor.EntityDescription(
        key="GAS_POWER",
        native_unit_of_measurement=core.Const.UnitOfVolume.CUBIC_METERS,
        device_class=core.Sensor.DeviceClass.GAS,
        state_class=core.Sensor.StateClass.MEASUREMENT,
    ),
    "GAS_ENERGY_COUNTER": core.Sensor.EntityDescription(
        key="GAS_ENERGY_COUNTER",
        native_unit_of_measurement=core.Const.UnitOfVolume.CUBIC_METERS,
        device_class=core.Sensor.DeviceClass.GAS,
        state_class=core.Sensor.StateClass.TOTAL_INCREASING,
    ),
    "RAIN_COUNTER": core.Sensor.EntityDescription(
        key="RAIN_COUNTER",
        native_unit_of_measurement=core.Const.UnitOfLength.MILLIMETERS,
    ),
    "WIND_SPEED": core.Sensor.EntityDescription(
        key="WIND_SPEED",
        native_unit_of_measurement=core.Const.UnitOfSpeed.KILOMETERS_PER_HOUR,
        icon="mdi:weather-windy",
    ),
    "WIND_DIRECTION": core.Sensor.EntityDescription(
        key="WIND_DIRECTION",
        native_unit_of_measurement=core.Const.DEGREE,
    ),
    "WIND_DIRECTION_RANGE": core.Sensor.EntityDescription(
        key="WIND_DIRECTION_RANGE",
        native_unit_of_measurement=core.Const.DEGREE,
    ),
    "SUNSHINEDURATION": core.Sensor.EntityDescription(
        key="SUNSHINEDURATION",
        native_unit_of_measurement="#",
    ),
    "AIR_PRESSURE": core.Sensor.EntityDescription(
        key="AIR_PRESSURE",
        native_unit_of_measurement=core.Const.UnitOfPressure.HPA,
        device_class=core.Sensor.DeviceClass.PRESSURE,
        state_class=core.Sensor.StateClass.MEASUREMENT,
    ),
    "FREQUENCY": core.Sensor.EntityDescription(
        key="FREQUENCY",
        native_unit_of_measurement=core.Const.UnitOfFrequency.HERTZ,
    ),
    "VALUE": core.Sensor.EntityDescription(
        key="VALUE",
        native_unit_of_measurement="#",
    ),
    "VALVE_STATE": core.Sensor.EntityDescription(
        key="VALVE_STATE",
        native_unit_of_measurement=core.Const.PERCENTAGE,
    ),
    "CARRIER_SENSE_LEVEL": core.Sensor.EntityDescription(
        key="CARRIER_SENSE_LEVEL",
        native_unit_of_measurement=core.Const.PERCENTAGE,
    ),
    "DUTY_CYCLE_LEVEL": core.Sensor.EntityDescription(
        key="DUTY_CYCLE_LEVEL",
        native_unit_of_measurement=core.Const.PERCENTAGE,
    ),
    "BRIGHTNESS": core.Sensor.EntityDescription(
        key="BRIGHTNESS",
        native_unit_of_measurement="#",
        icon="mdi:invert-colors",
    ),
    "MASS_CONCENTRATION_PM_1": core.Sensor.EntityDescription(
        key="MASS_CONCENTRATION_PM_1",
        native_unit_of_measurement=core.Const.CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
        device_class=core.Sensor.DeviceClass.PM1,
        state_class=core.Sensor.StateClass.MEASUREMENT,
    ),
    "MASS_CONCENTRATION_PM_2_5": core.Sensor.EntityDescription(
        key="MASS_CONCENTRATION_PM_2_5",
        native_unit_of_measurement=core.Const.CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
        device_class=core.Sensor.DeviceClass.PM25,
        state_class=core.Sensor.StateClass.MEASUREMENT,
    ),
    "MASS_CONCENTRATION_PM_10": core.Sensor.EntityDescription(
        key="MASS_CONCENTRATION_PM_10",
        native_unit_of_measurement=core.Const.CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
        device_class=core.Sensor.DeviceClass.PM10,
        state_class=core.Sensor.StateClass.MEASUREMENT,
    ),
    "MASS_CONCENTRATION_PM_1_24H_AVERAGE": core.Sensor.EntityDescription(
        key="MASS_CONCENTRATION_PM_1_24H_AVERAGE",
        native_unit_of_measurement=core.Const.CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
        device_class=core.Sensor.DeviceClass.PM1,
        state_class=core.Sensor.StateClass.MEASUREMENT,
    ),
    "MASS_CONCENTRATION_PM_2_5_24H_AVERAGE": core.Sensor.EntityDescription(
        key="MASS_CONCENTRATION_PM_2_5_24H_AVERAGE",
        native_unit_of_measurement=core.Const.CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
        device_class=core.Sensor.DeviceClass.PM25,
        state_class=core.Sensor.StateClass.MEASUREMENT,
    ),
    "MASS_CONCENTRATION_PM_10_24H_AVERAGE": core.Sensor.EntityDescription(
        key="MASS_CONCENTRATION_PM_10_24H_AVERAGE",
        native_unit_of_measurement=core.Const.CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
        device_class=core.Sensor.DeviceClass.PM10,
        state_class=core.Sensor.StateClass.MEASUREMENT,
    ),
}

_DEFAULT_SENSOR_DESCRIPTION: typing.Final = core.Sensor.EntityDescription(
    key="",
    entity_registry_enabled_default=True,
)


class HMSensor(HMDevice, core.Sensor.Entity):
    """Representation of a HomeMatic sensor."""

    @property
    def native_value(self):
        """Return the state of the sensor."""
        # Does a cast exist for this class?
        name = self._hmdevice.__class__.__name__
        if name in _HM_STATE_SHC_CAST:
            return _HM_STATE_SHC_CAST[name].get(self._hm_get_state())

        # No cast, return original value
        return self._hm_get_state()

    def _init_data_struct(self):
        """Generate a data dictionary (self._data) from metadata."""
        if self._state:
            self._data.update({self._state: None})
        else:
            _LOGGER.critical(f"Unable to initialize sensor: {self._name}")


# pylint: disable=unused-variable
async def async_setup_sensors(
    comp: HomematicIntegration,
    add_entities: core.AddEntitiesCallback,
    discovery_info: core.DiscoveryInfoType = None,
) -> None:
    """Set up the HomeMatic sensor platform."""
    if discovery_info is None:
        return

    devices = []
    for conf in discovery_info[Const.ATTR_DISCOVER_DEVICES]:
        state = conf.get(Const.ATTR_PARAM)
        if (entity_desc := _SENSOR_DESCRIPTIONS.get(state)) is None:
            name = conf.get(core.Const.ATTR_NAME)
            _LOGGER.warning(
                f"Sensor ({name}) entity description is missing. "
                + f"Sensor state ({state}) needs to be maintained",
            )
            entity_desc = copy.copy(_DEFAULT_SENSOR_DESCRIPTION)

        new_device = HMSensor(comp, conf, entity_desc)
        devices.append(new_device)

    add_entities(devices, True)
