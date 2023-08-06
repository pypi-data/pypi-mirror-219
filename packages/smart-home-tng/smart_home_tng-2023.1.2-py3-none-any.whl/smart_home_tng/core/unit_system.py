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

import numbers
import typing

from .const import Const
from .sensor import Sensor
from .unit_conversion import (
    DistanceConverter,
    MassConverter,
    PressureConverter,
    SpeedConverter,
    TemperatureConverter,
    VolumeConverter,
)

_length: typing.TypeAlias = Const.UnitOfLength
_mass: typing.TypeAlias = Const.UnitOfMass
_pressure: typing.TypeAlias = Const.UnitOfPressure
_speed: typing.TypeAlias = Const.UnitOfSpeed
_temperature: typing.TypeAlias = Const.UnitOfTemperature
_volume: typing.TypeAlias = Const.UnitOfVolume

_LENGTH_UNITS: typing.Final = DistanceConverter.VALID_UNITS
_MASS_UNITS: typing.Final[set[str]] = {
    Const.UnitOfMass.POUNDS,
    Const.UnitOfMass.OUNCES,
    Const.UnitOfMass.KILOGRAMS,
    Const.UnitOfMass.GRAMS,
}

_PRESSURE_UNITS: typing.Final = PressureConverter.VALID_UNITS

_VOLUME_UNITS: typing.Final = VolumeConverter.VALID_UNITS

_WIND_SPEED_UNITS: typing.Final = SpeedConverter.VALID_UNITS

_TEMPERATURE_UNITS: typing.Final[set[str]] = {
    Const.UnitOfTemperature.FAHRENHEIT,
    Const.UnitOfTemperature.CELSIUS,
}


