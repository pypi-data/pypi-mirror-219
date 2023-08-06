"""
Binary Sensor Component for Smart Home - The Next Generation.

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
import logging
import typing
import voluptuous as vol

from ... import core

_cv: typing.TypeAlias = core.ConfigValidation


_DEVICE_CLASS_NONE: typing.Final = "none"
_CONF_IS_BAT_LOW: typing.Final = "is_bat_low"
_CONF_IS_NOT_BAT_LOW: typing.Final = "is_not_bat_low"
_CONF_IS_CHARGING: typing.Final = "is_charging"
_CONF_IS_NOT_CHARGING: typing.Final = "is_not_charging"
_CONF_IS_CO: typing.Final = "is_co"
_CONF_IS_NO_CO: typing.Final = "is_no_co"
_CONF_IS_COLD: typing.Final = "is_cold"
_CONF_IS_NOT_COLD: typing.Final = "is_not_cold"
_CONF_IS_CONNECTED: typing.Final = "is_connected"
_CONF_IS_NOT_CONNECTED: typing.Final = "is_not_connected"
_CONF_IS_GAS: typing.Final = "is_gas"
_CONF_IS_NO_GAS: typing.Final = "is_no_gas"
_CONF_IS_HOT: typing.Final = "is_hot"
_CONF_IS_NOT_HOT: typing.Final = "is_not_hot"
_CONF_IS_LIGHT: typing.Final = "is_light"
_CONF_IS_NO_LIGHT: typing.Final = "is_no_light"
_CONF_IS_LOCKED: typing.Final = "is_locked"
_CONF_IS_NOT_LOCKED: typing.Final = "is_not_locked"
_CONF_IS_MOIST: typing.Final = "is_moist"
_CONF_IS_NOT_MOIST: typing.Final = "is_not_moist"
_CONF_IS_MOTION: typing.Final = "is_motion"
_CONF_IS_NO_MOTION: typing.Final = "is_no_motion"
_CONF_IS_MOVING: typing.Final = "is_moving"
_CONF_IS_NOT_MOVING: typing.Final = "is_not_moving"
_CONF_IS_OCCUPIED: typing.Final = "is_occupied"
_CONF_IS_NOT_OCCUPIED: typing.Final = "is_not_occupied"
_CONF_IS_PLUGGED_IN: typing.Final = "is_plugged_in"
_CONF_IS_NOT_PLUGGED_IN: typing.Final = "is_not_plugged_in"
_CONF_IS_POWERED: typing.Final = "is_powered"
_CONF_IS_NOT_POWERED: typing.Final = "is_not_powered"
_CONF_IS_PRESENT: typing.Final = "is_present"
_CONF_IS_NOT_PRESENT: typing.Final = "is_not_present"
_CONF_IS_PROBLEM: typing.Final = "is_problem"
_CONF_IS_NO_PROBLEM: typing.Final = "is_no_problem"
_CONF_IS_RUNNING: typing.Final = "is_running"
_CONF_IS_NOT_RUNNING: typing.Final = "is_not_running"
_CONF_IS_UNSAFE: typing.Final = "is_unsafe"
_CONF_IS_NOT_UNSAFE: typing.Final = "is_not_unsafe"
_CONF_IS_SMOKE: typing.Final = "is_smoke"
_CONF_IS_NO_SMOKE: typing.Final = "is_no_smoke"
_CONF_IS_SOUND: typing.Final = "is_sound"
_CONF_IS_NO_SOUND: typing.Final = "is_no_sound"
_CONF_IS_TAMPERED: typing.Final = "is_tampered"
_CONF_IS_NOT_TAMPERED: typing.Final = "is_not_tampered"
_CONF_IS_UPDATE: typing.Final = "is_update"
_CONF_IS_NO_UPDATE: typing.Final = "is_no_update"
_CONF_IS_VIBRATION: typing.Final = "is_vibration"
_CONF_IS_NO_VIBRATION: typing.Final = "is_no_vibration"
_CONF_IS_OPEN: typing.Final = "is_open"
_CONF_IS_NOT_OPEN: typing.Final = "is_not_open"

_IS_ON: typing.Final = [
    _CONF_IS_BAT_LOW,
    _CONF_IS_CHARGING,
    _CONF_IS_CO,
    _CONF_IS_COLD,
    _CONF_IS_CONNECTED,
    _CONF_IS_GAS,
    _CONF_IS_HOT,
    _CONF_IS_LIGHT,
    _CONF_IS_NOT_LOCKED,
    _CONF_IS_MOIST,
    _CONF_IS_MOTION,
    _CONF_IS_MOVING,
    _CONF_IS_OCCUPIED,
    _CONF_IS_OPEN,
    _CONF_IS_PLUGGED_IN,
    _CONF_IS_POWERED,
    _CONF_IS_PRESENT,
    _CONF_IS_PROBLEM,
    _CONF_IS_RUNNING,
    _CONF_IS_SMOKE,
    _CONF_IS_SOUND,
    _CONF_IS_TAMPERED,
    _CONF_IS_UPDATE,
    _CONF_IS_UNSAFE,
    _CONF_IS_VIBRATION,
    core.Toggle.CONF_IS_ON,
]

_IS_OFF: typing.Final = [
    _CONF_IS_NOT_BAT_LOW,
    _CONF_IS_NOT_CHARGING,
    _CONF_IS_NOT_COLD,
    _CONF_IS_NOT_CONNECTED,
    _CONF_IS_NOT_HOT,
    _CONF_IS_LOCKED,
    _CONF_IS_NOT_MOIST,
    _CONF_IS_NOT_MOVING,
    _CONF_IS_NOT_OCCUPIED,
    _CONF_IS_NOT_OPEN,
    _CONF_IS_NOT_PLUGGED_IN,
    _CONF_IS_NOT_POWERED,
    _CONF_IS_NOT_PRESENT,
    _CONF_IS_NOT_TAMPERED,
    _CONF_IS_NOT_UNSAFE,
    _CONF_IS_NO_CO,
    _CONF_IS_NO_GAS,
    _CONF_IS_NO_LIGHT,
    _CONF_IS_NO_MOTION,
    _CONF_IS_NO_PROBLEM,
    _CONF_IS_NOT_RUNNING,
    _CONF_IS_NO_SMOKE,
    _CONF_IS_NO_SOUND,
    _CONF_IS_NO_UPDATE,
    _CONF_IS_NO_VIBRATION,
    core.Toggle.CONF_IS_OFF,
]

_ENTITY_CONDITIONS: typing.Final = {
    core.BinarySensor.DeviceClass.BATTERY: [
        {core.Const.CONF_TYPE: _CONF_IS_BAT_LOW},
        {core.Const.CONF_TYPE: _CONF_IS_NOT_BAT_LOW},
    ],
    core.BinarySensor.DeviceClass.BATTERY_CHARGING: [
        {core.Const.CONF_TYPE: _CONF_IS_CHARGING},
        {core.Const.CONF_TYPE: _CONF_IS_NOT_CHARGING},
    ],
    core.BinarySensor.DeviceClass.CO: [
        {core.Const.CONF_TYPE: _CONF_IS_CO},
        {core.Const.CONF_TYPE: _CONF_IS_NO_CO},
    ],
    core.BinarySensor.DeviceClass.COLD: [
        {core.Const.CONF_TYPE: _CONF_IS_COLD},
        {core.Const.CONF_TYPE: _CONF_IS_NOT_COLD},
    ],
    core.BinarySensor.DeviceClass.CONNECTIVITY: [
        {core.Const.CONF_TYPE: _CONF_IS_CONNECTED},
        {core.Const.CONF_TYPE: _CONF_IS_NOT_CONNECTED},
    ],
    core.BinarySensor.DeviceClass.DOOR: [
        {core.Const.CONF_TYPE: _CONF_IS_OPEN},
        {core.Const.CONF_TYPE: _CONF_IS_NOT_OPEN},
    ],
    core.BinarySensor.DeviceClass.GARAGE_DOOR: [
        {core.Const.CONF_TYPE: _CONF_IS_OPEN},
        {core.Const.CONF_TYPE: _CONF_IS_NOT_OPEN},
    ],
    core.BinarySensor.DeviceClass.GAS: [
        {core.Const.CONF_TYPE: _CONF_IS_GAS},
        {core.Const.CONF_TYPE: _CONF_IS_NO_GAS},
    ],
    core.BinarySensor.DeviceClass.HEAT: [
        {core.Const.CONF_TYPE: _CONF_IS_HOT},
        {core.Const.CONF_TYPE: _CONF_IS_NOT_HOT},
    ],
    core.BinarySensor.DeviceClass.LIGHT: [
        {core.Const.CONF_TYPE: _CONF_IS_LIGHT},
        {core.Const.CONF_TYPE: _CONF_IS_NO_LIGHT},
    ],
    core.BinarySensor.DeviceClass.LOCK: [
        {core.Const.CONF_TYPE: _CONF_IS_LOCKED},
        {core.Const.CONF_TYPE: _CONF_IS_NOT_LOCKED},
    ],
    core.BinarySensor.DeviceClass.MOISTURE: [
        {core.Const.CONF_TYPE: _CONF_IS_MOIST},
        {core.Const.CONF_TYPE: _CONF_IS_NOT_MOIST},
    ],
    core.BinarySensor.DeviceClass.MOTION: [
        {core.Const.CONF_TYPE: _CONF_IS_MOTION},
        {core.Const.CONF_TYPE: _CONF_IS_NO_MOTION},
    ],
    core.BinarySensor.DeviceClass.MOVING: [
        {core.Const.CONF_TYPE: _CONF_IS_MOVING},
        {core.Const.CONF_TYPE: _CONF_IS_NOT_MOVING},
    ],
    core.BinarySensor.DeviceClass.OCCUPANCY: [
        {core.Const.CONF_TYPE: _CONF_IS_OCCUPIED},
        {core.Const.CONF_TYPE: _CONF_IS_NOT_OCCUPIED},
    ],
    core.BinarySensor.DeviceClass.OPENING: [
        {core.Const.CONF_TYPE: _CONF_IS_OPEN},
        {core.Const.CONF_TYPE: _CONF_IS_NOT_OPEN},
    ],
    core.BinarySensor.DeviceClass.PLUG: [
        {core.Const.CONF_TYPE: _CONF_IS_PLUGGED_IN},
        {core.Const.CONF_TYPE: _CONF_IS_NOT_PLUGGED_IN},
    ],
    core.BinarySensor.DeviceClass.POWER: [
        {core.Const.CONF_TYPE: _CONF_IS_POWERED},
        {core.Const.CONF_TYPE: _CONF_IS_NOT_POWERED},
    ],
    core.BinarySensor.DeviceClass.PRESENCE: [
        {core.Const.CONF_TYPE: _CONF_IS_PRESENT},
        {core.Const.CONF_TYPE: _CONF_IS_NOT_PRESENT},
    ],
    core.BinarySensor.DeviceClass.PROBLEM: [
        {core.Const.CONF_TYPE: _CONF_IS_PROBLEM},
        {core.Const.CONF_TYPE: _CONF_IS_NO_PROBLEM},
    ],
    core.BinarySensor.DeviceClass.RUNNING: [
        {core.Const.CONF_TYPE: _CONF_IS_RUNNING},
        {core.Const.CONF_TYPE: _CONF_IS_NOT_RUNNING},
    ],
    core.BinarySensor.DeviceClass.SAFETY: [
        {core.Const.CONF_TYPE: _CONF_IS_UNSAFE},
        {core.Const.CONF_TYPE: _CONF_IS_NOT_UNSAFE},
    ],
    core.BinarySensor.DeviceClass.SMOKE: [
        {core.Const.CONF_TYPE: _CONF_IS_SMOKE},
        {core.Const.CONF_TYPE: _CONF_IS_NO_SMOKE},
    ],
    core.BinarySensor.DeviceClass.SOUND: [
        {core.Const.CONF_TYPE: _CONF_IS_SOUND},
        {core.Const.CONF_TYPE: _CONF_IS_NO_SOUND},
    ],
    core.BinarySensor.DeviceClass.TAMPER: [
        {core.Const.CONF_TYPE: _CONF_IS_TAMPERED},
        {core.Const.CONF_TYPE: _CONF_IS_NOT_TAMPERED},
    ],
    core.BinarySensor.DeviceClass.UPDATE: [
        {core.Const.CONF_TYPE: _CONF_IS_UPDATE},
        {core.Const.CONF_TYPE: _CONF_IS_NO_UPDATE},
    ],
    core.BinarySensor.DeviceClass.VIBRATION: [
        {core.Const.CONF_TYPE: _CONF_IS_VIBRATION},
        {core.Const.CONF_TYPE: _CONF_IS_NO_VIBRATION},
    ],
    core.BinarySensor.DeviceClass.WINDOW: [
        {core.Const.CONF_TYPE: _CONF_IS_OPEN},
        {core.Const.CONF_TYPE: _CONF_IS_NOT_OPEN},
    ],
    _DEVICE_CLASS_NONE: [
        {core.Const.CONF_TYPE: core.Toggle.CONF_IS_ON},
        {core.Const.CONF_TYPE: core.Toggle.CONF_IS_OFF},
    ],
}

_CONDITION_SCHEMA: typing.Final = _cv.DEVICE_CONDITION_BASE_SCHEMA.extend(
    {
        vol.Required(core.Const.CONF_ENTITY_ID): _cv.entity_id,
        vol.Required(core.Const.CONF_TYPE): vol.In(_IS_OFF + _IS_ON),
        vol.Optional(core.Const.CONF_FOR): _cv.positive_time_period_dict,
    }
)

_CONF_BAT_LOW: typing.Final = "bat_low"
_CONF_NOT_BAT_LOW: typing.Final = "not_bat_low"
_CONF_CHARGING: typing.Final = "charging"
_CONF_NOT_CHARGING: typing.Final = "not_charging"
_CONF_CO: typing.Final = "co"
_CONF_NO_CO: typing.Final = "no_co"
_CONF_COLD: typing.Final = "cold"
_CONF_NOT_COLD: typing.Final = "not_cold"
_CONF_CONNECTED: typing.Final = "connected"
_CONF_NOT_CONNECTED: typing.Final = "not_connected"
_CONF_GAS: typing.Final = "gas"
_CONF_NO_GAS: typing.Final = "no_gas"
_CONF_HOT: typing.Final = "hot"
_CONF_NOT_HOT: typing.Final = "not_hot"
_CONF_LIGHT: typing.Final = "light"
_CONF_NO_LIGHT: typing.Final = "no_light"
_CONF_LOCKED: typing.Final = "locked"
_CONF_NOT_LOCKED: typing.Final = "not_locked"
_CONF_MOIST: typing.Final = "moist"
_CONF_NOT_MOIST: typing.Final = "not_moist"
_CONF_MOTION: typing.Final = "motion"
_CONF_NO_MOTION: typing.Final = "no_motion"
_CONF_MOVING: typing.Final = "moving"
_CONF_NOT_MOVING: typing.Final = "not_moving"
_CONF_OCCUPIED: typing.Final = "occupied"
_CONF_NOT_OCCUPIED: typing.Final = "not_occupied"
_CONF_PLUGGED_IN: typing.Final = "plugged_in"
_CONF_NOT_PLUGGED_IN: typing.Final = "not_plugged_in"
_CONF_POWERED: typing.Final = "powered"
_CONF_NOT_POWERED: typing.Final = "not_powered"
_CONF_PRESENT: typing.Final = "present"
_CONF_NOT_PRESENT: typing.Final = "not_present"
_CONF_PROBLEM: typing.Final = "problem"
_CONF_NO_PROBLEM: typing.Final = "no_problem"
_CONF_RUNNING: typing.Final = "running"
_CONF_NOT_RUNNING: typing.Final = "not_running"
_CONF_UNSAFE: typing.Final = "unsafe"
_CONF_NOT_UNSAFE: typing.Final = "not_unsafe"
_CONF_SMOKE: typing.Final = "smoke"
_CONF_NO_SMOKE: typing.Final = "no_smoke"
_CONF_SOUND: typing.Final = "sound"
_CONF_NO_SOUND: typing.Final = "no_sound"
_CONF_TAMPERED: typing.Final = "tampered"
_CONF_NOT_TAMPERED: typing.Final = "not_tampered"
_CONF_UPDATE: typing.Final = "update"
_CONF_NO_UPDATE: typing.Final = "no_update"
_CONF_VIBRATION: typing.Final = "vibration"
_CONF_NO_VIBRATION: typing.Final = "no_vibration"
_CONF_OPENED: typing.Final = "opened"
_CONF_NOT_OPENED: typing.Final = "not_opened"


_TURNED_ON: typing.Final = [
    _CONF_BAT_LOW,
    _CONF_CHARGING,
    _CONF_CO,
    _CONF_COLD,
    _CONF_CONNECTED,
    _CONF_GAS,
    _CONF_HOT,
    _CONF_LIGHT,
    _CONF_NOT_LOCKED,
    _CONF_MOIST,
    _CONF_MOTION,
    _CONF_MOVING,
    _CONF_OCCUPIED,
    _CONF_OPENED,
    _CONF_PLUGGED_IN,
    _CONF_POWERED,
    _CONF_PRESENT,
    _CONF_PROBLEM,
    _CONF_RUNNING,
    _CONF_SMOKE,
    _CONF_SOUND,
    _CONF_UNSAFE,
    _CONF_UPDATE,
    _CONF_VIBRATION,
    _CONF_TAMPERED,
    core.Toggle.CONF_TURNED_ON,
]

_TURNED_OFF: typing.Final = [
    _CONF_NOT_BAT_LOW,
    _CONF_NOT_CHARGING,
    _CONF_NOT_COLD,
    _CONF_NOT_CONNECTED,
    _CONF_NOT_HOT,
    _CONF_LOCKED,
    _CONF_NOT_MOIST,
    _CONF_NOT_MOVING,
    _CONF_NOT_OCCUPIED,
    _CONF_NOT_OPENED,
    _CONF_NOT_PLUGGED_IN,
    _CONF_NOT_POWERED,
    _CONF_NOT_PRESENT,
    _CONF_NOT_TAMPERED,
    _CONF_NOT_UNSAFE,
    _CONF_NO_CO,
    _CONF_NO_GAS,
    _CONF_NO_LIGHT,
    _CONF_NO_MOTION,
    _CONF_NO_PROBLEM,
    _CONF_NOT_RUNNING,
    _CONF_NO_SMOKE,
    _CONF_NO_SOUND,
    _CONF_NO_UPDATE,
    _CONF_NO_VIBRATION,
    core.Toggle.CONF_TURNED_OFF,
]


_ENTITY_TRIGGERS: typing.Final = {
    core.BinarySensor.DeviceClass.BATTERY: [
        {core.Const.CONF_TYPE: _CONF_BAT_LOW},
        {core.Const.CONF_TYPE: _CONF_NOT_BAT_LOW},
    ],
    core.BinarySensor.DeviceClass.BATTERY_CHARGING: [
        {core.Const.CONF_TYPE: _CONF_CHARGING},
        {core.Const.CONF_TYPE: _CONF_NOT_CHARGING},
    ],
    core.BinarySensor.DeviceClass.CO: [
        {core.Const.CONF_TYPE: _CONF_CO},
        {core.Const.CONF_TYPE: _CONF_NO_CO},
    ],
    core.BinarySensor.DeviceClass.COLD: [
        {core.Const.CONF_TYPE: _CONF_COLD},
        {core.Const.CONF_TYPE: _CONF_NOT_COLD},
    ],
    core.BinarySensor.DeviceClass.CONNECTIVITY: [
        {core.Const.CONF_TYPE: _CONF_CONNECTED},
        {core.Const.CONF_TYPE: _CONF_NOT_CONNECTED},
    ],
    core.BinarySensor.DeviceClass.DOOR: [
        {core.Const.CONF_TYPE: _CONF_OPENED},
        {core.Const.CONF_TYPE: _CONF_NOT_OPENED},
    ],
    core.BinarySensor.DeviceClass.GARAGE_DOOR: [
        {core.Const.CONF_TYPE: _CONF_OPENED},
        {core.Const.CONF_TYPE: _CONF_NOT_OPENED},
    ],
    core.BinarySensor.DeviceClass.GAS: [
        {core.Const.CONF_TYPE: _CONF_GAS},
        {core.Const.CONF_TYPE: _CONF_NO_GAS},
    ],
    core.BinarySensor.DeviceClass.HEAT: [
        {core.Const.CONF_TYPE: _CONF_HOT},
        {core.Const.CONF_TYPE: _CONF_NOT_HOT},
    ],
    core.BinarySensor.DeviceClass.LIGHT: [
        {core.Const.CONF_TYPE: _CONF_LIGHT},
        {core.Const.CONF_TYPE: _CONF_NO_LIGHT},
    ],
    core.BinarySensor.DeviceClass.LOCK: [
        {core.Const.CONF_TYPE: _CONF_LOCKED},
        {core.Const.CONF_TYPE: _CONF_NOT_LOCKED},
    ],
    core.BinarySensor.DeviceClass.MOISTURE: [
        {core.Const.CONF_TYPE: _CONF_MOIST},
        {core.Const.CONF_TYPE: _CONF_NOT_MOIST},
    ],
    core.BinarySensor.DeviceClass.MOTION: [
        {core.Const.CONF_TYPE: _CONF_MOTION},
        {core.Const.CONF_TYPE: _CONF_NO_MOTION},
    ],
    core.BinarySensor.DeviceClass.MOVING: [
        {core.Const.CONF_TYPE: _CONF_MOVING},
        {core.Const.CONF_TYPE: _CONF_NOT_MOVING},
    ],
    core.BinarySensor.DeviceClass.OCCUPANCY: [
        {core.Const.CONF_TYPE: _CONF_OCCUPIED},
        {core.Const.CONF_TYPE: _CONF_NOT_OCCUPIED},
    ],
    core.BinarySensor.DeviceClass.OPENING: [
        {core.Const.CONF_TYPE: _CONF_OPENED},
        {core.Const.CONF_TYPE: _CONF_NOT_OPENED},
    ],
    core.BinarySensor.DeviceClass.PLUG: [
        {core.Const.CONF_TYPE: _CONF_PLUGGED_IN},
        {core.Const.CONF_TYPE: _CONF_NOT_PLUGGED_IN},
    ],
    core.BinarySensor.DeviceClass.POWER: [
        {core.Const.CONF_TYPE: _CONF_POWERED},
        {core.Const.CONF_TYPE: _CONF_NOT_POWERED},
    ],
    core.BinarySensor.DeviceClass.PRESENCE: [
        {core.Const.CONF_TYPE: _CONF_PRESENT},
        {core.Const.CONF_TYPE: _CONF_NOT_PRESENT},
    ],
    core.BinarySensor.DeviceClass.PROBLEM: [
        {core.Const.CONF_TYPE: _CONF_PROBLEM},
        {core.Const.CONF_TYPE: _CONF_NO_PROBLEM},
    ],
    core.BinarySensor.DeviceClass.RUNNING: [
        {core.Const.CONF_TYPE: _CONF_RUNNING},
        {core.Const.CONF_TYPE: _CONF_NOT_RUNNING},
    ],
    core.BinarySensor.DeviceClass.SAFETY: [
        {core.Const.CONF_TYPE: _CONF_UNSAFE},
        {core.Const.CONF_TYPE: _CONF_NOT_UNSAFE},
    ],
    core.BinarySensor.DeviceClass.SMOKE: [
        {core.Const.CONF_TYPE: _CONF_SMOKE},
        {core.Const.CONF_TYPE: _CONF_NO_SMOKE},
    ],
    core.BinarySensor.DeviceClass.SOUND: [
        {core.Const.CONF_TYPE: _CONF_SOUND},
        {core.Const.CONF_TYPE: _CONF_NO_SOUND},
    ],
    core.BinarySensor.DeviceClass.UPDATE: [
        {core.Const.CONF_TYPE: _CONF_UPDATE},
        {core.Const.CONF_TYPE: _CONF_NO_UPDATE},
    ],
    core.BinarySensor.DeviceClass.TAMPER: [
        {core.Const.CONF_TYPE: _CONF_TAMPERED},
        {core.Const.CONF_TYPE: _CONF_NOT_TAMPERED},
    ],
    core.BinarySensor.DeviceClass.VIBRATION: [
        {core.Const.CONF_TYPE: _CONF_VIBRATION},
        {core.Const.CONF_TYPE: _CONF_NO_VIBRATION},
    ],
    core.BinarySensor.DeviceClass.WINDOW: [
        {core.Const.CONF_TYPE: _CONF_OPENED},
        {core.Const.CONF_TYPE: _CONF_NOT_OPENED},
    ],
    _DEVICE_CLASS_NONE: [
        {core.Const.CONF_TYPE: core.Toggle.CONF_TURNED_ON},
        {core.Const.CONF_TYPE: core.Toggle.CONF_TURNED_OFF},
    ],
}


_TRIGGER_SCHEMA: typing.Final = _cv.DEVICE_TRIGGER_BASE_SCHEMA.extend(
    {
        vol.Required(core.Const.CONF_ENTITY_ID): _cv.entity_id,
        vol.Required(core.Const.CONF_TYPE): vol.In(_TURNED_OFF + _TURNED_ON),
        vol.Optional(core.Const.CONF_FOR): _cv.positive_time_period_dict,
    }
)


# pylint: disable=unused-variable
class BinarySensorComponent(
    core.SmartHomeControllerComponent,
    core.ConditionPlatform,
    core.GroupPlatform,
    core.SignificantChangePlatform,
    core.TriggerPlatform,
):
    """Component to interface with binary sensors."""

    def __init__(self, path: typing.Iterable[str]):
        super().__init__(path)
        self._component: core.EntityComponent = None
        self._supported_platforms = frozenset(
            [
                core.Platform.CONDITION,
                core.Platform.GROUP,
                core.Platform.SIGNIFICANT_CHANGE,
                core.Platform.TRIGGER,
            ]
        )

    @property
    def entity_component(self) -> core.EntityComponent:
        return self._component

    @property
    def scan_interval(self) -> dt.timedelta:
        return dt.timedelta(seconds=30)

    async def async_setup(self, config: core.ConfigType) -> bool:
        """Track states and offer events for binary sensors."""
        if not await super().async_setup(config):
            return False

        component = core.EntityComponent(
            logging.getLogger(__name__), self.domain, self._shc, self.scan_interval
        )

        self._component = component
        await component.async_setup(config)
        return True

    async def async_setup_entry(self, entry: core.ConfigEntry) -> bool:
        """Set up a config entry."""
        component = self._component
        return await component.async_setup_entry(entry)

    async def async_remove_entry(self, entry: core.ConfigEntry) -> None:
        """Unload a config entry."""
        component = self._component
        return await component.async_unload_entry(entry)

    async def async_get_conditions(
        self, device_id: str
    ) -> list[dict[str, typing.Any]] | typing.Awaitable[list[dict[str, typing.Any]]]:
        """List device conditions."""
        conditions: list[dict[str, str]] = []
        entity_registry = self.controller.entity_registry
        domain = self.domain
        entries = [
            entry
            for entry in entity_registry.async_entries_for_device(device_id)
            if entry.domain == domain
        ]

        for entry in entries:
            device_class = (
                entity_registry.get_device_class(entry.entity_id) or _DEVICE_CLASS_NONE
            )

            templates = _ENTITY_CONDITIONS.get(
                device_class, _ENTITY_CONDITIONS[_DEVICE_CLASS_NONE]
            )

            conditions.extend(
                {
                    **template,
                    "condition": "device",
                    "device_id": device_id,
                    "entity_id": entry.entity_id,
                    "domain": domain,
                }
                for template in templates
            )

        return conditions

    @property
    def condition_schema(self) -> typing.Callable[[core.ConfigType], core.ConfigType]:
        return _CONDITION_SCHEMA

    async def async_condition_from_config(
        self, config: core.ConfigType
    ) -> core.ConditionCheckerType:
        """Evaluate state based on configuration."""
        condition_type = config[core.Const.CONF_TYPE]
        if condition_type in _IS_ON:
            stat = "on"
        else:
            stat = "off"
        state_config = {
            core.Const.CONF_CONDITION: "state",
            core.Const.CONF_ENTITY_ID: config[core.Const.CONF_ENTITY_ID],
            core.Const.CONF_STATE: stat,
        }
        if core.Const.CONF_FOR in config:
            state_config[core.Const.CONF_FOR] = config[core.Const.CONF_FOR]

        state_config = _cv.state_condition_schema(state_config)
        state_config = self.state_validate_config(state_config)

        return self.state_from_config(state_config)

    async def async_get_condition_capabilities(
        self, _config: core.ConfigType
    ) -> dict[str, vol.Schema] | typing.Awaitable[dict[str, vol.Schema]]:
        """List condition capabilities."""
        return {
            "extra_fields": vol.Schema(
                {vol.Optional(core.Const.CONF_FOR): _cv.positive_time_period_dict}
            )
        }

    def _is_on(self, entity_id: str) -> bool:
        state = self.controller.states.get(entity_id)
        if state is None:
            return False
        return state.state in _TURNED_ON

    def async_describe_on_off_states(
        self, registry: core.GroupIntegrationRegistry
    ) -> None:
        """Describe group on off states."""
        registry.on_off_states({core.Const.STATE_ON}, core.Const.STATE_OFF)

    def check_significant_change(
        self,
        old_state: str,
        _old_attrs: dict,
        new_state: str,
        _new_attrs: dict,
        **_kwargs: typing.Any,
    ) -> bool:
        """Test if state significantly changed."""
        if old_state != new_state:
            return True

        return False

    @property
    def trigger_schema(self) -> typing.Callable[[core.ConfigType], core.ConfigType]:
        return _TRIGGER_SCHEMA

    async def async_attach_trigger(
        self,
        config: core.ConfigType,
        action: core.TriggerActionType,
        trigger_info: core.TriggerInfo,
    ) -> core.CallbackType:
        """Listen for state changes based on configuration."""
        trigger_type = config[core.Const.CONF_TYPE]
        if trigger_type in _TURNED_ON:
            to_state = "on"
        else:
            to_state = "off"

        state_config = {
            core.Const.CONF_PLATFORM: "state",
            core.Const.CONF_ENTITY_ID: config[core.Const.CONF_ENTITY_ID],
            core.Const.CONF_TO: to_state,
        }
        if core.Const.CONF_FOR in config:
            state_config[core.Const.CONF_FOR] = config[core.Const.CONF_FOR]

        state_config = await core.Trigger.async_validate_trigger_config(state_config)
        return await core.Trigger.async_attach_state_trigger(
            self._shc, state_config, action, trigger_info, platform_type="device"
        )

    async def async_get_triggers(self, device_id: str) -> list[dict[str, str]]:
        """List device triggers."""
        triggers: list[dict[str, str]] = []
        entity_registry = self.controller.entity_registry

        entries = [
            entry
            for entry in entity_registry.async_entries_for_device(device_id)
            if entry.domain == self.domain
        ]

        for entry in entries:
            device_class = entry.device_class or _DEVICE_CLASS_NONE

            templates = _ENTITY_TRIGGERS.get(
                device_class, _ENTITY_TRIGGERS[_DEVICE_CLASS_NONE]
            )

            triggers.extend(
                {
                    **automation,
                    "platform": "device",
                    "device_id": device_id,
                    "entity_id": entry.entity_id,
                    "domain": self.domain,
                }
                for automation in templates
            )

        return triggers

    async def async_get_trigger_capabilities(
        self, _config: core.ConfigType
    ) -> dict[str, vol.Schema]:
        """List trigger capabilities."""
        return {
            "extra_fields": vol.Schema(
                {vol.Optional(core.Const.CONF_FOR): _cv.positive_time_period_dict}
            )
        }
