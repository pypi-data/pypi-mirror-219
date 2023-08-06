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

import typing

from .const import Const
from .smart_home_controller_error import SmartHomeControllerError

_flux: typing.TypeAlias = Const.UnitOfVolumetricFlux
_length: typing.TypeAlias = Const.UnitOfLength
_mass: typing.TypeAlias = Const.UnitOfMass
_power: typing.TypeAlias = Const.UnitOfPower
_pressure: typing.TypeAlias = Const.UnitOfPressure
_speed: typing.TypeAlias = Const.UnitOfSpeed
_temperature: typing.TypeAlias = Const.UnitOfTemperature
_volume: typing.TypeAlias = Const.UnitOfVolume

# Distance conversion constants
_MM_TO_M = 0.001  # 1 mm = 0.001 m
_CM_TO_M = 0.01  # 1 cm = 0.01 m
_KM_TO_M = 1000  # 1 km = 1000 m

_IN_TO_M = 0.0254  # 1 inch = 0.0254 m
_FOOT_TO_M = _IN_TO_M * 12  # 12 inches = 1 foot (0.3048 m)
_YARD_TO_M = _FOOT_TO_M * 3  # 3 feet = 1 yard (0.9144 m)
_MILE_TO_M = _YARD_TO_M * 1760  # 1760 yard = 1 mile (1609.344 m)

_NAUTICAL_MILE_TO_M = 1852  # 1 nautical mile = 1852 m

# Duration conversion constants
_HRS_TO_SECS = 60 * 60  # 1 hr = 3600 seconds
_DAYS_TO_SECS = 24 * _HRS_TO_SECS  # 1 day = 24 hours = 86400 seconds

# Mass conversion constants
_POUND_TO_G = 453.59237
_OUNCE_TO_G = _POUND_TO_G / 16

# Pressure conversion constants
_STANDARD_GRAVITY = 9.80665
_MERCURY_DENSITY = 13.5951

# Volume conversion constants
_L_TO_CUBIC_METER = 0.001  # 1 L = 0.001 m³
_ML_TO_CUBIC_METER = 0.001 * _L_TO_CUBIC_METER  # 1 mL = 0.001 L
_GALLON_TO_CUBIC_METER = 231 * pow(_IN_TO_M, 3)  # US gallon is 231 cubic inches
_FLUID_OUNCE_TO_CUBIC_METER = _GALLON_TO_CUBIC_METER / 128  # 128 fl. oz. in a US gallon
_CUBIC_FOOT_TO_CUBIC_METER = pow(_FOOT_TO_M, 3)

# pylint: disable=unused-variable


class BaseUnitConverter:
    """Define the format of a conversion utility."""

    # pylint: disable=invalid-name
    UNIT_CLASS: str
    NORMALIZED_UNIT: str
    VALID_UNITS: set[str]

    _UNIT_CONVERSION: dict[str, float]

    @classmethod
    def convert(cls, value: float, from_unit: str, to_unit: str) -> float:
        """Convert one unit of measurement to another."""
        if from_unit == to_unit:
            return value

        try:
            from_ratio = cls._UNIT_CONVERSION[from_unit]
        except KeyError as err:
            raise SmartHomeControllerError(
                Const.UNIT_NOT_RECOGNIZED_TEMPLATE.format(from_unit, cls.UNIT_CLASS)
            ) from err

        try:
            to_ratio = cls._UNIT_CONVERSION[to_unit]
        except KeyError as err:
            raise SmartHomeControllerError(
                Const.UNIT_NOT_RECOGNIZED_TEMPLATE.format(to_unit, cls.UNIT_CLASS)
            ) from err

        new_value = value / from_ratio
        return new_value * to_ratio

    @classmethod
    def get_unit_ratio(cls, from_unit: str, to_unit: str) -> float:
        """Get unit ratio between units of measurement."""
        return cls._UNIT_CONVERSION[from_unit] / cls._UNIT_CONVERSION[to_unit]


