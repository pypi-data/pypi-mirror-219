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

import contextlib
import dataclasses
import datetime as dt
import decimal as dec
import enum
import logging
import math
import typing

from ..backports import strenum
from . import helpers
from .callback import callback
from .const import Const
from .entity import _SensorEntityBase
from .entity_description import EntityDescription
from .extra_stored_data import ExtraStoredData
from .state_type import StateType
from .unit_conversion import (
    BaseUnitConverter,
    DataRateConverter,
    DistanceConverter,
    ElectricCurrentConverter,
    ElectricPotentialConverter,
    EnergyConverter,
    InformationConverter,
    MassConverter,
    PowerConverter,
    PressureConverter,
    SpeedConverter,
    TemperatureConverter,
    UnitlessRatioConverter,
    VolumeConverter,
)

_LOGGER: typing.Final = logging.getLogger(__name__)


class _DeviceClass(strenum.LowercaseStrEnum):
    """Device class for sensors."""

    APPARENT_POWER = enum.auto()
    """Apparent power.

    Unit of measurement: `VA`
    """

    AQI = enum.auto()
    """Air Quality Index.

    Unit of measurement: `None`
    """

    ATMOSPHERIC_PRESSURE = enum.auto()
    """Atmospheric pressure.

    Unit of measurement: `UnitOfPressure` units
    """

    BATTERY = enum.auto()
    """Percentage of battery that is left.

    Unit of measurement: `%`
    """

    CO = enum.auto()
    """Carbon Monoxide gas concentration.

    Unit of measurement: `ppm` (parts per million)
    """

    CO2 = enum.auto()
    """Carbon Dioxide gas concentration.

    Unit of measurement: `ppm` (parts per million)
    """

    CURRENT = enum.auto()
    """Current.

    Unit of measurement: `A`
    """

    DATA_RATE = enum.auto()
    """Data rate.

    Unit of measurement: UnitOfDataRate
    """

    DATA_SIZE = enum.auto()
    """Data size.

    Unit of measurement: UnitOfInformation
    """

    DATE = enum.auto()
    """Date.

    Unit of measurement: `None`

    ISO8601 format: https://en.wikipedia.org/wiki/ISO_8601
    """

    DISTANCE = enum.auto()
    """Generic distance.

    Unit of measurement: `LENGTH_*` units
    - SI /metric: `mm`, `cm`, `m`, `km`
    - USCS / imperial: `in`, `ft`, `yd`, `mi`
    """

    DURATION = enum.auto()
    """Fixed duration.

    Unit of measurement: `d`, `h`, `min`, `s`
    """

    ENERGY = enum.auto()
    """Energy.

    Unit of measurement: `Wh`, `kWh`, `MWh`, `GJ`
    """

    ENERGY_STORAGE = enum.auto()
    """Stored energy.

    Use this device class for sensors measuring stored energy, for example the amount
    of electric energy currently stored in a battery or the capacity of a battery.

    Unit of measurement: `Wh`, `kWh`, `MWh`, `MJ`, `GJ`
    """

    ENUM = enum.auto()
    """Enumeration.

    Provides a fixed list of options the state of the sensor can be in.

    Unit of measurement: `None`
    """

    FREQUENCY = enum.auto()
    """Frequency.

    Unit of measurement: `Hz`, `kHz`, `MHz`, `GHz`
    """

    GAS = enum.auto()
    """Gas.

    Unit of measurement: `m³`, `ft³`
    """

    HUMIDITY = enum.auto()
    """Relative humidity.

    Unit of measurement: `%`
    """

    ILLUMINANCE = enum.auto()
    """Illuminance.

    Unit of measurement: `lx`, `lm`
    """

    IRRADIANCE = enum.auto()
    """Irradiance.

    Unit of measurement:
    - SI / metric: `W/m²`
    - USCS / imperial: `BTU/(h⋅ft²)`
    """

    MOISTURE = enum.auto()
    """Moisture.

    Unit of measurement: `%`
    """

    MONETARY = enum.auto()
    """Amount of money.

    Unit of measurement: ISO4217 currency code

    See https://en.wikipedia.org/wiki/ISO_4217#Active_codes for active codes
    """

    NITROGEN_DIOXIDE = enum.auto()
    """Amount of NO2.

    Unit of measurement: `µg/m³`
    """

    NITROGEN_MONOXIDE = enum.auto()
    """Amount of NO.

    Unit of measurement: `µg/m³`
    """

    NITROUS_OXIDE = enum.auto()
    """Amount of N2O.

    Unit of measurement: `µg/m³`
    """

    OZONE = enum.auto()
    """Amount of O3.

    Unit of measurement: `µg/m³`
    """

    PM1 = enum.auto()
    """Particulate matter <= 0.1 μm.

    Unit of measurement: `µg/m³`
    """

    PM10 = enum.auto()
    """Particulate matter <= 10 μm.

    Unit of measurement: `µg/m³`
    """

    PM25 = enum.auto()
    """Particulate matter <= 2.5 μm.

    Unit of measurement: `µg/m³`
    """

    POWER_FACTOR = enum.auto()
    """Power factor.

    Unit of measurement: `%`
    """

    POWER = enum.auto()
    """Power.

    Unit of measurement: `W`, `kW`
    """

    PRECIPITATION = enum.auto()
    """Precipitation.

    Unit of measurement:
    - SI / metric: `mm`
    - USCS / imperial: `in`
    """

    PRECIPITATION_INTENSITY = enum.auto()
    """Precipitation intensity.

    Unit of measurement: UnitOfVolumetricFlux
    - SI /metric: `mm/d`, `mm/h`
    - USCS / imperial: `in/d`, `in/h`
    """

    PRESSURE = enum.auto()
    """Pressure.

    Unit of measurement:
    - `mbar`, `cbar`, `bar`
    - `Pa`, `hPa`, `kPa`
    - `inHg`
    - `psi`
    """

    REACTIVE_POWER = enum.auto()
    """Reactive power.

    Unit of measurement: `var`
    """

    SIGNAL_STRENGTH = enum.auto()
    """Signal strength.

    Unit of measurement: `dB`, `dBm`
    """

    SOUND_PRESSURE = enum.auto()
    """Sound pressure.

    Unit of measurement: `dB`, `dBA`
    """

    SPEED = enum.auto()
    """Generic speed.

    Unit of measurement: `SPEED_*` units or `UnitOfVolumetricFlux`
    - SI /metric: `mm/d`, `mm/h`, `m/s`, `km/h`
    - USCS / imperial: `in/d`, `in/h`, `ft/s`, `mph`
    - Nautical: `kn`
    """

    SULPHUR_DIOXIDE = enum.auto()
    """Amount of SO2.

    Unit of measurement: `µg/m³`
    """

    TEMPERATURE = enum.auto()
    """Temperature.

    Unit of measurement: `°C`, `°F`
    """

    TIMESTAMP = enum.auto()
    """Timestamp.

    Unit of measurement: `None`

    ISO8601 format: https://en.wikipedia.org/wiki/ISO_8601
    """

    VOLATILE_ORGANIC_COMPOUNDS = enum.auto()
    """Amount of VOC.

    Unit of measurement: `µg/m³`
    """

    VOLATILE_ORGANIC_COMPOUNDS_PARTS = enum.auto()
    """Ratio of VOC.

    Unit of measurement: `ppm`, `ppb`
    """

    VOLTAGE = enum.auto()
    """Voltage.

    Unit of measurement: `V`
    """

    VOLUME = enum.auto()
    """Generic volume.

    Unit of measurement: `VOLUME_*` units
    - SI / metric: `mL`, `L`, `m³`
    - USCS / imperial: `fl. oz.`, `ft³`, `gal` (warning: volumes expressed in
    USCS/imperial units are currently assumed to be US volumes)
    """

    VOLUME_STORAGE = enum.auto()
    """Generic stored volume.

    Use this device class for sensors measuring stored volume, for example the amount
    of fuel in a fuel tank.

    Unit of measurement: `VOLUME_*` units
    - SI / metric: `mL`, `L`, `m³`
    - USCS / imperial: `ft³`, `CCF`, `fl. oz.`, `gal` (warning: volumes expressed in
    USCS/imperial units are currently assumed to be US volumes)
    """

    WATER = enum.auto()
    """Water.

    Unit of measurement:
    - SI / metric: `m³`, `L`
    - USCS / imperial: `ft³`, `gal` (warning: volumes expressed in
    USCS/imperial units are currently assumed to be US volumes)
    """

    WEIGHT = enum.auto()
    """Generic weight, represents a measurement of an object's mass.

    Weight is used instead of mass to fit with every day language.

    Unit of measurement: `MASS_*` units
    - SI / metric: `µg`, `mg`, `g`, `kg`
    - USCS / imperial: `oz`, `lb`
    """

    WIND_SPEED = enum.auto()
    """Wind speed.

    Unit of measurement: `SPEED_*` units
    - SI /metric: `m/s`, `km/h`
    - USCS / imperial: `ft/s`, `mph`
    - Nautical: `kn`
    """


