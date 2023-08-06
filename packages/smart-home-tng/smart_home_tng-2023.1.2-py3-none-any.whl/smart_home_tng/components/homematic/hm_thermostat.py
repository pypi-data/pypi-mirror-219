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

from ... import core
from .const import Const
from .hm_device import HMDevice


if not typing.TYPE_CHECKING:

    class HomematicIntegration:
        pass


if typing.TYPE_CHECKING:
    from .homematic_integration import HomematicIntegration


_HM_TEMP_MAP: typing.Final = ["ACTUAL_TEMPERATURE", "TEMPERATURE"]

_HM_HUMI_MAP: typing.Final = ["ACTUAL_HUMIDITY", "HUMIDITY"]

_HM_PRESET_MAP: typing.Final = {
    "BOOST_MODE": core.Climate.PRESET_BOOST,
    "COMFORT_MODE": core.Climate.PRESET_COMFORT,
    "LOWERING_MODE": core.Climate.PRESET_ECO,
}

_HM_CONTROL_MODE: typing.Final = "CONTROL_MODE"
_HMIP_CONTROL_MODE: typing.Final = "SET_POINT_MODE"


# pylint: disable=unused-variable
class HMThermostat(HMDevice, core.Climate.Entity):
    """Representation of a Homematic thermostat."""

    _attr_supported_features = (
        core.Climate.EntityFeature.TARGET_TEMPERATURE
        | core.Climate.EntityFeature.PRESET_MODE
    )
    _attr_temperature_unit = core.Const.UnitOfTemperature.CELSIUS

    @property
    def hvac_mode(self) -> core.Climate.HVACMode:
        """Return hvac operation ie. heat, cool mode.

        Need to be one of HVAC_MODE_*.
        """
        if self.target_temperature <= self._hmdevice.OFF_VALUE + 0.5:
            return core.Climate.HVACMode.OFF
        if "MANU_MODE" in self._hmdevice.ACTIONNODE:
            if self._hm_control_mode == self._hmdevice.MANU_MODE:
                return core.Climate.HVACMode.HEAT
            return core.Climate.HVACMode.AUTO

        # Simple devices
        if self._data.get("BOOST_MODE"):
            return core.Climate.HVACMode.AUTO
        return core.Climate.HVACMode.HEAT

    @property
    def hvac_modes(self) -> list[core.Climate.HVACMode]:
        """Return the list of available hvac operation modes.

        Need to be a subset of HVAC_MODES.
        """
        if "AUTO_MODE" in self._hmdevice.ACTIONNODE:
            return [
                core.Climate.HVACMode.AUTO,
                core.Climate.HVACMode.HEAT,
                core.Climate.HVACMode.OFF,
            ]
        return [core.Climate.HVACMode.HEAT, core.Climate.HVACMode.OFF]

    @property
    def preset_mode(self):
        """Return the current preset mode, e.g., home, away, temp."""
        if self._data.get("BOOST_MODE", False):
            return "boost"

        if not self._hm_control_mode:
            return core.Climate.PRESET_NONE

        mode = Const.HM_ATTRIBUTE_SUPPORT[_HM_CONTROL_MODE][1][self._hm_control_mode]
        mode = mode.lower()

        # Filter HVAC states
        if mode not in (core.Climate.HVACMode.AUTO, core.Climate.HVACMode.HEAT):
            return core.Climate.PRESET_NONE
        return mode

    @property
    def preset_modes(self):
        """Return a list of available preset modes."""
        preset_modes = []
        for mode in self._hmdevice.ACTIONNODE:
            if mode in _HM_PRESET_MAP:
                preset_modes.append(_HM_PRESET_MAP[mode])
        return preset_modes

    @property
    def current_humidity(self):
        """Return the current humidity."""
        for node in _HM_HUMI_MAP:
            if node in self._data:
                return self._data[node]
        return None

    @property
    def current_temperature(self):
        """Return the current temperature."""
        for node in _HM_TEMP_MAP:
            if node in self._data:
                return self._data[node]
        return None

    @property
    def target_temperature(self):
        """Return the target temperature."""
        return self._data.get(self._state)

    def set_temperature(self, **kwargs: typing.Any) -> None:
        """Set new target temperature."""
        if (temperature := kwargs.get(core.Const.ATTR_TEMPERATURE)) is None:
            return

        self._hmdevice.writeNodeData(self._state, float(temperature))

    def set_hvac_mode(self, hvac_mode: core.Climate.HVACMode) -> None:
        """Set new target hvac mode."""
        if hvac_mode == core.Climate.HVACMode.AUTO:
            self._hmdevice.MODE = self._hmdevice.AUTO_MODE
        elif hvac_mode == core.Climate.HVACMode.HEAT:
            self._hmdevice.MODE = self._hmdevice.MANU_MODE
        elif hvac_mode == core.Climate.HVACMode.OFF:
            self._hmdevice.turnoff()

    def set_preset_mode(self, preset_mode: str) -> None:
        """Set new preset mode."""
        if preset_mode == core.Climate.PRESET_BOOST:
            self._hmdevice.MODE = self._hmdevice.BOOST_MODE
        elif preset_mode == core.Climate.PRESET_COMFORT:
            self._hmdevice.MODE = self._hmdevice.COMFORT_MODE
        elif preset_mode == core.Climate.PRESET_ECO:
            self._hmdevice.MODE = self._hmdevice.LOWERING_MODE

    @property
    def min_temp(self):
        """Return the minimum temperature."""
        return 4.5

    @property
    def max_temp(self):
        """Return the maximum temperature."""
        return 30.5

    @property
    def target_temperature_step(self):
        """Return the supported step of target temperature."""
        return 0.5

    @property
    def _hm_control_mode(self):
        """Return Control mode."""
        if _HMIP_CONTROL_MODE in self._data:
            return self._data[_HMIP_CONTROL_MODE]

        # Homematic
        return self._data.get("CONTROL_MODE")

    def _init_data_struct(self):
        """Generate a data dict (self._data) from the Homematic metadata."""
        self._state = next(iter(self._hmdevice.WRITENODE.keys()))
        self._data[self._state] = None

        if (
            _HM_CONTROL_MODE in self._hmdevice.ATTRIBUTENODE
            or _HMIP_CONTROL_MODE in self._hmdevice.ATTRIBUTENODE
        ):
            self._data[_HM_CONTROL_MODE] = None

        for node in self._hmdevice.SENSORNODE.keys():
            self._data[node] = None


async def async_setup_climates(
    comp: HomematicIntegration,
    add_entities: core.AddEntitiesCallback,
    discovery_info: core.DiscoveryInfoType = None,
) -> None:
    """Set up the Homematic thermostat platform."""
    if discovery_info is None:
        return

    devices = []
    for conf in discovery_info[Const.ATTR_DISCOVER_DEVICES]:
        new_device = HMThermostat(comp, conf)
        devices.append(new_device)

    add_entities(devices, True)