class DistanceConverter(BaseUnitConverter):
    """Utility to convert distance values."""

    UNIT_CLASS = "distance"
    NORMALIZED_UNIT = _length.METERS
    _UNIT_CONVERSION: dict[str, float] = {
        _length.METERS: 1,
        _length.MILLIMETERS: 1 / _MM_TO_M,
        _length.CENTIMETERS: 1 / _CM_TO_M,
        _length.KILOMETERS: 1 / _KM_TO_M,
        _length.INCHES: 1 / _IN_TO_M,
        _length.FEET: 1 / _FOOT_TO_M,
        _length.YARDS: 1 / _YARD_TO_M,
        _length.MILES: 1 / _MILE_TO_M,
    }
    VALID_UNITS = {
        _length.KILOMETERS,
        _length.MILES,
        _length.FEET,
        _length.METERS,
        _length.CENTIMETERS,
        _length.MILLIMETERS,
        _length.INCHES,
        _length.YARDS,
    }


class ElectricCurrentConverter(BaseUnitConverter):
    """Utility to convert electric current values."""

    UNIT_CLASS = "electric_current"
    NORMALIZED_UNIT = Const.UnitOfElectricCurrent.AMPERE
    _UNIT_CONVERSION: dict[str | None, float] = {
        Const.UnitOfElectricCurrent.AMPERE: 1,
        Const.UnitOfElectricCurrent.MILLIAMPERE: 1e3,
    }
    VALID_UNITS = set(Const.UnitOfElectricCurrent)


class ElectricPotentialConverter(BaseUnitConverter):
    """Utility to convert electric potential values."""

    UNIT_CLASS = "voltage"
    NORMALIZED_UNIT = Const.UnitOfElectricPotential.VOLT
    _UNIT_CONVERSION: dict[str | None, float] = {
        Const.UnitOfElectricPotential.VOLT: 1,
        Const.UnitOfElectricPotential.MILLIVOLT: 1e3,
    }
    VALID_UNITS = {
        Const.UnitOfElectricPotential.VOLT,
        Const.UnitOfElectricPotential.MILLIVOLT,
    }


class MassConverter(BaseUnitConverter):
    """Utility to convert mass values."""

    UNIT_CLASS = "mass"
    NORMALIZED_UNIT = _mass.GRAMS
    _UNIT_CONVERSION: dict[str, float] = {
        _mass.MICROGRAMS: 1 * 1000 * 1000,
        _mass.MILLIGRAMS: 1 * 1000,
        _mass.GRAMS: 1,
        _mass.KILOGRAMS: 1 / 1000,
        _mass.OUNCES: 1 / _OUNCE_TO_G,
        _mass.POUNDS: 1 / _POUND_TO_G,
    }
    VALID_UNITS = {
        _mass.GRAMS,
        _mass.KILOGRAMS,
        _mass.MILLIGRAMS,
        _mass.MICROGRAMS,
        _mass.OUNCES,
        _mass.POUNDS,
    }


class PowerConverter(BaseUnitConverter):
    """Utility to convert power values."""

    UNIT_CLASS = "power"
    NORMALIZED_UNIT = _power.WATT
    _UNIT_CONVERSION: dict[str, float] = {
        _power.WATT: 1,
        _power.KILO_WATT: 1 / 1000,
    }
    VALID_UNITS = {
        _power.WATT,
        _power.KILO_WATT,
    }


class PressureConverter(BaseUnitConverter):
    """Utility to convert pressure values."""

    UNIT_CLASS = "pressure"
    NORMALIZED_UNIT = _pressure.PA
    _UNIT_CONVERSION: dict[str, float] = {
        _pressure.PA: 1,
        _pressure.HPA: 1 / 100,
        _pressure.KPA: 1 / 1000,
        _pressure.BAR: 1 / 100000,
        _pressure.CBAR: 1 / 1000,
        _pressure.MBAR: 1 / 100,
        _pressure.INHG: 1 / (_IN_TO_M * 1000 * _STANDARD_GRAVITY * _MERCURY_DENSITY),
        _pressure.PSI: 1 / 6894.757,
        _pressure.MMHG: 1 / (_MM_TO_M * 1000 * _STANDARD_GRAVITY * _MERCURY_DENSITY),
    }
    VALID_UNITS = {
        _pressure.PA,
        _pressure.HPA,
        _pressure.KPA,
        _pressure.BAR,
        _pressure.CBAR,
        _pressure.MBAR,
        _pressure.INHG,
        _pressure.PSI,
        _pressure.MMHG,
    }