class _StateClass(strenum.LowercaseStrEnum):
    """State class for sensors."""

    MEASUREMENT = enum.auto()
    """The state represents a measurement in present time"""

    TOTAL = enum.auto()
    """The state represents a total amount, e.g. net energy consumption"""

    TOTAL_INCREASING = enum.auto()
    """The state represents a monotonically increasing total, e.g. an amount of consumed gas"""


@dataclasses.dataclass()
class _EntityDescription(EntityDescription):
    """A class that describes sensor entities."""

    device_class: _DeviceClass | str = None
    last_reset: dt.datetime = None
    native_unit_of_measurement: str = None
    state_class: _StateClass | str = None
    unit_of_measurement: None = None  # Type override, use native_unit_of_measurement


@dataclasses.dataclass
class _ExtraStoredData(ExtraStoredData):
    """Object to hold extra stored data."""

    native_value: StateType | dt.date | dt.datetime | dec.Decimal
    native_unit_of_measurement: str

    def as_dict(self) -> dict[str, typing.Any]:
        """Return a dict representation of the sensor data."""
        native_value: StateType | dt.date | dt.datetime | dec.Decimal | dict[
            str, str
        ] = self.native_value
        if isinstance(native_value, (dt.date, dt.datetime)):
            native_value = {
                "__type": str(type(native_value)),
                "isoformat": native_value.isoformat(),
            }
        if isinstance(native_value, dec.Decimal):
            native_value = {
                "__type": str(type(native_value)),
                "decimal_str": str(native_value),
            }
        return {
            "native_value": native_value,
            "native_unit_of_measurement": self.native_unit_of_measurement,
        }

    @classmethod
    def from_dict(cls, restored: dict[str, typing.Any]):
        """Initialize a stored sensor state from a dict."""
        try:
            native_value = restored["native_value"]
            native_unit_of_measurement: str = restored["native_unit_of_measurement"]
        except KeyError:
            return None
        try:
            type_ = native_value["__type"]
            if type_ == "<class 'datetime.datetime'>":
                native_value = helpers.parse_datetime(native_value["isoformat"])
            elif type_ == "<class 'datetime.date'>":
                native_value = helpers.parse_date(native_value["isoformat"])
            elif type_ == "<class 'decimal.Decimal'>":
                native_value = dec.Decimal(native_value["decimal_str"])
        except TypeError:
            # native_value is not a dict
            pass
        except KeyError:
            # native_value is a dict, but does not have all values
            return None
        except dec.InvalidOperation:
            # native_value coulnd't be returned from decimal_str
            return None

        return cls(native_value, native_unit_of_measurement)


