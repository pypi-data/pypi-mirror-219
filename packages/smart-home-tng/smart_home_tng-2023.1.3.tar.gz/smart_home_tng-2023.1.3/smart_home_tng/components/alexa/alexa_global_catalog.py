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

import typing


# pylint: disable=unused-variable
class AlexaGlobalCatalog:
    """The Global Alexa catalog.

    https://developer.amazon.com/docs/device-apis/resources-and-assets.html#global-alexa-catalog

    You can use the global Alexa catalog for pre-defined names of devices,
    settings, values, and units.
    This catalog is localized into all the languages that Alexa supports.

    You can reference the following catalog of pre-defined friendly names.
    Each item in the following list is an asset identifier followed by its
    supported friendly names. The first friendly name for each identifier is
    the one displayed in the Alexa mobile app.
    """

    # Air Purifier, Air Cleaner,Clean Air Machine
    DEVICE_NAME_AIR_PURIFIER: typing.Final = "Alexa.DeviceName.AirPurifier"

    # Fan, Blower
    DEVICE_NAME_FAN: typing.Final = "Alexa.DeviceName.Fan"

    # Router, Internet Router, Network Router, Wifi Router, Net Router
    DEVICE_NAME_ROUTER: typing.Final = "Alexa.DeviceName.Router"

    # Shade, Blind, Curtain, Roller, Shutter, Drape, Awning, Window shade, Interior blind
    DEVICE_NAME_SHADE: typing.Final = "Alexa.DeviceName.Shade"

    # Shower
    DEVICE_NAME_SHOWER: typing.Final = "Alexa.DeviceName.Shower"

    # Space Heater, Portable Heater
    DEVICE_NAME_SPACE_HEATER: typing.Final = "Alexa.DeviceName.SpaceHeater"

    # Washer, Washing Machine
    DEVICE_NAME_WASHER: typing.Final = "Alexa.DeviceName.Washer"

    # 2.4G Guest Wi-Fi, 2.4G Guest Network, Guest Network 2.4G, 2G Guest Wifi
    SETTING_2G_GUEST_WIFI: typing.Final = "Alexa.Setting.2GGuestWiFi"

    # 5G Guest Wi-Fi, 5G Guest Network, Guest Network 5G, 5G Guest Wifi
    SETTING_5G_GUEST_WIFI: typing.Final = "Alexa.Setting.5GGuestWiFi"

    # Auto, Automatic, Automatic Mode, Auto Mode
    SETTING_AUTO: typing.Final = "Alexa.Setting.Auto"

    # Direction
    SETTING_DIRECTION: typing.Final = "Alexa.Setting.Direction"

    # Dry Cycle, Dry Preset, Dry Setting, Dryer Cycle, Dryer Preset, Dryer Setting
    SETTING_DRY_CYCLE: typing.Final = "Alexa.Setting.DryCycle"

    # Fan Speed, Airflow speed, Wind Speed, Air speed, Air velocity
    SETTING_FAN_SPEED: typing.Final = "Alexa.Setting.FanSpeed"

    # Guest Wi-fi, Guest Network, Guest Net
    SETTING_GUEST_WIFI: typing.Final = "Alexa.Setting.GuestWiFi"

    # Heat
    SETTING_HEAT: typing.Final = "Alexa.Setting.Heat"

    # Mode
    SETTING_MODE: typing.Final = "Alexa.Setting.Mode"

    # Night, Night Mode
    SETTING_NIGHT: typing.Final = "Alexa.Setting.Night"

    # Opening, Height, Lift, Width
    SETTING_OPENING: typing.Final = "Alexa.Setting.Opening"

    # Oscillate, Swivel, Oscillation, Spin, Back and forth
    SETTING_OSCILLATE: typing.Final = "Alexa.Setting.Oscillate"

    # Preset, Setting
    SETTING_PRESET: typing.Final = "Alexa.Setting.Preset"

    # Quiet, Quiet Mode, Noiseless, Silent
    SETTING_QUIET: typing.Final = "Alexa.Setting.Quiet"

    # Temperature, Temp
    SETTING_TEMPERATURE: typing.Final = "Alexa.Setting.Temperature"

    # Wash Cycle, Wash Preset, Wash setting
    SETTING_WASH_CYCLE: typing.Final = "Alexa.Setting.WashCycle"

    # Water Temperature, Water Temp, Water Heat
    SETTING_WATER_TEMPERATURE: typing.Final = "Alexa.Setting.WaterTemperature"

    # Handheld Shower, Shower Wand, Hand Shower
    SHOWER_HAND_HELD: typing.Final = "Alexa.Shower.HandHeld"

    # Rain Head, Overhead shower, Rain Shower, Rain Spout, Rain Faucet
    SHOWER_RAIN_HEAD: typing.Final = "Alexa.Shower.RainHead"

    # Degrees, Degree
    UNIT_ANGLE_DEGREES: typing.Final = "Alexa.Unit.Angle.Degrees"

    # Radians, Radian
    UNIT_ANGLE_RADIANS: typing.Final = "Alexa.Unit.Angle.Radians"

    # Feet, Foot
    UNIT_DISTANCE_FEET: typing.Final = "Alexa.Unit.Distance.Feet"

    # Inches, Inch
    UNIT_DISTANCE_INCHES: typing.Final = "Alexa.Unit.Distance.Inches"

    # Kilometers
    UNIT_DISTANCE_KILOMETERS: typing.Final = "Alexa.Unit.Distance.Kilometers"

    # Meters, Meter, m
    UNIT_DISTANCE_METERS: typing.Final = "Alexa.Unit.Distance.Meters"

    # Miles, Mile
    UNIT_DISTANCE_MILES: typing.Final = "Alexa.Unit.Distance.Miles"

    # Yards, Yard
    UNIT_DISTANCE_YARDS: typing.Final = "Alexa.Unit.Distance.Yards"

    # Grams, Gram, g
    UNIT_MASS_GRAMS: typing.Final = "Alexa.Unit.Mass.Grams"

    # Kilograms, Kilogram, kg
    UNIT_MASS_KILOGRAMS: typing.Final = "Alexa.Unit.Mass.Kilograms"

    # Percent
    UNIT_PERCENT: typing.Final = "Alexa.Unit.Percent"

    # Celsius, Degrees Celsius, Degrees, C, Centigrade, Degrees Centigrade
    UNIT_TEMPERATURE_CELSIUS: typing.Final = "Alexa.Unit.Temperature.Celsius"

    # Degrees, Degree
    UNIT_TEMPERATURE_DEGREES: typing.Final = "Alexa.Unit.Temperature.Degrees"

    # Fahrenheit, Degrees Fahrenheit, Degrees F, Degrees, F
    UNIT_TEMPERATURE_FAHRENHEIT: typing.Final = "Alexa.Unit.Temperature.Fahrenheit"

    # Kelvin, Degrees Kelvin, Degrees K, Degrees, K
    UNIT_TEMPERATURE_KELVIN: typing.Final = "Alexa.Unit.Temperature.Kelvin"

    # Cubic Feet, Cubic Foot
    UNIT_VOLUME_CUBIC_FEET: typing.Final = "Alexa.Unit.Volume.CubicFeet"

    # Cubic Meters, Cubic Meter, Meters Cubed
    UNIT_VOLUME_CUBIC_METERS: typing.Final = "Alexa.Unit.Volume.CubicMeters"

    # Gallons, Gallon
    UNIT_VOLUME_GALLONS: typing.Final = "Alexa.Unit.Volume.Gallons"

    # Liters, Liter, L
    UNIT_VOLUME_LITERS: typing.Final = "Alexa.Unit.Volume.Liters"

    # Pints, Pint
    UNIT_VOLUME_PINTS: typing.Final = "Alexa.Unit.Volume.Pints"

    # Quarts, Quart
    UNIT_VOLUME_QUARTS: typing.Final = "Alexa.Unit.Volume.Quarts"

    # Ounces, Ounce, oz
    UNIT_WEIGHT_OUNCES: typing.Final = "Alexa.Unit.Weight.Ounces"

    # Pounds, Pound, lbs
    UNIT_WEIGHT_POUNDS: typing.Final = "Alexa.Unit.Weight.Pounds"

    # Close
    VALUE_CLOSE: typing.Final = "Alexa.Value.Close"

    # Delicates, Delicate
    VALUE_DELICATE: typing.Final = "Alexa.Value.Delicate"

    # High
    VALUE_HIGH: typing.Final = "Alexa.Value.High"

    # Low
    VALUE_LOW: typing.Final = "Alexa.Value.Low"

    # Maximum, Max
    VALUE_MAXIMUM: typing.Final = "Alexa.Value.Maximum"

    # Medium, Mid
    VALUE_MEDIUM: typing.Final = "Alexa.Value.Medium"

    # Minimum, Min
    VALUE_MINIMUM: typing.Final = "Alexa.Value.Minimum"

    # Open
    VALUE_OPEN: typing.Final = "Alexa.Value.Open"

    # Quick Wash, Fast Wash, Wash Quickly, Speed Wash
    VALUE_QUICK_WASH: typing.Final = "Alexa.Value.QuickWash"