class SpeedConverter(BaseUnitConverter):
    """Utility to convert speed values."""

    UNIT_CLASS = "speed"
    NORMALIZED_UNIT = _speed.METERS_PER_SECOND
    _UNIT_CONVERSION: dict[str, float] = {
        _flux.INCHES_PER_DAY: _DAYS_TO_SECS / _IN_TO_M,
        _flux.INCHES_PER_HOUR: _HRS_TO_SECS / _IN_TO_M,
        _flux.MILLIMETERS_PER_DAY: _DAYS_TO_SECS / _MM_TO_M,
        _flux.MILLIMETERS_PER_HOUR: _HRS_TO_SECS / _MM_TO_M,
        _speed.FEET_PER_SECOND: 1 / _FOOT_TO_M,
        _speed.KILOMETERS_PER_HOUR: _HRS_TO_SECS / _KM_TO_M,
        _speed.KNOTS: _HRS_TO_SECS / _NAUTICAL_MILE_TO_M,
        _speed.METERS_PER_SECOND: 1,
        _speed.MILES_PER_HOUR: _HRS_TO_SECS / _MILE_TO_M,
    }
    VALID_UNITS = {
        _flux.INCHES_PER_DAY,
        _flux.INCHES_PER_HOUR,
        _flux.MILLIMETERS_PER_DAY,
        _flux.MILLIMETERS_PER_HOUR,
        _speed.FEET_PER_SECOND,
        _speed.KILOMETERS_PER_HOUR,
        _speed.KNOTS,
        _speed.METERS_PER_SECOND,
        _speed.MILES_PER_HOUR,
    }


class TemperatureConverter(BaseUnitConverter):
    """Utility to convert temperature values."""

    UNIT_CLASS = "temperature"
    NORMALIZED_UNIT = _temperature.CELSIUS
    VALID_UNITS = {
        _temperature.CELSIUS,
        _temperature.FAHRENHEIT,
        _temperature.KELVIN,
    }
    _UNIT_CONVERSION = {
        _temperature.CELSIUS: 1.0,
        _temperature.FAHRENHEIT: 1.8,
        _temperature.KELVIN: 1.0,
    }

    @classmethod
    def convert(cls, value: float, from_unit: str, to_unit: str) -> float:
        """Convert a temperature from one unit to another.

        eg. 10°C will return 50°F

        For converting an interval between two temperatures, please use
        `convert_interval` instead.
        """
        # We cannot use the implementation from BaseUnitConverter here because the temperature
        # units do not use the same floor: 0°C, 0°F and 0K do not align
        if from_unit == to_unit:
            return value

        if from_unit == _temperature.CELSIUS:
            if to_unit == _temperature.FAHRENHEIT:
                return cls._celsius_to_fahrenheit(value)
            if to_unit == _temperature.KELVIN:
                return cls._celsius_to_kelvin(value)
            raise SmartHomeControllerError(
                Const.UNIT_NOT_RECOGNIZED_TEMPLATE.format(to_unit, cls.UNIT_CLASS)
            )

        if from_unit == _temperature.FAHRENHEIT:
            if to_unit == _temperature.CELSIUS:
                return cls._fahrenheit_to_celsius(value)
            if to_unit == _temperature.KELVIN:
                return cls._celsius_to_kelvin(cls._fahrenheit_to_celsius(value))
            raise SmartHomeControllerError(
                Const.UNIT_NOT_RECOGNIZED_TEMPLATE.format(to_unit, cls.UNIT_CLASS)
            )

        if from_unit == _temperature.KELVIN:
            if to_unit == _temperature.CELSIUS:
                return cls._kelvin_to_celsius(value)
            if to_unit == _temperature.FAHRENHEIT:
                return cls._celsius_to_fahrenheit(cls._kelvin_to_celsius(value))
            raise SmartHomeControllerError(
                Const.UNIT_NOT_RECOGNIZED_TEMPLATE.format(to_unit, cls.UNIT_CLASS)
            )
        raise SmartHomeControllerError(
            Const.UNIT_NOT_RECOGNIZED_TEMPLATE.format(from_unit, cls.UNIT_CLASS)
        )

    @classmethod
    def convert_interval(cls, interval: float, from_unit: str, to_unit: str) -> float:
        """Convert a temperature interval from one unit to another.

        eg. a 10°C interval (10°C to 20°C) will return a 18°F (50°F to 68°F) interval

        For converting a temperature value, please use `convert` as this method
        skips floor adjustment.
        """
        # We use BaseUnitConverter implementation here because we are only interested
        # in the ratio between the units.
        return super().convert(interval, from_unit, to_unit)

    @classmethod
    def _fahrenheit_to_celsius(cls, fahrenheit: float) -> float:
        """Convert a temperature in Fahrenheit to Celsius."""
        return (fahrenheit - 32.0) / 1.8

    @classmethod
    def _kelvin_to_celsius(cls, kelvin: float) -> float:
        """Convert a temperature in Kelvin to Celsius."""
        return kelvin - 273.15

    @classmethod
    def _celsius_to_fahrenheit(cls, celsius: float) -> float:
        """Convert a temperature in Celsius to Fahrenheit."""
        return celsius * 1.8 + 32.0

    @classmethod
    def _celsius_to_kelvin(cls, celsius: float) -> float:
        """Convert a temperature in Celsius to Kelvin."""
        return celsius + 273.15


