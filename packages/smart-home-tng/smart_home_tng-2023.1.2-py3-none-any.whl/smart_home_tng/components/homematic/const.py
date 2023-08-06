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

import typing


# pylint: disable=unused-variable
class Const:
    """Constants for the homematic component."""

    DISCOVER_SWITCHES: typing.Final = "homematic.switch"
    DISCOVER_LIGHTS: typing.Final = "homematic.light"
    DISCOVER_SENSORS: typing.Final = "homematic.sensor"
    DISCOVER_BINARY_SENSORS: typing.Final = "homematic.binary_sensor"
    DISCOVER_COVER: typing.Final = "homematic.cover"
    DISCOVER_CLIMATE: typing.Final = "homematic.climate"
    DISCOVER_LOCKS: typing.Final = "homematic.locks"
    DISCOVER_BATTERY: typing.Final = "homematic.battery"

    ATTR_DISCOVER_DEVICES: typing.Final = "devices"
    ATTR_PARAM: typing.Final = "param"
    ATTR_CHANNEL: typing.Final = "channel"
    ATTR_ADDRESS: typing.Final = "address"
    ATTR_DEVICE_TYPE: typing.Final = "device_type"
    ATTR_VALUE: typing.Final = "value"
    ATTR_VALUE_TYPE: typing.Final = "value_type"
    ATTR_INTERFACE: typing.Final = "interface"
    ATTR_ERRORCODE: typing.Final = "error"
    ATTR_MESSAGE: typing.Final = "message"
    ATTR_UNIQUE_ID: typing.Final = "unique_id"
    ATTR_PARAMSET_KEY: typing.Final = "paramset_key"
    ATTR_PARAMSET: typing.Final = "paramset"
    ATTR_RX_MODE: typing.Final = "rx_mode"
    ATTR_DISCOVERY_TYPE: typing.Final = "discovery_type"
    ATTR_LOW_BAT: typing.Final = "LOW_BAT"
    ATTR_LOWBAT: typing.Final = "LOWBAT"

    EVENT_KEYPRESS: typing.Final = "homematic.keypress"
    EVENT_IMPULSE: typing.Final = "homematic.impulse"
    EVENT_ERROR: typing.Final = "homematic.error"

    SERVICE_VIRTUALKEY: typing.Final = "virtualkey"
    SERVICE_RECONNECT: typing.Final = "reconnect"
    SERVICE_SET_VARIABLE_VALUE: typing.Final = "set_variable_value"
    SERVICE_SET_DEVICE_VALUE: typing.Final = "set_device_value"
    SERVICE_SET_INSTALL_MODE: typing.Final = "set_install_mode"
    SERVICE_PUT_PARAMSET: typing.Final = "put_paramset"

    HM_DEVICE_TYPES: typing.Final = {
        DISCOVER_SWITCHES: [
            "Switch",
            "SwitchPowermeter",
            "IOSwitch",
            "IOSwitchNoInhibit",
            "IPSwitch",
            "IPSwitchRssiDevice",
            "RFSiren",
            "IPSwitchPowermeter",
            "HMWIOSwitch",
            "Rain",
            "EcoLogic",
            "IPKeySwitchPowermeter",
            "IPGarage",
            "IPKeySwitch",
            "IPKeySwitchLevel",
            "IPMultiIO",
            "IPWSwitch",
            "IOSwitchWireless",
            "IPSwitchRssiDevice",
            "IPWIODevice",
            "IPSwitchBattery",
            "IPMultiIOPCB",
            "IPGarageSwitch",
            "IPWHS2",
        ],
        DISCOVER_LIGHTS: [
            "Dimmer",
            "KeyDimmer",
            "IPKeyDimmer",
            "IPDimmer",
            "ColorEffectLight",
            "IPKeySwitchLevel",
            "ColdWarmDimmer",
            "IPWDimmer",
        ],
        DISCOVER_SENSORS: [
            "SwitchPowermeter",
            "Motion",
            "MotionV2",
            "MotionIPV2",
            "MotionIPContactSabotage",
            "RemoteMotion",
            "MotionIP",
            "ThermostatWall",
            "AreaThermostat",
            "WaterSensor",
            "PowermeterGas",
            "LuxSensor",
            "WeatherSensor",
            "WeatherStation",
            "ThermostatWall2",
            "TemperatureDiffSensor",
            "TemperatureSensor",
            "CO2Sensor",
            "IPSwitchPowermeter",
            "HMWIOSwitch",
            "FillingLevel",
            "ValveDrive",
            "EcoLogic",
            "IPThermostatWall",
            "IPSmoke",
            "RFSiren",
            "PresenceIP",
            "IPAreaThermostat",
            "IPWeatherSensor",
            "IPPassageSensor",
            "IPKeySwitchPowermeter",
            "IPThermostatWall230V",
            "IPWeatherSensorPlus",
            "IPWeatherSensorBasic",
            "IPBrightnessSensor",
            "IPGarage",
            "UniversalSensor",
            "IPMultiIO",
            "IPThermostatWall2",
            "IPRemoteMotionV2",
            "HBUNISenWEA",
            "PresenceIPW",
            "IPRainSensor",
            "ValveBox",
            "IPKeyBlind",
            "IPKeyBlindTilt",
            "IPLanRouter",
            "TempModuleSTE2",
            "IPMultiIOPCB",
            "ValveBoxW",
            "CO2SensorIP",
            "IPLockDLD",
            "ParticulateMatterSensorIP",
            "IPRemoteMotionV2W",
        ],
        DISCOVER_CLIMATE: [
            "Thermostat",
            "ThermostatWall",
            "MAXThermostat",
            "ThermostatWall2",
            "MAXWallThermostat",
            "IPThermostat",
            "IPThermostatWall",
            "ThermostatGroup",
            "IPThermostatWall230V",
            "IPThermostatWall2",
            "IPWThermostatWall",
        ],
        DISCOVER_BINARY_SENSORS: [
            "ShutterContact",
            "Smoke",
            "SmokeV2",
            "SmokeV2Team",
            "Motion",
            "MotionV2",
            "MotionIP",
            "MotionIPV2",
            "MotionIPContactSabotage",
            "RemoteMotion",
            "WeatherSensor",
            "TiltSensor",
            "IPShutterContact",
            "HMWIOSwitch",
            "MaxShutterContact",
            "Rain",
            "WiredSensor",
            "PresenceIP",
            "PresenceIPW",
            "IPWeatherSensor",
            "IPPassageSensor",
            "SmartwareMotion",
            "IPWeatherSensorPlus",
            "WaterIP",
            "IPMultiIO",
            "TiltIP",
            "IPShutterContactSabotage",
            "IPContact",
            "IPRemoteMotionV2",
            "IPWInputDevice",
            "IPWMotionDection",
            "IPAlarmSensor",
            "IPRainSensor",
            "IPLanRouter",
            "IPMultiIOPCB",
            "IPWHS2",
            "IPRemoteMotionV2W",
        ],
        DISCOVER_COVER: [
            "Blind",
            "KeyBlind",
            "IPKeyBlind",
            "IPKeyBlindTilt",
            "IPGarage",
            "IPKeyBlindMulti",
            "IPWKeyBlindMulti",
        ],
        DISCOVER_LOCKS: ["KeyMatic"],
    }

    HM_IGNORE_DISCOVERY_NODE: typing.Final = ["ACTUAL_TEMPERATURE", "ACTUAL_HUMIDITY"]

    HM_IGNORE_DISCOVERY_NODE_EXCEPTIONS: typing.Final = {
        "ACTUAL_TEMPERATURE": [
            "IPAreaThermostat",
            "IPWeatherSensor",
            "IPWeatherSensorPlus",
            "IPWeatherSensorBasic",
            "IPThermostatWall",
            "IPThermostatWall2",
            "ParticulateMatterSensorIP",
            "CO2SensorIP",
            "TempModuleSTE2",
        ]
    }

    HM_ATTRIBUTE_SUPPORT: typing.Final = {
        "LOWBAT": ["battery", {0: "High", 1: "Low"}],
        "LOW_BAT": ["battery", {0: "High", 1: "Low"}],
        "ERROR": ["error", {0: "No"}],
        "ERROR_SABOTAGE": ["sabotage", {0: "No", 1: "Yes"}],
        "SABOTAGE": ["sabotage", {0: "No", 1: "Yes"}],
        "RSSI_PEER": ["rssi_peer", {}],
        "RSSI_DEVICE": ["rssi_device", {}],
        "VALVE_STATE": ["valve", {}],
        "LEVEL": ["level", {}],
        "BATTERY_STATE": ["battery", {}],
        "CONTROL_MODE": [
            "mode",
            {
                0: "Auto",
                1: "Manual",
                2: "Away",
                3: "Boost",
                4: "Comfort",
                5: "Lowering",
            },
        ],
        "POWER": ["power", {}],
        "CURRENT": ["current", {}],
        "VOLTAGE": ["voltage", {}],
        "OPERATING_VOLTAGE": ["voltage", {}],
        "WORKING": ["working", {0: "No", 1: "Yes"}],
        "STATE_UNCERTAIN": ["state_uncertain", {}],
        "SENDERID": ["last_senderid", {}],
        "SENDERADDRESS": ["last_senderaddress", {}],
        "ERROR_ALARM_TEST": ["error_alarm_test", {0: "No", 1: "Yes"}],
        "ERROR_SMOKE_CHAMBER": ["error_smoke_chamber", {0: "No", 1: "Yes"}],
    }

    HM_PRESS_EVENTS: typing.Final = [
        "PRESS_SHORT",
        "PRESS_LONG",
        "PRESS_CONT",
        "PRESS_LONG_RELEASE",
        "PRESS",
    ]

    HM_IMPULSE_EVENTS: typing.Final = ["SEQUENCE_OK"]

    CONF_RESOLVENAMES_OPTIONS: typing.Final = ["metadata", "json", "xml", False]

    DATA_HOMEMATIC: typing.Final = "homematic"
    DATA_STORE: typing.Final = "homematic_store"
    DATA_CONF: typing.Final = "homematic_conf"

    CONF_INTERFACES: typing.Final = "interfaces"
    CONF_LOCAL_IP: typing.Final = "local_ip"
    CONF_LOCAL_PORT: typing.Final = "local_port"
    CONF_CALLBACK_IP: typing.Final = "callback_ip"
    CONF_CALLBACK_PORT: typing.Final = "callback_port"
    CONF_RESOLVENAMES: typing.Final = "resolvenames"
    CONF_JSONPORT: typing.Final = "jsonport"