class UnitSystem:
    """A container for units of measure."""

    _metric = None
    _imperial = None

    LENGTH_UNITS: typing.Final = _LENGTH_UNITS
    MASS_UNITS: typing.Final = _MASS_UNITS
    PRESSURE_UNITS: typing.Final = _PRESSURE_UNITS
    SPEED_UNITS: typing.Final = _WIND_SPEED_UNITS
    TEMPERATURE_UNITS: typing.Final = _TEMPERATURE_UNITS
    VOLUME_UNITS: typing.Final = _VOLUME_UNITS

    def __init__(
        self,
        name: str,
        *,
        accumulated_precipitation: str,
        conversions: dict[tuple[Sensor.DeviceClass | str, str], str],
        length: str,
        mass: str,
        pressure: str,
        temperature: str,
        volume: str,
        wind_speed: str,
    ) -> None:
        """Initialize the unit system object."""
        errors: str = ", ".join(
            Const.UNIT_NOT_RECOGNIZED_TEMPLATE.format(unit, unit_type)
            for unit, unit_type in (
                (accumulated_precipitation, Const.ACCUMULATED_PRECIPITATION),
                (temperature, Const.TEMPERATURE),
                (length, Const.LENGTH),
                (wind_speed, Const.WIND_SPEED),
                (volume, Const.VOLUME),
                (mass, Const.MASS),
                (pressure, Const.PRESSURE),
            )
            if not self._is_valid_unit(unit, unit_type)
        )

        if errors:
            raise ValueError(errors)

        self._name = name
        self._accumulated_precipitation_unit = accumulated_precipitation
        self._temperature_unit = temperature
        self._length_unit = length
        self._mass_unit = mass
        self._pressure_unit = pressure
        self._volume_unit = volume
        self._wind_speed_unit = wind_speed
        self._conversions = conversions

    @staticmethod
    def IMPERIAL():  # pylint: disable=invalid-name
        """The imperial unit system."""
        if UnitSystem._imperial is None:
            UnitSystem._imperial = UnitSystem(
                Const.CONF_UNIT_SYSTEM_IMPERIAL,
                accumulated_precipitation=_length.INCHES,
                conversions={
                    # Convert non-USCS distances
                    ("distance", _length.CENTIMETERS): _length.INCHES,
                    ("distance", _length.KILOMETERS): _length.MILES,
                    ("distance", _length.METERS): _length.FEET,
                    ("distance", _length.MILLIMETERS): _length.INCHES,
                    # Convert non-USCS volumes of gas meters
                    ("gas", _volume.CUBIC_METERS): _volume.CUBIC_FEET,
                    # Convert non-USCS precipitation
                    ("precipitation", _length.MILLIMETERS): _length.INCHES,
                    # Convert non-USCS speeds except knots to mph
                    ("speed", _speed.METERS_PER_SECOND): _speed.MILES_PER_HOUR,
                    ("speed", _speed.KILOMETERS_PER_HOUR): _speed.MILES_PER_HOUR,
                    # Convert non-USCS volumes
                    ("volume", _volume.CUBIC_METERS): _volume.CUBIC_FEET,
                    ("volume", _volume.LITERS): _volume.GALLONS,
                    ("volume", _volume.MILLILITERS): _volume.FLUID_OUNCES,
                    # Convert non-USCS volumes of water meters
                    ("water", _volume.CUBIC_METERS): _volume.CUBIC_FEET,
                    ("water", _volume.LITERS): _volume.GALLONS,
                },
                length=_length.MILES,
                mass=_mass.POUNDS,
                pressure=_pressure.PSI,
                temperature=_temperature.FAHRENHEIT,
                volume=_volume.GALLONS,
                wind_speed=_speed.MILES_PER_HOUR,
            )
        return UnitSystem._imperial

    @staticmethod
    def METRIC():  # pylint: disable=invalid-name
        """The metric unit system."""
        if UnitSystem._metric is None:
            UnitSystem._metric = UnitSystem(
                Const.CONF_UNIT_SYSTEM_METRIC,
                accumulated_precipitation=_length.MILLIMETERS,
                conversions={
                    # Convert non-metric distances
                    ("distance", _length.FEET): _length.METERS,
                    ("distance", _length.INCHES): _length.MILLIMETERS,
                    ("distance", _length.MILES): _length.KILOMETERS,
                    ("distance", _length.YARDS): _length.METERS,
                    # Convert non-metric volumes of gas meters
                    ("gas", _volume.CUBIC_FEET): _volume.CUBIC_METERS,
                    # Convert non-metric precipitation
                    ("precipitation", _length.INCHES): _length.MILLIMETERS,
                    # Convert non-metric speeds except knots to km/h
                    ("speed", _speed.FEET_PER_SECOND): _speed.KILOMETERS_PER_HOUR,
                    ("speed", _speed.MILES_PER_HOUR): _speed.KILOMETERS_PER_HOUR,
                    # Convert non-metric volumes
                    ("volume", _volume.CUBIC_FEET): _volume.CUBIC_METERS,
                    ("volume", _volume.FLUID_OUNCES): _volume.MILLILITERS,
                    ("volume", _volume.GALLONS): _volume.LITERS,
                    # Convert non-metric volumes of water meters
                    ("water", _volume.CUBIC_FEET): _volume.CUBIC_METERS,
                    ("water", _volume.GALLONS): _volume.LITERS,
                },
                length=_length.KILOMETERS,
                mass=_mass.GRAMS,
                pressure=_pressure.PA,
                temperature=_temperature.CELSIUS,
                volume=_volume.LITERS,
                wind_speed=_speed.METERS_PER_SECOND,
            )
        return UnitSystem._metric

    @property
    def name(self) -> str:
        return self._name

    @property
    def accumulated_precipitation_unit(self) -> str:
        return self._accumulated_precipitation_unit

    @property
    def temperature_unit(self) -> str:
        return self._temperature_unit

    @property
    def length_unit(self) -> str:
        return self._length_unit

    @property
    def mass_unit(self) -> str:
        return self._mass_unit

    @property
    def pressure_unit(self) -> str:
        return self._pressure_unit

    @property
    def volume_unit(self) -> str:
        return self._volume_unit

    @property
    def wind_speed_unit(self) -> str:
        return self._wind_speed_unit

    @staticmethod
    def is_valid_unit(unit: str, unit_type: str) -> bool:
        return UnitSystem._is_valid_unit(unit, unit_type)

    @staticmethod
    def _is_valid_unit(unit: str, unit_type: str) -> bool:
        """Check if the unit is valid for it's type."""
        if unit_type == Const.LENGTH:
            units = _LENGTH_UNITS
        elif unit_type == Const.ACCUMULATED_PRECIPITATION:
            units = _LENGTH_UNITS
        elif unit_type == Const.WIND_SPEED:
            units = _WIND_SPEED_UNITS
        elif unit_type == Const.TEMPERATURE:
            units = _TEMPERATURE_UNITS
        elif unit_type == Const.MASS:
            units = _MASS_UNITS
        elif unit_type == Const.VOLUME:
            units = _VOLUME_UNITS
        elif unit_type == Const.PRESSURE:
            units = _PRESSURE_UNITS
        else:
            return False
        return unit in units

    @property
    def is_metric(self) -> bool:
        """Determine if this is the metric unit system."""
        return self._name == Const.CONF_UNIT_SYSTEM_METRIC

    def temperature(self, temperature: float, from_unit: str) -> float:
        """Convert the given temperature to this unit system."""
        if not isinstance(temperature, numbers.Number):
            raise TypeError(f"{temperature!s} is not a numeric value.")
        return TemperatureConverter.convert(
            temperature, from_unit, self._temperature_unit
        )

    def mass(self, mass: float, from_unit: str) -> float:
        """Convert the given mass to this unit system."""
        if not isinstance(mass, numbers.Number):
            raise TypeError(f"{mass!s} is not a numeric value.")
        return MassConverter.convert(mass, from_unit, self._mass_unit)

    def length(self, length: float, from_unit: str) -> float:
        """Convert the given length to this unit system."""
        if not isinstance(length, numbers.Number):
            raise TypeError(f"{length!s} is not a numeric value.")

        return DistanceConverter.convert(length, from_unit, self._length_unit)

    def accumulated_precipitation(self, precip: float, from_unit: str) -> float:
        """Convert the given length to this unit system."""
        if not isinstance(precip, numbers.Number):
            raise TypeError(f"{precip!s} is not a numeric value.")

        return DistanceConverter.convert(
            precip, from_unit, self._accumulated_precipitation_unit
        )

    def pressure(self, pressure: float, from_unit: str) -> float:
        """Convert the given pressure to this unit system."""
        if not isinstance(pressure, numbers.Number):
            raise TypeError(f"{pressure!s} is not a numeric value.")

        return PressureConverter.convert(pressure, from_unit, self._pressure_unit)

    def wind_speed(self, wind_speed: float, from_unit: str) -> float:
        """Convert the given wind_speed to this unit system."""
        if not isinstance(wind_speed, numbers.Number):
            raise TypeError(f"{wind_speed!s} is not a numeric value.")

        return SpeedConverter(wind_speed, from_unit, self.wind_speed_unit)

    def volume(self, volume: float, from_unit: str) -> float:
        """Convert the given volume to this unit system."""
        if not isinstance(volume, numbers.Number):
            raise TypeError(f"{volume!s} is not a numeric value.")

        return VolumeConverter.convert(volume, from_unit, self.volume_unit)

    def as_dict(self) -> dict[str, str]:
        """Convert the unit system to a dictionary."""
        return {
            Const.LENGTH: self.length_unit,
            Const.ACCUMULATED_PRECIPITATION: self.accumulated_precipitation_unit,
            Const.MASS: self.mass_unit,
            Const.PRESSURE: self.pressure_unit,
            Const.TEMPERATURE: self.temperature_unit,
            Const.VOLUME: self.volume_unit,
            Const.WIND_SPEED: self.wind_speed_unit,
        }

    def get_converted_unit(
        self,
        device_class: Sensor.DeviceClass | str,
        original_unit: str,
    ) -> str:
        """Return converted unit given a device class or an original unit."""
        return self._conversions.get((device_class, original_unit))