class VolumeConverter(BaseUnitConverter):
    """Utility to convert volume values."""

    UNIT_CLASS = "volume"
    NORMALIZED_UNIT = _volume.CUBIC_METERS
    # Units in terms of m³
    _UNIT_CONVERSION: dict[str, float] = {
        _volume.LITERS: 1 / _L_TO_CUBIC_METER,
        _volume.MILLILITERS: 1 / _ML_TO_CUBIC_METER,
        _volume.GALLONS: 1 / _GALLON_TO_CUBIC_METER,
        _volume.FLUID_OUNCES: 1 / _FLUID_OUNCE_TO_CUBIC_METER,
        _volume.CUBIC_METERS: 1,
        _volume.CUBIC_FEET: 1 / _CUBIC_FOOT_TO_CUBIC_METER,
        _volume.CENTUM_CUBIC_FEET: 1 / (100 * _CUBIC_FOOT_TO_CUBIC_METER),
    }
    VALID_UNITS = {
        _volume.LITERS,
        _volume.MILLILITERS,
        _volume.GALLONS,
        _volume.FLUID_OUNCES,
        _volume.CUBIC_METERS,
        _volume.CUBIC_FEET,
        _volume.CENTUM_CUBIC_FEET,
    }


class DataRateConverter(BaseUnitConverter):
    """Utility to convert data rate values."""

    UNIT_CLASS = "data_rate"
    NORMALIZED_UNIT = Const.UnitOfDataRate.BITS_PER_SECOND
    # Units in terms of bits
    _UNIT_CONVERSION: dict[str | None, float] = {
        Const.UnitOfDataRate.BITS_PER_SECOND: 1,
        Const.UnitOfDataRate.KILOBITS_PER_SECOND: 1 / 1e3,
        Const.UnitOfDataRate.MEGABITS_PER_SECOND: 1 / 1e6,
        Const.UnitOfDataRate.GIGABITS_PER_SECOND: 1 / 1e9,
        Const.UnitOfDataRate.BYTES_PER_SECOND: 1 / 8,
        Const.UnitOfDataRate.KILOBYTES_PER_SECOND: 1 / 8e3,
        Const.UnitOfDataRate.MEGABYTES_PER_SECOND: 1 / 8e6,
        Const.UnitOfDataRate.GIGABYTES_PER_SECOND: 1 / 8e9,
        Const.UnitOfDataRate.KIBIBYTES_PER_SECOND: 1 / 2**13,
        Const.UnitOfDataRate.MEBIBYTES_PER_SECOND: 1 / 2**23,
        Const.UnitOfDataRate.GIBIBYTES_PER_SECOND: 1 / 2**33,
    }
    VALID_UNITS = set(Const.UnitOfDataRate)


