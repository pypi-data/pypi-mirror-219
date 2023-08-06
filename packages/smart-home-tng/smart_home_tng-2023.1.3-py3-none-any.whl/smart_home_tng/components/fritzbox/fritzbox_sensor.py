"""
AVM FRITZ!SmartHome Integration for Smart Home - The Next Generation.

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

import datetime as dt
import typing

from ... import core
from .const import Const
from .fritz_sensor_entity_description import FritzSensorEntityDescription
from .fritzbox_data_update_coordinator import FritzboxDataUpdateCoordinator
from .fritzbox_entity import FritzboxEntity

if not typing.TYPE_CHECKING:

    class FritzboxIntegration:
        pass


if typing.TYPE_CHECKING:
    from .fritzbox_integration import FritzboxIntegration


_SENSOR_TYPES: typing.Final[tuple[FritzSensorEntityDescription, ...]] = (
    FritzSensorEntityDescription(
        key="temperature",
        name="Temperature",
        native_unit_of_measurement=core.Const.UnitOfTemperature.CELSIUS,
        device_class=core.Sensor.DeviceClass.TEMPERATURE,
        state_class=core.Sensor.StateClass.MEASUREMENT,
        entity_category=core.EntityCategory.DIAGNOSTIC,
        suitable=lambda device: (
            device.has_temperature_sensor and not device.has_thermostat
        ),
        native_value=lambda device: device.temperature,
    ),
    FritzSensorEntityDescription(
        key="humidity",
        name="Humidity",
        native_unit_of_measurement=core.Const.PERCENTAGE,
        device_class=core.Sensor.DeviceClass.HUMIDITY,
        state_class=core.Sensor.StateClass.MEASUREMENT,
        suitable=lambda device: device.rel_humidity is not None,
        native_value=lambda device: device.rel_humidity,
    ),
    FritzSensorEntityDescription(
        key="battery",
        name="Battery",
        native_unit_of_measurement=core.Const.PERCENTAGE,
        device_class=core.Sensor.DeviceClass.BATTERY,
        state_class=core.Sensor.StateClass.MEASUREMENT,
        entity_category=core.EntityCategory.DIAGNOSTIC,
        suitable=lambda device: device.battery_level is not None,
        native_value=lambda device: device.battery_level,
    ),
    FritzSensorEntityDescription(
        key="power_consumption",
        name="Power Consumption",
        native_unit_of_measurement=core.Const.UnitOfPower.WATT,
        device_class=core.Sensor.DeviceClass.POWER,
        state_class=core.Sensor.StateClass.MEASUREMENT,
        suitable=lambda device: device.has_powermeter,
        native_value=lambda device: device.power / 1000 if device.power else 0.0,
    ),
    FritzSensorEntityDescription(
        key="voltage",
        name="Voltage",
        native_unit_of_measurement=core.Const.UnitOfElectricPotential.VOLT,
        device_class=core.Sensor.DeviceClass.VOLTAGE,
        state_class=core.Sensor.StateClass.MEASUREMENT,
        suitable=lambda device: device.has_powermeter,
        native_value=lambda device: device.voltage
        if getattr(device, "voltage", None)
        else 0.0,
    ),
    FritzSensorEntityDescription(
        key="electric_current",
        name="Electric Current",
        native_unit_of_measurement=core.Const.UnitOfElectricCurrent.AMPERE,
        device_class=core.Sensor.DeviceClass.CURRENT,
        state_class=core.Sensor.StateClass.MEASUREMENT,
        suitable=lambda device: device.has_powermeter,
        native_value=lambda device: round(device.power / device.voltage, 3)
        if device.power and getattr(device, "voltage", None)
        else 0.0,
    ),
    FritzSensorEntityDescription(
        key="total_energy",
        name="Total Energy",
        native_unit_of_measurement=core.Const.UnitOfEnergy.KILO_WATT_HOUR,
        device_class=core.Sensor.DeviceClass.ENERGY,
        state_class=core.Sensor.StateClass.TOTAL_INCREASING,
        suitable=lambda device: device.has_powermeter,
        native_value=lambda device: device.energy / 1000 if device.energy else 0.0,
    ),
    # Thermostat Sensors
    FritzSensorEntityDescription(
        key="comfort_temperature",
        name="Comfort Temperature",
        native_unit_of_measurement=core.Const.UnitOfTemperature.CELSIUS,
        device_class=core.Sensor.DeviceClass.TEMPERATURE,
        state_class=core.Sensor.StateClass.MEASUREMENT,
        suitable=lambda device: device.has_thermostat
        and device.comfort_temperature is not None,
        native_value=lambda device: device.comfort_temperature,
    ),
    FritzSensorEntityDescription(
        key="eco_temperature",
        name="Eco Temperature",
        native_unit_of_measurement=core.Const.UnitOfTemperature.CELSIUS,
        device_class=core.Sensor.DeviceClass.TEMPERATURE,
        state_class=core.Sensor.StateClass.MEASUREMENT,
        suitable=lambda device: device.has_thermostat
        and device.eco_temperature is not None,
        native_value=lambda device: device.eco_temperature,
    ),
    FritzSensorEntityDescription(
        key="nextchange_temperature",
        name="Next Scheduled Temperature",
        native_unit_of_measurement=core.Const.UnitOfTemperature.CELSIUS,
        device_class=core.Sensor.DeviceClass.TEMPERATURE,
        state_class=core.Sensor.StateClass.MEASUREMENT,
        suitable=lambda device: device.has_thermostat
        and device.nextchange_temperature is not None,
        native_value=lambda device: device.nextchange_temperature,
    ),
    FritzSensorEntityDescription(
        key="nextchange_time",
        name="Next Scheduled Change Time",
        device_class=core.Sensor.DeviceClass.TIMESTAMP,
        state_class=core.Sensor.StateClass.MEASUREMENT,
        suitable=lambda device: device.has_thermostat
        and device.nextchange_endperiod is not None,
        native_value=lambda device: core.helpers.utc_from_timestamp(
            device.nextchange_endperiod
        ),
    ),
    FritzSensorEntityDescription(
        key="nextchange_preset",
        name="Next Scheduled Preset",
        suitable=lambda device: device.has_thermostat
        and device.nextchange_temperature is not None,
        native_value=lambda device: core.Climate.PRESET_ECO
        if device.nextchange_temperature == device.eco_temperature
        else core.Climate.PRESET_COMFORT,
    ),
    FritzSensorEntityDescription(
        key="scheduled_preset",
        name="Current Scheduled Preset",
        suitable=lambda device: device.has_thermostat
        and device.nextchange_temperature is not None,
        native_value=lambda device: core.Climate.PRESET_COMFORT
        if device.nextchange_temperature == device.eco_temperature
        else core.Climate.PRESET_ECO,
    ),
)


class FritzboxSensor(FritzboxEntity, core.Sensor.Entity):
    """The entity class for FRITZ!SmartHome sensors."""

    _entity_description: FritzSensorEntityDescription

    @property
    def entity_description(self) -> FritzSensorEntityDescription:
        return super().entity_description

    @property
    def native_value(self) -> core.StateType | dt.datetime:
        """Return the state of the sensor."""
        return self.entity_description.native_value(self.device)


# pylint: disable=unused-variable
async def async_setup_sensors(
    owner: FritzboxIntegration,
    entry: core.ConfigEntry,
    async_add_entities: core.AddEntitiesCallback,
) -> None:
    """Set up the FRITZ!SmartHome sensor from ConfigEntry."""
    coordinator: FritzboxDataUpdateCoordinator = owner.connection_config[
        entry.entry_id
    ][Const.CONF_COORDINATOR]

    async_add_entities(
        [
            FritzboxSensor(coordinator, ain, description)
            for ain, device in coordinator.data.items()
            for description in _SENSOR_TYPES
            if description.suitable(device)
        ]
    )