_PRESSURE_RATIO: typing.Final[dict[str, float]] = {
    Const.UnitOfPressure.PA: 1,
    Const.UnitOfPressure.HPA: 1 / 100,
    Const.UnitOfPressure.KPA: 1 / 1000,
    Const.UnitOfPressure.BAR: 1 / 100000,
    Const.UnitOfPressure.CBAR: 1 / 1000,
    Const.UnitOfPressure.MBAR: 1 / 100,
    Const.UnitOfPressure.INHG: 1 / 3386.389,
    Const.UnitOfPressure.PSI: 1 / 6894.757,
    Const.UnitOfPressure.MMHG: 1 / 133.322,
}
_TEMPERATURE_RATIO: typing.Final = {
    Const.UnitOfTemperature.CELSIUS: 1.0,
    Const.UnitOfTemperature.FAHRENHEIT: 1.8,
    Const.UnitOfTemperature.KELVIN: 1.0,
}
_ATTR_LAST_RESET: typing.Final = "last_reset"
_ATTR_STATE_CLASS: typing.Final = "state_class"
_UNIT_CONVERSIONS: dict[str, typing.Callable[[float, str, str], float]] = {
    _DeviceClass.PRESSURE: PressureConverter.convert,
    _DeviceClass.TEMPERATURE: TemperatureConverter.convert,
}
_UNIT_RATIOS: dict[str, dict[str, float]] = {
    _DeviceClass.PRESSURE: _PRESSURE_RATIO,
    _DeviceClass.TEMPERATURE: _TEMPERATURE_RATIO,
}
_VALID_UNITS: typing.Final = {
    _DeviceClass.PRESSURE: PressureConverter.VALID_UNITS,
    _DeviceClass.TEMPERATURE: TemperatureConverter.VALID_UNITS,
}