class EnergyConverter(BaseUnitConverter):
    """Utility to convert energy values."""

    UNIT_CLASS = "energy"
    NORMALIZED_UNIT = Const.UnitOfEnergy.KILO_WATT_HOUR
    _UNIT_CONVERSION: dict[str | None, float] = {
        Const.UnitOfEnergy.WATT_HOUR: 1 * 1000,
        Const.UnitOfEnergy.KILO_WATT_HOUR: 1,
        Const.UnitOfEnergy.MEGA_WATT_HOUR: 1 / 1000,
        Const.UnitOfEnergy.MEGA_JOULE: 3.6,
        Const.UnitOfEnergy.GIGA_JOULE: 3.6 / 1000,
    }
    VALID_UNITS = {
        Const.UnitOfEnergy.WATT_HOUR,
        Const.UnitOfEnergy.KILO_WATT_HOUR,
        Const.UnitOfEnergy.MEGA_WATT_HOUR,
        Const.UnitOfEnergy.MEGA_JOULE,
        Const.UnitOfEnergy.GIGA_JOULE,
    }


class InformationConverter(BaseUnitConverter):
    """Utility to convert information values."""

    UNIT_CLASS = "information"
    NORMALIZED_UNIT = Const.UnitOfInformation.BITS
    # Units in terms of bits
    _UNIT_CONVERSION: dict[str | None, float] = {
        Const.UnitOfInformation.BITS: 1,
        Const.UnitOfInformation.KILOBITS: 1 / 1e3,
        Const.UnitOfInformation.MEGABITS: 1 / 1e6,
        Const.UnitOfInformation.GIGABITS: 1 / 1e9,
        Const.UnitOfInformation.BYTES: 1 / 8,
        Const.UnitOfInformation.KILOBYTES: 1 / 8e3,
        Const.UnitOfInformation.MEGABYTES: 1 / 8e6,
        Const.UnitOfInformation.GIGABYTES: 1 / 8e9,
        Const.UnitOfInformation.TERABYTES: 1 / 8e12,
        Const.UnitOfInformation.PETABYTES: 1 / 8e15,
        Const.UnitOfInformation.EXABYTES: 1 / 8e18,
        Const.UnitOfInformation.ZETTABYTES: 1 / 8e21,
        Const.UnitOfInformation.YOTTABYTES: 1 / 8e24,
        Const.UnitOfInformation.KIBIBYTES: 1 / 2**13,
        Const.UnitOfInformation.MEBIBYTES: 1 / 2**23,
        Const.UnitOfInformation.GIBIBYTES: 1 / 2**33,
        Const.UnitOfInformation.TEBIBYTES: 1 / 2**43,
        Const.UnitOfInformation.PEBIBYTES: 1 / 2**53,
        Const.UnitOfInformation.EXBIBYTES: 1 / 2**63,
        Const.UnitOfInformation.ZEBIBYTES: 1 / 2**73,
        Const.UnitOfInformation.YOBIBYTES: 1 / 2**83,
    }
    VALID_UNITS = set(Const.UnitOfInformation)


class UnitlessRatioConverter(BaseUnitConverter):
    """Utility to convert unitless ratios."""

    UNIT_CLASS = "unitless"
    NORMALIZED_UNIT = None
    _UNIT_CONVERSION: dict[str | None, float] = {
        None: 1,
        Const.CONCENTRATION_PARTS_PER_BILLION: 1000000000,
        Const.CONCENTRATION_PARTS_PER_MILLION: 1000000,
        Const.PERCENTAGE: 100,
    }
    VALID_UNITS = {
        None,
        Const.PERCENTAGE,
    }