class _Entity(_SensorEntityBase):
    """Base class for sensor entities."""

    _entity_description: _EntityDescription
    _attr_device_class: _DeviceClass | str
    _attr_last_reset: dt.datetime
    _attr_native_unit_of_measurement: str
    _attr_native_value: StateType | dt.date | dt.datetime = None
    _attr_state_class: _StateClass | str
    _attr_state: None = None  # Subclasses of SensorEntity should not set this
    _attr_unit_of_measurement: None = (
        None  # Subclasses of SensorEntity should not set this
    )
    _last_reset_reported = False
    _temperature_conversion_reported = False
    _sensor_option_unit_of_measurement: str = None

    # Temporary private attribute to track if deprecation has been logged.
    __datetime_as_string_deprecation_logged = False

    async def async_internal_added_to_shc(self) -> None:
        """Call when the sensor entity is added to the Smart Home Controller."""
        await super().async_internal_added_to_shc()
        if not self.registry_entry:
            return
        self.async_registry_entry_updated()

    @property
    def entity_description(self) -> _EntityDescription:
        return super().entity_description

    @property
    def device_class(self) -> str:
        """Return the class of this entity."""
        if hasattr(self, "_attr_device_class"):
            return str(self._attr_device_class)
        if (description := self.entity_description) is not None:
            return str(description.device_class)
        return None

    @property
    def state_class(self) -> _StateClass | str:
        """Return the state class of this entity, if any."""
        if hasattr(self, "_attr_state_class"):
            return self._attr_state_class
        if (description := self.entity_description) is not None:
            return description.state_class
        return None

    @property
    def last_reset(self) -> dt.datetime:
        """Return the time when the sensor was last reset, if any."""
        if hasattr(self, "_attr_last_reset"):
            return self._attr_last_reset
        if (description := self.entity_description) is not None:
            return description.last_reset
        return None

    @property
    def capability_attributes(self) -> typing.Mapping[str, typing.Any]:
        """Return the capability attributes."""
        if state_class := self.state_class:
            return {_ATTR_STATE_CLASS: state_class}

        return None

    @typing.final
    @property
    def state_attributes(self) -> dict[str, typing.Any]:
        """Return state attributes."""
        if last_reset := self.last_reset:
            if self.state_class != _StateClass.TOTAL and not self._last_reset_reported:
                self._last_reset_reported = True
                report_issue = self._suggest_report_issue()
                # This should raise in Home Assistant Core 2022.5
                _LOGGER.warning(
                    f"Entity {self._entity_id} ({type(self)}) with state_class "
                    + f"{self.state_class} has set last_reset. Setting "
                    + "last_reset for entities with state_class other than 'total' is "
                    + "not supported. "
                    + "Please update your configuration if state_class is manually "
                    + f"configured, otherwise {report_issue}",
                    self.entity_id,
                    type(self),
                    self.state_class,
                    report_issue,
                )

            if self.state_class == _StateClass.TOTAL:
                return {_ATTR_LAST_RESET: last_reset.isoformat()}

        return None

    @property
    def native_value(self) -> StateType | dt.date | dt.datetime:
        """Return the value reported by the sensor."""
        return self._attr_native_value

    @property
    def native_unit_of_measurement(self) -> str:
        """Return the unit of measurement of the sensor, if any."""
        if hasattr(self, "_attr_native_unit_of_measurement"):
            return self._attr_native_unit_of_measurement
        if (description := self.entity_description) is not None:
            return description.native_unit_of_measurement
        return None

    @typing.final
    @property
    def unit_of_measurement(self) -> str:
        """Return the unit of measurement of the entity, after unit conversion."""
        if self._sensor_option_unit_of_measurement:
            return self._sensor_option_unit_of_measurement

        native_unit_of_measurement = self.native_unit_of_measurement

        if (
            self.device_class == _DeviceClass.TEMPERATURE
            and native_unit_of_measurement
            in (Const.UnitOfTemperature.CELSIUS, Const.UnitOfTemperature.FAHRENHEIT)
        ):
            return self._shc.config.units.temperature_unit

        return native_unit_of_measurement

    @typing.final
    @property
    def state(self) -> typing.Any:
        """Return the state of the sensor and perform unit conversions, if needed."""
        native_unit_of_measurement = self.native_unit_of_measurement
        unit_of_measurement = self.unit_of_measurement
        value = self.native_value
        device_class = self.device_class

        # Received a datetime
        if value is not None and device_class == _DeviceClass.TIMESTAMP:
            try:
                # We cast the value, to avoid using isinstance, but satisfy
                # typechecking. The errors are guarded in this try.
                value = typing.cast(dt.datetime, value)
                if value.tzinfo is None:
                    raise ValueError(
                        f"Invalid datetime: {self._entity_id} provides state '{value}', "
                        "which is missing timezone information"
                    )

                if value.tzinfo != dt.timezone.utc:
                    value = value.astimezone(dt.timezone.utc)

                return value.isoformat(timespec="seconds")
            except (AttributeError, TypeError) as err:
                raise ValueError(
                    f"Invalid datetime: {self._entity_id} has a timestamp device class "
                    + f"but does not provide a datetime state but {type(value)}"
                ) from err

        # Received a date value
        if value is not None and device_class == _DeviceClass.DATE:
            try:
                # We cast the value, to avoid using isinstance, but satisfy
                # typechecking. The errors are guarded in this try.
                value = typing.cast(dt.date, value)
                return value.isoformat()
            except (AttributeError, TypeError) as err:
                raise ValueError(
                    f"Invalid date: {self._entity_id} has a date device class "
                    f"but does not provide a date state but {type(value)}"
                ) from err

        if (
            value is not None
            and native_unit_of_measurement != unit_of_measurement
            and self.device_class in _UNIT_CONVERSIONS
        ):
            assert unit_of_measurement
            assert native_unit_of_measurement

            value_s = str(value)
            prec = len(value_s) - value_s.index(".") - 1 if "." in value_s else 0

            # Scale the precision when converting to a larger unit
            # For example 1.1 Wh should be rendered as 0.0011 kWh, not 0.0 kWh
            ratio_log = max(
                0,
                math.log10(
                    _UNIT_RATIOS[self.device_class][native_unit_of_measurement]
                    / _UNIT_RATIOS[self.device_class][unit_of_measurement]
                ),
            )
            prec = prec + math.floor(ratio_log)

            # Suppress ValueError (Could not convert sensor_value to float)
            with contextlib.suppress(ValueError):
                value_f = float(value)
                value_f_new = _UNIT_CONVERSIONS[self.device_class](
                    value_f,
                    native_unit_of_measurement,
                    unit_of_measurement,
                )

                # Round to the wanted precision
                value = round(value_f_new) if prec == 0 else round(value_f_new, prec)

        return value

    def __repr__(self) -> str:
        """Return the representation.

        Entity.__repr__ includes the state in the generated string, this fails if we're
        called before self._shc is set.
        """
        if not self._shc:
            return f"<Entity {self.name}>"

        return super().__repr__()

    @callback
    def async_registry_entry_updated(self) -> None:
        """Run when the entity registry entry has been updated."""
        assert self._registry_entry
        if (
            (sensor_options := self._registry_entry.options.get("sensor"))
            and (custom_unit := sensor_options.get(Const.CONF_UNIT_OF_MEASUREMENT))
            and (device_class := self.device_class) in _UNIT_CONVERSIONS
            and self.native_unit_of_measurement in _VALID_UNITS[device_class]
            and custom_unit in _VALID_UNITS[device_class]
        ):
            self._sensor_option_unit_of_measurement = custom_unit
            return

        self._sensor_option_unit_of_measurement = None


# pylint: disable=invalid-name
class Sensor:
    """Sensor namespace."""

    ATTR_LAST_RESET: typing.Final = _ATTR_LAST_RESET
    ATTR_STATE_CLASS: typing.Final = _ATTR_STATE_CLASS
    STATE_CLASSES: typing.Final[list[str]] = [cls.value for cls in _StateClass]

    DeviceClass: typing.TypeAlias = _DeviceClass
    Entity: typing.TypeAlias = _Entity
    EntityDescription: typing.TypeAlias = _EntityDescription
    ExtraStoredData: typing.TypeAlias = _ExtraStoredData
    StateClass: typing.TypeAlias = _StateClass

    UNIT_CONVERTERS: typing.Final[dict[_DeviceClass | str, type[BaseUnitConverter]]] = {
        _DeviceClass.ATMOSPHERIC_PRESSURE: PressureConverter,
        _DeviceClass.CURRENT: ElectricCurrentConverter,
        _DeviceClass.DATA_RATE: DataRateConverter,
        _DeviceClass.DATA_SIZE: InformationConverter,
        _DeviceClass.DISTANCE: DistanceConverter,
        _DeviceClass.ENERGY: EnergyConverter,
        _DeviceClass.ENERGY_STORAGE: EnergyConverter,
        _DeviceClass.GAS: VolumeConverter,
        _DeviceClass.POWER: PowerConverter,
        _DeviceClass.POWER_FACTOR: UnitlessRatioConverter,
        _DeviceClass.PRECIPITATION: DistanceConverter,
        _DeviceClass.PRECIPITATION_INTENSITY: SpeedConverter,
        _DeviceClass.PRESSURE: PressureConverter,
        _DeviceClass.SPEED: SpeedConverter,
        _DeviceClass.TEMPERATURE: TemperatureConverter,
        _DeviceClass.VOLATILE_ORGANIC_COMPOUNDS_PARTS: UnitlessRatioConverter,
        _DeviceClass.VOLTAGE: ElectricPotentialConverter,
        _DeviceClass.VOLUME: VolumeConverter,
        _DeviceClass.WATER: VolumeConverter,
        _DeviceClass.WEIGHT: MassConverter,
        _DeviceClass.WIND_SPEED: SpeedConverter,
    }

    NON_NUMERIC_DEVICE_CLASSES: typing.Final = {
        _DeviceClass.DATE,
        _DeviceClass.ENUM,
        _DeviceClass.TIMESTAMP,
    }

    DEVICE_CLASS_UNITS: typing.Final[
        dict[_DeviceClass, set[type[strenum.StrEnum] | str | None]]
    ] = {
        _DeviceClass.APPARENT_POWER: set(Const.UnitOfApparentPower),
        _DeviceClass.AQI: {None},
        _DeviceClass.ATMOSPHERIC_PRESSURE: set(Const.UnitOfPressure),
        _DeviceClass.BATTERY: {Const.PERCENTAGE},
        _DeviceClass.CO: {Const.CONCENTRATION_PARTS_PER_MILLION},
        _DeviceClass.CO2: {Const.CONCENTRATION_PARTS_PER_MILLION},
        _DeviceClass.CURRENT: set(Const.UnitOfElectricCurrent),
        _DeviceClass.DATA_RATE: set(Const.UnitOfDataRate),
        _DeviceClass.DATA_SIZE: set(Const.UnitOfInformation),
        _DeviceClass.DISTANCE: set(Const.UnitOfLength),
        _DeviceClass.DURATION: {
            Const.UnitOfTime.DAYS,
            Const.UnitOfTime.HOURS,
            Const.UnitOfTime.MINUTES,
            Const.UnitOfTime.SECONDS,
            Const.UnitOfTime.MILLISECONDS,
        },
        _DeviceClass.ENERGY: set(Const.UnitOfEnergy),
        _DeviceClass.ENERGY_STORAGE: set(Const.UnitOfEnergy),
        _DeviceClass.FREQUENCY: set(Const.UnitOfFrequency),
        _DeviceClass.GAS: {
            Const.UnitOfVolume.CENTUM_CUBIC_FEET,
            Const.UnitOfVolume.CUBIC_FEET,
            Const.UnitOfVolume.CUBIC_METERS,
        },
        _DeviceClass.HUMIDITY: {Const.PERCENTAGE},
        _DeviceClass.ILLUMINANCE: {Const.LIGHT_LUX},
        _DeviceClass.IRRADIANCE: set(Const.UnitOfIrradiance),
        _DeviceClass.MOISTURE: {Const.PERCENTAGE},
        _DeviceClass.NITROGEN_DIOXIDE: {Const.CONCENTRATION_MICROGRAMS_PER_CUBIC_METER},
        _DeviceClass.NITROGEN_MONOXIDE: {
            Const.CONCENTRATION_MICROGRAMS_PER_CUBIC_METER
        },
        _DeviceClass.NITROUS_OXIDE: {Const.CONCENTRATION_MICROGRAMS_PER_CUBIC_METER},
        _DeviceClass.OZONE: {Const.CONCENTRATION_MICROGRAMS_PER_CUBIC_METER},
        _DeviceClass.PM1: {Const.CONCENTRATION_MICROGRAMS_PER_CUBIC_METER},
        _DeviceClass.PM10: {Const.CONCENTRATION_MICROGRAMS_PER_CUBIC_METER},
        _DeviceClass.PM25: {Const.CONCENTRATION_MICROGRAMS_PER_CUBIC_METER},
        _DeviceClass.POWER_FACTOR: {Const.PERCENTAGE, None},
        _DeviceClass.POWER: {Const.UnitOfPower.WATT, Const.UnitOfPower.KILO_WATT},
        _DeviceClass.PRECIPITATION: set(Const.UnitOfPrecipitationDepth),
        _DeviceClass.PRECIPITATION_INTENSITY: set(Const.UnitOfVolumetricFlux),
        _DeviceClass.PRESSURE: set(Const.UnitOfPressure),
        _DeviceClass.REACTIVE_POWER: {Const.POWER_VOLT_AMPERE_REACTIVE},
        _DeviceClass.SIGNAL_STRENGTH: {
            Const.SIGNAL_STRENGTH_DECIBELS,
            Const.SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
        },
        _DeviceClass.SOUND_PRESSURE: set(Const.UnitOfSoundPressure),
        _DeviceClass.SPEED: set(Const.UnitOfSpeed).union(
            set(Const.UnitOfVolumetricFlux)
        ),
        _DeviceClass.SULPHUR_DIOXIDE: {Const.CONCENTRATION_MICROGRAMS_PER_CUBIC_METER},
        _DeviceClass.TEMPERATURE: set(Const.UnitOfTemperature),
        _DeviceClass.VOLATILE_ORGANIC_COMPOUNDS: {
            Const.CONCENTRATION_MICROGRAMS_PER_CUBIC_METER
        },
        _DeviceClass.VOLATILE_ORGANIC_COMPOUNDS_PARTS: {
            Const.CONCENTRATION_PARTS_PER_BILLION,
            Const.CONCENTRATION_PARTS_PER_MILLION,
        },
        _DeviceClass.VOLTAGE: set(Const.UnitOfElectricPotential),
        _DeviceClass.VOLUME: set(Const.UnitOfVolume),
        _DeviceClass.WATER: {
            Const.UnitOfVolume.CENTUM_CUBIC_FEET,
            Const.UnitOfVolume.CUBIC_FEET,
            Const.UnitOfVolume.CUBIC_METERS,
            Const.UnitOfVolume.GALLONS,
            Const.UnitOfVolume.LITERS,
        },
        _DeviceClass.WEIGHT: set(Const.UnitOfMass),
        _DeviceClass.WIND_SPEED: set(Const.UnitOfSpeed),
    }

    DEVICE_CLASS_STATE_CLASSES: dict[_DeviceClass, set[_StateClass]] = {
        _DeviceClass.APPARENT_POWER: {_StateClass.MEASUREMENT},
        _DeviceClass.AQI: {_StateClass.MEASUREMENT},
        _DeviceClass.ATMOSPHERIC_PRESSURE: {_StateClass.MEASUREMENT},
        _DeviceClass.BATTERY: {_StateClass.MEASUREMENT},
        _DeviceClass.CO: {_StateClass.MEASUREMENT},
        _DeviceClass.CO2: {_StateClass.MEASUREMENT},
        _DeviceClass.CURRENT: {_StateClass.MEASUREMENT},
        _DeviceClass.DATA_RATE: {_StateClass.MEASUREMENT},
        _DeviceClass.DATA_SIZE: set(_StateClass),
        _DeviceClass.DATE: set(),
        _DeviceClass.DISTANCE: set(_StateClass),
        _DeviceClass.DURATION: set(_StateClass),
        _DeviceClass.ENERGY: {
            _StateClass.TOTAL,
            _StateClass.TOTAL_INCREASING,
        },
        _DeviceClass.ENERGY_STORAGE: {_StateClass.MEASUREMENT},
        _DeviceClass.ENUM: set(),
        _DeviceClass.FREQUENCY: {_StateClass.MEASUREMENT},
        _DeviceClass.GAS: {_StateClass.TOTAL, _StateClass.TOTAL_INCREASING},
        _DeviceClass.HUMIDITY: {_StateClass.MEASUREMENT},
        _DeviceClass.ILLUMINANCE: {_StateClass.MEASUREMENT},
        _DeviceClass.IRRADIANCE: {_StateClass.MEASUREMENT},
        _DeviceClass.MOISTURE: {_StateClass.MEASUREMENT},
        _DeviceClass.MONETARY: {_StateClass.TOTAL},
        _DeviceClass.NITROGEN_DIOXIDE: {_StateClass.MEASUREMENT},
        _DeviceClass.NITROGEN_MONOXIDE: {_StateClass.MEASUREMENT},
        _DeviceClass.NITROUS_OXIDE: {_StateClass.MEASUREMENT},
        _DeviceClass.OZONE: {_StateClass.MEASUREMENT},
        _DeviceClass.PM1: {_StateClass.MEASUREMENT},
        _DeviceClass.PM10: {_StateClass.MEASUREMENT},
        _DeviceClass.PM25: {_StateClass.MEASUREMENT},
        _DeviceClass.POWER_FACTOR: {_StateClass.MEASUREMENT},
        _DeviceClass.POWER: {_StateClass.MEASUREMENT},
        _DeviceClass.PRECIPITATION: set(_StateClass),
        _DeviceClass.PRECIPITATION_INTENSITY: {_StateClass.MEASUREMENT},
        _DeviceClass.PRESSURE: {_StateClass.MEASUREMENT},
        _DeviceClass.REACTIVE_POWER: {_StateClass.MEASUREMENT},
        _DeviceClass.SIGNAL_STRENGTH: {_StateClass.MEASUREMENT},
        _DeviceClass.SOUND_PRESSURE: {_StateClass.MEASUREMENT},
        _DeviceClass.SPEED: {_StateClass.MEASUREMENT},
        _DeviceClass.SULPHUR_DIOXIDE: {_StateClass.MEASUREMENT},
        _DeviceClass.TEMPERATURE: {_StateClass.MEASUREMENT},
        _DeviceClass.TIMESTAMP: set(),
        _DeviceClass.VOLATILE_ORGANIC_COMPOUNDS: {_StateClass.MEASUREMENT},
        _DeviceClass.VOLATILE_ORGANIC_COMPOUNDS_PARTS: {_StateClass.MEASUREMENT},
        _DeviceClass.VOLTAGE: {_StateClass.MEASUREMENT},
        _DeviceClass.VOLUME: {
            _StateClass.TOTAL,
            _StateClass.TOTAL_INCREASING,
        },
        _DeviceClass.VOLUME_STORAGE: {_StateClass.MEASUREMENT},
        _DeviceClass.WATER: {
            _StateClass.TOTAL,
            _StateClass.TOTAL_INCREASING,
        },
        _DeviceClass.WEIGHT: {_StateClass.MEASUREMENT},
        _DeviceClass.WIND_SPEED: {_StateClass.MEASUREMENT},
    }
